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
/plugin install dev-tools@mrelph/claude-agents-skills
```

## Plugin Catalog

| Plugin | Description | Version | Install |
|--------|-------------|---------|---------|
| [tax-preparation](plugins/tax-preparation/) | US tax preparation: deduction analysis, RSU calculations, form processing | v2.0.0 | `/plugin install tax-preparation@mrelph/claude-agents-skills` |
| [portfolio-analyzer](plugins/portfolio-analyzer/) | Investment portfolio analysis, risk assessment, asset allocation | v3.0.0 | `/plugin install portfolio-analyzer@mrelph/claude-agents-skills` |
| [retirement-planner](plugins/retirement-planner/) | Retirement readiness, Social Security optimization, withdrawal strategies | v2.0.0 | `/plugin install retirement-planner@mrelph/claude-agents-skills` |
| [research-consolidator](plugins/research-consolidator/) | Multi-source research synthesis with confidence scoring and gap analysis | v2.0.0 | `/plugin install research-consolidator@mrelph/claude-agents-skills` |
| [kiro-spec-driven-dev](plugins/kiro-spec-driven-dev/) | Spec-driven development: requirements to design to tasks workflow | v2.0.0 | `/plugin install kiro-spec-driven-dev@mrelph/claude-agents-skills` |
| [dev-tools](plugins/dev-tools/) | Bundle of 5 development agents: bug tracking, DB architecture, security scanning, performance, documentation | v1.0.0 | `/plugin install dev-tools@mrelph/claude-agents-skills` |

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

### kiro-spec-driven-dev (v2.0.0)

Structured spec-driven development workflow using Kiro methodology. Transforms feature ideas into formal requirements documents, design specifications, and implementation task lists.

```bash
/plugin install kiro-spec-driven-dev@mrelph/claude-agents-skills
```

### dev-tools (v1.0.0)

A bundled collection of 5 specialized development agents:

- **bug-tracker-resolver** — Bug management, root cause analysis, resolution planning
- **database-architect** — PostgreSQL/Supabase schema design, query optimization, RLS policies
- **security-code-scanner** — Vulnerability identification, OWASP Top 10 analysis
- **performance-optimizer** — Core Web Vitals, bundle size reduction, runtime efficiency
- **documentation-maintainer** — READMEs, API docs, user guides, documentation consistency

```bash
/plugin install dev-tools@mrelph/claude-agents-skills
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
├── marketplace.json             # Machine-readable plugin catalog
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
│   ├── kiro-spec-driven-dev/
│   └── dev-tools/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── agents/              # Agent definitions
├── Skills/                      # Legacy personal skills (not published to marketplace)
├── Agents/                      # Legacy personal agents (not published to marketplace)
├── staging/                     # Contribution staging area and templates
└── releases/                    # Distribution packages (pre-v2.0.0)
```

## Legacy Content

The `Skills/` and `Agents/` directories contain personal items that remain in the repository for reference but are not part of the published plugin marketplace:

- `Skills/jr-kraken-18u-navy-lineup/` — Hockey lineup generator (personal use)
- `Agents/` — Individual agent markdown files (superseded by plugins/dev-tools)

These items are not installable via `/plugin install`. If you need them, clone the repository directly and copy the relevant files.

## Contributing

Contributions of new plugins are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full plugin format requirements and submission process.

The short version:

1. Create a directory under `plugins/your-plugin-name/`
2. Add a `plugin.json` manifest at `.claude-plugin/plugin.json`
3. Add skills under `skills/` and agents under `agents/` using `${CLAUDE_PLUGIN_ROOT}/` for all file paths
4. Add your plugin entry to `marketplace.json`
5. Open a pull request

## Marketplace Integration

For programmatic access, version checking, and advanced integration scenarios, see [MARKETPLACE.md](MARKETPLACE.md).

The `marketplace.json` file at the root of this repository provides a machine-readable catalog of all published plugins with metadata, keywords, and version information.

## License

MIT License — Feel free to use and adapt these plugins for your own projects.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Anthropic API Documentation](https://docs.anthropic.com/en/api)
