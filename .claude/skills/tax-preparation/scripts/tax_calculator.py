#!/usr/bin/env python3
"""
Tax Calculator - Calculate federal income tax based on filing status and income.
Supports 2024 tax year brackets and standard deductions.
"""

import argparse
import json
from typing import Dict, Tuple

# 2024 Tax Brackets
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
    ],
    "married_separately": [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (365600, 0.35),
        (float('inf'), 0.37)
    ],
    "head_of_household": [
        (16550, 0.10),
        (63100, 0.12),
        (100500, 0.22),
        (191950, 0.24),
        (243700, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ]
}

STANDARD_DEDUCTIONS = {
    "single": 14600,
    "married_jointly": 29200,
    "married_separately": 14600,
    "head_of_household": 21900
}

ADDITIONAL_DEDUCTION_65_BLIND = {
    "single": 1950,
    "married_jointly": 1550,
    "married_separately": 1550,
    "head_of_household": 1950
}


def calculate_tax(taxable_income: float, filing_status: str) -> Tuple[float, Dict]:
    """Calculate federal income tax and return breakdown by bracket."""
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["single"])

    tax = 0
    breakdown = []
    prev_bracket = 0
    remaining_income = taxable_income

    for bracket_top, rate in brackets:
        if remaining_income <= 0:
            break

        bracket_income = min(remaining_income, bracket_top - prev_bracket)
        bracket_tax = bracket_income * rate
        tax += bracket_tax

        if bracket_income > 0:
            breakdown.append({
                "bracket_floor": prev_bracket,
                "bracket_ceiling": bracket_top if bracket_top != float('inf') else "unlimited",
                "rate": rate,
                "income_in_bracket": round(bracket_income, 2),
                "tax_from_bracket": round(bracket_tax, 2)
            })

        remaining_income -= bracket_income
        prev_bracket = bracket_top

    return round(tax, 2), breakdown


def calculate_effective_rate(tax: float, gross_income: float) -> float:
    """Calculate effective tax rate."""
    if gross_income <= 0:
        return 0
    return round((tax / gross_income) * 100, 2)


def calculate_marginal_rate(taxable_income: float, filing_status: str) -> float:
    """Determine marginal tax rate based on taxable income."""
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["single"])

    prev_bracket = 0
    for bracket_top, rate in brackets:
        if taxable_income <= bracket_top:
            return rate
        prev_bracket = bracket_top

    return brackets[-1][1]


def calculate_standard_deduction(filing_status: str, age_65_plus: int = 0, blind: int = 0) -> float:
    """Calculate standard deduction including additional amounts for age/blindness."""
    base = STANDARD_DEDUCTIONS.get(filing_status, STANDARD_DEDUCTIONS["single"])
    additional = ADDITIONAL_DEDUCTION_65_BLIND.get(filing_status, 1950)

    return base + (additional * age_65_plus) + (additional * blind)


def main():
    parser = argparse.ArgumentParser(description="Calculate federal income tax")
    parser.add_argument("--gross-income", type=float, required=True, help="Gross income")
    parser.add_argument("--filing-status", choices=list(TAX_BRACKETS.keys()),
                        default="single", help="Filing status")
    parser.add_argument("--deductions", type=float, default=0,
                        help="Itemized deductions (if greater than standard, will use itemized)")
    parser.add_argument("--adjustments", type=float, default=0,
                        help="Above-the-line adjustments (IRA, student loan interest, etc.)")
    parser.add_argument("--age-65-plus", type=int, default=0,
                        help="Number of taxpayers 65+ (0, 1, or 2)")
    parser.add_argument("--blind", type=int, default=0,
                        help="Number of blind taxpayers (0, 1, or 2)")
    parser.add_argument("--credits", type=float, default=0,
                        help="Total tax credits")
    parser.add_argument("--output-format", choices=["json", "text"], default="text",
                        help="Output format")

    args = parser.parse_args()

    # Calculate AGI
    agi = args.gross_income - args.adjustments

    # Determine deduction to use
    standard_deduction = calculate_standard_deduction(
        args.filing_status,
        args.age_65_plus,
        args.blind
    )
    deduction_used = max(standard_deduction, args.deductions)
    using_itemized = args.deductions > standard_deduction

    # Calculate taxable income
    taxable_income = max(0, agi - deduction_used)

    # Calculate tax
    tax_before_credits, breakdown = calculate_tax(taxable_income, args.filing_status)

    # Apply credits
    tax_after_credits = max(0, tax_before_credits - args.credits)

    # Calculate rates
    effective_rate = calculate_effective_rate(tax_after_credits, args.gross_income)
    marginal_rate = calculate_marginal_rate(taxable_income, args.filing_status)

    result = {
        "input": {
            "gross_income": args.gross_income,
            "filing_status": args.filing_status,
            "adjustments": args.adjustments,
            "itemized_deductions": args.deductions,
            "credits": args.credits
        },
        "calculations": {
            "adjusted_gross_income": round(agi, 2),
            "standard_deduction": standard_deduction,
            "deduction_used": deduction_used,
            "using_itemized": using_itemized,
            "taxable_income": round(taxable_income, 2)
        },
        "tax": {
            "tax_before_credits": tax_before_credits,
            "credits_applied": min(args.credits, tax_before_credits),
            "tax_after_credits": tax_after_credits,
            "effective_rate_percent": effective_rate,
            "marginal_rate_percent": marginal_rate * 100
        },
        "bracket_breakdown": breakdown
    }

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*60)
        print("FEDERAL TAX CALCULATION")
        print("="*60)
        print(f"\nFiling Status: {args.filing_status.replace('_', ' ').title()}")
        print(f"\nINCOME:")
        print(f"  Gross Income:           ${args.gross_income:,.2f}")
        print(f"  - Adjustments:          ${args.adjustments:,.2f}")
        print(f"  = AGI:                  ${agi:,.2f}")
        print(f"\nDEDUCTIONS:")
        print(f"  Standard Deduction:     ${standard_deduction:,.2f}")
        if args.deductions > 0:
            print(f"  Itemized Deductions:    ${args.deductions:,.2f}")
        print(f"  Using:                  {'Itemized' if using_itemized else 'Standard'} (${deduction_used:,.2f})")
        print(f"\n  Taxable Income:         ${taxable_income:,.2f}")
        print(f"\nTAX CALCULATION:")
        for b in breakdown:
            ceiling = f"${b['bracket_ceiling']:,.0f}" if isinstance(b['bracket_ceiling'], (int, float)) else b['bracket_ceiling']
            print(f"  {b['rate']*100:.0f}% on ${b['income_in_bracket']:,.2f}: ${b['tax_from_bracket']:,.2f}")
        print(f"  ----------------------------------------")
        print(f"  Tax Before Credits:     ${tax_before_credits:,.2f}")
        if args.credits > 0:
            print(f"  - Credits Applied:      ${min(args.credits, tax_before_credits):,.2f}")
        print(f"  = Tax After Credits:    ${tax_after_credits:,.2f}")
        print(f"\nRATES:")
        print(f"  Effective Tax Rate:     {effective_rate:.2f}%")
        print(f"  Marginal Tax Rate:      {marginal_rate*100:.0f}%")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()
