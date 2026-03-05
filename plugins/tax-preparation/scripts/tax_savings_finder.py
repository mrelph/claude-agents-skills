#!/usr/bin/env python3
"""
Tax Savings Finder - Analyze tax data to find potential savings opportunities.
Proactively identifies overlooked deductions, credits, and optimization strategies.
"""

import argparse
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class TaxOpportunity:
    category: str
    name: str
    description: str
    potential_savings: str
    priority: Priority
    action_required: str
    documentation_needed: List[str]


# Tax savings rules and thresholds
SAVINGS_RULES = {
    "hsa_contribution": {
        "single_limit": 4150,
        "family_limit": 8300,
        "catchup_55_plus": 1000
    },
    "ira_contribution": {
        "limit": 7000,
        "catchup_50_plus": 1000
    },
    "401k_contribution": {
        "limit": 23000,
        "catchup_50_plus": 7500
    },
    "standard_deduction": {
        "single": 14600,
        "married_jointly": 29200,
        "head_of_household": 21900
    },
    "salt_cap": 10000,
    "medical_threshold": 0.075,  # 7.5% of AGI
    "charitable_cash_limit": 0.60,  # 60% of AGI
    "eitc_limits": {
        0: {"max_credit": 632, "max_income_single": 18591, "max_income_mfj": 25511},
        1: {"max_credit": 4213, "max_income_single": 49084, "max_income_mfj": 56004},
        2: {"max_credit": 6960, "max_income_single": 55768, "max_income_mfj": 62688},
        3: {"max_credit": 7830, "max_income_single": 59899, "max_income_mfj": 66819}
    },
    "savers_credit_limits": {
        "mfj": {"50_percent": 46000, "20_percent": 50000, "10_percent": 76500},
        "single": {"50_percent": 23000, "20_percent": 25000, "10_percent": 38250}
    }
}


def analyze_retirement_contributions(data: Dict) -> List[TaxOpportunity]:
    """Find retirement contribution opportunities."""
    opportunities = []

    age = data.get("age", 40)
    filing_status = data.get("filing_status", "single")
    agi = data.get("agi", 0)

    # HSA analysis
    if data.get("has_hdhp", False):
        hsa_contributed = data.get("hsa_contributions", 0)
        coverage = data.get("hsa_coverage", "single")
        limit = SAVINGS_RULES["hsa_contribution"]["family_limit" if coverage == "family" else "single_limit"]
        if age >= 55:
            limit += SAVINGS_RULES["hsa_contribution"]["catchup_55_plus"]

        remaining = limit - hsa_contributed
        if remaining > 0:
            # Estimate savings at marginal rate
            marginal_rate = estimate_marginal_rate(agi, filing_status)
            potential_tax_savings = remaining * marginal_rate

            opportunities.append(TaxOpportunity(
                category="Retirement",
                name="HSA Contribution",
                description=f"You can contribute ${remaining:,.0f} more to your HSA",
                potential_savings=f"${potential_tax_savings:,.0f} in tax savings",
                priority=Priority.HIGH,
                action_required=f"Contribute additional ${remaining:,.0f} to HSA before April 15",
                documentation_needed=["HSA contribution receipts", "HDHP coverage documentation"]
            ))

    # Traditional IRA analysis
    ira_contributed = data.get("ira_contributions", 0)
    ira_limit = SAVINGS_RULES["ira_contribution"]["limit"]
    if age >= 50:
        ira_limit += SAVINGS_RULES["ira_contribution"]["catchup_50_plus"]

    ira_remaining = ira_limit - ira_contributed
    if ira_remaining > 0 and can_deduct_ira(data):
        marginal_rate = estimate_marginal_rate(agi, filing_status)
        potential_savings = ira_remaining * marginal_rate

        opportunities.append(TaxOpportunity(
            category="Retirement",
            name="Traditional IRA Contribution",
            description=f"You may be able to contribute ${ira_remaining:,.0f} more to Traditional IRA",
            potential_savings=f"Up to ${potential_savings:,.0f} in tax savings",
            priority=Priority.HIGH,
            action_required=f"Contribute to Traditional IRA before April 15 for prior year",
            documentation_needed=["Form 5498 will be issued by May 31"]
        ))

    # 401k analysis
    if data.get("has_401k", False):
        contributed_401k = data.get("401k_contributions", 0)
        limit_401k = SAVINGS_RULES["401k_contribution"]["limit"]
        if age >= 50:
            limit_401k += SAVINGS_RULES["401k_contribution"]["catchup_50_plus"]

        remaining_401k = limit_401k - contributed_401k
        if remaining_401k > 0:
            opportunities.append(TaxOpportunity(
                category="Retirement",
                name="401(k) Contribution",
                description=f"You have ${remaining_401k:,.0f} of 401(k) contribution room remaining",
                potential_savings="Reduces taxable income dollar-for-dollar",
                priority=Priority.MEDIUM,
                action_required="Increase 401(k) contributions for remaining pay periods",
                documentation_needed=["Year-end pay stub", "W-2 Box 12 Code D"]
            ))

    return opportunities


def analyze_deductions(data: Dict) -> List[TaxOpportunity]:
    """Find deduction opportunities."""
    opportunities = []

    filing_status = data.get("filing_status", "single")
    agi = data.get("agi", 0)

    # Standard vs itemized analysis
    std_deduction = SAVINGS_RULES["standard_deduction"].get(filing_status, 14600)

    itemized = calculate_itemized_total(data)

    if itemized > std_deduction * 0.8 and itemized < std_deduction:
        # Close to itemizing - suggest bunching
        gap = std_deduction - itemized
        opportunities.append(TaxOpportunity(
            category="Deductions",
            name="Deduction Bunching Strategy",
            description=f"You're ${gap:,.0f} away from itemizing. Consider bunching deductions.",
            potential_savings="Could save thousands by alternating years",
            priority=Priority.MEDIUM,
            action_required="Prepay property taxes, make extra charitable donations before year-end",
            documentation_needed=["Property tax receipts", "Charitable donation receipts"]
        ))

    # SALT cap analysis
    salt_paid = data.get("state_taxes", 0) + data.get("property_taxes", 0)
    if salt_paid > SAVINGS_RULES["salt_cap"]:
        lost_to_cap = salt_paid - SAVINGS_RULES["salt_cap"]
        opportunities.append(TaxOpportunity(
            category="Deductions",
            name="SALT Cap Impact",
            description=f"You're losing ${lost_to_cap:,.0f} in SALT deductions due to $10,000 cap",
            potential_savings="Consider timing strategies or state tax planning",
            priority=Priority.LOW,
            action_required="Review if any deductions can be shifted or if state residency changes make sense",
            documentation_needed=["Property tax bills", "State income tax payments"]
        ))

    # Medical expenses analysis
    medical = data.get("medical_expenses", 0)
    medical_threshold = agi * SAVINGS_RULES["medical_threshold"]
    if medical > 0 and medical < medical_threshold:
        shortfall = medical_threshold - medical
        opportunities.append(TaxOpportunity(
            category="Deductions",
            name="Medical Expense Threshold",
            description=f"Medical expenses ${shortfall:,.0f} below 7.5% AGI threshold",
            potential_savings="Consider timing elective procedures",
            priority=Priority.LOW,
            action_required="If planning medical procedures, consider timing for tax benefit",
            documentation_needed=["Medical receipts", "EOBs"]
        ))
    elif medical > medical_threshold:
        deductible = medical - medical_threshold
        opportunities.append(TaxOpportunity(
            category="Deductions",
            name="Medical Expense Deduction Available",
            description=f"You have ${deductible:,.0f} in deductible medical expenses",
            potential_savings=f"Tax savings if you itemize",
            priority=Priority.HIGH,
            action_required="Ensure all medical expenses are documented",
            documentation_needed=["All medical receipts", "Prescription records", "Mileage log for medical travel"]
        ))

    # Charitable analysis
    charitable = data.get("charitable_cash", 0) + data.get("charitable_noncash", 0)
    if charitable > 0 and not data.get("charitable_documented", True):
        opportunities.append(TaxOpportunity(
            category="Deductions",
            name="Charitable Documentation",
            description="Ensure all charitable donations are properly documented",
            potential_savings="Documentation required to claim deduction",
            priority=Priority.HIGH,
            action_required="Get written acknowledgment for donations $250+",
            documentation_needed=["Receipts for all donations", "Written acknowledgments", "Non-cash item valuations"]
        ))

    return opportunities


def analyze_credits(data: Dict) -> List[TaxOpportunity]:
    """Find tax credit opportunities."""
    opportunities = []

    filing_status = data.get("filing_status", "single")
    agi = data.get("agi", 0)
    children = data.get("qualifying_children", 0)
    earned_income = data.get("earned_income", agi)

    # EITC analysis
    if children <= 3:
        eitc_rules = SAVINGS_RULES["eitc_limits"].get(children, SAVINGS_RULES["eitc_limits"][0])
        income_limit = eitc_rules["max_income_mfj" if filing_status == "married_jointly" else "max_income_single"]

        if earned_income <= income_limit and data.get("investment_income", 0) <= 11600:
            if not data.get("claimed_eitc", False):
                opportunities.append(TaxOpportunity(
                    category="Credits",
                    name="Earned Income Tax Credit (EITC)",
                    description=f"You may qualify for EITC worth up to ${eitc_rules['max_credit']:,}",
                    potential_savings=f"Up to ${eitc_rules['max_credit']:,} refundable credit",
                    priority=Priority.HIGH,
                    action_required="Claim EITC on tax return",
                    documentation_needed=["Proof of earned income", "Children's SSNs if applicable"]
                ))

    # Saver's Credit analysis
    if data.get("retirement_contributions_total", 0) > 0:
        savers_limits = SAVINGS_RULES["savers_credit_limits"]["mfj" if filing_status == "married_jointly" else "single"]
        if agi <= savers_limits["10_percent"]:
            if agi <= savers_limits["50_percent"]:
                rate = "50%"
            elif agi <= savers_limits["20_percent"]:
                rate = "20%"
            else:
                rate = "10%"

            opportunities.append(TaxOpportunity(
                category="Credits",
                name="Saver's Credit",
                description=f"You may qualify for {rate} Saver's Credit on retirement contributions",
                potential_savings="Up to $1,000 ($2,000 MFJ) credit",
                priority=Priority.HIGH,
                action_required="Claim Saver's Credit on Form 8880",
                documentation_needed=["Retirement contribution records"]
            ))

    # Child and Dependent Care Credit
    if data.get("childcare_expenses", 0) > 0:
        if not data.get("claimed_childcare_credit", False):
            opportunities.append(TaxOpportunity(
                category="Credits",
                name="Child and Dependent Care Credit",
                description="You have qualifying childcare expenses",
                potential_savings="Credit of 20-35% of expenses up to $3,000/$6,000",
                priority=Priority.HIGH,
                action_required="Claim credit on Form 2441",
                documentation_needed=["Provider name, address, SSN/EIN", "Amount paid per provider"]
            ))

    # Education Credits
    if data.get("education_expenses", 0) > 0:
        opportunities.append(TaxOpportunity(
            category="Credits",
            name="Education Credits",
            description="You may qualify for American Opportunity or Lifetime Learning Credit",
            potential_savings="Up to $2,500 (AOTC) or $2,000 (LLC) per return",
            priority=Priority.HIGH,
            action_required="Evaluate which credit is better; AOTC partially refundable",
            documentation_needed=["Form 1098-T", "Receipts for books and supplies"]
        ))

    # Energy Credits
    if data.get("energy_improvements", False):
        opportunities.append(TaxOpportunity(
            category="Credits",
            name="Residential Energy Credits",
            description="You may qualify for energy efficiency credits",
            potential_savings="30% of qualified expenses, various limits",
            priority=Priority.MEDIUM,
            action_required="Claim credit on Form 5695",
            documentation_needed=["Receipts for improvements", "Manufacturer certifications"]
        ))

    # Foreign Tax Credit
    if data.get("foreign_tax_paid", 0) > 0:
        ftc = data.get("foreign_tax_paid", 0)
        opportunities.append(TaxOpportunity(
            category="Credits",
            name="Foreign Tax Credit",
            description=f"You paid ${ftc:.2f} in foreign taxes (check 1099-DIV Box 7)",
            potential_savings=f"${ftc:.2f} credit available",
            priority=Priority.MEDIUM,
            action_required="Claim credit directly or file Form 1116",
            documentation_needed=["1099-DIV showing foreign tax paid"]
        ))

    return opportunities


def analyze_self_employment(data: Dict) -> List[TaxOpportunity]:
    """Find self-employment tax opportunities."""
    opportunities = []

    if not data.get("self_employed", False):
        return opportunities

    se_income = data.get("self_employment_income", 0)

    # Home office
    if data.get("works_from_home", False) and not data.get("claimed_home_office", False):
        opportunities.append(TaxOpportunity(
            category="Self-Employment",
            name="Home Office Deduction",
            description="You may qualify for home office deduction",
            potential_savings="$5/sq ft up to $1,500 (simplified) or actual expenses",
            priority=Priority.HIGH,
            action_required="Calculate using simplified or regular method",
            documentation_needed=["Office square footage", "Total home square footage", "Home expense records"]
        ))

    # Vehicle expenses
    if data.get("business_miles", 0) > 0:
        miles = data.get("business_miles", 0)
        deduction = miles * 0.67  # 2024 rate
        opportunities.append(TaxOpportunity(
            category="Self-Employment",
            name="Vehicle Deduction",
            description=f"{miles:,} business miles = ${deduction:,.0f} deduction at standard rate",
            potential_savings=f"${deduction:,.0f} deduction",
            priority=Priority.HIGH,
            action_required="Claim on Schedule C; compare to actual expense method",
            documentation_needed=["Contemporaneous mileage log"]
        ))

    # Self-employed health insurance
    if data.get("pays_own_health_insurance", False):
        premiums = data.get("health_insurance_premiums", 0)
        if premiums > 0:
            opportunities.append(TaxOpportunity(
                category="Self-Employment",
                name="Self-Employed Health Insurance Deduction",
                description=f"Deduct ${premiums:,.0f} in health insurance premiums above-the-line",
                potential_savings=f"Reduces AGI by ${premiums:,.0f}",
                priority=Priority.HIGH,
                action_required="Claim on Schedule 1 Line 17",
                documentation_needed=["Health insurance premium statements"]
            ))

    # Retirement contributions
    if se_income > 0:
        sep_limit = min(se_income * 0.25, 69000)
        opportunities.append(TaxOpportunity(
            category="Self-Employment",
            name="SEP-IRA Contribution",
            description=f"You can contribute up to ${sep_limit:,.0f} to SEP-IRA",
            potential_savings=f"Reduces taxable income by up to ${sep_limit:,.0f}",
            priority=Priority.HIGH,
            action_required="Contribute to SEP-IRA before tax filing deadline (with extension)",
            documentation_needed=["SEP-IRA contribution records"]
        ))

    return opportunities


def analyze_investment_taxes(data: Dict) -> List[TaxOpportunity]:
    """Find investment tax opportunities."""
    opportunities = []

    # Capital loss carryforward
    if data.get("capital_loss_carryforward", 0) > 0:
        carryforward = data.get("capital_loss_carryforward", 0)
        opportunities.append(TaxOpportunity(
            category="Investments",
            name="Capital Loss Carryforward",
            description=f"You have ${carryforward:,.0f} in capital loss carryforward",
            potential_savings="Can offset gains + $3,000 ordinary income annually",
            priority=Priority.MEDIUM,
            action_required="Apply carryforward on Schedule D",
            documentation_needed=["Prior year Schedule D with carryforward worksheet"]
        ))

    # Tax-loss harvesting
    if data.get("unrealized_losses", 0) > 0:
        losses = data.get("unrealized_losses", 0)
        opportunities.append(TaxOpportunity(
            category="Investments",
            name="Tax-Loss Harvesting Opportunity",
            description=f"You have ${losses:,.0f} in unrealized losses",
            potential_savings="Can offset gains and reduce taxes",
            priority=Priority.MEDIUM,
            action_required="Consider selling to realize losses (watch wash sale rule)",
            documentation_needed=["Brokerage statements showing cost basis"]
        ))

    # 0% LTCG bracket
    filing_status = data.get("filing_status", "single")
    taxable_income = data.get("taxable_income", 0)
    ltcg_threshold = 47025 if filing_status == "single" else 94050

    if taxable_income < ltcg_threshold and data.get("unrealized_gains", 0) > 0:
        room = ltcg_threshold - taxable_income
        opportunities.append(TaxOpportunity(
            category="Investments",
            name="0% Long-Term Capital Gains",
            description=f"You have ${room:,.0f} of room in 0% LTCG bracket",
            potential_savings="Realize gains tax-free, reset basis higher",
            priority=Priority.HIGH,
            action_required="Consider selling appreciated assets to reset basis",
            documentation_needed=["Brokerage statements", "Cost basis records"]
        ))

    return opportunities


def estimate_marginal_rate(agi: float, filing_status: str) -> float:
    """Estimate marginal tax rate."""
    brackets = {
        "single": [(11600, 0.10), (47150, 0.12), (100525, 0.22), (191950, 0.24), (243725, 0.32), (609350, 0.35), (float('inf'), 0.37)],
        "married_jointly": [(23200, 0.10), (94300, 0.12), (201050, 0.22), (383900, 0.24), (487450, 0.32), (731200, 0.35), (float('inf'), 0.37)]
    }

    bracket_list = brackets.get(filing_status, brackets["single"])
    for threshold, rate in bracket_list:
        if agi <= threshold:
            return rate
    return 0.37


def can_deduct_ira(data: Dict) -> bool:
    """Check if Traditional IRA contribution is deductible."""
    has_workplace_plan = data.get("has_workplace_plan", False)
    filing_status = data.get("filing_status", "single")
    agi = data.get("agi", 0)

    if not has_workplace_plan:
        return True

    # Simplified - full deduction phaseouts
    if filing_status == "single":
        return agi < 87000
    else:
        return agi < 143000


def calculate_itemized_total(data: Dict) -> float:
    """Calculate total itemized deductions."""
    medical = max(0, data.get("medical_expenses", 0) - data.get("agi", 0) * 0.075)
    salt = min(data.get("state_taxes", 0) + data.get("property_taxes", 0), 10000)
    mortgage = data.get("mortgage_interest", 0)
    charitable = data.get("charitable_cash", 0) + data.get("charitable_noncash", 0)

    return medical + salt + mortgage + charitable


def find_all_opportunities(data: Dict) -> Dict:
    """Run all analyses and return consolidated opportunities."""
    all_opportunities = []

    all_opportunities.extend(analyze_retirement_contributions(data))
    all_opportunities.extend(analyze_deductions(data))
    all_opportunities.extend(analyze_credits(data))
    all_opportunities.extend(analyze_self_employment(data))
    all_opportunities.extend(analyze_investment_taxes(data))

    # Sort by priority
    priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
    all_opportunities.sort(key=lambda x: priority_order[x.priority])

    # Convert to serializable format
    results = {
        "summary": {
            "total_opportunities": len(all_opportunities),
            "high_priority": len([o for o in all_opportunities if o.priority == Priority.HIGH]),
            "medium_priority": len([o for o in all_opportunities if o.priority == Priority.MEDIUM]),
            "low_priority": len([o for o in all_opportunities if o.priority == Priority.LOW])
        },
        "opportunities": [
            {
                "category": o.category,
                "name": o.name,
                "description": o.description,
                "potential_savings": o.potential_savings,
                "priority": o.priority.value,
                "action_required": o.action_required,
                "documentation_needed": o.documentation_needed
            }
            for o in all_opportunities
        ]
    }

    return results


def main():
    parser = argparse.ArgumentParser(description="Find tax savings opportunities")
    parser.add_argument("--data-file", type=str, help="JSON file with tax data")
    parser.add_argument("--output-format", choices=["json", "text"], default="text")

    # Allow inline data specification
    parser.add_argument("--agi", type=float, default=0)
    parser.add_argument("--filing-status", choices=["single", "married_jointly", "head_of_household"], default="single")
    parser.add_argument("--age", type=int, default=40)
    parser.add_argument("--qualifying-children", type=int, default=0)

    args = parser.parse_args()

    # Load data from file or build from args
    if args.data_file:
        with open(args.data_file) as f:
            data = json.load(f)
    else:
        data = {
            "agi": args.agi,
            "filing_status": args.filing_status,
            "age": args.age,
            "qualifying_children": args.qualifying_children
        }

    results = find_all_opportunities(data)

    if args.output_format == "json":
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*70)
        print("TAX SAVINGS OPPORTUNITIES")
        print("="*70)

        summary = results["summary"]
        print(f"\nFound {summary['total_opportunities']} opportunities:")
        print(f"  HIGH Priority: {summary['high_priority']}")
        print(f"  MEDIUM Priority: {summary['medium_priority']}")
        print(f"  LOW Priority: {summary['low_priority']}")

        for opp in results["opportunities"]:
            print(f"\n{'='*70}")
            print(f"[{opp['priority']}] {opp['name']}")
            print(f"Category: {opp['category']}")
            print(f"\n{opp['description']}")
            print(f"\nPotential Savings: {opp['potential_savings']}")
            print(f"\nAction Required: {opp['action_required']}")
            print(f"\nDocumentation Needed:")
            for doc in opp['documentation_needed']:
                print(f"  - {doc}")

        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
