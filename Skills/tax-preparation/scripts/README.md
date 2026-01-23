# Tax Preparation Scripts

Python scripts for tax calculations, analysis, and document management.

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## Scripts Overview

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `tax_calculator.py` | Calculate federal income tax | Bracket breakdown, effective/marginal rates |
| `estimated_tax_calculator.py` | Quarterly estimated payments | Safe harbor, SE tax, payment schedule |
| `deduction_analyzer.py` | Standard vs itemized analysis | SALT cap, optimization opportunities |
| `document_checklist_generator.py` | Personalized document lists | Situation-based, missing doc tracking |
| `tax_savings_finder.py` | Find tax reduction opportunities | Proactive savings identification |
| `credit_eligibility_checker.py` | Check credit eligibility | CTC, EITC, education, saver's credit |
| `rsu_calculator.py` | RSU tax calculations | Cost basis, withholding, lot tracking, Form 8949 |

---

## tax_calculator.py

Calculate federal income tax liability with detailed bracket breakdown.

### Usage

```bash
python tax_calculator.py \
  --gross-income 100000 \
  --filing-status single \
  --deductions 15000 \
  --adjustments 3000 \
  --credits 2000 \
  --output-format text
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--gross-income` | Yes | - | Total gross income |
| `--filing-status` | No | single | single, married_jointly, married_separately, head_of_household |
| `--deductions` | No | 0 | Itemized deductions (uses higher of this or standard) |
| `--adjustments` | No | 0 | Above-the-line adjustments |
| `--age-65-plus` | No | 0 | Number of taxpayers 65+ (0, 1, or 2) |
| `--blind` | No | 0 | Number of blind taxpayers |
| `--credits` | No | 0 | Total tax credits |
| `--output-format` | No | text | text or json |

### Output

- AGI calculation
- Standard vs itemized deduction comparison
- Tax by bracket breakdown
- Tax before and after credits
- Effective and marginal tax rates

### Example Output

```
==============================================================
FEDERAL TAX CALCULATION
==============================================================

Filing Status: Single

INCOME:
  Gross Income:           $100,000.00
  - Adjustments:          $3,000.00
  = AGI:                  $97,000.00

DEDUCTIONS:
  Standard Deduction:     $14,600.00
  Itemized Deductions:    $15,000.00
  Using:                  Itemized ($15,000.00)

  Taxable Income:         $82,000.00

TAX CALCULATION:
  10% on $11,600.00: $1,160.00
  12% on $35,550.00: $4,266.00
  22% on $34,850.00: $7,667.00
  ----------------------------------------
  Tax Before Credits:     $13,093.00
  - Credits Applied:      $2,000.00
  = Tax After Credits:    $11,093.00

RATES:
  Effective Tax Rate:     11.09%
  Marginal Tax Rate:      22%
==============================================================
```

---

## estimated_tax_calculator.py

Calculate quarterly estimated tax payments with safe harbor rules.

### Usage

```bash
python estimated_tax_calculator.py \
  --projected-income 150000 \
  --se-income 50000 \
  --w2-withholding 15000 \
  --prior-year-tax 28000 \
  --prior-year-agi 140000 \
  --filing-status married_jointly
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--projected-income` | Yes | - | Total projected income for year |
| `--se-income` | No | 0 | Self-employment income |
| `--w2-withholding` | No | 0 | Expected W-2 withholding |
| `--other-withholding` | No | 0 | Other withholding (1099, etc.) |
| `--prior-year-tax` | Yes | - | Total tax from prior year return |
| `--prior-year-agi` | Yes | - | AGI from prior year return |
| `--filing-status` | No | single | Filing status |
| `--credits` | No | 0 | Expected tax credits |
| `--deductions` | No | 0 | Itemized deductions |
| `--output-format` | No | text | text or json |

### Features

- Calculates self-employment tax (Social Security + Medicare)
- Determines safe harbor amount (100% or 110% of prior year)
- Compares 90% current year vs prior year safe harbor
- Generates quarterly payment schedule with due dates

### Output

- Income and withholding summary
- Tax calculation including SE tax
- Safe harbor determination
- Quarterly payment amounts and due dates

---

## deduction_analyzer.py

Compare standard vs itemized deductions and identify optimization opportunities.

### Usage

```bash
python deduction_analyzer.py \
  --filing-status married_jointly \
  --agi 150000 \
  --medical 8000 \
  --property-tax 12000 \
  --state-income-tax 10000 \
  --mortgage-interest 15000 \
  --mortgage-debt 400000 \
  --charitable-cash 5000
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--filing-status` | Yes | - | Filing status |
| `--agi` | Yes | - | Adjusted Gross Income |
| `--age-65-plus` | No | 0 | Number of taxpayers 65+ |
| `--blind` | No | 0 | Number of blind taxpayers |
| `--medical` | No | 0 | Medical expenses |
| `--property-tax` | No | 0 | Property taxes paid |
| `--state-income-tax` | No | 0 | State income tax paid |
| `--state-sales-tax` | No | 0 | State sales tax (alternative) |
| `--mortgage-interest` | No | 0 | Mortgage interest paid |
| `--mortgage-debt` | No | 0 | Acquisition debt balance |
| `--charitable-cash` | No | 0 | Cash charitable donations |
| `--charitable-property` | No | 0 | Appreciated property donations |
| `--other-itemized` | No | 0 | Other itemized deductions |
| `--output-format` | No | text | text or json |

### Features

- Analyzes each itemized category with limits
- Calculates SALT cap impact
- Determines medical expense threshold (7.5% AGI)
- Applies charitable contribution limits
- Identifies optimization opportunities:
  - Bunching strategies
  - SALT cap workarounds
  - Timing recommendations

---

## document_checklist_generator.py

Generate personalized tax document checklists based on tax situations.

### Usage

```bash
# Generate checklist
python document_checklist_generator.py \
  --situations employed_w2 investor homeowner parent

# Check missing documents
python document_checklist_generator.py \
  --situations employed_w2 investor \
  --collected w2 1099_div \
  --check-missing

# List available situations
python document_checklist_generator.py --list-situations
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--situations` | Yes | - | Tax situations (see list below) |
| `--triggers` | No | [] | Additional specific triggers |
| `--collected` | No | [] | Document IDs already collected |
| `--check-missing` | No | False | Check for missing documents |
| `--list-situations` | No | False | List available situation profiles |
| `--output-format` | No | text | text or json |

### Available Situations

| Situation | Triggers Included |
|-----------|-------------------|
| `employed_w2` | employed, health_insurance |
| `self_employed` | self_employed, contractor, business_vehicle, home_office |
| `investor` | investments, stocks, mutual_funds, sold_stocks, bank_accounts |
| `homeowner` | homeowner, mortgage, property_owner |
| `parent` | childcare |
| `student` | education, college, student_loans |
| `retiree` | retirement_distribution, social_security, pension |
| `rental_owner` | rental_income, property_owner, rental_property |
| `marketplace_health` | marketplace_insurance, aca |
| `hsa_user` | hsa, hsa_withdrawal |

### Output

Generates categorized checklist:
- Income Documents
- Deduction Documents
- Health Insurance Documents
- Retirement Documents
- Self-Employment Documents
- Tax Credit Documents
- Prior Year Documents

---

## tax_savings_finder.py

Analyze tax data to find potential savings opportunities.

### Usage

```bash
# Using inline parameters
python tax_savings_finder.py \
  --agi 80000 \
  --filing-status single \
  --age 45 \
  --qualifying-children 2

# Using data file
python tax_savings_finder.py --data-file tax_data.json
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--data-file` | No | - | JSON file with comprehensive tax data |
| `--agi` | No | 0 | Adjusted Gross Income |
| `--filing-status` | No | single | Filing status |
| `--age` | No | 40 | Taxpayer age |
| `--qualifying-children` | No | 0 | Number of qualifying children |
| `--output-format` | No | text | text or json |

### Data File Format

```json
{
  "agi": 80000,
  "earned_income": 80000,
  "filing_status": "single",
  "age": 45,
  "qualifying_children": 2,
  "has_hdhp": true,
  "hsa_contributions": 2000,
  "hsa_coverage": "family",
  "ira_contributions": 3000,
  "has_401k": true,
  "401k_contributions": 15000,
  "has_workplace_plan": true,
  "medical_expenses": 5000,
  "state_taxes": 8000,
  "property_taxes": 6000,
  "mortgage_interest": 12000,
  "charitable_cash": 2000,
  "self_employed": true,
  "self_employment_income": 30000,
  "works_from_home": true,
  "business_miles": 5000,
  "capital_loss_carryforward": 10000,
  "unrealized_losses": 5000
}
```

### Opportunity Categories

- **Retirement**: HSA, IRA, 401(k) contribution opportunities
- **Deductions**: Bunching strategies, SALT optimization
- **Credits**: EITC, Saver's Credit, childcare, education
- **Self-Employment**: Home office, vehicle, health insurance
- **Investments**: Tax-loss harvesting, 0% LTCG bracket

### Output

Lists opportunities with:
- Priority level (HIGH, MEDIUM, LOW)
- Description and potential savings
- Required action
- Documentation needed

---

## credit_eligibility_checker.py

Determine eligibility for major tax credits and calculate amounts.

### Usage

```bash
python credit_eligibility_checker.py \
  --agi 75000 \
  --earned-income 75000 \
  --filing-status married_jointly \
  --children-under-17 2 \
  --qualifying-children-eitc 2 \
  --childcare-expenses 8000 \
  --education-expenses 5000 \
  --retirement-contributions 6000 \
  --age 35
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--data-file` | No | - | JSON file with tax data |
| `--agi` | No | 50000 | Adjusted Gross Income |
| `--earned-income` | No | AGI | Earned income |
| `--filing-status` | No | single | Filing status |
| `--children-under-17` | No | 0 | Children under 17 for CTC |
| `--qualifying-children-eitc` | No | 0 | Qualifying children for EITC |
| `--childcare-expenses` | No | 0 | Childcare expenses |
| `--education-expenses` | No | 0 | Education expenses |
| `--retirement-contributions` | No | 0 | Retirement contributions |
| `--age` | No | 35 | Taxpayer age |
| `--output-format` | No | text | text or json |

### Credits Checked

| Credit | Max Amount | Refundable |
|--------|------------|------------|
| Child Tax Credit | $2,000/child | Partially ($1,700) |
| Earned Income Tax Credit | Up to $7,830 | Yes |
| Child and Dependent Care | Up to $2,100 | No |
| American Opportunity | $2,500/student | Partially (40%) |
| Saver's Credit | $1,000 ($2,000 MFJ) | No |

### Output

For each credit:
- Eligibility status
- Credit amount (with refundable portion)
- Phaseout impact
- Requirements checklist
- Documentation needed

---

## Common Output Formats

All scripts support `--output-format` with two options:

### Text Format (default)
Human-readable formatted output with headers, tables, and summaries.

### JSON Format
Machine-readable JSON output for integration with other tools:

```bash
python tax_calculator.py --gross-income 100000 --output-format json
```

Output:
```json
{
  "input": {
    "gross_income": 100000,
    "filing_status": "single",
    ...
  },
  "calculations": {
    "adjusted_gross_income": 100000,
    "taxable_income": 85400,
    ...
  },
  "tax": {
    "tax_before_credits": 14260,
    "effective_rate_percent": 14.26,
    ...
  }
}
```

---

## Error Handling

All scripts include:
- Input validation
- Helpful error messages
- Graceful handling of edge cases (zero income, etc.)

## Notes

- All scripts use **2024 tax year** figures
- Amounts are in USD
- Scripts are standalone (no dependencies between them)
- Results are estimates; consult a tax professional for final returns

---

## rsu_calculator.py

Comprehensive RSU calculator for cost basis, withholding analysis, lot tracking, and Form 8949 preparation.

### Commands

The script supports four subcommands:

#### `withholding` - Analyze withholding adequacy

```bash
python rsu_calculator.py withholding \
  --vesting-income 50000 \
  --ytd-wages 100000 \
  --filing-status single \
  --state-rate 0.093
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--vesting-income` | Yes | - | RSU vesting income amount |
| `--ytd-wages` | No | 0 | Year-to-date wages before vesting |
| `--filing-status` | No | single | Filing status |
| `--state-rate` | No | 0.05 | State tax rate (decimal) |
| `--output-format` | No | text | text or json |

**Features:**
- Compares typical employer withholding (22% federal supplemental) to actual tax owed
- Calculates Social Security and Medicare (including additional Medicare tax)
- Identifies withholding shortfall and provides action recommendations

#### `lots` - Display vesting lot summary

```bash
python rsu_calculator.py lots --vesting-file vestings.csv
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--vesting-file` | Yes | - | CSV or JSON file with vesting data |
| `--output-format` | No | text | text or json |

**CSV Format:**
```csv
vesting_date,shares_vested,fmv_at_vesting,shares_withheld,grant_date,grant_id
2024-01-15,250,100.00,87,2022-01-15,GRANT001
2024-04-15,250,110.00,96,2022-01-15,GRANT001
```

**JSON Format:**
```json
{
  "vestings": [
    {
      "vesting_date": "2024-01-15",
      "shares_vested": 250,
      "fmv_at_vesting": 100.00,
      "shares_withheld": 87,
      "grant_date": "2022-01-15",
      "grant_id": "GRANT001"
    }
  ]
}
```

#### `sale` - Calculate sale tax implications

```bash
# Single sale
python rsu_calculator.py sale \
  --vesting-file vestings.csv \
  --sale-date 2024-06-15 \
  --shares 100 \
  --sale-price 120 \
  --method fifo

# From specific lot
python rsu_calculator.py sale \
  --vesting-file vestings.csv \
  --sale-date 2024-06-15 \
  --shares 100 \
  --sale-price 120 \
  --from-vesting-date 2024-01-15 \
  --method specific

# Multiple sales from file
python rsu_calculator.py sale \
  --vesting-file vestings.csv \
  --sales-file sales.csv
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--vesting-file` | Yes | - | CSV or JSON file with vesting data |
| `--sales-file` | No | - | CSV or JSON file with sales data |
| `--sale-date` | No | - | Sale date (YYYY-MM-DD) |
| `--shares` | No | - | Number of shares sold |
| `--sale-price` | No | - | Sale price per share |
| `--from-vesting-date` | No | - | Specific lot to sell from |
| `--reported-basis` | No | 0 | Basis reported on 1099-B |
| `--method` | No | fifo | Lot selection: fifo or specific |
| `--output-format` | No | text | text or json |

**Features:**
- FIFO or Specific ID lot selection methods
- Automatic holding period calculation (short vs long-term)
- Form 8949 adjustment generation when 1099-B basis is incorrect
- Multi-lot allocation for large sales

**Sales CSV Format:**
```csv
sale_date,shares_sold,sale_price,from_vesting_date,reported_basis_1099b
2024-06-15,100,120.00,,0
2024-09-01,50,115.00,2024-01-15,0
```

#### `basis` - Calculate cost basis for a single vesting

```bash
python rsu_calculator.py basis \
  --shares-vested 250 \
  --fmv 100.00 \
  --shares-withheld 87
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--shares-vested` | Yes | - | Number of shares vested |
| `--fmv` | Yes | - | Fair market value at vesting |
| `--shares-withheld` | No | 0 | Shares withheld for taxes |
| `--output-format` | No | text | text or json |

### Example Outputs

**Withholding Analysis:**
```
================================================================================
RSU WITHHOLDING ANALYSIS
================================================================================

Vesting Income: $50,000.00

TYPICAL EMPLOYER WITHHOLDING:
  Federal (22%):       $11,000.00
  Social Security:          $3,100.00
  Medicare:                 $725.00
  State:                    $4,650.00
  ----------------------------------------
  Total Withheld:           $19,475.00

ESTIMATED ACTUAL TAX OWED:
  Federal (32% bracket):  $16,000.00
  Social Security:          $3,100.00
  Medicare:                 $725.00
  State:                    $4,650.00
  ----------------------------------------
  Total Estimated Tax:      $24,475.00

*** WITHHOLDING SHORTFALL: $5,000.00 (10.0%) ***

ACTION NEEDED:
  - Increase W-4 withholding at day job, OR
  - Make estimated tax payment (Form 1040-ES), OR
  - Set aside funds for tax payment at filing
================================================================================
```

**Sale Calculation:**
```
================================================================================
RSU SALE CALCULATION
================================================================================

Sale Date: 2024-06-15
Shares Sold: 100.00
Sale Price: $120.00
Total Proceeds: $12,000.00

Vesting Date    Shares    Basis/Sh        Basis     Proceeds    Gain/Loss         Type   Days
--------------------------------------------------------------------------------
2024-01-15      100.00   $  100.00   $ 10,000.00  $ 12,000.00  $  2,000.00   Short-term    152

  Short-term gain/loss: $2,000.00
  Long-term gain/loss:  $0.00

--------------------------------------------------------------------------------
FORM 8949 ADJUSTMENT REQUIRED
--------------------------------------------------------------------------------

The 1099-B cost basis is incorrect. You must report the correct basis on Form 8949.

  Lot from 2024-01-15:
    1099-B reported basis: $0.00
    Correct basis:         $10,000.00
    Adjustment amount:     $10,000.00
================================================================================
```

### Integration with Statement Imports

The calculator accepts CSV exports from common brokerage platforms. Map columns as follows:

| Platform | vesting_date | shares_vested | fmv_at_vesting |
|----------|--------------|---------------|----------------|
| E*TRADE | Vest Date | Shares Released | Fair Market Value |
| Fidelity | Release Date | Total Shares | Acquisition Price |
| Schwab | Vest Date | Shares | Market Value |
| Morgan Stanley | Vesting Date | Shares Vested | FMV Per Share |
