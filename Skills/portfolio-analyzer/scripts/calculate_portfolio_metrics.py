#!/usr/bin/env python3
"""
Calculate portfolio metrics and performance indicators.
Takes normalized portfolio data and computes key analytics.
"""

import sys
import json
from collections import defaultdict


def calculate_portfolio_metrics(holdings):
    """
    Calculate comprehensive portfolio metrics from holdings data.
    
    Metrics include:
    - Total portfolio value
    - Asset allocation by security
    - Concentration metrics
    - Gain/loss statistics
    - Cost basis and returns
    """
    if not holdings:
        return {
            'error': 'No holdings data provided'
        }
    
    metrics = {
        'total_value': 0,
        'total_cost_basis': 0,
        'total_gain_loss': 0,
        'total_positions': len(holdings),
        'allocation': [],
        'concentration': {},
        'performance': {}
    }
    
    # Calculate totals and collect data
    valid_holdings = []
    for holding in holdings:
        value = holding.get('value')
        if value is not None and value > 0:
            valid_holdings.append(holding)
            metrics['total_value'] += value
            
            cost_basis = holding.get('cost_basis')
            if cost_basis:
                metrics['total_cost_basis'] += cost_basis
            
            gain_loss = holding.get('gain_loss')
            if gain_loss:
                metrics['total_gain_loss'] += gain_loss
    
    # Calculate allocation percentages
    for holding in valid_holdings:
        symbol = holding.get('symbol', 'Unknown')
        description = holding.get('description', '')
        value = holding.get('value', 0)
        
        allocation_pct = (value / metrics['total_value'] * 100) if metrics['total_value'] > 0 else 0
        
        metrics['allocation'].append({
            'symbol': symbol,
            'description': description,
            'value': value,
            'allocation_pct': round(allocation_pct, 2)
        })
    
    # Sort by allocation percentage (largest first)
    metrics['allocation'].sort(key=lambda x: x['allocation_pct'], reverse=True)
    
    # Concentration metrics
    if metrics['allocation']:
        top_5_concentration = sum(h['allocation_pct'] for h in metrics['allocation'][:5])
        top_10_concentration = sum(h['allocation_pct'] for h in metrics['allocation'][:10])
        
        metrics['concentration'] = {
            'top_position_pct': metrics['allocation'][0]['allocation_pct'],
            'top_5_pct': round(top_5_concentration, 2),
            'top_10_pct': round(top_10_concentration, 2),
            'positions_over_5pct': sum(1 for h in metrics['allocation'] if h['allocation_pct'] > 5),
            'positions_over_10pct': sum(1 for h in metrics['allocation'] if h['allocation_pct'] > 10)
        }
    
    # Performance metrics
    if metrics['total_cost_basis'] > 0:
        metrics['performance'] = {
            'total_return': round(metrics['total_gain_loss'], 2),
            'total_return_pct': round((metrics['total_gain_loss'] / metrics['total_cost_basis']) * 100, 2),
            'average_cost_basis': round(metrics['total_cost_basis'] / len(valid_holdings), 2),
            'average_holding_value': round(metrics['total_value'] / len(valid_holdings), 2)
        }
    
    # Round top-level totals
    metrics['total_value'] = round(metrics['total_value'], 2)
    metrics['total_cost_basis'] = round(metrics['total_cost_basis'], 2)
    metrics['total_gain_loss'] = round(metrics['total_gain_loss'], 2)
    
    return metrics


def analyze_sector_allocation(holdings):
    """
    Analyze allocation by sector/asset class if available.
    This is a placeholder - actual sector data would come from market data APIs.
    """
    asset_classes = defaultdict(lambda: {'count': 0, 'value': 0})
    
    for holding in holdings:
        asset_class = holding.get('asset_class', 'Unknown')
        value = holding.get('value', 0)
        
        if value:
            asset_classes[asset_class]['count'] += 1
            asset_classes[asset_class]['value'] += value
    
    return dict(asset_classes)


def identify_risk_factors(metrics):
    """
    Identify potential risk factors in the portfolio based on metrics.
    Returns list of concerns with severity levels.
    """
    concerns = []
    concentration = metrics.get('concentration', {})
    
    # Check for over-concentration
    if concentration.get('top_position_pct', 0) > 20:
        concerns.append({
            'type': 'concentration',
            'severity': 'high',
            'message': f"Top position represents {concentration['top_position_pct']:.1f}% of portfolio (>20% threshold)"
        })
    elif concentration.get('top_position_pct', 0) > 15:
        concerns.append({
            'type': 'concentration',
            'severity': 'medium',
            'message': f"Top position represents {concentration['top_position_pct']:.1f}% of portfolio (>15% threshold)"
        })
    
    # Check for excessive concentration in top holdings
    if concentration.get('top_5_pct', 0) > 60:
        concerns.append({
            'type': 'diversification',
            'severity': 'high',
            'message': f"Top 5 positions represent {concentration['top_5_pct']:.1f}% of portfolio (>60% threshold)"
        })
    
    # Check for too few positions
    total_positions = metrics.get('total_positions', 0)
    if total_positions < 10:
        concerns.append({
            'type': 'diversification',
            'severity': 'medium',
            'message': f"Portfolio has only {total_positions} positions (recommend 10-15 minimum)"
        })
    
    # Check for too many positions (difficult to manage)
    if total_positions > 50:
        concerns.append({
            'type': 'complexity',
            'severity': 'low',
            'message': f"Portfolio has {total_positions} positions (may be difficult to monitor effectively)"
        })
    
    return concerns


def main():
    if len(sys.argv) < 2:
        print("Usage: python calculate_portfolio_metrics.py <holdings_json>")
        print("\nCalculates metrics from normalized holdings JSON.")
        print("Input JSON should have format: {'holdings': [...]}")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    holdings = data.get('holdings', [])
    
    if not holdings:
        print("Error: No holdings found in input JSON", file=sys.stderr)
        sys.exit(1)
    
    # Calculate metrics
    metrics = calculate_portfolio_metrics(holdings)
    
    # Analyze sectors if data available
    sector_allocation = analyze_sector_allocation(holdings)
    if sector_allocation:
        metrics['sector_allocation'] = sector_allocation
    
    # Identify risk factors
    metrics['risk_factors'] = identify_risk_factors(metrics)
    
    # Output results
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
