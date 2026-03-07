# Plugin Marketplace Evolution Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Evolve claude-agents-skills from a skill/agent catalog into a proper Claude Code/Cowork plugin marketplace with 6 installable plugins.

**Architecture:** Create a `plugins/` directory with 6 self-contained plugin subdirectories, each following the official `.claude-plugin/plugin.json` format. Migrate existing skill content, update paths to use `${CLAUDE_PLUGIN_ROOT}`, and replace the marketplace catalog with the official schema.

**Tech Stack:** JSON (manifests), Markdown (skills/agents), Python (scripts/tooling), Git

---

### Task 1: Create Plugin Directory Structure

**Files:**
- Create: `plugins/tax-preparation/.claude-plugin/` (dir)
- Create: `plugins/tax-preparation/skills/tax-preparation/` (dir)
- Create: `plugins/portfolio-analyzer/.claude-plugin/` (dir)
- Create: `plugins/portfolio-analyzer/skills/portfolio-analyzer/` (dir)
- Create: `plugins/retirement-planner/.claude-plugin/` (dir)
- Create: `plugins/retirement-planner/skills/retirement-planner/` (dir)
- Create: `plugins/research-consolidator/.claude-plugin/` (dir)
- Create: `plugins/research-consolidator/skills/research-consolidator/` (dir)
- Create: `plugins/kiro-spec-driven-dev/.claude-plugin/` (dir)
- Create: `plugins/kiro-spec-driven-dev/skills/kiro-spec-driven-dev/` (dir)
- Create: `plugins/dev-tools/.claude-plugin/` (dir)
- Create: `plugins/dev-tools/agents/` (dir)

**Step 1: Create all plugin directory scaffolds**

```bash
cd /mnt/c/Coding/claude-agents-skills
mkdir -p plugins/tax-preparation/.claude-plugin
mkdir -p plugins/tax-preparation/skills/tax-preparation
mkdir -p plugins/portfolio-analyzer/.claude-plugin
mkdir -p plugins/portfolio-analyzer/skills/portfolio-analyzer
mkdir -p plugins/retirement-planner/.claude-plugin
mkdir -p plugins/retirement-planner/skills/retirement-planner
mkdir -p plugins/research-consolidator/.claude-plugin
mkdir -p plugins/research-consolidator/skills/research-consolidator
mkdir -p plugins/kiro-spec-driven-dev/.claude-plugin
mkdir -p plugins/kiro-spec-driven-dev/skills/kiro-spec-driven-dev
mkdir -p plugins/dev-tools/.claude-plugin
mkdir -p plugins/dev-tools/agents
```

**Step 2: Verify structure**

Run: `find plugins -type d | sort`
Expected: All 12+ directories created

**Step 3: Commit**

```bash
git add plugins/
git commit -m "scaffold: create plugin directory structure for 6 plugins"
```

---

### Task 2: Create Plugin Manifests (plugin.json)

**Files:**
- Create: `plugins/tax-preparation/.claude-plugin/plugin.json`
- Create: `plugins/portfolio-analyzer/.claude-plugin/plugin.json`
- Create: `plugins/retirement-planner/.claude-plugin/plugin.json`
- Create: `plugins/research-consolidator/.claude-plugin/plugin.json`
- Create: `plugins/kiro-spec-driven-dev/.claude-plugin/plugin.json`
- Create: `plugins/dev-tools/.claude-plugin/plugin.json`

**Step 1: Create tax-preparation/plugin.json**

```json
{
  "name": "tax-preparation",
  "description": "US tax preparation: deduction analysis, RSU calculations, form processing, and tax optimization",
  "version": "2.0.0",
  "author": { "name": "mrelph" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["tax", "finance", "deductions", "RSU", "IRS", "W-2", "1099"]
}
```

**Step 2: Create portfolio-analyzer/plugin.json**

```json
{
  "name": "portfolio-analyzer",
  "description": "Investment portfolio analysis, risk assessment, asset allocation, and strategic recommendations",
  "version": "3.0.0",
  "author": { "name": "mrelph" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["investing", "portfolio", "finance", "analysis", "risk"]
}
```

**Step 3: Create retirement-planner/plugin.json**

```json
{
  "name": "retirement-planner",
  "description": "Retirement readiness assessment, Social Security optimization, and withdrawal strategies",
  "version": "2.0.0",
  "author": { "name": "mrelph" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["retirement", "social-security", "401k", "finance", "planning"]
}
```

**Step 4: Create research-consolidator/plugin.json**

```json
{
  "name": "research-consolidator",
  "description": "Synthesize research from multiple AI models and sources with confidence scoring and gap analysis",
  "version": "2.0.0",
  "author": { "name": "mrelph" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["research", "synthesis", "analysis", "multi-source", "consolidation"]
}
```

**Step 5: Create kiro-spec-driven-dev/plugin.json**

```json
{
  "name": "kiro-spec-driven-dev",
  "description": "Structured spec-driven development: Requirements to Design to Tasks workflow",
  "version": "2.0.0",
  "author": { "name": "mrelph" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["development", "methodology", "specs", "planning", "kiro"]
}
```

**Step 6: Create dev-tools/plugin.json**

```json
{
  "name": "dev-tools",
  "description": "Development agents: bug tracking, DB architecture, security scanning, performance optimization, documentation",
  "version": "1.0.0",
  "author": { "name": "mrelph" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["development", "debugging", "security", "performance", "database", "documentation"]
}
```

**Step 7: Commit**

```bash
git add plugins/*/. claude-plugin/plugin.json
git commit -m "feat: add plugin.json manifests for all 6 plugins"
```

---

### Task 3: Migrate tax-preparation Plugin

This is the most complex migration — it merges the main tax skill with amazon-rsu-tax-calculations content.

**Files:**
- Copy: `Skills/tax-preparation/SKILL.md` → `plugins/tax-preparation/skills/tax-preparation/SKILL.md`
- Copy: `Skills/tax-preparation/scripts/` → `plugins/tax-preparation/scripts/`
- Copy: `Skills/tax-preparation/references/` → `plugins/tax-preparation/references/`
- Copy: `Skills/tax-preparation/examples/` → `plugins/tax-preparation/examples/`
- Copy: `Skills/tax-preparation/README.md` → `plugins/tax-preparation/README.md`
- Copy: `Skills/amazon-rsu-tax-calculations/scripts/` → `plugins/tax-preparation/scripts/rsu/`
- Copy: `Skills/amazon-rsu-tax-calculations/references/` → `plugins/tax-preparation/references/rsu/`
- Copy: `Skills/amazon-rsu-tax-calculations/examples/` → `plugins/tax-preparation/examples/`
- Modify: `plugins/tax-preparation/skills/tax-preparation/SKILL.md` (update paths)

**Step 1: Copy tax-preparation files**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp Skills/tax-preparation/SKILL.md plugins/tax-preparation/skills/tax-preparation/SKILL.md
cp -r Skills/tax-preparation/scripts plugins/tax-preparation/scripts
cp -r Skills/tax-preparation/references plugins/tax-preparation/references
cp -r Skills/tax-preparation/examples plugins/tax-preparation/examples
cp Skills/tax-preparation/README.md plugins/tax-preparation/README.md
```

**Step 2: Copy RSU files into tax-preparation plugin (namespaced under rsu/)**

```bash
mkdir -p plugins/tax-preparation/scripts/rsu
mkdir -p plugins/tax-preparation/references/rsu
cp Skills/amazon-rsu-tax-calculations/scripts/*.py plugins/tax-preparation/scripts/rsu/
cp Skills/amazon-rsu-tax-calculations/references/*.md plugins/tax-preparation/references/rsu/
cp Skills/amazon-rsu-tax-calculations/examples/*.json plugins/tax-preparation/examples/
```

**Step 3: Update SKILL.md paths to use `${CLAUDE_PLUGIN_ROOT}`**

In `plugins/tax-preparation/skills/tax-preparation/SKILL.md`, replace ALL relative paths:
- `scripts/` → `${CLAUDE_PLUGIN_ROOT}/scripts/`
- `references/` → `${CLAUDE_PLUGIN_ROOT}/references/`
- `examples/` → `${CLAUDE_PLUGIN_ROOT}/examples/`

Use sed or manual edit. There are 15+ path references to update. Key patterns:
- `python3 scripts/tax_calculator.py` → `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/tax_calculator.py`
- `Read references/form_processing.md` → `Read ${CLAUDE_PLUGIN_ROOT}/references/form_processing.md`
- `python3 scripts/rsu_calculator.py` → `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rsu_calculator.py`

Also add a note about RSU scripts being available at `${CLAUDE_PLUGIN_ROOT}/scripts/rsu/`.

**Step 4: Verify file count**

Run: `find plugins/tax-preparation -type f | wc -l`
Expected: ~25+ files (7 scripts + 6 RSU scripts + 9 references + 4 RSU references + SKILL.md + README + examples)

**Step 5: Commit**

```bash
git add plugins/tax-preparation/
git commit -m "feat: migrate tax-preparation skill to plugin format with RSU integration"
```

---

### Task 4: Migrate portfolio-analyzer Plugin

**Files:**
- Copy: `Skills/portfolio-analyzer/SKILL.md` → `plugins/portfolio-analyzer/skills/portfolio-analyzer/SKILL.md`
- Copy: `Skills/portfolio-analyzer/scripts/` → `plugins/portfolio-analyzer/scripts/`
- Copy: `Skills/portfolio-analyzer/references/` → `plugins/portfolio-analyzer/references/`
- Copy: `Skills/portfolio-analyzer/examples/` → `plugins/portfolio-analyzer/examples/`
- Copy: `Skills/portfolio-analyzer/README.md` → `plugins/portfolio-analyzer/README.md`
- Modify: `plugins/portfolio-analyzer/skills/portfolio-analyzer/SKILL.md` (update paths)

**Step 1: Copy files**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp Skills/portfolio-analyzer/SKILL.md plugins/portfolio-analyzer/skills/portfolio-analyzer/SKILL.md
cp -r Skills/portfolio-analyzer/scripts plugins/portfolio-analyzer/scripts
cp -r Skills/portfolio-analyzer/references plugins/portfolio-analyzer/references
cp -r Skills/portfolio-analyzer/examples plugins/portfolio-analyzer/examples
cp Skills/portfolio-analyzer/README.md plugins/portfolio-analyzer/README.md
```

**Step 2: Update SKILL.md paths**

Replace in `plugins/portfolio-analyzer/skills/portfolio-analyzer/SKILL.md`:
- `scripts/extract_pdf_portfolio.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/extract_pdf_portfolio.py`
- `scripts/parse_csv_portfolio.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/parse_csv_portfolio.py`
- `scripts/calculate_portfolio_metrics.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/calculate_portfolio_metrics.py`
- `references/analysis_framework.md` → `${CLAUDE_PLUGIN_ROOT}/references/analysis_framework.md`
- `references/market_benchmarks.md` → `${CLAUDE_PLUGIN_ROOT}/references/market_benchmarks.md`

**Step 3: Commit**

```bash
git add plugins/portfolio-analyzer/
git commit -m "feat: migrate portfolio-analyzer skill to plugin format"
```

---

### Task 5: Migrate retirement-planner Plugin

**Files:**
- Copy: `Skills/retirement-planner/SKILL.md` → `plugins/retirement-planner/skills/retirement-planner/SKILL.md`
- Copy: `Skills/retirement-planner/scripts/` → `plugins/retirement-planner/scripts/`
- Copy: `Skills/retirement-planner/references/` → `plugins/retirement-planner/references/`
- Copy: `Skills/retirement-planner/examples/` → `plugins/retirement-planner/examples/`
- Copy: `Skills/retirement-planner/README.md` → `plugins/retirement-planner/README.md`
- Modify: `plugins/retirement-planner/skills/retirement-planner/SKILL.md` (update paths)

**Step 1: Copy files**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp Skills/retirement-planner/SKILL.md plugins/retirement-planner/skills/retirement-planner/SKILL.md
cp -r Skills/retirement-planner/scripts plugins/retirement-planner/scripts
cp -r Skills/retirement-planner/references plugins/retirement-planner/references
cp -r Skills/retirement-planner/examples plugins/retirement-planner/examples
cp Skills/retirement-planner/README.md plugins/retirement-planner/README.md
```

**Step 2: Update SKILL.md paths**

Replace in `plugins/retirement-planner/skills/retirement-planner/SKILL.md`:
- `scripts/retirement_calculator.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/retirement_calculator.py`
- `scripts/ss_optimizer.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/ss_optimizer.py`
- `scripts/tax_strategy.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/tax_strategy.py`
- `scripts/monte_carlo.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/monte_carlo.py`
- `scripts/sync_portfolio_data.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/sync_portfolio_data.py`
- `references/retirement_rules.md` → `${CLAUDE_PLUGIN_ROOT}/references/retirement_rules.md`
- `references/tax_strategies.md` → `${CLAUDE_PLUGIN_ROOT}/references/tax_strategies.md`
- `references/healthcare_guide.md` → `${CLAUDE_PLUGIN_ROOT}/references/healthcare_guide.md`
- `references/ss_optimization.md` → `${CLAUDE_PLUGIN_ROOT}/references/ss_optimization.md`

**Step 3: Commit**

```bash
git add plugins/retirement-planner/
git commit -m "feat: migrate retirement-planner skill to plugin format"
```

---

### Task 6: Migrate research-consolidator Plugin

**Files:**
- Copy: `Skills/research-consolidator/SKILL.md` → `plugins/research-consolidator/skills/research-consolidator/SKILL.md`
- Copy: `Skills/research-consolidator/scripts/` → `plugins/research-consolidator/scripts/`
- Copy: `Skills/research-consolidator/references/` → `plugins/research-consolidator/references/`
- Copy: `Skills/research-consolidator/examples/` → `plugins/research-consolidator/examples/`
- Copy: `Skills/research-consolidator/README.md` → `plugins/research-consolidator/README.md`
- Modify: `plugins/research-consolidator/skills/research-consolidator/SKILL.md` (update paths)

**Step 1: Copy files**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp Skills/research-consolidator/SKILL.md plugins/research-consolidator/skills/research-consolidator/SKILL.md
cp -r Skills/research-consolidator/scripts plugins/research-consolidator/scripts
cp -r Skills/research-consolidator/references plugins/research-consolidator/references
cp -r Skills/research-consolidator/examples plugins/research-consolidator/examples
cp Skills/research-consolidator/README.md plugins/research-consolidator/README.md
```

**Step 2: Update SKILL.md paths**

Replace in `plugins/research-consolidator/skills/research-consolidator/SKILL.md`:
- `scripts/source_parser.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/source_parser.py`
- `scripts/claim_alignment.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/claim_alignment.py`
- `scripts/gap_analyzer.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/gap_analyzer.py`
- `scripts/report_generator.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/report_generator.py`
- `scripts/report_validator.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/report_validator.py`
- `references/synthesis_methodology.md` → `${CLAUDE_PLUGIN_ROOT}/references/synthesis_methodology.md`
- `references/report_templates.md` → `${CLAUDE_PLUGIN_ROOT}/references/report_templates.md`
- `references/api_reference.md` → `${CLAUDE_PLUGIN_ROOT}/references/api_reference.md`
- `references/user_guide.md` → `${CLAUDE_PLUGIN_ROOT}/references/user_guide.md`
- `references/workflow_guide.md` → `${CLAUDE_PLUGIN_ROOT}/references/workflow_guide.md`

**Step 3: Commit**

```bash
git add plugins/research-consolidator/
git commit -m "feat: migrate research-consolidator skill to plugin format"
```

---

### Task 7: Migrate kiro-spec-driven-dev Plugin

**Files:**
- Copy: `Skills/kiro-spec-driven-development/SKILL.md` → `plugins/kiro-spec-driven-dev/skills/kiro-spec-driven-dev/SKILL.md`
- Copy: `Skills/kiro-spec-driven-development/references/` → `plugins/kiro-spec-driven-dev/references/`
- Copy: `Skills/kiro-spec-driven-development/examples/` → `plugins/kiro-spec-driven-dev/examples/`
- Copy: `Skills/kiro-spec-driven-development/README.md` → `plugins/kiro-spec-driven-dev/README.md`
- Modify: `plugins/kiro-spec-driven-dev/skills/kiro-spec-driven-dev/SKILL.md` (update paths + name)

**Step 1: Copy files**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp Skills/kiro-spec-driven-development/SKILL.md plugins/kiro-spec-driven-dev/skills/kiro-spec-driven-dev/SKILL.md
cp -r Skills/kiro-spec-driven-development/references plugins/kiro-spec-driven-dev/references
cp -r Skills/kiro-spec-driven-development/examples plugins/kiro-spec-driven-dev/examples
cp Skills/kiro-spec-driven-development/README.md plugins/kiro-spec-driven-dev/README.md
```

**Step 2: Update SKILL.md paths and name**

In `plugins/kiro-spec-driven-dev/skills/kiro-spec-driven-dev/SKILL.md`:
- Update `name: kiro-spec-driven-development` → `name: kiro-spec-driven-dev` in frontmatter
- Replace `references/workflow-definition.md` → `${CLAUDE_PLUGIN_ROOT}/references/workflow-definition.md`
- Replace `references/spec-requirements.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-requirements.md`
- Replace `references/spec-design.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-design.md`
- Replace `references/spec-tasks.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-tasks.md`
- Replace `references/spec-judge.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-judge.md`
- Replace `references/spec-impl.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-impl.md`
- Replace `references/spec-test.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-test.md`
- Replace `references/spec-system-prompt-loader.md` → `${CLAUDE_PLUGIN_ROOT}/references/spec-system-prompt-loader.md`

**Step 3: Commit**

```bash
git add plugins/kiro-spec-driven-dev/
git commit -m "feat: migrate kiro-spec-driven-development skill to plugin format"
```

---

### Task 8: Create dev-tools Plugin (Agent Bundle)

**Files:**
- Copy: `Agents/bug-tracker-resolver/bug-tracker-resolver.md` → `plugins/dev-tools/agents/bug-tracker-resolver.md`
- Copy: `Agents/database-architect/database-architect.md` → `plugins/dev-tools/agents/database-architect.md`
- Copy: `Agents/security-code-scanner/security-code-scanner.md` → `plugins/dev-tools/agents/security-code-scanner.md`
- Copy: `Agents/performance-optimizer/performance-optimizer.md` → `plugins/dev-tools/agents/performance-optimizer.md`
- Copy: `Agents/documentation-maintainer/documentation-maintainer.md` → `plugins/dev-tools/agents/documentation-maintainer.md`
- Create: `plugins/dev-tools/README.md`

**Step 1: Copy agent files**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp Agents/bug-tracker-resolver/bug-tracker-resolver.md plugins/dev-tools/agents/bug-tracker-resolver.md
cp Agents/database-architect/database-architect.md plugins/dev-tools/agents/database-architect.md
cp Agents/security-code-scanner/security-code-scanner.md plugins/dev-tools/agents/security-code-scanner.md
cp Agents/performance-optimizer/performance-optimizer.md plugins/dev-tools/agents/performance-optimizer.md
cp Agents/documentation-maintainer/documentation-maintainer.md plugins/dev-tools/agents/documentation-maintainer.md
```

**Step 2: Create dev-tools README.md**

```markdown
# Dev Tools Plugin

A collection of specialized development agents for Claude Code.

## Agents

| Agent | Purpose |
|-------|---------|
| **bug-tracker-resolver** | Manages bugs in Bugs.md, root cause analysis, resolution plans |
| **database-architect** | PostgreSQL/Supabase schema design, query optimization, RLS policies |
| **security-code-scanner** | Vulnerability identification, OWASP Top 10 analysis |
| **performance-optimizer** | Core Web Vitals, bundle size, runtime efficiency |
| **documentation-maintainer** | READMEs, API docs, user guides, documentation consistency |

## Installation

```bash
/plugin marketplace add mrelph/claude-agents-skills
/plugin install dev-tools@claude-agents-skills
```

## Usage

Agents are invoked automatically by Claude when relevant, or manually via the `/agents` interface.
```

**Step 3: Verify 5 agents + README**

Run: `ls plugins/dev-tools/agents/ && ls plugins/dev-tools/README.md`
Expected: 5 .md files + README

**Step 4: Commit**

```bash
git add plugins/dev-tools/
git commit -m "feat: create dev-tools plugin bundling 5 development agents"
```

---

### Task 9: Replace Marketplace Catalog

**Files:**
- Modify: `.claude-plugin/marketplace.json` (complete rewrite to official schema)
- Remove: `marketplace.json` (root copy — single source of truth now)

**Step 1: Back up old marketplace.json**

```bash
cd /mnt/c/Coding/claude-agents-skills
cp .claude-plugin/marketplace.json .claude-plugin/marketplace.json.bak
```

**Step 2: Write new `.claude-plugin/marketplace.json`**

Replace the entire contents of `.claude-plugin/marketplace.json` with the official schema format from the design doc (6 plugin entries with name, source, description, version, author, keywords, category).

See the design doc `docs/plans/2026-03-04-plugin-marketplace-design.md` "Marketplace Catalog" section for exact content.

**Step 3: Remove root marketplace.json**

```bash
git rm marketplace.json
```

**Step 4: Remove backup**

```bash
rm .claude-plugin/marketplace.json.bak
```

**Step 5: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: replace marketplace catalog with official plugin marketplace schema"
```

---

### Task 10: Clean Up Legacy Structure

Move converted skills out of `Skills/` to avoid confusion. Keep only personal/niche items.

**Files:**
- Remove from Skills/: `tax-preparation/`, `portfolio-analyzer/`, `retirement-planner/`, `research-consolidator/`, `kiro-spec-driven-development/`
- Keep in Skills/: `jr-kraken-18u-navy-lineup/`, `amazon-rsu-tax-calculations/` (reference only)
- Remove from Agents/: the 5 agents now in dev-tools plugin (but keep originals since other agents remain)

**Step 1: Remove migrated skills**

```bash
cd /mnt/c/Coding/claude-agents-skills
git rm -r Skills/tax-preparation/
git rm -r Skills/portfolio-analyzer/
git rm -r Skills/retirement-planner/
git rm -r Skills/research-consolidator/
git rm -r Skills/kiro-spec-driven-development/
```

**Step 2: Remove migrated agents from Agents/ dir**

```bash
git rm -r Agents/bug-tracker-resolver/
git rm -r Agents/database-architect/
git rm -r Agents/security-code-scanner/
git rm -r Agents/performance-optimizer/
git rm -r Agents/documentation-maintainer/
```

**Step 3: Update Skills/README.md and Agents/README.md**

Update these to note that most items have moved to `plugins/` and link there. Keep listing the remaining personal items.

**Step 4: Commit**

```bash
git add Skills/ Agents/
git commit -m "refactor: remove migrated skills and agents from legacy directories"
```

---

### Task 11: Update README.md

**Files:**
- Modify: `README.md` (complete rewrite for plugin marketplace)

**Step 1: Rewrite README.md**

Key sections to include:
- Title: "Claude Agents & Skills Marketplace" (plugin-focused)
- Badge: version 2.0.0
- Quick Install section with `/plugin marketplace add mrelph/claude-agents-skills`
- Plugin catalog table (6 plugins with descriptions)
- Individual plugin install commands
- Legacy section noting personal skills still in Skills/ and Agents/
- Contributing section pointing to CONTRIBUTING.md
- Link to MARKETPLACE.md for programmatic access

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README for plugin marketplace v2.0.0"
```

---

### Task 12: Update CONTRIBUTING.md

**Files:**
- Modify: `CONTRIBUTING.md`

**Step 1: Update contribution guidelines**

Update to show how to contribute a new plugin:
1. Create plugin directory under `plugins/`
2. Add `.claude-plugin/plugin.json` manifest
3. Add skills under `skills/` and/or agents under `agents/`
4. Use `${CLAUDE_PLUGIN_ROOT}` for all internal paths
5. Update staging workflow for plugin format
6. Add entry to `.claude-plugin/marketplace.json`

**Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: update CONTRIBUTING.md for plugin format"
```

---

### Task 13: Update MARKETPLACE.md

**Files:**
- Modify: `MARKETPLACE.md`

**Step 1: Update integration guide**

Document:
- How to add this marketplace: `/plugin marketplace add mrelph/claude-agents-skills`
- marketplace.json schema (now official format)
- Available plugin names for installation
- API/programmatic access to the catalog
- Remove old non-plugin integration instructions

**Step 2: Commit**

```bash
git add MARKETPLACE.md
git commit -m "docs: update MARKETPLACE.md for plugin marketplace format"
```

---

### Task 14: Update CHANGELOG.md

**Files:**
- Modify: `CHANGELOG.md`

**Step 1: Add v2.0.0 entry**

Add at the top of CHANGELOG.md:

```markdown
## [2.0.0] - 2026-03-04

### Added
- Plugin marketplace format with official `.claude-plugin/marketplace.json` schema
- 6 installable plugins: tax-preparation, portfolio-analyzer, retirement-planner, research-consolidator, kiro-spec-driven-dev, dev-tools
- Plugin manifests (plugin.json) for each plugin
- `${CLAUDE_PLUGIN_ROOT}` path resolution for all scripts and references
- dev-tools plugin bundling 5 development agents

### Changed
- Restructured repository from flat skill/agent catalog to plugin marketplace
- Moved skills into plugin format under `plugins/` directory
- Updated marketplace.json to official Claude Code plugin marketplace schema
- Merged amazon-rsu-tax-calculations into tax-preparation plugin

### Removed
- Root marketplace.json (replaced by .claude-plugin/marketplace.json)
- Legacy skill directories (migrated to plugins/)
- Old non-plugin marketplace format
```

**Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add v2.0.0 changelog entry for plugin marketplace evolution"
```

---

### Task 15: Update Tooling Scripts

**Files:**
- Modify: `marketplace-cli.py` (read new format, support plugin install)
- Modify: `add-to-marketplace.py` (scaffold plugin structure)
- Rename: `package-skills.py` → `package-plugins.py` (package plugin dirs)

**Step 1: Update marketplace-cli.py**

Key changes:
- Read `.claude-plugin/marketplace.json` instead of root `marketplace.json`
- Update list/search/info commands for new schema
- Add `install-plugin` command that scaffolds proper plugin dirs
- Remove references to old "source" paths pointing to Skills/Agents

**Step 2: Update add-to-marketplace.py**

Key changes:
- When adding a new item, create full plugin scaffold (`plugins/<name>/.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`)
- Update marketplace.json entry format
- Remove old Skills/Agents directory logic

**Step 3: Rename and update package-skills.py**

```bash
git mv package-skills.py package-plugins.py
```

Update to:
- Package entire plugin directories as ZIPs
- Include `.claude-plugin/plugin.json` in packages
- Update output to `releases/plugins/` instead of `releases/skills/`

**Step 4: Commit**

```bash
git add marketplace-cli.py add-to-marketplace.py package-plugins.py
git commit -m "feat: update tooling scripts for plugin marketplace format"
```

---

### Task 16: Update releases/ Directory

**Files:**
- Clean: `releases/skills/` (old ZIPs)
- Create: `releases/plugins/` (new location)
- Run: `python3 package-plugins.py` to generate new packages

**Step 1: Move old releases**

```bash
mkdir -p releases/plugins
# Old ZIPs can remain for backwards compatibility or be removed
```

**Step 2: Run packaging**

```bash
python3 package-plugins.py
```

**Step 3: Verify packages**

```bash
ls -la releases/plugins/
```
Expected: 6 ZIP files, one per plugin

**Step 4: Commit**

```bash
git add releases/
git commit -m "feat: generate plugin distribution packages"
```

---

### Task 17: Validate and Test

**Step 1: Validate marketplace JSON syntax**

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
```
Expected: No errors

**Step 2: Validate each plugin.json**

```bash
for d in plugins/*/; do
  echo "Validating $d..."
  python3 -c "import json; json.load(open('${d}.claude-plugin/plugin.json'))"
done
```
Expected: All pass

**Step 3: Verify SKILL.md paths use ${CLAUDE_PLUGIN_ROOT}**

```bash
grep -r "scripts/" plugins/*/skills/ | grep -v CLAUDE_PLUGIN_ROOT | grep -v "^Binary"
grep -r "references/" plugins/*/skills/ | grep -v CLAUDE_PLUGIN_ROOT | grep -v "^Binary"
```
Expected: No matches (all paths should use ${CLAUDE_PLUGIN_ROOT})

**Step 4: Verify no broken file references**

For each plugin, verify that every file referenced in SKILL.md exists in the plugin directory (accounting for the `${CLAUDE_PLUGIN_ROOT}/` prefix).

**Step 5: Test local marketplace add (if Claude Code available)**

```bash
/plugin marketplace add ./
/plugin install tax-preparation@claude-agents-skills
```

**Step 6: Final commit (if any fixes needed)**

```bash
git add -A
git commit -m "fix: address validation issues from plugin testing"
```

---

### Task 18: Final Review and Tag

**Step 1: Review git log**

```bash
git log --oneline -20
```

**Step 2: Verify clean working tree**

```bash
git status
```
Expected: clean

**Step 3: Tag release**

```bash
git tag -a v2.0.0 -m "Plugin marketplace evolution - 6 installable plugins"
```

**Step 4: Summary**

Verify all success criteria from design doc:
- [ ] All 6 plugins install cleanly via `/plugin install name@claude-agents-skills`
- [ ] `${CLAUDE_PLUGIN_ROOT}` paths resolve correctly for scripts and references
- [ ] Legacy items remain accessible in `Skills/` and `Agents/`
- [ ] Marketplace validates with `claude plugin validate .`
- [ ] Updated tooling works with new structure
- [ ] README documents the new installation flow
