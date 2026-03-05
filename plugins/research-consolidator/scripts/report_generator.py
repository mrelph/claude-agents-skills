#!/usr/bin/env python3
"""
Report Generator for Research Consolidator

Generates consolidated research reports from analyzed data including
parsed sources, alignment matrices, and gap analyses.

Usage:
    python report_generator.py \
        --findings consolidated_findings.json \
        --conflicts conflicts.json \
        --gaps gaps.json \
        --template executive \
        --output final_report.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def confidence_label(score: float) -> str:
    """Convert confidence score to label."""
    if score >= 0.85:
        return "VERY HIGH"
    elif score >= 0.70:
        return "HIGH"
    elif score >= 0.55:
        return "MODERATE"
    elif score >= 0.40:
        return "LOW"
    else:
        return "VERY LOW"


def confidence_indicator(level: str) -> str:
    """Return indicator emoji for confidence level."""
    indicators = {
        "VERY HIGH": "⬆️⬆️",
        "HIGH": "⬆️",
        "MODERATE": "➡️",
        "LOW": "⬇️",
        "VERY LOW": "⬇️⬇️"
    }
    return indicators.get(level.upper(), "➡️")


def generate_executive_report(
    findings: dict,
    alignment: dict,
    gaps: dict,
    metadata: dict
) -> str:
    """Generate executive report format."""

    report = []

    # Header
    report.append(f"# {metadata.get('title', 'Research Topic')} - Consolidated Research Report\n")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    report.append(f"**Sources Analyzed:** {len(metadata.get('sources', []))}")
    report.append(f"**Overall Confidence:** {metadata.get('overall_confidence', 'N/A')}\n")
    report.append("---\n")

    # Executive Summary
    report.append("## Executive Summary\n")
    report.append("### Key Findings\n")

    # Top findings
    top_findings = sorted(
        findings.get("consolidated_findings", []),
        key=lambda f: f.get("confidence_score", 0),
        reverse=True
    )[:5]

    for i, finding in enumerate(top_findings, 1):
        conf_level = confidence_label(finding.get("confidence_score", 0.5))
        report.append(f"{i}. **{finding.get('title', 'Finding ' + str(i))}** (Confidence: {conf_level})")
        report.append(f"   {finding.get('statement', finding.get('consolidated_statement', 'N/A'))[:150]}\n")

    # Critical Insights
    report.append("### Critical Insights\n")
    insights = findings.get("insights", [])[:3]
    if insights:
        for insight in insights:
            report.append(f"- {insight}")
    else:
        report.append("- See detailed findings below")
    report.append("")

    # Areas of Uncertainty
    report.append("### Areas of Uncertainty\n")
    conflicts = findings.get("conflicts", [])[:3]
    if conflicts:
        for conflict in conflicts:
            report.append(f"- {conflict.get('description', 'Unresolved conflict')}")
    else:
        report.append("- No major conflicts identified")
    report.append("")

    # Recommended Actions
    report.append("### Recommended Actions\n")
    recommendations = findings.get("recommendations", [])[:3]
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            if isinstance(rec, dict):
                report.append(f"{i}. {rec.get('action', rec.get('text', 'N/A'))}")
            else:
                report.append(f"{i}. {rec}")
    else:
        report.append("1. Review detailed findings below")
        report.append("2. Address identified gaps")
        report.append("3. Resolve any conflicts noted")
    report.append("")

    report.append("---\n")

    # Methodology
    report.append("## Methodology\n")
    report.append("### Sources Analyzed\n")
    report.append("| ID | Source Type | Name | Date | Credibility |")
    report.append("|----|-------------|------|------|-------------|")

    for source in metadata.get("sources", []):
        if isinstance(source, dict):
            report.append(f"| {source.get('id', 'N/A')} | {source.get('type', 'N/A')} | {source.get('name', 'N/A')} | {source.get('date', 'N/A')} | {source.get('credibility', 'N/A')} |")
        else:
            report.append(f"| {source} | - | - | - | - |")
    report.append("")

    report.append("### Consolidation Approach\n")
    report.append("Sources were analyzed using systematic extraction of claims, evidence, conclusions, and recommendations. ")
    report.append("Claims were aligned across sources to identify agreement, conflicts, and gaps. ")
    report.append("Confidence scores reflect source agreement, evidence quality, source authority, and recency.\n")

    report.append("### Confidence Scoring\n")
    report.append("Confidence levels reflect:")
    report.append("- Source agreement (40%)")
    report.append("- Evidence quality (30%)")
    report.append("- Source authority (20%)")
    report.append("- Recency (10%)\n")

    report.append("---\n")

    # Detailed Findings
    report.append("## Detailed Findings\n")

    for i, finding in enumerate(findings.get("consolidated_findings", []), 1):
        conf_score = finding.get("confidence_score", 0.5)
        conf_level = confidence_label(conf_score)

        report.append(f"### Finding {i}: {finding.get('title', 'Untitled')}\n")
        report.append(f"**Confidence Level:** {conf_level} ({conf_score:.2f})\n")
        report.append("**Consolidated Position:**")
        report.append(f"{finding.get('statement', finding.get('consolidated_statement', 'N/A'))}\n")

        # Source perspectives
        if finding.get("source_perspectives"):
            report.append("**Source Perspectives:**\n")
            report.append("| Source | Position | Evidence Provided |")
            report.append("|--------|----------|-------------------|")
            for perspective in finding["source_perspectives"]:
                report.append(f"| {perspective.get('source', 'N/A')} | {perspective.get('position', 'N/A')[:50]} | {perspective.get('evidence', 'N/A')[:50]} |")
            report.append("")

        # Caveats
        if finding.get("caveats"):
            report.append("**Caveats:**")
            for caveat in finding["caveats"]:
                report.append(f"- {caveat}")
            report.append("")

        report.append("---\n")

    # Areas of Conflict
    report.append("## Areas of Conflict\n")

    conflicts = findings.get("conflicts", [])
    if conflicts:
        for conflict in conflicts:
            report.append(f"### Conflict: {conflict.get('topic', 'Unnamed')}\n")
            report.append("**Nature of Disagreement:**")
            report.append(f"{conflict.get('description', 'N/A')}\n")

            report.append("**Position A:**")
            report.append(f"- Sources: {', '.join(conflict.get('sources_a', ['N/A']))}")
            report.append(f"- Claim: {conflict.get('position_a', 'N/A')}\n")

            report.append("**Position B:**")
            report.append(f"- Sources: {', '.join(conflict.get('sources_b', ['N/A']))}")
            report.append(f"- Claim: {conflict.get('position_b', 'N/A')}\n")

            report.append("**Resolution:**")
            report.append(f"{conflict.get('resolution', 'Unresolved - requires further investigation')}\n")
            report.append("---\n")
    else:
        report.append("No significant conflicts identified between sources.\n")
        report.append("---\n")

    # Research Gaps
    report.append("## Research Gaps\n")

    if gaps.get("gaps"):
        report.append("| Gap | Description | Impact | Recommendation |")
        report.append("|-----|-------------|--------|----------------|")

        all_gaps = []
        for gap_type, gap_list in gaps.get("gaps", {}).items():
            all_gaps.extend(gap_list)

        for gap in all_gaps[:10]:  # Top 10 gaps
            report.append(f"| {gap.get('topic', gap.get('source_id', 'N/A'))} | {gap.get('description', 'N/A')[:40]} | {gap.get('impact', 'N/A').upper()} | {gap.get('recommendation', 'N/A')[:40]} |")
        report.append("")
    else:
        report.append("No significant gaps identified.\n")

    report.append("---\n")

    # Recommendations
    report.append("## Recommendations\n")
    report.append("### Immediate Actions\n")

    recommendations = findings.get("recommendations", [])
    immediate = [r for r in recommendations if isinstance(r, dict) and r.get("priority") == "high"][:3]
    if immediate:
        for i, rec in enumerate(immediate, 1):
            report.append(f"{i}. **{rec.get('action', 'Action')}** - {rec.get('rationale', 'N/A')}")
    else:
        report.append("1. Review detailed findings with stakeholders")
        report.append("2. Prioritize addressing high-impact gaps")
    report.append("")

    report.append("### Further Research Needed\n")
    if gaps.get("gaps", {}).get("topic_gaps"):
        for i, gap in enumerate(gaps["gaps"]["topic_gaps"][:3], 1):
            report.append(f"{i}. {gap.get('topic', 'Topic')}: {gap.get('recommendation', 'Investigation needed')}")
    else:
        report.append("1. Monitor for updates to existing findings")
    report.append("")

    report.append("---\n")

    # Source Attribution
    report.append("## Source Attribution\n")
    report.append("| Source ID | Type | Name | Key Contributions |")
    report.append("|-----------|------|------|-------------------|")

    for source in metadata.get("sources", []):
        if isinstance(source, dict):
            report.append(f"| {source.get('id', 'N/A')} | {source.get('type', 'N/A')} | {source.get('name', 'N/A')} | {source.get('contributions', 'General analysis')[:50]} |")
    report.append("")

    report.append("---\n")
    report.append(f"*Report generated by Research Consolidator Skill*")
    report.append(f"*{datetime.now().strftime('%Y-%m-%d')} | v1.0.0*")

    return "\n".join(report)


def generate_comparison_matrix(
    alignment: dict,
    metadata: dict
) -> str:
    """Generate comparison matrix report format."""

    report = []

    report.append(f"# {metadata.get('title', 'Research Topic')} - Source Comparison Matrix\n")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    report.append(f"**Sources Compared:** {len(metadata.get('sources', []))}\n")
    report.append("---\n")

    # Quick Reference
    report.append("## Quick Reference\n")
    report.append("| Topic | Consensus? | Confidence |")
    report.append("|-------|------------|------------|")

    for item in alignment.get("alignment_matrix", {}).get("alignment", []):
        report.append(f"| {item.get('theme', 'N/A')} | {item.get('agreement', 'N/A')} | {item.get('confidence', 'N/A')} |")
    report.append("")

    report.append("---\n")

    # Detailed Comparison
    report.append("## Detailed Comparison\n")

    for item in alignment.get("alignment_matrix", {}).get("alignment", []):
        report.append(f"### Topic: {item.get('theme', 'Untitled')}\n")

        report.append("| Aspect | ", end="")
        sources = metadata.get("sources", [])
        for source in sources:
            source_id = source.get("id", source) if isinstance(source, dict) else source
            report.append(f"{source_id} | ")
        report.append("")

        report.append("|--------|", end="")
        for _ in sources:
            report.append("----------|")
        report.append("")

        report.append("| **Has Claim** | ", end="")
        for source in sources:
            source_id = source.get("id", source) if isinstance(source, dict) else source
            coverage = item.get("source_coverage", {}).get(source_id, {})
            status = "✓" if coverage.get("has_claim") else "✗"
            report.append(f"{status} | ")
        report.append("")

        report.append(f"\n**Synthesis:** {item.get('synthesis', 'See individual claims')}\n")
        report.append(f"**Agreement Level:** {item.get('agreement', 'N/A')}\n")
        report.append("---\n")

    report.append(f"*Comparison Matrix generated by Research Consolidator Skill*")

    return "\n".join(report)


def generate_summary(findings: dict, metadata: dict) -> str:
    """Generate brief findings summary."""

    report = []

    report.append(f"# {metadata.get('title', 'Research Topic')} - Findings Summary\n")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')} | **Sources:** {len(metadata.get('sources', []))} | **Overall Confidence:** {metadata.get('overall_confidence', 'N/A')}\n")
    report.append("---\n")

    report.append("## Top 5 Findings\n")

    top_findings = sorted(
        findings.get("consolidated_findings", []),
        key=lambda f: f.get("confidence_score", 0),
        reverse=True
    )[:5]

    for i, finding in enumerate(top_findings, 1):
        conf_score = finding.get("confidence_score", 0.5)
        conf_level = confidence_label(conf_score)
        indicator = confidence_indicator(conf_level)

        report.append(f"### {i}. {finding.get('title', 'Finding')} {indicator} {conf_level} CONFIDENCE\n")
        report.append(f"{finding.get('statement', 'N/A')[:200]}")
        sources = finding.get("supporting_sources", [])
        report.append(f"*Sources: {', '.join(sources) if sources else 'N/A'}*\n")

    report.append("---\n")

    # Conflicts
    report.append("## Conflicts Noted\n")
    report.append("| Topic | Conflict | Resolution |")
    report.append("|-------|----------|------------|")

    conflicts = findings.get("conflicts", [])[:5]
    for conflict in conflicts:
        report.append(f"| {conflict.get('topic', 'N/A')} | {conflict.get('description', 'N/A')[:30]} | {conflict.get('resolution', 'Unresolved')[:30]} |")

    if not conflicts:
        report.append("| None | - | - |")
    report.append("")

    report.append("---\n")

    # Recommended Next Steps
    report.append("## Recommended Next Steps\n")
    for i, rec in enumerate(findings.get("recommendations", [])[:3], 1):
        if isinstance(rec, dict):
            report.append(f"{i}. {rec.get('action', 'Action item')}")
        else:
            report.append(f"{i}. {rec}")
    report.append("")

    report.append("---\n")
    report.append(f"*Summary generated {datetime.now().strftime('%Y-%m-%d')}*")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Generate consolidated research reports"
    )
    parser.add_argument("--findings", required=True,
                        help="Consolidated findings JSON file")
    parser.add_argument("--alignment", help="Alignment matrix JSON file")
    parser.add_argument("--gaps", help="Gap analysis JSON file")
    parser.add_argument("--template", default="executive",
                        choices=["executive", "comparison", "summary"],
                        help="Report template to use")
    parser.add_argument("--title", default="Research Topic",
                        help="Report title")
    parser.add_argument("--output", default="report.md",
                        help="Output file path")

    args = parser.parse_args()

    # Load findings
    findings_path = Path(args.findings)
    if not findings_path.exists():
        print(f"Error: Findings file not found: {args.findings}", file=sys.stderr)
        sys.exit(1)

    with open(findings_path, "r", encoding="utf-8") as f:
        findings = json.load(f)

    # Load alignment if provided
    alignment = {}
    if args.alignment:
        alignment_path = Path(args.alignment)
        if alignment_path.exists():
            with open(alignment_path, "r", encoding="utf-8") as f:
                alignment = json.load(f)

    # Load gaps if provided
    gaps = {}
    if args.gaps:
        gaps_path = Path(args.gaps)
        if gaps_path.exists():
            with open(gaps_path, "r", encoding="utf-8") as f:
                gaps = json.load(f)

    # Build metadata
    metadata = {
        "title": args.title,
        "sources": findings.get("sources", findings.get("metadata", {}).get("sources", [])),
        "overall_confidence": findings.get("overall_confidence", findings.get("metadata", {}).get("overall_confidence", "N/A"))
    }

    # Generate report based on template
    if args.template == "executive":
        report = generate_executive_report(findings, alignment, gaps, metadata)
    elif args.template == "comparison":
        report = generate_comparison_matrix(alignment, metadata)
    elif args.template == "summary":
        report = generate_summary(findings, metadata)
    else:
        report = generate_executive_report(findings, alignment, gaps, metadata)

    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report generated: {args.output}")
    print(f"Template used: {args.template}")


if __name__ == "__main__":
    main()
