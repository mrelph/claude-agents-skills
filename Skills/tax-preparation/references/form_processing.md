# Form-by-Form Data Extraction Guide

Detailed field-mapping tables for extracting data from tax documents via the Read tool.

## Standard Tax Forms

### W-2 Extraction Fields
| Box | Field | Record As |
|-----|-------|-----------|
| 1 | Wages, tips, other compensation | `wages` |
| 2 | Federal income tax withheld | `federal_withholding` |
| 3 | Social Security wages | `ss_wages` |
| 4 | Social Security tax withheld | `ss_tax` |
| 5 | Medicare wages | `medicare_wages` |
| 6 | Medicare tax withheld | `medicare_tax` |
| 12a-d | Various codes (D=401k, W=HSA, etc.) | `box12_codes` |
| 17 | State income tax | `state_withholding` |

### 1099-INT Extraction Fields
| Box | Field | Record As |
|-----|-------|-----------|
| 1 | Interest income | `interest_income` |
| 2 | Early withdrawal penalty | `early_withdrawal_penalty` |
| 3 | Interest on U.S. Savings Bonds | `us_savings_bond_interest` |
| 4 | Federal income tax withheld | `federal_withholding` |
| 8 | Tax-exempt interest | `tax_exempt_interest` |

### 1099-DIV Extraction Fields
| Box | Field | Record As |
|-----|-------|-----------|
| 1a | Total ordinary dividends | `ordinary_dividends` |
| 1b | Qualified dividends | `qualified_dividends` |
| 2a | Total capital gain distributions | `capital_gain_dist` |
| 3 | Nondividend distributions | `return_of_capital` |
| 7 | Foreign tax paid | `foreign_tax_paid` |

### 1099-B Extraction Fields
| Field | Record As |
|-------|-----------|
| Description of property | `security_name` |
| Date acquired | `acquisition_date` |
| Date sold | `sale_date` |
| Proceeds | `proceeds` |
| Cost or other basis | `cost_basis` |
| Gain or loss | `gain_loss` |
| Short-term or Long-term | `holding_period` |
| Wash sale loss disallowed | `wash_sale_amount` |

### 1099-R Extraction Fields
| Box | Field | Record As |
|-----|-------|-----------|
| 1 | Gross distribution | `gross_distribution` |
| 2a | Taxable amount | `taxable_amount` |
| 4 | Federal tax withheld | `federal_withholding` |
| 7 | Distribution code | `distribution_code` |

### 1098 Extraction Fields
| Box | Field | Record As |
|-----|-------|-----------|
| 1 | Mortgage interest received | `mortgage_interest` |
| 2 | Outstanding mortgage principal | `mortgage_principal` |
| 5 | Mortgage insurance premiums | `pmi_premiums` |
| 6 | Points paid | `points_paid` |

### 1098-T Extraction Fields
| Box | Field | Record As |
|-----|-------|-----------|
| 1 | Payments received for tuition | `tuition_paid` |
| 5 | Scholarships or grants | `scholarships` |

---

## RSU and Stock Compensation Documents

**CRITICAL: RSU cost basis is the #1 source of tax errors. Always verify basis.**

### RSU/Stock Plan Statement Fields
| Field | Record As | Notes |
|-------|-----------|-------|
| Grant date | `grant_date` | When RSUs were awarded |
| Vesting date | `vesting_date` | When shares became yours (START of holding period) |
| Shares vested | `shares_vested` | Number of shares that vested |
| FMV at vesting | `fmv_at_vesting` | Price per share at vesting = YOUR COST BASIS |
| Shares withheld/sold for taxes | `shares_withheld` | Shares sold-to-cover for tax withholding |
| Net shares deposited | `net_shares` | Shares you actually received |
| Vesting income | `vesting_income` | FMV x shares vested (should match W-2) |

### 1099-B for RSU Sales

**WARNING: The 1099-B cost basis is often WRONG for RSUs!**

| Field | What It Shows | What To Check |
|-------|---------------|---------------|
| Proceeds | Sale price x shares | Usually correct |
| Cost basis | May show $0 or incorrect | VERIFY against vesting records |
| Date acquired | May be wrong | Should be VESTING date, not grant date |
| Short/Long term | Based on dates shown | Verify holding period from vesting |

### RSU Cost Basis Verification Process
1. Find vesting confirmation for each lot sold
2. Cost basis = FMV at vesting x shares sold from that lot
3. If 1099-B shows different basis, use Form 8949 code "B" to correct
4. Adjustment amount = Correct basis - Reported basis

### RSU Red Flags to Check
- [ ] 1099-B shows $0 cost basis -> MUST correct on Form 8949
- [ ] 1099-B basis doesn't match FMV x shares -> Verify and correct
- [ ] Date acquired shows grant date instead of vesting date -> Affects holding period
- [ ] W-2 Box 1 doesn't include RSU vesting income -> Contact employer
- [ ] Multiple vesting lots sold -> Track each lot's basis separately

---

## RSU Data Recording Format

```json
{
  "stock_compensation": {
    "rsus": [
      {
        "grant_date": "2022-01-15",
        "vesting_date": "2024-01-15",
        "shares_vested": 250,
        "fmv_at_vesting": 100.00,
        "vesting_income": 25000.00,
        "shares_withheld_for_taxes": 87,
        "net_shares_received": 163,
        "cost_basis_per_share": 100.00,
        "total_cost_basis": 25000.00,
        "holding_period_start": "2024-01-15"
      }
    ],
    "sales": [
      {
        "sale_date": "2024-06-15",
        "shares_sold": 100,
        "proceeds": 12000.00,
        "cost_basis": 10000.00,
        "gain_loss": 2000.00,
        "holding_period": "short_term",
        "from_vesting_date": "2024-01-15",
        "basis_adjustment_needed": true,
        "reported_basis_1099b": 0,
        "correct_basis": 10000.00
      }
    ]
  }
}
```

---

## RSU Statement Import by Brokerage Platform

### E*TRADE (Morgan Stanley at Work)
- Navigate to: Stock Plan > My Account > Gains & Losses or Tax Information
- Download: "Supplemental Information" or "Stock Plan Transactions" report
- Key columns: Release Date (vesting), Shares Released, Fair Market Value, Shares Sold-to-Cover

### Fidelity NetBenefits
- Navigate to: Stock Plans > History > Vesting History or Tax Info
- Download: "Stock Plan Transactions" or "Cost Basis" report
- Key columns: Release Date, Total Shares, Acquisition Price (this is your FMV/basis)

### Charles Schwab Equity Awards
- Navigate to: Equity Awards > Transaction History or Tax Documents
- Download: "Stock Plan Activity" or "Realized Gain/Loss" report
- Key columns: Vest Date, Shares, Market Value, Shares Withheld

### Morgan Stanley Shareworks
- Navigate to: My Portfolio > Transactions or Tax Center
- Download: "Vesting Details" or "Tax Lots" report
- Key columns: Vesting Date, Shares Vested, FMV Per Share, Net Shares

### CSV Column Mapping

When importing CSV files, the `rsu_calculator.py` script accepts these column name variations:

| Required Field | Accepted Column Names |
|----------------|----------------------|
| Vesting Date | `vesting_date`, `Vesting Date`, `Release Date`, `Date Acquired`, `Vest Date` |
| Shares Vested | `shares_vested`, `Shares Vested`, `Shares Released`, `Total Shares`, `Quantity` |
| FMV at Vesting | `fmv_at_vesting`, `FMV`, `Fair Market Value`, `Acquisition Price`, `Price`, `Market Value` |
| Shares Withheld | `shares_withheld`, `Shares Withheld`, `Sold-to-Cover`, `Shares Sold for Taxes` |
| Grant Date | `grant_date`, `Grant Date`, `Award Date` (optional) |
| Grant ID | `grant_id`, `Grant ID`, `Award ID`, `Grant Number` (optional) |

### Processing RSU Statement PDFs

When a user provides an RSU statement PDF:

1. **Read the PDF** using the Read tool
2. **Identify the document type**:
   - Vesting confirmation -> Extract vesting date, shares, FMV
   - Stock plan summary -> Extract all historical vestings
   - 1099-B -> Extract sales with (likely incorrect) basis
3. **Extract key data** into the RSU data recording format above
4. **Cross-reference** with W-2 to verify vesting income is included
5. **Flag discrepancies** between documents

---

## General Data Recording Format

After extracting data from documents, record in JSON format:

```json
{
  "tax_year": 2024,
  "documents_processed": [
    {
      "type": "W-2",
      "employer": "Employer Name",
      "ein": "XX-XXXXXXX",
      "data": {
        "wages": 75000.00,
        "federal_withholding": 9500.00,
        "state_withholding": 3200.00,
        "box12_codes": {"D": 8500.00, "W": 2400.00}
      }
    }
  ],
  "totals": {
    "total_wages": 75000.00,
    "total_federal_withholding": 9500.00
  }
}
```

---

## Document Processing Workflow

1. **User provides document**: Ask for file path or have user upload
2. **Read document**: Use Read tool on the PDF
3. **Extract key data**: Identify and record relevant fields
4. **Confirm with user**: "I extracted the following from your W-2: [summary]. Is this correct?"
5. **Record data**: Save to working data file for tax calculations
6. **Identify issues**: Flag any missing data, discrepancies, or concerns
7. **Request additional docs**: Based on what's found, ask for related documents

### Handling Multiple Documents

When processing multiple documents:
- Track each document separately with source identification
- Sum totals across documents (e.g., multiple W-2s)
- Cross-reference for consistency (e.g., W-2 Box 12 Code W should match 5498-SA)
- Flag duplicates or conflicts

---

## RSU Integration with Other Skills

### Integration with portfolio-analyzer

RSU holdings should be tracked in the portfolio-analyzer for comprehensive portfolio analysis. This helps assess concentration risk (too much in employer stock) and coordinate tax-efficient selling decisions.

**Export RSU holdings for portfolio tracking**:
```bash
python scripts/rsu_calculator.py lots --vesting-file vestings.csv --output-format json > ../portfolio-analyzer/data/rsu_holdings.json
```

**RSU data format for portfolio-analyzer**:
```json
{
  "rsu_holdings": {
    "symbol": "ACME",
    "description": "ACME Corp RSU Shares",
    "quantity": 500,
    "cost_basis_total": 50000.00,
    "cost_basis_per_share": 100.00,
    "current_value": 65000.00,
    "unrealized_gain": 15000.00,
    "lots": [
      {
        "vesting_date": "2024-01-15",
        "shares": 250,
        "cost_basis": 25000.00,
        "holding_period": "long_term"
      }
    ]
  }
}
```

**Concentration risk assessment** - Ask portfolio-analyzer to evaluate:
- RSU holdings as percentage of total portfolio
- Sector concentration (employer stock + related holdings)
- Tax implications of selling for diversification
- Optimal lot selection for tax-efficient sales

**Invoke portfolio-analyzer for RSU analysis**:
```
Skill command: "portfolio-analyzer"
Args: "--holdings data/rsu_holdings.json --concern concentration"
```

### Integration with retirement-planner

RSU vesting schedules significantly impact retirement planning, especially for pre-retirees with unvested equity. Coordinate RSU income with retirement tax strategies.

**RSU income planning considerations**:
- Large vesting events in final working years increase AGI, affecting Medicare IRMAA
- Immediate RSU sales at vesting provides tax simplicity and diversification
- Holding RSUs for long-term treatment delays capital gains tax but adds risk
- RSU income in early retirement years affects Roth conversion strategy

**Export RSU vesting schedule for retirement planning**:
```json
{
  "rsu_vesting_schedule": {
    "current_year": {
      "total_vesting_income": 100000,
      "tax_impact": "additional_withholding_needed"
    },
    "future_vestings": [
      {"year": 2025, "estimated_income": 120000},
      {"year": 2026, "estimated_income": 80000}
    ],
    "unvested_value_total": 400000,
    "cliff_vesting_years": [2025, 2027]
  }
}
```

**Invoke retirement-planner with RSU context**:
```
Skill command: "retirement-planner"
Args: "--scenario rsu-income-planning --vesting-file vestings.json"
```
