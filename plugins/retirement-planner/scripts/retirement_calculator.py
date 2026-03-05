#!/usr/bin/env python3
"""
Retirement Income Needs Calculator

Estimates annual retirement spending needs based on current income,
desired lifestyle, and expense category adjustments.

Usage:
    python retirement_calculator.py --current-income 150000 --retirement-age 65
    python retirement_calculator.py --current-income 200000 --retirement-age 62 --lifestyle affluent --current-age 55
    python retirement_calculator.py --current-income 150000 --retirement-age 65 --mortgage-paid
"""

import argparse
import json
from datetime import datetime


REPLACEMENT_RATIOS = {
    "basic": 0.60,
    "comfortable": 0.75,
    "affluent": 0.90
}


def calculate_retirement_needs(current_income, retirement_age, lifestyle,
                                mortgage_paid=False, current_age=None,
                                inflation_rate=0.03, healthcare_inflation=0.06):
    """Calculate estimated annual retirement spending needs."""

    base_ratio = REPLACEMENT_RATIOS.get(lifestyle, 0.75)
    base_spending = current_income * base_ratio

    if mortgage_paid:
        housing_savings = base_spending * 0.30 * 0.40
        base_spending -= housing_savings

    years_to_retirement = 0
    if current_age and current_age < retirement_age:
        years_to_retirement = retirement_age - current_age

    spending_at_retirement = base_spending * ((1 + inflation_rate) ** years_to_retirement)

    if retirement_age < 65:
        pre_medicare_years = min(65 - retirement_age, 10)
        annual_healthcare_pre_medicare = 20000 * ((1 + healthcare_inflation) ** years_to_retirement)
        annual_healthcare_medicare = 9000 * ((1 + healthcare_inflation) ** (years_to_retirement + pre_medicare_years))
    else:
        pre_medicare_years = 0
        annual_healthcare_pre_medicare = 0
        annual_healthcare_medicare = 9000 * ((1 + healthcare_inflation) ** years_to_retirement)

    expense_breakdown = {
        "housing": round(spending_at_retirement * 0.25, 2),
        "healthcare": round(annual_healthcare_pre_medicare if retirement_age < 65
                           else annual_healthcare_medicare, 2),
        "food_groceries": round(spending_at_retirement * 0.12, 2),
        "transportation": round(spending_at_retirement * 0.08, 2),
        "entertainment_travel": round(spending_at_retirement * 0.10, 2),
        "utilities_insurance": round(spending_at_retirement * 0.08, 2),
        "personal_misc": round(spending_at_retirement * 0.07, 2),
    }

    total_annual_need = sum(expense_breakdown.values())

    portfolio_targets = {
        "conservative_3pct": round(total_annual_need / 0.03, 2),
        "moderate_4pct": round(total_annual_need / 0.04, 2),
        "aggressive_5pct": round(total_annual_need / 0.05, 2),
    }

    spending_projections = []
    annual = total_annual_need
    for year in range(1, 41):
        annual *= (1 + inflation_rate)
        if year in [5, 10, 15, 20, 25, 30, 35, 40]:
            spending_projections.append({
                "year": year,
                "age": retirement_age + year,
                "annual_spending": round(annual, 2)
            })

    return {
        "timestamp": datetime.now().isoformat(),
        "inputs": {
            "current_income": current_income,
            "retirement_age": retirement_age,
            "current_age": current_age,
            "years_to_retirement": years_to_retirement,
            "lifestyle": lifestyle,
            "replacement_ratio": base_ratio,
            "mortgage_paid": mortgage_paid,
            "inflation_rate": inflation_rate,
            "healthcare_inflation": healthcare_inflation
        },
        "annual_spending_estimate": {
            "today_dollars": round(base_spending, 2),
            "at_retirement": round(total_annual_need, 2),
            "monthly_at_retirement": round(total_annual_need / 12, 2)
        },
        "expense_breakdown": expense_breakdown,
        "healthcare_planning": {
            "pre_medicare_years": pre_medicare_years,
            "annual_pre_medicare_cost": round(annual_healthcare_pre_medicare, 2),
            "annual_medicare_cost": round(annual_healthcare_medicare, 2),
            "note": "Healthcare costs inflate faster than general expenses (5-6% vs 2-3%)"
        },
        "portfolio_targets": portfolio_targets,
        "spending_projections": spending_projections
    }


def main():
    parser = argparse.ArgumentParser(
        description='Calculate retirement income needs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic calculation:
    python retirement_calculator.py --current-income 150000 --retirement-age 65

  With lifestyle and current age:
    python retirement_calculator.py --current-income 200000 --retirement-age 62 --lifestyle affluent --current-age 55

  Mortgage paid off:
    python retirement_calculator.py --current-income 150000 --retirement-age 65 --mortgage-paid
        """
    )

    parser.add_argument('--current-income', type=float, required=True,
                        help='Current annual gross income')
    parser.add_argument('--retirement-age', type=int, required=True,
                        help='Planned retirement age')
    parser.add_argument('--current-age', type=int, default=None,
                        help='Current age (for inflation projection)')
    parser.add_argument('--lifestyle', choices=['basic', 'comfortable', 'affluent'],
                        default='comfortable', help='Desired retirement lifestyle')
    parser.add_argument('--mortgage-paid', action='store_true',
                        help='Mortgage will be paid off at retirement')
    parser.add_argument('--inflation', type=float, default=3.0,
                        help='Expected general inflation rate (percent, default 3.0)')
    parser.add_argument('--healthcare-inflation', type=float, default=6.0,
                        help='Expected healthcare inflation rate (percent, default 6.0)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output JSON file path')
    parser.add_argument('--output-format', choices=['json', 'text'], default='text',
                        help='Output format')

    args = parser.parse_args()

    result = calculate_retirement_needs(
        current_income=args.current_income,
        retirement_age=args.retirement_age,
        lifestyle=args.lifestyle,
        mortgage_paid=args.mortgage_paid,
        current_age=args.current_age,
        inflation_rate=args.inflation / 100,
        healthcare_inflation=args.healthcare_inflation / 100
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
        print("\n" + "=" * 60)
        print("RETIREMENT INCOME NEEDS CALCULATOR")
        print("=" * 60)
        print(f"\nCurrent Income:     ${args.current_income:,.0f}")
        print(f"Retirement Age:     {args.retirement_age}")
        if args.current_age:
            print(f"Current Age:        {args.current_age}")
            print(f"Years to Retire:    {result['inputs']['years_to_retirement']}")
        print(f"Lifestyle:          {args.lifestyle.title()}")
        print(f"Replacement Ratio:  {result['inputs']['replacement_ratio']:.0%}")
        print(f"Mortgage Paid:      {'Yes' if args.mortgage_paid else 'No'}")

        est = result['annual_spending_estimate']
        print(f"\nESTIMATED ANNUAL SPENDING:")
        print(f"  Today's dollars:    ${est['today_dollars']:,.0f}")
        print(f"  At retirement:      ${est['at_retirement']:,.0f}")
        print(f"  Monthly:            ${est['monthly_at_retirement']:,.0f}")

        print(f"\nEXPENSE BREAKDOWN (at retirement):")
        for category, amount in result['expense_breakdown'].items():
            label = category.replace('_', ' ').title()
            print(f"  {label:25s} ${amount:>10,.0f}")

        hc = result['healthcare_planning']
        print(f"\nHEALTHCARE PLANNING:")
        if hc['pre_medicare_years'] > 0:
            print(f"  Pre-Medicare years:   {hc['pre_medicare_years']}")
            print(f"  Annual cost (pre-65): ${hc['annual_pre_medicare_cost']:,.0f}")
        print(f"  Annual cost (65+):    ${hc['annual_medicare_cost']:,.0f}")

        pt = result['portfolio_targets']
        print(f"\nPORTFOLIO TARGETS:")
        print(f"  Conservative (3%):  ${pt['conservative_3pct']:,.0f}")
        print(f"  Moderate (4%):      ${pt['moderate_4pct']:,.0f}")
        print(f"  Aggressive (5%):    ${pt['aggressive_5pct']:,.0f}")

        print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
