# Research Consolidator Scripts

Python scripts for parsing sources, aligning claims, identifying gaps, generating reports, and validating output.

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## Scripts Overview

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `source_parser.py` | Parse research sources | Extract claims, evidence, conclusions |
| `claim_alignment.py` | Align claims across sources | Clustering, conflict detection |
| `gap_analyzer.py` | Identify research gaps | Coverage analysis, prioritization |
| `report_generator.py` | Generate consolidated reports | Multiple templates |
| `report_validator.py` | Validate report quality | Completeness checks |

---

## source_parser.py

Parse research sources and extract structured elements.

### Usage

```bash
python source_parser.py \
  --input research_output.md \
  --output parsed/ \
  --source-type ai_model \
  --source-name "Claude Deep Research"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--input` | Yes | - | Input file path |
| `--output` | No | parsed/ | Output directory |
| `--source-id` | No | Auto | Source identifier |
| `--source-type` | No | document | ai_model, web_research, document, data, expert, other |
| `--source-name` | No | Filename | Name of source |
| `--output-format` | No | json | json or text |

### Extracted Elements

- **Claims**: Key assertions with category and confidence
- **Evidence**: Supporting data, quotes, citations
- **Conclusions**: Summary judgments
- **Recommendations**: Suggested actions
- **Uncertainties**: Caveats and limitations

### Output Format

```json
{
  "source_id": "SRC-001",
  "source_type": "ai_model",
  "source_name": "Claude Deep Research",
  "extracted": {
    "claims": [...],
    "evidence": [...],
    "conclusions": [...],
    "recommendations": [...],
    "uncertainties": [...]
  },
  "statistics": {
    "total_claims": 15,
    "word_count": 2500
  }
}
```

---

## claim_alignment.py

Align claims across multiple parsed sources to identify agreement and conflicts.

### Usage

```bash
python claim_alignment.py \
  --sources parsed/SRC-001_parsed.json parsed/SRC-002_parsed.json \
  --output alignment_matrix.json \
  --similarity-threshold 0.3
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--sources` | Yes | - | Parsed source JSON files |
| `--output` | No | alignment_matrix.json | Output file path |
| `--similarity-threshold` | No | 0.3 | Clustering threshold (0.0-1.0) |
| `--output-format` | No | json | json or text |

### Features

- Clusters similar claims using keyword overlap
- Determines agreement levels (HIGH, MODERATE, PARTIAL, SINGLE_SOURCE)
- Detects potential conflicts between clusters
- Builds alignment matrix showing coverage by source

### Agreement Levels

| Level | Description |
|-------|-------------|
| HIGH | 75%+ of sources agree |
| MODERATE | 50-75% of sources agree |
| PARTIAL | 2+ sources agree |
| SINGLE_SOURCE | Only one source has claim |

### Output Includes

- Alignment matrix by theme
- Claim clusters
- Detected conflicts
- Agreement summary statistics

---

## gap_analyzer.py

Identify gaps in research coverage across sources.

### Usage

```bash
python gap_analyzer.py \
  --sources parsed/*.json \
  --output gaps.json \
  --min-sources 2
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--sources` | Yes | - | Parsed source JSON files |
| `--topic-outline` | No | Built-in | Custom topic outline JSON |
| `--output` | No | gaps.json | Output file path |
| `--min-sources` | No | 2 | Minimum sources for coverage |
| `--output-format` | No | json | json or text |

### Gap Types Identified

| Gap Type | Description | Impact |
|----------|-------------|--------|
| Topic Gap | Topic not covered by any source | High |
| Source Gap | Topic covered by only one source | Medium |
| Depth Gap | Topic mentioned but lacking detail | Medium |
| Temporal Gap | Information may be outdated | High/Medium |
| Perspective Gap | Missing stakeholder viewpoint | Low |

### Default Topic Areas Checked

- Market Analysis
- Competitive Landscape
- Technology & Innovation
- Financial Analysis
- Regulatory Environment
- Risk Assessment
- Opportunities
- Stakeholder Analysis

### Custom Topic Outline

Create a JSON file with custom topics:

```json
{
  "custom_topic": {
    "name": "Custom Topic Name",
    "subtopics": ["subtopic1", "subtopic2"],
    "keywords": ["keyword1", "keyword2"]
  }
}
```

---

## report_generator.py

Generate consolidated research reports from analyzed data.

### Usage

```bash
python report_generator.py \
  --findings consolidated_findings.json \
  --alignment alignment_matrix.json \
  --gaps gaps.json \
  --template executive \
  --title "Market Analysis Report" \
  --output final_report.md
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--findings` | Yes | - | Consolidated findings JSON |
| `--alignment` | No | - | Alignment matrix JSON |
| `--gaps` | No | - | Gap analysis JSON |
| `--template` | No | executive | executive, comparison, summary |
| `--title` | No | Research Topic | Report title |
| `--output` | No | report.md | Output file path |

### Available Templates

| Template | Best For | Contents |
|----------|----------|----------|
| `executive` | Decision-makers | Full report with exec summary, findings, conflicts, gaps |
| `comparison` | Detailed review | Side-by-side source comparison matrix |
| `summary` | Quick updates | Brief bullet-point findings summary |

### Findings JSON Structure

```json
{
  "consolidated_findings": [
    {
      "title": "Finding Title",
      "statement": "Consolidated position",
      "confidence_score": 0.85,
      "supporting_sources": ["SRC-001", "SRC-002"],
      "caveats": ["Caveat 1"]
    }
  ],
  "conflicts": [...],
  "recommendations": [...],
  "sources": [...]
}
```

---

## report_validator.py

Validate consolidated reports for completeness and quality.

### Usage

```bash
python report_validator.py \
  --report final_report.md \
  --sources sources.json \
  --findings findings.json \
  --gaps gaps.json
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--report` | Yes | - | Report file to validate (markdown) |
| `--sources` | No | - | Sources JSON file |
| `--findings` | No | - | Findings JSON file |
| `--gaps` | No | - | Gaps JSON file |
| `--output-format` | No | text | text or json |

### Validation Checks

| Check | What It Validates | Severity |
|-------|-------------------|----------|
| Source Attribution | All sources referenced | Error |
| Orphaned Claims | Claims have sources | Warning |
| Conflict Handling | Conflicts addressed | Error |
| Confidence Scores | Scores are justified | Warning |
| Gap Acknowledgment | Gaps documented | Error |
| Executive Summary | Summary is complete | Error |
| Actionable Recommendations | Recommendations actionable | Warning |

### Validation Score

- **90%+**: High quality, ready for use
- **70-89%**: Acceptable with minor concerns
- **<70%**: Needs revision

### Example Output

```
======================================================================
REPORT VALIDATION RESULTS
======================================================================

Report: final_report.md
Validation Score: 86%
Checks Passed: 6/7
Warnings: 1
Errors: 0

--- VALIDATION DETAILS ---

✓ PASS [ℹ] Source Attribution
      All sources properly attributed

✓ PASS [⚠] Orphaned Claims
      2 claim(s) may lack explicit source
        - Line 45: Evidence strongly suggests market growth...

✓ PASS [ℹ] Conflict Handling
      All conflicts identified and resolved

...

======================================================================
⚠ Report passes validation with some concerns to address
```

---

## Typical Workflow

1. **Parse Sources**
   ```bash
   python source_parser.py --input claude_research.md --source-type ai_model --output parsed/
   python source_parser.py --input gpt4_research.md --source-type ai_model --output parsed/
   python source_parser.py --input industry_report.pdf --source-type document --output parsed/
   ```

2. **Align Claims**
   ```bash
   python claim_alignment.py --sources parsed/*.json --output alignment.json
   ```

3. **Identify Gaps**
   ```bash
   python gap_analyzer.py --sources parsed/*.json --output gaps.json
   ```

4. **Create Consolidated Findings** (manual or automated)
   - Combine alignment and gap analysis
   - Resolve conflicts
   - Calculate final confidence scores

5. **Generate Report**
   ```bash
   python report_generator.py \
     --findings consolidated.json \
     --alignment alignment.json \
     --gaps gaps.json \
     --template executive \
     --output final_report.md
   ```

6. **Validate Report**
   ```bash
   python report_validator.py \
     --report final_report.md \
     --findings consolidated.json \
     --gaps gaps.json
   ```

---

## Notes

- All scripts use standard Python library only (no external dependencies)
- JSON output is formatted for readability
- Text output is designed for terminal display
- Scripts can be chained in pipelines
- All extracted IDs follow consistent formats (SRC-XXX, CLM-XXX, etc.)
