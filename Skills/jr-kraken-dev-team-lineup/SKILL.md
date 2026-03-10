---
name: jr-kraken-dev-team-lineup
description: This skill should be used when the user asks to "build a dev team lineup", "create dev team lines", "dev team game plan", "dev team strategy", "optimize dev team line combinations", "set up dev team special teams", "plan dev team absences", "update dev team playbook", or mentions the Jr. Kraken Development Team, Dev Team lineup, Dev Team game strategy, or Dev Team forward lines. Do NOT use for the 18U Navy team -- use jr-kraken-18u-navy-lineup instead.
allowed-tools: Read, Bash, Write, Glob, Grep, AskUserQuestion, mcp__teamsnap__*
---

# Jr. Kraken Development Team - Lineup & Strategy Builder

Build competitive lineups and game strategies for Coach Mark's Jr. Kraken Development Team. Covers line combinations, defensive pairings, special teams, opponent analysis, and in-game adjustments -- all rooted in the team's "Competitive Excellence" identity: deploy lines based on player rankings, purpose, and game situations; execute advanced systems with discipline; dominate through preparation and relentless compete level.

## Quick Start

For any lineup or strategy request:

1. **Check RSVPs** -- if TeamSnap MCP is available (`mcp__teamsnap__*` tools), pull RSVPs first. See `references/teamsnap.md` for the full integration workflow. If unavailable, ask Coach Mark for availability.
2. **Read the roster** -- review `references/roster.md` for the full roster, ratings (1-3 or 1-5 scale, auto-detected), and positional capabilities. Cross-reference with RSVPs.
3. **Align with team identity** -- review `references/coach-strategy.md` for the "Competitive Excellence" philosophy.
4. **Assess context** -- game importance, opponent style, player availability, tournament vs regular season.
5. **Select a formation** -- review `references/formations.md` for 3-line vs 4-line approaches and defense pairing philosophies.
6. **Build the lineup** -- follow the step-by-step process in `references/game-planning.md`.
7. **Generate output** -- use `scripts/lineup_generator.py` for formatted lineup sheets, or create a custom artifact.

## Core Resources

### Roster (`references/roster.md`)

**Read first for every lineup request.** Contains the complete roster organized by position, with ratings, positional flexibility (F, D, F/D), depth analysis, special teams personnel, line templates, and absence contingency plans. Starts empty -- populate by uploading a roster file (see `references/roster-management.md`).

**Tier structure** (see `roster.md` for current names and ratings):
- **Elite tier (1.00-1.50)**: Top performers and team leaders
- **Strong tier (1.75-2.00)**: Reliable core contributors
- **Role tier (2.50-3.00)**: Situational players with defined roles

### Team Strategy (`references/coach-strategy.md`)

**Read when planning strategy or explaining team identity.** Covers the "Competitive Excellence" philosophy: ranking-driven deployment, advanced systems, four-line purpose, compete level expectations, strengths/weaknesses, opponent strategy templates, special teams approach, in-game adjustments, and communication guidelines.

### Formations (`references/formations.md`)

**Read when choosing line structure, special teams, or tactical approach.** Covers 4-line vs 3-line forward rotations, defense pair systems, special teams formations (PP umbrella/overload, PK box+1/passive), line deployment by zone, game-situation adjustments, overtime strategy, shift-length guidelines, and F/D player deployment.

### Game Planning (`references/game-planning.md`)

**Read when preparing for opponents or planning tournaments.** Covers pre-game checklist, opponent scouting framework, step-by-step lineup construction (8 steps), game strategy templates, in-game adjustment triggers, post-game analysis, tournament strategy, and communication templates.

## Common Workflows

### 1. Build Game Day Lineup

Read `roster.md` for availability. Choose 3-line or 4-line approach from `formations.md`. Follow `game-planning.md` step-by-step: confirm availability, build lines by player rankings and purpose, construct defense pairs, assign special teams, identify situational players. Generate output with `lineup_generator.py`.

### 2. Strategic Game Plan vs Opponent

Read scouting checklist in `game-planning.md` and opponent templates in `coach-strategy.md`. Determine 2-3 strategic objectives, plan line deployment and matchups, prepare adjustment scenarios.

### 3. In-Game Adjustments

Identify the problem using triggers in `game-planning.md`. Consider line shuffles, defense pair changes, moving F/D players between positions. Reference `formations.md` for structural integrity.

### 4. Special Teams Optimization

Read special teams section in `formations.md` and cross-reference player suitability in `roster.md`. Build PP units from highest-ranked skill players, PK units from defensive depth.

### 5. Tournament Planning

Review tournament section in `game-planning.md`. Pool play = full deployment, all lines with purpose. Playoffs = competitive focus, top lines elevated. Schedule goalie rotation, manage fatigue across games.

### 6. Managing Player Absences

Assess affected position. Use F/D versatile players to fill gaps. Promote by ranking. See absence contingency plans in `roster.md`.

## Updating Power Rankings

Player ratings can be refreshed anytime by uploading an Excel or CSV file. See `references/roster-management.md` for upload format, script usage (`scripts/update_roster.py`), and the update workflow.

## Updating Strategy Files

The strategy and game-planning files are living documents. See `references/file-management.md` for how to edit `coach-strategy.md` and `game-planning.md` when the team's approach evolves.

## Using the Lineup Generator Script

The `scripts/lineup_generator.py` tool creates formatted lineup sheets:

```python
from lineup_generator import DevTeamLineupGenerator

lineup = DevTeamLineupGenerator()
lineup.add_line(1, "LW_Name", "C_Name", "RW_Name", "Offensive")
lineup.add_defense_pair(1, "LD_Name", "RD_Name", "Shutdown")
lineup.set_goalies("Starter_Name", "Backup_Name")
print(lineup.generate_lineup_sheet(opponent="Team", date="March 15, 2026"))
```

Pre-built templates: `generate_standard_four_line_lineup()`, `generate_competitive_three_line_lineup()`, `generate_vs_elite_rival_lineup()`. Requires roster to be populated first.

## Output Workflow

**IMPORTANT: Stay in text until Coach Mark locks the lineup.** Do NOT generate Kraken-branded Word documents (bench card, lineup poster, strategy summary) until the coach explicitly confirms the lineup is final. Use phrases like "locked", "finalized", "good to go", "that's it", or "print it" as the signal to move to branded documents.

### Working Phase (Text Only)

All lineup building happens in plain text or via `scripts/lineup_generator.py` output. This keeps iteration fast:

1. Confirm player availability (TeamSnap RSVPs or manual)
2. Select formation (3-line vs 4-line)
3. Draft forward lines, defense pairs, goalies, special teams
4. Present to Coach Mark in text -- discuss, adjust, swap players, re-draft
5. Repeat until Coach Mark says the lineup is locked

During this phase, use plain text tables, `lineup_generator.py` formatted output, or simple markdown. No Word documents, no branded assets, no formatted bench cards. Keep it fast and easy to change.

### Locked Phase (Branded Documents)

Only after Coach Mark confirms the lineup is locked, produce Kraken-branded Word documents using the **Word skill** and **Kraken branding skill**. See `references/output-formats.md` for the three standard documents (Bench Card, Lineup Poster, Coach Strategy Summary) and other format options.

## Key Principles

**Team Identity -- "Competitive Excellence"**:
- Deploy lines based on rankings, purpose, and game situation
- Every line has a defined mission
- Advanced systems executed with discipline
- Merit-based deployment -- rankings determine opportunity

**Strategic Assets** (see `roster.md` for current counts):
- Defensive-capable players -- depth advantage
- F/D versatile players -- maximize flexibility
- Four-line capability -- roll lines with purpose
- Strong penalty kill -- defensive depth advantage

**Avoid**:
- Random line combinations (every line needs purpose)
- Ignoring F/D versatile players
- Making too many changes at once
- Deploying players outside their capability without reason

When building lineups: **Every line has a purpose. Every player earns their role. Deploy by rankings. Compete every shift.**
