# Document Extraction Templates

JSON templates for extracting structured data from RSU-related documents. Use with the Read tool when processing PDFs and CSVs.

---

## RSU Vesting Confirmation

```json
{
  "document_type": "RSU_VESTING_CONFIRMATION",
  "vesting_events": [
    {
      "grant_id": "string",
      "grant_date": "YYYY-MM-DD",
      "vesting_date": "YYYY-MM-DD",
      "shares_vested": "number",
      "fair_market_value_per_share": "number (FMV at vesting)",
      "total_vesting_value": "number (shares * FMV)",
      "shares_withheld_for_taxes": "number",
      "federal_tax_withheld": "number",
      "state_tax_withheld": "number",
      "social_security_withheld": "number",
      "medicare_withheld": "number",
      "net_shares_deposited": "number"
    }
  ]
}
```

---

## Form 1099-B

```json
{
  "document_type": "1099-B",
  "broker_name": "string",
  "tax_year": "number",
  "transactions": [
    {
      "description": "string (usually AMZN or AMAZON.COM INC)",
      "date_acquired": "YYYY-MM-DD or VARIOUS",
      "date_sold": "YYYY-MM-DD",
      "proceeds": "number",
      "cost_basis_reported": "number (VERIFY THIS - often wrong!)",
      "cost_basis_reported_to_irs": "boolean",
      "gain_loss_reported": "number",
      "wash_sale_loss_disallowed": "number",
      "box_checked": "A, B, D, or E (reporting category)"
    }
  ]
}
```

---

## W-2

```json
{
  "document_type": "W-2",
  "employer_ein": "string",
  "tax_year": "number",
  "box_1_wages": "number (includes RSU vesting income)",
  "box_2_federal_withheld": "number",
  "box_12_codes": {
    "code_V": "number (if present - exercise of nonstatutory stock option)",
    "other_codes": "object"
  },
  "box_14_other": "string (may show RSU details)"
}
```

---

## CSV Parsing

For CSV files from broker exports, use the parsing script:

```bash
python scripts/parse_broker_csv.py --file "path/to/file.csv" --broker "morgan_stanley"
```

Supported brokers: `morgan_stanley`, `fidelity`, `schwab`, `etrade`
