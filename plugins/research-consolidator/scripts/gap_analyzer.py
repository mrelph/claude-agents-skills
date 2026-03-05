#!/usr/bin/env python3
"""
Gap Analyzer for Research Consolidator

Identifies gaps in research coverage across sources including:
- Topics not covered by any source
- Topics covered by only one source
- Areas lacking depth
- Temporal gaps (outdated information)
- Missing stakeholder perspectives

Usage:
    python gap_analyzer.py --sources parsed/*.json --output gaps.json
    python gap_analyzer.py --sources parsed/*.json --topic-outline topics.json --output gaps.json
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional


# Standard research topic areas to check coverage
DEFAULT_TOPIC_AREAS = {
    "market_analysis": {
        "name": "Market Analysis",
        "subtopics": ["market_size", "growth_trends", "market_segments", "geographic_distribution"],
        "keywords": ["market", "growth", "size", "segment", "industry", "sector", "demand"]
    },
    "competitive_landscape": {
        "name": "Competitive Landscape",
        "subtopics": ["key_competitors", "market_share", "competitive_advantages", "barriers_to_entry"],
        "keywords": ["competitor", "competition", "rival", "market share", "advantage", "barrier"]
    },
    "technology": {
        "name": "Technology & Innovation",
        "subtopics": ["current_tech", "emerging_tech", "tech_trends", "r&d"],
        "keywords": ["technology", "tech", "innovation", "software", "hardware", "ai", "digital"]
    },
    "financial": {
        "name": "Financial Analysis",
        "subtopics": ["revenue", "costs", "profitability", "investment", "pricing"],
        "keywords": ["revenue", "cost", "profit", "price", "investment", "financial", "budget"]
    },
    "regulatory": {
        "name": "Regulatory Environment",
        "subtopics": ["current_regulations", "pending_legislation", "compliance_requirements", "regulatory_risks"],
        "keywords": ["regulation", "compliance", "law", "policy", "government", "legal", "requirement"]
    },
    "risks": {
        "name": "Risk Assessment",
        "subtopics": ["market_risks", "operational_risks", "strategic_risks", "external_risks"],
        "keywords": ["risk", "threat", "challenge", "vulnerability", "concern", "issue"]
    },
    "opportunities": {
        "name": "Opportunities",
        "subtopics": ["growth_opportunities", "market_gaps", "emerging_markets", "innovation_opportunities"],
        "keywords": ["opportunity", "potential", "growth", "expansion", "emerging", "untapped"]
    },
    "stakeholders": {
        "name": "Stakeholder Analysis",
        "subtopics": ["customers", "suppliers", "partners", "investors"],
        "keywords": ["customer", "client", "supplier", "partner", "investor", "stakeholder"]
    }
}


def load_topic_outline(filepath: Optional[str]) -> dict:
    """Load custom topic outline or use defaults."""
    if filepath:
        path = Path(filepath)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    return DEFAULT_TOPIC_AREAS


def check_topic_coverage(claims: List[dict], topic: dict) -> dict:
    """Check how well claims cover a topic area."""
    keywords = set(topic["keywords"])
    matching_claims = []

    for claim in claims:
        claim_text = claim["text"].lower()
        if any(kw in claim_text for kw in keywords):
            matching_claims.append(claim)

    coverage = {
        "topic_name": topic["name"],
        "claims_count": len(matching_claims),
        "sources_covering": list(set(c["source_id"] for c in matching_claims)),
        "subtopics_addressed": [],
        "claims": matching_claims
    }

    # Check subtopic coverage
    for subtopic in topic.get("subtopics", []):
        subtopic_keywords = subtopic.replace("_", " ").split()
        if any(any(kw in c["text"].lower() for kw in subtopic_keywords) for c in matching_claims):
            coverage["subtopics_addressed"].append(subtopic)

    return coverage


def identify_gaps(
    sources_data: List[dict],
    topic_outline: dict,
    min_sources_for_coverage: int = 2
) -> dict:
    """Identify all types of gaps in research coverage."""

    # Collect all claims across sources
    all_claims = []
    source_ids = []
    source_dates = {}

    for source in sources_data:
        source_ids.append(source["source_id"])
        all_claims.extend(source["extracted"]["claims"])

        # Track source dates for temporal analysis
        if "date_parsed" in source:
            try:
                source_dates[source["source_id"]] = datetime.fromisoformat(
                    source["date_parsed"].replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                pass

    total_sources = len(source_ids)

    gaps = {
        "topic_gaps": [],      # Topics not covered at all
        "source_gaps": [],     # Topics covered by only one source
        "depth_gaps": [],      # Topics mentioned but not explored
        "temporal_gaps": [],   # Information that may be outdated
        "perspective_gaps": [] # Missing stakeholder viewpoints
    }

    # Analyze each topic area
    for topic_id, topic in topic_outline.items():
        coverage = check_topic_coverage(all_claims, topic)

        # Topic gap: No coverage at all
        if coverage["claims_count"] == 0:
            gaps["topic_gaps"].append({
                "gap_id": f"GAP-T-{len(gaps['topic_gaps']) + 1:03d}",
                "gap_type": "not_covered",
                "topic": topic["name"],
                "topic_id": topic_id,
                "impact": "high",
                "description": f"No sources address {topic['name']}",
                "recommendation": f"Research needed on {topic['name']} including: {', '.join(topic.get('subtopics', [])[:3])}"
            })

        # Source gap: Only one source covers this
        elif len(coverage["sources_covering"]) < min_sources_for_coverage:
            gaps["source_gaps"].append({
                "gap_id": f"GAP-S-{len(gaps['source_gaps']) + 1:03d}",
                "gap_type": "single_source",
                "topic": topic["name"],
                "topic_id": topic_id,
                "sources_covering": coverage["sources_covering"],
                "impact": "medium",
                "description": f"Only {len(coverage['sources_covering'])} source(s) cover {topic['name']}",
                "recommendation": f"Seek additional sources to validate findings on {topic['name']}"
            })

        # Depth gap: Topic covered but subtopics missing
        missing_subtopics = set(topic.get("subtopics", [])) - set(coverage["subtopics_addressed"])
        if missing_subtopics and len(missing_subtopics) > len(topic.get("subtopics", [])) / 2:
            gaps["depth_gaps"].append({
                "gap_id": f"GAP-D-{len(gaps['depth_gaps']) + 1:03d}",
                "gap_type": "lacking_depth",
                "topic": topic["name"],
                "topic_id": topic_id,
                "subtopics_addressed": coverage["subtopics_addressed"],
                "subtopics_missing": list(missing_subtopics),
                "impact": "medium",
                "description": f"{topic['name']} lacks depth on: {', '.join(list(missing_subtopics)[:3])}",
                "recommendation": f"Deepen research on {', '.join(list(missing_subtopics)[:3])}"
            })

    # Temporal gaps: Check for potentially outdated sources
    if source_dates:
        six_months_ago = datetime.now() - timedelta(days=180)
        one_year_ago = datetime.now() - timedelta(days=365)

        for source_id, date in source_dates.items():
            if date < one_year_ago:
                gaps["temporal_gaps"].append({
                    "gap_id": f"GAP-TM-{len(gaps['temporal_gaps']) + 1:03d}",
                    "gap_type": "outdated",
                    "source_id": source_id,
                    "source_date": date.isoformat(),
                    "age_days": (datetime.now() - date).days,
                    "impact": "high",
                    "description": f"Source {source_id} is over 1 year old",
                    "recommendation": "Verify currency of information; seek updated sources"
                })
            elif date < six_months_ago:
                gaps["temporal_gaps"].append({
                    "gap_id": f"GAP-TM-{len(gaps['temporal_gaps']) + 1:03d}",
                    "gap_type": "potentially_outdated",
                    "source_id": source_id,
                    "source_date": date.isoformat(),
                    "age_days": (datetime.now() - date).days,
                    "impact": "medium",
                    "description": f"Source {source_id} is over 6 months old",
                    "recommendation": "Consider verifying time-sensitive information"
                })

    # Perspective gaps: Check for missing stakeholder viewpoints
    stakeholder_keywords = {
        "customer": ["customer", "client", "user", "consumer", "buyer"],
        "supplier": ["supplier", "vendor", "provider"],
        "investor": ["investor", "shareholder", "stakeholder"],
        "employee": ["employee", "worker", "staff", "team"],
        "regulator": ["regulator", "government", "authority"],
        "competitor": ["competitor", "rival", "peer"]
    }

    all_text = " ".join(c["text"].lower() for c in all_claims)
    for stakeholder, keywords in stakeholder_keywords.items():
        if not any(kw in all_text for kw in keywords):
            gaps["perspective_gaps"].append({
                "gap_id": f"GAP-P-{len(gaps['perspective_gaps']) + 1:03d}",
                "gap_type": "missing_perspective",
                "stakeholder": stakeholder,
                "impact": "low",
                "description": f"No {stakeholder} perspective represented",
                "recommendation": f"Consider adding research on {stakeholder} viewpoint"
            })

    return gaps


def calculate_coverage_score(gaps: dict, topic_outline: dict) -> dict:
    """Calculate overall coverage score and statistics."""
    total_topics = len(topic_outline)
    topics_not_covered = len(gaps["topic_gaps"])
    topics_single_source = len(gaps["source_gaps"])

    coverage_score = max(0, (total_topics - topics_not_covered - (topics_single_source * 0.5)) / total_topics)

    return {
        "overall_coverage_score": round(coverage_score, 2),
        "total_topics_expected": total_topics,
        "topics_fully_covered": total_topics - topics_not_covered - topics_single_source,
        "topics_partially_covered": topics_single_source,
        "topics_not_covered": topics_not_covered,
        "total_gaps_identified": sum(len(v) for v in gaps.values()),
        "gaps_by_type": {
            "topic_gaps": len(gaps["topic_gaps"]),
            "source_gaps": len(gaps["source_gaps"]),
            "depth_gaps": len(gaps["depth_gaps"]),
            "temporal_gaps": len(gaps["temporal_gaps"]),
            "perspective_gaps": len(gaps["perspective_gaps"])
        },
        "high_impact_gaps": sum(1 for gap_list in gaps.values() for gap in gap_list if gap.get("impact") == "high"),
        "medium_impact_gaps": sum(1 for gap_list in gaps.values() for gap in gap_list if gap.get("impact") == "medium"),
        "low_impact_gaps": sum(1 for gap_list in gaps.values() for gap in gap_list if gap.get("impact") == "low")
    }


def prioritize_gaps(gaps: dict) -> List[dict]:
    """Return gaps sorted by priority for action."""
    all_gaps = []
    for gap_type, gap_list in gaps.items():
        for gap in gap_list:
            gap["_gap_type_category"] = gap_type
            all_gaps.append(gap)

    # Sort by impact (high > medium > low) then by type
    impact_order = {"high": 0, "medium": 1, "low": 2}
    type_order = {"topic_gaps": 0, "source_gaps": 1, "depth_gaps": 2, "temporal_gaps": 3, "perspective_gaps": 4}

    all_gaps.sort(key=lambda g: (
        impact_order.get(g.get("impact"), 3),
        type_order.get(g.get("_gap_type_category"), 5)
    ))

    return all_gaps


def main():
    parser = argparse.ArgumentParser(
        description="Identify gaps in research coverage across sources"
    )
    parser.add_argument("--sources", nargs="+", required=True,
                        help="Parsed source JSON files")
    parser.add_argument("--topic-outline", help="Custom topic outline JSON file")
    parser.add_argument("--output", default="gaps.json",
                        help="Output file path")
    parser.add_argument("--min-sources", type=int, default=2,
                        help="Minimum sources for adequate coverage")
    parser.add_argument("--output-format", default="json",
                        choices=["json", "text"], help="Output format")

    args = parser.parse_args()

    # Load parsed sources
    sources_data = []
    for source_file in args.sources:
        path = Path(source_file)
        if not path.exists():
            print(f"Warning: Source file not found: {source_file}", file=sys.stderr)
            continue

        with open(path, "r", encoding="utf-8") as f:
            sources_data.append(json.load(f))

    if not sources_data:
        print("Error: No source files loaded", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(sources_data)} source files")

    # Load topic outline
    topic_outline = load_topic_outline(args.topic_outline)
    print(f"Analyzing coverage across {len(topic_outline)} topic areas")

    # Identify gaps
    gaps = identify_gaps(sources_data, topic_outline, args.min_sources)

    # Calculate coverage statistics
    coverage_stats = calculate_coverage_score(gaps, topic_outline)

    # Prioritize gaps
    prioritized_gaps = prioritize_gaps(gaps)

    # Prepare output
    output = {
        "metadata": {
            "sources_analyzed": [s["source_id"] for s in sources_data],
            "topic_areas_checked": len(topic_outline),
            "min_sources_for_coverage": args.min_sources,
            "analysis_date": datetime.now().isoformat()
        },
        "coverage_statistics": coverage_stats,
        "gaps": gaps,
        "prioritized_action_items": prioritized_gaps[:10]  # Top 10 priority gaps
    }

    if args.output_format == "json":
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"\nGap analysis written to: {args.output}")
    else:
        print("\n" + "=" * 70)
        print("RESEARCH GAP ANALYSIS")
        print("=" * 70)

        print(f"\n--- COVERAGE SUMMARY ---")
        print(f"Overall Coverage Score: {coverage_stats['overall_coverage_score']:.0%}")
        print(f"Topics Fully Covered: {coverage_stats['topics_fully_covered']}/{coverage_stats['total_topics_expected']}")
        print(f"Topics Partially Covered: {coverage_stats['topics_partially_covered']}")
        print(f"Topics Not Covered: {coverage_stats['topics_not_covered']}")
        print(f"Total Gaps Identified: {coverage_stats['total_gaps_identified']}")

        print(f"\n--- GAPS BY TYPE ---")
        for gap_type, count in coverage_stats["gaps_by_type"].items():
            print(f"  {gap_type.replace('_', ' ').title()}: {count}")

        print(f"\n--- HIGH PRIORITY GAPS ---")
        high_priority = [g for g in prioritized_gaps if g.get("impact") == "high"]
        if high_priority:
            for gap in high_priority[:5]:
                print(f"\n  [{gap['gap_id']}] {gap['gap_type'].upper()}")
                print(f"    Topic: {gap.get('topic', gap.get('source_id', 'N/A'))}")
                print(f"    {gap['description']}")
                print(f"    Recommendation: {gap['recommendation']}")
        else:
            print("  No high priority gaps identified")

        print(f"\n--- ALL GAPS BY IMPACT ---")
        print(f"  High Impact: {coverage_stats['high_impact_gaps']}")
        print(f"  Medium Impact: {coverage_stats['medium_impact_gaps']}")
        print(f"  Low Impact: {coverage_stats['low_impact_gaps']}")


if __name__ == "__main__":
    main()
