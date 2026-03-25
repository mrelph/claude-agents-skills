# Research Consolidator Plugin

A comprehensive research consolidation plugin for Claude Code that synthesizes outputs from multiple AI models and sources into cohesive, well-organized research reports.

## Overview

This plugin transforms Claude into an Expert Research Analyst capable of:
- Consolidating research from multiple AI models (Claude, GPT, Gemini, Perplexity)
- Integrating web research, documents, and data analyses
- Identifying conflicts between sources and proposing resolutions
- Scoring confidence levels for consolidated findings
- Highlighting research gaps and missing perspectives
- Generating executive reports with full source attribution

## Version

**Current Version**: 2.0.0 (2026-03-25)

## Directory Structure

```
research-consolidator/
├── .claude-plugin/
│   └── plugin.json                   # Plugin manifest
├── skills/
│   └── research-consolidator/
│       └── SKILL.md                  # Main skill definition and workflows
├── references/                       # Reference documents
│   ├── synthesis_methodology.md      # Research synthesis principles
│   ├── report_templates.md           # Report template examples
│   ├── api_reference.md              # Technical API reference
│   ├── user_guide.md                 # Complete user guide with examples
│   └── workflow_guide.md             # Step-by-step workflow guides
├── scripts/                          # Python helper scripts
│   ├── README.md                     # Scripts documentation
│   ├── source_parser.py              # Parse and extract from sources
│   ├── claim_alignment.py            # Align claims across sources
│   ├── gap_analyzer.py               # Identify research gaps
│   ├── report_generator.py           # Generate consolidated reports
│   └── report_validator.py           # Validate report quality
├── examples/                         # Sample source files
│   ├── sample_source_claude.md       # Example Claude research output
│   └── sample_source_web.md          # Example web research summary
└── README.md                         # This file
```

## Documentation

| Document | Description |
|----------|-------------|
| [User Guide](references/user_guide.md) | Complete guide to using the skill with examples |
| [Workflow Guide](references/workflow_guide.md) | Step-by-step workflows for common scenarios |
| [API Reference](references/api_reference.md) | Technical reference for scripts and data structures |
| [Synthesis Methodology](references/synthesis_methodology.md) | Research synthesis principles and scoring |
| [Report Templates](references/report_templates.md) | Standard report templates |
| [Scripts README](scripts/README.md) | Script usage and parameters |

## Key Features

### 1. Multi-Source Intake

**Supported Input Types:**
- AI Model Outputs (Claude, GPT-4, Gemini, Perplexity)
- Web research summaries and search results
- Document analyses (PDFs, reports, papers)
- Data extracts and spreadsheets
- Expert interviews or notes
- Previous research compilations

### 2. Systematic Extraction

For each source, the skill extracts:
- Key claims and assertions
- Supporting evidence
- Conclusions and judgments
- Recommendations
- Uncertainties and limitations
- Cited references

### 3. Cross-Source Analysis

- **Claim Alignment Matrix**: Maps similar claims across sources
- **Agreement Detection**: Identifies HIGH, MODERATE, PARTIAL agreement
- **Conflict Identification**: Flags contradictions and discrepancies
- **Gap Analysis**: Finds topics lacking coverage

### 4. Confidence Scoring

Multi-factor confidence calculation:
- Source Agreement (35%)
- Evidence Quality (25%)
- Source Authority (20%)
- Verification Status (10%)
- Recency (10%)

**Confidence Levels:**
- VERY HIGH (0.85-1.0)
- HIGH (0.70-0.84)
- MODERATE (0.55-0.69)
- LOW (0.40-0.54)
- VERY LOW (<0.40)

### 5. Report Generation

Multiple output formats:
- **Executive Report**: Full report with summary, findings, conflicts, gaps
- **Comparison Matrix**: Side-by-side source comparison
- **Findings Summary**: Brief bullet-point overview
- **Data Export**: JSON for further processing

## Usage

### Invoking the Skill

The skill activates when users need to:
- Consolidate research from multiple AI models
- Synthesize findings from varied sources
- Compare different research outputs
- Generate comprehensive research reports
- Identify conflicts or gaps in research

### Example Interactions

**Consolidating AI Research:**
```
User: I have research outputs from Claude, GPT-4, and Gemini on market trends.
      Please consolidate them into a single report.
Skill: Reads each source, extracts claims, aligns findings, identifies conflicts,
       calculates confidence, generates consolidated executive report.
```

**Identifying Conflicts:**
```
User: These two research reports seem to contradict each other. Help me understand
      where they agree and disagree.
Skill: Parses both sources, creates claim alignment matrix, flags conflicts,
       explains discrepancies, suggests resolution approaches.
```

### Running Scripts

Scripts are optional tools for structured data pipelines. For most tasks, Claude analyzes sources directly.

```bash
# Parse a source
python scripts/source_parser.py --input research.md --source-type ai_model --output parsed/

# Align claims across sources
python scripts/claim_alignment.py --sources parsed/*.json --output alignment.json

# Identify gaps
python scripts/gap_analyzer.py --sources parsed/*.json --output gaps.json

# Generate report
python scripts/report_generator.py --findings consolidated.json --template executive --output report.md

# Validate report
python scripts/report_validator.py --report report.md --findings consolidated.json
```

## Conflict Resolution Framework

| Strategy | When to Use |
|----------|-------------|
| Defer to Primary | One source has clear expertise |
| Recency Wins | Data-dependent findings |
| Conservative Estimate | Quantitative conflicts |
| Present Both | Legitimate differing views |
| Flag for User | Critical decision needed |

## Limitations

- Cannot independently verify factual claims
- Confidence scores are estimates, not guarantees
- May not catch subtle biases in source material
- Consolidation reflects available sources only
- Human review recommended for critical decisions

## Changelog

### v2.0.0 (2026-03-25)
- Restructured SKILL.md for progressive disclosure
- Harmonized confidence scoring (5-factor model)
- Added approach guidance (native analysis vs script pipeline)
- Improved trigger phrases in skill description
- Fixed directory structure documentation
- Added inline reference pointers throughout skill

### v1.0.0 (2025-12-09)
- Initial release
- Multi-source intake and parsing
- Cross-source claim alignment
- Conflict identification and resolution framework
- Confidence scoring system
- Gap identification
- Executive report generation with full attribution
- Support for AI models, web research, and documents
