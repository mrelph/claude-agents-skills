# Tax Planning & Optimization Strategies

Multi-year planning, estimated payments, state tax guidance, and life event tax strategies.

## Year-End Planning Opportunities

### Deduction Timing Strategies
- Accelerate deductions / defer income (or vice versa depending on bracket trajectory)
- Maximize retirement contributions before year-end
- Charitable giving strategies: bunching, donor-advised funds, QCDs for those 70.5+
- Roth conversion analysis in lower-income years
- Estimated payment adjustments to avoid penalties

### Bunching Strategy
If total itemized deductions are near the standard deduction threshold, consider bunching in alternating years:
- Prepay property taxes in December
- Make two years of charitable donations in one year
- Time elective medical procedures
- Use donor-advised fund for charitable bunching

### Multi-Year Projections
```bash
python scripts/tax_projector.py --current-year-data <file.json> --scenarios <params>
```

---

## Life Event Tax Impact

### Marriage
- Update withholding (new W-4s)
- Compare MFJ vs MFS (usually joint is better)
- Reassess itemized vs standard deduction with combined expenses
- Check education credit phaseouts with combined income

### Children
- Child Tax Credit ($2,000/child under 17)
- Dependent care credit for childcare expenses
- Education savings (529 plan, state deduction possible)
- Filing status may change to Head of Household if unmarried

### Home Purchase
- Mortgage interest deduction (up to $750k acquisition debt)
- Property tax deduction (subject to $10,000 SALT cap)
- Points paid at closing (deductible in year paid or amortized)
- First-time homebuyer considerations

### Job Change
- Review withholding to avoid underpayment
- Moving expenses (military only since 2018)
- Stock option/RSU forfeiture or acceleration
- 401(k) rollover decisions

### Retirement
- Distribution planning: minimize tax on withdrawals
- Roth conversions: fill low brackets before RMDs start
- Social Security timing: up to 85% taxable based on income
- Medicare IRMAA: manage MAGI to avoid premium surcharges ($103k single/$206k MFJ)

---

## Estimated Tax Payments

### Who Must Pay
- Expected tax liability of $1,000+ after withholding
- Self-employed individuals with no withholding
- Investors with significant investment income

### Safe Harbor Rules
Avoid penalties by paying the lesser of:
1. **100% of prior year tax** (110% if AGI > $150,000)
2. **90% of current year tax**

### Calculation
```bash
python scripts/estimated_tax_calculator.py --projected-income <amount> --withholding <amount>
```

### Due Dates (Calendar Year)
| Period | Due Date |
|--------|----------|
| Q1 (Jan 1 - Mar 31) | April 15 |
| Q2 (Apr 1 - May 31) | June 15 |
| Q3 (Jun 1 - Aug 31) | September 15 |
| Q4 (Sep 1 - Dec 31) | January 15 (next year) |

### Payment Options
- **IRS Direct Pay**: irs.gov/payments (free)
- **EFTPS**: Electronic Federal Tax Payment System
- **Credit/debit card**: Third-party processors (fees apply)
- **Check**: Mail with Form 1040-ES voucher

---

## State Tax Preparation

### Filing Requirements
- Resident state: All income taxable
- Part-year resident: Income during residency period
- Nonresident: Source income from that state only
- Reciprocal agreements: Check between neighboring states

### Common State Adjustments
- State may not conform to all federal deductions/credits
- State-specific credits (property tax, EITC supplements)
- State retirement income exclusions
- Municipal bond interest (in-state vs out-of-state treatment)

### Multi-State Situations
- Track which income is sourced to which state
- Calculate credit for taxes paid to other states
- Be aware of state-specific rules for remote workers

---

## Itemized vs Standard Deduction Decision

### Standard Deduction (2024)
| Filing Status | Amount |
|---------------|--------|
| Single | $14,600 |
| Married Filing Jointly | $29,200 |
| Head of Household | $21,900 |
| Additional for 65+/blind | $1,550 (married) or $1,950 (single/HoH) |

### Itemized Deductions Summary
| Category | Limit | Notes |
|----------|-------|-------|
| Medical expenses | >7.5% of AGI | Only amount exceeding threshold |
| State/local taxes (SALT) | $10,000 cap | Property + income or sales tax |
| Mortgage interest | $750k limit | Primary + one second home |
| Charitable contributions | 60% AGI cash, 30% appreciated | Substantiation requirements |
| Casualty/theft losses | Federally declared disasters only | $100 floor + 10% AGI |

### Comparison Script
```bash
python scripts/deduction_optimizer.py --income <agi> --itemized-items <file.json>
```

### Decision Factors
- Compare total itemized vs standard amount
- If close, consider bunching strategy (see above)
- Even if standard is higher, check if state return benefits from itemizing
- Some deductions are above-the-line regardless (HSA, student loan interest, etc.)

---

## Investment Tax Optimization

### Capital Gains Rates (2024)
- 0%: Taxable income up to $47,025 (single), $94,050 (MFJ)
- 15%: Up to $518,900 (single), $583,750 (MFJ)
- 20%: Above those thresholds

### Net Investment Income Tax (NIIT)
3.8% on investment income when MAGI exceeds $200k ($250k MFJ)

### Optimization Strategies
- **Tax-loss harvesting**: Offset gains with losses (watch wash sale rule)
- **Gain/loss timing**: Realize losses in high-income years, gains in low-income years
- **Long-term vs short-term**: Hold 12+ months for preferential rates
- **Asset location**: Tax-efficient placement across account types
- **Qualified dividends**: Understand holding period requirements
- **Capital loss carryforward**: Track unused losses ($3,000 annual limit against ordinary income)

### Integration with portfolio-analyzer
```bash
python scripts/capital_gains_analyzer.py --transactions <brokerage_1099b.csv>
```

---

## Filing Status Optimization

### Status Considerations
- **Married Filing Jointly vs Separately**: Usually joint is better; separate may help with income-driven loan repayments, medical deduction threshold, or liability concerns
- **Head of Household**: Requires unmarried, paying >50% household costs, qualifying person
- **Qualifying Surviving Spouse**: 2 years after spouse's death with dependent child

### Analysis Script
```bash
python scripts/filing_status_analyzer.py --income <amount> --dependents <count> --situation <params>
```

---

## Output Documents

### Tax Return Summary (Word document)
- Filing overview: Status, income summary, key deductions/credits
- Tax liability breakdown: Federal, state, FICA, estimated payments
- Refund or balance due with payment options
- Year-over-year comparison
- Planning recommendations for next year

### Tax Workpapers (Excel spreadsheet)
- Income detail by source
- Itemized deduction analysis
- Credit calculations with eligibility
- Estimated payment schedule
- Multi-year comparison

**Naming**: `tax_return_summary_YYYY.docx` / `tax_workpapers_YYYY.xlsx`

### Document Retention
- Tax returns: 7 years minimum
- Supporting documents: 7 years
- Investment purchase records: Until sold + 7 years
- Real estate records: Until sold + 7 years
