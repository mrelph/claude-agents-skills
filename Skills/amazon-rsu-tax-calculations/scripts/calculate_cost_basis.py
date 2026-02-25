#!/usr/bin/env python3
"""
RSU Cost Basis Calculator

Calculates the correct cost basis for RSU shares based on the fair market value
at the vesting date. This is critical because broker-reported basis is often wrong.

Usage:
    python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50
    python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50 --sale-price 190.00
    python calculate_cost_basis.py --vesting-file vesting_data.json
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional


def calculate_single_lot_basis(shares: float, fmv_at_vesting: float) -> Dict:
    """
    Calculate cost basis for a single RSU lot.

    Args:
        shares: Number of shares
        fmv_at_vesting: Fair market value per share at vesting date

    Returns:
        Dictionary with cost basis calculation
    """
    total_basis = shares * fmv_at_vesting

    return {
        "shares": shares,
        "fmv_at_vesting": fmv_at_vesting,
        "cost_basis_per_share": fmv_at_vesting,
        "total_cost_basis": round(total_basis, 2)
    }


def calculate_gain_loss(shares: float, fmv_at_vesting: float,
                        sale_price: float, sale_fees: float = 0) -> Dict:
    """
    Calculate capital gain or loss on RSU sale.

    Args:
        shares: Number of shares sold
        fmv_at_vesting: Fair market value per share at vesting (cost basis)
        sale_price: Sale price per share
        sale_fees: Any fees or commissions on the sale

    Returns:
        Dictionary with gain/loss calculation
    """
    cost_basis = shares * fmv_at_vesting
    gross_proceeds = shares * sale_price
    net_proceeds = gross_proceeds - sale_fees
    gain_loss = net_proceeds - cost_basis

    return {
        "shares_sold": shares,
        "cost_basis_per_share": fmv_at_vesting,
        "total_cost_basis": round(cost_basis, 2),
        "sale_price_per_share": sale_price,
        "gross_proceeds": round(gross_proceeds, 2),
        "sale_fees": round(sale_fees, 2),
        "net_proceeds": round(net_proceeds, 2),
        "capital_gain_loss": round(gain_loss, 2),
        "gain_or_loss": "gain" if gain_loss >= 0 else "loss"
    }


def compare_basis(shares: float, correct_fmv: float,
                  incorrect_basis: float, sale_price: float) -> Dict:
    """
    Compare correct basis to incorrect broker-reported basis.
    Shows the tax impact of using wrong basis.

    Args:
        shares: Number of shares
        correct_fmv: Correct FMV at vesting (true cost basis)
        incorrect_basis: Broker-reported (incorrect) basis
        sale_price: Sale price per share

    Returns:
        Dictionary comparing correct vs incorrect calculations
    """
    proceeds = shares * sale_price

    correct_basis_total = shares * correct_fmv
    incorrect_basis_total = shares * incorrect_basis

    correct_gain = proceeds - correct_basis_total
    incorrect_gain = proceeds - incorrect_basis_total

    over_reported_gain = incorrect_gain - correct_gain
    basis_adjustment = correct_basis_total - incorrect_basis_total

    # Estimate tax impact (assuming 15% LTCG + 3.8% NIIT = 18.8%)
    estimated_overtax_ltcg = over_reported_gain * 0.188
    # If short-term, could be much higher (assuming 32% bracket + NIIT)
    estimated_overtax_stcg = over_reported_gain * 0.358

    return {
        "shares": shares,
        "proceeds": round(proceeds, 2),
        "correct_calculation": {
            "cost_basis_per_share": correct_fmv,
            "total_cost_basis": round(correct_basis_total, 2),
            "capital_gain": round(correct_gain, 2)
        },
        "incorrect_calculation": {
            "cost_basis_per_share": incorrect_basis,
            "total_cost_basis": round(incorrect_basis_total, 2),
            "capital_gain": round(incorrect_gain, 2)
        },
        "impact": {
            "over_reported_gain": round(over_reported_gain, 2),
            "form_8949_adjustment": round(basis_adjustment, 2),
            "estimated_overtax_if_ltcg": round(estimated_overtax_ltcg, 2),
            "estimated_overtax_if_stcg": round(estimated_overtax_stcg, 2)
        },
        "action_required": "File Form 8949 with adjustment code 'B'" if over_reported_gain != 0 else "None"
    }


def process_vesting_file(filepath: str) -> Dict:
    """
    Process a JSON file containing multiple vesting lots.

    Expected JSON format:
    {
        "vesting_lots": [
            {
                "vesting_date": "2024-01-15",
                "shares": 100,
                "fmv_at_vesting": 175.50,
                "grant_id": "ABC123"
            },
            ...
        ]
    }

    Returns:
        Dictionary with calculated cost basis for all lots
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    lots = data.get('vesting_lots', [])
    results = []
    total_shares = 0
    total_basis = 0

    for lot in lots:
        shares = lot['shares']
        fmv = lot['fmv_at_vesting']
        basis = shares * fmv

        lot_result = {
            "vesting_date": lot.get('vesting_date', 'Unknown'),
            "grant_id": lot.get('grant_id', 'N/A'),
            "shares": shares,
            "fmv_at_vesting": fmv,
            "total_cost_basis": round(basis, 2)
        }
        results.append(lot_result)
        total_shares += shares
        total_basis += basis

    return {
        "lots": results,
        "summary": {
            "total_lots": len(results),
            "total_shares": total_shares,
            "total_cost_basis": round(total_basis, 2),
            "average_cost_basis_per_share": round(total_basis / total_shares, 2) if total_shares > 0 else 0
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Calculate correct RSU cost basis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Calculate cost basis for 100 shares:
    python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50

  Calculate gain/loss on sale:
    python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50 --sale-price 190.00

  Compare correct vs broker-reported basis:
    python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50 --incorrect-basis 0 --sale-price 190.00

  Process multiple lots from file:
    python calculate_cost_basis.py --vesting-file vesting_data.json
        """
    )

    parser.add_argument('--shares', type=float, help='Number of shares')
    parser.add_argument('--fmv-at-vesting', type=float,
                        help='Fair market value per share at vesting date')
    parser.add_argument('--sale-price', type=float,
                        help='Sale price per share (optional, for gain/loss calculation)')
    parser.add_argument('--sale-fees', type=float, default=0,
                        help='Sale fees/commissions (default: 0)')
    parser.add_argument('--incorrect-basis', type=float,
                        help='Broker-reported incorrect basis (for comparison)')
    parser.add_argument('--vesting-file', type=str,
                        help='JSON file with multiple vesting lots')
    parser.add_argument('--output', type=str, help='Output file path (optional)')

    args = parser.parse_args()

    result = {}

    # Process vesting file if provided
    if args.vesting_file:
        result = process_vesting_file(args.vesting_file)

    # Single lot calculation
    elif args.shares and args.fmv_at_vesting:
        # Compare to incorrect basis if provided
        if args.incorrect_basis is not None and args.sale_price:
            result = compare_basis(
                args.shares,
                args.fmv_at_vesting,
                args.incorrect_basis,
                args.sale_price
            )
        # Calculate gain/loss if sale price provided
        elif args.sale_price:
            result = calculate_gain_loss(
                args.shares,
                args.fmv_at_vesting,
                args.sale_price,
                args.sale_fees
            )
        # Just calculate cost basis
        else:
            result = calculate_single_lot_basis(args.shares, args.fmv_at_vesting)

    else:
        parser.print_help()
        sys.exit(1)

    # Output results
    output_json = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"Results written to {args.output}")
    else:
        print(output_json)

    return result


if __name__ == '__main__':
    main()
