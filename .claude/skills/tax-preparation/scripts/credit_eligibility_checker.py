#!/usr/bin/env python3
"""
Credit Eligibility Checker - Determine eligibility for major tax credits
and calculate potential credit amounts.
"""

import argparse
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CreditResult:
    name: str
    eligible: bool
    amount: float
    refundable_amount: float
    phaseout_applied: bool
    notes: List[str]
    requirements_met: Dict[str, bool]
    documentation_needed: List[str]


# 2024 Credit Parameters
CREDIT_PARAMS = {
    "child_tax_credit": {
        "credit_per_child": 2000,
        "refundable_max": 1700,
        "age_limit": 17,
        "phaseout_start_single": 200000,
        "phaseout_start_mfj": 400000,
        "phaseout_rate": 50  # $50 per $1000 over threshold
    },
    "other_dependent_credit": {
        "credit_per_dependent": 500,
        "phaseout_start_single": 200000,
        "phaseout_start_mfj": 400000
    },
    "eitc": {
        0: {"max_credit": 632, "earned_for_max": 7830, "phaseout_start_single": 9800, "phaseout_start_mfj": 16370, "max_single": 18591, "max_mfj": 25511},
        1: {"max_credit": 4213, "earned_for_max": 12390, "phaseout_start_single": 22720, "phaseout_start_mfj": 29640, "max_single": 49084, "max_mfj": 56004},
        2: {"max_credit": 6960, "earned_for_max": 17400, "phaseout_start_single": 22720, "phaseout_start_mfj": 29640, "max_single": 55768, "max_mfj": 62688},
        3: {"max_credit": 7830, "earned_for_max": 17400, "phaseout_start_single": 22720, "phaseout_start_mfj": 29640, "max_single": 59899, "max_mfj": 66819}
    },
    "eitc_investment_limit": 11600,
    "child_dependent_care": {
        "expense_limit_one": 3000,
        "expense_limit_two_plus": 6000,
        "max_percentage": 35,
        "min_percentage": 20,
        "agi_for_max": 15000,
        "agi_for_min": 43000
    },
    "aotc": {
        "max_credit": 2500,
        "refundable_percent": 40,
        "expense_100_percent": 2000,
        "expense_25_percent": 2000,
        "phaseout_start_single": 80000,
        "phaseout_end_single": 90000,
        "phaseout_start_mfj": 160000,
        "phaseout_end_mfj": 180000,
        "max_years": 4
    },
    "lifetime_learning": {
        "max_credit": 2000,
        "credit_rate": 0.20,
        "expense_limit": 10000,
        "phaseout_start_single": 80000,
        "phaseout_end_single": 90000,
        "phaseout_start_mfj": 160000,
        "phaseout_end_mfj": 180000
    },
    "savers_credit": {
        "max_contribution": 2000,
        "rates": {
            "mfj": [(46000, 0.50), (50000, 0.20), (76500, 0.10)],
            "hoh": [(34500, 0.50), (37500, 0.20), (57375, 0.10)],
            "single": [(23000, 0.50), (25000, 0.20), (38250, 0.10)]
        }
    },
    "adoption_credit": {
        "max_credit": 16810,
        "phaseout_start": 252150,
        "phaseout_end": 292150
    }
}


def calculate_child_tax_credit(data: Dict) -> CreditResult:
    """Calculate Child Tax Credit eligibility and amount."""
    params = CREDIT_PARAMS["child_tax_credit"]

    qualifying_children = data.get("children_under_17", 0)
    agi = data.get("agi", 0)
    filing_status = data.get("filing_status", "single")
    earned_income = data.get("earned_income", 0)

    requirements = {
        "has_qualifying_children": qualifying_children > 0,
        "children_have_ssn": data.get("children_have_ssn", True),
        "income_below_limit": True  # CTC phases out slowly, rarely fully eliminated
    }

    notes = []
    docs = ["Children's Social Security cards", "Proof of relationship", "Proof of residency"]

    if not requirements["has_qualifying_children"]:
        return CreditResult(
            name="Child Tax Credit",
            eligible=False,
            amount=0,
            refundable_amount=0,
            phaseout_applied=False,
            notes=["No qualifying children under age 17"],
            requirements_met=requirements,
            documentation_needed=docs
        )

    # Calculate base credit
    base_credit = qualifying_children * params["credit_per_child"]

    # Apply phaseout
    phaseout_start = params["phaseout_start_mfj"] if filing_status == "married_jointly" else params["phaseout_start_single"]
    phaseout_applied = False

    if agi > phaseout_start:
        excess = agi - phaseout_start
        reduction = (excess // 1000) * params["phaseout_rate"]
        base_credit = max(0, base_credit - reduction)
        phaseout_applied = True
        notes.append(f"Credit reduced by ${reduction:,.0f} due to income phaseout")

    # Calculate refundable portion (Additional Child Tax Credit)
    if earned_income > 2500:
        potential_refund = (earned_income - 2500) * 0.15
        refundable = min(potential_refund, params["refundable_max"] * qualifying_children, base_credit)
    else:
        refundable = 0

    notes.append(f"Credit: ${params['credit_per_child']:,} per qualifying child under 17")

    return CreditResult(
        name="Child Tax Credit",
        eligible=base_credit > 0,
        amount=base_credit,
        refundable_amount=refundable,
        phaseout_applied=phaseout_applied,
        notes=notes,
        requirements_met=requirements,
        documentation_needed=docs
    )


def calculate_eitc(data: Dict) -> CreditResult:
    """Calculate Earned Income Tax Credit eligibility and amount."""
    qualifying_children = min(data.get("qualifying_children_eitc", 0), 3)
    earned_income = data.get("earned_income", 0)
    agi = data.get("agi", 0)
    investment_income = data.get("investment_income", 0)
    filing_status = data.get("filing_status", "single")
    age = data.get("age", 30)

    params = CREDIT_PARAMS["eitc"][qualifying_children]

    requirements = {
        "has_earned_income": earned_income > 0,
        "investment_income_under_limit": investment_income <= CREDIT_PARAMS["eitc_investment_limit"],
        "income_under_limit": True,
        "valid_ssn": data.get("has_valid_ssn", True),
        "not_mfs": filing_status != "married_separately",
        "age_requirement": qualifying_children > 0 or (25 <= age <= 64)
    }

    notes = []
    docs = ["Proof of earned income (W-2, Schedule C)", "Children's SSNs if applicable", "Proof of residency for children"]

    # Check disqualifying factors
    if not requirements["has_earned_income"]:
        return CreditResult("Earned Income Tax Credit", False, 0, 0, False,
                           ["No earned income"], requirements, docs)

    if not requirements["investment_income_under_limit"]:
        return CreditResult("Earned Income Tax Credit", False, 0, 0, False,
                           [f"Investment income ${investment_income:,.0f} exceeds ${CREDIT_PARAMS['eitc_investment_limit']:,} limit"],
                           requirements, docs)

    if not requirements["not_mfs"]:
        return CreditResult("Earned Income Tax Credit", False, 0, 0, False,
                           ["Cannot claim EITC when filing Married Filing Separately"],
                           requirements, docs)

    if not requirements["age_requirement"]:
        return CreditResult("Earned Income Tax Credit", False, 0, 0, False,
                           ["Without qualifying children, must be age 25-64"],
                           requirements, docs)

    # Determine income limit
    is_mfj = filing_status == "married_jointly"
    income_limit = params["max_mfj"] if is_mfj else params["max_single"]

    income_for_calc = max(earned_income, agi)

    if income_for_calc > income_limit:
        requirements["income_under_limit"] = False
        return CreditResult("Earned Income Tax Credit", False, 0, 0, False,
                           [f"Income ${income_for_calc:,.0f} exceeds limit ${income_limit:,}"],
                           requirements, docs)

    # Calculate credit (simplified)
    phaseout_start = params["phaseout_start_mfj"] if is_mfj else params["phaseout_start_single"]

    if income_for_calc <= params["earned_for_max"]:
        # Phase-in
        credit = min(earned_income * 0.34, params["max_credit"])  # Simplified rate
    elif income_for_calc <= phaseout_start:
        credit = params["max_credit"]
    else:
        # Phaseout
        excess = income_for_calc - phaseout_start
        reduction = excess * 0.1598  # Simplified phaseout rate
        credit = max(0, params["max_credit"] - reduction)

    notes.append(f"Max credit for {qualifying_children} children: ${params['max_credit']:,}")
    notes.append("EITC is fully refundable")

    return CreditResult(
        name="Earned Income Tax Credit",
        eligible=credit > 0,
        amount=credit,
        refundable_amount=credit,  # EITC is fully refundable
        phaseout_applied=income_for_calc > phaseout_start,
        notes=notes,
        requirements_met=requirements,
        documentation_needed=docs
    )


def calculate_child_dependent_care(data: Dict) -> CreditResult:
    """Calculate Child and Dependent Care Credit."""
    params = CREDIT_PARAMS["child_dependent_care"]

    qualifying_persons = data.get("qualifying_dependents_care", 0)
    expenses = data.get("childcare_expenses", 0)
    agi = data.get("agi", 0)
    earned_income = data.get("earned_income", 0)
    spouse_earned_income = data.get("spouse_earned_income", earned_income)
    dependent_care_fsa = data.get("dependent_care_fsa", 0)

    requirements = {
        "has_qualifying_person": qualifying_persons > 0,
        "has_expenses": expenses > 0,
        "has_earned_income": earned_income > 0,
        "expenses_for_work": True  # Assumed
    }

    notes = []
    docs = ["Provider name, address, SSN/EIN", "Amount paid to each provider", "Dependent care FSA records (if any)"]

    if not requirements["has_qualifying_person"]:
        return CreditResult("Child and Dependent Care Credit", False, 0, 0, False,
                           ["No qualifying person (child under 13 or disabled dependent)"],
                           requirements, docs)

    if not requirements["has_expenses"]:
        return CreditResult("Child and Dependent Care Credit", False, 0, 0, False,
                           ["No qualifying childcare expenses"], requirements, docs)

    # Expense limit
    expense_limit = params["expense_limit_two_plus"] if qualifying_persons >= 2 else params["expense_limit_one"]

    # Reduce by dependent care FSA
    net_expenses = max(0, expenses - dependent_care_fsa)

    # Limit by earned income (lower of taxpayer or spouse)
    lower_earned = min(earned_income, spouse_earned_income)
    eligible_expenses = min(net_expenses, expense_limit, lower_earned)

    # Determine credit percentage based on AGI
    if agi <= params["agi_for_max"]:
        percentage = params["max_percentage"]
    elif agi >= params["agi_for_min"]:
        percentage = params["min_percentage"]
    else:
        # Gradual reduction
        reduction = ((agi - params["agi_for_max"]) // 2000)
        percentage = max(params["min_percentage"], params["max_percentage"] - reduction)

    credit = eligible_expenses * (percentage / 100)

    notes.append(f"Credit rate: {percentage}% of eligible expenses")
    notes.append(f"Expense limit: ${expense_limit:,}")
    if dependent_care_fsa > 0:
        notes.append(f"Reduced by ${dependent_care_fsa:,} FSA contributions")

    return CreditResult(
        name="Child and Dependent Care Credit",
        eligible=credit > 0,
        amount=credit,
        refundable_amount=0,  # Non-refundable
        phaseout_applied=agi > params["agi_for_max"],
        notes=notes,
        requirements_met=requirements,
        documentation_needed=docs
    )


def calculate_aotc(data: Dict) -> CreditResult:
    """Calculate American Opportunity Tax Credit."""
    params = CREDIT_PARAMS["aotc"]

    expenses = data.get("education_expenses", 0)
    agi = data.get("agi", 0)
    filing_status = data.get("filing_status", "single")
    years_claimed = data.get("aotc_years_claimed", 0)
    is_student = data.get("is_eligible_student", False)

    requirements = {
        "is_eligible_student": is_student,
        "first_four_years": years_claimed < 4,
        "has_expenses": expenses > 0,
        "at_least_half_time": data.get("at_least_half_time", True),
        "no_felony_drug_conviction": data.get("no_felony_drug", True)
    }

    notes = []
    docs = ["Form 1098-T", "Receipts for books and supplies", "Enrollment verification"]

    if not requirements["is_eligible_student"]:
        return CreditResult("American Opportunity Tax Credit", False, 0, 0, False,
                           ["No eligible student"], requirements, docs)

    if not requirements["first_four_years"]:
        return CreditResult("American Opportunity Tax Credit", False, 0, 0, False,
                           ["AOTC already claimed for 4 years"], requirements, docs)

    # Calculate credit
    credit = min(expenses, params["expense_100_percent"]) * 1.0
    if expenses > params["expense_100_percent"]:
        credit += min(expenses - params["expense_100_percent"], params["expense_25_percent"]) * 0.25

    credit = min(credit, params["max_credit"])

    # Apply phaseout
    is_mfj = filing_status == "married_jointly"
    phaseout_start = params["phaseout_start_mfj"] if is_mfj else params["phaseout_start_single"]
    phaseout_end = params["phaseout_end_mfj"] if is_mfj else params["phaseout_end_single"]

    phaseout_applied = False
    if agi > phaseout_start:
        if agi >= phaseout_end:
            credit = 0
            notes.append("Credit fully phased out due to income")
        else:
            reduction_ratio = (agi - phaseout_start) / (phaseout_end - phaseout_start)
            credit = credit * (1 - reduction_ratio)
            phaseout_applied = True
            notes.append(f"Credit reduced due to income phaseout")

    refundable = credit * params["refundable_percent"] / 100

    notes.append(f"Max credit: ${params['max_credit']:,} per student")
    notes.append(f"40% refundable (up to $1,000)")

    return CreditResult(
        name="American Opportunity Tax Credit",
        eligible=credit > 0,
        amount=credit,
        refundable_amount=refundable,
        phaseout_applied=phaseout_applied,
        notes=notes,
        requirements_met=requirements,
        documentation_needed=docs
    )


def calculate_savers_credit(data: Dict) -> CreditResult:
    """Calculate Retirement Savings Contribution Credit."""
    params = CREDIT_PARAMS["savers_credit"]

    contributions = data.get("retirement_contributions", 0)
    agi = data.get("agi", 0)
    filing_status = data.get("filing_status", "single")
    age = data.get("age", 30)
    is_student = data.get("is_full_time_student", False)

    status_key = "mfj" if filing_status == "married_jointly" else ("hoh" if filing_status == "head_of_household" else "single")
    rates = params["rates"][status_key]

    requirements = {
        "has_contributions": contributions > 0,
        "age_18_plus": age >= 18,
        "not_full_time_student": not is_student,
        "not_dependent": not data.get("is_dependent", False),
        "income_under_limit": agi <= rates[-1][0]
    }

    notes = []
    docs = ["Form 5498 (IRA)", "W-2 Box 12 (401k)", "Retirement account statements"]

    if not requirements["has_contributions"]:
        return CreditResult("Saver's Credit", False, 0, 0, False,
                           ["No retirement contributions"], requirements, docs)

    if not requirements["income_under_limit"]:
        return CreditResult("Saver's Credit", False, 0, 0, False,
                           [f"AGI ${agi:,.0f} exceeds limit ${rates[-1][0]:,}"], requirements, docs)

    if not requirements["age_18_plus"] or not requirements["not_full_time_student"]:
        return CreditResult("Saver's Credit", False, 0, 0, False,
                           ["Must be 18+, not full-time student, not a dependent"], requirements, docs)

    # Determine rate
    credit_rate = 0
    for threshold, rate in rates:
        if agi <= threshold:
            credit_rate = rate
            break

    eligible_contributions = min(contributions, params["max_contribution"])
    credit = eligible_contributions * credit_rate

    notes.append(f"Credit rate: {credit_rate*100:.0f}% of contributions")
    notes.append(f"Max eligible contributions: ${params['max_contribution']:,}")

    return CreditResult(
        name="Saver's Credit",
        eligible=credit > 0,
        amount=credit,
        refundable_amount=0,
        phaseout_applied=False,
        notes=notes,
        requirements_met=requirements,
        documentation_needed=docs
    )


def check_all_credits(data: Dict) -> Dict:
    """Check eligibility for all major credits."""
    results = []

    # Run all credit calculations
    results.append(calculate_child_tax_credit(data))
    results.append(calculate_eitc(data))
    results.append(calculate_child_dependent_care(data))
    results.append(calculate_aotc(data))
    results.append(calculate_savers_credit(data))

    # Calculate totals
    total_credits = sum(r.amount for r in results if r.eligible)
    total_refundable = sum(r.refundable_amount for r in results if r.eligible)

    return {
        "summary": {
            "total_potential_credits": round(total_credits, 2),
            "total_refundable": round(total_refundable, 2),
            "credits_eligible": len([r for r in results if r.eligible]),
            "credits_checked": len(results)
        },
        "credits": [
            {
                "name": r.name,
                "eligible": r.eligible,
                "amount": round(r.amount, 2),
                "refundable_amount": round(r.refundable_amount, 2),
                "phaseout_applied": r.phaseout_applied,
                "notes": r.notes,
                "requirements_met": r.requirements_met,
                "documentation_needed": r.documentation_needed
            }
            for r in results
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Check tax credit eligibility")
    parser.add_argument("--data-file", type=str, help="JSON file with tax data")
    parser.add_argument("--output-format", choices=["json", "text"], default="text")

    # Common inline parameters
    parser.add_argument("--agi", type=float, default=50000)
    parser.add_argument("--earned-income", type=float, default=None)
    parser.add_argument("--filing-status", choices=["single", "married_jointly", "head_of_household"], default="single")
    parser.add_argument("--children-under-17", type=int, default=0)
    parser.add_argument("--qualifying-children-eitc", type=int, default=0)
    parser.add_argument("--childcare-expenses", type=float, default=0)
    parser.add_argument("--education-expenses", type=float, default=0)
    parser.add_argument("--retirement-contributions", type=float, default=0)
    parser.add_argument("--age", type=int, default=35)

    args = parser.parse_args()

    if args.data_file:
        with open(args.data_file) as f:
            data = json.load(f)
    else:
        data = {
            "agi": args.agi,
            "earned_income": args.earned_income or args.agi,
            "filing_status": args.filing_status,
            "children_under_17": args.children_under_17,
            "qualifying_children_eitc": args.qualifying_children_eitc or args.children_under_17,
            "childcare_expenses": args.childcare_expenses,
            "qualifying_dependents_care": 1 if args.childcare_expenses > 0 else 0,
            "education_expenses": args.education_expenses,
            "is_eligible_student": args.education_expenses > 0,
            "retirement_contributions": args.retirement_contributions,
            "age": args.age
        }

    results = check_all_credits(data)

    if args.output_format == "json":
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*70)
        print("TAX CREDIT ELIGIBILITY CHECK")
        print("="*70)

        summary = results["summary"]
        print(f"\nSUMMARY:")
        print(f"  Total Potential Credits: ${summary['total_potential_credits']:,.2f}")
        print(f"  Total Refundable: ${summary['total_refundable']:,.2f}")
        print(f"  Eligible Credits: {summary['credits_eligible']} of {summary['credits_checked']}")

        for credit in results["credits"]:
            print(f"\n{'-'*70}")
            status = "ELIGIBLE" if credit["eligible"] else "NOT ELIGIBLE"
            print(f"{credit['name']}: {status}")

            if credit["eligible"]:
                print(f"  Credit Amount: ${credit['amount']:,.2f}")
                if credit["refundable_amount"] > 0:
                    print(f"  Refundable Portion: ${credit['refundable_amount']:,.2f}")
                if credit["phaseout_applied"]:
                    print(f"  Note: Income phaseout applied")

            print(f"\n  Requirements:")
            for req, met in credit["requirements_met"].items():
                symbol = "[x]" if met else "[ ]"
                print(f"    {symbol} {req.replace('_', ' ').title()}")

            if credit["notes"]:
                print(f"\n  Notes:")
                for note in credit["notes"]:
                    print(f"    - {note}")

            if credit["eligible"]:
                print(f"\n  Documentation Needed:")
                for doc in credit["documentation_needed"]:
                    print(f"    - {doc}")

        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
