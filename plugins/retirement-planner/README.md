# Retirement Planner Skill

Comprehensive pre-retirement planning tool for individuals and couples. Analyzes retirement readiness, optimizes claiming decisions, and creates detailed retirement income plans with Monte Carlo simulations.

## Overview

This skill helps you:
- Assess retirement readiness and identify gaps
- Project retirement income needs with inflation
- Optimize Social Security claiming strategies for couples
- Analyze tax-efficient withdrawal sequences and Roth conversions
- Run Monte Carlo simulations to test plan robustness
- Model different retirement scenarios (early retirement, market crashes, healthcare costs)
- Create detailed retirement plans with actionable recommendations

## Integration with Portfolio Analyzer

The retirement-planner skill is designed to work seamlessly with the portfolio-analyzer skill:

### Data Flow

```
portfolio-analyzer → holdings.json, metrics.json
        ↓
retirement-planner imports portfolio data
        ↓
Uses current portfolio value, allocation, expected returns
        ↓
Runs retirement projections and Monte Carlo
        ↓
Generates retirement plan + recommendations
```

### Setup Integration

1. **Ensure portfolio-analyzer is up to date**:
   ```bash
   cd ../portfolio-analyzer
   # Run latest analysis to generate current holdings and metrics
   ```

2. **Import portfolio data into retirement-planner**:
   ```bash
   cd ../retirement-planner
   python scripts/sync_portfolio_data.py --source ../portfolio-analyzer/holdings.json
   ```

3. **Run retirement planning**:
   - The skill will automatically use imported portfolio data
   - Expected returns based on allocation from portfolio-analyzer
   - Risk/volatility assumptions aligned with portfolio risk assessment

### Shared Data Elements

- **Portfolio Value**: Total investment assets for retirement
- **Asset Allocation**: Stock/bond mix determines expected returns
- **Risk Assessment**: Informs Monte Carlo volatility assumptions
- **Tax Efficiency**: Coordinates Roth conversions with portfolio tax strategy

## Quick Start

### 1. Gather Your Information

Before invoking the skill, collect:
- Current ages (you and spouse if applicable)
- Current retirement account balances (401k, IRA, Roth, etc.)
- Social Security statements or estimated benefits
- Pension information if applicable
- Current annual expenses
- Planned retirement age
- Mortgage balance and other debts

### 2. Invoke the Skill

Simply mention your retirement planning needs, and the skill will activate:
- "Can you help me assess my retirement readiness?"
- "I want to run a retirement projection with Monte Carlo analysis"
- "Should my wife and I delay Social Security or claim early?"
- "What's the optimal Roth conversion strategy for the next 5 years?"

### 3. Review Analysis

The skill will:
1. Ask clarifying questions about your situation
2. Import portfolio data if available
3. Run calculations and projections
4. Generate detailed analysis with recommendations
5. Create Word report and Excel scenario files

## Features

### Retirement Income Planning
- Replacement ratio calculation (income needed in retirement)
- Expense modeling (essential vs discretionary)
- Healthcare cost projections (pre-Medicare and Medicare years)
- Inflation adjustments (general and healthcare-specific)

### Social Security Optimization
- Claiming age optimization for singles and couples
- Spousal benefit analysis
- Survivor benefit planning
- Tax implications of claiming timing
- Break-even analysis

### Tax Strategies
- Roth conversion planning (bracket management)
- Withdrawal sequencing optimization
- IRMAA avoidance strategies
- Tax-efficient asset location
- QCD and charitable giving strategies

### Monte Carlo Simulation
- 10,000+ simulation runs
- Probabilistic success rates
- Scenario testing (bear markets, longevity, healthcare shocks)
- Sensitivity analysis
- Portfolio longevity projections

### Output Documents
- **Retirement Plan Report** (Word): Comprehensive analysis with recommendations
- **Scenario Comparison** (Excel): Multiple scenarios, charts, sensitivity tables

## Directory Structure

```
retirement-planner/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── scripts/
│   ├── retirement_calculator.py    # Core retirement needs calculation
│   ├── ss_optimizer.py            # Social Security optimization
│   ├── tax_strategy.py            # Tax planning and Roth conversions
│   ├── monte_carlo.py             # Monte Carlo simulation engine
│   └── sync_portfolio_data.py     # Import from portfolio-analyzer
├── references/
│   ├── retirement_rules.md        # IRS limits, RMDs, IRMAA, tax brackets
│   ├── tax_strategies.md          # Detailed tax optimization strategies
│   └── ss_optimization.md         # Social Security claiming strategies
├── data/
│   ├── current_portfolio.json     # Imported from portfolio-analyzer
│   └── user_inputs.json          # Your retirement planning inputs
└── history/
    └── scenarios/                 # Saved scenario analyses
```

## Scripts

### retirement_calculator.py
Calculates comprehensive retirement income needs based on current situation.

**Usage**:
```bash
python scripts/retirement_calculator.py \
  --current-income 150000 \
  --retirement-age 65 \
  --lifestyle comfortable
```

### ss_optimizer.py
Analyzes optimal Social Security claiming strategy for singles and couples.

**Usage**:
```bash
python scripts/ss_optimizer.py \
  --user-age 60 \
  --user-fra-benefit 2800 \
  --spouse-age 58 \
  --spouse-fra-benefit 1200
```

### tax_strategy.py
Plans optimal Roth conversion amounts and withdrawal sequencing.

**Usage**:
```bash
python scripts/tax_strategy.py \
  --scenario roth-conversion \
  --traditional-ira-balance 500000 \
  --current-age 60 \
  --current-tax-bracket 22
```

### monte_carlo.py
Runs probabilistic retirement projections.

**Usage**:
```bash
python scripts/monte_carlo.py \
  --portfolio-value 1000000 \
  --annual-spending 60000 \
  --retirement-age 65 \
  --simulations 10000
```

### sync_portfolio_data.py
Imports portfolio data from portfolio-analyzer.

**Usage**:
```bash
python scripts/sync_portfolio_data.py \
  --source ../portfolio-analyzer/holdings.json
```

## Key Concepts

### Safe Withdrawal Rate
Traditional: 4% of initial portfolio balance, adjusted for inflation annually.
Modern approaches: 3-3.5% more conservative, dynamic adjustments based on market performance.

### Roth Conversion Window
Optimal timing: Between retirement and Social Security (age 62-70), fill lower tax brackets before RMDs begin.

### Social Security Claiming
Rule of thumb: Higher earner delays to 70 (maximizes survivor benefit), lower earner may claim earlier.

### IRMAA
Medicare surcharges based on income from 2 years prior. Plan conversions to stay below thresholds ($103k single / $206k married for first tier).

### Sequence of Returns Risk
Market returns in first decade of retirement critical. Poor early returns can permanently impair portfolio.

## Tips for Best Results

1. **Be Realistic About Expenses**: Track current spending, adjust for retirement (no commute, but more travel)

2. **Plan Conservatively**: Assume longer life expectancy (95+), lower returns (6-7%), higher healthcare costs

3. **Update Regularly**: Rerun analysis annually as you approach retirement, adjust based on actual results

4. **Coordinate With Spouse**: Joint optimization often differs from individual optimization

5. **Consider Flexibility**: Part-time work, delayed retirement, reduced spending all improve outcomes significantly

6. **Tax Planning Matters**: Roth conversions and withdrawal sequencing can save tens of thousands in lifetime taxes

7. **Use Portfolio-Analyzer**: Keep your investment portfolio updated to ensure projections use current data

## Resources

### Official Government Sites
- **SSA.gov**: Social Security benefit estimates and calculators
- **Medicare.gov**: Medicare enrollment and cost information
- **IRS.gov**: Retirement account rules, RMD tables, tax guidance
- **MySSA**: Create account to view earnings history and estimates

### Recommended Reading
- "The Power of Zero" by David McKnight (tax planning)
- "How to Make Your Money Last" by Jane Bryant Quinn
- "Rethinking Retirement Income Strategies" (research papers on withdrawal strategies)

## Limitations

This skill provides sophisticated retirement planning analysis but doesn't replace professional financial advice. Consider consulting:
- **CFP (Certified Financial Planner)** for comprehensive planning
- **CPA** for complex tax situations
- **Estate attorney** for trusts, wills, and healthcare directives
- **Insurance specialist** for long-term care or annuity evaluation

## Support

For issues or questions about this skill:
1. Review reference documents in `references/` directory
2. Check script documentation and examples
3. Update portfolio-analyzer data if integration issues
4. Consult official sources (SSA, IRS) for rule clarifications

## Version History

See SKILL.md for detailed version history and updates.
