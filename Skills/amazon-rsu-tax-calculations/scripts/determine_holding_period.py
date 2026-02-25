#!/usr/bin/env python3
"""
RSU Holding Period Calculator

Determines whether an RSU sale qualifies for long-term or short-term capital gains
treatment based on the holding period from vesting date to sale date.

IRS Rule: Holding period > 1 year (365 days) = Long-term capital gain

Usage:
    python determine_holding_period.py --vesting-date 2023-01-15 --sale-date 2024-03-20
    python determine_holding_period.py --transactions-file transactions.json
"""

import argparse
import json
import sys
from datetime import datetime, date
from typing import Dict, List


def parse_date(date_str: str) -> date:
    """
    Parse a date string in various formats.

    Supported formats:
        - YYYY-MM-DD
        - MM/DD/YYYY
        - M/D/YYYY
    """
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_str}. Use YYYY-MM-DD or MM/DD/YYYY format.")


def calculate_holding_period(vesting_date: date, sale_date: date) -> Dict:
    """
    Calculate holding period and determine tax treatment.

    Args:
        vesting_date: Date shares vested (holding period starts here)
        sale_date: Date shares were sold

    Returns:
        Dictionary with holding period analysis
    """
    # Validate dates
    if sale_date < vesting_date:
        return {
            "error": True,
            "message": f"Sale date ({sale_date}) cannot be before vesting date ({vesting_date})"
        }

    # Calculate holding period
    holding_period = (sale_date - vesting_date).days

    # Determine treatment (> 1 year = long-term)
    is_long_term = holding_period > 365

    # Calculate the date that would qualify for long-term
    from datetime import timedelta
    long_term_date = vesting_date + timedelta(days=366)

    # If sold short-term, how many days until it would have been long-term?
    days_until_long_term = max(0, (long_term_date - sale_date).days) if not is_long_term else 0

    return {
        "vesting_date": vesting_date.isoformat(),
        "sale_date": sale_date.isoformat(),
        "holding_period_days": holding_period,
        "holding_period_description": describe_period(holding_period),
        "tax_treatment": "LONG-TERM" if is_long_term else "SHORT-TERM",
        "is_long_term": is_long_term,
        "long_term_qualifying_date": long_term_date.isoformat(),
        "days_until_long_term": days_until_long_term if not is_long_term else None,
        "tax_rate_info": {
            "short_term": "Taxed as ordinary income (10% - 37% depending on bracket)",
            "long_term": "Preferential rates (0%, 15%, or 20% depending on income)"
        },
        "recommendation": get_recommendation(is_long_term, days_until_long_term)
    }


def describe_period(days: int) -> str:
    """Convert days to human-readable period description."""
    if days == 0:
        return "Same day"
    elif days == 1:
        return "1 day"
    elif days < 30:
        return f"{days} days"
    elif days < 365:
        months = days // 30
        remaining_days = days % 30
        if remaining_days > 0:
            return f"~{months} month{'s' if months > 1 else ''}, {remaining_days} days"
        return f"~{months} month{'s' if months > 1 else ''}"
    else:
        years = days // 365
        remaining_days = days % 365
        if remaining_days > 0:
            months = remaining_days // 30
            if months > 0:
                return f"{years} year{'s' if years > 1 else ''}, ~{months} month{'s' if months > 1 else ''}"
        return f"{years} year{'s' if years > 1 else ''}"


def get_recommendation(is_long_term: bool, days_until: int) -> str:
    """Generate recommendation based on holding period."""
    if is_long_term:
        return "This sale qualifies for long-term capital gains treatment. Lower tax rates apply."

    if days_until and days_until <= 30:
        return f"WARNING: Only {days_until} day{'s' if days_until != 1 else ''} from long-term treatment! Consider waiting if possible."
    elif days_until and days_until <= 90:
        return f"This sale is short-term. {days_until} days until long-term treatment. Consider tax implications."
    else:
        return "This sale is short-term. Gains will be taxed as ordinary income at your marginal rate."


def calculate_tax_difference(gain: float, marginal_rate: float, ltcg_rate: float = 0.15) -> Dict:
    """
    Calculate the tax difference between short-term and long-term treatment.

    Args:
        gain: Capital gain amount
        marginal_rate: Taxpayer's marginal ordinary income rate (e.g., 0.32)
        ltcg_rate: Long-term capital gains rate (default 15%)

    Returns:
        Dictionary with tax comparison
    """
    short_term_tax = gain * marginal_rate
    long_term_tax = gain * ltcg_rate
    savings = short_term_tax - long_term_tax

    return {
        "capital_gain": gain,
        "short_term_tax": round(short_term_tax, 2),
        "short_term_rate": f"{marginal_rate * 100:.0f}%",
        "long_term_tax": round(long_term_tax, 2),
        "long_term_rate": f"{ltcg_rate * 100:.0f}%",
        "tax_savings_if_long_term": round(savings, 2),
        "savings_percentage": f"{(savings / short_term_tax * 100):.1f}%" if short_term_tax > 0 else "N/A"
    }


def process_multiple_transactions(transactions: List[Dict]) -> Dict:
    """
    Process multiple transactions and categorize by holding period.

    Args:
        transactions: List of transaction dicts with vesting_date, sale_date, shares, gain

    Returns:
        Summary with categorized transactions
    """
    short_term = []
    long_term = []
    total_st_gain = 0
    total_lt_gain = 0

    for txn in transactions:
        vesting_date = parse_date(txn['vesting_date'])
        sale_date = parse_date(txn['sale_date'])
        shares = txn.get('shares', 0)
        gain = txn.get('gain', 0)

        result = calculate_holding_period(vesting_date, sale_date)
        result['shares'] = shares
        result['gain'] = gain

        if result.get('is_long_term'):
            long_term.append(result)
            total_lt_gain += gain
        else:
            short_term.append(result)
            total_st_gain += gain

    return {
        "summary": {
            "total_transactions": len(transactions),
            "short_term_count": len(short_term),
            "long_term_count": len(long_term),
            "total_short_term_gain": round(total_st_gain, 2),
            "total_long_term_gain": round(total_lt_gain, 2)
        },
        "short_term_transactions": short_term,
        "long_term_transactions": long_term
    }


def main():
    parser = argparse.ArgumentParser(
        description='Determine RSU holding period and tax treatment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single transaction:
    python determine_holding_period.py --vesting-date 2023-01-15 --sale-date 2024-03-20

  With gain amount to show tax difference:
    python determine_holding_period.py --vesting-date 2023-01-15 --sale-date 2024-03-20 \\
        --gain 10000 --marginal-rate 0.32

  Process multiple transactions from file:
    python determine_holding_period.py --transactions-file transactions.json

  Example transactions.json format:
    {
      "transactions": [
        {"vesting_date": "2023-01-15", "sale_date": "2024-03-20", "shares": 100, "gain": 5000},
        {"vesting_date": "2023-06-15", "sale_date": "2024-01-20", "shares": 50, "gain": 2000}
      ]
    }
        """
    )

    parser.add_argument('--vesting-date', type=str,
                        help='Vesting date (YYYY-MM-DD or MM/DD/YYYY)')
    parser.add_argument('--sale-date', type=str,
                        help='Sale date (YYYY-MM-DD or MM/DD/YYYY)')
    parser.add_argument('--gain', type=float,
                        help='Capital gain amount (optional, for tax comparison)')
    parser.add_argument('--marginal-rate', type=float, default=0.32,
                        help='Marginal ordinary income tax rate (default: 0.32 = 32%%)')
    parser.add_argument('--ltcg-rate', type=float, default=0.15,
                        help='Long-term capital gains rate (default: 0.15 = 15%%)')
    parser.add_argument('--transactions-file', type=str,
                        help='JSON file with multiple transactions')
    parser.add_argument('--output', type=str, help='Output file path (optional)')

    args = parser.parse_args()

    result = {}

    # Process file with multiple transactions
    if args.transactions_file:
        with open(args.transactions_file, 'r') as f:
            data = json.load(f)
        transactions = data.get('transactions', data)
        result = process_multiple_transactions(transactions)

    # Process single transaction
    elif args.vesting_date and args.sale_date:
        vesting_date = parse_date(args.vesting_date)
        sale_date = parse_date(args.sale_date)
        result = calculate_holding_period(vesting_date, sale_date)

        # Add tax comparison if gain provided
        if args.gain:
            result['tax_comparison'] = calculate_tax_difference(
                args.gain,
                args.marginal_rate,
                args.ltcg_rate
            )

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
