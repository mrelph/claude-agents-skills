# Investment Tax Guide

Comprehensive reference for capital gains, dividends, cost basis, and investment tax optimization.

## Capital Gains Tax Rates (2024)

### Long-Term Capital Gains (held > 1 year)

| Filing Status | 0% Rate | 15% Rate | 20% Rate |
|---------------|---------|----------|----------|
| Single | $0 - $47,025 | $47,026 - $518,900 | Over $518,900 |
| Married Filing Jointly | $0 - $94,050 | $94,051 - $583,750 | Over $583,750 |
| Married Filing Separately | $0 - $47,025 | $47,026 - $291,850 | Over $291,850 |
| Head of Household | $0 - $63,000 | $63,001 - $551,350 | Over $551,350 |

**Note**: These brackets are based on TAXABLE INCOME, not AGI.

### Short-Term Capital Gains (held ≤ 1 year)
- Taxed as ordinary income at your marginal tax rate (10%-37%)
- No preferential rate

### Net Investment Income Tax (NIIT)
- Additional 3.8% on investment income
- Applies when MAGI exceeds: $200,000 (Single), $250,000 (MFJ), $125,000 (MFS)
- Applies to: Interest, dividends, capital gains, rental income, passive income
- Does NOT apply to: Tax-exempt interest, distributions from retirement accounts

### Collectibles and Section 1202 Stock
| Asset Type | Maximum Rate |
|------------|--------------|
| Collectibles (art, coins, antiques) | 28% |
| Section 1202 QSBS (excluded gain portion) | 28% |
| Unrecaptured Section 1250 gain (depreciation) | 25% |

---

## Dividends

### Qualified Dividends
**Tax treatment**: Same preferential rates as long-term capital gains (0%, 15%, 20%)

**Requirements to be qualified**:
1. Paid by U.S. corporation or qualified foreign corporation
2. Meet holding period: Must hold stock 61+ days during 121-day period around ex-dividend date
3. Not a dividend type that's excluded (see below)

**NOT qualified dividends**:
- Money market dividends
- REIT dividends (most)
- Credit union dividends
- Dividends on employee stock options
- Dividends from tax-exempt organizations
- Capital gains distributions from mutual funds (separate category)
- Dividends where holding period not met

### Ordinary Dividends
- Taxed as ordinary income at your marginal rate
- Includes non-qualified dividends
- REIT dividends (may qualify for 20% QBI deduction)

### Dividend Reporting
| 1099-DIV Box | Description |
|--------------|-------------|
| Box 1a | Total ordinary dividends |
| Box 1b | Qualified dividends (subset of 1a) |
| Box 2a | Total capital gain distributions |
| Box 2b | Unrecaptured Section 1250 gain |
| Box 3 | Nontaxable distributions (return of capital) |
| Box 7 | Foreign tax paid |

---

## Cost Basis Methods

### Specific Identification
- Choose which shares to sell
- Requires identifying shares at time of sale
- Best for: Maximizing losses or managing gains
- **Must instruct broker before sale**

### First In, First Out (FIFO)
- Default method for most brokers
- Oldest shares sold first
- May result in more long-term gains (good) or higher gains (bad)

### Average Cost
- Only available for mutual fund shares
- Single average basis for all shares
- Once elected for a fund, applies to all shares of that fund
- Simplest method for mutual funds

### Highest In, First Out (HIFO)
- Sell highest-cost shares first
- Minimizes current gain
- Some brokers offer this as automatic method

### Last In, First Out (LIFO)
- Most recently purchased shares sold first
- More likely to produce short-term gains
- Rarely advantageous

### Choosing the Right Method
| Goal | Best Method |
|------|-------------|
| Minimize current taxes | Specific ID (highest cost) or HIFO |
| Maximize long-term gains (lower rate) | FIFO or Specific ID (oldest first) |
| Simplicity | Average cost (mutual funds) or FIFO |
| Realize specific losses | Specific ID |
| Manage income for ACA/IRMAA | Specific ID with precise control |

---

## Wash Sale Rules

### Basic Rule
- Cannot deduct loss if you buy "substantially identical" security within 30 days BEFORE or AFTER the sale
- Loss is disallowed, not lost permanently
- Disallowed loss added to basis of replacement shares

### 61-Day Window
```
30 days before sale | Sale Date | 30 days after sale
        ↑               ↑                ↑
     No buy zone    Loss sale        No buy zone
```

### What's "Substantially Identical"?
**Yes, triggers wash sale**:
- Same stock or security
- Call options on same stock
- Contract to buy same stock

**Probably triggers wash sale**:
- ETF tracking same index (disputed, be cautious)
- Mutual fund with same index

**Does NOT trigger wash sale**:
- Different stock in same industry
- Different ETF tracking different index
- Bonds from same issuer (usually)
- Put options on same stock

### Wash Sale Adjustments
1. Loss disallowed on sale
2. Disallowed loss added to basis of replacement shares
3. Holding period of original shares tacks onto replacement shares

**Example**:
- Buy 100 shares at $50 ($5,000 basis)
- Sell at $30 for $3,000 ($2,000 loss)
- Within 30 days, buy 100 shares at $32 ($3,200)
- Wash sale: $2,000 loss disallowed
- New basis: $3,200 + $2,000 = $5,200 (recovers loss later)

### Wash Sales Across Accounts
- Rule applies across ALL accounts you control
- Includes: Brokerage, IRA, 401(k), spouse's accounts
- IRA wash sales are permanent loss (can't add to IRA basis)

---

## Tax-Loss Harvesting

### Strategy
1. Sell investments at a loss
2. Use losses to offset gains (short-term offsets short-term first)
3. Use up to $3,000 of excess losses against ordinary income
4. Carry forward remaining losses indefinitely

### Optimal Approach
| Your Situation | Strategy |
|----------------|----------|
| Have short-term gains | Harvest short-term losses first (offsets at ordinary rates) |
| Have long-term gains only | Harvest long-term losses |
| No gains | Harvest $3,000+ to offset income and carry forward |
| In 0% LTCG bracket | Consider realizing gains tax-free instead |

### Tax-Loss Harvesting Steps
1. Identify positions with losses
2. Determine if loss is short-term or long-term
3. Find replacement security (avoid wash sale)
4. Sell losing position
5. Buy replacement immediately (maintain market exposure)
6. Wait 31+ days before rebuying original if desired
7. Track disallowed losses if wash sale occurs

### Replacement Security Ideas
| Original | Replacement (Different Enough) |
|----------|-------------------------------|
| S&P 500 ETF (VOO) | Total Market ETF (VTI) |
| Total Market ETF (VTI) | Large Cap ETF (VV) |
| Individual stock | Competitor in same industry |
| Bond fund | Similar duration, different issuer |

### When NOT to Harvest
- If you're in 0% LTCG bracket (gains are tax-free)
- If state tax rate is high and you'll move to low-tax state
- If you need the position and can't find good substitute
- Transaction costs exceed tax benefit

---

## Tax-Gain Harvesting

### Strategy (Often Overlooked)
When in 0% LTCG bracket, realize gains tax-free to:
1. Reset cost basis higher
2. Reduce future tax liability
3. Rebalance without tax cost

### Who Benefits
- Retirees with low income years
- Years between jobs
- Early retirement before Social Security
- Students with investment accounts

### Example
- In 22% ordinary bracket but LTCG rate is 0%
- Have $20,000 gain in stock
- Sell and immediately rebuy
- Pay $0 federal tax (may owe state tax)
- New basis = current market value

---

## Municipal Bonds

### Federal Tax Treatment
- Interest is tax-exempt from federal income tax
- Still subject to AMT if private activity bonds
- Capital gains on sale ARE taxable

### State Tax Treatment
| Bond Type | Your State Tax |
|-----------|----------------|
| Your state's muni bonds | Usually exempt |
| Other state's muni bonds | Usually taxable |
| U.S. territory bonds (PR, VI, Guam) | Exempt in all states |

### Taxable-Equivalent Yield
Formula: Tax-Exempt Yield / (1 - Marginal Tax Rate)

**Example**: 3% muni bond, 32% federal bracket
```
3% / (1 - 0.32) = 3% / 0.68 = 4.41% taxable equivalent
```

### When Munis Make Sense
- High marginal tax bracket (24%+)
- Taxable accounts only (never in IRA/401k)
- State has high income tax (double benefit for in-state munis)

---

## Foreign Tax Credit

### What It Is
- Credit for foreign taxes paid on foreign investments
- Avoids double taxation
- Generally better than deduction

### Reporting Foreign Tax
| Situation | Form Required |
|-----------|---------------|
| Under $300 ($600 MFJ), all from 1099s | None - claim directly on 1040 |
| Over $300 or complex situations | Form 1116 |

### Finding Foreign Tax Paid
- 1099-DIV Box 7 (from mutual funds/ETFs)
- Foreign tax statements from direct holdings
- K-1s from partnerships with foreign investments

### Credit Limitations
- Cannot exceed U.S. tax on foreign income
- Calculated separately for passive and general income
- Excess credit carries back 1 year, forward 10 years

---

## Real Estate Investment Trusts (REITs)

### Dividend Taxation
| REIT Distribution Type | Tax Treatment |
|----------------------|---------------|
| Ordinary dividends | Ordinary income rates (may qualify for 20% QBI deduction) |
| Qualified dividends | Preferential rates (rare for REITs) |
| Capital gain distributions | LTCG rates |
| Return of capital | Reduces basis (tax-deferred until sale) |

### QBI Deduction for REIT Dividends
- 20% deduction on qualified REIT dividends
- No income limit (unlike pass-through QBI)
- Effectively reduces top rate from 37% to 29.6%

### Best Account Placement
- Tax-deferred accounts (IRA, 401k) - avoids ordinary income rates
- Or taxable if in lower bracket (for QBI deduction)

---

## Cryptocurrency

### Tax Treatment
- Property for tax purposes (not currency)
- Every sale, trade, or use is taxable event
- Includes: Selling for fiat, trading crypto-to-crypto, buying goods/services

### Taxable Events
| Event | Tax Treatment |
|-------|--------------|
| Sell crypto for USD | Capital gain/loss |
| Trade BTC for ETH | Capital gain/loss on BTC |
| Buy coffee with crypto | Capital gain/loss |
| Receive as payment | Ordinary income at FMV |
| Mining/staking rewards | Ordinary income when received |
| Airdrops | Ordinary income at FMV |
| Hard fork (new coins received) | Likely ordinary income (unclear) |

### NOT Taxable Events
- Buying crypto with USD
- Transferring between your own wallets
- Gifting crypto (may have gift tax implications)
- Donating to charity (deduction at FMV if held >1 year)

### Cost Basis Challenges
- Must track basis for every purchase
- Each trade creates new lot
- Use specific identification if possible
- Many tracking software options available

### Reporting
- Schedule D and Form 8949 for sales
- Form 1040 asks: "Did you receive, sell, exchange, or otherwise dispose of any digital asset?"
- Must answer yes if any crypto activity

---

## Employee Stock Compensation

### Restricted Stock Units (RSUs) - Comprehensive Guide

RSUs are one of the most common forms of equity compensation. Understanding the tax treatment is critical to avoid costly mistakes.

#### RSU Lifecycle and Tax Events

| Event | What Happens | Tax Treatment |
|-------|--------------|---------------|
| **Grant** | Company promises shares | NO tax event |
| **Vesting** | Shares delivered to you | ORDINARY INCOME on full FMV |
| **Sale** | You sell the shares | CAPITAL GAIN/LOSS from vesting price |

#### RSU Vesting - The Critical Tax Event

**At vesting, you owe ordinary income tax on the FULL fair market value of shares received.**

This is NOT optional - you owe tax even if you don't sell the shares.

**Example - RSU Vesting:**
```
Grant date: January 1, 2023 - 1,000 RSUs granted
Vesting date: January 1, 2024 - 250 shares vest
Stock price at vesting: $100/share

Ordinary income at vesting: 250 shares × $100 = $25,000
This $25,000 is added to your W-2 wages
Your cost basis in the shares: $25,000 ($100/share)
```

#### RSU Cost Basis - CRITICAL FOR TAX RETURNS

**Your cost basis = Fair Market Value at vesting date**

This is the #1 mistake on RSU tax returns. Many people:
- Use $0 as basis (WRONG - causes massive over-taxation)
- Use grant date price (WRONG)
- Don't adjust for taxes withheld (see below)

**The 1099-B Problem:**
- Brokers often report INCORRECT or MISSING cost basis for RSUs
- 1099-B may show $0 basis or be blank
- YOU must correct this on Form 8949 using adjustment code "B"

#### RSU Tax Withholding at Vesting

Companies typically withhold taxes at vesting using one of two methods:

**1. Sell-to-Cover (Most Common)**
```
250 shares vest at $100 = $25,000 income
Company withholds at 22% federal + state + FICA
Total withholding needed: ~$8,750 (35% example)
Shares sold to cover: 87.5 shares (rounded)
Net shares deposited: 162.5 shares
Your basis per share: Still $100 (full vesting price)
```

**2. Net Share Settlement**
- Company withholds some shares (never delivered to you)
- You only receive net shares after withholding
- Basis is still FMV × shares actually received

**IMPORTANT**: Withholding is often INSUFFICIENT
- Federal supplemental rate: Only 22% (or 37% over $1M)
- Your actual bracket may be higher
- May owe additional tax at filing

#### RSU Sale - Capital Gains Treatment

**When you sell RSU shares:**

| Holding Period | Tax Treatment |
|----------------|---------------|
| Held ≤ 1 year from vesting | Short-term capital gain (ordinary rates) |
| Held > 1 year from vesting | Long-term capital gain (0%/15%/20%) |

**Example - Selling RSU Shares:**
```
Vesting date: January 1, 2024
Shares received: 162.5
Vesting price (your basis): $100/share
Total basis: $16,250

Sale date: March 1, 2025 (14 months later = LONG-TERM)
Sale price: $150/share
Proceeds: 162.5 × $150 = $24,375

Capital gain: $24,375 - $16,250 = $8,125 LONG-TERM
Tax rate: 0%, 15%, or 20% depending on income
```

**Same-Day Sale Example:**
```
250 shares vest at $100 = $25,000 (ordinary income, reported on W-2)
You immediately sell all 250 shares at $100
Proceeds: $25,000
Basis: $25,000
Capital gain: $0

Total tax: Only on the W-2 income (no additional gain)
```

#### RSU Double Taxation Trap - AVOID THIS MISTAKE

**The Problem:**
If you don't adjust basis, you pay tax TWICE on the same income:
1. Once as ordinary income at vesting (correct)
2. Again as capital gain at sale (INCORRECT)

**Example of Double Taxation:**
```
WRONG calculation:
Vesting income: $25,000 (reported on W-2) ✓
Sale proceeds: $25,000
Reported basis: $0 (ERROR!)
Reported gain: $25,000 (WRONG - this was already taxed!)

CORRECT calculation:
Vesting income: $25,000 (reported on W-2) ✓
Sale proceeds: $25,000
Correct basis: $25,000
Capital gain: $0 ✓
```

#### How to Report RSU Sales on Tax Return

**Step 1: Get Your Documents**
- W-2: Check Box 1 includes RSU vesting income
- 1099-B: Shows sale proceeds (basis may be wrong!)
- Supplemental statement from broker: Shows vesting details
- E*TRADE, Fidelity, Schwab: Look for "Supplemental Information" or "Stock Plan Transactions"

**Step 2: Verify Cost Basis**
- Look up FMV on each vesting date
- Multiply by shares vested on that date
- This is your true cost basis

**Step 3: Report on Form 8949**
- If 1099-B basis is correct: Report as shown
- If 1099-B basis is wrong or missing:
  - Report proceeds as shown on 1099-B
  - Enter CORRECT basis
  - Use adjustment code "B" (basis incorrect)
  - Enter adjustment amount

**Form 8949 Example:**
```
Column (a): Description - "100 shares XYZ Corp RSU"
Column (b): Date acquired - "01/15/2024" (vesting date)
Column (c): Date sold - "06/20/2024"
Column (d): Proceeds - $15,000 (from 1099-B)
Column (e): Cost basis - $10,000 (YOUR CORRECTED BASIS)
Column (f): Adjustment code - "B"
Column (g): Adjustment - $10,000 (if 1099-B showed $0)
Column (h): Gain or loss - $5,000
```

#### RSU Withholding Verification

**Check your W-2 Box 12 codes:**
- Code V: Income from exercise of non-statutory stock options
- RSU income is typically just included in Box 1 (no special code)

**Verify amounts:**
1. Add up all RSU vesting events for the year
2. Calculate: Shares vested × FMV at each vesting date
3. This total should be included in W-2 Box 1

#### RSU Tax Planning Strategies

**1. Immediate Sale Strategy**
- Sell RSUs immediately upon vesting
- Eliminates market risk
- No additional capital gains tax (basis = sale price)
- Simplest tax reporting

**2. Hold for Long-Term Gains**
- Hold shares for >1 year after vesting
- Converts future gains to preferential LTCG rates
- Risk: Stock price could decline

**3. Diversification**
- Don't let RSUs become too large % of net worth
- Consider selling and reinvesting proceeds
- "Concentration risk" if too much in employer stock

**4. Tax-Loss Harvesting with RSUs**
- If stock drops below vesting price, you have a loss
- Can sell to realize capital loss
- Use loss to offset other gains or $3,000 ordinary income
- Watch wash sale rule if you want to rebuy

#### RSU Withholding Adequacy Calculator

| Marginal Tax Bracket | Typical Withholding | Shortfall |
|---------------------|---------------------|-----------|
| 22% | 22% federal | None (may owe state) |
| 24% | 22% federal | ~2% + state |
| 32% | 22% federal | ~10% + state |
| 35% | 22% federal | ~13% + state |
| 37% | 22% federal | ~15% + state |

**State Tax Reminder**: Federal supplemental withholding doesn't cover state tax (varies 0-13%+)

#### Multi-Year RSU Vesting Schedules

**Typical 4-year vesting schedule:**
```
Year 1: 25% vests → Ordinary income event
Year 2: 25% vests → Ordinary income event
Year 3: 25% vests → Ordinary income event
Year 4: 25% vests → Ordinary income event
```

Each vesting creates:
- Separate tax lot with different basis
- Different holding period start date
- Different W-2 income amount

**Track each lot separately for accurate gain/loss calculation**

#### RSU Documentation Checklist

- [ ] Grant agreement (shows total RSUs, vesting schedule)
- [ ] Vesting confirmations (date, shares, FMV)
- [ ] Brokerage statements showing shares deposited
- [ ] Sell-to-cover transaction records
- [ ] 1099-B for any sales
- [ ] Supplemental stock plan statement from broker
- [ ] W-2 showing RSU income in Box 1
- [ ] Historical stock prices for vesting dates

---

### Incentive Stock Options (ISOs)

| Event | Tax Treatment |
|-------|---------------|
| Grant | No tax |
| Exercise | No regular tax; AMT preference item |
| Sale (qualified) | LTCG from exercise price |
| Sale (disqualifying) | Ordinary income on spread at exercise |

**Qualified disposition**: Hold 2+ years from grant AND 1+ year from exercise

**AMT trap**: Spread at exercise is AMT preference; may trigger AMT

**ISO Cost Basis:**
- Regular tax basis: Exercise price paid
- AMT basis: FMV at exercise (if AMT paid)

**ISO Exercise Strategy:**
- Exercise early in year (more time to meet holding period)
- Calculate AMT exposure before exercising
- Consider exercising in low-income years

---

### Non-Qualified Stock Options (NQSOs)

| Event | Tax Treatment |
|-------|---------------|
| Grant | No tax (usually) |
| Exercise | Ordinary income on spread |
| Sale | Capital gain/loss from FMV at exercise |

**NQSO Cost Basis:**
- Your basis = Exercise price + Spread (which was taxed as ordinary income)
- Equivalent to: FMV at exercise date

**Example:**
```
Exercise price: $10
FMV at exercise: $50
Spread (ordinary income): $40/share

Your cost basis: $50 (FMV at exercise)
If you sell at $60, capital gain is $10/share
```

---

### Employee Stock Purchase Plans (ESPP)

| Disposition Type | Tax Treatment |
|------------------|---------------|
| Qualifying (2 years from offering, 1 year from purchase) | Ordinary income on discount (up to 15%); rest is LTCG |
| Disqualifying | Ordinary income on spread at purchase; rest is gain/loss |

**ESPP Cost Basis Calculation:**

**Qualifying Disposition:**
```
Offering price: $100
Purchase price (15% discount): $85
FMV at purchase: $100
FMV at sale: $120

Ordinary income: $15 (the discount)
Basis for capital gain: $100 ($85 + $15)
Capital gain: $20 ($120 - $100)
```

**Disqualifying Disposition:**
```
Offering price: $100
Purchase price: $85
FMV at purchase: $110
FMV at sale: $120

Ordinary income: $25 ($110 FMV - $85 purchase price)
Basis: $110 (FMV at purchase)
Capital gain: $10 ($120 - $110)
```

---

### Stock Compensation Summary Table

| Compensation Type | When Taxed | Tax Type | Cost Basis |
|-------------------|------------|----------|------------|
| RSUs | At vesting | Ordinary income | FMV at vesting |
| ISOs (qualified) | At sale | LTCG | Exercise price |
| ISOs (disqualifying) | At sale | Ordinary + Capital | Exercise price |
| NQSOs | At exercise | Ordinary income | FMV at exercise |
| ESPP (qualifying) | At sale | Ordinary + LTCG | Purchase price + discount |
| ESPP (disqualifying) | At sale | Ordinary + Capital | FMV at purchase |

---

## Asset Location Strategy

### Tax-Efficient Placement
| Account Type | Best Assets |
|--------------|-------------|
| **Tax-deferred (IRA, 401k)** | Bonds, REITs, high-turnover funds, anything generating ordinary income |
| **Roth** | Highest expected growth (small cap, emerging markets) |
| **Taxable** | Tax-efficient index funds, munis, stocks you'll hold forever |

### Why It Matters
- Bond interest is ordinary income (up to 37%)
- REIT dividends are ordinary income
- Qualified dividends and LTCG get preferential rates (0-20%)
- Assets in tax-deferred: No current tax, but all distributions taxed as ordinary income
- Assets in Roth: No tax ever
- Assets in taxable: Current tax, but preferential rates available

### Asset Location Example
**Portfolio**: $500k total - 60% stocks, 40% bonds
**Accounts**: $200k IRA, $100k Roth, $200k taxable

**Optimal allocation**:
- IRA ($200k): All bonds ($200k)
- Roth ($100k): Most aggressive stocks ($100k small cap/emerging)
- Taxable ($200k): Tax-efficient stock index funds ($200k)

---

## Key Forms and Reporting

### Form 1099-B
- Reports sales of securities
- Box 1a: Date acquired
- Box 1b: Date sold
- Box 1c: Proceeds
- Box 1d: Cost basis (may be blank for older purchases)
- Box 1e: Accrued market discount
- Box 1f: Wash sale loss disallowed

### Form 8949
- Details of each sale
- Separate parts for: Short-term with 1099-B basis, Short-term without, Long-term with, Long-term without
- Adjustment codes for wash sales, basis corrections, etc.

### Schedule D
- Summary of capital gains and losses
- Part I: Short-term (lines 1-7)
- Part II: Long-term (lines 8-15)
- Part III: Summary and tax calculation

### Common Adjustment Codes (Form 8949)
| Code | Meaning |
|------|---------|
| W | Wash sale loss disallowed |
| B | Basis reported incorrectly on 1099-B |
| T | Short-term reported as long-term (or vice versa) |
| O | Other (explain) |
