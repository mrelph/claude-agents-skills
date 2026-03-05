#!/usr/bin/env python3
"""
Tax Strategy Analyzer for Retirement Planning

Models tax-efficient strategies including Roth conversions,
withdrawal sequencing, and bracket management.

Usage:
    python tax_strategy.py --scenario roth-conversion --current-income 150000 --conversion-amount 50000
    python tax_strategy.py --scenario withdrawal-sequence --traditional 1000000 --roth 500000 --annual-need 80000
"""

import argparse
import json
from datetime import datetime


# 2025 Tax Brackets
TAX_BRACKETS = {
    "single": [
        (11925, 0.10), (48475, 0.12), (103350, 0.22),
        (197300, 0.24), (250525, 0.32), (626350, 0.35),
        (float('inf'), 0.37)
    ],
    "married_jointly": [
        (23850, 0.10), (96950, 0.12), (206700, 0.22),
        (394600, 0.24), (501050, 0.32), (751600, 0.35),
        (float('inf'), 0.37)
    ]
}

STANDARD_DEDUCTIONS_2025 = {
    "single": 15000,
    "married_jointly": 30000
}

IRMAA_THRESHOLDS = {
    "single": [103000, 129000, 161000, 193000, 500000],
    "married_jointly": [206000, 258000, 322000, 386000, 750000]
}


def calculate_tax(taxable_income, filing_status="married_jointly"):
    """Calculate federal income tax."""
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["married_jointly"])
    tax = 0
    prev = 0
    for top, rate in brackets:
        bracket_income = min(max(taxable_income - prev, 0), top - prev)
        tax += bracket_income * rate
        prev = top
        if taxable_income <= top:
            break
    return round(tax, 2)


def get_marginal_rate(taxable_income, filing_status="married_jointly"):
    """Get current marginal tax rate."""
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["married_jointly"])
    for top, rate in brackets:
        if taxable_income <= top:
            return rate
    return brackets[-1][1]


def analyze_roth_conversion(current_income, conversion_amount, filing_status,
                             current_bracket, retirement_bracket,
                             years_to_retirement, growth_rate=0.07):
    """Analyze whether a Roth conversion is favorable."""

    std_deduction = STANDARD_DEDUCTIONS_2025.get(filing_status, 30000)
    taxable_before = max(0, current_income - std_deduction)
    taxable_after = taxable_before + conversion_amount

    tax_before = calculate_tax(taxable_before, filing_status)
    tax_after = calculate_tax(taxable_after, filing_status)
    conversion_tax_cost = tax_after - tax_before

    marginal_rate = get_marginal_rate(taxable_after, filing_status)
    retirement_rate = retirement_bracket / 100

    future_value = conversion_amount * ((1 + growth_rate) ** years_to_retirement)
    tax_saved_in_retirement = future_value * retirement_rate
    net_benefit = tax_saved_in_retirement - conversion_tax_cost

    # Bracket space analysis
    brackets = TAX_BRACKETS.get(filing_status, TAX_BRACKETS["married_jointly"])
    bracket_space = {}
    prev = 0
    for top, rate in brackets:
        if taxable_before < top:
            space = top - max(taxable_before, prev)
            if space > 0:
                bracket_space[f"{rate * 100:.0f}%"] = round(space, 2)
        prev = top
        if rate >= 0.32:
            break

    # IRMAA check
    thresholds = IRMAA_THRESHOLDS.get(filing_status, IRMAA_THRESHOLDS["married_jointly"])
    magi_after = current_income + conversion_amount
    irmaa_warning = magi_after > thresholds[0]

    favorable = (conversion_tax_cost / conversion_amount < retirement_rate
                 if conversion_amount > 0 else False)

    recommendations = []
    if net_benefit > 0:
        recommendations.append(
            f"Conversion is favorable: net benefit of ${net_benefit:,.0f}"
        )
    else:
        recommendations.append(
            f"Conversion may not be favorable: net cost of ${abs(net_benefit):,.0f}"
        )
    if marginal_rate > retirement_rate:
        recommendations.append("Current rate exceeds retirement rate - consider smaller conversion")
    elif marginal_rate < retirement_rate:
        recommendations.append("Current rate below retirement rate - conversion is tax-efficient")
    if bracket_space:
        lowest = list(bracket_space.keys())[0]
        space = list(bracket_space.values())[0]
        recommendations.append(f"${space:,.0f} of room in {lowest} bracket")
    if irmaa_warning:
        recommendations.append(
            "WARNING: May trigger Medicare IRMAA surcharges (2-year lookback)"
        )

    return {
        "scenario": "roth_conversion",
        "timestamp": datetime.now().isoformat(),
        "inputs": {
            "current_income": current_income,
            "conversion_amount": conversion_amount,
            "filing_status": filing_status,
            "current_marginal_rate": marginal_rate,
            "expected_retirement_rate": retirement_rate,
            "years_to_retirement": years_to_retirement,
            "growth_rate": growth_rate
        },
        "analysis": {
            "tax_before_conversion": tax_before,
            "tax_after_conversion": tax_after,
            "conversion_tax_cost": conversion_tax_cost,
            "effective_rate_on_conversion": round(
                conversion_tax_cost / conversion_amount * 100, 2
            ) if conversion_amount > 0 else 0,
            "future_value_of_conversion": round(future_value, 2),
            "tax_saved_in_retirement": round(tax_saved_in_retirement, 2),
            "net_benefit": round(net_benefit, 2),
            "conversion_favorable": favorable
        },
        "bracket_space": bracket_space,
        "irmaa_warning": irmaa_warning,
        "recommendations": recommendations
    }


def analyze_withdrawal_sequence(traditional_balance, roth_balance, taxable_balance,
                                 annual_need, filing_status, social_security=0,
                                 pension=0, years=30):
    """Compare withdrawal sequencing strategies over retirement."""

    strategies = {}

    # Strategy 1: Traditional first
    trad, roth, taxable = traditional_balance, roth_balance, taxable_balance
    total_taxes = 0
    for _ in range(years):
        income = social_security + pension
        trad_draw = min(max(annual_need - income, 0), trad)
        trad -= trad_draw
        income += trad_draw
        remaining = annual_need - income
        tax_draw = min(max(remaining, 0), taxable)
        taxable -= tax_draw
        remaining -= tax_draw
        roth_draw = min(max(remaining, 0), roth)
        roth -= roth_draw

        std_ded = STANDARD_DEDUCTIONS_2025.get(filing_status, 30000)
        taxable_inc = max(0, (social_security * 0.85 + pension + trad_draw) - std_ded)
        total_taxes += calculate_tax(taxable_inc, filing_status)
        trad *= 1.06
        roth *= 1.06
        taxable *= 1.05

    strategies["traditional_first"] = {
        "total_taxes": round(total_taxes, 2),
        "ending_total": round(trad + roth + taxable, 2)
    }

    # Strategy 2: Proportional
    trad, roth, taxable = traditional_balance, roth_balance, taxable_balance
    total_taxes = 0
    for _ in range(years):
        total_bal = trad + roth + taxable
        income = social_security + pension
        remaining = annual_need - income
        if total_bal > 0:
            trad_draw = min(remaining * (trad / total_bal), trad)
            roth_draw = min(remaining * (roth / total_bal), roth)
            tax_draw = min(remaining * (taxable / total_bal), taxable)
        else:
            trad_draw = roth_draw = tax_draw = 0
        trad -= trad_draw
        roth -= roth_draw
        taxable -= tax_draw

        std_ded = STANDARD_DEDUCTIONS_2025.get(filing_status, 30000)
        taxable_inc = max(0, (social_security * 0.85 + pension + trad_draw) - std_ded)
        total_taxes += calculate_tax(taxable_inc, filing_status)
        trad *= 1.06
        roth *= 1.06
        taxable *= 1.05

    strategies["proportional"] = {
        "total_taxes": round(total_taxes, 2),
        "ending_total": round(trad + roth + taxable, 2)
    }

    best = min(strategies.items(), key=lambda x: x[1]['total_taxes'])
    tax_savings = abs(
        strategies["traditional_first"]["total_taxes"]
        - strategies["proportional"]["total_taxes"]
    )

    return {
        "scenario": "withdrawal_sequence",
        "timestamp": datetime.now().isoformat(),
        "inputs": {
            "traditional_balance": traditional_balance,
            "roth_balance": roth_balance,
            "taxable_balance": taxable_balance,
            "annual_need": annual_need,
            "social_security": social_security,
            "pension": pension,
            "years": years,
            "filing_status": filing_status
        },
        "strategies": strategies,
        "best_strategy": best[0],
        "tax_savings_vs_worst": round(tax_savings, 2),
        "recommendations": [
            f"Best: {best[0].replace('_', ' ').title()} - "
            f"saves ${tax_savings:,.0f} over {years} years",
            "Consider annual bracket management to optimize further",
            "Review strategy annually as balances and tax law change"
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description='Tax Strategy Analyzer for Retirement Planning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Roth conversion:
    python tax_strategy.py --scenario roth-conversion --current-income 150000 \\
      --conversion-amount 50000 --current-tax-bracket 24 --retirement-bracket 22

  Withdrawal sequence:
    python tax_strategy.py --scenario withdrawal-sequence --traditional 1000000 \\
      --roth 500000 --taxable 300000 --annual-need 80000
        """
    )

    parser.add_argument('--scenario', required=True,
                        choices=['roth-conversion', 'withdrawal-sequence'])
    parser.add_argument('--filing-status', choices=['single', 'married_jointly'],
                        default='married_jointly')
    parser.add_argument('--output', type=str, help='Output JSON file path')
    parser.add_argument('--output-format', choices=['json', 'text'], default='text')

    # Roth conversion args
    parser.add_argument('--current-income', type=float)
    parser.add_argument('--conversion-amount', type=float)
    parser.add_argument('--current-tax-bracket', type=float, default=24)
    parser.add_argument('--retirement-bracket', type=float, default=22)
    parser.add_argument('--years-to-retirement', type=int, default=10)

    # Withdrawal sequence args
    parser.add_argument('--traditional', type=float)
    parser.add_argument('--roth', type=float, default=0)
    parser.add_argument('--taxable', type=float, default=0)
    parser.add_argument('--annual-need', type=float)
    parser.add_argument('--social-security', type=float, default=0)
    parser.add_argument('--pension', type=float, default=0)

    args = parser.parse_args()

    if args.scenario == 'roth-conversion':
        if not args.current_income or args.conversion_amount is None:
            parser.error("Roth conversion requires --current-income and --conversion-amount")
        result = analyze_roth_conversion(
            current_income=args.current_income,
            conversion_amount=args.conversion_amount,
            filing_status=args.filing_status,
            current_bracket=args.current_tax_bracket,
            retirement_bracket=args.retirement_bracket,
            years_to_retirement=args.years_to_retirement
        )
    elif args.scenario == 'withdrawal-sequence':
        if not args.traditional or not args.annual_need:
            parser.error("Withdrawal sequence requires --traditional and --annual-need")
        result = analyze_withdrawal_sequence(
            traditional_balance=args.traditional,
            roth_balance=args.roth,
            taxable_balance=args.taxable,
            annual_need=args.annual_need,
            filing_status=args.filing_status,
            social_security=args.social_security,
            pension=args.pension
        )

    if args.output_format == 'json' or args.output:
        output_json = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
            print(f"Results saved to: {args.output}")
        else:
            print(output_json)
    else:
        if args.scenario == 'roth-conversion':
            a = result['analysis']
            print("\n" + "=" * 60)
            print("ROTH CONVERSION ANALYSIS")
            print("=" * 60)
            print(f"\nConversion Amount:    ${args.conversion_amount:,.0f}")
            print(f"Tax Cost:             ${a['conversion_tax_cost']:,.0f}")
            print(f"Effective Rate:       {a['effective_rate_on_conversion']:.1f}%")
            print(f"Future Value:         ${a['future_value_of_conversion']:,.0f}")
            print(f"Tax Saved Retirement: ${a['tax_saved_in_retirement']:,.0f}")
            print(f"Net Benefit:          ${a['net_benefit']:,.0f}")
            print(f"Favorable:            {'YES' if a['conversion_favorable'] else 'NO'}")
            if result['bracket_space']:
                print(f"\nBRACKET SPACE:")
                for bracket, space in result['bracket_space'].items():
                    print(f"  {bracket}: ${space:,.0f}")
            print(f"\nRECOMMENDATIONS:")
            for rec in result['recommendations']:
                print(f"  * {rec}")
            print("=" * 60 + "\n")
        elif args.scenario == 'withdrawal-sequence':
            print("\n" + "=" * 60)
            print("WITHDRAWAL SEQUENCE ANALYSIS")
            print("=" * 60)
            for name, strat in result['strategies'].items():
                marker = " << BEST" if name == result['best_strategy'] else ""
                label = name.replace('_', ' ').title()
                print(f"\n{label}{marker}:")
                print(f"  Total Taxes:  ${strat['total_taxes']:,.0f}")
                print(f"  Ending Total: ${strat['ending_total']:,.0f}")
            print(f"\nTax savings: ${result['tax_savings_vs_worst']:,.0f}")
            print(f"\nRECOMMENDATIONS:")
            for rec in result['recommendations']:
                print(f"  * {rec}")
            print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
