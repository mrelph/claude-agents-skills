#!/usr/bin/env python3
"""
Extract portfolio holdings and transactions from PDF statements.
Handles common brokerage statement formats (Fidelity, Schwab, Vanguard, etc.)
"""

import sys
import re
import json
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Install with: pip install pdfplumber --break-system-packages", file=sys.stderr)
    sys.exit(1)


def extract_tables_from_pdf(pdf_path):
    """Extract all tables from PDF."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:  # Skip empty tables
                    tables.append({
                        'page': page_num,
                        'data': table
                    })
    return tables


def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF."""
    text_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                text_content.append({
                    'page': page_num,
                    'text': text
                })
    return text_content


def find_account_info(text_content):
    """Extract account number, name, and statement period."""
    info = {}
    
    # Common patterns for account information
    patterns = {
        'account_number': r'Account\s*(?:Number|#)?\s*:?\s*([A-Z0-9-]+)',
        'account_name': r'Account\s*(?:Name|Owner)\s*:?\s*([A-Za-z\s\.]+)',
        'statement_period': r'(?:Statement|Period)\s*(?:Date|Period)?\s*:?\s*([\d/\-\s]+(?:to|through|\-)[\d/\-\s]+)',
        'statement_date': r'(?:Statement|As of)\s*Date\s*:?\s*([\d/\-]+)',
    }
    
    full_text = ' '.join([item['text'] for item in text_content])
    
    for key, pattern in patterns.items():
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            info[key] = match.group(1).strip()
    
    return info


def identify_holdings_table(tables):
    """
    Identify which table contains portfolio holdings.
    Look for tables with headers like Symbol, Quantity, Value, etc.
    """
    holding_keywords = ['symbol', 'ticker', 'quantity', 'shares', 'market value', 
                       'current value', 'description', 'security']
    
    for table in tables:
        if not table['data'] or len(table['data']) < 2:
            continue
            
        # Check header row
        header = [str(cell).lower() if cell else '' for cell in table['data'][0]]
        
        # Count how many holding-related keywords are in the header
        keyword_matches = sum(1 for keyword in holding_keywords 
                            if any(keyword in h for h in header))
        
        if keyword_matches >= 3:  # At least 3 relevant columns
            return table
    
    return None


def parse_holdings_table(table_data):
    """Parse a holdings table into structured format."""
    if not table_data or len(table_data) < 2:
        return []
    
    headers = [str(cell).lower().strip() if cell else '' for cell in table_data[0]]
    holdings = []
    
    # Map common header variations to standard fields
    header_map = {
        'symbol': ['symbol', 'ticker'],
        'description': ['description', 'security', 'security description', 'name'],
        'quantity': ['quantity', 'shares', 'units'],
        'price': ['price', 'current price', 'market price', 'unit price'],
        'value': ['value', 'market value', 'current value', 'total value'],
        'cost_basis': ['cost basis', 'cost', 'purchase price'],
        'gain_loss': ['gain/loss', 'gain', 'unrealized gain/loss'],
    }
    
    # Find column indices for each field
    col_indices = {}
    for field, variations in header_map.items():
        for i, header in enumerate(headers):
            if any(var in header for var in variations):
                col_indices[field] = i
                break
    
    # Parse data rows
    for row in table_data[1:]:
        if not row or len(row) == 0:
            continue
            
        # Skip totals/summary rows
        first_cell = str(row[0]).lower() if row[0] else ''
        if any(word in first_cell for word in ['total', 'subtotal', 'sum', 'balance']):
            continue
        
        holding = {}
        for field, idx in col_indices.items():
            if idx < len(row):
                value = row[idx]
                if value:
                    # Clean numeric values
                    if field in ['quantity', 'price', 'value', 'cost_basis', 'gain_loss']:
                        value = str(value).replace('$', '').replace(',', '').replace('(', '-').replace(')', '').strip()
                        try:
                            holding[field] = float(value) if value and value != '-' else None
                        except ValueError:
                            holding[field] = value
                    else:
                        holding[field] = str(value).strip()
        
        # Only add if we have at least a symbol or description
        if holding.get('symbol') or holding.get('description'):
            holdings.append(holding)
    
    return holdings


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_portfolio.py <pdf_file>")
        print("\nExtracts portfolio holdings from brokerage PDF statements.")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    # Extract content
    tables = extract_tables_from_pdf(pdf_path)
    text_content = extract_text_from_pdf(pdf_path)
    
    # Find account information
    account_info = find_account_info(text_content)
    
    # Find and parse holdings table
    holdings_table = identify_holdings_table(tables)
    holdings = []
    if holdings_table:
        holdings = parse_holdings_table(holdings_table['data'])
    
    # Output structured JSON
    result = {
        'source_file': pdf_path,
        'account_info': account_info,
        'holdings': holdings,
        'total_tables_found': len(tables),
    }
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
