# Research Consolidator - API Reference

Technical reference for programmatic use of Research Consolidator scripts and data structures.

---

## Table of Contents

1. [Data Structures](#data-structures)
2. [Script APIs](#script-apis)
3. [JSON Schemas](#json-schemas)
4. [Pipeline Integration](#pipeline-integration)
5. [Error Handling](#error-handling)

---

## Data Structures

### Source Object

Represents a registered research source.

```json
{
  "source_id": "SRC-001",
  "source_type": "ai_model|web_research|document|data|expert|other",
  "source_name": "Claude Deep Research",
  "model_version": "claude-3-opus (if applicable)",
  "date_generated": "2025-12-09",
  "query_or_topic": "Original research question",
  "file_path": "/path/to/source.md",
  "credibility_weight": 1.0,
  "notes": "Any context about this source"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | Yes | Unique identifier (format: SRC-XXX) |
| `source_type` | enum | Yes | Category of source |
| `source_name` | string | Yes | Human-readable name |
| `model_version` | string | No | AI model version if applicable |
| `date_generated` | string | No | ISO date when source was created |
| `query_or_topic` | string | No | Original research question |
| `file_path` | string | No | Path to source file |
| `credibility_weight` | float | No | Weight 0.0-1.0, default 1.0 |
| `notes` | string | No | Additional context |

---

### Claim Object

Represents an extracted claim from a source.

```json
{
  "claim_id": "CLM-001",
  "source_id": "SRC-001",
  "text": "The market is expected to grow 15% annually",
  "category": "market_analysis",
  "confidence_stated": "high",
  "evidence_refs": ["EVD-001", "EVD-002"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `claim_id` | string | Yes | Unique identifier (format: CLM-XXX) |
| `source_id` | string | Yes | Reference to source |
| `text` | string | Yes | The claim text |
| `category` | string | No | Claim category |
| `confidence_stated` | string | No | Confidence as stated in source |
| `evidence_refs` | array | No | References to supporting evidence |

**Categories**:
- `market_analysis`
- `risk_assessment`
- `opportunity`
- `technology`
- `financial`
- `competitive`
- `regulatory`
- `operational`
- `strategic`
- `general`

---

### Evidence Object

Represents supporting evidence for claims.

```json
{
  "evidence_id": "EVD-001",
  "source_id": "SRC-001",
  "text": "Industry reports show consistent 12-18% growth over 5 years",
  "type": "data",
  "original_source": "McKinsey Report 2024"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `evidence_id` | string | Yes | Unique identifier (format: EVD-XXX) |
| `source_id` | string | Yes | Reference to source |
| `text` | string | Yes | Evidence description |
| `type` | enum | Yes | Type: data, quote, study, example |
| `original_source` | string | No | Primary source of evidence |

---

### Conflict Object

Represents a conflict between sources.

```json
{
  "conflict_id": "CNF-001",
  "type": "contradiction",
  "severity": "high",
  "theme": "market_analysis",
  "claims_involved": ["CLM-001", "CLM-015"],
  "sources_involved": ["SRC-001", "SRC-003"],
  "description": "Source 1 predicts 15% growth, Source 3 predicts 5% decline",
  "resolution_approach": "Use conservative estimate",
  "resolved_position": "Estimate 10% growth given uncertainty",
  "resolved": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conflict_id` | string | Yes | Unique identifier (format: CNF-XXX) |
| `type` | enum | Yes | contradiction, discrepancy, opposing_view |
| `severity` | enum | Yes | high, medium, low |
| `theme` | string | No | Topic area of conflict |
| `claims_involved` | array | Yes | Claim IDs in conflict |
| `sources_involved` | array | Yes | Source IDs in conflict |
| `description` | string | Yes | Explanation of conflict |
| `resolution_approach` | string | No | How it was resolved |
| `resolved_position` | string | No | Final consolidated position |
| `resolved` | boolean | No | Whether conflict is resolved |

---

### Gap Object

Represents a gap in research coverage.

```json
{
  "gap_id": "GAP-T-001",
  "gap_type": "not_covered",
  "topic": "Regulatory Environment",
  "topic_id": "regulatory",
  "impact": "high",
  "description": "No sources address regulatory requirements",
  "recommendation": "Seek regulatory expert consultation"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gap_id` | string | Yes | Unique identifier (format: GAP-X-XXX) |
| `gap_type` | enum | Yes | not_covered, single_source, lacking_depth, outdated, missing_perspective |
| `topic` | string | Yes | Topic name |
| `topic_id` | string | No | Topic identifier |
| `impact` | enum | Yes | high, medium, low |
| `description` | string | Yes | Gap description |
| `recommendation` | string | Yes | Recommended action |

---

### Finding Object

Represents a consolidated finding.

```json
{
  "finding_id": "FND-001",
  "category": "market_analysis",
  "title": "Market Growth Projection",
  "consolidated_statement": "The market is projected to grow 12-15% annually",
  "confidence": "HIGH",
  "confidence_score": 0.85,
  "supporting_sources": ["SRC-001", "SRC-002", "SRC-004"],
  "evidence_summary": "Three independent analyses arrived at similar conclusions",
  "conflicts_noted": [],
  "caveats": ["Assumes no major regulatory changes"],
  "original_claims": ["CLM-001", "CLM-008", "CLM-022"],
  "source_perspectives": [
    {
      "source": "SRC-001",
      "position": "15% annual growth expected",
      "evidence": "Industry trend analysis"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finding_id` | string | Yes | Unique identifier (format: FND-XXX) |
| `category` | string | Yes | Finding category |
| `title` | string | Yes | Short title |
| `consolidated_statement` | string | Yes | Full finding statement |
| `confidence` | string | Yes | Confidence level label |
| `confidence_score` | float | Yes | Numeric confidence (0.0-1.0) |
| `supporting_sources` | array | Yes | Source IDs supporting this |
| `evidence_summary` | string | No | Summary of evidence |
| `conflicts_noted` | array | No | Related conflict IDs |
| `caveats` | array | No | Limitations or conditions |
| `original_claims` | array | No | Claim IDs consolidated |
| `source_perspectives` | array | No | Per-source details |

---

## Script APIs

### source_parser.py

**Purpose**: Parse research sources and extract structured elements.

**Command Line**:
```bash
python source_parser.py \
  --input <file_path> \
  --output <directory> \
  --source-id <id> \
  --source-type <type> \
  --source-name <name> \
  --output-format <json|text>
```

**Arguments**:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Input file path |
| `--output` | No | `parsed/` | Output directory |
| `--source-id` | No | Auto-generated | Source identifier |
| `--source-type` | No | `document` | Source type enum |
| `--source-name` | No | Filename | Source name |
| `--output-format` | No | `json` | Output format |

**Output Schema**:
```json
{
  "source_id": "string",
  "source_type": "string",
  "source_name": "string",
  "date_parsed": "ISO datetime",
  "extracted": {
    "claims": ["Claim objects"],
    "evidence": ["Evidence objects"],
    "conclusions": ["Conclusion objects"],
    "recommendations": ["Recommendation objects"],
    "uncertainties": ["Uncertainty objects"]
  },
  "statistics": {
    "total_claims": "integer",
    "total_evidence": "integer",
    "total_conclusions": "integer",
    "total_recommendations": "integer",
    "total_uncertainties": "integer",
    "word_count": "integer"
  }
}
```

**Exit Codes**:
- `0`: Success
- `1`: Input file not found
- `2`: Parse error

---

### claim_alignment.py

**Purpose**: Align claims across multiple parsed sources.

**Command Line**:
```bash
python claim_alignment.py \
  --sources <file1.json> <file2.json> ... \
  --output <output_file> \
  --similarity-threshold <0.0-1.0> \
  --output-format <json|text>
```

**Arguments**:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--sources` | Yes | - | Parsed source JSON files |
| `--output` | No | `alignment_matrix.json` | Output file |
| `--similarity-threshold` | No | `0.3` | Clustering threshold |
| `--output-format` | No | `json` | Output format |

**Output Schema**:
```json
{
  "metadata": {
    "sources_analyzed": ["source IDs"],
    "total_claims": "integer",
    "total_clusters": "integer",
    "total_conflicts": "integer",
    "similarity_threshold": "float"
  },
  "alignment_matrix": {
    "sources": ["source IDs"],
    "themes": ["theme names"],
    "alignment": [{
      "theme": "string",
      "agreement": "HIGH|MODERATE|PARTIAL|SINGLE_SOURCE",
      "source_coverage": {
        "SRC-001": {
          "has_claim": "boolean",
          "claim_id": "string|null",
          "summary": "string|null"
        }
      }
    }]
  },
  "clusters": ["Cluster objects"],
  "conflicts": ["Conflict objects"],
  "summary": {
    "high_agreement": "integer",
    "moderate_agreement": "integer",
    "partial_agreement": "integer",
    "single_source": "integer"
  }
}
```

---

### gap_analyzer.py

**Purpose**: Identify gaps in research coverage.

**Command Line**:
```bash
python gap_analyzer.py \
  --sources <file1.json> <file2.json> ... \
  --topic-outline <topics.json> \
  --output <output_file> \
  --min-sources <integer> \
  --output-format <json|text>
```

**Arguments**:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--sources` | Yes | - | Parsed source JSON files |
| `--topic-outline` | No | Built-in | Custom topic outline |
| `--output` | No | `gaps.json` | Output file |
| `--min-sources` | No | `2` | Minimum for coverage |
| `--output-format` | No | `json` | Output format |

**Topic Outline Schema**:
```json
{
  "topic_id": {
    "name": "Topic Display Name",
    "subtopics": ["subtopic1", "subtopic2"],
    "keywords": ["keyword1", "keyword2"]
  }
}
```

**Output Schema**:
```json
{
  "metadata": {
    "sources_analyzed": ["source IDs"],
    "topic_areas_checked": "integer",
    "min_sources_for_coverage": "integer",
    "analysis_date": "ISO datetime"
  },
  "coverage_statistics": {
    "overall_coverage_score": "float (0.0-1.0)",
    "total_topics_expected": "integer",
    "topics_fully_covered": "integer",
    "topics_partially_covered": "integer",
    "topics_not_covered": "integer",
    "total_gaps_identified": "integer",
    "gaps_by_type": {
      "topic_gaps": "integer",
      "source_gaps": "integer",
      "depth_gaps": "integer",
      "temporal_gaps": "integer",
      "perspective_gaps": "integer"
    },
    "high_impact_gaps": "integer",
    "medium_impact_gaps": "integer",
    "low_impact_gaps": "integer"
  },
  "gaps": {
    "topic_gaps": ["Gap objects"],
    "source_gaps": ["Gap objects"],
    "depth_gaps": ["Gap objects"],
    "temporal_gaps": ["Gap objects"],
    "perspective_gaps": ["Gap objects"]
  },
  "prioritized_action_items": ["Top 10 Gap objects"]
}
```

---

### report_generator.py

**Purpose**: Generate consolidated research reports.

**Command Line**:
```bash
python report_generator.py \
  --findings <findings.json> \
  --alignment <alignment.json> \
  --gaps <gaps.json> \
  --template <executive|comparison|summary> \
  --title <report_title> \
  --output <output_file>
```

**Arguments**:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--findings` | Yes | - | Consolidated findings JSON |
| `--alignment` | No | - | Alignment matrix JSON |
| `--gaps` | No | - | Gap analysis JSON |
| `--template` | No | `executive` | Report template |
| `--title` | No | `Research Topic` | Report title |
| `--output` | No | `report.md` | Output file |

**Findings Input Schema**:
```json
{
  "consolidated_findings": ["Finding objects"],
  "conflicts": ["Conflict objects"],
  "recommendations": ["Recommendation objects"],
  "insights": ["string"],
  "sources": ["Source objects"],
  "overall_confidence": "string"
}
```

**Output**: Markdown formatted report

---

### report_validator.py

**Purpose**: Validate report quality and completeness.

**Command Line**:
```bash
python report_validator.py \
  --report <report.md> \
  --sources <sources.json> \
  --findings <findings.json> \
  --gaps <gaps.json> \
  --output-format <json|text>
```

**Arguments**:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--report` | Yes | - | Report file (markdown) |
| `--sources` | No | - | Sources JSON |
| `--findings` | No | - | Findings JSON |
| `--gaps` | No | - | Gaps JSON |
| `--output-format` | No | `text` | Output format |

**Output Schema** (JSON):
```json
{
  "report_file": "string",
  "validation_score": "float (0.0-1.0)",
  "total_checks": "integer",
  "passed": "integer",
  "warnings": "integer",
  "errors": "integer",
  "results": [{
    "check": "string",
    "passed": "boolean",
    "message": "string",
    "severity": "info|warning|error",
    "details": ["string"]
  }]
}
```

**Validation Checks**:
1. Source Attribution
2. Orphaned Claims
3. Conflict Handling
4. Confidence Scores
5. Gap Acknowledgment
6. Executive Summary
7. Actionable Recommendations

---

## JSON Schemas

### Complete Findings Export

Full schema for consolidated research data:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "sources", "findings"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "date_generated": {"type": "string", "format": "date-time"},
        "skill_version": {"type": "string"},
        "overall_confidence": {"type": "number", "minimum": 0, "maximum": 1}
      }
    },
    "sources": {
      "type": "array",
      "items": {"$ref": "#/definitions/Source"}
    },
    "findings": {
      "type": "array",
      "items": {"$ref": "#/definitions/Finding"}
    },
    "conflicts": {
      "type": "array",
      "items": {"$ref": "#/definitions/Conflict"}
    },
    "gaps": {
      "type": "array",
      "items": {"$ref": "#/definitions/Gap"}
    },
    "recommendations": {
      "type": "array",
      "items": {"$ref": "#/definitions/Recommendation"}
    }
  },
  "definitions": {
    "Source": {
      "type": "object",
      "required": ["id", "type", "name"],
      "properties": {
        "id": {"type": "string"},
        "type": {"enum": ["ai_model", "web_research", "document", "data", "expert", "other"]},
        "name": {"type": "string"},
        "date": {"type": "string"},
        "credibility": {"type": "number"}
      }
    },
    "Finding": {
      "type": "object",
      "required": ["id", "title", "statement", "confidence_score"],
      "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "statement": {"type": "string"},
        "confidence_score": {"type": "number"},
        "confidence_level": {"enum": ["VERY HIGH", "HIGH", "MODERATE", "LOW", "VERY LOW"]},
        "supporting_sources": {"type": "array", "items": {"type": "string"}},
        "caveats": {"type": "array", "items": {"type": "string"}}
      }
    },
    "Conflict": {
      "type": "object",
      "required": ["id", "type", "description"],
      "properties": {
        "id": {"type": "string"},
        "type": {"enum": ["contradiction", "discrepancy", "opposing_view"]},
        "severity": {"enum": ["high", "medium", "low"]},
        "description": {"type": "string"},
        "resolved": {"type": "boolean"}
      }
    },
    "Gap": {
      "type": "object",
      "required": ["id", "gap_type", "description"],
      "properties": {
        "id": {"type": "string"},
        "gap_type": {"enum": ["not_covered", "single_source", "lacking_depth", "outdated", "missing_perspective"]},
        "topic": {"type": "string"},
        "impact": {"enum": ["high", "medium", "low"]},
        "description": {"type": "string"},
        "recommendation": {"type": "string"}
      }
    },
    "Recommendation": {
      "type": "object",
      "required": ["id", "action"],
      "properties": {
        "id": {"type": "string"},
        "action": {"type": "string"},
        "rationale": {"type": "string"},
        "priority": {"enum": ["high", "medium", "low"]},
        "based_on_findings": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

---

## Pipeline Integration

### Bash Pipeline

Complete pipeline from sources to validated report:

```bash
#!/bin/bash

# Configuration
SOURCES_DIR="./sources"
OUTPUT_DIR="./output"
TITLE="Market Analysis Report"

# Create output directory
mkdir -p "$OUTPUT_DIR/parsed"

# Step 1: Parse all sources
for source in "$SOURCES_DIR"/*.md; do
  filename=$(basename "$source" .md)
  python scripts/source_parser.py \
    --input "$source" \
    --source-type ai_model \
    --output "$OUTPUT_DIR/parsed/"
done

# Step 2: Align claims
python scripts/claim_alignment.py \
  --sources "$OUTPUT_DIR/parsed/"*.json \
  --output "$OUTPUT_DIR/alignment.json"

# Step 3: Identify gaps
python scripts/gap_analyzer.py \
  --sources "$OUTPUT_DIR/parsed/"*.json \
  --output "$OUTPUT_DIR/gaps.json"

# Step 4: Generate report (requires consolidated findings)
python scripts/report_generator.py \
  --findings "$OUTPUT_DIR/findings.json" \
  --alignment "$OUTPUT_DIR/alignment.json" \
  --gaps "$OUTPUT_DIR/gaps.json" \
  --template executive \
  --title "$TITLE" \
  --output "$OUTPUT_DIR/report.md"

# Step 5: Validate report
python scripts/report_validator.py \
  --report "$OUTPUT_DIR/report.md" \
  --findings "$OUTPUT_DIR/findings.json" \
  --gaps "$OUTPUT_DIR/gaps.json" \
  --output-format json > "$OUTPUT_DIR/validation.json"

echo "Pipeline complete. Report: $OUTPUT_DIR/report.md"
```

### Python Integration

```python
import json
import subprocess
from pathlib import Path

def run_consolidation_pipeline(
    source_files: list[Path],
    output_dir: Path,
    title: str = "Research Report"
) -> dict:
    """Run complete consolidation pipeline."""

    output_dir.mkdir(parents=True, exist_ok=True)
    parsed_dir = output_dir / "parsed"
    parsed_dir.mkdir(exist_ok=True)

    # Step 1: Parse sources
    parsed_files = []
    for source in source_files:
        result = subprocess.run([
            "python", "scripts/source_parser.py",
            "--input", str(source),
            "--output", str(parsed_dir),
            "--output-format", "json"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            parsed_files.append(parsed_dir / f"{source.stem}_parsed.json")

    # Step 2: Align claims
    alignment_file = output_dir / "alignment.json"
    subprocess.run([
        "python", "scripts/claim_alignment.py",
        "--sources", *[str(f) for f in parsed_files],
        "--output", str(alignment_file)
    ])

    # Step 3: Analyze gaps
    gaps_file = output_dir / "gaps.json"
    subprocess.run([
        "python", "scripts/gap_analyzer.py",
        "--sources", *[str(f) for f in parsed_files],
        "--output", str(gaps_file)
    ])

    # Load results
    with open(alignment_file) as f:
        alignment = json.load(f)
    with open(gaps_file) as f:
        gaps = json.load(f)

    return {
        "parsed_files": parsed_files,
        "alignment": alignment,
        "gaps": gaps
    }
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` | Input file doesn't exist | Verify file path |
| `JSONDecodeError` | Invalid JSON in input | Validate JSON format |
| `KeyError: 'source_id'` | Missing required field | Check input schema |
| `No claims found` | Parser couldn't extract claims | Check source format |

### Exit Codes

All scripts use consistent exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Input file not found |
| 2 | Parse/processing error |
| 3 | Output write error |
| 4 | Validation failed |

### Logging

Enable verbose output for debugging:

```bash
# Set environment variable for verbose mode
export RC_VERBOSE=1

# Or use stderr redirection
python scripts/source_parser.py --input file.md 2>&1 | tee debug.log
```

---

*API Reference for Research Consolidator Skill v1.0.0*
