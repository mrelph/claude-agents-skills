# Tax Preparation Skill

A comprehensive tax preparation and planning skill for Claude Code that helps individuals and families prepare accurate tax returns while maximizing legal tax savings.

## Overview

This skill transforms Claude into a US Tax Expert capable of:
- Reading and extracting data from tax documents (PDFs)
- Identifying overlooked deductions and credits
- Calculating tax liability and estimated payments
- Handling complex situations (RSUs, self-employment, investments)
- Ensuring complete documentation for audit protection

## Version

**Current Version**: 1.3.0 (2025-12-09)

## Directory Structure

```
tax-preparation/
├── SKILL.md                 # Main skill definition and workflows
├── README.md                # This file
├── references/              # Reference documents
│   ├── tax_brackets_deductions.md   # 2024 brackets, limits, thresholds
│   ├── credits_guide.md             # Tax credit eligibility & calculations
│   ├── self_employment_guide.md     # SE tax, deductions, retirement
│   ├── overlooked_deductions.md     # Commonly missed deductions
│   └── investment_taxes.md          # Capital gains, RSUs, cost basis
└── scripts/                 # Python calculation scripts
    ├── tax_calculator.py              # Federal income tax calculator
    ├── estimated_tax_calculator.py    # Quarterly payment calculator
    ├── deduction_analyzer.py          # Standard vs itemized analysis
    ├── document_checklist_generator.py # Personalized checklists
    ├── tax_savings_finder.py          # Opportunity identification
    └── credit_eligibility_checker.py  # Credit qualification analysis
```

## Key Features

### 1. PDF Document Reading
The skill can read tax documents directly:
- W-2 (wages, withholding, Box 12 codes)
- 1099-INT, 1099-DIV, 1099-B (investment income)
- 1099-R (retirement distributions)
- 1098 (mortgage interest)
- 1098-T (tuition)
- RSU/Stock plan statements

### 2. Proactive Tax Reduction Discovery
- Comprehensive checklists for missed deductions
- 13 probing questions to uncover savings
- Tables of overlooked deductions by taxpayer type
- Automatic opportunity identification

### 3. RSU & Stock Compensation
Complete handling of:
- RSU cost basis calculation and verification
- 1099-B basis correction (common errors)
- Form 8949 reporting with adjustment codes
- ISO, NQSO, and ESPP tax treatment
- Double taxation trap prevention

### 4. Documentation Completeness
- Document checklists by income/deduction type
- Prior year carryforward tracking
- Red flags requiring substantiation
- Missing document resolution guidance

### 5. Calculation Tools
Python scripts for:
- Tax liability with bracket breakdown
- Estimated quarterly payments with safe harbor
- Standard vs itemized deduction comparison
- Credit eligibility checking
- Tax savings opportunity analysis

## Usage

### Invoking the Skill
When a user needs tax preparation help, the skill activates based on the description in SKILL.md. It can be invoked for:
- Annual tax return preparation
- Tax optimization strategies
- Deduction/credit identification
- Estimated tax planning
- Document organization
- RSU/stock compensation questions

### Example Interactions

**Document Processing:**
```
User: Here's my W-2 [provides PDF path]
Skill: Reads PDF, extracts Box 1-17 data, confirms with user, identifies opportunities
```

**Tax Savings Discovery:**
```
User: Help me prepare my taxes
Skill: Asks probing questions, identifies missed deductions, calculates optimal strategy
```

**RSU Questions:**
```
User: I sold some RSU shares, how do I report them?
Skill: Explains cost basis = FMV at vesting, warns about 1099-B errors, shows Form 8949 reporting
```

### Running Scripts

**Tax Calculator:**
```bash
python scripts/tax_calculator.py \
  --gross-income 100000 \
  --filing-status married_jointly \
  --deductions 15000
```

**Estimated Tax Calculator:**
```bash
python scripts/estimated_tax_calculator.py \
  --projected-income 150000 \
  --se-income 50000 \
  --prior-year-tax 25000 \
  --prior-year-agi 140000
```

**Document Checklist Generator:**
```bash
python scripts/document_checklist_generator.py \
  --situations employed_w2 investor homeowner
```

**Credit Eligibility Checker:**
```bash
python scripts/credit_eligibility_checker.py \
  --agi 75000 \
  --filing-status married_jointly \
  --children-under-17 2 \
  --childcare-expenses 8000
```

## Reference Documents

### tax_brackets_deductions.md
- 2024 federal tax brackets (all filing statuses)
- Standard deductions and additional amounts
- Capital gains rates and NIIT thresholds
- Retirement contribution limits (401k, IRA, HSA)
- SALT cap, mortgage limits, charitable limits
- AMT exemptions and rates
- Key deadlines and mileage rates

### credits_guide.md
- Child Tax Credit (CTC) eligibility and phaseouts
- Earned Income Tax Credit (EITC) tables
- Child and Dependent Care Credit
- American Opportunity Tax Credit (AOTC)
- Lifetime Learning Credit
- Saver's Credit
- Residential Energy Credits
- Foreign Tax Credit
- Adoption Credit
- Premium Tax Credit

### self_employment_guide.md
- Self-employment tax calculation
- Business deduction categories
- Home office deduction (simplified and regular)
- Vehicle deduction methods
- Health insurance deduction
- Estimated tax payments and safe harbor
- Retirement plan options (SEP, Solo 401k, SIMPLE)
- Recordkeeping requirements

### overlooked_deductions.md
- Above-the-line deductions people miss
- Itemized deductions by category
- Deductions by taxpayer type (homeowner, investor, parent, self-employed)
- Credits people don't know they qualify for
- State-specific deductions
- Carryforward items to track
- Year-end planning opportunities

### investment_taxes.md
- Capital gains rates and brackets
- Dividend taxation (qualified vs ordinary)
- Cost basis methods (FIFO, specific ID, average)
- Wash sale rules and 61-day window
- Tax-loss harvesting strategies
- Tax-gain harvesting in 0% bracket
- RSU comprehensive guide (critical section)
- ISO, NQSO, ESPP treatment
- Cryptocurrency taxation
- Asset location strategy
- Form 8949 and Schedule D reporting

## Integration with Other Skills

### portfolio-analyzer
- Import investment positions for Schedule D
- Pull capital gains/losses data
- Coordinate tax-efficient strategies

### retirement-planner
- Import retirement tax strategies
- Coordinate Roth conversion analysis
- Align withdrawal sequencing

## Key Tax Concepts

### Filing Status Priority
1. Married Filing Jointly (usually best)
2. Head of Household (if unmarried with qualifying person)
3. Single
4. Married Filing Separately (special situations only)

### Deduction Decision
- Compare standard deduction vs itemized
- Consider bunching strategy if close to threshold
- Account for SALT cap impact

### Credit vs Deduction
- Credits reduce tax dollar-for-dollar
- Deductions reduce taxable income
- Refundable credits can exceed tax liability

### RSU Cost Basis (Critical)
- Basis = FMV at vesting date
- NOT grant date, NOT $0
- 1099-B often wrong - must verify
- Use Form 8949 code "B" to correct

## Limitations

This skill provides tax preparation assistance but does not replace professional tax advice. Recommend consulting a CPA or Enrolled Agent for:
- Complex business structures
- International tax situations
- IRS audits or disputes
- Estate and trust taxation
- Significant tax controversy

## Tax Year

This skill uses **2024 tax year** figures. Adjust brackets, limits, and thresholds for other tax years.

## Changelog

See Version History section in SKILL.md for detailed changelog.
