---
name: retirement-planner
description: This skill should be used when the user asks "am I ready to retire", "when can I retire", "Social Security claiming strategy", "Roth conversion analysis", "withdrawal strategy", "how much do I need to retire", "Monte Carlo simulation", "retirement income plan", or mentions 401(k), IRA, RMD, pension, Medicare planning, or retirement savings targets. Also triggered by questions about retirement spending, sequence of returns risk, or survivor benefits.
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Skill, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: 2025-10-31
  target-users: pre-retirees and families
---

# Retirement Planner

Comprehensive pre-retirement planning tool for individuals and couples to assess retirement readiness, optimize decisions, and create detailed retirement income plans with Monte Carlo analysis.

## Core Planning Framework

### 1. Gather Current State

**Personal Information**:
- Ages (user and spouse), planned retirement ages, life expectancy assumptions
- Current income, expected salary growth, years to retirement
- Health status, family longevity, lifestyle goals

**Financial Inventory**:
- Retirement accounts: 401(k), 403(b), Traditional IRA, Roth IRA (balances, contributions)
- Taxable investments: Brokerage accounts, real estate, business interests
- Defined benefit pensions: Monthly benefit, COLA provisions, survivor benefits
- Social Security: Earnings history, estimated benefits, spousal benefits
- Debts: Mortgage, loans (balances, rates, payoff timeline)
- Emergency fund and liquid assets

**Integration with portfolio-analyzer**:
```bash
# Import portfolio data from portfolio-analyzer
cp ../portfolio-analyzer/holdings.json data/current_portfolio.json
cp ../portfolio-analyzer/history/metrics_latest.json data/portfolio_metrics.json
```

**Ask user to clarify** (use AskUserQuestion):
- Target retirement age(s) and desired lifestyle
- Risk tolerance for retirement planning (conservative/moderate/aggressive)
- Essential vs discretionary spending split
- Legacy/inheritance goals
- Part-time work or phased retirement plans

### 2. Calculate Retirement Income Needs

**Retirement expenses framework**:

Use scripts to calculate detailed needs:
```bash
python scripts/retirement_calculator.py --current-income <amount> --retirement-age <age> --lifestyle <basic|comfortable|affluent>
```

**Expense categories**:
- **Essential**: Housing, utilities, food, healthcare, insurance, property taxes
- **Discretionary**: Travel, hobbies, entertainment, gifts
- **One-time**: Major purchases, home improvements, vehicle replacement
- **Inflation-adjusted**: Apply 2-3% annual inflation, higher (5-7%) for healthcare

**Income replacement rules**:
- 70-80% of pre-retirement income for most households
- Lower if mortgage paid off, no commuting, children independent
- Higher if extensive travel, healthcare concerns, supporting family

**Healthcare costs** (critical for pre-Medicare years):
- Age 55-65: ACA marketplace, COBRA, spousal coverage (~$15-25k/year)
- Age 65+: Medicare Parts A/B/D, Medigap, out-of-pocket (~$6-12k/year per person)
- Long-term care insurance or self-insure reserves

### 3. Project Retirement Income Sources

**Social Security optimization**:

Run optimization analysis:
```bash
python scripts/ss_optimizer.py --user-age <age> --spouse-age <age> --earnings-history <file>
```

**Key decisions**:
- Claim age (62-70): Each year delay = 8% permanent increase
- Spousal benefits: Lower earner can claim 50% of higher earner's FRA benefit
- Survivor benefits: Plan for worst-case scenario
- File-and-suspend no longer available (post-2016 rules)
- Earnings test if claiming before FRA while working

**Pension analysis**:
- Lump sum vs annuity decision (use present value calculator)
- COLA provisions vs inflation protection gap
- Survivor benefit elections (100%, 75%, 50% continuation)
- Pension Risk Transfer considerations if offered

**Portfolio withdrawal strategy**:
- **Integration point**: Pull portfolio allocation from portfolio-analyzer
- Calculate sustainable withdrawal rate (3-4% safe, 4-5% moderate, 5-6% aggressive)
- Sequence of returns risk: First decade critical for portfolio longevity
- Dynamic withdrawal strategies: Adjust based on market performance

**Required Minimum Distributions (RMDs)**:
- Starts age 73 (as of 2023), age 75 (starting 2033)
- RMD calculator based on IRS Uniform Lifetime Table
- Tax planning: May push into higher brackets

### 4. Tax Optimization Strategies

**Roth conversion analysis**:

Run tax-efficient conversion scenarios:
```bash
python scripts/tax_strategy.py --scenario roth-conversion --current-tax-bracket <bracket> --retirement-bracket <bracket>
```

**Key strategies**:
- **Pre-retirement conversions**: Fill lower brackets (12%, 22%) before RMDs/SS start
- **Early retirement conversions**: Age 62-70 window before SS, ideal for conversions
- **Medicare IRMAA considerations**: Keep MAGI below thresholds ($103k single, $206k married)
- **State tax planning**: Consider residency changes, no-income-tax states

**Withdrawal sequence optimization**:
1. **Taxable accounts first**: Tax-efficient, step-up basis at death, flexibility
2. **Tax-deferred (Traditional IRA/401k)**: After taxable depleted, manage brackets
3. **Tax-free (Roth)**: Last resort, maximize tax-free growth, legacy asset
4. **Alternative**: Proportional withdrawals to manage brackets annually

**Tax-loss harvesting and asset location**:
- Coordinate with portfolio-analyzer for tax-efficient positioning
- Bonds/REITs in tax-deferred accounts
- Growth stocks in Roth accounts
- Tax-efficient index funds in taxable accounts

### 5. Monte Carlo Simulation & Scenario Analysis

**Run probabilistic projections**:

```bash
python scripts/monte_carlo.py \
  --portfolio-value <amount> \
  --annual-spending <amount> \
  --retirement-age <age> \
  --simulations 10000 \
  --inflation-mean 2.5 --inflation-std 1.5 \
  --return-mean 7.0 --return-std 15.0
```

**Monte Carlo inputs**:
- Current portfolio value and allocation (from portfolio-analyzer)
- Annual spending needs (inflated over time)
- Expected returns and volatility by asset class
- Inflation rates and variation
- Years in retirement (to age 95+)
- Social Security and pension income streams

**Success metrics**:
- **90%+ success rate**: Very safe, may be over-saving
- **80-90% success rate**: Conservative, comfortable margin
- **70-80% success rate**: Moderate risk, may need adjustments
- **<70% success rate**: High risk, requires changes

**Scenario modeling**:
- **Base case**: Current plan, expected returns, planned retirement age
- **Bear market scenario**: Retire into -20% market, low returns first 5 years
- **Longevity scenario**: Live to 100, extended retirement period
- **Healthcare shock**: $100k+ medical expenses, long-term care needs
- **Part-time work**: Phased retirement, reduced withdrawals first 5-10 years
- **Delayed retirement**: Work 2-5 extra years, impact on success rate

**Save scenarios** for comparison:
```bash
mkdir -p history/scenarios
python scripts/monte_carlo.py <params> > history/scenarios/base_case_$(date +%Y-%m-%d).json
```

### 6. Gap Analysis & Action Plan

**Retirement readiness assessment**:

Calculate key metrics:
- **Savings rate**: Current savings / income (target: 15-20%+ for pre-retirees)
- **Replacement ratio**: Projected retirement income / current income (target: 70-80%)
- **Income coverage ratio**: Guaranteed income (SS + pension) / essential expenses (target: 80-100%)
- **Nest egg multiple**: Portfolio value / annual expenses (target: 25-30x for 4% rule)

**If gaps exist, prioritize actions**:

1. **Immediate (this year)**:
   - Max out 401(k)/403(b) contributions ($23k/year, $30.5k if 50+)
   - Catch-up contributions to IRA ($7.5k if 50+)
   - HSA max contributions ($8,300 family, triple tax advantage)
   - Debt payoff: High-interest debt, target mortgage payoff by retirement

2. **Near-term (1-3 years)**:
   - Roth conversions in low-income years
   - Adjust portfolio allocation for target retirement date (coordinate with portfolio-analyzer)
   - Review and update estate planning documents
   - Evaluate Medicare/healthcare transition plan

3. **Strategic (3+ years to retirement)**:
   - Consider delayed retirement (even 1-2 years significantly improves outcomes)
   - Social Security claiming strategy finalization
   - Pension decision analysis (if applicable)
   - Develop retirement spending budget with trial runs

### 7. Ongoing Monitoring & Updates

**Annual review cadence**:
- Update portfolio values (integrate with portfolio-analyzer monthly reviews)
- Rerun Monte Carlo with actual returns and updated assumptions
- Adjust spending projections based on lifestyle changes
- Review tax strategy and conversion opportunities
- Track progress toward retirement readiness goals

**Track in project memory**:
- `retirement.target_age`: Planned retirement age(s)
- `retirement.annual_spending_goal`: Inflated retirement budget
- `retirement.ss_strategy`: Optimal claiming age(s)
- `retirement.last_simulation_date`: When Monte Carlo last run
- `retirement.success_rate`: Latest simulation success probability
- `retirement.gap_actions`: Outstanding optimization opportunities

**Trigger re-planning when**:
- Major life changes (health, family, job change)
- Market volatility (>20% moves up or down)
- Tax law changes affecting retirement accounts
- 1-2 years from planned retirement date (final validation)

## Deep Research Capabilities

**Use Task agent** for comprehensive research:

**Retirement policy research**:
- Current Social Security solvency projections and potential benefit cuts
- Tax law changes affecting retirement accounts (SECURE Act updates)
- Medicare/ACA changes and IRMAA threshold updates
- State-specific retirement tax considerations

**Economic outlook**:
- Inflation projections and impact on retirement spending power
- Interest rate environment for bond allocation and annuity pricing
- Market outlook for sequence-of-returns risk assessment
- Healthcare cost trend analysis

**Strategy optimization**:
- Roth conversion case studies and bracket management strategies
- Social Security claiming strategies for various scenarios
- Pension vs lump sum decision frameworks
- Long-term care insurance vs self-insurance analysis

**Key sources**: SSA.gov, IRS.gov, Medicare.gov, FRED, actuarial tables, retirement research studies

## Output Generation

**Retirement plan report** (Word document via word skill):
- Executive summary: Retirement readiness assessment, success probability, key recommendations
- Current state: Financial inventory, income sources, projected needs
- Monte Carlo results: Probability of success, scenario comparisons, sensitivity analysis
- Action plan: Prioritized recommendations with timeline and impact
- Appendix: Detailed assumptions, calculation methodologies

**Scenario comparison** (Excel spreadsheet):
- Multiple scenarios side-by-side
- Charts: Portfolio balance over time, income vs expenses, probability cones
- Sensitivity tables: Impact of retirement age, returns, spending changes
- Decision tools: Roth conversion calculator, SS claiming optimizer

**Naming**: `retirement_plan_YYYY-MM-DD.docx` / `retirement_scenarios_YYYY-MM-DD.xlsx`

## Integration with Portfolio Analyzer

**Automatic data sync**:
```bash
# Run portfolio-analyzer first, then import results
python scripts/sync_portfolio_data.py --source ../portfolio-analyzer/holdings.json
```

**Shared data points**:
- Current portfolio value and allocation
- Expected returns by asset class
- Risk assessment and volatility assumptions
- Tax-efficiency of current holdings
- Rebalancing recommendations for retirement timeline

**Coordinated analysis**:
- Portfolio-analyzer provides investment context and performance
- Retirement-planner consumes portfolio data for projections
- Both skills share market research and economic outlook
- Combined reporting: Portfolio status + retirement readiness

## Key Assumptions & Considerations

**Default assumptions** (adjust based on personal situation):
- Life expectancy: 90-95 (conservative for planning purposes)
- Inflation: 2.5-3.0% general, 5-6% healthcare
- Investment returns: 6-8% depending on allocation (coordinate with portfolio-analyzer)
- Social Security COLA: 2-2.5% annually
- Tax rates: Current law unless change anticipated
- Healthcare costs: $300k-400k per couple age 65+ (Fidelity estimate)

**Risks to plan**:
- Longevity risk: Outliving savings (plan to 95+)
- Sequence risk: Poor returns early in retirement
- Inflation risk: Eroding purchasing power
- Healthcare risk: Major medical expenses or long-term care
- Policy risk: Social Security cuts, tax law changes
- Market risk: Extended bear markets or volatility

## Reference Documents (Load as needed)

**`references/retirement_rules.md`** - IRS contribution limits, RMD tables, IRMAA thresholds, tax brackets

**`references/tax_strategies.md`** - Roth conversion analysis, withdrawal sequencing, bracket management

**`references/healthcare_guide.md`** - Medicare enrollment, ACA marketplace, HSA strategies, long-term care

**`references/ss_optimization.md`** - Claiming strategies, spousal benefits, survivor planning, earnings test

Load these only when specific technical guidance needed beyond built-in knowledge.

## When to Ask User Questions

**Essential clarifications**:
- Current ages, planned retirement ages, life expectancy assumptions
- Risk tolerance for retirement planning (affects withdrawal rate and asset allocation)
- Essential vs discretionary expense split (impacts minimum income needs)
- Social Security earnings history or estimated benefits
- Pension details if applicable (monthly benefit, COLA, survivor options)
- Health status and long-term care considerations
- Legacy goals (leave inheritance vs spend it all)
- Flexibility on retirement timing (can work longer if needed?)

**Ask when**:
- Multiple valid strategies exist (e.g., SS claiming age)
- Personal preferences significantly impact recommendations
- Critical data missing (portfolio value, current savings rate, etc.)
- Major assumptions need validation (investment returns, spending needs)

## Analysis Principles

- **Personalized planning**: Tailor to specific family situation, not generic rules
- **Probabilistic thinking**: Use Monte Carlo, not deterministic projections
- **Stress testing**: Model adverse scenarios, not just base case
- **Tax optimization**: Significant value through strategic planning
- **Flexibility**: Build adaptable plans, not rigid schedules
- **Integration**: Coordinate with portfolio-analyzer for investment context
- **Conservative assumptions**: Better to under-promise and over-deliver
- **Actionable guidance**: Clear recommendations with priorities and timelines

## Limitations

This skill provides sophisticated retirement planning analysis but doesn't replace professional financial advice. Consider working with:
- CFP (Certified Financial Planner) for comprehensive planning
- CPA for complex tax situations (Roth conversions, state changes)
- Estate attorney for trusts, wills, healthcare directives
- Insurance specialist for long-term care or annuity evaluation

Projections are based on assumptions that may not materialize. Markets, taxes, and personal circumstances change. Review and update plans regularly.

