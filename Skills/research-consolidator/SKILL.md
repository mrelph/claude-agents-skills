---
name: research-consolidator
description: This skill should be used when the user asks to "consolidate research", "synthesize findings from multiple sources", "compare research from Claude and GPT", "merge research outputs", "combine AI research results", "create a research report from these sources", or has research from multiple AI models, web searches, or documents to combine into a unified analysis. Also triggered by mentions of cross-referencing findings, confidence scoring, or source attribution.
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Skill, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: 2025-12-09
  target-users: researchers, analysts, decision-makers
---

# Research Consolidator Skill

Consolidate diverse research outputs--from AI models, web searches, and document analyses--into clear, comprehensive, and actionable reports.

Core principles:
- **Objectivity**: Present findings without bias toward any single source
- **Transparency**: Always attribute findings to their sources
- **Critical Analysis**: Identify conflicts, gaps, and varying confidence levels
- **Clarity**: Make complex research accessible and actionable

## Core Consolidation Framework

### 1. Intake & Source Registration

**Supported Input Types:**
- AI Model Outputs (Claude, GPT-4, Gemini, Perplexity, etc.)
- Web research summaries and search results
- Document analyses (PDFs, reports, papers)
- Data extracts and spreadsheets
- Expert interviews or notes
- Previous research compilations

**For each source, capture:**
```json
{
  "source_id": "SRC-001",
  "source_type": "ai_model|web_research|document|data|expert|other",
  "source_name": "Claude Deep Research",
  "model_version": "claude-3-opus (if applicable)",
  "date_generated": "2025-12-09",
  "query_or_topic": "Original research question",
  "file_path": "/path/to/source.md (if applicable)",
  "credibility_weight": 1.0,
  "notes": "Any context about this source"
}
```

**Ask user to provide:**
- All research outputs to consolidate (file paths or paste content)
- The original research question or topic
- Any priority weighting for sources
- Specific focus areas or questions to answer
- Intended audience for final report

### 2. Content Extraction & Parsing

**Read and parse each source:**

```bash
# For each source file provided
python scripts/source_parser.py --input <source_file> --output parsed/
```

**Extract structured elements:**

| Element | Description | Record As |
|---------|-------------|-----------|
| Key Claims | Main assertions or findings | `claims[]` |
| Evidence | Supporting data, quotes, citations | `evidence[]` |
| Conclusions | Summary judgments | `conclusions[]` |
| Recommendations | Suggested actions | `recommendations[]` |
| Uncertainties | Caveats, limitations noted | `uncertainties[]` |
| Sources Cited | References within the research | `citations[]` |

**Parsing Template:**
```json
{
  "source_id": "SRC-001",
  "extracted": {
    "claims": [
      {
        "claim_id": "CLM-001",
        "text": "The market is expected to grow 15% annually",
        "category": "market_analysis",
        "confidence_stated": "high",
        "evidence_refs": ["EVD-001", "EVD-002"]
      }
    ],
    "evidence": [
      {
        "evidence_id": "EVD-001",
        "text": "Industry reports show consistent 12-18% growth over 5 years",
        "type": "data|quote|study|example",
        "original_source": "McKinsey Report 2024"
      }
    ],
    "conclusions": [],
    "recommendations": [],
    "uncertainties": []
  }
}
```

### 3. Cross-Source Analysis

**After parsing all sources, perform systematic analysis:**

#### 3.1 Claim Alignment Matrix

Map similar claims across sources:

| Claim Theme | Source 1 | Source 2 | Source 3 | Agreement |
|-------------|----------|----------|----------|-----------|
| Market Growth | 15% annual | 12-18% range | 14% projected | HIGH |
| Key Risk | Regulation | Competition | Regulation | PARTIAL |
| Timeline | 2-3 years | 18 months | 2025-2027 | MODERATE |

```bash
python scripts/claim_alignment.py --sources parsed/*.json --output alignment_matrix.json
```

#### 3.2 Conflict Identification

**Flag conflicts when:**
- Direct contradictions (Source A says X, Source B says not-X)
- Numerical discrepancies beyond reasonable variance (>20% difference)
- Opposing recommendations
- Mutually exclusive conclusions

**Conflict Record:**
```json
{
  "conflict_id": "CNF-001",
  "type": "contradiction|discrepancy|opposing_view",
  "severity": "high|medium|low",
  "claims_involved": ["CLM-001", "CLM-015"],
  "sources_involved": ["SRC-001", "SRC-003"],
  "description": "Source 1 predicts 15% growth, Source 3 predicts 5% decline",
  "resolution_approach": "Further investigation needed|Use conservative estimate|Defer to primary source",
  "resolved_position": "Split the difference at 10% growth given uncertainty"
}
```

#### 3.3 Confidence Scoring

**Calculate confidence for each consolidated finding:**

| Factor | Weight | Scoring |
|--------|--------|---------|
| Source Agreement | 40% | 3+ sources agree = High, 2 = Medium, 1 = Low |
| Evidence Quality | 30% | Primary data = High, Secondary = Medium, Opinion = Low |
| Source Credibility | 20% | Based on source_type and credibility_weight |
| Recency | 10% | <6 months = High, 6-12 = Medium, >12 = Low |

**Confidence Levels:**
- **HIGH** (0.8-1.0): Multiple sources agree with quality evidence
- **MEDIUM** (0.5-0.79): Some agreement or single strong source
- **LOW** (0.3-0.49): Limited agreement or weak evidence
- **UNCERTAIN** (<0.3): Conflicting sources or insufficient data

#### 3.4 Gap Identification

**Identify research gaps:**

| Gap Type | Description | Action |
|----------|-------------|--------|
| Topic Gap | Subject not covered by any source | Flag for additional research |
| Source Gap | Topic covered by only one source | Note limited validation |
| Depth Gap | Topic mentioned but not explored | Consider follow-up |
| Temporal Gap | Data may be outdated | Verify currency |
| Perspective Gap | Missing stakeholder viewpoint | Acknowledge limitation |

```bash
python scripts/gap_analyzer.py --sources parsed/*.json --topic-outline topics.json --output gaps.json
```

### 4. Synthesis & Consolidation

**Synthesize findings into consolidated positions:**

#### 4.1 Consolidation Rules

1. **High Agreement Claims**: Merge into single statement with combined evidence
2. **Partial Agreement**: Present consensus view, note variations
3. **Conflicts**: Present both sides, recommend resolution, or flag for user decision
4. **Unique Findings**: Include if from credible source, note single-source status

#### 4.2 Consolidated Finding Template

```json
{
  "finding_id": "FND-001",
  "category": "market_analysis|risk|opportunity|recommendation|other",
  "consolidated_statement": "The market is projected to grow 12-15% annually over the next 3 years",
  "confidence": "HIGH",
  "confidence_score": 0.85,
  "supporting_sources": ["SRC-001", "SRC-002", "SRC-004"],
  "evidence_summary": "Three independent analyses using different methodologies arrived at similar conclusions",
  "conflicts_noted": [],
  "caveats": ["Assumes no major regulatory changes", "Based on current market conditions"],
  "original_claims": ["CLM-001", "CLM-008", "CLM-022"]
}
```

#### 4.3 Handling Conflicts

**Resolution Strategies:**

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Defer to Primary** | One source has clear expertise | Academic study vs blog post |
| **Recency Wins** | Data-dependent findings | Use most recent market data |
| **Conservative Estimate** | Quantitative conflicts | Use lower/safer projection |
| **Present Both** | Legitimate differing views | Note both perspectives |
| **Flag for User** | Critical decision needed | Ask user to decide |

### 5. Report Generation

**Generate final consolidated report:**

```bash
python scripts/report_generator.py \
  --findings consolidated_findings.json \
  --conflicts conflicts.json \
  --gaps gaps.json \
  --template templates/executive_report.md \
  --output final_report.md
```

#### 5.1 Report Structure

```markdown
# [Research Topic] - Consolidated Research Report

## Executive Summary
- 3-5 key findings
- Overall confidence assessment
- Critical conflicts or gaps noted
- Top recommendations

## Methodology
- Sources analyzed (count and types)
- Consolidation approach
- Confidence scoring explanation

## Key Findings

### Finding 1: [Title]
**Confidence: HIGH/MEDIUM/LOW**

[Consolidated statement]

**Supporting Evidence:**
- Source 1 (Claude): [summary]
- Source 2 (GPT-4): [summary]
- Source 3 (Web Research): [summary]

**Caveats:** [Any limitations]

### Finding 2: [Title]
...

## Areas of Conflict

### Conflict 1: [Topic]
**Sources Disagree On:** [Description]

| Position A | Position B |
|------------|------------|
| [View] | [View] |
| Sources: X, Y | Sources: Z |

**Resolution/Recommendation:** [How addressed]

## Research Gaps

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| [Topic not covered] | [Significance] | [Suggested action] |

## Detailed Analysis
[Full detailed findings by category]

## Source Attribution

| Source ID | Type | Name | Key Contributions |
|-----------|------|------|-------------------|
| SRC-001 | AI Model | Claude Deep Research | Market analysis, risk assessment |
| SRC-002 | Document | Industry Report 2024 | Historical data, projections |

## Appendices
- A: Full Source Details
- B: Claim Alignment Matrix
- C: Confidence Scoring Details
- D: Raw Extracted Data
```

### 6. Quality Assurance

**Before finalizing, verify:**

- [ ] All sources properly attributed
- [ ] No orphaned claims (claims without source)
- [ ] Conflicts identified and addressed
- [ ] Confidence scores justified
- [ ] Gaps acknowledged
- [ ] Executive summary accurately reflects details
- [ ] Recommendations actionable and supported

**Run validation:**
```bash
python scripts/report_validator.py --report final_report.md --sources sources.json
```

---

## Source Type Handling

### AI Model Outputs

**Characteristics:**
- May lack citations to primary sources
- Can have "hallucinated" facts
- Generally well-structured
- May reflect training data biases

**Handling:**
- Cross-reference factual claims across models
- Higher confidence when multiple models agree
- Flag specific facts for verification
- Note model and version for context

### Web Research

**Characteristics:**
- May include primary sources
- Varying credibility (news vs blog vs academic)
- More current information
- May have commercial bias

**Handling:**
- Evaluate source credibility
- Prefer primary sources
- Check publication dates
- Note potential biases

### Document Analysis

**Characteristics:**
- Often contains primary research
- May be dated
- Usually peer-reviewed or professionally produced
- Detailed methodology typically available

**Handling:**
- Weight based on publication type
- Check publication date
- Note methodology quality
- Extract specific data points

---

## Conflict Resolution Framework

### Decision Tree

```
Is there a factual conflict?
├── Yes
│   ├── Is one source clearly more authoritative?
│   │   ├── Yes → Defer to authoritative source, note dissent
│   │   └── No → Is this a quantitative claim?
│   │       ├── Yes → Use conservative estimate or range
│   │       └── No → Present both views with attribution
│   └── Is this a critical finding?
│       ├── Yes → Flag for user decision
│       └── No → Note conflict, use best judgment
└── No (interpretive difference)
    └── Present as different perspectives, both may be valid
```

### Conflict Documentation

For each conflict, document:
1. **What**: Exact nature of disagreement
2. **Who**: Which sources disagree
3. **Why**: Possible reasons for conflict (methodology, data, interpretation)
4. **Resolution**: How you resolved it or why you didn't
5. **Impact**: How this affects overall conclusions

---

## Confidence Scoring Details

### Source Credibility Weights

| Source Type | Base Weight | Adjustments |
|-------------|-------------|-------------|
| Peer-reviewed research | 1.0 | +0.1 if recent, -0.2 if >3 years old |
| Industry reports | 0.9 | +0.1 if primary data |
| AI model (multiple agree) | 0.8 | +0.1 per additional agreeing model |
| AI model (single) | 0.6 | -0.1 if unverifiable facts |
| News articles | 0.7 | -0.2 if opinion piece |
| Blog/informal | 0.4 | +0.2 if expert author |
| User-provided notes | 0.5 | Varies by context |

### Agreement Scoring

| Sources Agreeing | Agreement Score |
|------------------|-----------------|
| 4+ sources | 1.0 |
| 3 sources | 0.85 |
| 2 sources | 0.7 |
| 1 source | 0.5 |
| 0 sources (conflict) | 0.3 |

### Final Confidence Calculation

```
confidence = (agreement_score × 0.4) +
             (evidence_quality × 0.3) +
             (avg_source_credibility × 0.2) +
             (recency_score × 0.1)
```

---

## Output Formats

### Executive Report (Default)
Full report with executive summary, detailed findings, conflicts, and appendices.

### Comparison Matrix
Side-by-side view of what each source said on each topic.

### Findings Summary
Bullet-point summary of key findings with confidence levels.

### Data Export
JSON export of all structured data for further processing.

---

## When to Ask User Questions

**Ask for clarification when:**
- Critical conflicts require domain expertise to resolve
- Research scope is ambiguous
- Confidence is low on key findings
- Significant gaps need prioritization
- Output format preferences unclear

**Use AskUserQuestion for:**
- "Sources conflict on [X]. Which perspective should I prioritize?"
- "Should I include [topic] despite limited coverage?"
- "This finding has low confidence. Include or exclude?"
- "What level of detail do you need for [section]?"

---

## Limitations

- Cannot independently verify factual claims
- Confidence scores are estimates, not guarantees
- May not catch subtle biases in source material
- Consolidation reflects available sources only
- Human review recommended for critical decisions

---

## Reference Documents

- `references/synthesis_methodology.md` -- Detailed synthesis methodology, source hierarchy, claim extraction framework, confidence scoring system, and quality assurance checklist
- `references/report_templates.md` -- Standard report templates (executive, comparison matrix, findings summary, JSON data export) with customization guidance
- `references/api_reference.md` -- Technical reference for data structures, script APIs, JSON schemas, pipeline integration, and error handling
- `references/user_guide.md` -- Complete user guide with source preparation, basic/advanced consolidation workflows, use cases, troubleshooting, and FAQ
- `references/workflow_guide.md` -- Step-by-step visual workflows for standard consolidation, AI model comparison, conflict resolution, gap analysis, and executive reporting
