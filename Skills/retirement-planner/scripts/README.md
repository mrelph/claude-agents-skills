# Retirement Planner Scripts

Python scripts for retirement planning calculations and analysis.

## Available Scripts

### monte_carlo.py ✅ (Implemented)
Monte Carlo simulation for probabilistic retirement projections.

**Status**: Fully functional
**Usage**: See script for argument details

### sync_portfolio_data.py ✅ (Implemented)
Import portfolio data from portfolio-analyzer skill.

**Status**: Fully functional
**Usage**: See script for argument details

### retirement_calculator.py 📋 (Placeholder)
Calculate comprehensive retirement income needs.

**TODO**: Implement expense modeling, replacement ratio calculations, healthcare cost projections

### ss_optimizer.py 📋 (Placeholder)
Optimize Social Security claiming strategy for singles and couples.

**TODO**: Implement break-even analysis, spousal benefit optimization, tax implications

### tax_strategy.py 📋 (Placeholder)
Tax planning for Roth conversions and withdrawal sequencing.

**TODO**: Implement Roth conversion bracket filling, IRMAA optimization, withdrawal sequencing

## Implementation Notes

The placeholder scripts need to be implemented based on your specific needs. The Monte Carlo and sync scripts provide working examples of the structure and patterns to follow.

Key Python packages you'll need:
- numpy (for calculations)
- pandas (for data manipulation)
- matplotlib/plotly (for charts)
- json (for data I/O)

## Running Scripts

All scripts are designed to be run from the retirement-planner directory:

```bash
cd retirement-planner
python scripts/monte_carlo.py --portfolio-value 1000000 --annual-spending 60000 --retirement-age 65
```

## Integration with Skill

The retirement-planner skill will invoke these scripts as needed during analysis. You can also run them manually for testing or custom scenarios.
