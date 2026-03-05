# Research Synthesis Methodology

A comprehensive guide to synthesizing research from multiple sources into coherent, reliable findings.

## Principles of Research Synthesis

### 1. Systematic Approach

Research synthesis must be:
- **Reproducible**: Another analyst could follow the same process
- **Transparent**: Methods and decisions are documented
- **Comprehensive**: All relevant sources are considered
- **Objective**: Personal bias is minimized

### 2. Source Hierarchy

Not all sources are equal. Use this hierarchy for weighting:

| Tier | Source Type | Characteristics | Base Weight |
|------|-------------|-----------------|-------------|
| 1 | Primary Research | Original data, experiments, surveys | 1.0 |
| 2 | Peer-Reviewed | Academic journals, vetted publications | 0.95 |
| 3 | Expert Analysis | Industry reports, professional analysis | 0.85 |
| 4 | AI Model Consensus | Multiple AI models agreeing | 0.80 |
| 5 | Single AI Model | One AI model output | 0.60 |
| 6 | News/Media | Journalism, news reports | 0.70 |
| 7 | Opinion/Commentary | Blogs, op-eds, social media | 0.40 |

### 3. The CRAAP Test for Sources

Evaluate each source using:

| Criterion | Questions to Ask |
|-----------|------------------|
| **Currency** | When was it published? Is it current for your topic? |
| **Relevance** | Does it relate to your research question? |
| **Authority** | Who is the author? What are their credentials? |
| **Accuracy** | Is it supported by evidence? Can it be verified? |
| **Purpose** | Why was it written? Is there bias? |

---

## Claim Extraction Framework

### Types of Claims

| Claim Type | Definition | Example |
|------------|------------|---------|
| **Factual** | Verifiable statement of fact | "The market size was $5B in 2024" |
| **Causal** | Asserts cause-effect relationship | "Interest rates drove the decline" |
| **Predictive** | Forecast or projection | "Growth will reach 15% by 2027" |
| **Evaluative** | Judgment or assessment | "This approach is most effective" |
| **Prescriptive** | Recommendation | "Companies should invest in AI" |

### Claim Strength Indicators

**Strong Claims:**
- Supported by multiple sources
- Based on primary data
- Include specific numbers/dates
- Acknowledge limitations
- Provide methodology

**Weak Claims:**
- Single source only
- Vague language ("many experts say")
- No supporting evidence
- Absolute statements without caveats
- Unknown methodology

### Extracting Claims

For each source, identify:

1. **Main Thesis**: The central argument or finding
2. **Supporting Claims**: Evidence backing the thesis
3. **Counter-Arguments**: Any opposing views mentioned
4. **Limitations**: Acknowledged weaknesses
5. **Recommendations**: Suggested actions

---

## Cross-Source Analysis Methods

### 1. Triangulation

Verify findings by checking if:
- Multiple independent sources reach same conclusion
- Different methodologies produce consistent results
- Various data types support the same finding

**Triangulation Matrix:**
```
Finding: [State the finding]

| Method/Source Type | Supports | Contradicts | Neutral |
|--------------------|----------|-------------|---------|
| AI Models          |    ✓     |             |         |
| Academic Research  |    ✓     |             |         |
| Industry Reports   |          |      ✓      |         |
| News Sources       |    ✓     |             |         |

Triangulation Status: PARTIAL (3/4 support)
```

### 2. Thematic Analysis

Group related findings across sources:

```
Theme: Market Growth Projections

Source 1 (Claude): 12-15% annual growth expected
Source 2 (GPT-4): Conservative 10% baseline, optimistic 18%
Source 3 (Report): 14.2% CAGR projected through 2028
Source 4 (Web): Industry leaders expect "double-digit growth"

Synthesis: Consensus points to 12-15% annual growth, with range of 10-18%
depending on economic conditions. Most specific projection: 14.2% CAGR.
```

### 3. Gap Analysis

Systematically identify what's missing:

| Expected Topic | Source 1 | Source 2 | Source 3 | Coverage |
|----------------|----------|----------|----------|----------|
| Market Size    |    ✓     |    ✓     |    ✓     | Full |
| Competitors    |    ✓     |    ✓     |          | Partial |
| Regulations    |          |    ✓     |          | Limited |
| Technology     |    ✓     |          |          | Single Source |
| Risks          |          |          |          | **GAP** |

---

## Conflict Resolution Strategies

### Types of Conflicts

| Conflict Type | Example | Resolution Approach |
|---------------|---------|---------------------|
| **Factual** | Different numbers cited | Verify primary source |
| **Interpretive** | Same data, different conclusions | Present both views |
| **Methodological** | Different approaches used | Note methodology differences |
| **Temporal** | Findings from different time periods | Prefer recent, note evolution |
| **Scope** | Different aspects analyzed | May not be true conflict |

### Resolution Decision Tree

```
CONFLICT DETECTED
│
├── Is it factual (verifiable)?
│   ├── YES → Can we verify the correct fact?
│   │   ├── YES → Use verified fact, note discrepancy
│   │   └── NO → Use most credible source, flag uncertainty
│   │
│   └── NO (interpretive) → Are both interpretations valid?
│       ├── YES → Present both perspectives
│       └── NO → Explain why one is more supported
│
├── Is one source clearly more authoritative?
│   ├── YES → Defer to authority, cite dissenting view
│   └── NO → Weight by source quality and recency
│
└── Is this critical to the research question?
    ├── YES → Flag for user decision
    └── NO → Use best judgment, document reasoning
```

### Documenting Conflict Resolution

For every conflict resolved, record:

```markdown
## Conflict: [Brief description]

**Sources Involved:** SRC-001, SRC-003

**Nature of Conflict:**
Source 1 claims X, while Source 3 claims Y.

**Analysis:**
[Explain why the conflict exists - different data, methodology, interpretation]

**Resolution:**
[State how you resolved it]

**Confidence in Resolution:** High/Medium/Low

**Reasoning:**
[Justify the resolution approach]

**Remaining Uncertainty:**
[Note any lingering questions]
```

---

## Confidence Scoring System

### Multi-Factor Confidence Model

```
CONFIDENCE SCORE =
  (Source Agreement × 0.35) +
  (Evidence Quality × 0.25) +
  (Source Authority × 0.20) +
  (Verification Status × 0.10) +
  (Recency × 0.10)
```

### Factor Scoring

**Source Agreement (0-1):**
| Condition | Score |
|-----------|-------|
| 4+ sources agree | 1.0 |
| 3 sources agree | 0.85 |
| 2 sources agree | 0.70 |
| 1 source only | 0.50 |
| Sources conflict | 0.30 |

**Evidence Quality (0-1):**
| Evidence Type | Score |
|---------------|-------|
| Primary data with methodology | 1.0 |
| Secondary data with citation | 0.80 |
| Referenced but not shown | 0.60 |
| General assertion | 0.40 |
| Opinion only | 0.20 |

**Source Authority (0-1):**
| Source Type | Score |
|-------------|-------|
| Peer-reviewed academic | 1.0 |
| Industry expert/analyst | 0.85 |
| Multiple AI models agree | 0.75 |
| Single authoritative AI | 0.60 |
| News/media | 0.50 |
| Unknown/unverified | 0.30 |

**Verification Status (0-1):**
| Status | Score |
|--------|-------|
| Independently verified | 1.0 |
| Verifiable but not verified | 0.70 |
| Difficult to verify | 0.40 |
| Cannot be verified | 0.20 |

**Recency (0-1):**
| Age of Information | Score |
|--------------------|-------|
| < 3 months | 1.0 |
| 3-6 months | 0.90 |
| 6-12 months | 0.75 |
| 1-2 years | 0.50 |
| > 2 years | 0.30 |

### Interpreting Confidence Scores

| Score Range | Label | Interpretation |
|-------------|-------|----------------|
| 0.85 - 1.00 | Very High | Strong consensus, quality evidence |
| 0.70 - 0.84 | High | Good agreement, reliable sources |
| 0.55 - 0.69 | Moderate | Some support, verify if critical |
| 0.40 - 0.54 | Low | Limited support, use with caution |
| 0.00 - 0.39 | Very Low | Unreliable, flag concerns |

---

## Synthesis Writing Guidelines

### Language for Confidence Levels

**High Confidence:**
- "Evidence strongly suggests..."
- "Sources consistently indicate..."
- "There is broad consensus that..."

**Moderate Confidence:**
- "Evidence suggests..."
- "Most sources indicate..."
- "The balance of evidence points to..."

**Low Confidence:**
- "Some evidence suggests..."
- "Limited sources indicate..."
- "It appears that... though evidence is mixed"

**Noting Uncertainty:**
- "Sources disagree on..."
- "Evidence is inconclusive regarding..."
- "Further research is needed to determine..."

### Attribution Best Practices

**Always attribute:**
- Direct quotes
- Specific statistics
- Unique insights or findings
- Controversial claims

**Attribution formats:**
- Inline: "According to [Source], ..."
- Parenthetical: "...reaching 15% growth (Claude Analysis, GPT-4 Report)"
- Footnote: For detailed source information

### Synthesized Statement Structure

```
[Confidence indicator] + [Synthesized finding] + [Source attribution] + [Caveats if any]
```

**Example:**
"Evidence strongly suggests that the market will experience 12-15% annual growth through 2028 (supported by Claude Analysis, McKinsey Report, and industry surveys), though this assumes stable regulatory conditions."

---

## Quality Assurance Checklist

### Before Finalizing Synthesis

**Completeness:**
- [ ] All provided sources analyzed
- [ ] Key claims extracted from each source
- [ ] Themes identified across sources
- [ ] Gaps documented

**Accuracy:**
- [ ] Claims correctly attributed
- [ ] Numbers and dates verified where possible
- [ ] Context preserved in extractions
- [ ] No misrepresentation of source positions

**Consistency:**
- [ ] Confidence scores applied consistently
- [ ] Conflict resolution logic consistent
- [ ] Terminology used consistently
- [ ] Formatting uniform throughout

**Transparency:**
- [ ] Methodology documented
- [ ] Conflicts explicitly noted
- [ ] Limitations acknowledged
- [ ] Source list complete

**Usefulness:**
- [ ] Answers original research question
- [ ] Executive summary captures key points
- [ ] Findings are actionable
- [ ] Appropriate level of detail for audience

---

## Common Pitfalls to Avoid

### 1. Cherry-Picking
**Problem:** Selectively using sources that support a predetermined conclusion
**Solution:** Include all relevant sources; document exclusions with reasons

### 2. False Equivalence
**Problem:** Treating all sources as equally credible
**Solution:** Use source hierarchy and credibility weighting

### 3. Anchoring Bias
**Problem:** Over-weighting the first source reviewed
**Solution:** Complete all extractions before synthesis; use systematic process

### 4. Confirmation Bias
**Problem:** Interpreting ambiguous evidence to support existing beliefs
**Solution:** Actively seek disconfirming evidence; document conflicts

### 5. Over-Aggregation
**Problem:** Combining incompatible findings into single statement
**Solution:** Preserve nuance; present ranges; note conditions

### 6. Source Laundering
**Problem:** AI models citing each other or common training data
**Solution:** Trace claims to primary sources where possible; weight accordingly

---

## Special Considerations for AI Sources

### AI Model Characteristics

| Model Type | Strengths | Weaknesses | Handling |
|------------|-----------|------------|----------|
| Claude | Nuanced analysis, admits uncertainty | Training cutoff | Note version/date |
| GPT-4 | Broad knowledge, structured output | May hallucinate | Cross-verify facts |
| Gemini | Recent training, web access | Varying quality | Check citations |
| Perplexity | Citations provided, web-sourced | Citation accuracy varies | Verify citations |

### When AI Models Agree

High agreement across multiple AI models suggests:
- Well-established information in training data
- OR common training source (may not indicate independent confirmation)

**Best practice:** Even with AI agreement, seek primary source verification for critical claims.

### When AI Models Disagree

Possible causes:
- Different training data or cutoff dates
- Different interpretation of ambiguous query
- One model hallucinating
- Genuinely contested topic

**Resolution:**
1. Check for factual vs interpretive disagreement
2. Verify claims against non-AI sources
3. Use more recent or specialized model as tiebreaker
4. Present both views if legitimately contested
