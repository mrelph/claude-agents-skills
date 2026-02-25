# Form 8949 Adjustment Guide

Use Form 8949 to report capital gains/losses and correct broker-reported cost basis errors on 1099-B.

---

## When Adjustments Are Required

Form 8949 adjustments are needed when the 1099-B cost basis is incorrect. For RSUs, this occurs when the broker reports:
- $0 cost basis (most common)
- Grant date FMV instead of vesting date FMV
- "N/A" or blank basis

---

## Adjustment Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| B | Basis reported to IRS is incorrect | Broker reported wrong cost basis on 1099-B |
| O | Other (describe in adjustment column) | Other adjustments not covered by specific codes |

---

## Reporting Categories

Match the category from the 1099-B box:

| Box | Description | Form 8949 Section |
|-----|-------------|-------------------|
| A | Short-term, basis reported to IRS | Part I, Box A |
| B | Short-term, basis NOT reported | Part I, Box B |
| D | Long-term, basis reported to IRS | Part II, Box D |
| E | Long-term, basis NOT reported | Part II, Box E |

Most Amazon RSU sales fall under Box B or E (basis not reported or reported incorrectly).

---

## Form 8949 Entry Format

Each sale transaction requires one line:

```
Column (a): Description      - AMZN (50 sh)
Column (b): Date Acquired    - 01/15/2023
Column (c): Date Sold        - 03/20/2024
Column (d): Proceeds         - $9,500
Column (e): Cost Basis       - $0 (as reported on 1099-B)
Column (f): Adjustment Code  - B
Column (g): Adjustment Amount - $9,000 (correct basis - reported basis)
Column (h): Gain/Loss        - $500 (proceeds - correct basis)
```

### Adjustment Calculation

```
Adjustment Amount = Correct Cost Basis - Reported Cost Basis

Where:
  Correct Cost Basis = Shares Sold x FMV at Vesting Date
  Reported Cost Basis = Value shown on 1099-B
```

---

## Generating Form 8949 Data

```bash
python scripts/generate_form_8949.py \
  --sales-file "sales_records.json" \
  --vesting-file "vesting_records.json" \
  --output "form_8949_data.json"
```

---

## Verification

After generating Form 8949 entries, verify each line:

1. Reported basis + Adjustment = Correct cost basis
2. Proceeds - Correct cost basis = Gain/Loss in column (h)
3. Short-term vs long-term classification matches holding period
4. Adjustment code is appropriate (typically "B" for RSU basis corrections)
