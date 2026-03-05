#!/usr/bin/env python3
"""
Document Checklist Generator - Generate personalized tax document checklists
based on user's situation and identify missing documents.
"""

import argparse
import json
from typing import Dict, List, Set

# Document categories with metadata
DOCUMENT_DEFINITIONS = {
    # Income Documents
    "w2": {
        "name": "W-2 (Wage Statement)",
        "category": "income",
        "triggers": ["employed"],
        "description": "Wage and tax statement from each employer",
        "source": "Employer (by Jan 31)",
        "irs_form": "W-2"
    },
    "1099_nec": {
        "name": "1099-NEC (Nonemployee Compensation)",
        "category": "income",
        "triggers": ["self_employed", "contractor", "freelance", "gig_work"],
        "description": "Income from clients/platforms paying $600+",
        "source": "Each payer (by Jan 31)",
        "irs_form": "1099-NEC"
    },
    "1099_k": {
        "name": "1099-K (Payment Card/Third Party)",
        "category": "income",
        "triggers": ["self_employed", "online_sales", "gig_work"],
        "description": "Income from payment platforms (Venmo, PayPal, etc.)",
        "source": "Payment processors",
        "irs_form": "1099-K"
    },
    "1099_int": {
        "name": "1099-INT (Interest Income)",
        "category": "income",
        "triggers": ["bank_accounts", "investments", "bonds"],
        "description": "Interest income from banks, bonds, etc.",
        "source": "Banks, brokerages",
        "irs_form": "1099-INT"
    },
    "1099_div": {
        "name": "1099-DIV (Dividend Income)",
        "category": "income",
        "triggers": ["investments", "stocks", "mutual_funds"],
        "description": "Dividends from stocks and mutual funds",
        "source": "Brokerages",
        "irs_form": "1099-DIV"
    },
    "1099_b": {
        "name": "1099-B (Broker Sales)",
        "category": "income",
        "triggers": ["investments", "sold_stocks", "sold_crypto"],
        "description": "Proceeds from sales of stocks, bonds, crypto",
        "source": "Brokerages, crypto exchanges",
        "irs_form": "1099-B"
    },
    "1099_r": {
        "name": "1099-R (Retirement Distributions)",
        "category": "income",
        "triggers": ["retirement_distribution", "pension", "ira_withdrawal"],
        "description": "Distributions from retirement accounts",
        "source": "Retirement plan administrators",
        "irs_form": "1099-R"
    },
    "ssa_1099": {
        "name": "SSA-1099 (Social Security Benefits)",
        "category": "income",
        "triggers": ["social_security"],
        "description": "Social Security benefit statement",
        "source": "Social Security Administration",
        "irs_form": "SSA-1099"
    },
    "1099_g": {
        "name": "1099-G (Government Payments)",
        "category": "income",
        "triggers": ["unemployment", "state_refund"],
        "description": "Unemployment compensation, state tax refunds",
        "source": "State agencies",
        "irs_form": "1099-G"
    },
    "1099_misc": {
        "name": "1099-MISC (Miscellaneous Income)",
        "category": "income",
        "triggers": ["rental_income", "royalties", "prizes"],
        "description": "Rent, royalties, prizes, awards",
        "source": "Various payers",
        "irs_form": "1099-MISC"
    },
    "k1": {
        "name": "Schedule K-1",
        "category": "income",
        "triggers": ["partnership", "s_corp", "trust", "estate"],
        "description": "Income from partnerships, S-corps, trusts",
        "source": "Entity (by Mar 15 or Sep 15)",
        "irs_form": "K-1"
    },
    "w2_g": {
        "name": "W-2G (Gambling Winnings)",
        "category": "income",
        "triggers": ["gambling"],
        "description": "Gambling winnings over threshold",
        "source": "Casinos, lottery",
        "irs_form": "W-2G"
    },

    # Deduction Documents
    "1098": {
        "name": "1098 (Mortgage Interest)",
        "category": "deduction",
        "triggers": ["homeowner", "mortgage"],
        "description": "Mortgage interest paid",
        "source": "Mortgage lender",
        "irs_form": "1098"
    },
    "1098_e": {
        "name": "1098-E (Student Loan Interest)",
        "category": "deduction",
        "triggers": ["student_loans"],
        "description": "Student loan interest paid",
        "source": "Loan servicer",
        "irs_form": "1098-E"
    },
    "1098_t": {
        "name": "1098-T (Tuition Statement)",
        "category": "deduction",
        "triggers": ["education", "college"],
        "description": "Tuition and education expenses",
        "source": "Educational institution",
        "irs_form": "1098-T"
    },
    "property_tax": {
        "name": "Property Tax Statements",
        "category": "deduction",
        "triggers": ["homeowner", "property_owner"],
        "description": "Real estate tax bills/receipts",
        "source": "County tax assessor",
        "irs_form": "N/A"
    },
    "charitable_receipts": {
        "name": "Charitable Donation Receipts",
        "category": "deduction",
        "triggers": ["charitable_donations"],
        "description": "Receipts for donations $250+",
        "source": "Charities",
        "irs_form": "N/A"
    },
    "medical_receipts": {
        "name": "Medical Expense Records",
        "category": "deduction",
        "triggers": ["medical_expenses", "itemizing"],
        "description": "Out-of-pocket medical expenses",
        "source": "Healthcare providers, pharmacies",
        "irs_form": "N/A"
    },

    # Health Insurance Documents
    "1095_a": {
        "name": "1095-A (Marketplace Insurance)",
        "category": "health",
        "triggers": ["marketplace_insurance", "aca"],
        "description": "Health Insurance Marketplace statement",
        "source": "Healthcare.gov or state marketplace",
        "irs_form": "1095-A"
    },
    "1095_b": {
        "name": "1095-B (Health Coverage)",
        "category": "health",
        "triggers": ["health_insurance"],
        "description": "Health coverage statement",
        "source": "Insurance company",
        "irs_form": "1095-B"
    },
    "1095_c": {
        "name": "1095-C (Employer Health Coverage)",
        "category": "health",
        "triggers": ["employed", "employer_insurance"],
        "description": "Employer-provided health coverage",
        "source": "Employer",
        "irs_form": "1095-C"
    },
    "5498_sa": {
        "name": "5498-SA (HSA Contributions)",
        "category": "health",
        "triggers": ["hsa"],
        "description": "HSA contribution statement",
        "source": "HSA custodian",
        "irs_form": "5498-SA"
    },
    "1099_sa": {
        "name": "1099-SA (HSA Distributions)",
        "category": "health",
        "triggers": ["hsa", "hsa_withdrawal"],
        "description": "HSA distribution statement",
        "source": "HSA custodian",
        "irs_form": "1099-SA"
    },

    # Retirement Documents
    "5498": {
        "name": "5498 (IRA Contributions)",
        "category": "retirement",
        "triggers": ["ira_contribution"],
        "description": "IRA contribution information",
        "source": "IRA custodian (by May 31)",
        "irs_form": "5498"
    },

    # Self-Employment Documents
    "business_income_records": {
        "name": "Business Income Records",
        "category": "self_employment",
        "triggers": ["self_employed"],
        "description": "All income records including cash/check payments",
        "source": "Your records",
        "irs_form": "N/A"
    },
    "business_expense_receipts": {
        "name": "Business Expense Receipts",
        "category": "self_employment",
        "triggers": ["self_employed"],
        "description": "Receipts for all business expenses by category",
        "source": "Your records",
        "irs_form": "N/A"
    },
    "mileage_log": {
        "name": "Vehicle Mileage Log",
        "category": "self_employment",
        "triggers": ["business_vehicle", "self_employed"],
        "description": "Contemporaneous mileage log",
        "source": "Your records",
        "irs_form": "N/A"
    },
    "home_office_records": {
        "name": "Home Office Documentation",
        "category": "self_employment",
        "triggers": ["home_office"],
        "description": "Square footage, exclusive use documentation",
        "source": "Your records",
        "irs_form": "N/A"
    },

    # Credit Documents
    "childcare_records": {
        "name": "Childcare Provider Information",
        "category": "credit",
        "triggers": ["childcare"],
        "description": "Provider name, address, SSN/EIN, amount paid",
        "source": "Childcare provider",
        "irs_form": "Form 2441"
    },
    "adoption_records": {
        "name": "Adoption Expense Records",
        "category": "credit",
        "triggers": ["adoption"],
        "description": "Adoption fees, legal fees, travel",
        "source": "Your records",
        "irs_form": "Form 8839"
    },
    "energy_improvement_receipts": {
        "name": "Energy Improvement Receipts",
        "category": "credit",
        "triggers": ["energy_improvements", "solar", "ev_purchase"],
        "description": "Receipts for qualifying energy improvements",
        "source": "Contractors, dealers",
        "irs_form": "Form 5695"
    },

    # Prior Year Documents
    "prior_return": {
        "name": "Prior Year Tax Return",
        "category": "prior_year",
        "triggers": ["always"],
        "description": "Complete prior year federal and state returns",
        "source": "Your records or IRS transcript",
        "irs_form": "Form 1040"
    },
    "form_8606": {
        "name": "Form 8606 (IRA Basis)",
        "category": "prior_year",
        "triggers": ["ira_contribution", "ira_withdrawal", "roth_conversion"],
        "description": "Nondeductible IRA contribution history",
        "source": "Prior year returns",
        "irs_form": "Form 8606"
    },
    "capital_loss_carryforward": {
        "name": "Capital Loss Carryforward",
        "category": "prior_year",
        "triggers": ["investments", "prior_capital_loss"],
        "description": "Unused capital losses from prior years",
        "source": "Prior year Schedule D",
        "irs_form": "Schedule D"
    },
    "depreciation_schedules": {
        "name": "Prior Depreciation Schedules",
        "category": "prior_year",
        "triggers": ["rental_property", "business_assets"],
        "description": "Asset depreciation history",
        "source": "Prior year returns",
        "irs_form": "Form 4562"
    }
}

# Situation profiles with associated triggers
SITUATION_PROFILES = {
    "employed_w2": ["employed", "health_insurance"],
    "self_employed": ["self_employed", "contractor", "business_vehicle", "home_office"],
    "investor": ["investments", "stocks", "mutual_funds", "sold_stocks", "bank_accounts"],
    "homeowner": ["homeowner", "mortgage", "property_owner"],
    "parent": ["childcare"],
    "student": ["education", "college", "student_loans"],
    "retiree": ["retirement_distribution", "social_security", "pension"],
    "rental_owner": ["rental_income", "property_owner", "rental_property"],
    "marketplace_health": ["marketplace_insurance", "aca"],
    "hsa_user": ["hsa", "hsa_withdrawal"]
}


def get_required_documents(situations: List[str], additional_triggers: List[str] = None) -> Dict:
    """Generate list of required documents based on situations."""

    triggers: Set[str] = {"always"}  # Always include baseline documents

    # Add triggers from situation profiles
    for situation in situations:
        if situation in SITUATION_PROFILES:
            triggers.update(SITUATION_PROFILES[situation])
        else:
            # Treat as direct trigger
            triggers.add(situation)

    # Add any additional explicit triggers
    if additional_triggers:
        triggers.update(additional_triggers)

    # Find matching documents
    required_docs = {}
    for doc_id, doc_info in DOCUMENT_DEFINITIONS.items():
        doc_triggers = set(doc_info["triggers"])
        if doc_triggers & triggers:  # If any trigger matches
            category = doc_info["category"]
            if category not in required_docs:
                required_docs[category] = []
            required_docs[category].append({
                "id": doc_id,
                "name": doc_info["name"],
                "description": doc_info["description"],
                "source": doc_info["source"],
                "irs_form": doc_info["irs_form"],
                "status": "pending"
            })

    return required_docs


def generate_checklist(situations: List[str], output_format: str = "text") -> str:
    """Generate a formatted checklist."""

    docs = get_required_documents(situations)

    if output_format == "json":
        return json.dumps(docs, indent=2)

    # Text format
    lines = []
    lines.append("\n" + "="*70)
    lines.append("TAX DOCUMENT CHECKLIST")
    lines.append("="*70)
    lines.append(f"\nBased on situations: {', '.join(situations)}\n")

    category_names = {
        "income": "INCOME DOCUMENTS",
        "deduction": "DEDUCTION DOCUMENTS",
        "health": "HEALTH INSURANCE DOCUMENTS",
        "retirement": "RETIREMENT DOCUMENTS",
        "self_employment": "SELF-EMPLOYMENT DOCUMENTS",
        "credit": "TAX CREDIT DOCUMENTS",
        "prior_year": "PRIOR YEAR DOCUMENTS"
    }

    for category, category_label in category_names.items():
        if category in docs:
            lines.append(f"\n{category_label}")
            lines.append("-" * len(category_label))
            for doc in docs[category]:
                lines.append(f"\n[ ] {doc['name']}")
                lines.append(f"    {doc['description']}")
                lines.append(f"    Source: {doc['source']}")
                if doc['irs_form'] != "N/A":
                    lines.append(f"    IRS Form: {doc['irs_form']}")

    lines.append("\n" + "="*70)
    lines.append("NOTES:")
    lines.append("- Check each box as you gather documents")
    lines.append("- Request missing documents from sources listed")
    lines.append("- IRS transcripts available at irs.gov/individuals/get-transcript")
    lines.append("="*70 + "\n")

    return "\n".join(lines)


def check_missing_documents(situations: List[str], collected: List[str]) -> Dict:
    """Check which required documents are still missing."""

    required = get_required_documents(situations)
    collected_set = set(collected)

    missing = {}
    complete = {}

    for category, docs in required.items():
        missing_in_category = []
        complete_in_category = []

        for doc in docs:
            if doc["id"] in collected_set:
                doc["status"] = "collected"
                complete_in_category.append(doc)
            else:
                doc["status"] = "missing"
                missing_in_category.append(doc)

        if missing_in_category:
            missing[category] = missing_in_category
        if complete_in_category:
            complete[category] = complete_in_category

    return {
        "missing": missing,
        "complete": complete,
        "summary": {
            "total_required": sum(len(docs) for docs in required.values()),
            "total_collected": len(collected_set),
            "total_missing": sum(len(docs) for docs in missing.values())
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate personalized tax document checklist"
    )
    parser.add_argument(
        "--situations",
        nargs="+",
        required=True,
        help="Tax situations (e.g., employed_w2 self_employed investor homeowner)"
    )
    parser.add_argument(
        "--triggers",
        nargs="+",
        default=[],
        help="Additional specific triggers"
    )
    parser.add_argument(
        "--collected",
        nargs="+",
        default=[],
        help="Document IDs already collected (to check missing)"
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "text"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--check-missing",
        action="store_true",
        help="Check for missing documents against collected list"
    )
    parser.add_argument(
        "--list-situations",
        action="store_true",
        help="List available situation profiles"
    )

    args = parser.parse_args()

    if args.list_situations:
        print("\nAvailable situation profiles:")
        print("-" * 40)
        for profile, triggers in SITUATION_PROFILES.items():
            print(f"\n{profile}:")
            print(f"  Triggers: {', '.join(triggers)}")
        return

    if args.check_missing:
        result = check_missing_documents(args.situations, args.collected)

        if args.output_format == "json":
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "="*60)
            print("DOCUMENT STATUS CHECK")
            print("="*60)

            summary = result["summary"]
            print(f"\nTotal Required: {summary['total_required']}")
            print(f"Collected: {summary['total_collected']}")
            print(f"Missing: {summary['total_missing']}")

            if result["missing"]:
                print("\nMISSING DOCUMENTS:")
                print("-" * 40)
                for category, docs in result["missing"].items():
                    print(f"\n{category.upper()}:")
                    for doc in docs:
                        print(f"  [ ] {doc['name']}")
                        print(f"      Source: {doc['source']}")

            if result["complete"]:
                print("\nCOLLECTED DOCUMENTS:")
                print("-" * 40)
                for category, docs in result["complete"].items():
                    print(f"\n{category.upper()}:")
                    for doc in docs:
                        print(f"  [x] {doc['name']}")

            print("="*60 + "\n")
    else:
        print(generate_checklist(args.situations, args.output_format))


if __name__ == "__main__":
    main()
