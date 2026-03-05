#!/usr/bin/env python3
"""
Source Parser for Research Consolidator

Parses research sources and extracts structured elements including
claims, evidence, conclusions, recommendations, and uncertainties.

Usage:
    python source_parser.py --input source.md --output parsed/
    python source_parser.py --input source.txt --source-id SRC-001 --source-type ai_model
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def generate_id(prefix: str, counter: int) -> str:
    """Generate a unique ID with prefix."""
    return f"{prefix}-{counter:03d}"


def extract_claims(text: str, source_id: str) -> list:
    """
    Extract claims from text.

    Looks for patterns indicating claims:
    - Sentences with strong assertions
    - Numbered lists
    - Bullet points with key findings
    - Sentences containing keywords like "shows", "indicates", "suggests"
    """
    claims = []
    claim_counter = 1

    # Patterns that indicate claims
    claim_patterns = [
        r'(?:research|data|evidence|analysis|study|report)\s+(?:shows?|indicates?|suggests?|demonstrates?|reveals?|confirms?)\s+(.+?)(?:\.|$)',
        r'(?:key finding|main finding|conclusion|result):\s*(.+?)(?:\.|$)',
        r'(?:we found|findings show|results indicate)\s+(.+?)(?:\.|$)',
    ]

    # Look for bullet points and numbered items
    list_pattern = r'(?:^|\n)\s*(?:[-•*]|\d+\.)\s+(.+?)(?=\n|$)'

    # Extract from patterns
    for pattern in claim_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            match = match.strip()
            if len(match) > 20:  # Filter out very short matches
                claims.append({
                    "claim_id": generate_id("CLM", claim_counter),
                    "source_id": source_id,
                    "text": match,
                    "category": categorize_claim(match),
                    "confidence_stated": extract_confidence_level(match),
                    "evidence_refs": []
                })
                claim_counter += 1

    # Extract from list items (often contain key claims)
    list_matches = re.findall(list_pattern, text, re.MULTILINE)
    for match in list_matches:
        match = match.strip()
        if len(match) > 30 and not any(c['text'] == match for c in claims):
            claims.append({
                "claim_id": generate_id("CLM", claim_counter),
                "source_id": source_id,
                "text": match,
                "category": categorize_claim(match),
                "confidence_stated": extract_confidence_level(match),
                "evidence_refs": []
            })
            claim_counter += 1

    return claims


def categorize_claim(text: str) -> str:
    """Categorize a claim based on its content."""
    text_lower = text.lower()

    categories = {
        "market_analysis": ["market", "growth", "revenue", "sales", "demand", "industry"],
        "risk_assessment": ["risk", "threat", "vulnerability", "danger", "concern"],
        "opportunity": ["opportunity", "potential", "advantage", "benefit"],
        "technology": ["technology", "tech", "software", "hardware", "ai", "machine learning"],
        "financial": ["cost", "price", "investment", "budget", "expense", "profit"],
        "competitive": ["competitor", "competition", "rival", "market share"],
        "regulatory": ["regulation", "compliance", "law", "policy", "government"],
        "operational": ["process", "operation", "efficiency", "workflow"],
        "strategic": ["strategy", "strategic", "plan", "roadmap", "vision"],
    }

    for category, keywords in categories.items():
        if any(kw in text_lower for kw in keywords):
            return category

    return "general"


def extract_confidence_level(text: str) -> str:
    """Extract confidence level from claim text."""
    text_lower = text.lower()

    high_confidence = ["clearly", "definitely", "certainly", "strongly", "significantly", "conclusively"]
    low_confidence = ["possibly", "might", "may", "could", "potentially", "uncertain"]

    if any(word in text_lower for word in high_confidence):
        return "high"
    elif any(word in text_lower for word in low_confidence):
        return "low"

    return "medium"


def extract_evidence(text: str, source_id: str) -> list:
    """
    Extract evidence items from text.

    Looks for:
    - Statistics and numbers
    - Citations and references
    - Quotes
    - Data mentions
    """
    evidence = []
    evidence_counter = 1

    # Pattern for statistics/numbers
    stat_pattern = r'(?:^|\s)(\d+(?:\.\d+)?%?\s+(?:of|percent|growth|increase|decrease|decline).+?)(?:\.|$)'

    # Pattern for citations
    citation_pattern = r'(?:according to|per|based on|from)\s+([^,\.]+(?:report|study|research|survey|analysis))'

    # Pattern for quotes
    quote_pattern = r'"([^"]+)"'

    # Extract statistics
    stat_matches = re.findall(stat_pattern, text, re.IGNORECASE | re.MULTILINE)
    for match in stat_matches:
        evidence.append({
            "evidence_id": generate_id("EVD", evidence_counter),
            "source_id": source_id,
            "text": match.strip(),
            "type": "data",
            "original_source": "extracted_statistic"
        })
        evidence_counter += 1

    # Extract citations
    citation_matches = re.findall(citation_pattern, text, re.IGNORECASE)
    for match in citation_matches:
        evidence.append({
            "evidence_id": generate_id("EVD", evidence_counter),
            "source_id": source_id,
            "text": f"Referenced: {match.strip()}",
            "type": "study",
            "original_source": match.strip()
        })
        evidence_counter += 1

    # Extract quotes
    quote_matches = re.findall(quote_pattern, text)
    for match in quote_matches:
        if len(match) > 20:
            evidence.append({
                "evidence_id": generate_id("EVD", evidence_counter),
                "source_id": source_id,
                "text": match.strip(),
                "type": "quote",
                "original_source": "inline_quote"
            })
            evidence_counter += 1

    return evidence


def extract_conclusions(text: str, source_id: str) -> list:
    """Extract conclusions from text."""
    conclusions = []
    conclusion_counter = 1

    # Patterns for conclusions
    patterns = [
        r'(?:in conclusion|to conclude|overall|in summary|to summarize)[,:]?\s*(.+?)(?:\.|$)',
        r'(?:we conclude|this suggests|this indicates|this demonstrates)\s+(.+?)(?:\.|$)',
        r'(?:the main takeaway|key takeaway|bottom line)[:\s]+(.+?)(?:\.|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            match = match.strip()
            if len(match) > 20:
                conclusions.append({
                    "conclusion_id": generate_id("CON", conclusion_counter),
                    "source_id": source_id,
                    "text": match
                })
                conclusion_counter += 1

    return conclusions


def extract_recommendations(text: str, source_id: str) -> list:
    """Extract recommendations from text."""
    recommendations = []
    rec_counter = 1

    # Patterns for recommendations
    patterns = [
        r'(?:recommend|suggest|advise|should consider)\s+(.+?)(?:\.|$)',
        r'(?:best practice|recommended approach)[:\s]+(.+?)(?:\.|$)',
        r'(?:organizations should|companies should|teams should)\s+(.+?)(?:\.|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            match = match.strip()
            if len(match) > 15:
                recommendations.append({
                    "recommendation_id": generate_id("REC", rec_counter),
                    "source_id": source_id,
                    "text": match,
                    "priority": "medium"
                })
                rec_counter += 1

    return recommendations


def extract_uncertainties(text: str, source_id: str) -> list:
    """Extract uncertainties and limitations from text."""
    uncertainties = []
    unc_counter = 1

    # Patterns for uncertainties
    patterns = [
        r'(?:limitation|caveat|uncertainty|unclear|unknown)[:\s]+(.+?)(?:\.|$)',
        r'(?:however|but|although)[,]?\s+(.+?)(?:\.|$)',
        r'(?:more research|further study|additional investigation)\s+(?:is needed|required|necessary)\s*(.*)(?:\.|$)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            match = match.strip()
            if len(match) > 15:
                uncertainties.append({
                    "uncertainty_id": generate_id("UNC", unc_counter),
                    "source_id": source_id,
                    "text": match
                })
                unc_counter += 1

    return uncertainties


def parse_source(content: str, source_id: str, source_type: str, source_name: str) -> dict:
    """Parse a source document and extract all structured elements."""

    parsed = {
        "source_id": source_id,
        "source_type": source_type,
        "source_name": source_name,
        "date_parsed": datetime.now().isoformat(),
        "extracted": {
            "claims": extract_claims(content, source_id),
            "evidence": extract_evidence(content, source_id),
            "conclusions": extract_conclusions(content, source_id),
            "recommendations": extract_recommendations(content, source_id),
            "uncertainties": extract_uncertainties(content, source_id)
        },
        "statistics": {
            "total_claims": 0,
            "total_evidence": 0,
            "total_conclusions": 0,
            "total_recommendations": 0,
            "total_uncertainties": 0,
            "word_count": len(content.split())
        }
    }

    # Update statistics
    parsed["statistics"]["total_claims"] = len(parsed["extracted"]["claims"])
    parsed["statistics"]["total_evidence"] = len(parsed["extracted"]["evidence"])
    parsed["statistics"]["total_conclusions"] = len(parsed["extracted"]["conclusions"])
    parsed["statistics"]["total_recommendations"] = len(parsed["extracted"]["recommendations"])
    parsed["statistics"]["total_uncertainties"] = len(parsed["extracted"]["uncertainties"])

    return parsed


def main():
    parser = argparse.ArgumentParser(
        description="Parse research sources and extract structured elements"
    )
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", default="parsed/", help="Output directory")
    parser.add_argument("--source-id", help="Source ID (auto-generated if not provided)")
    parser.add_argument("--source-type", default="document",
                        choices=["ai_model", "web_research", "document", "data", "expert", "other"],
                        help="Type of source")
    parser.add_argument("--source-name", help="Name of source (defaults to filename)")
    parser.add_argument("--output-format", default="json", choices=["json", "text"],
                        help="Output format")

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Set defaults
    source_id = args.source_id or f"SRC-{input_path.stem[:3].upper()}"
    source_name = args.source_name or input_path.name

    # Parse the source
    parsed = parse_source(content, source_id, args.source_type, source_name)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write output
    output_file = output_dir / f"{source_id}_parsed.json"

    if args.output_format == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
        print(f"Parsed output written to: {output_file}")
    else:
        # Text format
        print("=" * 60)
        print(f"PARSED SOURCE: {source_name}")
        print("=" * 60)
        print(f"\nSource ID: {source_id}")
        print(f"Source Type: {args.source_type}")
        print(f"Word Count: {parsed['statistics']['word_count']}")

        print(f"\n--- CLAIMS ({parsed['statistics']['total_claims']}) ---")
        for claim in parsed["extracted"]["claims"]:
            print(f"  [{claim['claim_id']}] ({claim['category']}) {claim['text'][:100]}...")

        print(f"\n--- EVIDENCE ({parsed['statistics']['total_evidence']}) ---")
        for ev in parsed["extracted"]["evidence"]:
            print(f"  [{ev['evidence_id']}] ({ev['type']}) {ev['text'][:80]}...")

        print(f"\n--- CONCLUSIONS ({parsed['statistics']['total_conclusions']}) ---")
        for con in parsed["extracted"]["conclusions"]:
            print(f"  [{con['conclusion_id']}] {con['text'][:80]}...")

        print(f"\n--- RECOMMENDATIONS ({parsed['statistics']['total_recommendations']}) ---")
        for rec in parsed["extracted"]["recommendations"]:
            print(f"  [{rec['recommendation_id']}] {rec['text'][:80]}...")

        print(f"\n--- UNCERTAINTIES ({parsed['statistics']['total_uncertainties']}) ---")
        for unc in parsed["extracted"]["uncertainties"]:
            print(f"  [{unc['uncertainty_id']}] {unc['text'][:80]}...")

    # Print summary
    print(f"\nExtraction Summary:")
    print(f"  Claims: {parsed['statistics']['total_claims']}")
    print(f"  Evidence: {parsed['statistics']['total_evidence']}")
    print(f"  Conclusions: {parsed['statistics']['total_conclusions']}")
    print(f"  Recommendations: {parsed['statistics']['total_recommendations']}")
    print(f"  Uncertainties: {parsed['statistics']['total_uncertainties']}")


if __name__ == "__main__":
    main()
