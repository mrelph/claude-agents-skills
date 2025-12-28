# Changelog - Retirement Planner Skill

All notable changes to the retirement-planner skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-31

### Added

- Initial release of retirement-planner skill
- Comprehensive pre-retirement planning framework for individuals and couples
- Financial inventory and current state gathering
  - Retirement accounts (401k, 403b, Traditional IRA, Roth IRA)
  - Taxable investments and real estate
  - Defined benefit pensions
  - Social Security earnings and estimates
  - Debt tracking and payoff timelines
  - Emergency fund assessment
- Integration with portfolio-analyzer skill
  - Automatic portfolio data sync
  - Shared return assumptions
  - Coordinated rebalancing recommendations
- Retirement income needs calculation
  - Essential vs discretionary expense framework
  - Healthcare cost estimation (pre-Medicare and Medicare)
  - Inflation adjustments (general and healthcare-specific)
  - Income replacement ratio analysis
- Retirement income source projections
  - Social Security optimization (claim age 62-70)
  - Pension analysis (lump sum vs annuity)
  - Portfolio withdrawal strategies (3-6% rates)
  - Required Minimum Distribution (RMD) calculations
- Tax optimization strategies
  - Roth conversion analysis with bracket management
  - Withdrawal sequence optimization (taxable → tax-deferred → tax-free)
  - Medicare IRMAA threshold management
  - State tax planning considerations
- Monte Carlo simulation and scenario modeling
  - 10,000+ simulation capability
  - Probabilistic success rate calculation (70-90%+ targets)
  - Multiple scenario support (base, bear market, longevity, healthcare shock)
  - Portfolio longevity projections
- Gap analysis and action planning
  - Retirement readiness assessment metrics
  - Immediate, near-term, and strategic action prioritization
  - Savings rate and replacement ratio tracking
- Ongoing monitoring framework
  - Annual review cadence
  - Project memory integration
  - Progress tracking toward retirement goals
- Deep research capabilities via Task agent
  - Retirement policy research (Social Security, tax law, Medicare/ACA)
  - Economic outlook integration
  - Strategy optimization research
- Output generation
  - Word document retirement plan reports
  - Excel scenario comparison spreadsheets
  - Probability charts and sensitivity analysis
- Python utility scripts
  - retirement_calculator.py: Income needs calculation
  - ss_optimizer.py: Social Security claiming optimization
  - tax_strategy.py: Roth conversion and tax efficiency analysis
  - monte_carlo.py: Probabilistic retirement projections
  - sync_portfolio_data.py: Portfolio-analyzer integration
- Reference documentation
  - retirement_rules.md: IRS limits, RMD tables, IRMAA thresholds
  - tax_strategies.md: Conversion and withdrawal optimization
  - healthcare_guide.md: Medicare, ACA, HSA strategies
  - ss_optimization.md: Social Security claiming strategies

### Features

- **Monte Carlo Simulations**: 10,000+ simulations with customizable parameters
- **Social Security Optimization**: Claiming age analysis (62-70) with spousal benefits
- **Tax-Efficient Withdrawals**: Three-tier withdrawal sequencing
- **Roth Conversion Planning**: Bracket-aware conversion strategies
- **Healthcare Planning**: Pre-Medicare (55-65) and Medicare (65+) cost modeling
- **Scenario Modeling**: Bear market, longevity, healthcare shock, part-time work scenarios
- **Integration**: Seamless data sharing with portfolio-analyzer skill
- **Project Memory**: Tracks retirement goals, simulation results, and action items

### Tool Access

- Read: Loading portfolio data, reference documents
- Bash: Running retirement calculation scripts
- WebSearch: Current policy and economic research
- WebFetch: Accessing official government sources (SSA.gov, IRS.gov, Medicare.gov)
- Write: Generating retirement plans and reports
- Task: Deep research on complex topics
- Skill: Invoking portfolio-analyzer and other skills
- AskUserQuestion: Clarifying risk tolerance, goals, and assumptions

### Target Users

- Pre-retirees (5-15 years from retirement)
- Individuals and couples planning retirement
- Those needing Social Security optimization
- People evaluating early retirement (before 65)
- Anyone seeking tax-efficient retirement strategies

### Key Assumptions (Defaults)

- Life expectancy: 90-95 years (conservative)
- Inflation: 2.5-3.0% general, 5-6% healthcare
- Investment returns: 6-8% (coordinated with portfolio-analyzer)
- Social Security COLA: 2-2.5% annually
- Healthcare costs: $300k-400k per couple age 65+

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for incompatible workflow changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

See also: SKILL.md for detailed workflow and usage instructions
