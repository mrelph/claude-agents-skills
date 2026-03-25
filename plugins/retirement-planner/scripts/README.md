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

### retirement_calculator.py ✅ (Implemented)
Calculate comprehensive retirement income needs with expense modeling, replacement ratios (basic/comfortable/affluent), healthcare cost projections for pre-Medicare and Medicare years, and portfolio size targets based on withdrawal rates.

**Status**: Fully functional
**Usage**: `python retirement_calculator.py --current-income 150000 --retirement-age 65 --lifestyle comfortable`

### ss_optimizer.py ✅ (Implemented)
Optimize Social Security claiming strategy for individuals and couples. Includes break-even analysis across claiming ages (62-70), spousal benefit comparison, survivor benefit estimates, and lifetime benefit projections with COLA adjustments.

**Status**: Fully functional
**Usage**: `python ss_optimizer.py --user-age 60 --user-fra-benefit 2800 --spouse-age 58 --spouse-fra-benefit 1500`

### tax_strategy.py ✅ (Implemented)
Tax planning for Roth conversions and withdrawal sequencing. Analyzes conversion tax cost vs retirement tax savings, bracket space availability, IRMAA threshold warnings, and compares traditional-first vs proportional withdrawal strategies over 30 years.

**Status**: Fully functional
**Usage**: `python tax_strategy.py --scenario roth-conversion --current-income 150000 --conversion-amount 50000`

## Dependencies

Key Python packages used:
- numpy (for Monte Carlo calculations)
- json (for data I/O)
- argparse (for CLI interfaces)

## Running Scripts

All scripts are designed to be run from the retirement-planner directory:

```bash
cd retirement-planner
python scripts/monte_carlo.py --portfolio-value 1000000 --annual-spending 60000 --retirement-age 65
```

## Integration with Skill

The retirement-planner skill will invoke these scripts as needed during analysis. You can also run them manually for testing or custom scenarios.
