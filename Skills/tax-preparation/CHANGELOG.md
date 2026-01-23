# Changelog - Tax Preparation Skill

All notable changes to the tax-preparation skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2025-01-22

### Added

- **RSU Calculator Script** (`scripts/rsu_calculator.py`)
  - Four subcommands: `withholding`, `lots`, `sale`, `basis`
  - Cost basis calculation from vesting records with proper FMV tracking
  - Withholding shortfall estimation comparing 22% supplemental rate to actual marginal bracket
  - Multi-lot tracking with FIFO and Specific ID lot selection methods
  - Capital gains calculation with automatic short-term vs long-term determination
  - Form 8949 adjustment generation for incorrect 1099-B cost basis
  - CSV/JSON import support for broker statement data
  - Comprehensive text and JSON output formats
- **RSU-Specific Discovery Questions**
  - 10 probing questions specifically for RSU holders
  - RSU tax trap warnings section (double taxation, withholding shortfall, holding periods, lot identification)
  - Dedicated RSU holder checklist covering documents, calculations, and tax planning
- **RSU Statement Review & Data Import**
  - Platform-specific import guidance for major brokers:
    - E*TRADE (Morgan Stanley at Work)
    - Fidelity NetBenefits
    - Charles Schwab Equity Awards
    - Morgan Stanley Shareworks
  - CSV column mapping reference table for flexible imports
  - PDF data extraction workflow for vesting confirmation statements
  - Example data extraction patterns
- **RSU Integration with Other Skills**
  - Export format for RSU holdings to portfolio-analyzer
  - Concentration risk assessment coordination
  - Export format for RSU vesting schedules to retirement-planner
  - Retirement planning scenarios for RSU income (Roth conversions, Medicare IRMAA)
  - Cross-skill command invocation examples

### Changed

- Updated skill version to 1.4.0
- Enhanced scripts/README.md with full RSU calculator documentation
- Added broker column mapping reference for CSV imports

## [1.3.0] - 2025-12-09

### Added

- **Comprehensive RSU Tax Treatment**
  - Complete guide to RSU cost basis calculation and taxation
  - RSU lifecycle explanation from grant through sale
  - Double taxation trap warning and prevention
  - Form 8949 reporting instructions for basis corrections
  - Withholding adequacy calculator guidance
  - Multi-year vesting schedule tracking framework
  - Tax planning strategies (immediate sale vs hold analysis)
- **RSU Document Extraction Templates**
  - Fields for vesting confirmations (grant date, vesting date, shares, FMV)
  - Stock plan statement parsing (shares withheld, net shares deposited)
  - 1099-B verification against vesting records
  - RSU data recording format in JSON
- **RSU Cost Basis Verification Process**
  - Step-by-step basis correction workflow
  - Adjustment calculation methodology
  - Form 8949 code "B" usage guidance
  - Holding period determination (from vesting date, not grant date)
- **RSU Red Flags Checklist**
  - 1099-B shows $0 cost basis → Correction required
  - 1099-B basis doesn't match FMV × shares → Verify and correct
  - Date acquired shows grant date instead of vesting date → Affects holding period
  - W-2 Box 1 doesn't include RSU vesting income → Contact employer
  - Multiple vesting lots sold → Track each lot's basis separately
- **Expanded investment_taxes.md Reference**
  - RSU lifecycle and tax events documentation
  - ISO, NQSO, and ESPP cost basis guidance
  - Stock compensation summary comparison table
  - Withholding strategies for stock compensation
- **New Python Scripts**
  - scripts/document_checklist_generator.py: Personalized document checklists
  - scripts/tax_savings_finder.py: Proactive opportunity identification
  - scripts/credit_eligibility_checker.py: Credit qualification analysis

### Changed

- Enhanced PDF document reading capability section with RSU-specific extraction
- Expanded "Commonly Overlooked Deductions" with stock compensation focus
- Updated "Documentation Completeness Checklist" to include RSU/stock compensation

## [1.2.0] - 2025-12-09

### Added

- **PDF Document Reading & Data Extraction**
  - Direct PDF reading capability for tax documents using Read tool
  - Extraction templates for common tax forms:
    - W-2: Wages, withholding, box 12 codes (401k, HSA)
    - 1099-INT: Interest income, early withdrawal penalties
    - 1099-DIV: Ordinary and qualified dividends, capital gains
    - 1099-B: Capital gains/losses, cost basis, holding period
    - 1099-R: Retirement distributions, taxable amounts
    - 1098: Mortgage interest, points, PMI premiums
    - 1098-T: Education expenses, scholarships
- **JSON Data Recording Format**
  - Structured data capture from extracted documents
  - Standardized format for tax year aggregation
  - Cross-document validation support
  - Totals calculation framework
- **Document Processing Workflow**
  - Step-by-step guide for handling user documents
  - User confirmation of extracted data
  - Issue identification and flagging
  - Request for additional documents based on findings
- **Multi-Document Handling**
  - Track each document separately with source identification
  - Sum totals across multiple documents (e.g., multiple W-2s)
  - Cross-reference for consistency (W-2 Box 12 vs 5498-SA)
  - Duplicate and conflict detection
- **New Reference Documents**
  - references/overlooked_deductions.md: Comprehensive missed deductions guide
  - references/investment_taxes.md: Capital gains, cost basis, wash sales
- **PDF Reading Best Practices**
  - Document format handling
  - Data validation techniques
  - Error detection and resolution

## [1.1.0] - 2025-12-09

### Added

- **US Tax Expert System Prompt**
  - Establishes authoritative tax knowledge persona
  - "You could run the IRS if you wanted to" expertise level
  - Mission-focused on maximizing legal tax reductions
- **Proactive Tax Reduction Discovery**
  - Comprehensive checklists for finding missed deductions
  - Income adjustments hunting (above-the-line deductions)
  - Itemized deductions deep dive by category
  - Credits investigation checklist
  - Self-employment opportunities identification
  - Investment tax opportunities
  - Life event trigger questions
- **13 Probing Questions**
  - Questions to uncover savings users don't mention
  - Retirement contributions, healthcare, home office, childcare
  - Education, foreign income, investments, side income
  - Student loans, 529 plans, carryforwards
- **Commonly Overlooked Deductions Tables**
  - By taxpayer type: Everyone, Homeowners, Investors, Parents, Self-Employed
  - "Why It's Missed" and "How to Find It" columns
  - Specific deduction examples with context
- **Credits People Don't Know They Qualify For**
  - Income limit table with 2024 thresholds
  - "Who Misses It" column explaining common misconceptions
  - Saver's Credit, EITC, Child Tax Credit, Lifetime Learning, Foreign Tax Credit
- **Documentation Completeness Checklist**
  - By income type (Employment, Self-Employment, Investment, Retirement, Other)
  - By deduction category (Medical, Property, Charitable, Education, Childcare)
  - Prior year documents needed (carryforwards, basis tracking)
  - Documentation red flags (large donations, home office, vehicle, medical)
- **Missing Document Resolution**
  - IRS transcript options (Wage & Income, Account)
  - Reconstruction from bank statements
  - Required vs optional documentation guidance
- **AskUserQuestion Tool Access**
  - Added to allowed-tools for proactive tax savings discovery
  - Enables clarification questions about potential deductions

### Changed

- Enhanced proactive approach: "Don't wait to be asked - investigate every potential deduction"
- Expanded questioning strategy for uncovering hidden savings
- More aggressive stance on finding overlooked opportunities

## [1.0.0] - 2025-12-09

### Added

- Initial release of tax-preparation skill
- Comprehensive tax preparation framework for individuals and families
- **Core Tax Preparation Capabilities**
  - Filing status optimization (Single, MFJ, MFS, HoH, QSS)
  - Standard vs itemized deduction analysis
  - Complete income tracking across all sources
  - Deduction identification and optimization
  - Tax credit eligibility and calculation
  - Federal and state tax preparation
- **Income Processing**
  - Wages (W-2), self-employment (1099-NEC, 1099-K)
  - Investments (1099-B, 1099-DIV, 1099-INT)
  - Retirement distributions (1099-R, SSA-1099)
  - Rental, unemployment, gambling, other income sources
- **Deduction Support**
  - Medical expenses (itemized)
  - State and local taxes (SALT cap)
  - Mortgage interest and property taxes
  - Charitable contributions
  - Above-the-line adjustments (HSA, student loan interest, IRA, etc.)
- **Tax Credit Analysis**
  - Child Tax Credit and Credit for Other Dependents
  - Earned Income Tax Credit (EITC)
  - Child and Dependent Care Credit
  - Education credits (American Opportunity, Lifetime Learning)
  - Saver's Credit
  - Residential Energy Credits
  - Premium Tax Credit (ACA)
- **Self-Employment Tax**
  - SE tax calculation (15.3% + 0.9% Medicare)
  - Business expense categories and documentation
  - Home office deduction (simplified and actual)
  - Vehicle expenses (standard mileage vs actual)
  - Quarterly estimated payments with safe harbor rules
  - Retirement contributions (SEP-IRA, Solo 401k)
- **Investment Tax Optimization**
  - Capital gains rates (0%, 15%, 20%)
  - Net Investment Income Tax (NIIT 3.8%)
  - Tax-loss harvesting strategies
  - Wash sale rule compliance
  - Long-term vs short-term holding periods
  - Capital loss carryforwards
- **State Tax Preparation**
  - Resident, part-year, non-resident filing
  - State-specific adjustments and credits
  - Multi-state income sourcing
  - Credit for taxes paid to other states
- **Tax Planning & Projections**
  - Year-end planning opportunities
  - Multi-year tax projections
  - Life event tax planning (marriage, children, home purchase, retirement)
  - Roth conversion analysis
- **Integration Capabilities**
  - Portfolio-analyzer integration for investment taxes
  - Retirement-planner integration for retirement tax strategies
  - Data exchange for tax-loss harvesting and cost basis
- **Document Generation**
  - Tax return summary (Word document)
  - Tax workpapers (Excel spreadsheet)
  - Year-over-year comparison
  - Planning recommendations
- **Python Utility Scripts**
  - scripts/filing_status_analyzer.py: Optimal status determination
  - scripts/income_calculator.py: AGI calculation
  - scripts/deduction_optimizer.py: Standard vs itemized comparison
  - scripts/credit_analyzer.py: Credit eligibility checker
  - scripts/estimated_tax_calculator.py: Quarterly payment calculation
  - scripts/capital_gains_analyzer.py: Schedule D preparation
  - scripts/tax_projector.py: Multi-year projections
  - scripts/sync_retirement_tax_data.py: Retirement-planner integration
- **Reference Documentation**
  - references/tax_brackets_deductions.md: Brackets, deductions, limits, thresholds
  - references/credits_guide.md: Detailed credit eligibility and calculations
  - references/self_employment_guide.md: Business deductions and quarterly payments
  - references/investment_taxes.md: Capital gains rules, wash sales, cost basis

### Features

- **Proactive Discovery**: Actively searches for tax savings opportunities
- **Document Processing**: Direct PDF reading for tax forms
- **Multi-Source Integration**: Coordinates with portfolio and retirement planning
- **Comprehensive Coverage**: All major tax situations (W-2, 1099s, Schedule C, Schedule D, etc.)
- **Planning Focus**: Not just preparation, but multi-year optimization

### Tool Access

- Read: PDF tax documents, reference materials
- Bash: Running Python tax calculation scripts
- WebSearch: Current year tax law research
- WebFetch: IRS.gov and state tax authority guidance
- Write: Generating tax returns and workpapers
- Task: Deep tax law research
- Skill: Invoking portfolio-analyzer and retirement-planner
- AskUserQuestion: Clarifying filing status, deductions, and tax situations
- Grep: Searching documentation
- Glob: Finding tax files

### Target Users

- Individuals and families preparing annual tax returns
- Self-employed and small business owners
- Investors with complex capital gains
- Pre-retirees planning tax-efficient strategies
- Anyone seeking tax optimization and deduction maximization

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for significant workflow or methodology changes
- MINOR version for new features or substantial capability additions
- PATCH version for bug fixes, documentation improvements, or minor enhancements

See also: SKILL.md for detailed workflow and usage instructions
