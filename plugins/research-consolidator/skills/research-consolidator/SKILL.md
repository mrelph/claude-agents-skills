---
name: research-consolidator
description: This skill should be used when the user asks to "consolidate research", "synthesize findings from multiple sources", "compare research from Claude and GPT", "merge research outputs", "combine AI research results", "create a research report from these sources", "pull together these research docs", "what do these sources agree on", "compare these reports", "summarize what I found", "cross-reference these results", or has research from multiple AI models, web searches, or documents to combine into a unified analysis. Also triggered by mentions of cross-referencing findings, confidence scoring, gap analysis, source attribution, or when the user says they researched something in multiple tools and wants it pulled together.
version: 2.0.0
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Write, AskUserQuestion
metadata:
  last-updated: 2026-03-25
  target-users: researchers, analysts, decision-makers
---

# Research Consolidator

Consolidate diverse research outputs -- from AI models, web searches, and document analyses -- into clear, comprehensive, and actionable reports.

**Core principles:** Objectivity, Transparency, Critical Analysis, Clarity. The core value of consolidation is trust through triangulation -- when multiple independent sources converge on the same finding, confidence increases. When they diverge, that divergence itself is valuable information.

## Approach

For most consolidation tasks, **read and analyze sources directly**. Use your judgment to extract claims, identify agreements and conflicts, score confidence, and synthesize findings into a narrative report with proper attribution.

Use the Python scripts in `${CLAUDE_PLUGIN_ROOT}/scripts/` only when:
- The user requests structured JSON data output
- A formal, repeatable pipeline is needed
- There are many sources (5+) that benefit from automated parsing

For sample source formats, see `${CLAUDE_PLUGIN_ROOT}/examples/`.

## When to Ask the User

Before diving deep, clarify when needed:
- Critical conflicts that require domain expertise to resolve
- Ambiguous research scope or priorities
- Significant gaps that need user prioritization
- Output format preferences (executive report, comparison matrix, summary, JSON)
- Which sources should carry more weight

## Consolidation Framework

### 1. Gather Sources

**Ask the user to provide:**
- All research outputs (file paths or pasted content)
- The original research question or topic
- Any priority weighting for sources
- Specific focus areas or questions to answer
- Intended audience for the final report

**Supported inputs:** AI model outputs, web research, document analyses (PDFs, reports, papers), data extracts, expert notes, previous compilations.

**For each source, note:** source type, name/model, date generated, credibility level, and any context the user provides.

For the full source registration JSON schema, see `${CLAUDE_PLUGIN_ROOT}/references/api_reference.md`.

### 2. Content Extraction

Read each source carefully. Understand the thesis, supporting evidence, and limitations before extracting structured elements.

**Extract from each source:**

| Element | What to Look For |
|---------|------------------|
| Key Claims | Main assertions, findings, statements of fact |
| Evidence | Data, statistics, quotes, citations |
| Conclusions | Summary judgments, overall assessments |
| Recommendations | Suggested actions |
| Uncertainties | Caveats, limitations, unknowns |

Preserve each source's original voice and framing when summarizing perspectives -- don't reduce everything to bare claim/evidence tuples.

**Script alternative:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/source_parser.py --input <source_file> --output parsed/`

**Find agreement.** When multiple sources independently reach the same conclusion, that's a strong signal. Map which sources agree on which claims -- a claim supported by 3+ independent sources is far more trustworthy than one from a single source, regardless of how authoritative that source seems.

#### 3.1 Claim Alignment

Map similar claims across sources to identify agreement levels:

| Agreement Level | Meaning |
|-----------------|---------|
| HIGH | 75%+ of sources agree |
| MODERATE | 50-75% of sources agree |
| PARTIAL | At least 2 sources agree |
| SINGLE SOURCE | Only one source addresses this |

**Script alternative:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/claim_alignment.py --sources parsed/*.json --output alignment_matrix.json`

#### 3.2 Conflict Identification

Flag conflicts when sources directly contradict, show numerical discrepancies beyond reasonable variance (>20%), or give opposing recommendations. For each conflict, document: what the disagreement is, which sources disagree, possible reasons, and severity.

For the complete conflict resolution decision tree and documentation templates, see `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`.

#### 3.3 Confidence Scoring

Calculate confidence for each consolidated finding using five weighted factors:

| Factor | Weight | High Score |
|--------|--------|------------|
| Source Agreement | 35% | 3+ sources agree |
| Evidence Quality | 25% | Primary data with methodology |
| Source Authority | 20% | Peer-reviewed or expert analysis |
| Verification Status | 10% | Independently verifiable |
| Recency | 10% | Less than 3 months old |

**Confidence levels:** Very High (0.85-1.0), High (0.70-0.84), Moderate (0.55-0.69), Low (0.40-0.54), Very Low (<0.40).

For detailed scoring rubrics and source credibility weights, see `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`.

#### 3.4 Gap Identification

Identify what's missing across five gap types: topic gaps (not covered), source gaps (single source only), depth gaps (mentioned but unexplored), temporal gaps (outdated), and perspective gaps (missing stakeholder viewpoint).

**Script alternative:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/gap_analyzer.py --sources parsed/*.json --output gaps.json`

### 3. Synthesize Findings

Apply these rules when merging findings:

| Situation | Approach |
|-----------|----------|
| High agreement | Merge into single statement with combined evidence |
| Partial agreement | Present consensus view, note variations |
| Conflicts | Present both sides, recommend resolution or flag for user |
| Unique findings | Include if credible source, note single-source status |

**Conflict resolution strategies:** Defer to primary source (clear expertise), recency wins (data-dependent), conservative estimate (quantitative conflicts), present both (legitimate differing views), flag for user (critical decisions).

The goal is a coherent narrative, not a data dump. Connect findings to each other and to the user's original question.

For the full conflict resolution decision tree, see `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`.

Choose the output format based on the user's needs:

Generate the report in the user's preferred format:

| Format | Best For |
|--------|----------|
| Executive Report | Decision-makers, full detail with summary |
| Comparison Matrix | Side-by-side source comparison |
| Findings Summary | Quick bullet-point overview |
| Data Export (JSON) | Integration with other tools |

For complete report templates with section structures, see `${CLAUDE_PLUGIN_ROOT}/references/report_templates.md`.

**Script alternative:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/report_generator.py --findings consolidated.json --template executive --output report.md`

### 6. Quality Assurance

Before finalizing, verify:

- [ ] All sources properly attributed
- [ ] No orphaned claims (claims without source)
- [ ] Conflicts identified and addressed
- [ ] Confidence scores justified
- [ ] Gaps acknowledged
- [ ] Executive summary accurately reflects details
- [ ] Recommendations actionable and supported

**Script alternative:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/report_validator.py --report report.md --sources sources.json`

Each source type has characteristic strengths and weaknesses that affect how to weight it:

Different source types need different treatment:

| Source Type | Key Consideration |
|-------------|-------------------|
| AI Models | Cross-reference across models; agreement may reflect shared training data, not independent confirmation |
| Web Research | Evaluate credibility (news vs blog vs academic); check dates; note commercial bias |
| Documents | Weight by publication type and peer review status; check methodology quality |

For detailed source credibility weights and the CRAAP test framework, see `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`.

## Limitations

- Cannot independently verify factual claims -- consolidation improves confidence but doesn't guarantee truth
- Confidence scores are estimates based on source agreement and quality, not guarantees
- May not catch subtle biases embedded in source material
- Consolidation quality reflects the quality and coverage of the sources provided

## Reference Documents

- `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md` -- Detailed methodology, source hierarchy, CRAAP test, claim extraction, confidence scoring rubrics, conflict resolution decision tree, quality assurance checklist
- `${CLAUDE_PLUGIN_ROOT}/references/report_templates.md` -- Full report templates (executive, comparison matrix, findings summary, JSON export) with customization guidance
- `${CLAUDE_PLUGIN_ROOT}/references/api_reference.md` -- JSON schemas, script APIs, pipeline integration, error handling
- `${CLAUDE_PLUGIN_ROOT}/references/user_guide.md` -- Complete user guide with workflows, use cases, troubleshooting, FAQ
- `${CLAUDE_PLUGIN_ROOT}/references/workflow_guide.md` -- Step-by-step visual workflows for standard consolidation, AI comparison, conflict resolution, gap analysis
