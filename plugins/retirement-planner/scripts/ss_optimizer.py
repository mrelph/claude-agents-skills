#!/usr/bin/env python3
"""
Social Security Claiming Strategy Optimizer

Analyzes optimal Social Security claiming ages for individuals and couples
by comparing lifetime benefits across different claiming scenarios.

Usage:
    python ss_optimizer.py --user-age 60 --user-fra-benefit 2800
    python ss_optimizer.py --user-age 58 --user-fra-benefit 3000 --spouse-age 55 --spouse-fra-benefit 1500
    python ss_optimizer.py --user-age 62 --user-fra-benefit 2500 --life-expectancy 95
"""

import argparse
import json
from datetime import datetime


# Reduction for claiming before FRA
EARLY_REDUCTION_FIRST_36 = 5 / 9 * 0.01   # per month, first 36 months
EARLY_REDUCTION_AFTER_36 = 5 / 12 * 0.01  # per month, beyond 36 months

# Delayed retirement credits
DELAYED_CREDIT_PER_MONTH = 2 / 3 * 0.01   # 8% per year


def calculate_benefit_at_age(fra_benefit, claiming_age, fra=67):
    """Calculate monthly benefit for a given claiming age."""
    if claiming_age < 62 or claiming_age > 70:
        return 0

    months_from_fra = (claiming_age - fra) * 12

    if months_from_fra < 0:
        months_early = abs(months_from_fra)
        if months_early <= 36:
            reduction = months_early * EARLY_REDUCTION_FIRST_36
        else:
            reduction = (36 * EARLY_REDUCTION_FIRST_36) + (
                (months_early - 36) * EARLY_REDUCTION_AFTER_36
            )
        return round(fra_benefit * (1 - reduction), 2)
    elif months_from_fra > 0:
        increase = months_from_fra * DELAYED_CREDIT_PER_MONTH
        return round(fra_benefit * (1 + increase), 2)
    else:
        return fra_benefit


def calculate_lifetime_benefits(monthly_benefit, claiming_age, life_expectancy, cola=0.02):
    """Calculate total lifetime benefits with COLA adjustments."""
    total = 0
    annual_benefit = monthly_benefit * 12

    for age in range(claiming_age, life_expectancy + 1):
        years_collecting = age - claiming_age
        adjusted_benefit = annual_benefit * ((1 + cola) ** years_collecting)
        total += adjusted_benefit

    return round(total, 2)


def analyze_claiming_strategies(user_fra_benefit, user_age, user_fra=67,
                                 spouse_fra_benefit=None, spouse_age=None,
                                 spouse_fra=67, life_expectancy=90,
                                 spouse_life_expectancy=90, cola=0.02):
    """Analyze all claiming age combinations and find optimal strategy."""

    individual_strategies = []
    for claim_age in range(62, 71):
        monthly = calculate_benefit_at_age(user_fra_benefit, claim_age, user_fra)
        annual = monthly * 12
        lifetime = calculate_lifetime_benefits(monthly, claim_age, life_expectancy, cola)
        pct_of_fra = (monthly / user_fra_benefit) * 100

        individual_strategies.append({
            "claiming_age": claim_age,
            "monthly_benefit": monthly,
            "annual_benefit": round(annual, 2),
            "percent_of_fra": round(pct_of_fra, 1),
            "lifetime_benefits": lifetime,
            "years_collecting": life_expectancy - claim_age
        })

    best_individual = max(individual_strategies, key=lambda x: x['lifetime_benefits'])

    result = {
        "timestamp": datetime.now().isoformat(),
        "inputs": {
            "user_age": user_age,
            "user_fra_benefit": user_fra_benefit,
            "user_fra": user_fra,
            "life_expectancy": life_expectancy,
            "cola_assumption": cola
        },
        "individual_analysis": {
            "strategies": individual_strategies,
            "optimal_claiming_age": best_individual['claiming_age'],
            "optimal_monthly_benefit": best_individual['monthly_benefit'],
            "optimal_lifetime_benefits": best_individual['lifetime_benefits']
        },
        "breakeven_analysis": []
    }

    # Breakeven analysis for key age pairs
    for early, later in [(62, 67), (62, 70), (67, 70)]:
        early_monthly = calculate_benefit_at_age(user_fra_benefit, early, user_fra)
        later_monthly = calculate_benefit_at_age(user_fra_benefit, later, user_fra)

        early_total = 0
        later_total = 0
        breakeven_age = None

        for age in range(62, 100):
            if age >= early:
                early_total += early_monthly * 12 * ((1 + cola) ** (age - early))
            if age >= later:
                later_total += later_monthly * 12 * ((1 + cola) ** (age - later))
            if later_total > early_total and breakeven_age is None:
                breakeven_age = age

        if breakeven_age:
            result['breakeven_analysis'].append({
                "claim_early": early,
                "claim_later": later,
                "breakeven_age": breakeven_age,
                "monthly_early": early_monthly,
                "monthly_later": later_monthly,
                "benefit_increase": round(later_monthly - early_monthly, 2)
            })

    # Spousal analysis
    if spouse_fra_benefit is not None and spouse_age is not None:
        result["inputs"]["spouse_age"] = spouse_age
        result["inputs"]["spouse_fra_benefit"] = spouse_fra_benefit
        result["inputs"]["spouse_life_expectancy"] = spouse_life_expectancy

        spousal_50pct = user_fra_benefit * 0.5

        spouse_strategies = []
        for claim_age in range(62, 71):
            own_monthly = calculate_benefit_at_age(spouse_fra_benefit, claim_age, spouse_fra)
            spousal_monthly = calculate_benefit_at_age(spousal_50pct, claim_age, spouse_fra)
            best_monthly = max(own_monthly, spousal_monthly)
            lifetime = calculate_lifetime_benefits(
                best_monthly, claim_age, spouse_life_expectancy, cola
            )

            spouse_strategies.append({
                "claiming_age": claim_age,
                "own_benefit": own_monthly,
                "spousal_benefit": round(spousal_monthly, 2),
                "best_benefit": best_monthly,
                "benefit_type": "own" if own_monthly >= spousal_monthly else "spousal",
                "lifetime_benefits": lifetime
            })

        best_spouse = max(spouse_strategies, key=lambda x: x['lifetime_benefits'])
        survivor_benefit = calculate_benefit_at_age(
            user_fra_benefit, best_individual['claiming_age'], user_fra
        )

        result["spousal_analysis"] = {
            "strategies": spouse_strategies,
            "optimal_claiming_age": best_spouse['claiming_age'],
            "optimal_benefit_type": best_spouse['benefit_type'],
            "optimal_monthly_benefit": best_spouse['best_benefit'],
            "survivor_benefit_estimate": round(survivor_benefit, 2),
            "note": "Survivor receives the higher of own benefit or deceased spouse's benefit"
        }

        combined_monthly = best_individual['monthly_benefit'] + best_spouse['best_benefit']
        result["combined_analysis"] = {
            "optimal_user_claim_age": best_individual['claiming_age'],
            "optimal_spouse_claim_age": best_spouse['claiming_age'],
            "combined_monthly_benefit": round(combined_monthly, 2),
            "combined_annual_benefit": round(combined_monthly * 12, 2)
        }

    # Recommendations
    recommendations = []
    if life_expectancy >= 85:
        recommendations.append(
            "With life expectancy 85+, delaying to 70 typically maximizes lifetime benefits"
        )
    recommendations.append(
        f"Optimal claiming age: {best_individual['claiming_age']} "
        f"for ${best_individual['monthly_benefit']:,.0f}/month "
        f"(${best_individual['lifetime_benefits'] / 1000:.0f}k lifetime)"
    )
    if result.get('breakeven_analysis'):
        be = result['breakeven_analysis'][-1]
        recommendations.append(
            f"Breakeven for delaying {be['claim_early']}->{be['claim_later']}: "
            f"age {be['breakeven_age']}"
        )
    result["recommendations"] = recommendations

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Social Security Claiming Strategy Optimizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Individual analysis:
    python ss_optimizer.py --user-age 60 --user-fra-benefit 2800

  Couple analysis:
    python ss_optimizer.py --user-age 60 --user-fra-benefit 3000 \\
      --spouse-age 58 --spouse-fra-benefit 1500

  Custom life expectancy:
    python ss_optimizer.py --user-age 62 --user-fra-benefit 2500 --life-expectancy 95
        """
    )

    parser.add_argument('--user-age', type=int, required=True, help='Current age')
    parser.add_argument('--user-fra-benefit', type=float, required=True,
                        help='Estimated monthly benefit at full retirement age')
    parser.add_argument('--spouse-age', type=int, default=None, help='Spouse current age')
    parser.add_argument('--spouse-fra-benefit', type=float, default=None,
                        help='Spouse monthly benefit at FRA')
    parser.add_argument('--life-expectancy', type=int, default=90,
                        help='Life expectancy (default: 90)')
    parser.add_argument('--spouse-life-expectancy', type=int, default=90,
                        help='Spouse life expectancy (default: 90)')
    parser.add_argument('--cola', type=float, default=2.0,
                        help='Annual COLA percent (default: 2.0)')
    parser.add_argument('--output', type=str, default=None, help='Output JSON file path')
    parser.add_argument('--output-format', choices=['json', 'text'], default='text')

    args = parser.parse_args()

    result = analyze_claiming_strategies(
        user_fra_benefit=args.user_fra_benefit,
        user_age=args.user_age,
        spouse_fra_benefit=args.spouse_fra_benefit,
        spouse_age=args.spouse_age,
        life_expectancy=args.life_expectancy,
        spouse_life_expectancy=args.spouse_life_expectancy,
        cola=args.cola / 100
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
        print("SOCIAL SECURITY CLAIMING OPTIMIZER")
        print("=" * 60)
        print(f"\nAge: {args.user_age}  |  FRA Benefit: "
              f"${args.user_fra_benefit:,.0f}/mo  |  "
              f"Life Expectancy: {args.life_expectancy}")

        ind = result['individual_analysis']
        print(f"\nCLAIMING AGE COMPARISON:")
        print(f"  {'Age':>4s}  {'Monthly':>10s}  {'Annual':>10s}  "
              f"{'% of FRA':>8s}  {'Lifetime':>12s}")
        print(f"  {'---':>4s}  {'---':>10s}  {'---':>10s}  "
              f"{'---':>8s}  {'---':>12s}")
        for s in ind['strategies']:
            marker = " << OPTIMAL" if s['claiming_age'] == ind['optimal_claiming_age'] else ""
            print(f"  {s['claiming_age']:>4d}  ${s['monthly_benefit']:>9,.0f}  "
                  f"${s['annual_benefit']:>9,.0f}  {s['percent_of_fra']:>6.1f}%  "
                  f"${s['lifetime_benefits']:>11,.0f}{marker}")

        if result.get('breakeven_analysis'):
            print(f"\nBREAKEVEN AGES:")
            for be in result['breakeven_analysis']:
                print(f"  Claim {be['claim_early']} vs {be['claim_later']}: "
                      f"Breakeven at age {be['breakeven_age']} "
                      f"(+${be['benefit_increase']:,.0f}/mo)")

        if result.get('spousal_analysis'):
            sa = result['spousal_analysis']
            print(f"\nSPOUSAL ANALYSIS:")
            print(f"  Optimal age:      {sa['optimal_claiming_age']} "
                  f"({sa['optimal_benefit_type']} benefit)")
            print(f"  Monthly benefit:  ${sa['optimal_monthly_benefit']:,.0f}")
            print(f"  Survivor benefit: ${sa['survivor_benefit_estimate']:,.0f}")

            ca = result['combined_analysis']
            print(f"\nCOMBINED OPTIMAL:")
            print(f"  Monthly: ${ca['combined_monthly_benefit']:,.0f}  |  "
                  f"Annual: ${ca['combined_annual_benefit']:,.0f}")

        print(f"\nRECOMMENDATIONS:")
        for rec in result['recommendations']:
            print(f"  * {rec}")

        print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
