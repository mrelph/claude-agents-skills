---
name: hockey-lineup-builder
description: This skill should be used when the user asks to "build a lineup", "create game day lines", "plan strategy for the game", "optimize line combinations", "set up special teams", "plan for player absences", "update our strategy", "change our game plan", "add a new opponent", "update the playbook", "check who's available", "update player ratings", "upload a new roster", "plan for a tournament", "generate a bench card", "set up my hockey team", or mentions hockey lineup, forward lines, defense pairings, or game strategy for any hockey team.
allowed-tools: Read, Bash, Write, Edit, Glob, Grep, AskUserQuestion, mcp__teamsnap__*
---

# Hockey Lineup & Strategy Builder

Build effective lineups and game strategies for any hockey team. Covers line combinations, defense pairings, special teams, opponent analysis, and in-game adjustments — driven by the team's own roster and playing identity.

This skill is **generic across teams**. On first use it walks the coach through a short setup interview to capture team name, level, coach, branding, and roster source. Those answers are persisted to `.claude/hockey-lineup-builder.local.md` so subsequent lineup requests skip the setup.

---

## First-Run Setup (Required Before Building Lineups)

Before any lineup or strategy work, check whether the team has been configured:

1. **Look for the config file** at `.claude/hockey-lineup-builder.local.md` (relative to the user's working directory).
2. If it exists, read it — that's the team config. Skip to "Lineup Workflows" below.
3. If it does **not** exist, run the setup interview before doing anything else.

### Setup Interview

Use `AskUserQuestion` to collect the following. Ask in groups of 1-2 questions per turn (don't dump all at once):

**Team identity**
- Team name (e.g. "Jr. Kraken 18U C Navy")
- Age group / division (e.g. "18U", "Squirt", "Bantam")
- Competitive level (e.g. "C", "AA", "Tier 1")
- Head coach name

**Team strategy basics** (free-form OK, can be filled in more later)
- Playing style in 1-2 sentences (e.g. "Defensive grinding team that wins through depth")
- Team identity tagline if any (e.g. "Balanced Depth")

**Branding**
- Is there specific branding (colors, logo, fonts) the team uses? **Yes / No**
- If **Yes**: is there a Claude branding skill installed for this team? (e.g. `anthropic-skills:jr-kraken-brand`)
  - If yes, capture the skill name
  - If no, capture branding notes (colors, fonts, taglines) as free text
- If **No**: documents will be unbranded / generic

**Roster source**
- How will the roster be provided?
  - **(a) Excel / CSV file** — ask for the path; run `update_roster.py` to import
  - **(b) JSON inline** — collect the JSON and run `update_roster.py --json`
  - **(c) Skip for now** — leave the placeholder roster; user will import later

After collecting answers, write `.claude/hockey-lineup-builder.local.md` (see template below). Confirm with the user before writing.

If a roster source was provided, run the import:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py <path>
# or
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py --json '<json>'
```

Then offer to help the user fill in `${CLAUDE_PLUGIN_ROOT}/references/team-strategy.md` (which starts as a template).

### Config File Template

Write to `.claude/hockey-lineup-builder.local.md`:

```markdown
---
team_name: <team name>
age_group: <e.g. 18U>
level: <e.g. C, AA, Tier 1>
head_coach: <name>
branding_skill: <skill name OR empty>
branding_notes: <free text OR empty>
roster_source: <file path OR "json" OR "manual">
created: <YYYY-MM-DD>
---

# <Team Name> Configuration

## Identity
- Team name: <name>
- Level: <age group> <level>
- Head coach: <name>
- Playing style: <1-2 sentences>
- Tagline: <if any>

## Branding
<one of:>
- Branding skill: `<skill name>` — invoke before generating Word documents
- Branding notes: <colors / fonts / taglines>
- No team branding — produce clean unbranded documents

## Roster
- Source: <path or "json" or "manual">
- Last imported: <YYYY-MM-DD or "not yet imported">
```

**When to re-run setup**: only if the user explicitly asks to reconfigure ("set up the team again", "change the team", "switch teams"). Otherwise read the existing config and proceed.

---

## Lineup Workflows

For any lineup or strategy request (after setup is complete):

1. **Read the team config** at `.claude/hockey-lineup-builder.local.md` to load team name, branding choice, etc.
2. **Check RSVPs** (if TeamSnap MCP available) — pull RSVPs for the upcoming game/event. If unavailable, ask the user for player availability.
3. **Read the roster** — `${CLAUDE_PLUGIN_ROOT}/references/roster.md` for current players, ratings, and capabilities. Cross-reference with RSVPs.
4. **Align with team identity** — `${CLAUDE_PLUGIN_ROOT}/references/team-strategy.md` for the team's philosophy.
5. **Assess context** — game importance, opponent style, player availability, tournament vs regular season.
6. **Select a formation** — `${CLAUDE_PLUGIN_ROOT}/references/formations.md` for 3-line vs 4-line approaches and defense pair philosophies.
7. **Build the lineup** — follow the step-by-step process in `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`.
8. **Generate output** — use `${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py` for a formatted text sheet, or produce branded Word documents (see Output Workflow below).

---

## Core Resources

### Roster (`${CLAUDE_PLUGIN_ROOT}/references/roster.md`)

**Read first for every lineup request.** Generated by importing a roster file via `scripts/update_roster.py`. Contains the full roster organized by position, with ratings, positional flexibility (F, D, F/D), depth analysis, special teams personnel, and absence contingency notes.

If the roster is empty (skill not yet imported), prompt the user to import via `update_roster.py` before continuing.

### Team Strategy (`${CLAUDE_PLUGIN_ROOT}/references/team-strategy.md`)

**Read when planning strategy or explaining team identity.** Customizable per team — covers core philosophy, strengths/weaknesses, line/pair construction philosophy, special teams approach, opponent strategy templates, in-game adjustments, and communication notes.

If `team-strategy.md` is still a template (unfilled), offer to help the coach fill it in.

### Formations (`${CLAUDE_PLUGIN_ROOT}/references/formations.md`)

**Read when choosing line structure, special teams, or tactical approach.** Team-agnostic library covering 4-line vs 3-line forward systems, 3-pair / 4-pair / 2-pair defense systems, special teams formations (PP umbrella / overload, PK box+1 / passive box), line deployment by zone, game-situation adjustments, overtime strategy, shift lengths, and goalie rotation.

### Game Planning (`${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`)

**Read when preparing for opponents or planning tournaments.** Pre-game prep checklist, opponent scouting framework, step-by-step lineup construction (8 steps), opponent-archetype templates, in-game adjustment triggers, post-game analysis, tournament strategy, and communication templates.

---

## Common Workflows

### 1. Build Game Day Lineup

Read `roster.md` for availability. Choose a 3-line or 4-line approach from `formations.md`. Follow the 8-step construction process in `game-planning.md`: confirm availability, build top forward line, construct defense pairs, fill remaining lines, assign special teams, identify situational players, shelter development players. Generate output with `lineup_generator.py` or as a custom artifact.

**Output**: Complete lineup with forward lines, defense pairs, goalies, special teams, sheltering notes.

### 2. Strategic Game Plan vs Opponent

Read scouting checklist in `game-planning.md`. For specific opponent archetypes, also read the strategy templates in `team-strategy.md`. Determine 2-3 strategic objectives, plan deployment and matchups, prepare adjustment scenarios, identify how to exploit opponent weaknesses.

**Output**: Game plan with scouting notes, objectives, lineup, contingency plans.

### 3. In-Game Adjustments

Identify the problem using triggers in `game-planning.md`. Consider line shuffles within a tier, defense pair changes, moving versatile F/D players, or special teams personnel changes. Reference `formations.md` to maintain structural integrity.

**Output**: Revised lineup with rationale.

### 4. Special Teams Optimization

Read special teams sections in `formations.md` and cross-reference player suitability in `roster.md`. PP: highest-rated skill players. PK: defensive depth (two-way forwards, top D). Plan backup units to cover absences.

**Output**: Special teams units with formations and personnel.

### 5. Tournament Planning

Review tournament considerations in `game-planning.md`. Plan pool play (4 lines, balanced ice time, development focus) vs playoff approach (3 lines, top players more, hot goalie). Schedule goalie rotation, build per-game depth charts, manage fatigue across the weekend.

**Output**: Tournament game plans with adjusted lineups for each game.

### 6. Managing Player Absences

Assess affected positions. Use F/D versatile players to fill gaps. Promote from lower lines as needed, adjust strategy to match available personnel, communicate changes. See absence notes in `roster.md`.

**Output**: Modified lineup that maintains competitive balance.

---

## Updating Power Rankings (Roster Refresh)

Player ratings are not hardcoded. Refresh by running:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py <path_to_file>
```

Supports Excel, CSV, and inline JSON. See `${CLAUDE_PLUGIN_ROOT}/references/roster-management.md` for file format specs, examples, and post-update checklist. Dry-run is supported via `--dry-run`.

---

## Updating Strategy & Game Planning Files

`team-strategy.md`, `game-planning.md`, and `formations.md` are living documents. When the coach's approach evolves, edit them directly. **Keep edits name-free** — use tier/rating references only. Player names belong in `roster.md`. Confirm changes with the user before writing. See `${CLAUDE_PLUGIN_ROOT}/references/file-management.md` for procedures and editing rules.

---

## Using the Lineup Generator Script

`${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py` creates formatted lineup sheets.

```python
from lineup_generator import LineupGenerator

lineup = LineupGenerator(team_name="Your Team Name", tagline="Your Identity")

lineup.add_line(1, "LW_Name", "C_Name", "RW_Name", "Top/Offensive")
lineup.add_line(2, "LW_Name", "C_Name", "RW_Name", "Two-Way")

lineup.add_defense_pair(1, "LD_Name", "RD_Name", "Shutdown")
lineup.add_defense_pair(2, "LD_Name", "RD_Name", "Balanced")
lineup.add_defense_pair(3, "LD_Name", "RD_Name", "Sheltered")

lineup.set_goalies("Starter_Name", "Backup_Name")

print(lineup.generate_lineup_sheet(
    opponent="Opponent Name",
    date="October 26, 2025",
    game_type="League",
    notes="Key tactical focus"
))
```

The script also includes generic templates: `generate_standard_four_line_lineup()` and `generate_competitive_three_line_lineup()`. Both use placeholder names — populate from your roster.

---

## TeamSnap Integration (RSVP Checking)

When the TeamSnap MCP is available, use it as the **first step** in any lineup-building workflow.

### How to Use

1. **Check if TeamSnap MCP tools are available** (`mcp__teamsnap__*`). If not, fall back to asking the coach for availability.
2. **Pull RSVPs for the upcoming game** — list events and retrieve RSVP statuses.
3. **Map RSVPs to roster** in `${CLAUDE_PLUGIN_ROOT}/references/roster.md`. Categorize:
   - **Available (Yes)** — confirmed attending
   - **Not Available (No)** — confirmed absent
   - **Maybe / No Response** — flag for coach follow-up; build contingency assuming they're out
4. **Adjust lineup strategy** based on availability:
   - Missing 1-2 forwards: use F/D versatile players
   - Missing 3+ forwards: consider three-line system
   - Missing defense: move F/D players back

### When TeamSnap Is Not Available

Ask the user directly: "Which players are available for this game?" Reference absence notes in `roster.md` for common scenarios.

---

## Output Workflow

When building a lineup, follow this two-phase process:

### Phase 1: Build in Text (Decision-Making)

Work through the lineup in plain text first.

1. Confirm player availability (TeamSnap RSVPs or manual)
2. Select formation (3-line vs 4-line)
3. Draft forward lines, defense pairs, goalies, special teams
4. Note sheltering requirements for development players
5. Add game-specific tactical focus and notes

Present the text lineup to the coach for review and adjustments. Use `lineup_generator.py` for quick formatted output. Iterate until finalized.

### Phase 2: Generate Branded Word Documents

Once the lineup is locked, produce three Word documents using the **Word skill**.

**Branding application** — read `.claude/hockey-lineup-builder.local.md`:
- If `branding_skill` is set: invoke that skill before generating documents (e.g. `anthropic-skills:jr-kraken-brand`)
- If `branding_notes` is set: apply colors / fonts / taglines manually
- If neither: produce clean unbranded documents

See `${CLAUDE_PLUGIN_ROOT}/references/output-templates.md` for Bench Card, Lineup Poster, and Coach Strategy Summary specs.

---

## Tips for Success

1. **Setup once, build many** — finish the setup interview thoroughly so subsequent lineup requests are fast.
2. **Embrace depth** — most teams' biggest unrealized advantage is rolling more lines than the opponent.
3. **Leverage versatility** — F/D players solve most lineup problems. Use them to fill gaps and create matchup advantages.
4. **Shelter development players** — give development-tier players opportunities in the right situations. Protect from overwhelming matchups while building confidence.
5. **Track what works** — note successful line combinations, special teams units, and opponent strategies. Update `team-strategy.md` and `game-planning.md` as the season progresses.
6. **Plan for absences** — at youth levels, players miss games for school, family, and other commitments. Always have a contingency lineup ready.

---

## Worked Example

For a fully populated example of how this skill is configured for a real team, see `${CLAUDE_PLUGIN_ROOT}/examples/jr-kraken-18u-navy/`. It contains:
- A populated `roster.md` (17-player roster with ratings)
- A fully filled-in `team-strategy.md` ("Balanced Depth" identity)
- A sample lineup request

Use it as a reference when helping a new coach fill in their own files.
