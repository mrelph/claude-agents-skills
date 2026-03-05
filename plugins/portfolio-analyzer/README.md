# Portfolio Analyzer Skill

**Version:** 2.3.0
**Last Updated:** 2025-10-30

A comprehensive investment portfolio analysis skill for Claude Code that extracts data from statements, calculates performance metrics, compares against benchmarks, and generates strategic recommendations.

## Overview

The Portfolio Analyzer skill helps you:
- Extract holdings from PDFs, CSVs, or screenshots
- Calculate portfolio health indicators and performance metrics
- Gather real-time market context via web search
- Perform deep research on economic trends, sectors, and individual holdings
- Generate strategic recommendations with severity levels
- Track portfolio changes month-over-month
- Create professional Word and Excel reports

## Directory Structure

```
portfolio-analyzer/
├── SKILL.md                 # Main skill definition
├── README.md                # This file
├── references/
│   ├── analysis_framework.md   # Comprehensive analysis checklist
│   └── market_benchmarks.md    # Benchmark comparison guidance
├── scripts/
│   ├── extract_pdf_portfolio.py      # Extract holdings from PDF statements
│   ├── parse_csv_portfolio.py        # Parse CSV portfolio files
│   └── calculate_portfolio_metrics.py # Calculate portfolio metrics
├── data/                    # Working data directory (created as needed)
└── history/                 # Historical snapshots for tracking changes
```

## Quick Start

### Basic Usage

1. **Invoke the skill** when you need portfolio analysis:
   - "Analyze my portfolio" (with PDF/CSV attached)
   - "Review my investment holdings"
   - "Do you have any concerns with my portfolio?"
   - "Compare my investment strategy to current market trends"

2. **Provide portfolio data** via:
   - PDF brokerage statements
   - CSV export files
   - Screenshots of holdings
   - Manual list of positions

3. **Receive analysis** including:
   - Executive summary
   - Performance overview with benchmark comparison
   - Key findings and concerns (with severity levels)
   - Prioritized recommendations (immediate → near-term → strategic)
   - Market context and forward considerations

### Example Queries

- "Analyze this Fidelity statement and tell me if I'm too concentrated"
- "How does my portfolio compare to the S&P 500 this year?"
- "Review my holdings for tax-loss harvesting opportunities"
- "Is my asset allocation appropriate for someone 10 years from retirement?"

## Scripts

### extract_pdf_portfolio.py

Extracts holdings from PDF brokerage statements.

```bash
python scripts/extract_pdf_portfolio.py <file.pdf> > holdings.json
```

**Output fields:** symbol, description, quantity, price, value, cost_basis, gain_loss

### parse_csv_portfolio.py

Parses CSV portfolio exports from various brokerages.

```bash
python scripts/parse_csv_portfolio.py <file.csv> > holdings.json
```

### calculate_portfolio_metrics.py

Computes portfolio health indicators from holdings data.

```bash
python scripts/calculate_portfolio_metrics.py holdings.json > metrics.json
```

**Key metrics calculated:**
- Total portfolio value
- Asset allocation percentages
- Concentration ratios
- Performance/returns
- Risk flags

## Reference Documents

### analysis_framework.md

Comprehensive framework for portfolio analysis covering:
- Asset allocation analysis (equity/fixed income/cash, market cap, geographic, sector)
- Concentration and diversification metrics
- Investment strategy identification (growth, value, income, index)
- Risk assessment dimensions
- Strategic recommendation framework
- Common portfolio concerns checklist
- Monthly review structure

**When to use:** For systematic concern assessments or comprehensive evaluations.

### market_benchmarks.md

Guidance on benchmark selection and comparison including:
- Index selection by portfolio type
- Benchmark construction for blended portfolios
- Performance attribution methods

**When to use:** When you need specific benchmark guidance or index selection help.

## Key Features

### Deep Research Integration

The skill uses Task agents for comprehensive research on:
- **Economic trends:** Inflation, Fed policy, recession indicators
- **Sector analysis:** Competitive dynamics, growth outlook, regulatory changes
- **Company fundamentals:** Earnings, valuations, risk factors
- **Thematic research:** AI, ESG, demographic trends

### Month-over-Month Tracking

Save portfolio snapshots to track changes over time:

```bash
mkdir -p history
python scripts/calculate_portfolio_metrics.py holdings.json > history/metrics_$(date +%Y-%m-%d).json
```

The skill tracks:
- Portfolio composition changes
- New and closed positions
- Allocation drift
- Recommendation implementation status

### Output Generation

- **Word reports:** Professional documents via word skill for monthly reviews
- **Excel spreadsheets:** Multi-sheet workbooks for detailed data analysis
- **Naming convention:** `portfolio_analysis_YYYY-MM-DD.docx` / `portfolio_data_YYYY-MM-DD.xlsx`

## Integration

### With Retirement Planner

Portfolio data can be consumed by the retirement-planner skill:

```bash
cp holdings.json ../retirement-planner/data/current_portfolio.json
```

### With Tax Preparation

Coordinate with tax-preparation skill for:
- Tax-loss harvesting opportunities
- Cost basis tracking
- Tax-efficient positioning recommendations

## Allowed Tools

- `Read` - Read portfolio documents and reference files
- `Bash` - Run Python analysis scripts
- `WebSearch` - Real-time market data and news
- `WebFetch` - Detailed financial information
- `Grep`, `Glob` - Search files and documents
- `Task` - Deep research via specialized agents
- `Skill` - Integration with word, tax-preparation, retirement-planner
- `Write` - Save analysis results and reports
- `AskUserQuestion` - Clarify risk tolerance, time horizon, targets

## When to Ask User Questions

The skill will ask for clarification about:
- **Risk tolerance** - When making rebalancing recommendations
- **Time horizon** - When volatility considerations matter
- **Target allocation** - When rebalancing opportunities exist
- **Ambiguous data** - When portfolio information is unclear

## Limitations

This skill provides analytical frameworks but doesn't replace professional financial advice. Consider:
- Individual circumstances, time horizon, and risk tolerance
- Market data reflects point-in-time conditions
- Automated checks catch mechanical issues but not subtle risks like correlations or liquidity constraints

## Version History

### v2.3.0 (2025-10-30)
- Enhanced deep research capabilities with comprehensive financial/economic research framework
- Added 5 categories of research: Economic Trends, Sector Deep Dives, Portfolio-Specific, Company Analysis, Thematic Investing
- Expanded external data sources (SEC EDGAR, Treasury.gov, BLS.gov)
- Added research best practices framework

### v2.2.0 (2025-10-30)
- Added project memory integration for tracking portfolio changes over time
- Added history directory structure for persistent snapshots
- Track user preferences (risk tolerance, time horizon, goals)

### v2.1.0 (2025-10-30)
- Added Word document generation using word skill
- Added Excel spreadsheet creation for detailed data analysis
- Added Skill and Write tools to allowed-tools

### v2.0.0 (2025-10-30)
- Streamlined skill from 360 to ~120 lines for token efficiency
- Added deep research capabilities with Task agent integration
- Added external data source integration
- Made reference documents optional to reduce context usage

### v1.0.0 (Initial)
- Basic portfolio analysis workflow
- PDF/CSV/screenshot extraction
- Metrics calculation and strategic recommendations
