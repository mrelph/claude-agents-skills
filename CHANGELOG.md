# Changelog

All notable changes to the Claude Code Agents & Skills Plugin Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-03-05

### Added

- **Plugin marketplace format**: Repository is now a proper Claude Code plugin marketplace installable via `/plugin marketplace add mrelph/claude-agents-skills`
- **6 installable plugins** under `plugins/` directory, each with a `.claude-plugin/plugin.json` manifest:
  - `tax-preparation` (v2.0.0) — US tax preparation with RSU calculations merged in
  - `portfolio-analyzer` (v3.0.0) — Investment portfolio analysis and reporting
  - `retirement-planner` (v2.0.0) — Retirement readiness and Social Security optimization
  - `research-consolidator` (v2.0.0) — Multi-source research synthesis with confidence scoring
  - `kiro-spec-driven-dev` (v2.0.0) — Spec-driven development workflow
  - `dev-tools` (v1.0.0) — Bundle of 5 development agents
- **plugin.json manifests** at `.claude-plugin/plugin.json` for all 6 plugins with `name`, `description`, `version`, `author`, `repository`, `license`, and `keywords` fields
- **dev-tools agent bundle**: New plugin packaging bug-tracker-resolver, database-architect, security-code-scanner, performance-optimizer, and documentation-maintainer as a single installable unit
- **`${CLAUDE_PLUGIN_ROOT}/` path variable**: All intra-plugin file references in skill definitions now use this variable for correct path resolution after installation
- **CONTRIBUTING.md plugin guide**: Complete documentation for creating new plugins in the v2.0.0 format
- **MARKETPLACE.md v2.0.0**: Updated integration guide covering the new plugin format, manifest schema, and programmatic access patterns

### Changed

- **Restructured repository**: Primary content moved from `Skills/` and `Agents/` into `plugins/` with proper plugin manifests
- **RSU content merged into tax-preparation**: Amazon RSU tax calculations skill content consolidated into the `tax-preparation` plugin (was previously a separate `amazon-rsu-tax-calculations` skill)
- **marketplace.json schema updated**: Root catalog now uses the official plugin marketplace format (`plugins` array with `source` paths) instead of the legacy `categories.agents` / `categories.skills` nested structure
- **Plugin versions bumped** to reflect the structural migration and RSU merge:
  - tax-preparation: v1.4.0 → v2.0.0
  - portfolio-analyzer: v2.3.0 → v3.0.0
  - retirement-planner: v1.0.0 → v2.0.0
  - research-consolidator: v1.0.0 → v2.0.0
  - kiro-spec-driven-dev: v1.0.0 → v2.0.0
- **README.md rewritten** for plugin marketplace experience with quick install command, plugin catalog table, and per-plugin install examples
- **CONTRIBUTING.md rewritten** to document the plugin format, `${CLAUDE_PLUGIN_ROOT}` requirements, and validation steps

### Removed

- **Root `.claude-plugin/` directory**: Replaced by per-plugin `.claude-plugin/` directories under `plugins/`
- **Legacy `marketplace.json` nested category structure**: Root `marketplace.json` now uses the flat `plugins` array format; the old `categories.agents` / `categories.skills` / `integrations` / `stats` structure is gone
- **`jr-kraken-18u-navy-lineup` from published plugins**: This personal-use skill is no longer part of the installable plugin catalog (remains in `Skills/` for reference)

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

The marketplace version (currently 2.0.0) tracks major changes to the marketplace infrastructure, plugin format, and significant additions/changes across multiple components.

### Individual Plugin Versions

Each plugin maintains its own semantic version tracked in its `.claude-plugin/plugin.json` manifest:

- **tax-preparation**: v2.0.0 (plugin format migration, RSU content merged in)
- **portfolio-analyzer**: v3.0.0 (plugin format migration, enhanced reporting)
- **retirement-planner**: v2.0.0 (plugin format migration)
- **research-consolidator**: v2.0.0 (plugin format migration)
- **kiro-spec-driven-dev**: v2.0.0 (plugin format migration)
- **dev-tools**: v1.0.0 (initial release as agent bundle)

### Link References

[Unreleased]: https://github.com/mrelph/claude-agents-skills/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/mrelph/claude-agents-skills/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/mrelph/claude-agents-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mrelph/claude-agents-skills/releases/tag/v1.0.0
