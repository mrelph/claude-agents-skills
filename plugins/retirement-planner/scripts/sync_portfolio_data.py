#!/usr/bin/env python3
"""
Sync Portfolio Data from Portfolio Analyzer

Imports portfolio holdings and metrics from the portfolio-analyzer skill.
"""

import argparse
import json
import shutil
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description='Import portfolio data')
    parser.add_argument('--source', type=str, required=True,
                        help='Path to portfolio holdings.json file')
    parser.add_argument('--metrics', type=str, default=None,
                        help='Path to portfolio metrics.json file (optional)')
    return parser.parse_args()

def import_portfolio_data(args):
    """Import and process portfolio data"""

    # Read source holdings
    with open(args.source, 'r') as f:
        holdings = json.load(f)

    # Calculate total portfolio value
    total_value = sum(h.get('value', 0) for h in holdings)

    # Determine asset allocation
    # This is placeholder logic - actual implementation would be more sophisticated
    stock_allocation = 0.70  # Default assumption
    bond_allocation = 0.30

    portfolio_data = {
        'total_value': total_value,
        'asset_allocation': {
            'stocks': stock_allocation,
            'bonds': bond_allocation
        },
        'holdings_count': len(holdings),
        'imported_from': args.source
    }

    # If metrics provided, import additional data
    if args.metrics:
        with open(args.metrics, 'r') as f:
            metrics = json.load(f)

        portfolio_data['risk_level'] = metrics.get('risk_level', 'moderate')
        portfolio_data['concentration'] = metrics.get('top_5_concentration', 0)

    # Save to data directory
    output_path = Path('data/current_portfolio.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(portfolio_data, f, indent=2)

    print(f"Portfolio data imported successfully!")
    print(f"Total value: ${total_value:,.0f}")
    print(f"Asset allocation: {stock_allocation:.0%} stocks, {bond_allocation:.0%} bonds")
    print(f"Saved to: {output_path}")

    return portfolio_data

def main():
    args = parse_arguments()

    print("Importing portfolio data from portfolio-analyzer...")
    import_portfolio_data(args)

if __name__ == '__main__':
    main()
