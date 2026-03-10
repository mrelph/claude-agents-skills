---
name: research-consolidator
description: This skill should be used when the user asks to "consolidate research", "synthesize findings from multiple sources", "compare research from Claude and GPT", "merge research outputs", "combine AI research results", "create a research report from these sources", "summarize what I found", "cross-reference these results", or has research from multiple AI models, web searches, or documents to combine into a unified analysis. Also triggered by mentions of cross-referencing findings, confidence scoring, source attribution, or when the user says they researched something in multiple tools and wants it pulled together.
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Skill, Write, AskUserQuestion
metadata:
  version: 2.0.0
  last-updated: 2026-03-07
  target-users: researchers, analysts, decision-makers
---

# Research Consolidator

Consolidate diverse research outputs -- from AI models, web searches, and document analyses -- into clear, comprehensive, and actionable reports.

The core value of consolidation is trust through triangulation. A single source may be wrong, biased, or incomplete. When multiple independent sources converge on the same finding, confidence increases. When they diverge, that divergence itself is valuable information. This skill makes that process systematic rather than ad hoc.

## Workflow

### 1. Gather Sources

Ask the user to provide:
- All research outputs to consolidate (file paths or pasted content)
- The original research question or topic
- Any priority weighting for sources (optional)
- Intended audience for the final report (optional)

**Supported inputs:** AI model outputs (Claude, GPT, Gemini, Perplexity), web research summaries, PDFs/reports/papers, data extracts, expert notes, and previous research compilations.

For file-based sources, use the source parser to extract structured elements:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/source_parser.py --input <source_file> --output parsed/
```

For pasted content, extract claims, evidence, conclusions, recommendations, and uncertainties directly. See `${CLAUDE_PLUGIN_ROOT}/references/api_reference.md` for the JSON data structures if working with scripts.

### 2. Analyze Across Sources

This is where the real value emerges. Read each source carefully, then:

**Find agreement.** When multiple sources independently reach the same conclusion, that's a strong signal. Map which sources agree on which claims -- a claim supported by 3+ independent sources is far more trustworthy than one from a single source, regardless of how authoritative that source seems.

**Surface conflicts.** Disagreements between sources are not problems to hide -- they're insights. Flag direct contradictions, numerical discrepancies (>20% difference), and opposing recommendations. Document what each side says and why they might differ (different methodology, different data, different time period).

**Assess confidence.** Not all sources are equal. Primary research outweighs opinion pieces. Recent data outweighs stale data. Multiple AI models agreeing outweighs a single model. See `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md` for the detailed source hierarchy, credibility weights, and confidence scoring formula.

**Identify gaps.** What questions did none of the sources address? What was covered by only one source? Where is the data outdated? Gaps are as important as findings because they tell the user where additional research is needed.

Use the analysis scripts when working with many sources:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/claim_alignment.py --sources parsed/*.json --output alignment_matrix.json
python ${CLAUDE_PLUGIN_ROOT}/scripts/gap_analyzer.py --sources parsed/*.json --topic-outline topics.json --output gaps.json
```

### 3. Synthesize Findings

Merge the cross-source analysis into consolidated positions:

- **High agreement:** Merge into a single statement with combined evidence. This is your strongest material.
- **Partial agreement:** Present the consensus view, note variations. Explain the range rather than picking a single number.
- **Conflicts:** Present both sides with attribution. Use your judgment on resolution -- defer to more authoritative sources, use conservative estimates for numbers, or flag for user decision on critical questions.
- **Unique findings:** Include if the source is credible, but note the single-source status so the user understands the limitation.

The goal is a coherent narrative, not a data dump. Connect findings to each other and to the user's original question.

### 4. Resolve Conflicts

When sources disagree, context determines the right approach:

| Situation | Resolution |
|-----------|------------|
| One source clearly more expert | Defer to authority, note dissent |
| Data-dependent disagreement | Use most recent data |
| Quantitative disagreement | Present range or conservative estimate |
| Legitimate differing perspectives | Present both views as valid |
| Critical decision at stake | Flag for user decision |

For each conflict, document: what the disagreement is, which sources disagree, why they might differ, how you resolved it, and what impact it has on overall conclusions. See `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md` for the full conflict resolution decision tree.

### 5. Generate Report

Choose the output format based on the user's needs:

- **Executive Report** (default): Key findings, conflicts, gaps, and recommendations. Best for decision-makers.
- **Comparison Matrix**: Side-by-side view of what each source said on each topic. Best for detailed analysis.
- **Findings Summary**: Bullet-point key findings with confidence levels. Best for quick consumption.
- **Data Export**: JSON of all structured data for further processing.

See `${CLAUDE_PLUGIN_ROOT}/references/report_templates.md` for complete templates for each format.

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/report_generator.py \
  --findings consolidated_findings.json \
  --conflicts conflicts.json \
  --gaps gaps.json \
  --output final_report.md
```

### 6. Validate

Before delivering, verify:
- All sources are properly attributed (no orphaned claims)
- Conflicts are identified and addressed
- Confidence assessments are justified
- Gaps are acknowledged
- Executive summary accurately reflects the detailed findings
- Recommendations are actionable and supported by evidence

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/report_validator.py --report final_report.md --sources sources.json
```

## Working with Different Source Types

Each source type has characteristic strengths and weaknesses that affect how to weight it:

**AI model outputs** tend to be well-structured but may hallucinate facts. Cross-reference factual claims across models -- when multiple models agree on specifics, confidence increases significantly. Always note the model and version.

**Web research** varies widely in credibility. Prefer primary sources over commentary. Check publication dates. Be alert to commercial bias in industry content.

**Documents and papers** often contain primary research and detailed methodology, but may be dated. Weight based on publication type and recency.

For detailed source evaluation criteria, load `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`.

## When to Ask User Questions

Ask for clarification when:
- Critical conflicts require domain expertise to resolve
- Research scope is ambiguous
- Confidence is low on key findings and inclusion/exclusion matters
- Significant gaps need prioritization
- Output format preferences are unclear

Example prompts: "Sources conflict on [X] -- which perspective should I prioritize?", "This finding has low confidence. Include or flag it?", "What level of detail do you need?"

## Limitations

- Cannot independently verify factual claims -- consolidation improves confidence but doesn't guarantee truth
- Confidence scores are estimates based on source agreement and quality, not guarantees
- May not catch subtle biases embedded in source material
- Consolidation quality reflects the quality and coverage of the sources provided

## Reference Documents (Load as needed)

- **`${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`** -- Source hierarchy, credibility weights, confidence scoring formula, CRAAP test, claim extraction framework, quality assurance checklist. Load when you need detailed scoring guidance.
- **`${CLAUDE_PLUGIN_ROOT}/references/report_templates.md`** -- Complete report templates (executive, comparison matrix, findings summary, data export) with customization guidance. Load when generating formal reports.
- **`${CLAUDE_PLUGIN_ROOT}/references/api_reference.md`** -- JSON schemas for all data structures, script APIs, pipeline integration. Load when working with scripts programmatically.
- **`${CLAUDE_PLUGIN_ROOT}/references/user_guide.md`** -- End-to-end user guide with workflows, use cases, troubleshooting, and FAQ.
- **`${CLAUDE_PLUGIN_ROOT}/references/workflow_guide.md`** -- Visual step-by-step workflows for common consolidation scenarios.
