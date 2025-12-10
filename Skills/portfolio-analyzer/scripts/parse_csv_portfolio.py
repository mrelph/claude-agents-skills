#!/usr/bin/env python3
"""
Parse CSV portfolio files into normalized format.
Handles various CSV export formats from brokers and portfolio tracking tools.
"""

import sys
import csv
import json
from pathlib import Path


def detect_csv_format(rows):
    """
    Detect the CSV format by examining headers.
    Returns a format type and column mapping.
    """
    if not rows or len(rows) < 1:
        return None, {}
    
    # Get header row (convert to lowercase for matching)
    header = [str(cell).lower().strip() for cell in rows[0]]
    
    # Common column name variations for standard fields
    mappings = {
        'symbol': ['symbol', 'ticker', 'stock symbol', 'security symbol'],
        'description': ['description', 'name', 'security name', 'security description', 'company'],
        'quantity': ['quantity', 'shares', 'units', 'qty', 'number of shares'],
        'price': ['price', 'current price', 'market price', 'last price', 'quote'],
        'value': ['value', 'market value', 'current value', 'total value', 'market val'],
        'cost_basis': ['cost basis', 'cost', 'total cost', 'purchase price', 'basis'],
        'gain_loss': ['gain/loss', 'gain', 'total gain/loss', 'unrealized gain/loss', 'p&l'],
        'gain_loss_pct': ['gain/loss %', 'gain %', '% gain/loss', 'return %'],
        'account': ['account', 'account number', 'account #', 'acct'],
        'asset_class': ['asset class', 'type', 'category', 'asset type'],
    }
    
    # Find column indices for each field
    col_map = {}
    for field, variations in mappings.items():
        for i, col in enumerate(header):
            if any(var in col for var in variations):
                col_map[field] = i
                break
    
    # Determine format type based on which columns are present
    if 'symbol' in col_map and 'quantity' in col_map:
        format_type = 'holdings'
    elif 'symbol' in col_map and any(k in col_map for k in ['gain_loss', 'value']):
        format_type = 'performance'
    else:
        format_type = 'generic'
    
    return format_type, col_map


def clean_numeric_value(value):
    """Clean and convert numeric string to float."""
    if not value or value == '-' or value == '':
        return None
    
    # Remove currency symbols, commas, parentheses (negative numbers)
    cleaned = str(value).replace('$', '').replace(',', '').replace('%', '')
    cleaned = cleaned.replace('(', '-').replace(')', '').strip()
    
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_csv_rows(rows, col_map):
    """Parse CSV rows into normalized holdings format."""
    holdings = []
    
    # Skip header row
    for row in rows[1:]:
        if not row or len(row) == 0:
            continue
        
        # Skip empty rows or total rows
        first_cell = str(row[0]).lower() if row and len(row) > 0 else ''
        if not first_cell or any(word in first_cell for word in ['total', 'sum', 'subtotal', 'grand total']):
            continue
        
        holding = {}
        
        # Extract each mapped field
        for field, idx in col_map.items():
            if idx < len(row):
                value = row[idx]
                
                # Handle numeric fields
                if field in ['quantity', 'price', 'value', 'cost_basis', 'gain_loss', 'gain_loss_pct']:
                    holding[field] = clean_numeric_value(value)
                else:
                    # Text fields
                    holding[field] = str(value).strip() if value else None
        
        # Only include if we have meaningful data (symbol or description)
        if holding.get('symbol') or holding.get('description'):
            holdings.append(holding)
    
    return holdings


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_csv_portfolio.py <csv_file>")
        print("\nParses portfolio CSV files into normalized JSON format.")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    if not Path(csv_path).exists():
        print(f"Error: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    
    # Read CSV file
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not rows:
        print("Error: CSV file is empty", file=sys.stderr)
        sys.exit(1)
    
    # Detect format and get column mapping
    format_type, col_map = detect_csv_format(rows)
    
    if not col_map:
        print("Error: Could not identify portfolio data columns in CSV", file=sys.stderr)
        print(f"Header found: {rows[0] if rows else 'None'}", file=sys.stderr)
        sys.exit(1)
    
    # Parse the rows
    holdings = parse_csv_rows(rows, col_map)
    
    # Output structured JSON
    result = {
        'source_file': csv_path,
        'format_type': format_type,
        'columns_found': list(col_map.keys()),
        'holdings': holdings,
        'total_holdings': len(holdings)
    }
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
