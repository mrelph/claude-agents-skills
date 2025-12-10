#!/usr/bin/env python3
"""
Estimated Tax Calculator - Calculate quarterly estimated tax payments.
Determines safe harbor amounts and generates payment schedule.
"""

import argparse
import json
from datetime import date
from typing import Dict, List

# 2024 Tax Brackets (simplified for estimation)
TAX_BRACKETS = {
    "single": [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ],
    "married_jointly": [
        (23200, 0.10),
        (94300, 0.12),
        (201050, 0.22),
        (383900, 0.24),
        (487450, 0.32),
        (731200, 0.35),
        (float('inf'), 0.37)
    ]
}

STANDARD_DEDUCTIONS = {
    "single": 14600,
    "married_jointly": 29200,
    "head_of_household": 21900
}

# SE Tax rates
SS_RATE = 0.124
MEDICARE_RATE = 0.029
SS_WAGE_BASE_2024 = 168600

# Quarterly due dates for 2024 tax year (payments made in 2024 for 2024 taxes)
QUARTERLY_DUE_DATES = [
    ("Q1", "2024-04-15", "Jan 1 - Mar 31"),
    ("Q2", "2024-06-17", "Apr 1 - May 31"),
    ("Q3", "2024-09-16", "Jun 1 - Aug 31"),
    ("Q4", "2025-01-15", "Sep 1 - Dec 31")
]


def calculate_income_tax(taxable_income: float, filing_status: str) -> float:
    """Calculate federal income tax."""
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["single"])

    tax = 0
    prev_bracket = 0

    for bracket_top, rate in brackets:
        if taxable_income <= prev_bracket:
            break
        bracket_income = min(taxable_income - prev_bracket, bracket_top - prev_bracket)
        tax += bracket_income * rate
        prev_bracket = bracket_top

    return round(tax, 2)


def calculate_se_tax(net_se_income: float) -> Dict:
    """Calculate self-employment tax."""
    if net_se_income <= 0:
        return {"total": 0, "social_security": 0, "medicare": 0, "deduction": 0}

    # SE tax base is 92.35% of net SE income
    se_tax_base = net_se_income * 0.9235

    # Social Security portion (capped at wage base)
    ss_taxable = min(se_tax_base, SS_WAGE_BASE_2024)
    ss_tax = ss_taxable * SS_RATE

    # Medicare portion (no cap)
    medicare_tax = se_tax_base * MEDICARE_RATE

    total_se_tax = ss_tax + medicare_tax

    # Deductible portion (half of SE tax)
    se_deduction = total_se_tax / 2

    return {
        "total": round(total_se_tax, 2),
        "social_security": round(ss_tax, 2),
        "medicare": round(medicare_tax, 2),
        "deduction": round(se_deduction, 2)
    }


def calculate_safe_harbor(prior_year_tax: float, prior_year_agi: float) -> Dict:
    """Calculate safe harbor amounts to avoid underpayment penalty."""
    # Standard safe harbor: 100% of prior year tax
    standard_safe_harbor = prior_year_tax

    # High income safe harbor: 110% if AGI > $150k
    high_income_threshold = 150000
    if prior_year_agi > high_income_threshold:
        high_income_safe_harbor = prior_year_tax * 1.10
    else:
        high_income_safe_harbor = prior_year_tax

    return {
        "standard": round(standard_safe_harbor, 2),
        "high_income": round(high_income_safe_harbor, 2),
        "applies_high_income": prior_year_agi > high_income_threshold,
        "minimum_required": round(high_income_safe_harbor if prior_year_agi > high_income_threshold else standard_safe_harbor, 2)
    }


def calculate_estimated_payments(
    projected_income: float,
    se_income: float,
    w2_withholding: float,
    other_withholding: float,
    prior_year_tax: float,
    prior_year_agi: float,
    filing_status: str,
    credits: float = 0,
    deductions: float = 0
) -> Dict:
    """Calculate estimated tax payments needed."""

    # Calculate SE tax
    se_tax_info = calculate_se_tax(se_income)

    # Calculate AGI
    standard_deduction = STANDARD_DEDUCTIONS.get(filing_status, 14600)
    deduction_used = max(standard_deduction, deductions)

    # Adjustments (half of SE tax)
    adjustments = se_tax_info["deduction"]

    agi = projected_income - adjustments
    taxable_income = max(0, agi - deduction_used)

    # Calculate income tax
    income_tax = calculate_income_tax(taxable_income, filing_status)

    # Total tax liability
    total_tax = income_tax + se_tax_info["total"] - credits

    # Total withholding
    total_withholding = w2_withholding + other_withholding

    # Tax due after withholding
    tax_due = max(0, total_tax - total_withholding)

    # Safe harbor calculation
    safe_harbor = calculate_safe_harbor(prior_year_tax, prior_year_agi)

    # Determine required payments
    # Must pay: 90% of current year OR 100%/110% of prior year
    current_year_90 = total_tax * 0.90
    prior_year_required = safe_harbor["minimum_required"]

    # Amount needed beyond withholding
    needed_current = max(0, current_year_90 - total_withholding)
    needed_prior = max(0, prior_year_required - total_withholding)

    # Use lower of two methods
    estimated_payments_needed = min(needed_current, needed_prior)

    # Quarterly payment amount
    quarterly_payment = estimated_payments_needed / 4

    # Generate payment schedule
    payment_schedule = []
    for quarter, due_date, period in QUARTERLY_DUE_DATES:
        payment_schedule.append({
            "quarter": quarter,
            "period": period,
            "due_date": due_date,
            "amount": round(quarterly_payment, 2)
        })

    return {
        "income_summary": {
            "projected_total_income": projected_income,
            "self_employment_income": se_income,
            "w2_withholding": w2_withholding,
            "other_withholding": other_withholding,
            "total_withholding": total_withholding
        },
        "tax_calculation": {
            "adjusted_gross_income": round(agi, 2),
            "deduction_used": deduction_used,
            "taxable_income": round(taxable_income, 2),
            "income_tax": income_tax,
            "self_employment_tax": se_tax_info["total"],
            "se_deduction": se_tax_info["deduction"],
            "credits": credits,
            "total_tax_liability": round(total_tax, 2)
        },
        "safe_harbor": safe_harbor,
        "estimated_payments": {
            "total_needed": round(estimated_payments_needed, 2),
            "quarterly_amount": round(quarterly_payment, 2),
            "method_used": "90% current year" if needed_current < needed_prior else "prior year safe harbor"
        },
        "payment_schedule": payment_schedule,
        "warnings": []
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate estimated tax payments")
    parser.add_argument("--projected-income", type=float, required=True,
                        help="Total projected income for the year")
    parser.add_argument("--se-income", type=float, default=0,
                        help="Self-employment income")
    parser.add_argument("--w2-withholding", type=float, default=0,
                        help="Expected W-2 withholding for the year")
    parser.add_argument("--other-withholding", type=float, default=0,
                        help="Other withholding (1099, etc.)")
    parser.add_argument("--prior-year-tax", type=float, required=True,
                        help="Total tax from prior year return")
    parser.add_argument("--prior-year-agi", type=float, required=True,
                        help="AGI from prior year return")
    parser.add_argument("--filing-status", choices=["single", "married_jointly", "head_of_household"],
                        default="single", help="Filing status")
    parser.add_argument("--credits", type=float, default=0,
                        help="Expected tax credits")
    parser.add_argument("--deductions", type=float, default=0,
                        help="Itemized deductions (if greater than standard)")
    parser.add_argument("--output-format", choices=["json", "text"], default="text",
                        help="Output format")

    args = parser.parse_args()

    result = calculate_estimated_payments(
        projected_income=args.projected_income,
        se_income=args.se_income,
        w2_withholding=args.w2_withholding,
        other_withholding=args.other_withholding,
        prior_year_tax=args.prior_year_tax,
        prior_year_agi=args.prior_year_agi,
        filing_status=args.filing_status,
        credits=args.credits,
        deductions=args.deductions
    )

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*60)
        print("ESTIMATED TAX PAYMENT CALCULATOR")
        print("="*60)

        print(f"\nFiling Status: {args.filing_status.replace('_', ' ').title()}")

        print(f"\nINCOME & WITHHOLDING:")
        print(f"  Projected Total Income:    ${result['income_summary']['projected_total_income']:,.2f}")
        if args.se_income > 0:
            print(f"  Self-Employment Income:    ${result['income_summary']['self_employment_income']:,.2f}")
        print(f"  W-2 Withholding:           ${result['income_summary']['w2_withholding']:,.2f}")
        if args.other_withholding > 0:
            print(f"  Other Withholding:         ${result['income_summary']['other_withholding']:,.2f}")
        print(f"  Total Withholding:         ${result['income_summary']['total_withholding']:,.2f}")

        print(f"\nTAX CALCULATION:")
        print(f"  AGI:                       ${result['tax_calculation']['adjusted_gross_income']:,.2f}")
        print(f"  Deduction:                 ${result['tax_calculation']['deduction_used']:,.2f}")
        print(f"  Taxable Income:            ${result['tax_calculation']['taxable_income']:,.2f}")
        print(f"  Income Tax:                ${result['tax_calculation']['income_tax']:,.2f}")
        if result['tax_calculation']['self_employment_tax'] > 0:
            print(f"  Self-Employment Tax:       ${result['tax_calculation']['self_employment_tax']:,.2f}")
        if args.credits > 0:
            print(f"  Credits:                   ${result['tax_calculation']['credits']:,.2f}")
        print(f"  Total Tax Liability:       ${result['tax_calculation']['total_tax_liability']:,.2f}")

        print(f"\nSAFE HARBOR:")
        print(f"  Prior Year Tax:            ${args.prior_year_tax:,.2f}")
        if result['safe_harbor']['applies_high_income']:
            print(f"  110% Safe Harbor:          ${result['safe_harbor']['high_income']:,.2f}")
            print(f"  (Applies because prior AGI > $150,000)")
        else:
            print(f"  100% Safe Harbor:          ${result['safe_harbor']['standard']:,.2f}")

        print(f"\nESTIMATED PAYMENTS NEEDED:")
        print(f"  Total Estimated Payments:  ${result['estimated_payments']['total_needed']:,.2f}")
        print(f"  Quarterly Payment:         ${result['estimated_payments']['quarterly_amount']:,.2f}")
        print(f"  Method:                    {result['estimated_payments']['method_used']}")

        print(f"\nPAYMENT SCHEDULE:")
        print("-"*50)
        for payment in result['payment_schedule']:
            print(f"  {payment['quarter']}: {payment['period']}")
            print(f"      Due: {payment['due_date']}    Amount: ${payment['amount']:,.2f}")
        print("-"*50)
        print(f"  TOTAL:                     ${result['estimated_payments']['total_needed']:,.2f}")

        print("="*60 + "\n")


if __name__ == "__main__":
    main()
