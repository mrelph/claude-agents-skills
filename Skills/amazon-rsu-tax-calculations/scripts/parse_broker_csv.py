#!/usr/bin/env python3
"""
Broker CSV Parser for RSU Transactions

Parses CSV exports from common brokers (Morgan Stanley, Fidelity, Schwab, E*TRADE)
and normalizes the data for RSU tax calculations.

Handles various CSV formats and field naming conventions used by different brokers.

Usage:
    python parse_broker_csv.py --file transactions.csv --broker morgan_stanley
    python parse_broker_csv.py --file transactions.csv --auto-detect
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional


# Field mapping for different brokers
BROKER_FIELD_MAPPINGS = {
    "morgan_stanley": {
        "symbol": ["Symbol", "Ticker", "Security"],
        "description": ["Description", "Security Name", "Security Description"],
        "transaction_type": ["Transaction Type", "Type", "Action"],
        "date": ["Date", "Trade Date", "Transaction Date", "Settlement Date"],
        "quantity": ["Quantity", "Shares", "Units", "Qty"],
        "price": ["Price", "Price Per Share", "Unit Price", "Execution Price"],
        "proceeds": ["Proceeds", "Amount", "Total", "Net Amount"],
        "cost_basis": ["Cost Basis", "Cost", "Basis", "Purchase Price"],
        "gain_loss": ["Gain/Loss", "Gain", "Loss", "Realized Gain/Loss"],
        "fees": ["Fees", "Commission", "Transaction Fees"]
    },
    "fidelity": {
        "symbol": ["Symbol", "Security"],
        "description": ["Description", "Security Description"],
        "transaction_type": ["Action", "Transaction Type"],
        "date": ["Run Date", "Trade Date", "Settlement Date"],
        "quantity": ["Quantity", "Shares"],
        "price": ["Price ($)", "Price", "Price Per Share"],
        "proceeds": ["Amount ($)", "Amount", "Proceeds"],
        "cost_basis": ["Cost Basis", "Cost Basis ($)"],
        "gain_loss": ["Gain/Loss ($)", "Gain/Loss"],
        "fees": ["Fees ($)", "Commission ($)"]
    },
    "schwab": {
        "symbol": ["Symbol"],
        "description": ["Description"],
        "transaction_type": ["Action"],
        "date": ["Date"],
        "quantity": ["Quantity"],
        "price": ["Price"],
        "proceeds": ["Amount"],
        "cost_basis": ["Cost Basis"],
        "gain_loss": ["Gain/Loss"],
        "fees": ["Fees & Comm"]
    },
    "etrade": {
        "symbol": ["Symbol", "Security Symbol"],
        "description": ["Description", "Security Description"],
        "transaction_type": ["Transaction Type", "TransactionType"],
        "date": ["Date", "TransactionDate"],
        "quantity": ["Quantity", "Shares"],
        "price": ["Price", "Share Price"],
        "proceeds": ["Amount", "Principal"],
        "cost_basis": ["Cost Basis", "Adjusted Cost Basis"],
        "gain_loss": ["Gain/Loss", "GainLoss"],
        "fees": ["Commission", "Fees"]
    }
}

# Vesting-specific field mappings
VESTING_FIELD_MAPPINGS = {
    "morgan_stanley": {
        "vesting_date": ["Release Date", "Vest Date", "Vesting Date"],
        "grant_date": ["Grant Date", "Award Date"],
        "grant_id": ["Grant ID", "Award ID", "Grant Number"],
        "shares_released": ["Shares Released", "Shares Vested", "Released Shares"],
        "release_price": ["Release Price", "FMV", "Fair Market Value", "Price at Release"],
        "shares_withheld": ["Shares Withheld", "Tax Shares", "Withheld for Taxes"],
        "net_shares": ["Net Shares", "Shares Deposited", "Net Released"]
    }
}


def detect_broker(headers: List[str]) -> Optional[str]:
    """
    Auto-detect broker based on CSV headers.

    Args:
        headers: List of column headers from CSV

    Returns:
        Broker name or None if not detected
    """
    headers_lower = [h.lower().strip() for h in headers]

    # Morgan Stanley specific fields
    if any('release price' in h for h in headers_lower) or any('shareworks' in h for h in headers_lower):
        return "morgan_stanley"

    # Fidelity specific fields
    if any('run date' in h for h in headers_lower) or any('fidelity' in h for h in headers_lower):
        return "fidelity"

    # Schwab specific patterns
    if 'fees & comm' in headers_lower:
        return "schwab"

    # E*TRADE specific
    if any('etrade' in h for h in headers_lower) or 'transactiontype' in headers_lower:
        return "etrade"

    return None


def find_matching_field(row: Dict, field_options: List[str]) -> Optional[str]:
    """
    Find the first matching field from a list of possible field names.

    Args:
        row: Dictionary representing a CSV row
        field_options: List of possible field names to look for

    Returns:
        The value if found, None otherwise
    """
    for field in field_options:
        if field in row:
            return row[field]
        # Try case-insensitive match
        for key in row.keys():
            if key.lower().strip() == field.lower().strip():
                return row[key]
    return None


def parse_date(date_str: str) -> Optional[str]:
    """Parse date string to ISO format."""
    if not date_str or date_str.strip() == '':
        return None

    formats = [
        "%m/%d/%Y",
        "%Y-%m-%d",
        "%m/%d/%y",
        "%d-%b-%Y",
        "%b %d, %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return date_str  # Return original if can't parse


def parse_number(value: str) -> Optional[float]:
    """Parse a numeric string, handling currency formatting."""
    if not value or value.strip() == '':
        return None

    # Remove currency symbols and formatting
    cleaned = value.strip()
    cleaned = cleaned.replace('$', '').replace(',', '').replace('(', '-').replace(')', '')

    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_sale_transactions(filepath: str, broker: str) -> Dict:
    """
    Parse sale transactions from broker CSV.

    Args:
        filepath: Path to CSV file
        broker: Broker name for field mapping

    Returns:
        Dictionary with parsed transactions
    """
    mapping = BROKER_FIELD_MAPPINGS.get(broker, BROKER_FIELD_MAPPINGS["morgan_stanley"])

    transactions = []
    errors = []

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        # Try to detect delimiter
        sample = f.read(4096)
        f.seek(0)

        dialect = csv.Sniffer().sniff(sample, delimiters=',\t;')
        reader = csv.DictReader(f, dialect=dialect)

        for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 for header)
            try:
                # Extract fields using mapping
                symbol = find_matching_field(row, mapping.get("symbol", []))
                date = find_matching_field(row, mapping.get("date", []))
                quantity = find_matching_field(row, mapping.get("quantity", []))
                price = find_matching_field(row, mapping.get("price", []))
                proceeds = find_matching_field(row, mapping.get("proceeds", []))
                cost_basis = find_matching_field(row, mapping.get("cost_basis", []))
                gain_loss = find_matching_field(row, mapping.get("gain_loss", []))
                txn_type = find_matching_field(row, mapping.get("transaction_type", []))

                # Skip non-sale transactions
                if txn_type and txn_type.lower() not in ['sell', 'sale', 'sold', 'release', 'exercise']:
                    continue

                # Filter for Amazon stock only
                if symbol and 'AMZN' not in symbol.upper() and 'AMAZON' not in symbol.upper():
                    continue

                transaction = {
                    "row_number": row_num,
                    "symbol": symbol,
                    "date": parse_date(date) if date else None,
                    "quantity": parse_number(quantity),
                    "price": parse_number(price),
                    "proceeds": parse_number(proceeds),
                    "cost_basis_reported": parse_number(cost_basis),
                    "gain_loss_reported": parse_number(gain_loss),
                    "transaction_type": txn_type,
                    "raw_data": dict(row)
                }

                # Validate essential fields
                if transaction["quantity"] and (transaction["price"] or transaction["proceeds"]):
                    transactions.append(transaction)
                else:
                    errors.append({
                        "row": row_num,
                        "issue": "Missing essential fields (quantity, price, or proceeds)",
                        "data": dict(row)
                    })

            except Exception as e:
                errors.append({
                    "row": row_num,
                    "issue": str(e),
                    "data": dict(row)
                })

    # Calculate totals
    total_shares = sum(t["quantity"] or 0 for t in transactions)
    total_proceeds = sum(t["proceeds"] or 0 for t in transactions)
    total_reported_basis = sum(t["cost_basis_reported"] or 0 for t in transactions)

    return {
        "file": filepath,
        "broker": broker,
        "transactions": transactions,
        "summary": {
            "total_transactions": len(transactions),
            "total_shares_sold": total_shares,
            "total_proceeds": round(total_proceeds, 2),
            "total_reported_cost_basis": round(total_reported_basis, 2),
            "reported_gain_loss": round(total_proceeds - total_reported_basis, 2)
        },
        "warnings": [
            {
                "message": "Cost basis reported may be INCORRECT. Verify against vesting FMV.",
                "affected_rows": [t["row_number"] for t in transactions if t["cost_basis_reported"] == 0]
            }
        ] if any(t["cost_basis_reported"] == 0 for t in transactions) else [],
        "errors": errors
    }


def parse_vesting_transactions(filepath: str, broker: str = "morgan_stanley") -> Dict:
    """
    Parse RSU vesting records from broker CSV.

    Args:
        filepath: Path to CSV file
        broker: Broker name for field mapping

    Returns:
        Dictionary with parsed vesting records
    """
    mapping = VESTING_FIELD_MAPPINGS.get(broker, VESTING_FIELD_MAPPINGS["morgan_stanley"])

    vesting_records = []
    errors = []

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        sample = f.read(4096)
        f.seek(0)

        dialect = csv.Sniffer().sniff(sample, delimiters=',\t;')
        reader = csv.DictReader(f, dialect=dialect)

        for row_num, row in enumerate(reader, start=2):
            try:
                vesting_date = find_matching_field(row, mapping.get("vesting_date", []))
                grant_date = find_matching_field(row, mapping.get("grant_date", []))
                grant_id = find_matching_field(row, mapping.get("grant_id", []))
                shares_released = find_matching_field(row, mapping.get("shares_released", []))
                release_price = find_matching_field(row, mapping.get("release_price", []))
                shares_withheld = find_matching_field(row, mapping.get("shares_withheld", []))
                net_shares = find_matching_field(row, mapping.get("net_shares", []))

                if not shares_released or not release_price:
                    continue

                shares = parse_number(shares_released)
                fmv = parse_number(release_price)
                withheld = parse_number(shares_withheld) if shares_withheld else 0
                net = parse_number(net_shares) if net_shares else (shares - withheld if shares else 0)

                record = {
                    "row_number": row_num,
                    "vesting_date": parse_date(vesting_date) if vesting_date else None,
                    "grant_date": parse_date(grant_date) if grant_date else None,
                    "grant_id": grant_id,
                    "shares_vested": shares,
                    "fmv_at_vesting": fmv,
                    "vesting_income": round(shares * fmv, 2) if shares and fmv else None,
                    "shares_withheld_for_taxes": withheld,
                    "net_shares_received": net,
                    "cost_basis_per_share": fmv,  # This is the KEY value for tax calculations
                    "raw_data": dict(row)
                }

                vesting_records.append(record)

            except Exception as e:
                errors.append({
                    "row": row_num,
                    "issue": str(e),
                    "data": dict(row)
                })

    # Calculate totals
    total_shares_vested = sum(r["shares_vested"] or 0 for r in vesting_records)
    total_vesting_income = sum(r["vesting_income"] or 0 for r in vesting_records)
    total_net_shares = sum(r["net_shares_received"] or 0 for r in vesting_records)
    total_cost_basis = sum((r["shares_vested"] or 0) * (r["fmv_at_vesting"] or 0) for r in vesting_records)

    return {
        "file": filepath,
        "broker": broker,
        "vesting_records": vesting_records,
        "summary": {
            "total_vesting_events": len(vesting_records),
            "total_shares_vested": total_shares_vested,
            "total_vesting_income": round(total_vesting_income, 2),
            "total_net_shares_received": total_net_shares,
            "total_cost_basis": round(total_cost_basis, 2)
        },
        "tax_notes": {
            "w2_verification": f"Total vesting income of ${total_vesting_income:,.2f} should be included in W-2 Box 1",
            "cost_basis_reminder": "Use FMV at vesting date as cost basis for each lot when calculating gains/losses"
        },
        "errors": errors
    }


def main():
    parser = argparse.ArgumentParser(
        description='Parse broker CSV files for RSU tax calculations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Parse sales from Morgan Stanley:
    python parse_broker_csv.py --file sales.csv --broker morgan_stanley --type sales

  Parse vesting records:
    python parse_broker_csv.py --file vesting.csv --broker morgan_stanley --type vesting

  Auto-detect broker:
    python parse_broker_csv.py --file transactions.csv --auto-detect --type sales

Supported brokers: morgan_stanley, fidelity, schwab, etrade
        """
    )

    parser.add_argument('--file', required=True, help='Path to CSV file')
    parser.add_argument('--broker', choices=['morgan_stanley', 'fidelity', 'schwab', 'etrade'],
                        help='Broker name')
    parser.add_argument('--auto-detect', action='store_true',
                        help='Auto-detect broker from CSV headers')
    parser.add_argument('--type', choices=['sales', 'vesting'], default='sales',
                        help='Type of transactions to parse')
    parser.add_argument('--output', help='Output file path (optional)')

    args = parser.parse_args()

    # Determine broker
    broker = args.broker
    if args.auto_detect or not broker:
        with open(args.file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)
            broker = detect_broker(headers)
            if not broker:
                print("Warning: Could not auto-detect broker. Using morgan_stanley as default.")
                broker = "morgan_stanley"
            else:
                print(f"Detected broker: {broker}")

    # Parse based on type
    if args.type == 'vesting':
        result = parse_vesting_transactions(args.file, broker)
    else:
        result = parse_sale_transactions(args.file, broker)

    # Output
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
