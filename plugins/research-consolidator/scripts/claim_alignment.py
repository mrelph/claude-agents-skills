#!/usr/bin/env python3
"""
Claim Alignment Tool for Research Consolidator

Maps similar claims across multiple sources to identify areas of
agreement, partial agreement, and conflict.

Usage:
    python claim_alignment.py --sources parsed/*.json --output alignment_matrix.json
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(text: str) -> Set[str]:
    """Extract keywords from text for matching."""
    # Common stopwords to ignore
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'that', 'this', 'these',
        'those', 'it', 'its', 'they', 'their', 'them', 'we', 'our', 'you',
        'your', 'which', 'what', 'who', 'whom', 'when', 'where', 'why', 'how'
    }

    normalized = normalize_text(text)
    words = normalized.split()
    keywords = {w for w in words if len(w) > 2 and w not in stopwords}
    return keywords


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using keyword overlap."""
    keywords1 = extract_keywords(text1)
    keywords2 = extract_keywords(text2)

    if not keywords1 or not keywords2:
        return 0.0

    intersection = keywords1 & keywords2
    union = keywords1 | keywords2

    return len(intersection) / len(union) if union else 0.0


def cluster_claims(all_claims: List[dict], similarity_threshold: float = 0.3) -> List[dict]:
    """
    Cluster similar claims together.

    Returns list of claim groups with their sources.
    """
    clusters = []
    assigned = set()

    for i, claim1 in enumerate(all_claims):
        if i in assigned:
            continue

        cluster = {
            "theme": "",
            "claims": [claim1],
            "sources": {claim1["source_id"]},
            "categories": {claim1.get("category", "general")}
        }

        for j, claim2 in enumerate(all_claims[i + 1:], start=i + 1):
            if j in assigned:
                continue

            similarity = calculate_similarity(claim1["text"], claim2["text"])
            if similarity >= similarity_threshold:
                cluster["claims"].append(claim2)
                cluster["sources"].add(claim2["source_id"])
                cluster["categories"].add(claim2.get("category", "general"))
                assigned.add(j)

        # Generate theme from most common category
        cluster["theme"] = max(cluster["categories"], key=lambda c:
            sum(1 for cl in cluster["claims"] if cl.get("category") == c))

        # Convert sets to lists for JSON serialization
        cluster["sources"] = list(cluster["sources"])
        cluster["categories"] = list(cluster["categories"])

        assigned.add(i)
        clusters.append(cluster)

    return clusters


def determine_agreement(cluster: dict, total_sources: int) -> str:
    """Determine level of agreement for a claim cluster."""
    source_count = len(cluster["sources"])
    source_ratio = source_count / total_sources if total_sources > 0 else 0

    if source_ratio >= 0.75:
        return "HIGH"
    elif source_ratio >= 0.5:
        return "MODERATE"
    elif source_count >= 2:
        return "PARTIAL"
    else:
        return "SINGLE_SOURCE"


def detect_conflicts(clusters: List[dict]) -> List[dict]:
    """
    Detect potential conflicts between claim clusters.

    Looks for clusters with similar themes but potentially contradictory content.
    """
    conflicts = []
    conflict_counter = 1

    # Keywords that might indicate opposing views
    negative_indicators = {'not', 'no', 'never', 'decline', 'decrease', 'fall', 'drop', 'fail', 'unlikely'}
    positive_indicators = {'yes', 'increase', 'growth', 'rise', 'success', 'likely', 'improve'}

    for i, cluster1 in enumerate(clusters):
        for cluster2 in clusters[i + 1:]:
            # Check if themes are similar
            if cluster1["theme"] != cluster2["theme"]:
                continue

            # Check if different sources
            sources1 = set(cluster1["sources"])
            sources2 = set(cluster2["sources"])
            if sources1 == sources2:
                continue

            # Check for potential contradiction
            text1 = " ".join(c["text"].lower() for c in cluster1["claims"])
            text2 = " ".join(c["text"].lower() for c in cluster2["claims"])

            words1 = set(text1.split())
            words2 = set(text2.split())

            # Check if one has negative indicators and other has positive
            has_negative1 = bool(words1 & negative_indicators)
            has_positive1 = bool(words1 & positive_indicators)
            has_negative2 = bool(words2 & negative_indicators)
            has_positive2 = bool(words2 & positive_indicators)

            if (has_negative1 and has_positive2) or (has_positive1 and has_negative2):
                conflicts.append({
                    "conflict_id": f"CNF-{conflict_counter:03d}",
                    "type": "opposing_view",
                    "severity": "medium",
                    "theme": cluster1["theme"],
                    "cluster_1_sources": cluster1["sources"],
                    "cluster_1_sample": cluster1["claims"][0]["text"][:100],
                    "cluster_2_sources": cluster2["sources"],
                    "cluster_2_sample": cluster2["claims"][0]["text"][:100],
                    "description": f"Potential opposing views on {cluster1['theme']}"
                })
                conflict_counter += 1

    return conflicts


def build_alignment_matrix(clusters: List[dict], sources: List[str]) -> dict:
    """Build alignment matrix showing claim coverage by source."""
    matrix = {
        "sources": sources,
        "themes": [],
        "alignment": []
    }

    for cluster in clusters:
        theme_data = {
            "theme": cluster["theme"],
            "agreement": determine_agreement(cluster, len(sources)),
            "source_coverage": {}
        }

        for source in sources:
            if source in cluster["sources"]:
                # Find the claim from this source
                claim = next((c for c in cluster["claims"] if c["source_id"] == source), None)
                theme_data["source_coverage"][source] = {
                    "has_claim": True,
                    "claim_id": claim["claim_id"] if claim else None,
                    "summary": claim["text"][:80] + "..." if claim else None
                }
            else:
                theme_data["source_coverage"][source] = {
                    "has_claim": False,
                    "claim_id": None,
                    "summary": None
                }

        matrix["themes"].append(cluster["theme"])
        matrix["alignment"].append(theme_data)

    return matrix


def main():
    parser = argparse.ArgumentParser(
        description="Align claims across multiple parsed sources"
    )
    parser.add_argument("--sources", nargs="+", required=True,
                        help="Parsed source JSON files")
    parser.add_argument("--output", default="alignment_matrix.json",
                        help="Output file path")
    parser.add_argument("--similarity-threshold", type=float, default=0.3,
                        help="Similarity threshold for clustering (0.0-1.0)")
    parser.add_argument("--output-format", default="json",
                        choices=["json", "text"], help="Output format")

    args = parser.parse_args()

    # Load all parsed sources
    all_claims = []
    source_ids = []

    for source_file in args.sources:
        path = Path(source_file)
        if not path.exists():
            print(f"Warning: Source file not found: {source_file}", file=sys.stderr)
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        source_ids.append(data["source_id"])
        all_claims.extend(data["extracted"]["claims"])

    if not all_claims:
        print("Error: No claims found in source files", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(all_claims)} claims from {len(source_ids)} sources")

    # Cluster similar claims
    clusters = cluster_claims(all_claims, args.similarity_threshold)
    print(f"Identified {len(clusters)} claim clusters/themes")

    # Detect conflicts
    conflicts = detect_conflicts(clusters)
    print(f"Detected {len(conflicts)} potential conflicts")

    # Build alignment matrix
    matrix = build_alignment_matrix(clusters, source_ids)

    # Prepare output
    output = {
        "metadata": {
            "sources_analyzed": source_ids,
            "total_claims": len(all_claims),
            "total_clusters": len(clusters),
            "total_conflicts": len(conflicts),
            "similarity_threshold": args.similarity_threshold
        },
        "alignment_matrix": matrix,
        "clusters": clusters,
        "conflicts": conflicts,
        "summary": {
            "high_agreement": sum(1 for c in clusters if determine_agreement(c, len(source_ids)) == "HIGH"),
            "moderate_agreement": sum(1 for c in clusters if determine_agreement(c, len(source_ids)) == "MODERATE"),
            "partial_agreement": sum(1 for c in clusters if determine_agreement(c, len(source_ids)) == "PARTIAL"),
            "single_source": sum(1 for c in clusters if determine_agreement(c, len(source_ids)) == "SINGLE_SOURCE")
        }
    }

    if args.output_format == "json":
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"\nAlignment matrix written to: {args.output}")
    else:
        print("\n" + "=" * 70)
        print("CLAIM ALIGNMENT MATRIX")
        print("=" * 70)

        print(f"\nSources: {', '.join(source_ids)}")
        print(f"Total Claims: {len(all_claims)}")
        print(f"Claim Clusters: {len(clusters)}")

        print("\n--- AGREEMENT SUMMARY ---")
        print(f"  High Agreement: {output['summary']['high_agreement']}")
        print(f"  Moderate Agreement: {output['summary']['moderate_agreement']}")
        print(f"  Partial Agreement: {output['summary']['partial_agreement']}")
        print(f"  Single Source: {output['summary']['single_source']}")

        print("\n--- ALIGNMENT BY THEME ---")
        for item in matrix["alignment"]:
            print(f"\n  Theme: {item['theme'].upper()}")
            print(f"  Agreement: {item['agreement']}")
            for source, data in item["source_coverage"].items():
                status = "✓" if data["has_claim"] else "✗"
                print(f"    {source}: {status}", end="")
                if data["summary"]:
                    print(f" - {data['summary'][:50]}...")
                else:
                    print(" (no claim)")

        if conflicts:
            print("\n--- POTENTIAL CONFLICTS ---")
            for conflict in conflicts:
                print(f"\n  [{conflict['conflict_id']}] {conflict['theme']}")
                print(f"    Type: {conflict['type']} | Severity: {conflict['severity']}")
                print(f"    Sources A ({', '.join(conflict['cluster_1_sources'])}): {conflict['cluster_1_sample'][:50]}...")
                print(f"    Sources B ({', '.join(conflict['cluster_2_sources'])}): {conflict['cluster_2_sample'][:50]}...")


if __name__ == "__main__":
    main()
