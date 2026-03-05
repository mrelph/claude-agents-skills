# Research Consolidator Skill

A comprehensive research consolidation skill for Claude Code that synthesizes outputs from multiple AI models and sources into cohesive, well-organized research reports.

## Overview

This skill transforms Claude into an Expert Research Analyst capable of:
- Consolidating research from multiple AI models (Claude, GPT, Gemini, Perplexity)
- Integrating web research, documents, and data analyses
- Identifying conflicts between sources and proposing resolutions
- Scoring confidence levels for consolidated findings
- Highlighting research gaps and missing perspectives
- Generating executive reports with full source attribution

## Version

**Current Version**: 1.0.0 (2025-12-09)

## Directory Structure

```
research-consolidator/
├── SKILL.md                    # Main skill definition and workflows
├── README.md                   # This file
├── docs/                       # Documentation
│   ├── USER_GUIDE.md               # Complete user guide with examples
│   ├── WORKFLOW.md                 # Step-by-step workflow guides
│   └── API_REFERENCE.md            # Technical API reference
├── references/                 # Reference documents
│   ├── synthesis_methodology.md    # Research synthesis principles
│   └── report_templates.md         # Report template examples
└── scripts/                    # Python helper scripts
    ├── README.md                   # Scripts documentation
    ├── source_parser.py            # Parse and extract from sources
    ├── claim_alignment.py          # Align claims across sources
    ├── gap_analyzer.py             # Identify research gaps
    ├── report_generator.py         # Generate consolidated reports
    └── report_validator.py         # Validate report quality
```

## Documentation

| Document | Description |
|----------|-------------|
| [USER_GUIDE.md](docs/USER_GUIDE.md) | Complete guide to using the skill with examples |
| [WORKFLOW.md](docs/WORKFLOW.md) | Step-by-step workflows for common scenarios |
| [API_REFERENCE.md](docs/API_REFERENCE.md) | Technical reference for scripts and data structures |
| [scripts/README.md](scripts/README.md) | Script usage and parameters |

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
- Source Agreement (40%)
- Evidence Quality (30%)
- Source Authority (20%)
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

**Gap Analysis:**
```
User: I've gathered research from several sources. What topics are missing coverage?
Skill: Analyzes all sources against expected topic areas, identifies gaps,
       prioritizes by impact, recommends additional research areas.
```

### Running Scripts

**Parse a Source:**
```bash
python scripts/source_parser.py \
  --input research_output.md \
  --source-type ai_model \
  --source-name "Claude Analysis" \
  --output parsed/
```

**Align Claims:**
```bash
python scripts/claim_alignment.py \
  --sources parsed/*.json \
  --output alignment_matrix.json
```

**Identify Gaps:**
```bash
python scripts/gap_analyzer.py \
  --sources parsed/*.json \
  --output gaps.json
```

**Generate Report:**
```bash
python scripts/report_generator.py \
  --findings consolidated.json \
  --gaps gaps.json \
  --template executive \
  --output final_report.md
```

**Validate Report:**
```bash
python scripts/report_validator.py \
  --report final_report.md \
  --findings consolidated.json
```

## Reference Documents

### synthesis_methodology.md

- Research synthesis principles (systematic, transparent, comprehensive, objective)
- Source hierarchy and credibility weighting
- CRAAP test for source evaluation
- Claim extraction framework
- Cross-source analysis methods (triangulation, thematic analysis)
- Conflict resolution strategies and decision tree
- Confidence scoring details
- Quality assurance checklist
- Common pitfalls to avoid
- Special considerations for AI sources

### report_templates.md

- Executive Research Report template
- Comparison Matrix Report template
- Findings Summary (Brief) template
- Data Export (JSON) template
- Template selection guide
- Customization notes

## Conflict Resolution Framework

### Resolution Strategies

| Strategy | When to Use |
|----------|-------------|
| Defer to Primary | One source has clear expertise |
| Recency Wins | Data-dependent findings |
| Conservative Estimate | Quantitative conflicts |
| Present Both | Legitimate differing views |
| Flag for User | Critical decision needed |

### Decision Tree

1. Is it a factual conflict? → Verify against primary sources
2. Is one source more authoritative? → Defer with noted dissent
3. Is this critical to the research question? → Flag for user decision
4. Otherwise → Present both perspectives

## Source Type Handling

### AI Model Outputs
- Cross-reference factual claims across models
- Higher confidence when multiple models agree
- Flag specific facts for verification
- Note model version and training cutoff

### Web Research
- Evaluate source credibility
- Prefer primary sources
- Check publication dates
- Note potential biases

### Document Analysis
- Weight based on publication type
- Check methodology quality
- Extract specific data points
- Note peer review status

## Quality Assurance

Before finalizing, the skill verifies:
- [ ] All sources properly attributed
- [ ] No orphaned claims
- [ ] Conflicts identified and addressed
- [ ] Confidence scores justified
- [ ] Gaps acknowledged
- [ ] Executive summary accurate
- [ ] Recommendations actionable

## Limitations

- Cannot independently verify factual claims
- Confidence scores are estimates, not guarantees
- May not catch subtle biases in source material
- Consolidation reflects available sources only
- Human review recommended for critical decisions

## Best Practices

1. **Provide Clear Context**: Include the original research question
2. **Specify Priorities**: Indicate which sources or topics matter most
3. **Note Intended Audience**: Executive vs technical vs general
4. **Highlight Concerns**: Point out any suspected issues with sources
5. **Request Specific Format**: Executive summary, comparison matrix, or detailed analysis

## Changelog

### v1.0.0 (2025-12-09)
- Initial release
- Multi-source intake and parsing
- Cross-source claim alignment
- Conflict identification and resolution framework
- Confidence scoring system
- Gap identification
- Executive report generation with full attribution
- Support for AI models, web research, and documents
