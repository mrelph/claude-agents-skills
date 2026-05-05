# Claude Agents & Skills Plugin Marketplace

A curated collection of specialized plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), extending Claude's capabilities with domain expertise and task automation.

## Quick Install

Add this marketplace to Claude Code with a single command:

```bash
/plugin marketplace add mrelph/claude-agents-skills
```

Once added, install any plugin individually:

```bash
/plugin install tax-preparation@mrelph/claude-agents-skills
/plugin install portfolio-analyzer@mrelph/claude-agents-skills
/plugin install hockey-lineup-builder@mrelph/claude-agents-skills
```

## Plugin Catalog

| Plugin | Description | Version | Install |
|--------|-------------|---------|---------|
| [tax-preparation](plugins/tax-preparation/) | US tax preparation: deduction analysis, RSU calculations, form processing | v2.0.0 | `/plugin install tax-preparation@mrelph/claude-agents-skills` |
| [portfolio-analyzer](plugins/portfolio-analyzer/) | Investment portfolio analysis, risk assessment, asset allocation | v3.0.0 | `/plugin install portfolio-analyzer@mrelph/claude-agents-skills` |
| [retirement-planner](plugins/retirement-planner/) | Retirement readiness, Social Security optimization, withdrawal strategies | v2.0.0 | `/plugin install retirement-planner@mrelph/claude-agents-skills` |
| [research-consolidator](plugins/research-consolidator/) | Multi-source research synthesis with confidence scoring and gap analysis | v2.0.0 | `/plugin install research-consolidator@mrelph/claude-agents-skills` |
| [hockey-lineup-builder](plugins/hockey-lineup-builder/) | Generic hockey lineup building, game strategy, special teams planning, and player management for any team | v2.0.0 | `/plugin install hockey-lineup-builder@mrelph/claude-agents-skills` |
| [second-brain](plugins/second-brain/) | Interview or ingest mode for scaffolding a personal knowledge base via the `second-brain` CLI | v0.1.0 | `/plugin install second-brain@mrelph/claude-agents-skills` |

## Plugin Details

### tax-preparation (v2.0.0)

US tax preparation and planning for individuals and families. Reads tax documents, identifies deductions, calculates liability, and handles complex situations including RSU income, self-employment, and investment taxation.

```bash
/plugin install tax-preparation@mrelph/claude-agents-skills
```

### portfolio-analyzer (v3.0.0)

Investment portfolio analysis with performance metrics, asset allocation review, risk assessment, and strategic recommendations. Produces professional-grade reports in multiple formats.

```bash
/plugin install portfolio-analyzer@mrelph/claude-agents-skills
```

### retirement-planner (v2.0.0)

Retirement readiness assessment with Social Security optimization, withdrawal strategy planning, Roth conversion analysis, and Monte Carlo simulations for longevity risk.

```bash
/plugin install retirement-planner@mrelph/claude-agents-skills
```

### research-consolidator (v2.0.0)

Synthesizes research from multiple AI models and sources into comprehensive reports. Features confidence scoring, gap analysis, and structured output formats for actionable insights.

```bash
/plugin install research-consolidator@mrelph/claude-agents-skills
```

### hockey-lineup-builder (v2.0.0)

Team-agnostic hockey coaching plugin: lineup building, formation generation, special teams planning, opponent strategy, and roster management. Ships with starter templates for `roster.md` and `team-strategy.md`, plus a worked example under `examples/jr-kraken-18u-navy/`.

```bash
/plugin install hockey-lineup-builder@mrelph/claude-agents-skills
```

### second-brain (v0.1.0)

Conversational front-end for the [`second-brain` CLI](https://github.com/mrelph/second-brain). The bundled `second-brain-init` skill conducts a brief interview — or ingests an existing folder of notes — to draft a `.second-brain.json` config and scaffold a personal knowledge base your AI assistant can maintain.

Requires the `second-brain` CLI (≥ v0.2.0) on `PATH`.

```bash
/plugin install second-brain@mrelph/claude-agents-skills
```

## Plugin Integrations

Several plugins are designed to work together, passing context and data between sessions:

- **portfolio-analyzer** feeds into **retirement-planner** — Portfolio holdings and performance inform retirement projections
- **portfolio-analyzer** feeds into **tax-preparation** — Tax-loss harvesting, cost basis, and capital gains coordination
- **retirement-planner** feeds into **tax-preparation** — Roth conversion strategies and withdrawal tax planning

## Repository Structure

```
claude-agents-skills/
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── MARKETPLACE.md               # Marketplace integration guide
├── .claude-plugin/
│   └── marketplace.json         # Machine-readable plugin catalog
├── plugins/                     # Plugin marketplace plugins (v2.0.0+)
│   ├── tax-preparation/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json      # Plugin manifest
│   │   ├── skills/
│   │   │   └── tax-preparation/ # Skill files with ${CLAUDE_PLUGIN_ROOT} paths
│   │   ├── references/          # Tax reference documents
│   │   ├── scripts/             # Python utility scripts
│   │   ├── examples/            # Sample data files
│   │   └── README.md
│   ├── portfolio-analyzer/
│   ├── retirement-planner/
│   ├── research-consolidator/
│   ├── hockey-lineup-builder/
│   └── second-brain/
├── Skills/                      # Legacy personal skills (not published to marketplace)
├── Agents/                      # Legacy personal agents (not published to marketplace)
├── staging/                     # Contribution staging area and templates
└── releases/                    # Distribution packages (pre-v2.0.0)
```

## Legacy Content

The `Skills/` and `Agents/` directories contain personal items that remain in the repository for reference but are not part of the published plugin marketplace:

- `Agents/` — Individual agent markdown files retained for reference (e.g. `claude-desktop-skills-builder`, `marketplace-manager`, `roadmap-feature-planner`, `ux-ui-design-expert`, `video-integration-specialist`)

These items are not installable via `/plugin install`. If you need them, clone the repository directly and copy the relevant files.

## Contributing

Contributions of new plugins are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full plugin format requirements and submission process.

The short version:

1. Create a directory under `plugins/your-plugin-name/`
2. Add a `plugin.json` manifest at `.claude-plugin/plugin.json`
3. Add skills under `skills/` and agents under `agents/` using `${CLAUDE_PLUGIN_ROOT}/` for all file paths
4. Add your plugin entry to `.claude-plugin/marketplace.json`
5. Open a pull request

## Marketplace Integration

For programmatic access, version checking, and advanced integration scenarios, see [MARKETPLACE.md](MARKETPLACE.md).

The `.claude-plugin/marketplace.json` file in this repository provides a machine-readable catalog of all published plugins with metadata, keywords, and version information.

## License

MIT License — Feel free to use and adapt these plugins for your own projects.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Anthropic API Documentation](https://docs.anthropic.com/en/api)
