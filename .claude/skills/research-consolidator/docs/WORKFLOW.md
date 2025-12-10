# Research Consolidator - Workflow Guide

Step-by-step workflows for common research consolidation scenarios.

---

## Table of Contents

1. [Standard Consolidation Workflow](#standard-consolidation-workflow)
2. [AI Model Comparison Workflow](#ai-model-comparison-workflow)
3. [Conflict Resolution Workflow](#conflict-resolution-workflow)
4. [Gap Analysis Workflow](#gap-analysis-workflow)
5. [Executive Report Workflow](#executive-report-workflow)
6. [Quick Comparison Workflow](#quick-comparison-workflow)

---

## Standard Consolidation Workflow

The complete end-to-end process for consolidating multiple research sources.

### Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. INTAKE      │────▶│  2. EXTRACTION  │────▶│  3. ANALYSIS    │
│  Gather sources │     │  Parse content  │     │  Cross-reference│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  6. DELIVERY    │◀────│  5. VALIDATION  │◀────│  4. SYNTHESIS   │
│  Final report   │     │  Quality check  │     │  Consolidate    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Step 1: Intake & Source Registration

**Goal**: Gather and catalog all research sources.

**Actions**:
1. Collect all source materials (files, text, links)
2. Identify source type for each (AI model, document, web, etc.)
3. Note source dates and versions
4. Assign credibility weights if known

**User Provides**:
```
I have the following sources to consolidate:

1. Source: Claude Deep Research
   Type: AI Model (Claude)
   Date: 2025-12-09
   File: /path/to/claude_research.md
   Notes: Comprehensive market analysis

2. Source: GPT-4 Analysis
   Type: AI Model (GPT-4)
   Date: 2025-12-08
   Content: [paste content]
   Notes: Focus on competitive landscape

3. Source: Industry Report 2024
   Type: Document (Industry Report)
   Date: 2024-Q4
   File: /path/to/report.pdf
   Notes: Primary research, high credibility
```

**Output**: Source registry with IDs (SRC-001, SRC-002, etc.)

---

### Step 2: Content Extraction

**Goal**: Extract structured elements from each source.

**For Each Source, Extract**:

| Element | What to Look For |
|---------|------------------|
| **Claims** | Main assertions, findings, statements of fact |
| **Evidence** | Data, statistics, quotes, citations |
| **Conclusions** | Summary judgments, overall assessments |
| **Recommendations** | Suggested actions, advice |
| **Uncertainties** | Caveats, limitations, unknowns |

**Example Extraction**:
```
Source: SRC-001 (Claude Deep Research)

CLAIMS:
- CLM-001: Market expected to grow 15% annually through 2027
- CLM-002: Three dominant players control 65% market share
- CLM-003: Regulatory changes pose significant risk

EVIDENCE:
- EVD-001: Industry data shows 12-18% growth over past 5 years
- EVD-002: Market share data from Q3 2024 reports

CONCLUSIONS:
- CON-001: Market is attractive but competitive

RECOMMENDATIONS:
- REC-001: Enter market through acquisition strategy

UNCERTAINTIES:
- UNC-001: Regulatory timeline uncertain
```

---

### Step 3: Cross-Source Analysis

**Goal**: Map relationships between sources.

**3.1 Claim Alignment**

Create a matrix showing which sources support which claims:

| Claim Theme | SRC-001 | SRC-002 | SRC-003 | Agreement |
|-------------|---------|---------|---------|-----------|
| Market Growth Rate | 15% | 12-18% | 14% CAGR | HIGH |
| Key Competitors | 3 players | 4 players | 3 major | PARTIAL |
| Main Risk | Regulation | Competition | Regulation | MODERATE |
| Entry Strategy | Acquisition | Organic | Partnership | CONFLICT |

**3.2 Conflict Identification**

For each conflict, document:

```
CONFLICT: CNF-001
Topic: Market Entry Strategy
Type: Opposing Views
Severity: HIGH (affects key decision)

Position A (SRC-001, SRC-003):
- Acquisition strategy recommended
- Rationale: Speed to market, established customer base

Position B (SRC-002):
- Organic growth recommended
- Rationale: Lower risk, better cultural fit

Resolution Needed: YES - Critical to decision
```

**3.3 Gap Identification**

Document missing coverage:

| Gap | Description | Sources Missing | Impact |
|-----|-------------|-----------------|--------|
| Regulatory Details | No source provides specific regulations | All | HIGH |
| Customer Segmentation | Only SRC-001 addresses | SRC-002, SRC-003 | MEDIUM |
| Pricing Strategy | Not covered | All | MEDIUM |

---

### Step 4: Synthesis & Consolidation

**Goal**: Create unified findings with confidence scores.

**4.1 For Areas of Agreement**

Merge into consolidated statements:

```
FINDING: FND-001
Title: Market Growth Projection
Category: Market Analysis
Confidence: HIGH (0.82)

Consolidated Statement:
The market is projected to grow 12-15% annually through 2027, with most
estimates centering around 14% CAGR.

Supporting Sources: SRC-001, SRC-002, SRC-003
Evidence Summary: Multiple independent analyses using different methodologies
arrived at consistent conclusions.

Caveats:
- Assumes stable regulatory environment
- Based on current economic conditions
```

**4.2 For Conflicts**

Document resolution approach:

```
FINDING: FND-004
Title: Recommended Entry Strategy
Category: Strategic Recommendation
Confidence: MODERATE (0.58)

Consolidated Statement:
Acquisition strategy is recommended, though organic growth remains a viable
alternative depending on risk tolerance.

Resolution Applied: Defer to primary source (SRC-003 has industry expertise)
with noted dissent.

Minority View: SRC-002 recommends organic growth citing lower risk profile.
```

**4.3 For Gaps**

Acknowledge and recommend:

```
GAP: Research does not address specific regulatory requirements.
Impact: HIGH - Cannot assess compliance costs
Recommendation: Consult regulatory specialist before final decision
```

---

### Step 5: Quality Validation

**Goal**: Ensure report completeness and accuracy.

**Validation Checklist**:

| Check | Status | Notes |
|-------|--------|-------|
| All sources attributed | ✓ | |
| No orphaned claims | ✓ | |
| Conflicts identified | ✓ | 2 conflicts documented |
| Conflicts addressed | ✓ | Resolutions provided |
| Confidence scores justified | ✓ | |
| Gaps acknowledged | ✓ | 3 gaps noted |
| Executive summary accurate | ✓ | Reflects details |
| Recommendations actionable | ✓ | |

---

### Step 6: Report Delivery

**Goal**: Generate final output in requested format.

**Available Formats**:
- Executive Report (full detail)
- Comparison Matrix (side-by-side)
- Findings Summary (brief)
- JSON Data Export

**Final Report Structure**:
```
1. Executive Summary
   - Key findings (top 3-5)
   - Critical conflicts
   - Top recommendations

2. Methodology
   - Sources analyzed
   - Approach description
   - Confidence scoring explanation

3. Detailed Findings
   - Finding 1 with confidence, sources, caveats
   - Finding 2...
   - Finding N...

4. Areas of Conflict
   - Conflict descriptions
   - Resolution approaches

5. Research Gaps
   - Gap list with impact and recommendations

6. Recommendations
   - Prioritized action items

7. Source Attribution
   - Full source details
```

---

## AI Model Comparison Workflow

Specialized workflow for comparing outputs from multiple AI models.

### When to Use

- You asked the same question to multiple AI models
- You want to identify consensus vs unique insights
- You need to verify AI-generated claims

### Process

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Claude       │     │ GPT-4        │     │ Gemini       │
│ Research     │     │ Analysis     │     │ Summary      │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────┬───────┴────────────┬──────┘
                    │                    │
                    ▼                    ▼
           ┌───────────────┐    ┌───────────────┐
           │ Consensus     │    │ Unique        │
           │ Findings      │    │ Insights      │
           └───────────────┘    └───────────────┘
```

### Step-by-Step

**1. Ensure Comparable Inputs**
- Same question/prompt to each model
- Similar scope and depth requested
- Note model versions and dates

**2. Parse Each Model's Output**
- Extract claims, evidence, conclusions
- Note confidence language used by each model
- Identify unique terminology or frameworks

**3. Create Consensus Map**

| Topic | Claude | GPT-4 | Gemini | Status |
|-------|--------|-------|--------|--------|
| Market Size | $50B | $45-55B | $52B | CONSENSUS |
| Growth Rate | 15% | 12% | 18% | VARIANCE |
| Top Risk | Regulation | Regulation | Competition | PARTIAL |

**4. Evaluate Model-Specific Insights**
- Which model provided unique insights?
- Are unique claims verifiable?
- Should unique insights be included or flagged?

**5. Generate Comparison Report**

```
CONSENSUS FINDINGS (High Confidence):
- Finding 1: All models agree...
- Finding 2: All models agree...

MAJORITY FINDINGS (Moderate Confidence):
- Finding 3: 2/3 models agree...

DIVERGENT FINDINGS (Requires Verification):
- Topic X: Models disagree - Claude says A, GPT-4 says B

UNIQUE INSIGHTS (Single Model):
- Claude uniquely identified...
- GPT-4 uniquely identified...
```

---

## Conflict Resolution Workflow

Focused workflow for resolving contradictions between sources.

### When to Use

- Sources directly contradict each other
- Numbers differ significantly
- Recommendations oppose each other

### Decision Process

```
                    ┌─────────────────────┐
                    │ CONFLICT DETECTED   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Is it FACTUAL?      │
                    │ (verifiable fact)   │
                    └──────────┬──────────┘
                         │           │
                        YES         NO
                         │           │
              ┌──────────▼───┐ ┌────▼──────────┐
              │ Can we verify?│ │ Interpretive  │
              └──────┬───────┘ │ difference    │
                 │       │     └───────┬───────┘
                YES     NO             │
                 │       │             │
    ┌────────────▼─┐ ┌───▼────────┐ ┌──▼─────────────┐
    │ Use verified │ │ Use most   │ │ Are both views │
    │ fact         │ │ credible   │ │ valid?         │
    └──────────────┘ │ source     │ └────┬───────────┘
                     └────────────┘   │        │
                                     YES      NO
                                      │        │
                            ┌─────────▼─┐ ┌───▼──────────┐
                            │ Present   │ │ Explain why  │
                            │ both      │ │ one is better│
                            └───────────┘ └──────────────┘
```

### Resolution Documentation

For each conflict, document:

```markdown
## Conflict: [Topic]

**Nature**: [Factual/Interpretive/Methodological]
**Severity**: [High/Medium/Low]

**Source A Position**:
- Source: [ID]
- Claim: [What they say]
- Evidence: [Their support]

**Source B Position**:
- Source: [ID]
- Claim: [What they say]
- Evidence: [Their support]

**Analysis**:
[Why the conflict exists]

**Resolution**:
[How resolved or why unresolved]

**Confidence in Resolution**: [High/Medium/Low]

**Recommendation**:
[What the user should do with this information]
```

---

## Gap Analysis Workflow

Focused workflow for identifying and addressing research gaps.

### Process

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Define Expected │────▶│ Check Coverage  │────▶│ Identify Gaps   │
│ Topic Areas     │     │ Against Sources │     │ & Prioritize    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ Recommend       │
                                                │ Actions         │
                                                └─────────────────┘
```

### Step 1: Define Expected Coverage

List topics that should be covered for comprehensive research:

```
Research Topic: Market Entry Analysis

Expected Coverage:
□ Market Size & Growth
□ Competitive Landscape
□ Customer Segments
□ Pricing Dynamics
□ Regulatory Environment
□ Technology Trends
□ Risk Factors
□ Entry Barriers
□ Success Factors
```

### Step 2: Check Coverage

Map sources to topics:

| Topic | SRC-001 | SRC-002 | SRC-003 | Coverage |
|-------|---------|---------|---------|----------|
| Market Size | ✓ | ✓ | ✓ | FULL |
| Competitors | ✓ | ✓ | - | PARTIAL |
| Customers | ✓ | - | - | SINGLE |
| Pricing | - | - | - | **GAP** |
| Regulatory | - | ✓ | - | SINGLE |
| Technology | ✓ | ✓ | ✓ | FULL |
| Risks | ✓ | - | ✓ | PARTIAL |
| Barriers | - | - | - | **GAP** |
| Success | ✓ | - | - | SINGLE |

### Step 3: Categorize Gaps

| Gap Type | Description | Topics Affected |
|----------|-------------|-----------------|
| **NOT COVERED** | No source addresses | Pricing, Barriers |
| **SINGLE SOURCE** | Only one perspective | Customers, Regulatory, Success |
| **LACKING DEPTH** | Mentioned but shallow | (assess per topic) |

### Step 4: Prioritize by Impact

| Gap | Impact | Priority |
|-----|--------|----------|
| Regulatory (single source) | HIGH - compliance critical | 1 |
| Pricing (not covered) | HIGH - affects business model | 2 |
| Entry Barriers (not covered) | MEDIUM - strategic importance | 3 |
| Customers (single source) | MEDIUM - market understanding | 4 |
| Success Factors (single source) | LOW - nice to validate | 5 |

### Step 5: Recommend Actions

```
HIGH PRIORITY GAPS:

1. Regulatory Environment
   Current: Single source (SRC-002)
   Action: Seek regulatory expert review or legal consultation
   Urgency: Before final decision

2. Pricing Dynamics
   Current: Not covered
   Action: Request pricing-focused research or competitive intelligence
   Urgency: Before business model finalization
```

---

## Executive Report Workflow

Workflow for generating executive-ready consolidated reports.

### Audience Considerations

| Audience | Needs | Emphasis |
|----------|-------|----------|
| C-Suite | Quick insights, decisions | Summary, recommendations |
| Board | Risk awareness, strategy | Conflicts, gaps, confidence |
| Analysts | Full detail | Methodology, data, sources |
| Project Team | Actionable items | Recommendations, next steps |

### Report Structure for Executives

```
┌─────────────────────────────────────────┐
│         EXECUTIVE SUMMARY               │
│  • 3-5 key findings (highest confidence)│
│  • Critical risks/conflicts             │
│  • Top 3 recommendations                │
│  [1 page maximum]                       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         KEY FINDINGS                    │
│  • Finding + Confidence + Sources       │
│  • Visual confidence indicators         │
│  • Brief supporting evidence            │
│  [2-3 pages]                            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         APPENDICES                      │
│  • Full source details                  │
│  • Methodology explanation              │
│  • Conflict resolution details          │
│  • Gap analysis complete                │
│  [Reference only]                       │
└─────────────────────────────────────────┘
```

### Executive Summary Template

```markdown
# [Topic] - Research Consolidation

**Sources**: [N] sources analyzed | **Date**: [Date] | **Confidence**: [Overall]

## Key Findings

1. **[Finding Title]** ⬆️ HIGH CONFIDENCE
   [One sentence summary]

2. **[Finding Title]** ➡️ MODERATE CONFIDENCE
   [One sentence summary]

3. **[Finding Title]** ⬇️ LOW CONFIDENCE
   [One sentence summary]

## Critical Attention Required

- **Conflict**: [Brief description of key conflict]
- **Gap**: [Brief description of critical gap]

## Recommendations

1. [Top recommendation with rationale]
2. [Second recommendation]
3. [Third recommendation]

---
*Full details in attached report*
```

---

## Quick Comparison Workflow

Rapid workflow for simple source comparisons.

### When to Use

- 2-3 sources only
- Need quick comparison, not full report
- Time-sensitive decision

### Process (15-minute workflow)

```
1. READ (5 min)
   - Skim each source for main points
   - Note obvious agreements/conflicts

2. COMPARE (5 min)
   - Create simple comparison table
   - Mark agree/disagree/unique

3. SUMMARIZE (5 min)
   - State consensus findings
   - Note key differences
   - Quick recommendation
```

### Quick Comparison Template

```markdown
## Quick Comparison: [Topic]

| Aspect | Source 1 | Source 2 | Source 3 |
|--------|----------|----------|----------|
| Main Finding | X | X (agree) | Y (differ) |
| Key Data | 15% | 14% | 18% |
| Recommendation | A | A | B |

**Consensus**: [What they agree on]

**Difference**: [Key disagreement and likely reason]

**Quick Take**: [1-2 sentence recommendation]
```

---

*Workflow Guide for Research Consolidator Skill v1.0.0*
