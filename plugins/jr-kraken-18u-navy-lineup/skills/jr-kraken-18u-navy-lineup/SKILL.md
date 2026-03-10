---
name: jr-kraken-18u-navy-lineup
description: This skill should be used when the user asks to "build a lineup", "create game day lines", "plan strategy for the game", "optimize line combinations", "set up special teams", "plan for player absences", "update our strategy", "change our game plan", "add a new opponent", "update the playbook", or mentions the Jr. Kraken 18U Navy team, Coach Mark, hockey lineup, forward lines, defense pairings, or game strategy.
allowed-tools: Read, Bash, Write, Glob, Grep, AskUserQuestion, mcp__teamsnap__*
---

# Jr. Kraken 18U C Navy - Lineup & Strategy Builder

Build effective lineups and game strategies for Coach Mark's Jr. Kraken 18U C Navy Team. Covers line combinations, defensive pairings, special teams, opponent analysis, and in-game adjustments -- all rooted in the team's "Balanced Depth" identity: win through depth, defense, and attrition; wear opponents down over three periods; everyone contributes across four lines; dominate third periods when the depth advantage emerges.

## Quick Start

For any lineup or strategy request:

1. **Check RSVPs (if TeamSnap MCP available)** -- use the TeamSnap MCP tools to pull RSVPs for the upcoming game/event. This gives you confirmed availability before building the lineup. If the TeamSnap MCP is not available, ask Coach Mark for player availability manually.
2. **Read the roster** -- review `${CLAUDE_PLUGIN_ROOT}/references/roster.md` for the 17-player roster, ratings (1.00-3.00 scale), and positional capabilities. Cross-reference with TeamSnap RSVPs to identify who is in/out/maybe.
3. **Align with team identity** -- review `${CLAUDE_PLUGIN_ROOT}/references/coach-strategy.md` for the "Balanced Depth" coaching philosophy.
4. **Assess context** -- game importance, opponent style, player availability, tournament vs regular season.
5. **Select a formation** -- review `${CLAUDE_PLUGIN_ROOT}/references/formations.md` for 3-line vs 4-line approaches and defense pairing philosophies.
6. **Build the lineup** -- follow the step-by-step process in `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`.
7. **Generate output** -- use `${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py` for formatted lineup sheets, or create a custom artifact.

## Core Resources

### Roster (`${CLAUDE_PLUGIN_ROOT}/references/roster.md`)

**Read first for every lineup request.** Contains the complete 17-player roster organized by position, with ratings (1.00 = elite, 3.00 = significant development), positional flexibility indicators (F, D, F/D), depth analysis, special teams personnel, line combination templates, absence contingency plans, and goalie capabilities.

**Key roster facts** (see `roster.md` for current names and ratings):
- **17 total players** (15 skaters + 2 goalies)
- **Elite tier (1.00-1.50)**: Team leaders and solid core
- **Strong tier (1.75-2.00)**: Team backbone
- **Development tier (2.50-3.00)**: Need sheltering
- **9 defensive-capable players** -- major strategic advantage over most teams' 6
- **6 F/D versatile players** -- critical for flexibility
- **12 forward-capable players** -- enables 4-line rotation

### Team Strategy (`${CLAUDE_PLUGIN_ROOT}/references/coach-strategy.md`)

**Read when planning strategy or explaining team identity.** Covers the "Balanced Depth" philosophy, four-line rotation principles, defensive structure priorities, grinding style tactics, development player protection, strengths/weaknesses analysis, opponent strategy templates, special teams approach (strong PK focus), in-game adjustments, and communication guidelines.

**Core identity**:
- Win through depth, defense, and attrition
- Wear opponents down over three periods
- Everyone contributes -- four lines all matter
- Strong third-period team (depth advantage emerges)
- Protect developing players while giving them opportunities

### Formations (`${CLAUDE_PLUGIN_ROOT}/references/formations.md`)

**Read when choosing line structure, special teams, or tactical approach.** Covers 4-line vs 3-line forward rotations with specific line structures, 3-pair/4-pair/2-pair defense systems (leveraging 9 D-capable players), special teams formations (PP umbrella, PP overload, PK box+1 aggressive, PK passive box), line deployment by zone, game-situation adjustments (score-based, period-specific), overtime strategy, shift-length guidelines, F/D player deployment, goalie rotation, and line chemistry factors.

### Game Planning (`${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`)

**Read when preparing for opponents or planning tournaments.** Covers pre-game preparation checklist (24-48 hours out), opponent scouting framework, step-by-step lineup construction (8 steps), game strategy templates for different opponent types (elite skill, physical, weak, unknown), in-game adjustment triggers and common fixes, post-game analysis framework, tournament multi-game strategy (pool play vs playoffs), back-to-back game management, communication templates, and decision trees for mid-game changes.

## Common Workflows

### 1. Build Game Day Lineup

Read `${CLAUDE_PLUGIN_ROOT}/references/roster.md` to confirm player availability (18U players often have conflicts). Choose a 3-line or 4-line approach from `${CLAUDE_PLUGIN_ROOT}/references/formations.md`. Follow the step-by-step process in `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`: confirm availability, build the top forward line (elite tier core), construct defense pairs (leverage 9 D-capable players), fill remaining lines with balanced talent distribution, assign special teams (PK is a priority), identify situational players, and shelter development players appropriately. Generate formatted output with `${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py` or create a custom artifact.

**Output**: Complete lineup with forward lines, defense pairs, goalies, special teams, and sheltering notes.

### 2. Strategic Game Plan vs Opponent

Read the scouting checklist in `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`. For elite skill opponents, also read the opponent strategy templates in `${CLAUDE_PLUGIN_ROOT}/references/coach-strategy.md`. Determine 2-3 strategic objectives, plan line deployment and matchups using roster knowledge, prepare adjustment scenarios (if losing, if winning, special teams struggling), and identify how to exploit opponent weaknesses (e.g., limited D depth).

**Output**: Game plan with scouting notes, strategic objectives, lineup, and contingency plans.

### 3. In-Game Adjustments

Identify the problem using adjustment triggers in `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md` (line getting dominated, chemistry off, matchup exploited, score/situation demands a change). Consider line shuffles among the 2.00-rated players, defense pair changes, moving elite F/D players between forward and defense, or special teams personnel modifications. Leverage F/D versatile players to solve problems without disrupting overall balance. Reference `${CLAUDE_PLUGIN_ROOT}/references/formations.md` to maintain structural integrity.

**Output**: Revised lineup with rationale for changes.

### 4. Special Teams Optimization

Read the special teams section in `${CLAUDE_PLUGIN_ROOT}/references/formations.md` and cross-reference player suitability in `${CLAUDE_PLUGIN_ROOT}/references/roster.md`. For power play, use the highest-rated skill players (elite tier on PP1, strong tier on PP2). For penalty kill, leverage defensive depth (two-way forwards and top D-men on PK1, grind-line forwards and depth D on PK2). Plan backup units to cover absences.

**Output**: Special teams units with formations and player positioning.

### 5. Tournament Planning

Review tournament considerations in `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`. Plan pool play approach (4 lines, balanced ice time, everyone contributes, development focus) vs playoff approach (3 lines, top players get more ice time, hot goalie gets preference). Schedule goalie rotation (split starts, alternate for back-to-back days). Build depth charts for each game, manage fatigue across the weekend, and give development players meaningful opportunities in appropriate games. Four-line depth is a major advantage in multi-game tournaments.

**Output**: Tournament game plans with adjusted lineups for each game.

### 6. Managing Player Absences

Assess which position is affected. Use F/D versatile players to fill gaps -- 9 D-capable players is the key advantage. Promote from lower lines, adjust strategy to match available personnel, and communicate changes to the team. See the absence contingency plans in `${CLAUDE_PLUGIN_ROOT}/references/roster.md` for specific scenarios (elite player out, both elite players out, multiple forwards missing, D missing).

**Output**: Modified lineup that maintains competitive balance despite absences.

## Lineup Building Principles

### Always Consider

**Team Identity -- "Balanced Depth"**:
- Spread talent across all four lines (do not overload top line)
- Everyone contributes meaningfully
- Wear opponents down over 60 minutes
- Third period is our period (depth advantage emerges)
- Defense-first structure

**Development Focus**:
- Balance winning with growth at C-level competitive hockey
- Rotate players through different line positions
- Give everyone meaningful ice time (especially tournaments)
- **Critical**: Shelter development players (2.50+ tier) but give them chances

**Strategic Assets**:
- **9 defensive-capable players** -- biggest advantage, use it
- **6 F/D versatile players** -- maximize flexibility
- **Four-line capability** -- roll lines when others cannot
- **Strong penalty kill foundation** -- defensive depth pays off

**Chemistry Indicators**:
- Players who have succeeded together before
- Complementary playing styles (shooter + playmaker, speed + grit)
- On-ice communication and work rate matching
- Speed/skill/size balance within lines

### Avoid

- Overloading the top line (spread the wealth)
- Running the same combinations every game (explore options)
- Ignoring F/D versatile players (they are strategic gold)
- Forgetting about special teams when building 5v5 lines
- Making too many changes at once (adjust gradually)
- Overexposing development players in tough situations
- Trying to match an opponent's elite speed (play to our strengths)

## Key Decision Points

**3-line vs 4-line forward rotation**:
- Use **4 lines** for most games (our strength), when depth will wear opponents down, and when balancing ice time matters.
- Use **3 lines** for close playoff games, late in tight games, or when short-handed due to absences.

**Development vs winning balance**:
- League games: 4 lines, balanced ice time, focus on structure and development.
- Close/playoff games: 3 lines, best players get more ice time, but everyone still plays.
- Tournaments: Pool play = development focus; playoffs = competitive focus.

**Goalie selection**:
- Recent performance matters most. Consider opponent strength and goalie tendencies (see `roster.md`). Split back-to-back games. Communicate the decision 24-48 hours ahead.

**Against elite skill / star-heavy opponents**:
- Read the opponent strategy templates in `${CLAUDE_PLUGIN_ROOT}/references/coach-strategy.md` and `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`. Common traits: multiple elite forwards, speed-based attack, strong power play, but limited D depth. Key approach: grind them down with four lines, heavy forecheck against their tired D-men, strong penalty kill to neutralize their PP, physical but disciplined play, and dominate the third period when our depth emerges.

## Updating Power Rankings

Player ratings are **not hardcoded** -- they can be refreshed at any time by uploading a new Excel or CSV file. This updates both `${CLAUDE_PLUGIN_ROOT}/references/roster.md` and the roster in `${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py`.

### How to Update

When a user provides a new roster file (Excel, CSV) or asks to update player ratings:

1. **Save the uploaded file** to a working location.
2. **Run the update script**:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py <path_to_roster.xlsx>
# or
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py <path_to_roster.csv>
```

3. **Review the output** -- the script reports what it found and updated.
4. **Read the refreshed `${CLAUDE_PLUGIN_ROOT}/references/roster.md`** to confirm the new ratings are correct before building any lineups.

### Expected File Format

The Excel or CSV file needs at minimum two columns (case-insensitive, flexible matching):

| Column | Aliases | Required | Example |
|--------|---------|----------|---------|
| Name | Name, Player, Player Name | Yes | Massey Relph |
| Rating | Rating, Power Ranking, Rank, Score | Yes | 1.00 |
| Position | Position, Pos | No (defaults to F) | F/D |
| Notes | Notes, Comments | No | Elite at both positions |
| Can Also Play | Can Also Play, Alt Position | No (goalies) | Forward (emergency) |

Use `G` for goalies in the Position column. Use `F/D` for versatile players.

### Example CSV

```csv
Name,Position,Rating,Notes
Massey Relph,F/D,1.00,"Coach's son, elite at both positions"
Shaya Marsh,F/D,1.00,"Elite talent, leadership"
Thad Freeman,F/D,1.50,"Versatile two-way player"
Cas Haffey,G,2.00,"Reliable starter"
```

### JSON Alternative

For inline updates without a file:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py --json '{"players": [
  {"name": "Massey Relph", "position": "F/D", "rating": 1.00, "notes": "Elite"},
  {"name": "Shaya Marsh", "position": "F/D", "rating": 1.25, "notes": "Rating adjusted"}
]}'
```

### Dry Run

Preview changes without writing files:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py --dry-run <path_to_roster.xlsx>
```

### What Gets Updated

- **`${CLAUDE_PLUGIN_ROOT}/references/roster.md`** -- fully regenerated with new ratings, tiers, positional depth analysis, and deployment notes
- **`${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py`** -- the internal roster dict is updated to match

### After Updating

After refreshing the roster, re-read `${CLAUDE_PLUGIN_ROOT}/references/roster.md` before building any lineups. The tier groupings (Elite, Strong, Development) and lineup templates may shift based on the new ratings. Pay attention to:
- Players who moved between tiers (e.g., 2.50 player improved to 2.00)
- Changes in who needs sheltering
- Shifts in F/D versatile player count
- Updated average team rating

## Updating Strategy & Game Planning Files

The `${CLAUDE_PLUGIN_ROOT}/references/game-planning.md` and `${CLAUDE_PLUGIN_ROOT}/references/coach-strategy.md` files are **living documents** that can be updated when Coach Mark's approach evolves. When the user asks to update strategy, change the game plan, add opponent scouting, or modify the team's approach, edit these files directly.

### What Can Be Updated

**`${CLAUDE_PLUGIN_ROOT}/references/coach-strategy.md`** — the team's identity and philosophy:
- Core philosophy and "Balanced Depth" principles
- Strengths and weaknesses assessment
- Opponent strategy templates (vs elite skill, vs physical, vs speed, vs weak teams)
- Special teams philosophy (PP/PK approach)
- In-game adjustment guidelines
- Communication messaging (to players, parents, assistant coaches)
- Season goals and success metrics

**`${CLAUDE_PLUGIN_ROOT}/references/game-planning.md`** — tactical execution:
- Pre-game preparation checklist
- Opponent scouting framework
- Step-by-step lineup construction process
- Game strategy templates for different opponent types
- In-game adjustment triggers and fixes
- Post-game analysis framework
- Tournament strategy
- Communication templates

### How to Update

1. **Read the current file first** — always read the full file before making changes to understand the existing structure and avoid breaking the format.
2. **Make targeted edits** — modify specific sections rather than rewriting the whole file. Preserve the markdown structure, headers, and formatting conventions.
3. **Keep it name-free** — these files reference players by tier/rating (e.g., "elite tier", "1.50-rated F/D player", "development D-man") rather than by name. Player names belong in `${CLAUDE_PLUGIN_ROOT}/references/roster.md` only. This ensures strategy files stay valid when the roster changes.
4. **Confirm with the user** — before writing changes, summarize what will be updated and get approval.

### Common Update Scenarios

**"Add a new opponent strategy"**:
- Add a new `### vs [Opponent Type]` section in `coach-strategy.md` under Game Strategy Templates
- Add a corresponding game plan template in `game-planning.md` if detailed tactical planning is needed
- Structure it like existing templates: Their Strengths, Their Weaknesses, Our Strategy, Keys

**"Update our PK/PP approach"**:
- Edit the Special Teams Philosophy section in `coach-strategy.md`
- Update Step 7 (Assign Special Teams) in `game-planning.md` if the personnel selection criteria change

**"Change our in-game adjustment approach"**:
- Edit the In-Game Adjustments section in `coach-strategy.md` (high-level philosophy)
- Edit the corresponding section in `game-planning.md` (tactical details and triggers)

**"We learned something from last game"**:
- Incorporate insights into the relevant strategy template or adjustment section
- If it's a recurring pattern, add it to the game-planning.md adjustment triggers

**"Our identity is evolving"**:
- Update the Core Philosophy and Team Identity sections in `coach-strategy.md`
- Review all downstream sections (strengths, weaknesses, opponent strategies) for consistency with the new identity

### Rules for Edits

- **Never hardcode player names** in these files — use tier/rating references only
- **Preserve the overall structure** — don't remove headers or reorganize sections without asking
- **Keep it actionable** — strategy files should contain concrete guidance, not vague aspirations
- **Cross-reference roster.md** — when strategy depends on specific roster capabilities (e.g., "9 D-capable players"), add a note like "(see `roster.md` for current count)" so it stays accurate after roster updates

## Using the Lineup Generator Script

The `${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py` tool creates formatted lineup sheets.

```python
from lineup_generator import NavyLineupGenerator

lineup = NavyLineupGenerator()

# Add forward lines
lineup.add_line(1, "LW_Name", "C_Name", "RW_Name", "Elite/Offensive")
lineup.add_line(2, "LW_Name", "C_Name", "RW_Name", "Two-Way")

# Add defense pairs (use names from roster.md)
lineup.add_defense_pair(1, "LD_Name", "RD_Name", "Shutdown")
lineup.add_defense_pair(2, "LD_Name", "RD_Name", "Balanced")
lineup.add_defense_pair(3, "LD_Name", "RD_Name", "Sheltered")

# Set goalies
lineup.set_goalies("Starter_Name", "Backup_Name")

# Generate formatted output
print(lineup.generate_lineup_sheet(
    opponent="Opponent Name",
    date="October 26, 2025",
    game_type="League",
    notes="Exploit their limited D depth, strong forecheck"
))
```

Use the script for official lineup sheets, comparing multiple scenarios, documenting decisions, and sharing with coaches/parents. The script also includes pre-built templates accessible via `generate_standard_four_line_lineup()`, `generate_competitive_three_line_lineup()`, and `generate_vs_elite_rival_lineup()`.

## TeamSnap Integration (RSVP Checking)

When the TeamSnap MCP is available, use it as the **first step** in any lineup-building workflow to get real-time player availability.

### How to Use

1. **Check if TeamSnap MCP tools are available** -- look for `mcp__teamsnap__*` tools. If not available, fall back to asking the user for availability.
2. **Pull RSVPs for the upcoming game** -- use the TeamSnap MCP to list events/games and retrieve RSVP statuses for each player.
3. **Map RSVPs to roster** -- match TeamSnap player names to the roster in `${CLAUDE_PLUGIN_ROOT}/references/roster.md`. Categorize players as:
   - **Available (Yes)** -- confirmed attending, include in lineup
   - **Not Available (No)** -- confirmed absent, plan around their absence
   - **Maybe / No Response** -- flag these for Coach Mark to follow up on; build a contingency lineup assuming they are out
4. **Adjust lineup strategy** -- based on who is available:
   - If missing 1-2 forwards: use F/D versatile players to fill gaps
   - If missing 3+ forwards: consider 3-line system
   - If missing defense: move F/D players back (see `roster.md` for F/D versatile list)
   - If both elite players are out: see absence contingency plans in `roster.md`

### Workflow Example

```
Step 1: "Let me check TeamSnap for RSVPs..."
        → Use TeamSnap MCP to get game event and RSVP list

Step 2: "Here's the availability for Saturday's game:
         YES (13): [list confirmed players from roster.md]
         NO (2):   [list absent players]
         MAYBE (2): [list uncertain players]"

Step 3: "With 2 confirmed out and 2 uncertain:
         - We have 11 confirmed skaters + 2 goalies
         - Building a 3-line base lineup with contingency for 4 lines if uncertain players confirm
         - Assess which positions are affected and plan F/D moves
         - Can move an F/D versatile player to D to create a 3rd pair"

Step 4: Build the lineup using the standard process in game-planning.md
```

### When TeamSnap Is Not Available

If the TeamSnap MCP is not configured or unavailable:
- Ask the user directly: "Which players are available for this game?"
- Or ask: "Are there any absences I should plan around?"
- Reference the absence contingency plans in `roster.md` for common scenarios

## Output Workflow

When building a lineup, follow this two-phase process:

### Phase 1: Build in Text (Decision-Making)

Work through the lineup in plain text first. This is the thinking/decision phase:

1. Confirm player availability (TeamSnap RSVPs or manual)
2. Select formation (3-line vs 4-line)
3. Draft forward lines, defense pairs, goalies, special teams
4. Note sheltering requirements for development players
5. Add game-specific tactical focus and notes

Present the text lineup to Coach Mark for review and adjustments. Use the `${CLAUDE_PLUGIN_ROOT}/scripts/lineup_generator.py` for quick formatted text output. Iterate until the lineup is finalized.

### Phase 2: Generate Word Documents (Kraken-Branded)

Once the lineup is finalized, produce three Word documents using the **Word skill** and **Kraken branding skill** in Claude Desktop. All three documents should use Jr. Kraken branding (colors, fonts, logos) via the Kraken branding skill.

#### Document 1: Bench Card

A compact, laminate-ready reference card for the coach to hold on the bench during the game.

**Contents**:
- Game header: Opponent, date, time, location
- Forward lines: Line 1-4 with LW / C / RW and line role (Elite, Skilled, Grind, Development)
- Defense pairs: Pair 1-3 with LD / RD and pair role (Shutdown, Two-Way, Sheltered)
- Goalies: Starter and backup
- Power play units: PP1 and PP2 with player names and formation (umbrella/overload)
- Penalty kill units: PK1 and PK2 with player names and system (box+1/passive)
- Situational notes: Late game (protecting lead / need goal), overtime shifts
- Sheltering reminders: Development player deployment limits (shift length, zone starts, minutes cap)

**Format**: Single page, landscape orientation, dense layout with clear sections. Designed to be printed, laminated, and used on the bench. Large enough font to read at a glance.

#### Document 2: Lineup Poster

A locker room display for the team to see before the game.

**Contents**:
- Game header: "NAVY vs [OPPONENT]" with date and location
- Forward lines: Line 1-4 with player names in a clear visual layout
- Defense pairs: Pair 1-3 with player names
- Goalies: Starter (highlighted) and backup
- Special teams: PP and PK units
- Game focus: 2-3 tactical bullet points for this game (e.g., "Heavy forecheck", "Roll four lines", "Third period is OURS")
- Team identity reminder: "Balanced Depth" tagline or motivational message

**Format**: Single page, portrait orientation, clean and bold. Designed to be printed large (11x17 or taped to the locker room wall). Player names should be prominent. Kraken branding throughout.

#### Document 3: Coach Strategy Summary

A game plan overview for Coach Mark and assistant coaches.

**Contents**:
- Game header: Opponent, date, time, location, game type (league/tournament/playoff)
- Opponent scouting: Their style, strengths, weaknesses, key threats (if known)
- Strategic objectives: 2-3 tactical priorities for this game
- Full lineup: Forward lines, defense pairs, goalies with ratings and roles
- Special teams: PP and PK units with formations
- Deployment plan: Ice time targets per line/pair, zone start preferences
- Sheltering plan: Specific deployment limits for development players
- Adjustment triggers: What to watch for and how to respond (line shuffles, F/D moves, 3-line collapse)
- Period-by-period approach: P1 (establish), P2 (maintain), P3 (take control)
- Communication notes: Pre-game message to team, key coaching points

**Format**: 1-2 pages, portrait orientation, detailed but scannable. Sections with headers, bullet points, and tables. Designed for the coach to review before the game and reference during intermissions. Kraken branding on header/footer.

### When to Generate Which Documents

| Scenario | Text | Bench Card | Lineup Poster | Strategy Summary |
|----------|------|------------|---------------|------------------|
| Quick lineup check | Yes | No | No | No |
| Standard league game | Yes | Yes | Yes | Optional |
| Rivalry / tough opponent | Yes | Yes | Yes | Yes |
| Tournament game | Yes | Yes | Yes | Yes |
| Playoff game | Yes | Yes | Yes | Yes |
| In-game adjustment | Yes | No | No | No |

### Other Output Formats

For non-standard requests, the skill can also produce:
- **Email templates** -- formatted lineup emails with game details, lineup, and tactical focus
- **Spreadsheets** -- season tracking, player combinations, ice time analysis (use Excel/spreadsheet skill)
- **Presentation slides** -- team meetings or parent presentations (use PowerPoint/slides skill)

## Sheltering Guidelines

Development players (2.50+ tier) require special deployment considerations in every lineup. See `${CLAUDE_PLUGIN_ROOT}/references/roster.md` for current development players, their ratings, and detailed sheltering plans.

**Development Forwards (2.50 tier)**:
- Deploy on the third or fourth line only
- Pair with 1.50-1.75+ rated linemates for support
- Prefer offensive zone starts when possible
- Limit penalty kill duty
- Give development chances but protect from tough matchups
- Target ice time: 8-12 minutes (regular), 5-8 minutes (competitive/playoff)

**Development Defensemen (3.00 tier)**:
- Deploy on the third defense pair only
- **Always** pair with a strong, experienced partner (1.75 or better)
- Limit ice time in critical situations
- Assign simple, structured defensive tasks
- Target ice time: 6-10 minutes (regular), 3-6 minutes (competitive/playoff)

## Tips for Success

1. **Embrace four-line depth** -- it is our identity and biggest strength. Roll all four lines in most games and trust the system.
2. **Leverage versatility** -- 6 F/D players solve most lineup problems. Use them to fill gaps, adjust mid-game, and create matchup advantages.
3. **Shelter development players** -- give 2.50+ tier players opportunities in the right situations. Protect them from overwhelming matchups while building their confidence.
4. **Track what works** -- keep notes on successful line combinations, special teams units, and opponent strategies. Review and adjust after every game.
5. **Plan for absences** -- at 18U, players frequently miss games for school, family, and other commitments. Always have a contingency lineup ready, and use the absence plans in `${CLAUDE_PLUGIN_ROOT}/references/roster.md`.

When building lineups, always remember: **We are Coach Mark's Navy team. We win through Balanced Depth, defensive structure, four-line rotation, and grinding determination. We wear opponents down and win third periods.**
