# Research Consolidator - User Guide

A complete guide to using the Research Consolidator skill for synthesizing multi-source research into comprehensive reports.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Preparing Your Sources](#preparing-your-sources)
3. [Basic Consolidation](#basic-consolidation)
4. [Advanced Features](#advanced-features)
5. [Understanding the Output](#understanding-the-output)
6. [Common Use Cases](#common-use-cases)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Getting Started

### What This Skill Does

The Research Consolidator takes multiple research outputs—from AI models, web searches, documents, and other sources—and synthesizes them into a single, coherent report. It:

- Extracts key claims, evidence, and recommendations from each source
- Identifies where sources agree and disagree
- Calculates confidence levels for findings
- Highlights gaps in research coverage
- Generates professional reports with full attribution

### When to Use This Skill

Use the Research Consolidator when you have:

- **Multiple AI research outputs** (e.g., Claude, GPT-4, Gemini analyses on the same topic)
- **Mixed source types** (AI outputs + industry reports + web research)
- **Potentially conflicting information** that needs reconciliation
- **A need for comprehensive reporting** with source attribution
- **Research gaps** you want to identify before making decisions

### Quick Start Example

```
User: I have three research documents on electric vehicle market trends:
      1. claude_ev_research.md - Claude's deep research output
      2. gpt4_ev_analysis.md - GPT-4's market analysis
      3. industry_report_2024.pdf - McKinsey EV report

      Please consolidate these into an executive report.

Claude: I'll consolidate these three sources into a comprehensive report.
        Let me read and analyze each one...

        [Claude reads each file, extracts claims, identifies agreements/conflicts,
        calculates confidence, and generates the consolidated report]
```

---

## Preparing Your Sources

### Supported Source Types

| Source Type | Examples | Best For |
|-------------|----------|----------|
| **AI Model Outputs** | Claude, GPT-4, Gemini, Perplexity | Broad analysis, multiple perspectives |
| **Web Research** | News articles, blog posts, search results | Current events, recent data |
| **Documents** | PDFs, reports, whitepapers, academic papers | Deep analysis, primary research |
| **Data** | Spreadsheets, datasets, statistics | Quantitative backing |
| **Expert Notes** | Interview transcripts, meeting notes | Domain expertise |

### How to Provide Sources

**Option 1: File Paths**
```
User: Please consolidate these research files:
      - /path/to/claude_research.md
      - /path/to/gpt4_analysis.md
      - /path/to/industry_report.pdf
```

**Option 2: Paste Content**
```
User: I have research from two sources. Here's the first:

      [Paste Claude's research output]

      And here's the second:

      [Paste GPT-4's analysis]

      Please consolidate these.
```

**Option 3: Mixed Approach**
```
User: Please consolidate:
      - File: /path/to/detailed_report.pdf
      - This Perplexity research: [paste content]
      - Key findings from my meeting: [paste notes]
```

### Source Quality Tips

1. **Include full outputs**: Don't truncate AI research—include complete responses
2. **Note the source**: Indicate which AI model or source produced each output
3. **Include dates**: Mention when each source was generated
4. **Flag concerns**: Note if you suspect any source has issues

---

## Basic Consolidation

### Step 1: Provide Context

Tell the skill what you're researching and why:

```
User: I'm researching the feasibility of launching a SaaS product in the
      healthcare space. I need to understand market size, competition,
      and regulatory requirements.

      I have research from three AI models. Please consolidate into an
      executive report for my leadership team.
```

### Step 2: Provide Sources

Share all your research outputs:

```
User: Here are my sources:

      Source 1 (Claude): [paste or file path]
      Source 2 (GPT-4): [paste or file path]
      Source 3 (Gemini): [paste or file path]
```

### Step 3: Specify Output Preferences

Indicate your desired format and audience:

```
User: Please create:
      - An executive summary (1 page max)
      - Detailed findings with confidence levels
      - A section on where sources disagree
      - Recommendations prioritized by confidence
```

### Step 4: Review and Refine

After receiving the consolidated report:

```
User: This is helpful. Can you:
      - Expand on the regulatory findings?
      - Show me exactly where Source 1 and Source 3 disagree?
      - Increase focus on the competitive landscape?
```

---

## Advanced Features

### Custom Confidence Weighting

You can adjust how sources are weighted:

```
User: For this consolidation, please weight the sources as follows:
      - McKinsey Report: Highest credibility (primary research)
      - Claude Analysis: High credibility
      - Web articles: Medium credibility
      - Social media mentions: Low credibility
```

### Specific Topic Focus

Narrow the consolidation to specific topics:

```
User: I only need consolidation on these specific topics:
      1. Market size and growth projections
      2. Key competitors and their market share
      3. Regulatory barriers to entry

      Please ignore other topics from the sources.
```

### Conflict Deep-Dive

Request detailed conflict analysis:

```
User: Sources seem to disagree on market growth rates. Please:
      1. Show me exactly what each source says
      2. Explain why they might differ
      3. Recommend which figure to use and why
```

### Gap Analysis Focus

Request explicit gap identification:

```
User: Before I make a decision, I need to know:
      - What topics weren't covered by any source?
      - Where do we only have one source's perspective?
      - What additional research would you recommend?
```

### Custom Report Sections

Request specific report structure:

```
User: Please generate a report with these sections:
      1. Executive Summary
      2. Market Opportunity (with confidence scores)
      3. Competitive Threats (ranked by severity)
      4. Regulatory Considerations
      5. Source Disagreements & Resolution
      6. Research Gaps & Next Steps
      7. Full Source Attribution
```

---

## Understanding the Output

### Confidence Levels Explained

| Level | Score | Meaning | Action |
|-------|-------|---------|--------|
| **VERY HIGH** | 0.85-1.0 | Strong consensus, quality evidence | Safe to rely on |
| **HIGH** | 0.70-0.84 | Good agreement, reliable sources | Reliable for decisions |
| **MODERATE** | 0.55-0.69 | Some support, verify if critical | Verify before major decisions |
| **LOW** | 0.40-0.54 | Limited support, use with caution | Needs additional research |
| **VERY LOW** | <0.40 | Unreliable, flag concerns | Do not rely on without verification |

### Agreement Indicators

- **HIGH Agreement**: 75%+ of sources agree on the finding
- **MODERATE Agreement**: 50-75% of sources agree
- **PARTIAL Agreement**: At least 2 sources agree
- **SINGLE SOURCE**: Only one source addresses this topic

### Conflict Types

| Type | Description | Example |
|------|-------------|---------|
| **Contradiction** | Sources directly oppose each other | "Growth will be 15%" vs "Growth will be -5%" |
| **Discrepancy** | Numbers differ beyond variance | "$5B market" vs "$12B market" |
| **Opposing View** | Different interpretations | "Regulation is a barrier" vs "Regulation creates opportunity" |

### Gap Types

| Type | Description | Impact |
|------|-------------|--------|
| **Topic Gap** | No source covers this topic | May miss critical information |
| **Source Gap** | Only one source covers this | Cannot validate findings |
| **Depth Gap** | Topic mentioned but not explored | May lack necessary detail |
| **Temporal Gap** | Information may be outdated | Decisions may use stale data |
| **Perspective Gap** | Missing stakeholder viewpoint | May have blind spots |

---

## Common Use Cases

### Use Case 1: AI Model Comparison

**Scenario**: You asked Claude, GPT-4, and Gemini the same research question and want to combine their insights.

```
User: I asked three AI models to analyze the future of remote work.
      Here are their responses:

      [Provide each response]

      Please consolidate, highlighting where they agree and differ.
```

**What You'll Get**:
- Unified findings where models agree
- Explicit callout of disagreements
- Confidence scores based on model consensus
- Recommendations on which perspectives to trust

### Use Case 2: Due Diligence Research

**Scenario**: You're evaluating a company for investment and have multiple research sources.

```
User: I'm doing due diligence on AcmeCorp. I have:
      - Company's investor presentation (PDF)
      - Industry analyst report
      - Claude's analysis of their competitive position
      - News articles from the past 6 months

      Please consolidate into a due diligence summary with risk factors.
```

**What You'll Get**:
- Consolidated company overview
- Validated claims (where multiple sources agree)
- Flagged inconsistencies (company claims vs analyst views)
- Risk factors with confidence levels
- Information gaps to investigate

### Use Case 3: Market Entry Analysis

**Scenario**: Evaluating whether to enter a new market.

```
User: I'm considering entering the Indian e-commerce market. I have:
      - Market research report from Statista
      - GPT-4's analysis of regulatory environment
      - Claude's competitive landscape analysis
      - Recent news articles about market trends

      Consolidate into a market entry recommendation.
```

**What You'll Get**:
- Market size and growth (with source agreement)
- Competitive landscape synthesis
- Regulatory requirements (consolidated)
- Entry barriers and opportunities
- Confidence-weighted recommendations
- Research gaps to address before decision

### Use Case 4: Technical Decision Support

**Scenario**: Choosing between technology options with conflicting recommendations.

```
User: I'm deciding between Kubernetes and Docker Swarm for our container
      orchestration. I have:
      - Claude's technical comparison
      - GPT-4's analysis of our specific requirements
      - Three technical blog posts with different recommendations
      - Vendor documentation for both

      Help me understand the consensus and conflicts.
```

**What You'll Get**:
- Feature comparison synthesis
- Use case recommendations (where sources agree)
- Explicit conflicts with explanations
- Factors unique to your situation
- Confidence-weighted recommendation

---

## Troubleshooting

### Issue: Sources Are Too Different

**Problem**: Sources cover completely different aspects of the topic.

**Solution**:
```
User: These sources don't overlap much. Please:
      1. Create separate sections for each major topic area
      2. Note which sources contributed to each section
      3. Highlight where we only have one perspective
```

### Issue: Too Many Conflicts

**Problem**: Sources contradict each other frequently.

**Solution**:
```
User: There are many conflicts between sources. Please:
      1. Prioritize the most critical conflicts
      2. For each, explain the likely reason for disagreement
      3. Recommend a resolution approach for each
      4. Flag any that require my decision
```

### Issue: Low Confidence Overall

**Problem**: Most findings have low confidence scores.

**Solution**:
```
User: Confidence is low across the board. Please:
      1. Identify which topics have the best support
      2. Explain what additional sources would help
      3. Give me findings I can rely on vs those needing verification
```

### Issue: Missing Critical Topic

**Problem**: An important topic isn't covered by any source.

**Solution**:
```
User: None of my sources address [specific topic]. Can you:
      1. Search for current information on this topic
      2. Add it to the consolidated report
      3. Clearly mark it as coming from supplemental research
```

### Issue: Report Is Too Long/Short

**Problem**: Output doesn't match your needs.

**Solution**:
```
User: The report is too detailed for my executives. Please:
      - Create a 1-page executive summary
      - Include only HIGH confidence findings
      - Put details in an appendix
```

Or:

```
User: I need more detail on [specific section]. Please expand with:
      - Full source quotes
      - All supporting evidence
      - Complete conflict analysis
```

---

## FAQ

### Q: How does confidence scoring work?

Confidence is calculated using four factors:
- **Source Agreement (40%)**: How many sources agree on the finding
- **Evidence Quality (30%)**: Is it backed by data, studies, or just opinion
- **Source Authority (20%)**: How credible is the source (academic > blog)
- **Recency (10%)**: How current is the information

### Q: Can I trust findings where AI models agree?

AI model agreement increases confidence but doesn't guarantee accuracy. Models may:
- Share similar training data (not truly independent)
- Make the same logical assumptions
- Have the same knowledge gaps

For critical decisions, verify against primary sources.

### Q: How should I handle conflicts?

Options:
1. **Defer to authority**: Use the most credible source
2. **Use conservative estimate**: For numbers, use the safer figure
3. **Present both**: For interpretive differences, acknowledge both views
4. **Verify independently**: For critical conflicts, seek additional sources

### Q: What if I disagree with the confidence score?

You can override confidence based on your domain knowledge:

```
User: I know Source X is highly authoritative in this field. Please
      increase its weight and recalculate confidence for findings
      where it contributes.
```

### Q: Can I get just the raw data without the report?

Yes:

```
User: Please give me the consolidated data in JSON format without
      generating a narrative report. I'll use it in my own analysis.
```

### Q: How do I cite the consolidated report?

The report includes full source attribution. For the consolidation itself:

```
"Consolidated Research Report generated using Research Consolidator Skill,
synthesizing [N] sources including [list sources]. [Date]."
```

### Q: Can I save and update the consolidation later?

You can:
1. Save the generated report
2. Add new sources later
3. Ask for re-consolidation with the new sources

```
User: I have a previous consolidation on [topic]. Here's a new source
      to add: [new source]. Please update the consolidation.
```

---

## Tips for Best Results

1. **Be specific about your goal**: "Executive summary for board meeting" vs "Technical deep-dive"

2. **Note source quality upfront**: "The academic paper is more reliable than the blog post"

3. **Ask for what you need**: Don't accept generic output—request specific sections

4. **Iterate**: Use the first output to identify what needs more detail

5. **Verify critical findings**: For high-stakes decisions, always verify independently

6. **Keep sources organized**: Clear labeling helps track attribution

7. **Update regularly**: Research consolidations become stale—refresh with new sources

---

*User Guide for Research Consolidator Skill v1.0.0*
