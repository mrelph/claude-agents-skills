---
name: tax-preparation
description: This skill should be used when the user asks to "prepare my taxes", "find deductions", "calculate my tax liability", "what tax credits do I qualify for", "estimated tax payments", "optimize my tax return", "review my W-2", "itemize or standard deduction", "self-employment taxes", or provides tax documents like W-2s, 1099s, K-1s, or 1098s. Also triggered by mentions of tax brackets, filing status, AMT, capital gains tax, or tax planning strategies.
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Skill, Write, AskUserQuestion
metadata:
  version: 1.4.0
  last-updated: 2025-01-22
  target-users: individuals, families, self-employed
---

# Tax Preparation Skill

Comprehensive tax preparation and planning tool for individuals and families. Analyze tax documents, identify all legal deductions and credits, calculate tax liability, plan estimated payments, and prepare accurate returns.

## PDF Document Reading

**IMPORTANT**: This skill reads PDF documents directly. When users provide tax documents (W-2s, 1099s, statements), use the Read tool with the file path to view and extract data.

The Read tool supports PDF files and extracts both text and visual content. After reading a document:
1. Extract relevant fields using the field-mapping tables in `references/form_processing.md`
2. Confirm extracted data with the user
3. Record in JSON format for calculations
4. Flag discrepancies or missing data
5. Request related documents as needed

For RSU and stock compensation documents, always verify cost basis against vesting records. The 1099-B cost basis is frequently incorrect for RSUs. See `references/form_processing.md` for detailed extraction procedures, brokerage platform import guidance, and the RSU verification process.

---

## Core Workflow

### Phase 1: Gather Documents and Information

Collect all tax documents and personal information. Use the comprehensive checklist in `references/document_checklist.md` to ensure nothing is missed.

**Essential information to establish first:**
- Filing status (Single, MFJ, MFS, HoH, Qualifying Surviving Spouse)
- Dependents (names, SSNs, qualifying child/relative tests, custody arrangements)
- State residency (full-year, part-year, multiple states)
- Prior year return for comparison and carryforwards
- Major life changes (marriage, divorce, home purchase, job change, new child)

**Core document categories:**
- Income: W-2s, 1099-NEC/K/B/DIV/INT/R, SSA-1099, K-1s
- Deductions: 1098 (mortgage), property tax bills, medical receipts, charitable receipts
- Credits: 1098-T (tuition), childcare provider info, energy improvement receipts
- Retirement: 5498 (IRA), 5498-SA (HSA), 401(k) statements
- Stock compensation: RSU vesting confirmations, ESPP statements, ISO exercise records

Use `AskUserQuestion` to clarify filing status, income sources beyond W-2 wages, self-employment or side income, and any prior year issues (amended returns, audits, payment plans).

### Phase 2: Determine Filing Status and Requirements

**Federal filing thresholds (2024):**
- Single, under 65: $14,600
- MFJ, both under 65: $29,200
- Head of Household, under 65: $21,900
- Self-employed with net earnings $400+: Must file

Analyze the optimal filing status. MFJ is usually better than MFS; separate filing may help with income-driven loan repayments or medical deduction thresholds. Head of Household requires unmarried status, paying >50% of household costs, and a qualifying person.

### Phase 3: Calculate Income and Adjustments

Categorize all income by source:

| Category | Forms | Notes |
|----------|-------|-------|
| Wages | W-2 | Box 1 taxable wages; check Box 12 codes |
| Self-employment | 1099-NEC, 1099-K | Gross receipts minus expenses |
| Interest | 1099-INT | Including municipal (affects other calculations) |
| Dividends | 1099-DIV | Qualified vs ordinary treatment |
| Capital gains | 1099-B | Short-term vs long-term rates |
| Retirement distributions | 1099-R | Taxable amount, early withdrawal penalties |
| Social Security | SSA-1099 | Up to 85% taxable based on combined income |
| Rental income | Schedule E | Net after expenses |
| Other | Various 1099s | Unemployment, gambling, prizes |

Apply above-the-line adjustments to reduce AGI: self-employed health insurance, retirement contributions (SEP, SIMPLE, Solo 401k), half of SE tax, student loan interest (up to $2,500), HSA contributions, Traditional IRA contributions (if eligible), educator expenses ($300), and alimony paid (pre-2019 agreements only).

```bash
python scripts/tax_calculator.py --income-sources <file.json> --adjustments <file.json>
```

### Phase 4: Determine Deductions

Compare standard deduction against itemized total:

```bash
python scripts/deduction_analyzer.py --income <agi> --itemized-items <file.json>
```

**Standard Deduction (2024)**: Single $14,600 | MFJ $29,200 | HoH $21,900 | Additional for 65+/blind: $1,550 (married) or $1,950 (single/HoH).

**Itemized categories**: Medical (>7.5% AGI threshold), SALT ($10,000 cap covering property + income or sales tax), mortgage interest ($750k acquisition debt limit), and charitable contributions (60% AGI cash, 30% appreciated property). Consider bunching strategies for taxpayers near the threshold -- prepay property taxes, double up charitable donations in alternating years, time elective medical procedures. See `references/tax_planning.md` for the full decision framework.

### Phase 5: Calculate Credits

```bash
python scripts/credit_eligibility_checker.py --agi <amount> --filing-status <status> --dependents <info> --expenses <file.json>
```

**Nonrefundable credits** (reduce tax to zero): Child Tax Credit ($2,000/child under 17, phaseout at $200k/$400k MFJ), Credit for Other Dependents ($500), dependent care (20-35% of up to $3,000/$6,000 expenses), education credits (AOTC up to $2,500 per student, Lifetime Learning up to $2,000 per return), Saver's Credit (up to $1,000/$2,000 MFJ for retirement contributions), residential energy (30% of qualified improvements), and foreign tax credit.

**Refundable credits** (can exceed tax liability): EITC (up to $7,830 for 3+ children), Additional Child Tax Credit ($1,700/child), AOTC 40% refundable portion (up to $1,000), and Premium Tax Credit (ACA marketplace reconciliation via Form 8962).

See `references/credits_guide.md` for detailed eligibility requirements, phaseout calculations, and interaction rules.

### Phase 6: Handle Self-Employment

Calculate SE tax: 15.3% on 92.35% of net income (12.4% Social Security up to $168,600 wage base, 2.9% Medicare unlimited, plus 0.9% Additional Medicare over $200k/$250k MFJ). Deduct half of SE tax above-the-line.

Evaluate business deductions: home office (simplified at $5/sq ft up to 300 sq ft, or actual expenses), vehicle (67 cents/mile 2024 or actual expenses), equipment (Section 179 expensing), professional services, supplies, advertising, and insurance. Determine estimated payment requirements using the safe harbor: pay 100% of prior year tax (110% if AGI >$150k) or 90% of current year tax.

```bash
python scripts/estimated_tax_calculator.py --projected-income <amount> --withholding <amount>
```

See `references/self_employment_guide.md` for full guidance on deductions, retirement plan options, and recordkeeping.

### Phase 7: Optimize Investments

Apply appropriate capital gains rates: 0% up to $47,025 single/$94,050 MFJ, 15% up to $518,900/$583,750, 20% above those thresholds. Check for NIIT exposure (3.8% on investment income when MAGI exceeds $200k/$250k MFJ).

Optimization strategies:
- **Tax-loss harvesting**: Offset gains with losses (watch 61-day wash sale window)
- **Gain/loss timing**: Realize losses in high-income years, gains in low-income years
- **Long-term vs short-term**: Hold 12+ months for preferential rates
- **Asset location**: Place tax-inefficient assets in tax-advantaged accounts
- **Capital loss carryforward**: Track unused losses ($3,000 annual limit against ordinary income)

For RSU holders, always verify cost basis against vesting records and correct 1099-B errors on Form 8949 using code "B". See `references/investment_taxes.md` for comprehensive guidance including wash sales, cost basis methods, and stock compensation treatment.

### Phase 8: State Tax Preparation

Determine state filing requirements (resident, part-year, nonresident). Identify state-specific adjustments and credits. Calculate credit for taxes paid to other states in multi-state situations. See `references/tax_planning.md` for state tax details.

### Phase 9: Proactive Tax Reduction Discovery

Actively search for savings the user may not know about. Load `references/deduction_finder.md` and run through the hunting checklist, probing questions, and overlooked deduction tables. For RSU holders, run the RSU-specific discovery questions and holder checklist. Cross-reference with `references/overlooked_deductions.md` for situation-specific deductions.

### Phase 10: Generate Output and Plan Ahead

Produce a tax return summary document (`tax_return_summary_YYYY.docx`) covering filing overview, tax liability breakdown (federal, state, FICA), refund or balance due with payment options, and year-over-year comparison. Generate workpapers (`tax_workpapers_YYYY.xlsx`) with income detail, deduction analysis, credit calculations, and estimated payment schedule.

Include planning recommendations for next year: withholding adjustments, retirement contribution optimization, Roth conversion opportunities, estimated payment scheduling, and charitable giving strategies. See `references/tax_planning.md` for output formats and multi-year planning strategies.

**Document retention**: Tax returns and supporting documents 7 years minimum. Investment and real estate purchase records until sold plus 7 years.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/tax_calculator.py` | Core tax liability calculation |
| `scripts/deduction_analyzer.py` | Standard vs itemized comparison |
| `scripts/estimated_tax_calculator.py` | Quarterly payment calculations |
| `scripts/credit_eligibility_checker.py` | Credit qualification analysis |
| `scripts/tax_savings_finder.py` | Proactive deduction/credit identification |
| `scripts/document_checklist_generator.py` | Personalized document checklists |
| `scripts/rsu_calculator.py` | RSU cost basis, withholding, lot tracking, Form 8949 adjustments |

### RSU Calculator Usage

```bash
# Calculate withholding shortfall
python scripts/rsu_calculator.py withholding --vesting-income 25000 --ytd-wages 75000 --filing-status married_jointly --state-rate 0.093

# Load and display lot summary
python scripts/rsu_calculator.py lots --vesting-file vestings.csv

# Calculate sale tax implications
python scripts/rsu_calculator.py sale --vesting-file vestings.csv --sale-date 2024-06-15 --shares 100 --sale-price 120.00 --reported-basis 0

# Quick cost basis calculation
python scripts/rsu_calculator.py basis --shares-vested 250 --fmv 100.00 --shares-withheld 87
```

---

## Reference Documents

Load these when specific technical guidance is needed beyond built-in knowledge.

| Reference | Contents |
|-----------|----------|
| `references/tax_brackets_deductions.md` | Current year brackets, standard deductions, contribution limits, phaseout thresholds, AMT |
| `references/credits_guide.md` | Detailed eligibility and calculations for all major tax credits |
| `references/self_employment_guide.md` | Business deductions, quarterly payments, retirement options, recordkeeping |
| `references/investment_taxes.md` | Capital gains, dividends, cost basis methods, wash sales, RSU/ISO/ESPP/NQSO treatment |
| `references/overlooked_deductions.md` | Commonly missed deductions by situation (above-the-line, itemized, state-specific, carryforwards) |
| `references/deduction_finder.md` | Proactive discovery checklists, probing questions, RSU-specific discovery, overlooked deduction tables |
| `references/form_processing.md` | Form-by-form data extraction fields, RSU import procedures, brokerage CSV mapping, data recording format |
| `references/document_checklist.md` | Complete document gathering checklist by income/deduction type, prior year documents, red flags |
| `references/tax_planning.md` | Multi-year planning, estimated payments, state tax, bunching strategies, life event impact, output formats |

---

## Skill Integrations

### portfolio-analyzer
- Import investment data for Schedule D preparation
- Export RSU holdings for concentration risk assessment
- Coordinate tax-efficient selling decisions across accounts

### retirement-planner
- Import retirement tax strategy recommendations
- Export RSU vesting schedules for income planning
- Coordinate Roth conversion strategies with current-year tax position
- Model Medicare IRMAA impact from RSU income

---

## Deep Research Capabilities

Use the Task agent for comprehensive research on:
- Current year tax law changes and new provisions
- IRS guidance and rulings on specific situations
- State-specific tax rules and conformity issues
- Complex situations: stock compensation, crypto reporting, foreign income, FBAR/FATCA compliance
- Life event implications: divorce, estate planning, education funding

**Key sources**: IRS.gov, Tax Foundation, state DOR websites, tax court decisions

---

## When to Ask User Questions

**Essential clarifications:**
- Filing status and dependent eligibility
- Sources of income beyond W-2 wages
- Major life changes during tax year
- State residency and multi-state filing
- Self-employment income and expenses
- Investment activities and cost basis information
- Prior year carryforwards (losses, credits)

**Ask when:**
- Multiple valid filing strategies exist
- Significant tax planning decisions to make
- Missing or incomplete documentation
- Unusual situations requiring specific treatment

---

## Analysis Principles

- **Accuracy first**: Tax returns must be correct; verify calculations
- **Maximize legal deductions**: Identify all legitimate tax-saving opportunities
- **Document everything**: Maintain audit-ready records
- **Consider full picture**: Federal, state, current year, and future implications
- **Integration**: Coordinate with portfolio-analyzer and retirement-planner
- **Stay current**: Tax law changes frequently; verify current year rules
- **Professional referral**: Complex situations may need CPA or tax attorney

---

## Limitations

This skill provides tax preparation assistance but does not replace professional tax advice. Recommend consulting a CPA or Enrolled Agent for complex business structures, international tax situations, IRS audits or disputes, estate and trust taxation, and significant tax controversy.

Tax laws are complex and change frequently. Verify all information against current IRS publications and state tax authority guidance. This skill uses 2024 tax year figures; adjust for the applicable tax year.
