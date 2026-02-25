# Amazon RSU Tax Calculation Scripts

Python utilities for calculating taxes on Amazon RSU compensation.

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `calculate_cost_basis.py` | Calculate correct RSU cost basis (FMV at vesting) |
| `calculate_rsu_tax.py` | Full tax calculation including federal, state, NIIT |
| `determine_holding_period.py` | Determine short-term vs long-term treatment |
| `parse_broker_csv.py` | Parse broker CSV exports (Morgan Stanley, Fidelity, etc.) |
| `generate_form_8949.py` | Generate Form 8949 data with adjustments |
| `verify_calculations.py` | Verify all calculations before filing |

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## Quick Start

### 1. Parse Broker Data

```bash
# Parse sale transactions
python parse_broker_csv.py --file sales.csv --broker morgan_stanley --type sales --output sales.json

# Parse vesting records
python parse_broker_csv.py --file vesting.csv --broker morgan_stanley --type vesting --output vesting.json
```

### 2. Calculate Cost Basis

```bash
# Single lot
python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50

# With sale (shows gain/loss)
python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50 --sale-price 190.00

# Compare correct vs broker-reported basis
python calculate_cost_basis.py --shares 100 --fmv-at-vesting 175.50 --incorrect-basis 0 --sale-price 190.00
```

### 3. Determine Holding Period

```bash
python determine_holding_period.py --vesting-date 2023-01-15 --sale-date 2024-03-20
```

### 4. Calculate Full Tax Liability

```bash
python calculate_rsu_tax.py \
  --filing-status single \
  --total-income 250000 \
  --rsu-vesting-income 50000 \
  --short-term-gains 5000 \
  --long-term-gains 20000 \
  --state CA
```

### 5. Generate Form 8949 Data

```bash
python generate_form_8949.py \
  --sales-file sales.json \
  --vesting-file vesting.json \
  --output form_8949_data.json
```

### 6. Verify All Calculations

```bash
python verify_calculations.py \
  --vesting vesting.json \
  --sales sales.json \
  --w2-income 150000 \
  --form-8949 form_8949_data.json
```

## Detailed Usage

### calculate_cost_basis.py

Calculates the correct cost basis for RSU shares. **Critical because broker-reported basis is often wrong.**

```bash
# Basic cost basis calculation
python calculate_cost_basis.py --shares 50 --fmv-at-vesting 180.00
# Output:
{
  "shares": 50,
  "fmv_at_vesting": 180.0,
  "cost_basis_per_share": 180.0,
  "total_cost_basis": 9000.0
}

# Calculate gain/loss on sale
python calculate_cost_basis.py --shares 50 --fmv-at-vesting 180.00 --sale-price 200.00
# Output shows capital gain of $1,000

# Compare correct vs incorrect basis (shows tax impact)
python calculate_cost_basis.py \
  --shares 50 \
  --fmv-at-vesting 180.00 \
  --incorrect-basis 0 \
  --sale-price 200.00
# Output shows $9,000 over-reported gain if using $0 basis!
```

### calculate_rsu_tax.py

Comprehensive tax calculation using 2024 IRS rates.

```bash
python calculate_rsu_tax.py \
  --filing-status mfj \
  --total-income 400000 \
  --rsu-vesting-income 150000 \
  --short-term-gains 10000 \
  --long-term-gains 50000 \
  --state WA \
  --output tax_calculation.json
```

**Supported filing statuses:** `single`, `mfj` (married filing jointly), `mfs` (married filing separately), `hoh` (head of household)

**Supported states:** CA, WA, NY, TX, FL, NJ, MA, IL, PA, OR, NONE

### determine_holding_period.py

Determines if a sale qualifies for preferential long-term capital gains rates.

```bash
# Single transaction
python determine_holding_period.py \
  --vesting-date 2023-01-15 \
  --sale-date 2024-03-20

# With tax comparison
python determine_holding_period.py \
  --vesting-date 2023-01-15 \
  --sale-date 2024-03-20 \
  --gain 10000 \
  --marginal-rate 0.32

# Multiple transactions from file
python determine_holding_period.py --transactions-file transactions.json
```

### parse_broker_csv.py

Parses CSV exports from various brokers.

```bash
# Auto-detect broker
python parse_broker_csv.py --file export.csv --auto-detect --type sales

# Specify broker
python parse_broker_csv.py --file vesting.csv --broker morgan_stanley --type vesting
```

**Supported brokers:** `morgan_stanley`, `fidelity`, `schwab`, `etrade`

### generate_form_8949.py

Generates IRS Form 8949 data with proper adjustments for incorrect broker-reported basis.

```bash
python generate_form_8949.py \
  --sales-file sales.json \
  --vesting-file vesting.json \
  --lot-method fifo \
  --output form_8949.json
```

**Output includes:**
- Part I (Short-term) entries
- Part II (Long-term) entries
- Adjustment codes and amounts
- Schedule D summary lines
- Tax impact analysis

### verify_calculations.py

Final verification before filing. Catches common errors.

```bash
python verify_calculations.py --all-data complete_rsu_data.json
```

**Verifications performed:**
1. Vesting income matches W-2
2. Cost basis is correct (not $0)
3. Holding periods calculated correctly
4. Capital gains math verified
5. Form 8949 adjustments complete

## Data File Formats

### Vesting Records JSON
```json
{
  "vesting_records": [
    {
      "vesting_date": "2024-01-15",
      "grant_id": "RSU-2022-001",
      "shares_vested": 100,
      "fmv_at_vesting": 175.50,
      "shares_withheld_for_taxes": 35,
      "net_shares_received": 65
    }
  ]
}
```

### Sales Records JSON
```json
{
  "transactions": [
    {
      "date": "2024-06-15",
      "symbol": "AMZN",
      "quantity": 50,
      "price": 190.00,
      "proceeds": 9500.00,
      "cost_basis_reported": 0,
      "vesting_date": "2024-01-15"
    }
  ]
}
```

## Common Workflows

### Complete Tax Year Processing

```bash
# 1. Parse all broker data
python parse_broker_csv.py --file vesting_confirmations.csv --broker morgan_stanley --type vesting --output vesting.json
python parse_broker_csv.py --file 1099b_sales.csv --broker morgan_stanley --type sales --output sales.json

# 2. Generate Form 8949
python generate_form_8949.py --sales-file sales.json --vesting-file vesting.json --output form_8949.json

# 3. Calculate total tax
python calculate_rsu_tax.py --filing-status single --total-income 300000 --rsu-vesting-income 100000 --long-term-gains 25000 --state CA

# 4. Verify everything
python verify_calculations.py --vesting vesting.json --sales sales.json --w2-income 100000 --form-8949 form_8949.json
```

## Important Notes

1. **Cost Basis Warning**: The most critical error is using incorrect cost basis. Always verify against vesting confirmations.

2. **Holding Period**: Starts at VESTING date, not grant date.

3. **Tax Rates**: Scripts use 2024 IRS rates. Verify rates for your tax year.

4. **State Taxes**: State tax calculations are estimates. Consult state-specific guidance.

5. **Professional Advice**: These scripts provide calculations, not tax advice. Consult a tax professional for complex situations.

## Troubleshooting

**CSV parsing fails:**
- Check file encoding (UTF-8 recommended)
- Verify delimiter (comma, tab, semicolon)
- Remove any header rows before the actual column names

**Date parsing fails:**
- Use format YYYY-MM-DD or MM/DD/YYYY
- Ensure dates are valid

**Calculations seem wrong:**
- Verify FMV at vesting from original documents
- Check that all shares are accounted for
- Verify stock split adjustments (2022 20:1 split)
