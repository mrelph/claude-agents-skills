# Changelog - Research Consolidator Skill

All notable changes to the research-consolidator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-09

### Added

- Initial release of research-consolidator skill
- Multi-source research consolidation framework
  - Support for AI model outputs (Claude, GPT, Gemini, Perplexity)
  - Web research summaries and search results
  - Document analyses (PDFs, reports, papers)
  - Data extracts and spreadsheets
  - Expert interviews and notes
- Source intake and registration system
  - Structured source metadata tracking
  - Credibility weighting
  - Source type classification
- Content extraction and parsing
  - Automated claim extraction
  - Evidence linking
  - Conclusion and recommendation capture
  - Uncertainty tracking
- Cross-source analysis capabilities
  - Claim alignment matrix
  - Conflict identification and resolution
  - Confidence scoring system (0.0-1.0 scale)
  - Research gap identification
- Comprehensive synthesis framework
  - Consolidation rules for agreement levels
  - Conflict resolution strategies
  - Unique finding preservation
- Report generation
  - Executive summary format
  - Detailed findings with confidence levels
  - Conflict documentation
  - Research gap analysis
  - Full source attribution
  - Multiple output formats (Markdown, JSON)
- Quality assurance validation
  - Automated report checks
  - Source verification
  - Citation completeness validation
- Python utility scripts
  - source_parser.py: Structured content extraction
  - claim_alignment.py: Cross-source claim mapping
  - gap_analyzer.py: Research gap identification
  - report_generator.py: Final report creation
  - report_validator.py: Quality assurance checks
- Comprehensive reference documentation
  - Source type handling guidelines
  - Conflict resolution decision trees
  - Confidence scoring methodology
  - Output format templates

### Features

- **Source Type Handling**: Specialized handling for AI models, web research, and documents
- **Confidence Scoring**: Four-factor scoring system (agreement, evidence quality, credibility, recency)
- **Conflict Resolution**: Six resolution strategies with decision tree guidance
- **Gap Identification**: Five gap types (topic, source, depth, temporal, perspective)
- **Multiple Output Formats**: Executive reports, comparison matrices, findings summaries, data exports

### Tool Access

- Read: Source file loading and parsing
- Bash: Running Python consolidation scripts
- WebSearch: Verifying claims when needed
- WebFetch: Accessing online sources
- Write: Generating final reports
- Task: Delegating deep analysis
- Skill: Invoking related research skills
- AskUserQuestion: Clarifying conflicts and priorities

### Target Users

- Researchers synthesizing multi-source findings
- Analysts consolidating competitive intelligence
- Decision-makers requiring comprehensive research summaries
- Teams coordinating research from multiple AI tools

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for incompatible workflow changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

See also: SKILL.md for detailed workflow and usage instructions
