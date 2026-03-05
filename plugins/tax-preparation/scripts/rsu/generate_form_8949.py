#!/usr/bin/env python3
"""
Form 8949 Data Generator for RSU Transactions

Generates data for IRS Form 8949 (Sales and Other Dispositions of Capital Assets)
with proper adjustments for incorrect broker-reported cost basis.

This is critical for RSUs because broker 1099-B forms often report wrong cost basis.

Usage:
    python generate_form_8949.py --sales-file sales.json --vesting-file vesting.json
    python generate_form_8949.py --combined-file rsu_data.json
"""

import argparse
import json
import sys
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple


def parse_date(date_str: str) -> Optional[date]:
    """Parse date string to date object."""
    if not date_str:
        return None

    formats = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None


def determine_holding_period(vesting_date: date, sale_date: date) -> Tuple[bool, int]:
    """
    Determine if long-term (> 1 year) and calculate days held.

    Returns:
        Tuple of (is_long_term, days_held)
    """
    days_held = (sale_date - vesting_date).days
    is_long_term = days_held > 365
    return is_long_term, days_held


def match_sale_to_vesting_lot(sale: Dict, vesting_records: List[Dict],
                              method: str = "fifo") -> Optional[Dict]:
    """
    Match a sale transaction to its corresponding vesting lot.

    Args:
        sale: Sale transaction data
        vesting_records: List of vesting records
        method: Lot matching method (fifo, lifo, specific)

    Returns:
        Matching vesting record or None
    """
    sale_date = parse_date(sale.get("date") or sale.get("sale_date", ""))

    # Filter vesting records that could apply (vested before sale)
    eligible_lots = []
    for vest in vesting_records:
        vest_date = parse_date(vest.get("vesting_date", ""))
        if vest_date and sale_date and vest_date <= sale_date:
            eligible_lots.append({
                **vest,
                "vesting_date_parsed": vest_date
            })

    if not eligible_lots:
        return None

    if method == "fifo":
        # First In, First Out - oldest lot first
        eligible_lots.sort(key=lambda x: x["vesting_date_parsed"])
    elif method == "lifo":
        # Last In, First Out - newest lot first
        eligible_lots.sort(key=lambda x: x["vesting_date_parsed"], reverse=True)

    # Return the first eligible lot
    return eligible_lots[0] if eligible_lots else None


def generate_form_8949_entry(
    sale: Dict,
    vesting_record: Optional[Dict],
    broker_reported_basis: float = 0
) -> Dict:
    """
    Generate a Form 8949 entry for a sale transaction.

    Args:
        sale: Sale transaction data
        vesting_record: Corresponding vesting record (for correct cost basis)
        broker_reported_basis: What the broker reported on 1099-B (often wrong)

    Returns:
        Dictionary with Form 8949 entry data
    """
    # Extract sale data
    sale_date = parse_date(sale.get("date") or sale.get("sale_date", ""))
    shares = sale.get("quantity") or sale.get("shares", 0)
    proceeds = sale.get("proceeds", 0)
    description = sale.get("symbol", "AMZN") or "AMZN"

    # Get correct cost basis from vesting record
    if vesting_record:
        vesting_date = parse_date(vesting_record.get("vesting_date", ""))
        fmv_at_vesting = vesting_record.get("fmv_at_vesting") or vesting_record.get("release_price", 0)
        correct_cost_basis = shares * fmv_at_vesting
    else:
        vesting_date = None
        fmv_at_vesting = None
        correct_cost_basis = broker_reported_basis  # Fall back if no vesting data

    # Calculate adjustment
    adjustment_amount = correct_cost_basis - broker_reported_basis
    needs_adjustment = adjustment_amount != 0

    # Determine holding period
    if vesting_date and sale_date:
        is_long_term, days_held = determine_holding_period(vesting_date, sale_date)
    else:
        is_long_term = None
        days_held = None

    # Determine Form 8949 box
    # Box A/D: Short/Long-term, basis reported to IRS
    # Box B/E: Short/Long-term, basis NOT reported to IRS
    # Box C/F: Short/Long-term, Form 1099-B not received
    basis_reported = sale.get("basis_reported_to_irs", True)

    if is_long_term is True:
        box = "D" if basis_reported and not needs_adjustment else "E"
    elif is_long_term is False:
        box = "A" if basis_reported and not needs_adjustment else "B"
    else:
        box = "B"  # Default to short-term, basis not reported

    # Determine adjustment code
    adjustment_code = ""
    if needs_adjustment:
        adjustment_code = "B"  # Code B = Basis reported to IRS is incorrect

    # Calculate gain/loss
    correct_gain_loss = proceeds - correct_cost_basis
    reported_gain_loss = proceeds - broker_reported_basis

    return {
        "form_8949_entry": {
            "column_a_description": f"{description} ({shares:.0f} sh)" if shares else description,
            "column_b_date_acquired": vesting_date.strftime("%m/%d/%Y") if vesting_date else "VARIOUS",
            "column_c_date_sold": sale_date.strftime("%m/%d/%Y") if sale_date else "",
            "column_d_proceeds": round(proceeds, 2),
            "column_e_cost_basis": round(broker_reported_basis, 2),
            "column_f_adjustment_code": adjustment_code,
            "column_g_adjustment_amount": round(adjustment_amount, 2) if adjustment_amount else None,
            "column_h_gain_or_loss": round(correct_gain_loss, 2),
            "box": box
        },
        "details": {
            "shares": shares,
            "sale_date": sale_date.isoformat() if sale_date else None,
            "vesting_date": vesting_date.isoformat() if vesting_date else None,
            "holding_period_days": days_held,
            "is_long_term": is_long_term,
            "fmv_at_vesting": fmv_at_vesting,
            "correct_cost_basis": round(correct_cost_basis, 2),
            "broker_reported_basis": round(broker_reported_basis, 2),
            "correct_gain_loss": round(correct_gain_loss, 2),
            "reported_gain_loss": round(reported_gain_loss, 2),
            "adjustment_amount": round(adjustment_amount, 2),
            "tax_savings_from_correction": round((reported_gain_loss - correct_gain_loss) * 0.20, 2)  # Rough estimate
        },
        "warnings": []
    }


def process_all_sales(
    sales: List[Dict],
    vesting_records: List[Dict],
    lot_method: str = "fifo"
) -> Dict:
    """
    Process all sales and generate Form 8949 data.

    Args:
        sales: List of sale transactions
        vesting_records: List of vesting records
        lot_method: Lot matching method (fifo, lifo)

    Returns:
        Complete Form 8949 data with summaries
    """
    entries = []
    warnings = []

    # Track running totals
    total_proceeds = 0
    total_correct_basis = 0
    total_reported_basis = 0
    total_adjustment = 0

    short_term_gain = 0
    long_term_gain = 0

    for sale in sales:
        # Match to vesting lot
        vesting_lot = match_sale_to_vesting_lot(sale, vesting_records, lot_method)

        # Get broker-reported basis
        broker_basis = sale.get("cost_basis_reported") or sale.get("cost_basis", 0) or 0

        if not vesting_lot:
            warnings.append({
                "sale": sale,
                "warning": "Could not match sale to vesting lot. Using broker-reported basis."
            })

        # Generate Form 8949 entry
        entry = generate_form_8949_entry(sale, vesting_lot, broker_basis)
        entries.append(entry)

        # Update totals
        details = entry["details"]
        total_proceeds += sale.get("proceeds", 0)
        total_correct_basis += details["correct_cost_basis"]
        total_reported_basis += broker_basis
        total_adjustment += details["adjustment_amount"]

        if details["is_long_term"]:
            long_term_gain += details["correct_gain_loss"]
        else:
            short_term_gain += details["correct_gain_loss"]

    # Separate by Form 8949 box
    short_term_entries = [e for e in entries if e["form_8949_entry"]["box"] in ["A", "B", "C"]]
    long_term_entries = [e for e in entries if e["form_8949_entry"]["box"] in ["D", "E", "F"]]

    return {
        "form_8949_part_1_short_term": {
            "box": "B" if any(e["form_8949_entry"]["adjustment_code"] for e in short_term_entries) else "A",
            "entries": [e["form_8949_entry"] for e in short_term_entries],
            "totals": {
                "total_proceeds": sum(e["form_8949_entry"]["column_d_proceeds"] for e in short_term_entries),
                "total_cost_basis": sum(e["form_8949_entry"]["column_e_cost_basis"] for e in short_term_entries),
                "total_adjustment": sum(e["form_8949_entry"]["column_g_adjustment_amount"] or 0 for e in short_term_entries),
                "total_gain_loss": sum(e["form_8949_entry"]["column_h_gain_or_loss"] for e in short_term_entries)
            }
        },
        "form_8949_part_2_long_term": {
            "box": "E" if any(e["form_8949_entry"]["adjustment_code"] for e in long_term_entries) else "D",
            "entries": [e["form_8949_entry"] for e in long_term_entries],
            "totals": {
                "total_proceeds": sum(e["form_8949_entry"]["column_d_proceeds"] for e in long_term_entries),
                "total_cost_basis": sum(e["form_8949_entry"]["column_e_cost_basis"] for e in long_term_entries),
                "total_adjustment": sum(e["form_8949_entry"]["column_g_adjustment_amount"] or 0 for e in long_term_entries),
                "total_gain_loss": sum(e["form_8949_entry"]["column_h_gain_or_loss"] for e in long_term_entries)
            }
        },
        "summary": {
            "total_transactions": len(entries),
            "short_term_transactions": len(short_term_entries),
            "long_term_transactions": len(long_term_entries),
            "total_proceeds": round(total_proceeds, 2),
            "total_correct_cost_basis": round(total_correct_basis, 2),
            "total_broker_reported_basis": round(total_reported_basis, 2),
            "total_basis_adjustment": round(total_adjustment, 2),
            "short_term_gain_loss": round(short_term_gain, 2),
            "long_term_gain_loss": round(long_term_gain, 2),
            "total_gain_loss": round(short_term_gain + long_term_gain, 2)
        },
        "schedule_d_summary": {
            "line_1b": round(short_term_gain, 2),  # Short-term from Form 8949 Box A
            "line_2": round(short_term_gain, 2),   # Short-term from Form 8949 Box B
            "line_8b": round(long_term_gain, 2),   # Long-term from Form 8949 Box D
            "line_9": round(long_term_gain, 2),    # Long-term from Form 8949 Box E
            "note": "Transfer totals to appropriate Schedule D lines based on box used"
        },
        "tax_impact": {
            "if_using_incorrect_basis": {
                "total_gain": round(total_proceeds - total_reported_basis, 2),
                "estimated_tax_at_25_percent": round((total_proceeds - total_reported_basis) * 0.25, 2)
            },
            "with_correct_basis": {
                "total_gain": round(total_proceeds - total_correct_basis, 2),
                "estimated_tax_at_25_percent": round((total_proceeds - total_correct_basis) * 0.25, 2)
            },
            "tax_savings_from_correction": round(total_adjustment * 0.25, 2),
            "note": "Actual tax depends on your marginal rate and capital gains rates"
        },
        "detailed_entries": entries,
        "warnings": warnings,
        "instructions": {
            "step_1": "Review each entry for accuracy",
            "step_2": "Enter short-term transactions on Form 8949 Part I",
            "step_3": "Enter long-term transactions on Form 8949 Part II",
            "step_4": "Use adjustment code 'B' where broker basis is incorrect",
            "step_5": "Transfer totals to Schedule D",
            "step_6": "Keep vesting confirmations as documentation"
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Generate Form 8949 data for RSU transactions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  From separate files:
    python generate_form_8949.py --sales-file sales.json --vesting-file vesting.json

  From combined file:
    python generate_form_8949.py --combined-file rsu_data.json

  Expected JSON format for sales:
    {"transactions": [{"date": "2024-03-15", "shares": 100, "proceeds": 17500, "cost_basis_reported": 0}]}

  Expected JSON format for vesting:
    {"vesting_records": [{"vesting_date": "2023-01-15", "shares_vested": 100, "fmv_at_vesting": 150.00}]}
        """
    )

    parser.add_argument('--sales-file', help='JSON file with sale transactions')
    parser.add_argument('--vesting-file', help='JSON file with vesting records')
    parser.add_argument('--combined-file', help='JSON file with both sales and vesting')
    parser.add_argument('--lot-method', choices=['fifo', 'lifo'], default='fifo',
                        help='Lot matching method (default: fifo)')
    parser.add_argument('--output', help='Output file path (optional)')

    args = parser.parse_args()

    sales = []
    vesting_records = []

    # Load data
    if args.combined_file:
        with open(args.combined_file, 'r') as f:
            data = json.load(f)
        sales = data.get('transactions', data.get('sales', []))
        vesting_records = data.get('vesting_records', data.get('vesting', []))

    else:
        if args.sales_file:
            with open(args.sales_file, 'r') as f:
                sales_data = json.load(f)
            sales = sales_data.get('transactions', sales_data)

        if args.vesting_file:
            with open(args.vesting_file, 'r') as f:
                vesting_data = json.load(f)
            vesting_records = vesting_data.get('vesting_records', vesting_data)

    if not sales:
        print("Error: No sales data provided")
        sys.exit(1)

    if not vesting_records:
        print("Warning: No vesting records provided. Using broker-reported basis.")

    # Process and generate Form 8949 data
    result = process_all_sales(sales, vesting_records, args.lot_method)

    # Output
    output_json = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"Form 8949 data written to {args.output}")
    else:
        print(output_json)

    return result


if __name__ == '__main__':
    main()
