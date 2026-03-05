#!/usr/bin/env python3
"""
Report Validator for Research Consolidator

Validates consolidated reports for completeness, accuracy, and quality.
Checks for:
- Proper source attribution
- Orphaned claims (claims without sources)
- Conflict identification and resolution
- Confidence score justification
- Gap acknowledgment
- Executive summary accuracy

Usage:
    python report_validator.py --report final_report.md --sources sources.json
    python report_validator.py --report final_report.md --findings findings.json --gaps gaps.json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class ValidationResult:
    """Holds validation results."""
    check_name: str
    passed: bool
    message: str
    severity: str = "warning"  # info, warning, error
    details: List[str] = field(default_factory=list)


@dataclass
class ValidationSummary:
    """Holds overall validation summary."""
    total_checks: int = 0
    passed: int = 0
    warnings: int = 0
    errors: int = 0
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def score(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return self.passed / self.total_checks


def check_source_attribution(report_content: str, sources: List[dict]) -> ValidationResult:
    """Check that all sources are properly attributed in the report."""
    source_ids = {s.get("id", s.get("source_id", s)) for s in sources if isinstance(s, dict)}
    source_ids.update({s for s in sources if isinstance(s, str)})

    # Look for source references in report
    found_sources = set()
    for source_id in source_ids:
        if source_id in report_content:
            found_sources.add(source_id)

    missing_sources = source_ids - found_sources
    missing_ratio = len(missing_sources) / len(source_ids) if source_ids else 0

    if missing_ratio == 0:
        return ValidationResult(
            check_name="Source Attribution",
            passed=True,
            message="All sources properly attributed",
            severity="info"
        )
    elif missing_ratio < 0.5:
        return ValidationResult(
            check_name="Source Attribution",
            passed=True,
            message=f"{len(missing_sources)} source(s) not explicitly referenced",
            severity="warning",
            details=[f"Missing: {s}" for s in missing_sources]
        )
    else:
        return ValidationResult(
            check_name="Source Attribution",
            passed=False,
            message=f"Many sources not attributed ({len(missing_sources)}/{len(source_ids)})",
            severity="error",
            details=[f"Missing: {s}" for s in missing_sources]
        )


def check_orphaned_claims(report_content: str, findings: dict) -> ValidationResult:
    """Check for claims without proper source attribution."""
    # Look for claim patterns that should have sources
    claim_patterns = [
        r'(?:evidence|research|data|analysis)\s+(?:shows?|indicates?|suggests?)',
        r'(?:according to|per|based on)\s+\w+',
        r'\d+(?:\.\d+)?%\s+(?:of|growth|increase|decrease)'
    ]

    orphaned_claims = []
    lines = report_content.split('\n')

    for i, line in enumerate(lines, 1):
        for pattern in claim_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Check if there's a source reference nearby
                context = ' '.join(lines[max(0, i-2):min(len(lines), i+2)])
                if not re.search(r'(?:Source|SRC-|S\d+|according to)', context, re.IGNORECASE):
                    orphaned_claims.append(f"Line {i}: {line[:60]}...")

    if not orphaned_claims:
        return ValidationResult(
            check_name="Orphaned Claims",
            passed=True,
            message="All claims appear to have source attribution",
            severity="info"
        )
    elif len(orphaned_claims) <= 3:
        return ValidationResult(
            check_name="Orphaned Claims",
            passed=True,
            message=f"{len(orphaned_claims)} claim(s) may lack explicit source",
            severity="warning",
            details=orphaned_claims[:5]
        )
    else:
        return ValidationResult(
            check_name="Orphaned Claims",
            passed=False,
            message=f"{len(orphaned_claims)} claims may lack source attribution",
            severity="error",
            details=orphaned_claims[:10]
        )


def check_conflict_handling(report_content: str, findings: dict) -> ValidationResult:
    """Check that conflicts are identified and addressed."""
    conflicts = findings.get("conflicts", [])

    if not conflicts:
        # Check if report mentions no conflicts
        if re.search(r'no\s+(?:significant\s+)?conflicts?', report_content, re.IGNORECASE):
            return ValidationResult(
                check_name="Conflict Handling",
                passed=True,
                message="No conflicts to report (acknowledged in report)",
                severity="info"
            )
        return ValidationResult(
            check_name="Conflict Handling",
            passed=True,
            message="No conflicts identified",
            severity="info"
        )

    # Check if conflicts are mentioned in report
    conflicts_mentioned = 0
    conflicts_resolved = 0

    for conflict in conflicts:
        topic = conflict.get("topic", conflict.get("theme", ""))
        if topic and topic.lower() in report_content.lower():
            conflicts_mentioned += 1
            # Check if resolution is mentioned
            if conflict.get("resolution") and conflict["resolution"].lower() in report_content.lower():
                conflicts_resolved += 1

    if conflicts_mentioned == len(conflicts) and conflicts_resolved == len(conflicts):
        return ValidationResult(
            check_name="Conflict Handling",
            passed=True,
            message="All conflicts identified and resolved",
            severity="info"
        )
    elif conflicts_mentioned >= len(conflicts) * 0.5:
        return ValidationResult(
            check_name="Conflict Handling",
            passed=True,
            message=f"{conflicts_mentioned}/{len(conflicts)} conflicts addressed, {conflicts_resolved} resolved",
            severity="warning",
            details=[f"Conflict: {c.get('topic', 'Unknown')}" for c in conflicts]
        )
    else:
        return ValidationResult(
            check_name="Conflict Handling",
            passed=False,
            message=f"Only {conflicts_mentioned}/{len(conflicts)} conflicts addressed in report",
            severity="error",
            details=[f"Missing conflict: {c.get('topic', 'Unknown')}" for c in conflicts]
        )


def check_confidence_scores(report_content: str, findings: dict) -> ValidationResult:
    """Check that confidence scores are justified."""
    # Look for confidence mentions in report
    confidence_pattern = r'(?:confidence|confident|confidence\s+level)[:\s]+(?:HIGH|MEDIUM|LOW|VERY\s+HIGH|VERY\s+LOW|\d+\.?\d*)'

    confidence_mentions = re.findall(confidence_pattern, report_content, re.IGNORECASE)

    consolidated_findings = findings.get("consolidated_findings", [])
    findings_with_scores = [f for f in consolidated_findings if "confidence_score" in f or "confidence" in f]

    if not findings_with_scores:
        return ValidationResult(
            check_name="Confidence Scores",
            passed=True,
            message="No confidence scores to validate",
            severity="info"
        )

    if len(confidence_mentions) >= len(findings_with_scores):
        return ValidationResult(
            check_name="Confidence Scores",
            passed=True,
            message=f"{len(confidence_mentions)} confidence indicators found",
            severity="info"
        )
    elif len(confidence_mentions) >= len(findings_with_scores) * 0.5:
        return ValidationResult(
            check_name="Confidence Scores",
            passed=True,
            message=f"{len(confidence_mentions)} of {len(findings_with_scores)} findings have confidence noted",
            severity="warning"
        )
    else:
        return ValidationResult(
            check_name="Confidence Scores",
            passed=False,
            message=f"Only {len(confidence_mentions)} confidence indicators for {len(findings_with_scores)} findings",
            severity="error"
        )


def check_gap_acknowledgment(report_content: str, gaps: dict) -> ValidationResult:
    """Check that research gaps are acknowledged."""
    all_gaps = []
    for gap_type, gap_list in gaps.get("gaps", {}).items():
        all_gaps.extend(gap_list)

    if not all_gaps:
        if "gap" in report_content.lower() or "no significant gaps" in report_content.lower():
            return ValidationResult(
                check_name="Gap Acknowledgment",
                passed=True,
                message="Gap section present (no gaps or gaps acknowledged)",
                severity="info"
            )
        return ValidationResult(
            check_name="Gap Acknowledgment",
            passed=True,
            message="No gaps to acknowledge",
            severity="info"
        )

    # Check for gap section
    has_gap_section = bool(re.search(r'##?\s*(?:research\s+)?gaps?', report_content, re.IGNORECASE))

    # Count acknowledged gaps
    gaps_mentioned = 0
    high_impact_gaps = [g for g in all_gaps if g.get("impact") == "high"]

    for gap in all_gaps:
        topic = gap.get("topic", gap.get("source_id", ""))
        if topic and topic.lower() in report_content.lower():
            gaps_mentioned += 1

    if has_gap_section and gaps_mentioned >= len(high_impact_gaps):
        return ValidationResult(
            check_name="Gap Acknowledgment",
            passed=True,
            message=f"Gaps section present; {gaps_mentioned} gaps acknowledged",
            severity="info"
        )
    elif has_gap_section:
        return ValidationResult(
            check_name="Gap Acknowledgment",
            passed=True,
            message=f"Gaps section present but only {gaps_mentioned}/{len(all_gaps)} gaps explicitly mentioned",
            severity="warning",
            details=[f"High impact gap: {g.get('topic', 'Unknown')}" for g in high_impact_gaps]
        )
    else:
        return ValidationResult(
            check_name="Gap Acknowledgment",
            passed=False,
            message="No research gaps section found in report",
            severity="error",
            details=[f"Gap: {g.get('topic', g.get('description', 'Unknown'))}" for g in all_gaps[:5]]
        )


def check_executive_summary(report_content: str, findings: dict) -> ValidationResult:
    """Check that executive summary accurately reflects detailed findings."""
    # Find executive summary section
    exec_match = re.search(
        r'##?\s*Executive\s+Summary\s*(.*?)(?=##|\Z)',
        report_content,
        re.IGNORECASE | re.DOTALL
    )

    if not exec_match:
        return ValidationResult(
            check_name="Executive Summary",
            passed=False,
            message="No executive summary section found",
            severity="error"
        )

    exec_summary = exec_match.group(1)

    # Check for key components
    has_findings = bool(re.search(r'(?:key\s+)?findings?', exec_summary, re.IGNORECASE))
    has_recommendations = bool(re.search(r'recommend', exec_summary, re.IGNORECASE))
    has_uncertainty = bool(re.search(r'(?:uncertainty|conflict|gap|caveat)', exec_summary, re.IGNORECASE))

    components_present = sum([has_findings, has_recommendations, has_uncertainty])

    if components_present == 3:
        return ValidationResult(
            check_name="Executive Summary",
            passed=True,
            message="Executive summary contains all key components",
            severity="info"
        )
    elif components_present >= 2:
        missing = []
        if not has_findings:
            missing.append("key findings")
        if not has_recommendations:
            missing.append("recommendations")
        if not has_uncertainty:
            missing.append("uncertainties/caveats")
        return ValidationResult(
            check_name="Executive Summary",
            passed=True,
            message=f"Executive summary missing: {', '.join(missing)}",
            severity="warning",
            details=missing
        )
    else:
        return ValidationResult(
            check_name="Executive Summary",
            passed=False,
            message="Executive summary incomplete",
            severity="error",
            details=["Missing key findings and/or recommendations"]
        )


def check_actionable_recommendations(report_content: str) -> ValidationResult:
    """Check that recommendations are actionable."""
    # Find recommendations section
    rec_match = re.search(
        r'##?\s*Recommend(?:ations|ed)?\s*(.*?)(?=##|\Z)',
        report_content,
        re.IGNORECASE | re.DOTALL
    )

    if not rec_match:
        return ValidationResult(
            check_name="Actionable Recommendations",
            passed=False,
            message="No recommendations section found",
            severity="warning"
        )

    recommendations = rec_match.group(1)

    # Look for actionable language
    action_patterns = [
        r'\d+\.\s+\w+',  # Numbered list
        r'[-•]\s+\w+',   # Bullet list
        r'should\s+\w+',
        r'recommend\s+\w+',
        r'consider\s+\w+'
    ]

    action_count = sum(len(re.findall(p, recommendations)) for p in action_patterns)

    if action_count >= 3:
        return ValidationResult(
            check_name="Actionable Recommendations",
            passed=True,
            message=f"{action_count} actionable items found in recommendations",
            severity="info"
        )
    elif action_count >= 1:
        return ValidationResult(
            check_name="Actionable Recommendations",
            passed=True,
            message=f"Only {action_count} actionable item(s) found",
            severity="warning"
        )
    else:
        return ValidationResult(
            check_name="Actionable Recommendations",
            passed=False,
            message="Recommendations section lacks actionable items",
            severity="warning"
        )


def validate_report(
    report_content: str,
    sources: List[dict],
    findings: dict,
    gaps: dict
) -> ValidationSummary:
    """Run all validation checks on the report."""
    summary = ValidationSummary()

    checks = [
        check_source_attribution(report_content, sources),
        check_orphaned_claims(report_content, findings),
        check_conflict_handling(report_content, findings),
        check_confidence_scores(report_content, findings),
        check_gap_acknowledgment(report_content, gaps),
        check_executive_summary(report_content, findings),
        check_actionable_recommendations(report_content)
    ]

    for result in checks:
        summary.results.append(result)
        summary.total_checks += 1
        if result.passed:
            summary.passed += 1
        if result.severity == "warning":
            summary.warnings += 1
        elif result.severity == "error":
            summary.errors += 1

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Validate consolidated research reports"
    )
    parser.add_argument("--report", required=True,
                        help="Report file to validate (markdown)")
    parser.add_argument("--sources", help="Sources JSON file")
    parser.add_argument("--findings", help="Findings JSON file")
    parser.add_argument("--gaps", help="Gaps JSON file")
    parser.add_argument("--output-format", default="text",
                        choices=["text", "json"], help="Output format")

    args = parser.parse_args()

    # Load report
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Error: Report file not found: {args.report}", file=sys.stderr)
        sys.exit(1)

    with open(report_path, "r", encoding="utf-8") as f:
        report_content = f.read()

    # Load sources
    sources = []
    if args.sources:
        sources_path = Path(args.sources)
        if sources_path.exists():
            with open(sources_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sources = data if isinstance(data, list) else data.get("sources", [])

    # Load findings
    findings = {}
    if args.findings:
        findings_path = Path(args.findings)
        if findings_path.exists():
            with open(findings_path, "r", encoding="utf-8") as f:
                findings = json.load(f)

    # Load gaps
    gaps = {}
    if args.gaps:
        gaps_path = Path(args.gaps)
        if gaps_path.exists():
            with open(gaps_path, "r", encoding="utf-8") as f:
                gaps = json.load(f)

    # Run validation
    summary = validate_report(report_content, sources, findings, gaps)

    if args.output_format == "json":
        output = {
            "report_file": str(report_path),
            "validation_score": summary.score,
            "total_checks": summary.total_checks,
            "passed": summary.passed,
            "warnings": summary.warnings,
            "errors": summary.errors,
            "results": [
                {
                    "check": r.check_name,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity,
                    "details": r.details
                }
                for r in summary.results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print("=" * 70)
        print("REPORT VALIDATION RESULTS")
        print("=" * 70)
        print(f"\nReport: {report_path.name}")
        print(f"Validation Score: {summary.score:.0%}")
        print(f"Checks Passed: {summary.passed}/{summary.total_checks}")
        print(f"Warnings: {summary.warnings}")
        print(f"Errors: {summary.errors}")

        print("\n--- VALIDATION DETAILS ---\n")

        for result in summary.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            severity_icon = {"info": "ℹ", "warning": "⚠", "error": "✗"}.get(result.severity, "?")

            print(f"{status} [{severity_icon}] {result.check_name}")
            print(f"      {result.message}")
            if result.details:
                for detail in result.details[:3]:
                    print(f"        - {detail}")
                if len(result.details) > 3:
                    print(f"        ... and {len(result.details) - 3} more")
            print()

        # Summary recommendation
        print("=" * 70)
        if summary.score >= 0.9:
            print("✓ Report passes validation with high quality")
        elif summary.score >= 0.7:
            print("⚠ Report passes validation with some concerns to address")
        else:
            print("✗ Report needs revision before finalization")


if __name__ == "__main__":
    main()
