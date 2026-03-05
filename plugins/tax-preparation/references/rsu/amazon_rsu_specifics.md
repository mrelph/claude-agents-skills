# Amazon RSU Specifics Reference

## Amazon Stock Compensation Overview

Amazon grants RSUs as part of total compensation for many employees. Understanding Amazon-specific practices helps accurately calculate taxes.

---

## Amazon RSU Vesting Schedule

### Standard 4-Year Vesting Schedule

Amazon uses a **back-weighted vesting schedule**:

| Year | Vesting Percentage | Cumulative |
|------|-------------------|------------|
| Year 1 | 5% | 5% |
| Year 2 | 15% | 20% |
| Year 3 | 40% | 60% |
| Year 4 | 40% | 100% |

**Important Notes:**
- Year 3 and 4 vest semi-annually (20% every 6 months)
- Vesting typically occurs on the 15th of the month
- Specific dates vary by grant agreement

### Monthly Vesting (for some grants)

Some grants may have monthly vesting in years 3-4:
- ~3.33% per month instead of 20% semi-annually
- Check specific grant agreement for details

### Refresh Grants

- Additional RSU grants given during employment
- May have different vesting schedules (often 2-year or 4-year)
- Stack on top of initial grants

---

## Amazon's Stock Plan Administrator

### Current: Morgan Stanley at Work (Shareworks)

As of recent years, Amazon uses Morgan Stanley for stock plan administration.

**Morgan Stanley Shareworks Portal:**
- View grants and vesting schedules
- Download vesting confirmations
- Execute sales
- Access tax documents (1099-B)

### Historical: Other Administrators

Previously, Amazon may have used:
- Fidelity
- E*TRADE
- Other providers

**Document Impact:** Older RSUs may have documents from different providers.

---

## Key Amazon RSU Documents

### 1. Grant Agreement/Award Letter

**Contains:**
- Number of shares granted
- Grant date
- Vesting schedule
- Grant price (for reference only - NOT cost basis)

**Tax Relevance:** Limited - grant date price is NOT your cost basis.

### 2. Vesting Confirmation (Critical Document)

**Contains:**
- Vesting date
- Number of shares vested
- Fair Market Value (FMV) at vesting - **THIS IS YOUR COST BASIS**
- Shares withheld for taxes
- Net shares deposited

**Sample Data Points:**
```
Vesting Date: March 15, 2024
Shares Released: 50
Release Price (FMV): $178.42
Gross Value: $8,921.00
Shares Withheld: 17 shares
Withholding Value: $3,033.14
Net Shares: 33
```

### 3. Supplemental Stock Plan Information

**Contains:**
- Detailed tax withholding breakdown
- Federal, state, Social Security, Medicare amounts
- May reconcile to W-2

### 4. Form 1099-B (from broker)

**Contains:**
- Proceeds from sales
- Date acquired / Date sold
- Cost basis (OFTEN WRONG!)
- Whether basis was reported to IRS

**Cost Basis Warning:**
The 1099-B cost basis is frequently incorrect because:
- Broker may not have vesting FMV
- May show $0 or original grant price
- May show "N/A" or "See attached"

### 5. W-2 (from Amazon)

**RSU Income Location:**
- Box 1: Includes RSU vesting income (with all other wages)
- Box 14: May show "RSU" or "Stock" amount separately (informational)

**Verification:**
Sum of all vesting FMV values should approximately equal RSU income shown on W-2.

---

## Amazon RSU Tax Withholding

### Standard Withholding at Vesting

Amazon withholds taxes by selling ("selling to cover") a portion of vested shares:

| Tax Type | Rate | Notes |
|----------|------|-------|
| Federal | 22% | Supplemental wage rate |
| Social Security | 6.2% | Up to wage base ($168,600 in 2024) |
| Medicare | 1.45% | No limit |
| Additional Medicare | 0.9% | If over $200k/$250k threshold |
| State | Varies | Based on work location |

### Over $1 Million Supplemental Income

If supplemental wages (including RSUs) exceed $1 million in a year:
- Federal rate increases to **37%** on excess
- This provides closer withholding to actual liability

### Withholding Adequacy

**Common Problem:** 22% federal withholding is often INSUFFICIENT for high earners.

**Example:**
```
RSU Vesting: $100,000
Federal Withheld: $22,000 (22%)
Actual Tax Due (32% bracket): $32,000
SHORTFALL: $10,000
```

**Solution:** Make estimated tax payments to cover shortfall.

---

## Amazon Stock Ticker Information

**Ticker Symbol:** AMZN
**Exchange:** NASDAQ

### Historical Stock Splits

| Date | Split Ratio | Effect |
|------|-------------|--------|
| June 6, 2022 | 20-for-1 | Each share became 20 shares |
| September 2, 1999 | 2-for-1 | |
| January 5, 1999 | 3-for-1 | |
| June 2, 1998 | 2-for-1 | |

### 2022 Stock Split Impact on RSUs

The June 2022 20-for-1 split affected RSU calculations:

**Before Split:**
- 10 shares at $2,000/share = $20,000

**After Split:**
- 200 shares at $100/share = $20,000

**Tax Impact:**
- Cost basis per share divided by 20
- Total cost basis unchanged
- Number of shares multiplied by 20

**Document Considerations:**
- Pre-split vesting confirmations show original share count
- Post-split documents show split-adjusted amounts
- Ensure consistent treatment when matching lots

---

## Common Amazon RSU Scenarios

### Scenario 1: Simple Vest and Hold

```
Grant: 100 shares (pre-split = 2,000 post-split)
Vest Date: January 15, 2024
FMV at Vest: $155.00/share
Vesting Income: 2,000 × $155 = $310,000

Tax at Vesting:
- Federal (22%): $68,200
- Social Security: (already maxed from salary)
- Medicare (1.45%): $4,495
- Add'l Medicare (0.9%): $2,790
- State (CA 9.3%): $28,830
- Total Withholding: ~$104,315

Shares Withheld: ~673 shares
Net Shares Received: ~1,327 shares

Cost Basis: $155.00 per share
Holding Period Starts: January 15, 2024
```

### Scenario 2: Immediate Sale (Same Day)

```
Continuing from above...
Sold: All 1,327 shares on January 15, 2024
Sale Price: $155.50/share
Proceeds: $206,348.50

Capital Gain Calculation:
- Proceeds: $206,348.50
- Cost Basis: 1,327 × $155.00 = $205,685.00
- Gain: $663.50 (SHORT-TERM)
```

### Scenario 3: Sale After 1+ Year (Long-Term)

```
Original Vest: January 15, 2023
FMV at Vest: $95.00/share
Shares Held: 500 shares

Sold: March 1, 2024
Sale Price: $175.00/share
Proceeds: $87,500

Capital Gain:
- Proceeds: $87,500
- Cost Basis: 500 × $95.00 = $47,500
- Gain: $40,000 (LONG-TERM)

Holding Period: 410 days (> 1 year)
Tax Rate: 15% (LTCG rate for most taxpayers)
Federal Tax on Gain: $6,000
```

### Scenario 4: Sale at Loss

```
Vest Date: November 15, 2023
FMV at Vest: $145.00/share
Shares: 100

Sold: February 15, 2024
Sale Price: $130.00/share
Proceeds: $13,000

Capital Loss:
- Proceeds: $13,000
- Cost Basis: 100 × $145.00 = $14,500
- Loss: ($1,500) (SHORT-TERM)

Tax Benefit: Loss offsets other gains or up to $3,000 of ordinary income
```

---

## Multiple Vesting Lots

Most Amazon employees have multiple vesting lots from:
- Different grant dates
- Different vesting dates within same grant
- Refresh grants

### Lot Tracking Example

```
Lot 1: Vested 1/15/2023, 50 shares @ $100 = $5,000 basis
Lot 2: Vested 3/15/2023, 50 shares @ $105 = $5,250 basis
Lot 3: Vested 7/15/2023, 75 shares @ $130 = $9,750 basis
Lot 4: Vested 1/15/2024, 100 shares @ $155 = $15,500 basis

Total: 275 shares, $35,500 total cost basis
```

### When Selling Partial Holdings

**Default: FIFO (First In, First Out)**
- Oldest shares sold first
- Generally results in long-term treatment sooner

**Alternative: Specific Identification**
- Choose which lots to sell
- Must identify at time of sale
- Requires broker documentation

---

## Amazon ESPP (If Applicable)

Some Amazon employees also participate in Employee Stock Purchase Plan:

**Key Differences from RSUs:**
- Purchase at discount (typically 15%)
- Different tax treatment
- Qualifying vs disqualifying dispositions

**NOT covered in detail by this skill** - Use tax-preparation skill for ESPP.

---

## Form 8949 Reporting Categories

### Category Based on 1099-B Reporting

| Box | Description | Form 8949 Code |
|-----|-------------|----------------|
| A | Short-term, basis reported to IRS | Part I, Box A |
| B | Short-term, basis NOT reported | Part I, Box B |
| D | Long-term, basis reported to IRS | Part II, Box D |
| E | Long-term, basis NOT reported | Part II, Box E |

### Common Amazon RSU Situations

**Most Common:** Box B or E (basis not reported or reported incorrectly)
- Requires Form 8949 adjustment
- Use adjustment code "B" for incorrect basis

---

## Tips for Amazon Employees

### Record Keeping

Keep these records for ALL RSU vests:
1. Vesting confirmation (PDF or screenshot)
2. FMV on vesting date
3. Number of shares (pre and post-split if applicable)
4. Tax withholding amounts
5. Net shares received

### Annual Tax Planning

1. **Q4 Review:** Estimate total RSU income for year
2. **Withholding Check:** Verify 22% is adequate or make Q4 estimated payment
3. **Loss Harvesting:** Review other holdings for tax-loss opportunities
4. **Holding Period:** Track which lots qualify for long-term treatment

### Common Mistakes to Avoid

1. **Using $0 cost basis** - Always use FMV at vesting
2. **Using grant date FMV** - Cost basis is VESTING date FMV
3. **Forgetting stock split adjustments** - Ensure consistent share counts
4. **Missing RSU income on W-2** - It's included in Box 1
5. **Not tracking multiple lots** - Each vest is a separate lot
6. **Wash sale violations** - 30-day rule applies to AMZN purchases

---

## Contact Information

### Morgan Stanley Shareworks Support
- Access equity awards and statements
- Download tax documents
- Execute trades

### Amazon HR/Benefits
- Questions about grant agreements
- Vesting schedule clarification
- W-2 questions

### IRS Resources
- Publication 525 (Taxable and Nontaxable Income)
- Publication 550 (Investment Income)
- Form 8949 Instructions

---

*This document covers Amazon-specific RSU practices as of 2024. Policies may change - verify with official sources.*
