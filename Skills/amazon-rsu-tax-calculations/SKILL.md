---
name: amazon-rsu-tax-calculations
description: This skill should be used when the user asks about "RSU taxes", "Amazon stock compensation", "cost basis for RSUs", "Form 8949 adjustment", "vesting income calculation", "1099-B cost basis is wrong", "RSU double taxation", or provides RSU vesting confirmations, 1099-B forms, or W-2s with stock compensation. Also triggered by mentions of fair market value at vesting, capital gains on RSU sales, or broker-reported basis errors.
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Skill, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: 2025-12-09
  target-users: Amazon employees, tax preparers, financial advisors working with Amazon stock compensation
---

# Amazon RSU Tax Calculations Skill

## Overview

Calculate taxes on Amazon Restricted Stock Units (RSUs). RSU taxation is complex because income is recognized at vesting (ordinary income) and again at sale (capital gains/losses). The most common and costly error is **incorrect cost basis reporting** on Form 1099-B.

**CRITICAL WARNING**: Broker-reported cost basis on Form 1099-B is frequently WRONG for RSUs. The broker often reports $0 or the grant date value instead of the fair market value at vesting. This can result in significant overpayment of taxes.

---

## Core Workflow

### Phase 1: Document Collection and Extraction

**Gather these documents (use AskUserQuestion for missing items):**

| Document | Purpose |
|----------|---------|
| W-2 | RSU vesting income in Box 1 |
| 1099-B | Stock sales (WARNING: cost basis often wrong!) |
| RSU Vesting Confirmations | FMV at vesting, shares vested, tax withheld |
| Supplemental Stock Plan Statement | Detailed withholding breakdown |
| Sale Confirmations | Proceeds and dates for shares sold |

Optional: prior year RSU records, ESPP statements, equity award statements.

Also determine: which brokerage (Morgan Stanley, Fidelity, Schwab) and which tax year.

**Extract data using the Read tool.** Load `references/extraction_templates.md` for JSON extraction templates (W-2, 1099-B, Vesting Confirmation). For CSV files, use:

```bash
python scripts/parse_broker_csv.py --file "path/to/file.csv" --broker "morgan_stanley"
```

**Validate extracted data:**
1. **Cross-reference vesting income:** sum of all RSU vesting values should approximately equal the RSU income on W-2. Small differences may result from timing adjustments or rounding.
2. **Verify share counts:** Shares Vested - Shares Withheld = Net Shares Received. Net shares should match broker account records.
3. **Check date consistency:** vesting dates should fall within the tax year; sale dates must be after corresponding vesting dates.
4. **Flag discrepancies:** alert the user to any mismatches between documents and ask for clarification or additional records.

### Phase 2: RSU Income Calculation

**Calculate vesting income (ordinary income):**

```
Vesting Income = Shares Vested x FMV per Share at Vesting Date
```

**Example:**
```
Grant: 100 shares
Vesting Date: March 15, 2024
FMV on Vesting Date: $180.00/share
Vesting Income: 100 x $180.00 = $18,000 (ordinary income)
```

**IMPORTANT:** This income is already included in W-2 Box 1. Do NOT double-count it.

**Verify W-2 reporting:**

| Item | W-2 Location | Verification |
|------|-------------|--------------|
| RSU vesting income | Box 1 (included in total) | Matches sum of vesting confirmations |
| Federal withholding | Box 2 | Includes RSU withholding |
| Social Security wages | Box 3 | Includes RSU income (up to SS limit) |
| Medicare wages | Box 5 | Includes RSU income |

Box 14 may show "RSU" or "Stock" with a separate amount -- this is informational only.

**Determine correct cost basis (MOST CRITICAL STEP):**

```
Cost Basis per Share = FMV at Vesting Date
Total Cost Basis = Shares Sold x FMV at Vesting Date
```

The cost basis equals FMV at vesting because income tax was already paid on that value when shares vested (reported as ordinary income on W-2). Using $0 or a wrong basis means paying tax TWICE on the same income -- once as wages and again as capital gains.

**Correct vs Incorrect example:**
```
50 shares vested at $180/share FMV, sold at $190/share
Proceeds: $9,500

CORRECT: Basis $9,000 -> Gain $500
INCORRECT ($0 basis): Gain $9,500 -> $9,000 of DOUBLE TAXATION!
```

```bash
python scripts/calculate_cost_basis.py --shares 50 --fmv-at-vesting 180.00 --sale-price 190.00
```

### Phase 3: Sale Transaction Analysis

**For each sale, determine:**
1. Which lot was sold (FIFO default; specific identification requires documentation)
2. Original vesting date (for holding period)
3. FMV at vesting (for cost basis)
4. Sale date and proceeds

**Lot matching rules:**
- Default is FIFO (First In, First Out) -- oldest shares sold first
- Specific identification requires documentation at time of sale
- Amazon RSUs typically use FIFO unless the user specified otherwise with the broker

**Calculate capital gains/losses:**

```
Capital Gain (Loss) = Sale Proceeds - Adjusted Cost Basis

Where:
  Sale Proceeds    = Shares Sold x Sale Price per Share
  Adjusted Basis   = Shares Sold x FMV at Vesting Date
```

**Determine short-term vs long-term treatment:**

| Holding Period | Treatment | Rate |
|----------------|-----------|------|
| <= 1 year from vesting | Short-Term | Ordinary income rates |
| > 1 year from vesting | Long-Term | 0%, 15%, or 20% |

**Holding period calculation:**
```
Holding Period = Sale Date - Vesting Date

Example:
  Vesting Date: January 15, 2023
  Sale Date: March 20, 2024
  Holding Period: 430 days -> LONG-TERM
```

```bash
python scripts/determine_holding_period.py --vesting-date "2023-01-15" --sale-date "2024-03-20"
```

### Phase 4: Tax Calculation

Load `references/irs_tax_rates.md` for current year brackets and capital gains rate tables.

**Tax calculation components:**
1. **Ordinary income tax** on RSU vesting -- already included in regular tax calculation and withheld via W-2. Check whether withholding was adequate for the actual marginal rate.
2. **Capital gains tax** on stock sales -- short-term gains are added to ordinary income and taxed at marginal rates; long-term gains receive preferential rates (0%, 15%, or 20% depending on total taxable income and filing status).
3. **Additional Medicare tax**: 0.9% on wages (including RSU vesting income) exceeding $200,000 (single) or $250,000 (MFJ).
4. **Net Investment Income Tax (NIIT)**: 3.8% on the lesser of net investment income or the amount by which MAGI exceeds $200,000 (single) / $250,000 (MFJ). Capital gains from RSU sales count as investment income; vesting income does not.

```bash
python scripts/calculate_rsu_tax.py \
  --filing-status "single" \
  --total-income 250000 \
  --rsu-vesting-income 50000 \
  --short-term-gains 5000 \
  --long-term-gains 15000 \
  --state "CA"
```

**Optimization strategies to review:**
- Hold shares > 1 year for long-term capital gains rates; calculate break-even for holding vs selling
- Offset gains with losses from other investments (watch 30-day wash sale window)
- Verify 22% federal withholding is adequate -- Amazon withholds at 22% supplemental rate, which is often insufficient for high earners in 32%+ brackets; calculate whether estimated tax payments are needed
- Check state tax considerations: some states tax all capital gains as ordinary income (e.g., California); multi-state situations may require allocation between states

### Phase 5: Reporting and Verification

**Prepare Form 8949 adjustments** when 1099-B cost basis is wrong. Load `references/form_8949_guide.md` for adjustment codes, entry format, and reporting categories.

```bash
python scripts/generate_form_8949.py \
  --sales-file "sales_records.json" \
  --vesting-file "vesting_records.json" \
  --output "form_8949_data.json"
```

**Mandatory verification checklist -- run through every item before delivering results:**
- Vesting income: sum of all vesting FMV approximately matches W-2 RSU income; each vesting event has date, shares, and FMV
- Cost basis: equals FMV at vesting for each lot (NOT $0 or grant date value); each sale has correct corresponding vesting lot
- Holding period: calculated from vesting date (not grant date); short-term vs long-term classification is accurate
- Capital gains: Proceeds - Correct Cost Basis = Gain/Loss; short-term and long-term amounts separated correctly
- Tax rates: correct tax year rates used; filing status applied correctly; NIIT threshold checked; state taxes considered
- Form 8949: all incorrect 1099-B basis items adjusted; adjustment codes correct; math verified (Reported + Adjustment = Correct)

```bash
python scripts/verify_calculations.py --all-data "tax_calculation_results.json"
```

**Generate a comprehensive summary report covering:**

1. **RSU Vesting Summary** -- total shares vested, total vesting income, tax withheld at vesting
2. **Stock Sales Summary** -- total proceeds, correct cost basis, short-term gains/losses, long-term gains/losses
3. **Tax Liability Summary** -- estimated federal tax on capital gains, NIIT if applicable, state tax estimate, comparison to withholding already paid
4. **Form 8949 Adjustments** -- list of all required adjustments with total adjustment amount
5. **Action Items** -- estimated payments needed, documents to keep for records, recommendations for next steps

---

## Scripts Reference

| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `calculate_cost_basis.py` | Correct cost basis and gains | --shares, --fmv-at-vesting, --sale-price |
| `determine_holding_period.py` | Short vs long-term determination | --vesting-date, --sale-date |
| `calculate_rsu_tax.py` | Full tax calculation | --filing-status, --income, --gains |
| `parse_broker_csv.py` | Parse broker CSV exports | --file, --broker, --type |
| `generate_form_8949.py` | Create Form 8949 data | --sales-file, --vesting-file |
| `verify_calculations.py` | Verify all calculations | --all-data, --vesting, --sales |

---

## Reference Documents

Load these references as needed:

| Reference | When to Load | Contents |
|-----------|--------------|----------|
| `references/irs_tax_rates.md` | Tax calculation phase | Current year tax brackets, capital gains rates, thresholds |
| `references/amazon_rsu_specifics.md` | Document extraction | Amazon vesting schedules, broker info, common formats |
| `references/extraction_templates.md` | Document extraction | JSON extraction templates for W-2, 1099-B, Vesting Confirmation |
| `references/form_8949_guide.md` | Reporting phase | Adjustment codes, entry format, reporting categories |

---

## Common Errors to Catch

1. **$0 cost basis on 1099-B** -- almost always wrong for RSUs. The broker often does not have the correct vesting FMV and reports $0, leading to massive over-taxation. Always verify against vesting confirmations.
2. **Grant date used instead of vesting date** -- cost basis should be FMV at VESTING, not at grant. Holding period also starts at VESTING, not grant. This is one of the most frequent mistakes.
3. **Missing RSU income on W-2** -- all vesting income belongs in W-2 Box 1. If missing, contact the employer before filing. Without this, the correct cost basis cannot be established.
4. **Wrong share count** -- shares withheld for taxes reduce net shares deposited. Only net shares can be sold. Verify: Shares Vested - Shares Withheld = Net Shares.
5. **Wash sale violations** -- buying AMZN within 30 days before or after selling at a loss disallows the loss. The disallowed loss must be added to the replacement shares' basis.
6. **Multi-state issues** -- RSUs that vested while living in a different state may require income allocation between states. Check whether the user relocated during the tax year.

---

## Integration with Other Skills

**Tax Preparation Skill (`tax-preparation`):**
- Direction: `amazon-rsu-tax-calculations` -> `tax-preparation`
- Pass corrected capital gains/losses, Form 8949 adjustments, and RSU income verification
- Invoke via Skill tool after completing RSU calculations

**Portfolio Analyzer Skill (`portfolio-analyzer`):**
- Direction: `portfolio-analyzer` -> `amazon-rsu-tax-calculations`
- Receive current Amazon holdings, historical transactions, and cost basis records

---

## When to Ask User Questions

Always ask if:
- Required documents are missing
- Discrepancy exists between data sources (e.g., vesting confirmation total does not match W-2)
- Multiple interpretations are possible
- Filing status needs confirmation
- State tax situation is unclear (e.g., moved during the year)
- Prior year carryforward losses may exist
- Estimated tax payments were made during the year

---

## Limitations

- Provides calculations and guidance, NOT tax advice
- Cannot guarantee accuracy -- the user should verify all results with a qualified tax professional
- Does not file taxes -- generates data and reports for use in tax preparation
- May not cover all edge cases (ISO conversion to RSU, 83(b) elections, NQSOs, etc.)
- State tax calculations are estimates only; state-specific rules vary significantly
- Does not handle ESPP (Employee Stock Purchase Plan) calculations -- use the `tax-preparation` skill for ESPP

**Recommend professional help when:** very large RSU amounts (>$500k), complex multi-state situations, AMT implications, international tax issues, or audit concerns.
