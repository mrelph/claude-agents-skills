#!/usr/bin/env python3
"""
Deduction Analyzer - Compare standard vs itemized deductions and identify optimization opportunities.
"""

import argparse
import json
from typing import Dict, List

# 2024 Standard Deductions
STANDARD_DEDUCTIONS = {
    "single": 14600,
    "married_jointly": 29200,
    "married_separately": 14600,
    "head_of_household": 21900
}

ADDITIONAL_DEDUCTION = {
    "single": 1950,
    "married_jointly": 1550,
    "married_separately": 1550,
    "head_of_household": 1950
}

# Limits and thresholds
SALT_CAP = 10000
SALT_CAP_MFS = 5000
MORTGAGE_DEBT_LIMIT = 750000
MORTGAGE_DEBT_LIMIT_MFS = 375000


def analyze_medical_deduction(expenses: float, agi: float) -> Dict:
    """Calculate deductible medical expenses (>7.5% of AGI)."""
    threshold = agi * 0.075
    deductible = max(0, expenses - threshold)

    return {
        "total_expenses": expenses,
        "agi_threshold_75": round(threshold, 2),
        "deductible_amount": round(deductible, 2),
        "non_deductible": round(min(expenses, threshold), 2)
    }


def analyze_salt_deduction(
    property_tax: float,
    state_income_tax: float,
    state_sales_tax: float,
    filing_status: str
) -> Dict:
    """Analyze state and local tax deduction with cap."""
    cap = SALT_CAP_MFS if filing_status == "married_separately" else SALT_CAP

    # Can use income OR sales tax, not both
    income_or_sales = max(state_income_tax, state_sales_tax)
    used_sales_tax = state_sales_tax > state_income_tax

    total_before_cap = property_tax + income_or_sales
    deductible = min(total_before_cap, cap)
    lost_to_cap = max(0, total_before_cap - cap)

    return {
        "property_tax": property_tax,
        "state_income_tax": state_income_tax,
        "state_sales_tax": state_sales_tax,
        "used_sales_tax_method": used_sales_tax,
        "income_or_sales_used": round(income_or_sales, 2),
        "total_before_cap": round(total_before_cap, 2),
        "salt_cap": cap,
        "deductible_amount": round(deductible, 2),
        "lost_to_cap": round(lost_to_cap, 2)
    }


def analyze_mortgage_interest(
    interest_paid: float,
    acquisition_debt: float,
    filing_status: str
) -> Dict:
    """Analyze mortgage interest deduction."""
    debt_limit = MORTGAGE_DEBT_LIMIT_MFS if filing_status == "married_separately" else MORTGAGE_DEBT_LIMIT

    if acquisition_debt <= debt_limit:
        deductible = interest_paid
        limited = False
    else:
        # Pro-rate the interest
        ratio = debt_limit / acquisition_debt
        deductible = interest_paid * ratio
        limited = True

    return {
        "interest_paid": interest_paid,
        "acquisition_debt": acquisition_debt,
        "debt_limit": debt_limit,
        "deductible_amount": round(deductible, 2),
        "limited_by_debt_cap": limited
    }


def analyze_charitable(
    cash_donations: float,
    appreciated_property: float,
    agi: float
) -> Dict:
    """Analyze charitable contribution deduction limits."""
    # Cash: 60% of AGI limit
    cash_limit = agi * 0.60
    cash_deductible = min(cash_donations, cash_limit)
    cash_carryover = max(0, cash_donations - cash_limit)

    # Appreciated property: 30% of AGI limit
    property_limit = agi * 0.30
    property_deductible = min(appreciated_property, property_limit)
    property_carryover = max(0, appreciated_property - property_limit)

    return {
        "cash_donations": cash_donations,
        "cash_agi_limit_60": round(cash_limit, 2),
        "cash_deductible": round(cash_deductible, 2),
        "cash_carryover": round(cash_carryover, 2),
        "appreciated_property": appreciated_property,
        "property_agi_limit_30": round(property_limit, 2),
        "property_deductible": round(property_deductible, 2),
        "property_carryover": round(property_carryover, 2),
        "total_deductible": round(cash_deductible + property_deductible, 2),
        "total_carryover": round(cash_carryover + property_carryover, 2)
    }


def compare_deductions(
    filing_status: str,
    agi: float,
    age_65_plus: int,
    blind: int,
    medical_expenses: float,
    property_tax: float,
    state_income_tax: float,
    state_sales_tax: float,
    mortgage_interest: float,
    acquisition_debt: float,
    cash_charitable: float,
    property_charitable: float,
    other_itemized: float
) -> Dict:
    """Compare standard vs itemized deductions and provide recommendation."""

    # Calculate standard deduction
    base_std = STANDARD_DEDUCTIONS.get(filing_status, 14600)
    additional = ADDITIONAL_DEDUCTION.get(filing_status, 1950)
    standard_deduction = base_std + (additional * age_65_plus) + (additional * blind)

    # Analyze each itemized category
    medical = analyze_medical_deduction(medical_expenses, agi)
    salt = analyze_salt_deduction(property_tax, state_income_tax, state_sales_tax, filing_status)
    mortgage = analyze_mortgage_interest(mortgage_interest, acquisition_debt, filing_status)
    charitable = analyze_charitable(cash_charitable, property_charitable, agi)

    # Total itemized deductions
    total_itemized = (
        medical["deductible_amount"] +
        salt["deductible_amount"] +
        mortgage["deductible_amount"] +
        charitable["total_deductible"] +
        other_itemized
    )

    # Recommendation
    use_itemized = total_itemized > standard_deduction
    benefit = abs(total_itemized - standard_deduction)

    # Identify optimization opportunities
    opportunities = []

    if salt["lost_to_cap"] > 0:
        opportunities.append({
            "category": "SALT",
            "issue": f"${salt['lost_to_cap']:,.2f} lost to SALT cap",
            "suggestion": "Consider prepaying property taxes in alternate years to bunch deductions"
        })

    if medical["deductible_amount"] == 0 and medical_expenses > 0:
        shortfall = medical["agi_threshold_75"] - medical_expenses
        opportunities.append({
            "category": "Medical",
            "issue": f"Medical expenses below 7.5% AGI threshold by ${shortfall:,.2f}",
            "suggestion": "Consider timing elective procedures to bunch medical expenses"
        })

    if charitable["total_carryover"] > 0:
        opportunities.append({
            "category": "Charitable",
            "issue": f"${charitable['total_carryover']:,.2f} in charitable carryover",
            "suggestion": "Charitable donations exceeded AGI limits; carryover available for 5 years"
        })

    if not use_itemized and (total_itemized > standard_deduction * 0.8):
        opportunities.append({
            "category": "Bunching Strategy",
            "issue": "Close to itemizing threshold",
            "suggestion": "Consider bunching deductions in alternate years to maximize benefit"
        })

    return {
        "filing_status": filing_status,
        "agi": agi,
        "standard_deduction": {
            "base_amount": base_std,
            "additional_for_age_blind": additional * (age_65_plus + blind),
            "total": standard_deduction
        },
        "itemized_analysis": {
            "medical": medical,
            "salt": salt,
            "mortgage_interest": mortgage,
            "charitable": charitable,
            "other": other_itemized,
            "total_itemized": round(total_itemized, 2)
        },
        "recommendation": {
            "use_itemized": use_itemized,
            "deduction_to_use": round(max(standard_deduction, total_itemized), 2),
            "benefit_over_alternative": round(benefit, 2)
        },
        "optimization_opportunities": opportunities
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze deductions: standard vs itemized")
    parser.add_argument("--filing-status", choices=list(STANDARD_DEDUCTIONS.keys()),
                        required=True, help="Filing status")
    parser.add_argument("--agi", type=float, required=True, help="Adjusted Gross Income")
    parser.add_argument("--age-65-plus", type=int, default=0, help="Number of taxpayers 65+")
    parser.add_argument("--blind", type=int, default=0, help="Number of blind taxpayers")
    parser.add_argument("--medical", type=float, default=0, help="Medical expenses")
    parser.add_argument("--property-tax", type=float, default=0, help="Property taxes paid")
    parser.add_argument("--state-income-tax", type=float, default=0, help="State income tax paid")
    parser.add_argument("--state-sales-tax", type=float, default=0, help="State sales tax (alternative)")
    parser.add_argument("--mortgage-interest", type=float, default=0, help="Mortgage interest paid")
    parser.add_argument("--mortgage-debt", type=float, default=0, help="Acquisition debt balance")
    parser.add_argument("--charitable-cash", type=float, default=0, help="Cash charitable donations")
    parser.add_argument("--charitable-property", type=float, default=0, help="Appreciated property donations")
    parser.add_argument("--other-itemized", type=float, default=0, help="Other itemized deductions")
    parser.add_argument("--output-format", choices=["json", "text"], default="text")

    args = parser.parse_args()

    result = compare_deductions(
        filing_status=args.filing_status,
        agi=args.agi,
        age_65_plus=args.age_65_plus,
        blind=args.blind,
        medical_expenses=args.medical,
        property_tax=args.property_tax,
        state_income_tax=args.state_income_tax,
        state_sales_tax=args.state_sales_tax,
        mortgage_interest=args.mortgage_interest,
        acquisition_debt=args.mortgage_debt,
        cash_charitable=args.charitable_cash,
        property_charitable=args.charitable_property,
        other_itemized=args.other_itemized
    )

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*60)
        print("DEDUCTION ANALYSIS")
        print("="*60)

        print(f"\nFiling Status: {args.filing_status.replace('_', ' ').title()}")
        print(f"AGI: ${args.agi:,.2f}")

        std = result["standard_deduction"]
        print(f"\nSTANDARD DEDUCTION:")
        print(f"  Base Amount:                ${std['base_amount']:,.2f}")
        if std["additional_for_age_blind"] > 0:
            print(f"  Additional (65+/Blind):     ${std['additional_for_age_blind']:,.2f}")
        print(f"  Total Standard:             ${std['total']:,.2f}")

        item = result["itemized_analysis"]
        print(f"\nITEMIZED DEDUCTIONS:")

        if item["medical"]["total_expenses"] > 0:
            print(f"\n  Medical Expenses:")
            print(f"    Total Expenses:           ${item['medical']['total_expenses']:,.2f}")
            print(f"    7.5% AGI Threshold:       ${item['medical']['agi_threshold_75']:,.2f}")
            print(f"    Deductible:               ${item['medical']['deductible_amount']:,.2f}")

        print(f"\n  State & Local Taxes (SALT):")
        print(f"    Property Tax:             ${item['salt']['property_tax']:,.2f}")
        if item["salt"]["used_sales_tax_method"]:
            print(f"    Sales Tax (used):         ${item['salt']['state_sales_tax']:,.2f}")
        else:
            print(f"    State Income Tax:         ${item['salt']['state_income_tax']:,.2f}")
        print(f"    Total Before Cap:         ${item['salt']['total_before_cap']:,.2f}")
        print(f"    SALT Cap:                 ${item['salt']['salt_cap']:,.2f}")
        print(f"    Deductible:               ${item['salt']['deductible_amount']:,.2f}")
        if item["salt"]["lost_to_cap"] > 0:
            print(f"    Lost to Cap:              ${item['salt']['lost_to_cap']:,.2f}")

        if item["mortgage_interest"]["interest_paid"] > 0:
            print(f"\n  Mortgage Interest:")
            print(f"    Interest Paid:            ${item['mortgage_interest']['interest_paid']:,.2f}")
            print(f"    Deductible:               ${item['mortgage_interest']['deductible_amount']:,.2f}")

        if item["charitable"]["cash_donations"] > 0 or item["charitable"]["appreciated_property"] > 0:
            print(f"\n  Charitable Contributions:")
            if item["charitable"]["cash_donations"] > 0:
                print(f"    Cash Donations:           ${item['charitable']['cash_donations']:,.2f}")
            if item["charitable"]["appreciated_property"] > 0:
                print(f"    Property Donations:       ${item['charitable']['appreciated_property']:,.2f}")
            print(f"    Total Deductible:         ${item['charitable']['total_deductible']:,.2f}")
            if item["charitable"]["total_carryover"] > 0:
                print(f"    Carryover to Next Year:   ${item['charitable']['total_carryover']:,.2f}")

        if item["other"] > 0:
            print(f"\n  Other Itemized:             ${item['other']:,.2f}")

        print(f"\n  ----------------------------------------")
        print(f"  TOTAL ITEMIZED:             ${item['total_itemized']:,.2f}")

        rec = result["recommendation"]
        print(f"\n{'='*60}")
        print(f"RECOMMENDATION: {'ITEMIZE' if rec['use_itemized'] else 'STANDARD DEDUCTION'}")
        print(f"Deduction Amount: ${rec['deduction_to_use']:,.2f}")
        print(f"Benefit: ${rec['benefit_over_alternative']:,.2f} more than alternative")

        if result["optimization_opportunities"]:
            print(f"\nOPTIMIZATION OPPORTUNITIES:")
            for opp in result["optimization_opportunities"]:
                print(f"\n  [{opp['category']}]")
                print(f"    Issue: {opp['issue']}")
                print(f"    Suggestion: {opp['suggestion']}")

        print("="*60 + "\n")


if __name__ == "__main__":
    main()
