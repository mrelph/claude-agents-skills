#!/usr/bin/env python3
"""
RSU Calculator - Comprehensive tool for RSU cost basis, withholding, lot tracking, and tax reporting.

Features:
- Cost basis calculation from vesting records
- Withholding shortfall estimation
- Multi-lot tracking with FIFO/specific ID
- Capital gains calculation for sales
- Form 8949 adjustment generation
- CSV/JSON input support for statement imports
"""

import argparse
import json
import csv
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP


# 2024 Tax rates for withholding calculations
FEDERAL_SUPPLEMENTAL_RATE = 0.22
FEDERAL_SUPPLEMENTAL_RATE_OVER_1M = 0.37
SOCIAL_SECURITY_RATE = 0.062
SOCIAL_SECURITY_WAGE_BASE = 168600
MEDICARE_RATE = 0.0145
MEDICARE_ADDITIONAL_RATE = 0.009
MEDICARE_ADDITIONAL_THRESHOLD = {"single": 200000, "married_jointly": 250000, "married_separately": 125000}

# Federal income tax brackets for estimating actual tax
TAX_BRACKETS = {
    "single": [(11600, 0.10), (47150, 0.12), (100525, 0.22), (191950, 0.24), (243725, 0.32), (609350, 0.35), (float('inf'), 0.37)],
    "married_jointly": [(23200, 0.10), (94300, 0.12), (201050, 0.22), (383900, 0.24), (487450, 0.32), (731200, 0.35), (float('inf'), 0.37)],
    "married_separately": [(11600, 0.10), (47150, 0.12), (100525, 0.22), (191950, 0.24), (243725, 0.32), (365600, 0.35), (float('inf'), 0.37)],
    "head_of_household": [(16550, 0.10), (63100, 0.12), (100500, 0.22), (191950, 0.24), (243700, 0.32), (609350, 0.35), (float('inf'), 0.37)]
}

STANDARD_DEDUCTIONS = {"single": 14600, "married_jointly": 29200, "married_separately": 14600, "head_of_household": 21900}


@dataclass
class VestingLot:
    """Represents a single RSU vesting lot."""
    vesting_date: str
    shares_vested: float
    fmv_at_vesting: float
    shares_withheld: float = 0
    net_shares: float = 0
    grant_date: Optional[str] = None
    grant_id: Optional[str] = None

    def __post_init__(self):
        if self.net_shares == 0:
            self.net_shares = self.shares_vested - self.shares_withheld
        self.cost_basis_per_share = self.fmv_at_vesting
        self.total_cost_basis = self.fmv_at_vesting * self.shares_vested
        self.vesting_income = self.total_cost_basis
        self.shares_remaining = self.net_shares


@dataclass
class SaleLot:
    """Represents a sale transaction."""
    sale_date: str
    shares_sold: float
    sale_price: float
    from_vesting_date: Optional[str] = None
    reported_basis_1099b: float = 0

    def __post_init__(self):
        self.proceeds = self.shares_sold * self.sale_price


@dataclass
class TaxLotResult:
    """Result of selling from a specific tax lot."""
    vesting_date: str
    shares_sold: float
    cost_basis_per_share: float
    sale_price: float
    proceeds: float
    cost_basis: float
    gain_loss: float
    holding_period: str  # "short_term" or "long_term"
    holding_days: int
    basis_adjustment_needed: bool
    reported_basis: float
    correct_basis: float
    adjustment_amount: float
    form_8949_code: str


def parse_date(date_str: str) -> datetime:
    """Parse date string in various formats."""
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}")


def calculate_holding_period(vesting_date: str, sale_date: str) -> Tuple[str, int]:
    """Calculate holding period and classification."""
    vesting = parse_date(vesting_date)
    sale = parse_date(sale_date)
    days = (sale - vesting).days

    # Long-term if held more than 1 year (365 days)
    if days > 365:
        return "long_term", days
    return "short_term", days


def calculate_marginal_rate(taxable_income: float, filing_status: str) -> float:
    """Get marginal tax rate for given income and filing status."""
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["single"])
    for bracket_top, rate in brackets:
        if taxable_income <= bracket_top:
            return rate
    return brackets[-1][1]


def calculate_withholding_estimate(
    vesting_income: float,
    ytd_wages: float = 0,
    filing_status: str = "single",
    state_rate: float = 0.05
) -> Dict:
    """
    Estimate withholding on RSU vesting and compare to actual tax owed.

    Returns dict with typical withholding vs estimated actual tax.
    """
    # Typical employer withholding
    if vesting_income > 1000000:
        federal_withholding_rate = FEDERAL_SUPPLEMENTAL_RATE_OVER_1M
    else:
        federal_withholding_rate = FEDERAL_SUPPLEMENTAL_RATE

    federal_withheld = vesting_income * federal_withholding_rate

    # Social Security (check if over wage base)
    remaining_ss_wages = max(0, SOCIAL_SECURITY_WAGE_BASE - ytd_wages)
    ss_wages = min(vesting_income, remaining_ss_wages)
    ss_withheld = ss_wages * SOCIAL_SECURITY_RATE

    # Medicare
    medicare_withheld = vesting_income * MEDICARE_RATE

    # Additional Medicare (typically not withheld correctly)
    medicare_threshold = MEDICARE_ADDITIONAL_THRESHOLD.get(filing_status, 200000)
    if ytd_wages + vesting_income > medicare_threshold:
        additional_medicare_income = min(vesting_income, ytd_wages + vesting_income - medicare_threshold)
        additional_medicare = additional_medicare_income * MEDICARE_ADDITIONAL_RATE
    else:
        additional_medicare = 0

    # State withholding (simplified)
    state_withheld = vesting_income * state_rate

    total_withheld = federal_withheld + ss_withheld + medicare_withheld + state_withheld

    # Estimate actual tax (simplified - assumes this income on top of other income)
    total_income = ytd_wages + vesting_income
    standard_deduction = STANDARD_DEDUCTIONS.get(filing_status, 14600)
    taxable_income = max(0, total_income - standard_deduction)

    marginal_rate = calculate_marginal_rate(taxable_income, filing_status)
    estimated_federal_tax = vesting_income * marginal_rate
    estimated_state_tax = vesting_income * state_rate
    estimated_total = estimated_federal_tax + ss_withheld + medicare_withheld + additional_medicare + estimated_state_tax

    shortfall = estimated_total - total_withheld

    return {
        "vesting_income": round(vesting_income, 2),
        "withholding": {
            "federal": round(federal_withheld, 2),
            "federal_rate": federal_withholding_rate,
            "social_security": round(ss_withheld, 2),
            "medicare": round(medicare_withheld, 2),
            "state": round(state_withheld, 2),
            "total_withheld": round(total_withheld, 2)
        },
        "estimated_actual_tax": {
            "marginal_bracket": marginal_rate,
            "federal": round(estimated_federal_tax, 2),
            "social_security": round(ss_withheld, 2),
            "medicare": round(medicare_withheld + additional_medicare, 2),
            "additional_medicare": round(additional_medicare, 2),
            "state": round(estimated_state_tax, 2),
            "total": round(estimated_total, 2)
        },
        "shortfall": round(shortfall, 2),
        "shortfall_percent": round((shortfall / vesting_income) * 100, 1) if vesting_income > 0 else 0
    }


def calculate_lot_sale(
    lot: VestingLot,
    shares_to_sell: float,
    sale_price: float,
    sale_date: str,
    reported_basis_1099b: float = 0
) -> TaxLotResult:
    """Calculate tax implications of selling shares from a specific lot."""

    holding_period, holding_days = calculate_holding_period(lot.vesting_date, sale_date)

    proceeds = shares_to_sell * sale_price
    cost_basis = shares_to_sell * lot.cost_basis_per_share
    gain_loss = proceeds - cost_basis

    # Check if basis adjustment needed
    basis_adjustment_needed = abs(reported_basis_1099b - cost_basis) > 0.01 if reported_basis_1099b else True
    adjustment_amount = cost_basis - reported_basis_1099b if basis_adjustment_needed else 0
    form_8949_code = "B" if basis_adjustment_needed else ""

    return TaxLotResult(
        vesting_date=lot.vesting_date,
        shares_sold=shares_to_sell,
        cost_basis_per_share=lot.cost_basis_per_share,
        sale_price=sale_price,
        proceeds=round(proceeds, 2),
        cost_basis=round(cost_basis, 2),
        gain_loss=round(gain_loss, 2),
        holding_period=holding_period,
        holding_days=holding_days,
        basis_adjustment_needed=basis_adjustment_needed,
        reported_basis=reported_basis_1099b,
        correct_basis=round(cost_basis, 2),
        adjustment_amount=round(adjustment_amount, 2),
        form_8949_code=form_8949_code
    )


def process_sale_fifo(lots: List[VestingLot], sale: SaleLot) -> List[TaxLotResult]:
    """Process a sale using FIFO (First In, First Out) method."""
    results = []
    shares_remaining = sale.shares_sold

    # Sort lots by vesting date (oldest first)
    sorted_lots = sorted(lots, key=lambda x: parse_date(x.vesting_date))

    for lot in sorted_lots:
        if shares_remaining <= 0:
            break

        if lot.shares_remaining <= 0:
            continue

        shares_from_lot = min(shares_remaining, lot.shares_remaining)

        # Allocate reported basis proportionally if provided
        reported_basis = 0
        if sale.reported_basis_1099b and sale.shares_sold > 0:
            reported_basis = (shares_from_lot / sale.shares_sold) * sale.reported_basis_1099b

        result = calculate_lot_sale(
            lot=lot,
            shares_to_sell=shares_from_lot,
            sale_price=sale.sale_price,
            sale_date=sale.sale_date,
            reported_basis_1099b=reported_basis
        )
        results.append(result)

        lot.shares_remaining -= shares_from_lot
        shares_remaining -= shares_from_lot

    if shares_remaining > 0.001:
        print(f"Warning: Not enough shares in lots to cover sale. {shares_remaining:.4f} shares unaccounted for.", file=sys.stderr)

    return results


def process_sale_specific_id(lots: List[VestingLot], sale: SaleLot) -> List[TaxLotResult]:
    """Process a sale from a specific vesting lot."""
    results = []

    # Find the matching lot
    matching_lot = None
    for lot in lots:
        if lot.vesting_date == sale.from_vesting_date and lot.shares_remaining >= sale.shares_sold:
            matching_lot = lot
            break

    if not matching_lot:
        # Fall back to FIFO if specific lot not found or insufficient shares
        print(f"Warning: Specific lot {sale.from_vesting_date} not found or insufficient shares. Using FIFO.", file=sys.stderr)
        return process_sale_fifo(lots, sale)

    result = calculate_lot_sale(
        lot=matching_lot,
        shares_to_sell=sale.shares_sold,
        sale_price=sale.sale_price,
        sale_date=sale.sale_date,
        reported_basis_1099b=sale.reported_basis_1099b
    )
    results.append(result)
    matching_lot.shares_remaining -= sale.shares_sold

    return results


def load_vesting_data(file_path: str) -> List[VestingLot]:
    """Load vesting data from JSON or CSV file."""
    lots = []

    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            vesting_records = data.get('vestings', data.get('vesting_lots', data))
            if isinstance(vesting_records, list):
                for record in vesting_records:
                    lots.append(VestingLot(**record))

    elif file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lot = VestingLot(
                    vesting_date=row.get('vesting_date', row.get('Vesting Date', row.get('Date Acquired', ''))),
                    shares_vested=float(row.get('shares_vested', row.get('Shares Vested', row.get('Quantity', 0)))),
                    fmv_at_vesting=float(row.get('fmv_at_vesting', row.get('FMV', row.get('Fair Market Value', row.get('Price', 0))))),
                    shares_withheld=float(row.get('shares_withheld', row.get('Shares Withheld', 0))),
                    grant_date=row.get('grant_date', row.get('Grant Date', None)),
                    grant_id=row.get('grant_id', row.get('Grant ID', None))
                )
                lots.append(lot)

    return lots


def load_sales_data(file_path: str) -> List[SaleLot]:
    """Load sales data from JSON or CSV file."""
    sales = []

    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            sale_records = data.get('sales', data)
            if isinstance(sale_records, list):
                for record in sale_records:
                    sales.append(SaleLot(**record))

    elif file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sale = SaleLot(
                    sale_date=row.get('sale_date', row.get('Sale Date', row.get('Date Sold', ''))),
                    shares_sold=float(row.get('shares_sold', row.get('Shares Sold', row.get('Quantity', 0)))),
                    sale_price=float(row.get('sale_price', row.get('Sale Price', row.get('Price', 0)))),
                    from_vesting_date=row.get('from_vesting_date', row.get('Acquisition Date', None)),
                    reported_basis_1099b=float(row.get('reported_basis_1099b', row.get('Cost Basis', row.get('Reported Basis', 0))))
                )
                sales.append(sale)

    return sales


def generate_form_8949_entry(result: TaxLotResult, description: str = "RSU shares") -> Dict:
    """Generate Form 8949 entry for a sale."""
    return {
        "description": description,
        "date_acquired": result.vesting_date,
        "date_sold": result.vesting_date,  # Will be overwritten
        "proceeds": result.proceeds,
        "cost_basis": result.correct_basis,
        "adjustment_code": result.form_8949_code,
        "adjustment_amount": result.adjustment_amount,
        "gain_loss": result.gain_loss,
        "holding_period": result.holding_period
    }


def print_lot_summary(lots: List[VestingLot], output_format: str = "text"):
    """Print summary of all vesting lots."""
    total_shares = sum(lot.net_shares for lot in lots)
    total_remaining = sum(lot.shares_remaining for lot in lots)
    total_basis = sum(lot.shares_remaining * lot.cost_basis_per_share for lot in lots)

    if output_format == "json":
        summary = {
            "lots": [asdict(lot) for lot in lots],
            "totals": {
                "total_lots": len(lots),
                "total_net_shares": total_shares,
                "total_remaining_shares": total_remaining,
                "total_cost_basis": round(total_basis, 2)
            }
        }
        print(json.dumps(summary, indent=2))
    else:
        print("\n" + "="*80)
        print("RSU VESTING LOT SUMMARY")
        print("="*80)
        print(f"\n{'Vesting Date':<14} {'Shares Vested':>14} {'FMV':>10} {'Withheld':>10} {'Net Shares':>12} {'Remaining':>10} {'Basis/Share':>12}")
        print("-"*80)

        for lot in sorted(lots, key=lambda x: parse_date(x.vesting_date)):
            print(f"{lot.vesting_date:<14} {lot.shares_vested:>14,.2f} ${lot.fmv_at_vesting:>8,.2f} {lot.shares_withheld:>10,.2f} {lot.net_shares:>12,.2f} {lot.shares_remaining:>10,.2f} ${lot.cost_basis_per_share:>10,.2f}")

        print("-"*80)
        print(f"{'TOTALS':<14} {'':<14} {'':<10} {'':<10} {total_shares:>12,.2f} {total_remaining:>10,.2f} ${total_basis:>10,.2f}")
        print("="*80 + "\n")


def print_sale_results(results: List[TaxLotResult], sale: SaleLot, output_format: str = "text"):
    """Print sale calculation results."""
    total_proceeds = sum(r.proceeds for r in results)
    total_basis = sum(r.correct_basis for r in results)
    total_gain = sum(r.gain_loss for r in results)
    st_gain = sum(r.gain_loss for r in results if r.holding_period == "short_term")
    lt_gain = sum(r.gain_loss for r in results if r.holding_period == "long_term")

    if output_format == "json":
        output = {
            "sale": {
                "sale_date": sale.sale_date,
                "shares_sold": sale.shares_sold,
                "sale_price": sale.sale_price,
                "total_proceeds": total_proceeds
            },
            "lot_breakdown": [asdict(r) for r in results],
            "totals": {
                "total_proceeds": round(total_proceeds, 2),
                "total_cost_basis": round(total_basis, 2),
                "total_gain_loss": round(total_gain, 2),
                "short_term_gain": round(st_gain, 2),
                "long_term_gain": round(lt_gain, 2)
            },
            "form_8949_entries": [generate_form_8949_entry(r) for r in results]
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "="*80)
        print("RSU SALE CALCULATION")
        print("="*80)
        print(f"\nSale Date: {sale.sale_date}")
        print(f"Shares Sold: {sale.shares_sold:,.2f}")
        print(f"Sale Price: ${sale.sale_price:,.2f}")
        print(f"Total Proceeds: ${total_proceeds:,.2f}")

        print(f"\n{'Vesting Date':<14} {'Shares':>10} {'Basis/Sh':>10} {'Basis':>12} {'Proceeds':>12} {'Gain/Loss':>12} {'Type':>12} {'Days':>6}")
        print("-"*80)

        for r in results:
            gain_type = "Long-term" if r.holding_period == "long_term" else "Short-term"
            print(f"{r.vesting_date:<14} {r.shares_sold:>10,.2f} ${r.cost_basis_per_share:>8,.2f} ${r.cost_basis:>10,.2f} ${r.proceeds:>10,.2f} ${r.gain_loss:>10,.2f} {gain_type:>12} {r.holding_days:>6}")

        print("-"*80)
        print(f"{'TOTALS':<14} {sale.shares_sold:>10,.2f} {'':<10} ${total_basis:>10,.2f} ${total_proceeds:>10,.2f} ${total_gain:>10,.2f}")

        if st_gain != 0 or lt_gain != 0:
            print(f"\n  Short-term gain/loss: ${st_gain:,.2f}")
            print(f"  Long-term gain/loss:  ${lt_gain:,.2f}")

        # Form 8949 guidance
        any_adjustment = any(r.basis_adjustment_needed for r in results)
        if any_adjustment:
            print("\n" + "-"*80)
            print("FORM 8949 ADJUSTMENT REQUIRED")
            print("-"*80)
            print("\nThe 1099-B cost basis is incorrect. You must report the correct basis on Form 8949.")
            print("\nFor each lot with incorrect basis:")
            print("  - Column (e): Enter your CORRECT cost basis")
            print("  - Column (f): Enter code 'B' (basis reported incorrectly)")
            print("  - Column (g): Enter the adjustment amount")

            for r in results:
                if r.basis_adjustment_needed:
                    print(f"\n  Lot from {r.vesting_date}:")
                    print(f"    1099-B reported basis: ${r.reported_basis:,.2f}")
                    print(f"    Correct basis:         ${r.correct_basis:,.2f}")
                    print(f"    Adjustment amount:     ${r.adjustment_amount:,.2f}")

        print("="*80 + "\n")


def print_withholding_analysis(analysis: Dict, output_format: str = "text"):
    """Print withholding analysis results."""
    if output_format == "json":
        print(json.dumps(analysis, indent=2))
    else:
        print("\n" + "="*80)
        print("RSU WITHHOLDING ANALYSIS")
        print("="*80)
        print(f"\nVesting Income: ${analysis['vesting_income']:,.2f}")

        print("\nTYPICAL EMPLOYER WITHHOLDING:")
        w = analysis['withholding']
        print(f"  Federal ({w['federal_rate']*100:.0f}%):       ${w['federal']:,.2f}")
        print(f"  Social Security:          ${w['social_security']:,.2f}")
        print(f"  Medicare:                 ${w['medicare']:,.2f}")
        print(f"  State:                    ${w['state']:,.2f}")
        print(f"  ----------------------------------------")
        print(f"  Total Withheld:           ${w['total_withheld']:,.2f}")

        print("\nESTIMATED ACTUAL TAX OWED:")
        e = analysis['estimated_actual_tax']
        print(f"  Federal ({e['marginal_bracket']*100:.0f}% bracket):  ${e['federal']:,.2f}")
        print(f"  Social Security:          ${e['social_security']:,.2f}")
        print(f"  Medicare:                 ${e['medicare']:,.2f}")
        if e['additional_medicare'] > 0:
            print(f"    (includes additional)   ${e['additional_medicare']:,.2f}")
        print(f"  State:                    ${e['state']:,.2f}")
        print(f"  ----------------------------------------")
        print(f"  Total Estimated Tax:      ${e['total']:,.2f}")

        shortfall = analysis['shortfall']
        if shortfall > 0:
            print(f"\n*** WITHHOLDING SHORTFALL: ${shortfall:,.2f} ({analysis['shortfall_percent']:.1f}%) ***")
            print("\nACTION NEEDED:")
            print("  - Increase W-4 withholding at day job, OR")
            print("  - Make estimated tax payment (Form 1040-ES), OR")
            print("  - Set aside funds for tax payment at filing")
        elif shortfall < 0:
            print(f"\n  Potential overwithholding: ${-shortfall:,.2f}")
        else:
            print("\n  Withholding appears adequate")

        print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="RSU Calculator - Cost basis, withholding, and tax calculations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate withholding shortfall
  python rsu_calculator.py withholding --vesting-income 50000 --ytd-wages 100000 --filing-status single

  # Load vesting lots from file and display summary
  python rsu_calculator.py lots --vesting-file vestings.csv

  # Calculate sale from lots
  python rsu_calculator.py sale --vesting-file vestings.csv --sale-date 2024-06-15 --shares 100 --sale-price 120

  # Process sales from file
  python rsu_calculator.py sale --vesting-file vestings.json --sales-file sales.json
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Withholding analysis subcommand
    withhold_parser = subparsers.add_parser("withholding", help="Analyze withholding adequacy")
    withhold_parser.add_argument("--vesting-income", type=float, required=True, help="RSU vesting income amount")
    withhold_parser.add_argument("--ytd-wages", type=float, default=0, help="Year-to-date wages before vesting")
    withhold_parser.add_argument("--filing-status", default="single", choices=list(TAX_BRACKETS.keys()), help="Filing status")
    withhold_parser.add_argument("--state-rate", type=float, default=0.05, help="State tax rate (decimal, e.g., 0.05 for 5%%)")
    withhold_parser.add_argument("--output-format", choices=["text", "json"], default="text")

    # Lot summary subcommand
    lots_parser = subparsers.add_parser("lots", help="Display vesting lot summary")
    lots_parser.add_argument("--vesting-file", required=True, help="CSV or JSON file with vesting data")
    lots_parser.add_argument("--output-format", choices=["text", "json"], default="text")

    # Sale calculation subcommand
    sale_parser = subparsers.add_parser("sale", help="Calculate sale tax implications")
    sale_parser.add_argument("--vesting-file", required=True, help="CSV or JSON file with vesting data")
    sale_parser.add_argument("--sales-file", help="CSV or JSON file with sales data")
    sale_parser.add_argument("--sale-date", help="Sale date (YYYY-MM-DD)")
    sale_parser.add_argument("--shares", type=float, help="Number of shares sold")
    sale_parser.add_argument("--sale-price", type=float, help="Sale price per share")
    sale_parser.add_argument("--from-vesting-date", help="Specific vesting lot to sell from (specific ID method)")
    sale_parser.add_argument("--reported-basis", type=float, default=0, help="Basis reported on 1099-B")
    sale_parser.add_argument("--method", choices=["fifo", "specific"], default="fifo", help="Lot selection method")
    sale_parser.add_argument("--output-format", choices=["text", "json"], default="text")

    # Basis calculation subcommand
    basis_parser = subparsers.add_parser("basis", help="Calculate cost basis for a single vesting")
    basis_parser.add_argument("--shares-vested", type=float, required=True, help="Number of shares vested")
    basis_parser.add_argument("--fmv", type=float, required=True, help="Fair market value at vesting")
    basis_parser.add_argument("--shares-withheld", type=float, default=0, help="Shares withheld for taxes")
    basis_parser.add_argument("--output-format", choices=["text", "json"], default="text")

    args = parser.parse_args()

    if args.command == "withholding":
        analysis = calculate_withholding_estimate(
            vesting_income=args.vesting_income,
            ytd_wages=args.ytd_wages,
            filing_status=args.filing_status,
            state_rate=args.state_rate
        )
        print_withholding_analysis(analysis, args.output_format)

    elif args.command == "lots":
        lots = load_vesting_data(args.vesting_file)
        print_lot_summary(lots, args.output_format)

    elif args.command == "sale":
        lots = load_vesting_data(args.vesting_file)

        if args.sales_file:
            sales = load_sales_data(args.sales_file)
            for sale in sales:
                if args.method == "specific" and sale.from_vesting_date:
                    results = process_sale_specific_id(lots, sale)
                else:
                    results = process_sale_fifo(lots, sale)
                print_sale_results(results, sale, args.output_format)
        elif args.sale_date and args.shares and args.sale_price:
            sale = SaleLot(
                sale_date=args.sale_date,
                shares_sold=args.shares,
                sale_price=args.sale_price,
                from_vesting_date=args.from_vesting_date,
                reported_basis_1099b=args.reported_basis
            )
            if args.method == "specific" and args.from_vesting_date:
                results = process_sale_specific_id(lots, sale)
            else:
                results = process_sale_fifo(lots, sale)
            print_sale_results(results, sale, args.output_format)
        else:
            print("Error: Either --sales-file or (--sale-date, --shares, --sale-price) required", file=sys.stderr)
            sys.exit(1)

    elif args.command == "basis":
        lot = VestingLot(
            vesting_date=datetime.now().strftime("%Y-%m-%d"),
            shares_vested=args.shares_vested,
            fmv_at_vesting=args.fmv,
            shares_withheld=args.shares_withheld
        )

        if args.output_format == "json":
            print(json.dumps({
                "shares_vested": lot.shares_vested,
                "fmv_at_vesting": lot.fmv_at_vesting,
                "shares_withheld": lot.shares_withheld,
                "net_shares": lot.net_shares,
                "cost_basis_per_share": lot.cost_basis_per_share,
                "total_cost_basis": lot.total_cost_basis,
                "vesting_income": lot.vesting_income
            }, indent=2))
        else:
            print("\n" + "="*60)
            print("RSU COST BASIS CALCULATION")
            print("="*60)
            print(f"\nShares Vested:        {lot.shares_vested:,.2f}")
            print(f"FMV at Vesting:       ${lot.fmv_at_vesting:,.2f}")
            print(f"Shares Withheld:      {lot.shares_withheld:,.2f}")
            print(f"Net Shares Received:  {lot.net_shares:,.2f}")
            print(f"\nCost Basis per Share: ${lot.cost_basis_per_share:,.2f}")
            print(f"Total Cost Basis:     ${lot.total_cost_basis:,.2f}")
            print(f"Vesting Income (W-2): ${lot.vesting_income:,.2f}")
            print("="*60 + "\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
