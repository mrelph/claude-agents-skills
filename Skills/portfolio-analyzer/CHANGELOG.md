# Changelog - Portfolio Analyzer Skill

All notable changes to the portfolio-analyzer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.0] - 2025-10-30

### Added

- **Enhanced Deep Research Capabilities**
  - Comprehensive financial and economic research framework
  - Five research categories:
    1. Economic Trends: Inflation, Fed policy, recession indicators, valuations
    2. Sector Deep Dives: Competitive dynamics, growth outlook, regulatory changes
    3. Portfolio-Specific: Correlation analysis, institutional positioning, strategy performance
    4. Company Analysis: Earnings, valuations, risk factors, dividend sustainability
    5. Thematic Investing: AI, ESG, demographic trends, sector rotations
  - Task agent research prompt examples for each category
  - Expanded external data sources (SEC EDGAR, Treasury.gov, BLS.gov)
  - Research best practices framework
  - Enhanced connection between research findings and portfolio implications
- **Specific Data Source Integration**
  - FRED (Federal Reserve Economic Data)
  - SEC EDGAR (Company filings and financials)
  - Treasury.gov (Government securities, economic data)
  - BLS.gov (Bureau of Labor Statistics)
  - Yahoo Finance (Market data, quotes)
  - Morningstar (Fund analysis, ratings)
- **Research Quality Guidelines**
  - Verify official sources
  - Cross-reference data points
  - Timestamp findings
  - Connect research to portfolio implications

### Changed

- Expanded Task agent usage guidance from general to category-specific
- Enhanced market context gathering section with deeper research capabilities
- Improved integration between web search and deep research workflows

## [2.2.0] - 2025-10-30

### Added

- **Project Memory Integration**
  - Track portfolio changes over time
  - Store user preferences (risk tolerance, time horizon, investment goals)
  - Track outstanding recommendations and implementation status
  - Compare new vs closed positions
  - Monitor allocation drift month-over-month
- **History Directory Structure**
  - Persistent snapshots in history/ directory
  - Month-over-month comparison logic
  - Dated metrics files (metrics_YYYY-MM-DD.json)
  - Historical trend analysis
- **Portfolio Tracking**
  - Previous analysis reference
  - Implementation status monitoring
  - Progress tracking for recommendations
  - Concentration change alerts

### Changed

- Enhanced analysis workflow to include historical context checking
- Added "Leverage historical data" to analysis principles
- Incorporated month-over-month trend tracking in monthly reviews

## [2.1.0] - 2025-10-30

### Added

- **Word Document Generation**
  - Professional portfolio analysis reports using word skill
  - Executive summary, performance tables, recommendations
  - Formatted .docx output for client sharing
- **Excel Spreadsheet Creation**
  - Multi-sheet workbooks using pandas
  - Holdings, Metrics, Performance sheets
  - Detailed data for analysis and what-if scenarios
- **Output File Naming Conventions**
  - portfolio_analysis_YYYY-MM-DD.docx for reports
  - portfolio_data_YYYY-MM-DD.xlsx for spreadsheets
  - Consistent dating and organization
- **Output Structure Guidance**
  - When to create Word vs Excel outputs
  - Content recommendations for each format
  - Professional formatting standards
- **Tool Access Expansion**
  - Added Skill tool (for word skill invocation)
  - Added Write tool (for file creation)

### Changed

- Workflow section 7 added for document generation
- Best practices updated to include output format selection

## [2.0.0] - 2025-10-30

### Major Refactor

- **Streamlined Skill Design**
  - Reduced from 360 lines to ~120 lines for token efficiency
  - Made reference documents optional (load only when needed)
  - Simplified workflow while maintaining capabilities
- **Deep Research Integration**
  - Added Task agent integration for complex analysis
  - Defined when to use Task vs WebSearch
  - Examples of research prompts for different scenarios
- **External Data Source Integration**
  - FRED for economic data
  - Morningstar for fund analysis
  - Yahoo Finance for market data
  - Financial news integration
- **Structured Output Format**
  - Standardized report structure (Executive Summary → Performance → Findings → Concerns → Recommendations → Market Context)
  - Severity levels for concerns (Critical, Important, Minor)
  - Urgency tiers for recommendations (Immediate, Near-term, Strategic)
  - Word count guidance (400-600 for monthly, 800-1200 for deep)
- **User Question Guidance**
  - Added AskUserQuestion tool to allowed-tools
  - Defined when to ask about risk tolerance, time horizon, target allocation
  - Clarification guidelines for ambiguous situations
- **Enhanced Web Search**
  - Real-time market data integration
  - Index performance tracking
  - Sector trend analysis
  - Federal Reserve policy monitoring
  - News on concentrated positions

### Changed

- Reference documents changed from required to optional
- Workflow simplified to 7 steps (from more detailed previous version)
- Analysis principles updated to emphasize historical data usage
- Made progressive disclosure of reference docs the default approach

### Removed

- Mandatory reference document loading
- Overly prescriptive workflow steps
- Redundant explanations now covered in best practices

## [1.0.0] - Initial Release

### Added

- Initial release of portfolio-analyzer skill
- Basic portfolio analysis workflow
  - PDF/CSV/screenshot data extraction
  - Metrics calculation
  - Market context gathering
  - Strategic analysis and recommendations
- **Data Extraction**
  - scripts/extract_pdf_portfolio.py for PDF statements
  - scripts/parse_csv_portfolio.py for CSV files
  - Tesseract OCR support for screenshots
  - Standardized JSON format (symbol, description, quantity, price, value, cost_basis, gain_loss)
- **Metrics Calculation**
  - scripts/calculate_portfolio_metrics.py
  - Total value, asset allocation %, concentration ratios
  - Performance/returns, risk flags
- **Market Context**
  - WebSearch integration for real-time data
  - Index performance comparison
  - Sector trends and leadership
  - Market sentiment indicators
- **Strategic Analysis**
  - Strategy identification (growth/value/income/index)
  - Concern assessment framework
  - Recommendation structuring
- **Output Structure**
  - Executive summary (2-4 sentences)
  - Performance overview with benchmark comparison
  - Key findings (3-5 bullets)
  - Concerns with severity levels
  - Recommendations by urgency
  - Market context section
- **Reference Documents**
  - references/analysis_framework.md: Concern assessment checklist
  - references/market_benchmarks.md: Benchmark construction guidance
- **Python Scripts**
  - Portfolio data extraction and parsing
  - Metrics calculation
  - Benchmark comparison
- **Tool Access**
  - Read: Loading files, PDFs, documents
  - Bash: Running Python scripts
  - WebSearch: Real-time market data
  - WebFetch: Specific URL content
  - Task: Deep research delegation
  - Skill: Related skill invocation (added in v2.1.0)
  - Write: Report creation (added in v2.1.0)
  - AskUserQuestion: Clarification (added in v2.0.0)
  - Grep, Glob: File operations

### Features

- PDF, CSV, and screenshot portfolio import
- Automated metrics calculation
- Real-time market data integration
- Benchmark comparison
- Concern identification with severity
- Actionable recommendations
- Conversational output format

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for significant workflow changes or breaking changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

Notable version jumps:
- v1.0.0 → v2.0.0: Major streamlining and deep research integration
- v2.0.0 → v2.1.0: Output generation capabilities
- v2.1.0 → v2.2.0: Project memory and historical tracking
- v2.2.0 → v2.3.0: Enhanced research framework

See also: SKILL.md for detailed workflow and usage instructions
