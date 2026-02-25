# Amazon RSU Tax Calculations Skill

A Claude Code skill for calculating taxes on Amazon Restricted Stock Unit (RSU) compensation.

## Overview

This skill helps Amazon employees and tax preparers accurately calculate taxes on RSU compensation. RSU taxation is complex because:

1. **Income is recognized at vesting** as ordinary income (included in W-2)
2. **Gains/losses are recognized at sale** as capital gains
3. **Broker-reported cost basis is often WRONG** (the #1 source of tax errors)

## Key Features

- **PDF/CSV Document Reading**: Extract data from broker statements and vesting confirmations
- **IRS-Compliant Calculations**: Uses current year tax brackets and rates
- **Cost Basis Verification**: Ensures correct FMV at vesting is used
- **Holding Period Analysis**: Determines short-term vs long-term treatment
- **Form 8949 Generation**: Creates adjustment entries for incorrect broker basis
- **Verification Checks**: Double-checks all calculations before filing

## Quick Start

1. **Gather Documents**:
   - W-2 (shows RSU vesting income)
   - 1099-B (shows stock sales - cost basis often wrong!)
   - RSU Vesting Confirmations (from Morgan Stanley)
   - Sale Confirmations

2. **Invoke the Skill**:
   ```
   /skill amazon-rsu-tax-calculations
   ```

3. **Follow the Workflow**:
   - Provide document paths
   - Review extracted data
   - Verify calculations
   - Get Form 8949 adjustments

## Critical Warning

**The most common and costly RSU tax error is incorrect cost basis.**

Brokers often report $0 or the grant date price instead of the Fair Market Value (FMV) at vesting. This can cause significant **double taxation** - you pay ordinary income tax at vesting AND capital gains tax on the same amount.

**Example of the Problem:**
```
50 shares vested at $180/share
Sold at $190/share
Broker reports $0 cost basis

WRONG (if using $0 basis):
  Proceeds: $9,500
  Cost Basis: $0
  Taxable Gain: $9,500  ← WRONG!

CORRECT (using FMV at vesting):
  Proceeds: $9,500
  Cost Basis: $9,000 (50 × $180)
  Taxable Gain: $500   ← CORRECT
```

## Directory Structure

```
amazon-rsu-tax-calculations/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── references/
│   ├── irs_tax_rates.md          # 2024 tax brackets and rates
│   └── amazon_rsu_specifics.md   # Amazon vesting schedules, brokers
└── scripts/
    ├── README.md                  # Scripts documentation
    ├── calculate_cost_basis.py    # Cost basis calculator
    ├── calculate_rsu_tax.py       # Full tax calculator
    ├── determine_holding_period.py # Short vs long-term
    ├── parse_broker_csv.py        # CSV parser
    ├── generate_form_8949.py      # Form 8949 generator
    └── verify_calculations.py     # Verification checks
```

## Workflow Phases

### Phase 1: Document Collection
- Gather W-2, 1099-B, vesting confirmations
- Extract data from PDFs/CSVs

### Phase 2: Income Calculation
- Calculate vesting income
- Verify against W-2
- Determine correct cost basis

### Phase 3: Sale Analysis
- Analyze stock sales
- Calculate capital gains/losses
- Determine holding periods

### Phase 4: Tax Calculation
- Apply IRS tax rates
- Calculate NIIT if applicable
- Estimate state taxes

### Phase 5: Reporting
- Generate Form 8949 adjustments
- Double-check all calculations
- Create summary report

## Integration

This skill integrates with:
- **tax-preparation**: Pass RSU data to complete tax return
- **portfolio-analyzer**: Receive holding data for analysis

## Limitations

- Provides calculations, not tax advice
- Cannot guarantee accuracy - verify with tax professional
- Does not file taxes - generates data only
- May not cover all edge cases (ISO conversion, 83(b) elections)

## When to Seek Professional Help

- Very large RSU amounts (>$500k)
- Multi-state tax situations
- AMT implications
- International tax issues
- Audit concerns

## Version

v1.0.0 - December 2025

## Support

For issues with the skill, check the scripts documentation in `scripts/README.md`.

For tax questions, consult a qualified tax professional.
