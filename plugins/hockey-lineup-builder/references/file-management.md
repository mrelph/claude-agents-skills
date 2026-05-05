# Updating Strategy & Game Planning Files

The reference files in this skill are **living documents** — update them as the team's approach evolves. When asked to update strategy, change the game plan, add opponent scouting, or modify the team's approach, edit these files directly.

## What Can Be Updated

**`references/team-strategy.md`** — the team's identity and philosophy:
- Core philosophy and team identity tagline
- Strengths and weaknesses assessment
- Forward / defense construction philosophy
- Special teams philosophy (PP/PK approach)
- Opponent strategy templates (vs skill-heavy, vs physical, vs speed-based, vs weaker)
- In-game adjustment guidelines
- Communication notes (to players, parents, assistant coaches)

**`references/game-planning.md`** — tactical execution:
- Pre-game preparation checklist
- Opponent scouting framework
- Step-by-step lineup construction process
- Game strategy templates for different opponent types
- In-game adjustment triggers and fixes
- Post-game analysis framework
- Tournament strategy
- Communication templates

**`references/formations.md`** — tactical systems:
- Forward line structures (3-line vs 4-line)
- Defense pairing philosophies (3-pair, 4-pair, 2-pair)
- Special teams formations (PP umbrella/overload, PK box+1/passive)
- Line deployment by zone and game situation
- Shift length guidelines

**`references/output-templates.md`** — document specifications for the locked-lineup deliverables (Bench Card, Lineup Poster, Strategy Summary).

**`.claude/hockey-lineup-builder.local.md`** — the team config (team name, level, coach name, branding skill, roster source). Edit when team details change.

## How to Update

1. **Read the current file first** — always read the full file before making changes to preserve structure and formatting.
2. **Make targeted edits** — modify specific sections, don't rewrite the whole file.
3. **Keep it name-free** — strategy and tactical files reference players by tier or rating only (e.g. "elite tier", "1.50-rated F/D"). Player names belong in `roster.md`.
4. **Confirm with the user** — summarize what will change and get approval before writing.

## Common Update Scenarios

**"Add a new opponent type / scouting template"**:
- Add a new `### vs [Opponent Type]` section in `team-strategy.md` under Opponent Strategy Templates
- Add a corresponding section in `game-planning.md` if detailed tactical planning differs
- Structure: Their typical traits → Tactical focus → Keys

**"Update our PK/PP approach"**:
- Edit Special Teams Philosophy in `team-strategy.md`
- Update Step 7 in `game-planning.md` if personnel selection criteria change

**"Strategy has evolved mid-season"**:
- Update Core Philosophy and identity sections in `team-strategy.md`
- Review downstream sections (strengths, weaknesses, opponent templates) for consistency

**"Change our in-game adjustment approach"**:
- Edit In-Game Adjustments in `team-strategy.md` (high-level philosophy)
- Edit corresponding section in `game-planning.md` (tactical triggers and fixes)

**"We learned something from last game"**:
- Incorporate insights into the relevant strategy template or adjustment section
- If recurring, add to the game-planning adjustment triggers

## Rules for Edits

- **Never hardcode player names** in `team-strategy.md`, `formations.md`, `game-planning.md` — use tier/rating references only
- **Preserve overall structure** — don't remove headers or reorganize sections without asking
- **Keep it actionable** — concrete guidance, not vague aspirations
- **Cross-reference roster.md** — when strategy depends on specific roster capabilities, add a note like "(see `roster.md` for current count)" so it stays accurate after roster updates
