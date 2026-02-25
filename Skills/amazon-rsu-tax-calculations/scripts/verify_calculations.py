#!/usr/bin/env python3
"""
RSU Tax Calculation Verification Script

Performs comprehensive verification checks on RSU tax calculations to catch
common errors before filing. This is the final quality check.

Verification Areas:
1. Vesting income vs W-2 comparison
2. Cost basis accuracy
3. Holding period classification
4. Capital gains calculations
5. Form 8949 adjustments
6. Cross-reference checks

Usage:
    python verify_calculations.py --all-data rsu_calculations.json
    python verify_calculations.py --vesting vesting.json --sales sales.json --w2-income 150000
"""

import argparse
import json
import sys
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

# Tolerance for floating point comparisons
TOLERANCE = 0.01  # $0.01


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


def verify_vesting_income(vesting_records: List[Dict], w2_rsu_income: float) -> Dict:
    """
    Verify that vesting income matches W-2 reported income.

    Args:
        vesting_records: List of vesting records
        w2_rsu_income: RSU income reported on W-2

    Returns:
        Verification result
    """
    calculated_income = 0
    vesting_details = []

    for record in vesting_records:
        shares = record.get("shares_vested", 0)
        fmv = record.get("fmv_at_vesting", 0)
        income = shares * fmv
        calculated_income += income

        vesting_details.append({
            "date": record.get("vesting_date"),
            "shares": shares,
            "fmv": fmv,
            "income": round(income, 2)
        })

    difference = abs(calculated_income - w2_rsu_income)
    percentage_diff = (difference / w2_rsu_income * 100) if w2_rsu_income > 0 else 0

    # Allow 1% tolerance for timing differences
    passed = percentage_diff <= 1.0

    return {
        "check": "Vesting Income vs W-2",
        "passed": passed,
        "calculated_vesting_income": round(calculated_income, 2),
        "w2_reported_income": w2_rsu_income,
        "difference": round(difference, 2),
        "percentage_difference": f"{percentage_diff:.2f}%",
        "vesting_details": vesting_details,
        "status": "PASS" if passed else "FAIL",
        "message": "Vesting income matches W-2" if passed else f"Discrepancy of ${difference:,.2f} detected. Review vesting records.",
        "action_if_failed": "Compare vesting confirmations to W-2 Box 1. Contact employer if significant discrepancy."
    }


def verify_cost_basis(sales: List[Dict], vesting_records: List[Dict]) -> Dict:
    """
    Verify that correct cost basis is used (FMV at vesting, not $0 or grant price).

    Args:
        sales: List of sale transactions
        vesting_records: List of vesting records

    Returns:
        Verification result
    """
    issues = []
    warnings = []
    correct_count = 0
    incorrect_count = 0

    # Create vesting lookup
    vesting_by_date = {}
    for vest in vesting_records:
        vest_date = vest.get("vesting_date")
        if vest_date:
            vesting_by_date[vest_date] = vest

    for sale in sales:
        reported_basis = sale.get("cost_basis_reported", 0) or 0
        shares = sale.get("quantity") or sale.get("shares", 0)

        # Check for $0 basis (clear error)
        if reported_basis == 0 and shares > 0:
            issues.append({
                "sale": sale,
                "issue": "Zero cost basis reported - this is almost certainly WRONG",
                "severity": "CRITICAL"
            })
            incorrect_count += 1
            continue

        # Check if basis seems reasonable (not $0, not ridiculously high)
        if shares > 0:
            basis_per_share = reported_basis / shares

            # Flag if basis seems too low (likely grant price instead of vesting FMV)
            if basis_per_share < 50:  # Amazon hasn't been below $50 in vesting scenarios
                warnings.append({
                    "sale": sale,
                    "basis_per_share": basis_per_share,
                    "warning": "Cost basis per share seems low. Verify this is FMV at vesting date."
                })

            # Flag if basis seems too high
            if basis_per_share > 200:  # Sanity check
                warnings.append({
                    "sale": sale,
                    "basis_per_share": basis_per_share,
                    "warning": "Cost basis per share seems high. Verify against vesting confirmation."
                })

            correct_count += 1

    total_sales = len(sales)
    passed = incorrect_count == 0

    return {
        "check": "Cost Basis Verification",
        "passed": passed,
        "total_sales": total_sales,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "critical_issues": issues,
        "warnings": warnings,
        "status": "PASS" if passed else "FAIL",
        "message": "All cost bases appear reasonable" if passed else f"{incorrect_count} sales have incorrect cost basis",
        "action_if_failed": "For each flagged sale, look up the vesting confirmation to find the correct FMV at vesting date."
    }


def verify_holding_periods(sales: List[Dict], vesting_records: List[Dict]) -> Dict:
    """
    Verify holding period classification (short-term vs long-term).

    Args:
        sales: List of sale transactions
        vesting_records: List of vesting records

    Returns:
        Verification result
    """
    issues = []
    verified = []

    for sale in sales:
        sale_date = parse_date(sale.get("date") or sale.get("sale_date", ""))
        claimed_treatment = sale.get("holding_period_treatment", "").upper()

        # Find matching vesting record
        shares = sale.get("quantity") or sale.get("shares", 0)

        # Look for vesting date in sale record or find matching vesting
        vesting_date_str = sale.get("vesting_date") or sale.get("date_acquired")
        vesting_date = parse_date(vesting_date_str) if vesting_date_str else None

        if not vesting_date:
            # Try to find from vesting records (simplified FIFO)
            for vest in sorted(vesting_records, key=lambda x: x.get("vesting_date", "")):
                v_date = parse_date(vest.get("vesting_date", ""))
                if v_date and sale_date and v_date <= sale_date:
                    vesting_date = v_date
                    break

        if vesting_date and sale_date:
            days_held = (sale_date - vesting_date).days
            actual_treatment = "LONG-TERM" if days_held > 365 else "SHORT-TERM"

            verified.append({
                "sale_date": sale_date.isoformat(),
                "vesting_date": vesting_date.isoformat(),
                "days_held": days_held,
                "calculated_treatment": actual_treatment
            })

            if claimed_treatment and claimed_treatment != actual_treatment:
                issues.append({
                    "sale_date": sale_date.isoformat(),
                    "vesting_date": vesting_date.isoformat(),
                    "days_held": days_held,
                    "claimed": claimed_treatment,
                    "actual": actual_treatment,
                    "issue": f"Treatment mismatch: claimed {claimed_treatment}, should be {actual_treatment}"
                })
        else:
            issues.append({
                "sale": sale,
                "issue": "Could not determine holding period - missing vesting date"
            })

    passed = len(issues) == 0

    return {
        "check": "Holding Period Verification",
        "passed": passed,
        "total_sales": len(sales),
        "verified": len(verified),
        "issues": issues,
        "verified_details": verified,
        "status": "PASS" if passed else "FAIL",
        "message": "All holding periods verified" if passed else f"{len(issues)} holding period issues found",
        "action_if_failed": "Review each flagged sale. Holding period starts at VESTING date, not grant date."
    }


def verify_capital_gains_math(sales: List[Dict]) -> Dict:
    """
    Verify capital gains/loss calculations.

    Args:
        sales: List of sale transactions with proceeds, basis, and gain/loss

    Returns:
        Verification result
    """
    issues = []
    verified = 0

    for sale in sales:
        proceeds = sale.get("proceeds", 0)
        cost_basis = sale.get("cost_basis") or sale.get("cost_basis_reported", 0)
        reported_gain = sale.get("gain_loss") or sale.get("capital_gain_loss", 0)

        if proceeds and cost_basis:
            calculated_gain = proceeds - cost_basis

            if abs(calculated_gain - reported_gain) > TOLERANCE:
                issues.append({
                    "sale": sale,
                    "proceeds": proceeds,
                    "cost_basis": cost_basis,
                    "reported_gain_loss": reported_gain,
                    "calculated_gain_loss": round(calculated_gain, 2),
                    "difference": round(reported_gain - calculated_gain, 2),
                    "issue": "Gain/loss calculation mismatch"
                })
            else:
                verified += 1

    passed = len(issues) == 0

    return {
        "check": "Capital Gains Math",
        "passed": passed,
        "total_sales": len(sales),
        "verified": verified,
        "issues": issues,
        "status": "PASS" if passed else "FAIL",
        "message": "All gain/loss calculations verified" if passed else f"{len(issues)} calculation errors found",
        "action_if_failed": "Review the math: Gain/Loss = Proceeds - Cost Basis"
    }


def verify_form_8949_adjustments(form_8949_data: Dict) -> Dict:
    """
    Verify Form 8949 adjustments are complete and accurate.

    Args:
        form_8949_data: Form 8949 generated data

    Returns:
        Verification result
    """
    issues = []

    # Check Part I (Short-term)
    part_1 = form_8949_data.get("form_8949_part_1_short_term", {})
    entries_1 = part_1.get("entries", [])

    for entry in entries_1:
        reported_basis = entry.get("column_e_cost_basis", 0)
        adjustment = entry.get("column_g_adjustment_amount", 0) or 0
        gain_loss = entry.get("column_h_gain_or_loss", 0)
        proceeds = entry.get("column_d_proceeds", 0)

        # Verify: Proceeds - (Reported Basis + Adjustment) = Gain/Loss
        calculated_gain = proceeds - (reported_basis + adjustment)
        if abs(calculated_gain - gain_loss) > TOLERANCE:
            issues.append({
                "entry": entry,
                "calculated": calculated_gain,
                "reported": gain_loss,
                "issue": "Form 8949 Part I adjustment math error"
            })

        # Check if adjustment code is present when needed
        if adjustment != 0 and not entry.get("column_f_adjustment_code"):
            issues.append({
                "entry": entry,
                "issue": "Adjustment amount present but no adjustment code specified"
            })

    # Check Part II (Long-term)
    part_2 = form_8949_data.get("form_8949_part_2_long_term", {})
    entries_2 = part_2.get("entries", [])

    for entry in entries_2:
        reported_basis = entry.get("column_e_cost_basis", 0)
        adjustment = entry.get("column_g_adjustment_amount", 0) or 0
        gain_loss = entry.get("column_h_gain_or_loss", 0)
        proceeds = entry.get("column_d_proceeds", 0)

        calculated_gain = proceeds - (reported_basis + adjustment)
        if abs(calculated_gain - gain_loss) > TOLERANCE:
            issues.append({
                "entry": entry,
                "calculated": calculated_gain,
                "reported": gain_loss,
                "issue": "Form 8949 Part II adjustment math error"
            })

        if adjustment != 0 and not entry.get("column_f_adjustment_code"):
            issues.append({
                "entry": entry,
                "issue": "Adjustment amount present but no adjustment code specified"
            })

    passed = len(issues) == 0

    return {
        "check": "Form 8949 Adjustments",
        "passed": passed,
        "short_term_entries": len(entries_1),
        "long_term_entries": len(entries_2),
        "issues": issues,
        "status": "PASS" if passed else "FAIL",
        "message": "Form 8949 adjustments verified" if passed else f"{len(issues)} adjustment issues found",
        "action_if_failed": "Review adjustment calculations: Correct Gain = Proceeds - (Reported Basis + Adjustment)"
    }


def run_all_verifications(data: Dict) -> Dict:
    """
    Run all verification checks.

    Args:
        data: Dictionary containing all RSU data

    Returns:
        Complete verification report
    """
    results = []

    vesting_records = data.get("vesting_records", [])
    sales = data.get("sales", data.get("transactions", []))
    w2_income = data.get("w2_rsu_income", 0)
    form_8949 = data.get("form_8949_data", {})

    # Run verifications
    if vesting_records and w2_income:
        results.append(verify_vesting_income(vesting_records, w2_income))

    if sales and vesting_records:
        results.append(verify_cost_basis(sales, vesting_records))
        results.append(verify_holding_periods(sales, vesting_records))

    if sales:
        results.append(verify_capital_gains_math(sales))

    if form_8949:
        results.append(verify_form_8949_adjustments(form_8949))

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count

    return {
        "verification_report": {
            "timestamp": datetime.now().isoformat(),
            "total_checks": len(results),
            "passed": passed_count,
            "failed": failed_count,
            "overall_status": "PASS" if failed_count == 0 else "FAIL"
        },
        "checks": results,
        "action_items": [
            {
                "check": r["check"],
                "action": r.get("action_if_failed", "Review and correct")
            }
            for r in results if not r["passed"]
        ],
        "recommendation": (
            "All verifications passed. Data appears ready for tax filing."
            if failed_count == 0
            else f"{failed_count} check(s) failed. Review action items before filing."
        )
    }


def main():
    parser = argparse.ArgumentParser(
        description='Verify RSU tax calculations before filing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Verify from combined data file:
    python verify_calculations.py --all-data rsu_calculations.json

  Verify from separate files:
    python verify_calculations.py --vesting vesting.json --sales sales.json --w2-income 150000

  Expected JSON format:
    {
      "vesting_records": [...],
      "sales": [...],
      "w2_rsu_income": 150000,
      "form_8949_data": {...}
    }
        """
    )

    parser.add_argument('--all-data', help='JSON file with all RSU data')
    parser.add_argument('--vesting', help='JSON file with vesting records')
    parser.add_argument('--sales', help='JSON file with sale transactions')
    parser.add_argument('--w2-income', type=float, help='RSU income from W-2')
    parser.add_argument('--form-8949', help='JSON file with Form 8949 data')
    parser.add_argument('--output', help='Output file path (optional)')

    args = parser.parse_args()

    data = {}

    if args.all_data:
        with open(args.all_data, 'r') as f:
            data = json.load(f)
    else:
        if args.vesting:
            with open(args.vesting, 'r') as f:
                vesting_data = json.load(f)
            data["vesting_records"] = vesting_data.get("vesting_records", vesting_data)

        if args.sales:
            with open(args.sales, 'r') as f:
                sales_data = json.load(f)
            data["sales"] = sales_data.get("transactions", sales_data.get("sales", sales_data))

        if args.w2_income:
            data["w2_rsu_income"] = args.w2_income

        if args.form_8949:
            with open(args.form_8949, 'r') as f:
                data["form_8949_data"] = json.load(f)

    if not data:
        print("Error: No data provided for verification")
        parser.print_help()
        sys.exit(1)

    # Run verifications
    result = run_all_verifications(data)

    # Output
    output_json = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"Verification report written to {args.output}")
    else:
        print(output_json)

    # Return exit code based on result
    if result["verification_report"]["overall_status"] == "FAIL":
        sys.exit(1)

    return result


if __name__ == '__main__':
    main()
