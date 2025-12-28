# Changelog

All notable changes to the Claude Code Agents & Skills Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-12-28

### Added

- **Slash Command Support for Skills**: Skills can now be invoked using custom slash commands (e.g., `/tax-prep`, `/portfolio`) for faster access in Claude Code conversations
  - Added `get_slash_command_input()` function to add-to-marketplace.py
  - Marketplace entries now support optional `slash_command` field
  - Interactive workflow prompts for slash command configuration during skill addition
- **kiro-spec-driven-development skill** (v1.0.0): Structured spec-driven development workflow that transforms feature ideas into requirements, design documents, and implementation plans using Kiro methodology
  - Complete three-phase workflow: Requirements → Design → Tasks
  - Parallel execution support for faster iteration
  - Specialized sub-agents for each phase
  - Integration with Claude Code's TodoWrite tool
- **marketplace-manager agent** (v1.0.0): Automates adding new agents and skills to the Claude Code marketplace from staging directory
  - Streamlines contribution workflow
  - Validates entries and updates marketplace.json files
  - Works alongside existing add-to-marketplace.py script
- **Staging Workflow**: New contribution workflow with templates and automation
  - Agent and skill templates in staging/ directory
  - Automated processing with marketplace-manager agent
  - Clear contribution guidelines in documentation

### Changed

- **Agent Directory Structure**: Restructured agents into individual directories for plugin compatibility
  - Each agent now has its own directory (e.g., `Agents/database-architect/`)
  - Agent markdown files moved into subdirectories
  - Maintains backward compatibility with existing installations
- **marketplace.json Schema**: Multiple schema updates to meet Claude Code official requirements
  - Fixed plugin structure and metadata fields
  - Added proper category classifications
  - Improved keyword organization
  - Both root and .claude-plugin/ marketplace.json files stay synchronized
- **Documentation**: Updated contribution documentation to mention marketplace-manager agent option
  - README.md includes both automated and manual workflows
  - CONTRIBUTING.md enhanced with clearer guidelines

### Fixed

- marketplace.json schema compliance with Claude Code requirements
- Plugin marketplace directory structure (.claude-plugin/)
- Marketplace catalog and CLI for programmatic access

## [1.0.0] - 2025-12-09

### Added

- **Initial marketplace release** with 9 agents and 6 skills
- **Agents** (v1.0.0):
  - bug-tracker-resolver: Bug management and resolution
  - database-architect: PostgreSQL/Supabase expertise
  - documentation-maintainer: Documentation creation and maintenance
  - performance-optimizer: Web performance optimization
  - roadmap-feature-planner: Strategic feature planning
  - security-code-scanner: Security vulnerability analysis
  - ux-ui-design-expert: UX/UI design guidance
  - video-integration-specialist: Video streaming integration
  - marketplace-manager: Marketplace automation
- **Skills**:
  - research-consolidator (v1.0.0): Multi-source research synthesis
  - tax-preparation (v1.3.0): US tax preparation and planning
  - portfolio-analyzer (v2.3.0): Investment portfolio analysis
  - retirement-planner (v1.0.0): Pre-retirement planning
  - jr-kraken-18u-navy-lineup (v1.0.0): Hockey team lineup generation
  - kiro-spec-driven-development (v1.0.0): Spec-driven development workflow
- **Marketplace Infrastructure**:
  - marketplace.json catalog with complete metadata
  - marketplace-cli.py for browsing and installation
  - Plugin marketplace support (.claude-plugin/ directory)
  - Programmatic API for integration
- **Documentation**:
  - Comprehensive README.md with usage examples
  - MARKETPLACE.md integration guide
  - CONTRIBUTING.md for contributors
  - Individual README files for all agents and skills
  - Agents/README.md and Skills/README.md overview documents

### Infrastructure

- Git repository with MIT license
- GitHub repository setup
- Semantic versioning for all components
- Consistent directory structure across agents and skills

---

## Version History Notes

### Marketplace Version (Root)

The marketplace version (currently 1.1.0) tracks major changes to the marketplace infrastructure, tooling, and significant additions/changes across multiple components.

### Individual Component Versions

Each agent and skill maintains its own semantic version:

- **Agents**: Currently all at v1.0.0 (initial stable releases)
- **Skills**: Individual version histories documented in each SKILL.md file
  - tax-preparation: v1.3.0 (RSU support, PDF reading, proactive tax discovery)
  - portfolio-analyzer: v2.3.0 (deep research, project memory, Word/Excel output)
  - retirement-planner: v1.0.0 (initial release)
  - research-consolidator: v1.0.0 (initial release)
  - jr-kraken-18u-navy-lineup: v1.0.0 (initial release)
  - kiro-spec-driven-development: v1.0.0 (initial release)

### Link References

[Unreleased]: https://github.com/mrelph/claude-agents-skills/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/mrelph/claude-agents-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mrelph/claude-agents-skills/releases/tag/v1.0.0
