#!/usr/bin/env python3
"""
Monte Carlo Retirement Simulation

Runs probabilistic projections to assess retirement plan robustness.
Uses historical returns, volatility, and inflation to model thousands of scenarios.
"""

import argparse
import json
import numpy as np
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monte Carlo Retirement Simulation')
    parser.add_argument('--portfolio-value', type=float, required=True,
                        help='Current portfolio value')
    parser.add_argument('--annual-spending', type=float, required=True,
                        help='Annual retirement spending need')
    parser.add_argument('--retirement-age', type=int, required=True,
                        help='Retirement age')
    parser.add_argument('--current-age', type=int, default=None,
                        help='Current age (if not yet retired)')
    parser.add_argument('--simulations', type=int, default=10000,
                        help='Number of Monte Carlo simulations')
    parser.add_argument('--years', type=int, default=40,
                        help='Years to simulate (default 40)')
    parser.add_argument('--return-mean', type=float, default=7.0,
                        help='Expected annual return (percent)')
    parser.add_argument('--return-std', type=float, default=15.0,
                        help='Return standard deviation (percent)')
    parser.add_argument('--inflation-mean', type=float, default=2.5,
                        help='Expected inflation rate (percent)')
    parser.add_argument('--inflation-std', type=float, default=1.5,
                        help='Inflation standard deviation (percent)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output JSON file path')
    return parser.parse_args()

def run_single_simulation(portfolio, spending, years, returns, inflation):
    """Run single Monte Carlo simulation path"""
    balance = portfolio
    balances = [balance]

    for year in range(years):
        # Apply return
        annual_return = returns[year]
        balance *= (1 + annual_return / 100)

        # Withdraw spending (inflated)
        inflation_factor = (1 + inflation[year] / 100) ** year
        withdrawal = spending * inflation_factor
        balance -= withdrawal

        balances.append(balance)

        # Check if depleted
        if balance <= 0:
            break

    return balances

def run_monte_carlo(args):
    """Run full Monte Carlo simulation"""
    np.random.seed(42)  # For reproducibility

    results = []
    success_count = 0

    for i in range(args.simulations):
        # Generate random returns and inflation for this simulation
        returns = np.random.normal(args.return_mean, args.return_std, args.years)
        inflation = np.random.normal(args.inflation_mean, args.inflation_std, args.years)

        # Run simulation
        balances = run_single_simulation(
            args.portfolio_value,
            args.annual_spending,
            args.years,
            returns,
            inflation
        )

        # Check if money lasted full period
        if len(balances) > args.years and balances[-1] > 0:
            success_count += 1

        results.append({
            'simulation': i + 1,
            'final_balance': balances[-1] if balances[-1] > 0 else 0,
            'years_lasted': len(balances) - 1,
            'success': len(balances) > args.years and balances[-1] > 0
        })

    success_rate = (success_count / args.simulations) * 100

    # Calculate percentiles for final balance
    final_balances = [r['final_balance'] for r in results if r['success']]

    output = {
        'timestamp': datetime.now().isoformat(),
        'inputs': {
            'portfolio_value': args.portfolio_value,
            'annual_spending': args.annual_spending,
            'retirement_age': args.retirement_age,
            'simulations': args.simulations,
            'years': args.years,
            'expected_return': args.return_mean,
            'return_volatility': args.return_std,
            'expected_inflation': args.inflation_mean,
            'inflation_volatility': args.inflation_std
        },
        'results': {
            'success_rate': success_rate,
            'successes': success_count,
            'failures': args.simulations - success_count,
            'percentiles': {
                '10th': np.percentile(final_balances, 10) if final_balances else 0,
                '25th': np.percentile(final_balances, 25) if final_balances else 0,
                '50th': np.percentile(final_balances, 50) if final_balances else 0,
                '75th': np.percentile(final_balances, 75) if final_balances else 0,
                '90th': np.percentile(final_balances, 90) if final_balances else 0
            }
        },
        'detailed_results': results[:100]  # Save first 100 for analysis
    }

    return output

def main():
    args = parse_arguments()

    print(f"Running Monte Carlo simulation with {args.simulations:,} simulations...")
    print(f"Portfolio: ${args.portfolio_value:,.0f}")
    print(f"Annual spending: ${args.annual_spending:,.0f}")
    print(f"Expected return: {args.return_mean}% ± {args.return_std}%")
    print(f"Expected inflation: {args.inflation_mean}% ± {args.inflation_std}%")
    print()

    results = run_monte_carlo(args)

    print(f"Success Rate: {results['results']['success_rate']:.1f}%")
    print(f"Successes: {results['results']['successes']:,}")
    print(f"Failures: {results['results']['failures']:,}")
    print()
    print("Final Balance Percentiles (successful cases):")
    for pct, value in results['results']['percentiles'].items():
        print(f"  {pct}: ${value:,.0f}")

    # Output to file or stdout
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    else:
        print("\nFull results:")
        print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
