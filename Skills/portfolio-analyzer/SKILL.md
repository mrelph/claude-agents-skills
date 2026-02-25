---
name: portfolio-analyzer
description: This skill should be used when the user asks to "analyze my portfolio", "review my investments", "check my asset allocation", "how is my portfolio performing", "what should I rebalance", "compare to benchmarks", or provides brokerage statements, holdings CSVs, portfolio PDFs, or screenshots. Also triggered by mentions of portfolio risk, concentration, diversification, sector allocation, or investment performance metrics.
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Task, Skill, Write, AskUserQuestion
metadata:
  version: 2.3.0
  last-updated: 2025-10-30
---

# Portfolio Analyzer

Comprehensive analysis of investment portfolios by extracting data from statements, calculating performance metrics, comparing against benchmarks, and generating strategic recommendations.

## Workflow

### 1. Data Extraction & Normalization

Extract holdings from PDFs, CSVs, or screenshots into standardized JSON format.

**Scripts**:
- `python scripts/extract_pdf_portfolio.py <file.pdf> > holdings.json` - Extract from PDF statements
- `python scripts/parse_csv_portfolio.py <file.csv> > holdings.json` - Parse CSV files
- Use Tesseract OCR for screenshots, then process extracted text

**Validation**: Check scripts exist with `ls scripts/*.py`. If missing, create them or work manually.

**Target JSON fields**: symbol, description, quantity, price, value, cost_basis, gain_loss

### 2. Calculate Metrics

Compute portfolio health indicators:

```bash
python scripts/calculate_portfolio_metrics.py holdings.json > metrics.json
```

**Key metrics**: Total value, asset allocation %, concentration ratios, performance/returns, risk flags

### 3. Gather Market Context & Deep Research

**Use WebSearch for real-time market data**:
- Index performance (S&P 500, Russell 2000, Nasdaq, sector indices)
- Sector trends and leadership (growth vs value, cyclical vs defensive)
- Federal Reserve policy, interest rates, and monetary policy outlook
- News on concentrated positions and individual holdings
- Current market sentiment and volatility (VIX, fear/greed indicators)

**Use Task agent for deep research** (`subagent_type=Explore` or `general-purpose`):

Deploy for complex analysis requiring synthesis of multiple sources:
- Economic trends (inflation, Fed policy, recession indicators, valuations)
- Sector/industry analysis (competitive dynamics, growth outlook, regulatory changes)
- Portfolio-specific (correlation analysis, institutional positioning, strategy performance)
- Company fundamentals (earnings, valuations, risk factors, dividend sustainability)
- Thematic research (AI, ESG, demographic trends, sector rotations)

**Key data sources**: FRED, SEC EDGAR, Treasury.gov, BLS.gov, Yahoo Finance, Morningstar, financial news

**Best practices**: Verify official sources, cross-reference data, timestamp findings, connect to portfolio implications

### 4. Strategic Analysis

Match analysis to user's question type:

**Strategy vs market trends**: Identify portfolio strategy (growth/value/income/index), compare to current market dynamics, explain alignment implications

**Concern assessment**: Use `references/analysis_framework.md` checklist - evaluate concentration, diversification, risk levels, inefficiencies, tax implications. Provide context and severity

**Recommendations**: Structure by urgency (immediate → near-term → strategic). Always explain reasoning

### 5. Deliver Insights

**Standard output structure**:

1. **Executive Summary** (2-4 sentences) - Direct answer to user's question
2. **Performance Overview** - Value, returns, benchmark comparison, attribution, market context
3. **Key Findings** (3-5 bullets) - Strengths, concerns, trends, opportunities
4. **Concerns** (if any) - Critical/Important/Minor severity with mitigation steps
5. **Recommendations** - By urgency: immediate (this week), near-term (this month), strategic (ongoing)
6. **Market Context** - Current environment, portfolio positioning, forward considerations

**Format**: Clear headings, bullet points, bold key metrics, conversational tone, 400-600 words (monthly reviews) or 800-1200 words (deep analysis)

### 6. Track Portfolio History

**Project memory tracking**:
- Portfolio composition, user preferences (risk tolerance, time horizon, goals)
- Previous recommendations and implementation status
- Month-over-month performance and concentration changes

**History snapshots**: Save to `history/` directory:
```bash
mkdir -p history
python scripts/calculate_portfolio_metrics.py holdings.json > history/metrics_$(date +%Y-%m-%d).json
```

**Monthly comparison**: Load previous snapshot, calculate value changes, identify new/closed positions, track allocation drift, update project memory

### 7. Generate Output Documents

**Word reports**: Use word skill (`Skill command: "word"`) for monthly reviews, comprehensive reports, or formal presentations. Creates formatted .docx with executive summary, performance tables, and recommendations.

**Excel spreadsheets**: Use pandas to create multi-sheet workbooks (Holdings, Metrics, Performance) for detailed data, tracking, or what-if analysis.

**Naming**: `portfolio_analysis_YYYY-MM-DD.docx` / `portfolio_data_YYYY-MM-DD.xlsx`

## Reference Documents (Load ONLY if needed)

**IMPORTANT**: Only load these when the necessary domain knowledge is lacking for the specific question.

**`references/analysis_framework.md`** - Load ONLY when user explicitly asks for concern assessment or needs systematic evaluation checklist

**`references/market_benchmarks.md`** - Load ONLY when specific benchmark construction guidance is needed or the appropriate index is unclear

Most analyses can be completed without loading these documents. Use your existing knowledge of portfolio analysis principles.

## Analysis Principles

- Balance quantitative rigor with strategic judgment
- Match depth to user's question (tactical vs comprehensive)
- Prioritize authoritative sources for market data
- Connect insights to actionable implications
- **Leverage historical data** - Always check project memory and history files for context on previous analyses
- Track month-over-month trends for regular reviews
- Acknowledge uncertainty and tradeoffs

## When to Ask User Questions

Use the AskUserQuestion tool to clarify critical context before analysis:

**Ask about risk tolerance when**:
- Making rebalancing recommendations
- Evaluating whether concentration is excessive
- Suggesting portfolio adjustments

**Ask about time horizon when**:
- Unclear if this is short-term (<5 years) or long-term investing
- Volatility considerations matter for recommendations
- Asset allocation guidance is needed

**Ask about target allocation when**:
- User mentions "drift" but no targets are evident
- Rebalancing opportunities exist but targets are unknown
- Multiple valid allocation strategies could apply

**Ask for clarification when**:
- Portfolio data is ambiguous (unclear symbols, missing info)
- User's question could be interpreted multiple ways
- Critical assumptions would significantly impact recommendations

## Limitations

This skill provides analytical frameworks but doesn't replace professional financial advice. Consider individual circumstances, time horizon, risk tolerance, and life goals. Market data reflects point-in-time conditions. Automated checks catch mechanical issues but not subtle risks like correlations or liquidity constraints.

