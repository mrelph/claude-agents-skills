---
name: jr-kraken-18u-navy-lineup
description: This skill should be used when the user asks to "build a lineup", "create game day lines", "plan strategy for the game", "optimize line combinations", "set up special teams", "plan for player absences", or mentions the Jr. Kraken 18U Navy team, Coach Mark, hockey lineup, forward lines, defense pairings, or game strategy. Also triggered by mentions of specific players like Marsh, Relph, Freeman, or opponent matchups against Paul's team.
allowed-tools: Read, Bash, Write, Glob, Grep, AskUserQuestion
---

# Jr. Kraken 18U C Navy - Lineup & Strategy Builder

Build effective lineups and game strategies for Coach Mark's Jr. Kraken 18U C Navy Team. Covers line combinations, defensive pairings, special teams, opponent analysis, and in-game adjustments -- all rooted in the team's "Balanced Depth" identity: win through depth, defense, and attrition; wear opponents down over three periods; everyone contributes across four lines; dominate third periods when the depth advantage emerges.

## Quick Start

For any lineup or strategy request:

1. **Read the roster** -- review `references/roster.md` for the 17-player roster, ratings (1.00-3.00 scale), and positional capabilities.
2. **Align with team identity** -- review `references/mark-strategy.md` for the "Balanced Depth" coaching philosophy.
3. **Assess context** -- game importance, opponent style (especially Paul's team), player availability, tournament vs regular season.
4. **Select a formation** -- review `references/formations.md` for 3-line vs 4-line approaches and defense pairing philosophies.
5. **Build the lineup** -- follow the step-by-step process in `references/game-planning.md`.
6. **Generate output** -- use `scripts/lineup_generator.py` for formatted lineup sheets, or create a custom artifact.

## Core Resources

### Roster (`references/roster.md`)

**Read first for every lineup request.** Contains the complete 17-player roster organized by position, with ratings (1.00 = elite, 3.00 = significant development), positional flexibility indicators (F, D, F/D), depth analysis, special teams personnel, line combination templates, absence contingency plans, and goalie capabilities.

**Key roster facts**:
- **17 total players** (15 skaters + 2 goalies)
- **Two 1.00 elite players**: Marsh and Relph (team leaders, both F/D)
- **Three 1.50 strong players**: Freeman, Klakring, Silliker (solid core)
- **Eight 1.75-2.00 players**: McCredy, Young, Bagga, Berry, Butler, Herrick, Jaeger, Tegart (team backbone)
- **Two development players**: Cram (2.50 F), Thompson (3.00 D) -- both need sheltering
- **9 defensive-capable players** -- major strategic advantage over most teams' 6
- **6 F/D versatile players** -- Marsh, Relph, Freeman, Silliker, Berry, Tegart
- **12 forward-capable players** -- enables 4-line rotation

### Team Strategy (`references/mark-strategy.md`)

**Read when planning strategy or explaining team identity.** Covers the "Balanced Depth" philosophy, four-line rotation principles, defensive structure priorities, grinding style tactics, development player protection, strengths/weaknesses analysis, strategy vs Paul's team, special teams approach (strong PK focus), in-game adjustments, and communication guidelines.

**Core identity**:
- Win through depth, defense, and attrition
- Wear opponents down over three periods
- Everyone contributes -- four lines all matter
- Strong third-period team (depth advantage emerges)
- Protect developing players while giving them opportunities

### Formations (`references/formations.md`)

**Read when choosing line structure, special teams, or tactical approach.** Covers 4-line vs 3-line forward rotations with specific line structures, 3-pair/4-pair/2-pair defense systems (leveraging 9 D-capable players), special teams formations (PP umbrella, PP overload, PK box+1 aggressive, PK passive box), line deployment by zone, game-situation adjustments (score-based, period-specific), overtime strategy, shift-length guidelines, F/D player deployment, goalie rotation, and line chemistry factors.

### Game Planning (`references/game-planning.md`)

**Read when preparing for opponents or planning tournaments.** Covers pre-game preparation checklist (24-48 hours out), opponent scouting framework, step-by-step lineup construction (8 steps), game strategy templates for different opponent types (Paul's team, elite skill, physical, weak, unknown), in-game adjustment triggers and common fixes, post-game analysis framework, tournament multi-game strategy (pool play vs playoffs), back-to-back game management, communication templates, and decision trees for mid-game changes.

## Common Workflows

### 1. Build Game Day Lineup

Read `roster.md` to confirm player availability (18U players often have conflicts). Choose a 3-line or 4-line approach from `formations.md`. Follow the step-by-step process in `game-planning.md`: confirm availability, build the top forward line (Marsh-Relph-Freeman core), construct defense pairs (leverage 9 D-capable players), fill remaining lines with balanced talent distribution, assign special teams (PK is a priority), identify situational players, and shelter Cram and Thompson appropriately. Generate formatted output with `lineup_generator.py` or create a custom artifact.

**Output**: Complete lineup with forward lines, defense pairs, goalies, special teams, and sheltering notes.

### 2. Strategic Game Plan vs Opponent

Read the scouting checklist in `game-planning.md`. For Paul's team, also read the head-to-head section in `mark-strategy.md`. Determine 2-3 strategic objectives, plan line deployment and matchups using roster knowledge, prepare adjustment scenarios (if losing, if winning, special teams struggling), and identify how to exploit opponent weaknesses (e.g., Paul's limited D depth).

**Output**: Game plan with scouting notes, strategic objectives, lineup, and contingency plans.

### 3. In-Game Adjustments

Identify the problem using adjustment triggers in `game-planning.md` (line getting dominated, chemistry off, matchup exploited, score/situation demands a change). Consider line shuffles among the 2.00-rated players, defense pair changes, moving Marsh or Relph between F and D, or special teams personnel modifications. Leverage F/D versatile players to solve problems without disrupting overall balance. Reference `formations.md` to maintain structural integrity.

**Output**: Revised lineup with rationale for changes.

### 4. Special Teams Optimization

Read the special teams section in `formations.md` and cross-reference player suitability in `roster.md`. For power play, use skill players (Marsh, Relph, Freeman, Klakring on PP1; Silliker, McCredy, Herrick on PP2). For penalty kill, leverage defensive depth (Silliker, Tegart, Freeman, McCredy as PK forwards; Young, Butler, Berry on PK defense). Plan backup units to cover absences.

**Output**: Special teams units with formations and player positioning.

### 5. Tournament Planning

Review tournament considerations in `game-planning.md`. Plan pool play approach (4 lines, balanced ice time, everyone contributes, development focus) vs playoff approach (3 lines, top players get more ice time, hot goalie gets preference). Schedule goalie rotation (Haffey/Schuchart split, alternate for back-to-back days). Build depth charts for each game, manage fatigue across the weekend, and give development players meaningful opportunities in appropriate games. Four-line depth is a major advantage in multi-game tournaments.

**Output**: Tournament game plans with adjusted lineups for each game.

### 6. Managing Player Absences

Assess which position is affected. Use F/D versatile players to fill gaps -- 9 D-capable players is the key advantage. Promote from lower lines, adjust strategy to match available personnel, and communicate changes to the team. See the absence contingency plans in `roster.md` for specific scenarios (Marsh out, Relph out, both elite players out, multiple forwards missing, D missing).

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
- **Critical**: Shelter Cram (2.50) and Thompson (3.00) but give them chances

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
- Overexposing Cram or Thompson in tough situations
- Trying to match Paul's elite speed (play to our strengths)

## Key Decision Points

**3-line vs 4-line forward rotation**:
- Use **4 lines** for most games (our strength), when depth will wear opponents down, and when balancing ice time matters.
- Use **3 lines** for close playoff games, late in tight games, or when short-handed due to absences.

**Development vs winning balance**:
- League games: 4 lines, balanced ice time, focus on structure and development.
- Close/playoff games: 3 lines, best players get more ice time, but everyone still plays.
- Tournaments: Pool play = development focus; playoffs = competitive focus.

**Goalie selection**:
- Recent performance matters most. Consider opponent strength (Haffey for skill teams, Schuchart for physical teams). Split back-to-back games. Communicate the decision 24-48 hours ahead.

**Against Paul's team**:
- Read the detailed head-to-head strategy in `mark-strategy.md` and the game plan template in `game-planning.md`. Their strengths: 4 elite (1.25) forwards, speed-based attack, strong power play. Their weakness: only 6 D-capable players (vs our 9). Key approach: grind them down with four lines, heavy forecheck against their tired D-men, strong penalty kill to neutralize their PP, physical but disciplined play, and dominate the third period when our depth emerges.

## Using the Lineup Generator Script

The `scripts/lineup_generator.py` tool creates formatted lineup sheets.

```python
from lineup_generator import NavyLineupGenerator

lineup = NavyLineupGenerator()

# Add forward lines
lineup.add_line(1, "Marsh", "Relph", "Freeman", "Elite/Offensive")
lineup.add_line(2, "Klakring", "Silliker", "McCredy", "Two-Way")

# Add defense pairs
lineup.add_defense_pair(1, "Young", "Berry", "Shutdown")
lineup.add_defense_pair(2, "Butler", "Tegart", "Balanced")
lineup.add_defense_pair(3, "Thompson", "Bagga", "Sheltered")

# Set goalies
lineup.set_goalies("Haffey", "Schuchart")

# Generate formatted output
print(lineup.generate_lineup_sheet(
    opponent="Paul's White Team",
    date="October 26, 2025",
    game_type="League",
    notes="Exploit their limited D depth, strong forecheck"
))
```

Use the script for official lineup sheets, comparing multiple scenarios, documenting decisions, and sharing with coaches/parents. The script also includes pre-built templates accessible via `generate_standard_four_line_lineup()`, `generate_competitive_three_line_lineup()`, and `generate_vs_paul_lineup()`.

## Output Formats

Choose the format that fits the request:

- **Text lineups** -- use the script or manual formatting for quick game-day sheets
- **Document artifacts** -- Word/PDF for printing and distribution; use Kraken brand colors from project files
- **Interactive artifacts** -- React components for lineup experimentation and drag-and-drop visualization
- **Spreadsheets** -- Excel files for tracking lineups across the season, analyzing player combinations, and recording ice time
- **Presentation slides** -- PowerPoint for team meetings or parent presentations
- **Email templates** -- formatted lineup emails using team contact lists from project files; include game details, lineup, and tactical focus

## Sheltering Guidelines

These two players require special deployment considerations in every lineup. See `roster.md` for full details.

**Ender Cram (F, 2.50)**:
- Deploy on the third or fourth line only
- Pair with 1.50-1.75+ rated linemates for support
- Prefer offensive zone starts when possible
- Limit penalty kill duty
- Give development chances but protect from tough matchups
- Target ice time: 8-12 minutes (regular), 5-8 minutes (competitive/playoff)

**Timothy Thompson (D, 3.00)**:
- Deploy on the third defense pair only
- **Always** pair with a strong, experienced partner (Young, Berry, or Butler)
- Limit ice time in critical situations
- Assign simple, structured defensive tasks
- Skating development is his primary growth area
- Target ice time: 6-10 minutes (regular), 3-6 minutes (competitive/playoff)

## Tips for Success

1. **Embrace four-line depth** -- it is our identity and biggest strength. Roll all four lines in most games and trust the system.
2. **Leverage versatility** -- 6 F/D players solve most lineup problems. Use them to fill gaps, adjust mid-game, and create matchup advantages.
3. **Shelter development players** -- give Cram and Thompson opportunities in the right situations. Protect them from overwhelming matchups while building their confidence.
4. **Track what works** -- keep notes on successful line combinations, special teams units, and opponent strategies. Review and adjust after every game.
5. **Plan for absences** -- at 18U, players frequently miss games for school, family, and other commitments. Always have a contingency lineup ready, and use the absence plans in `roster.md`.

When building lineups, always remember: **We are Coach Mark's Navy team. We win through Balanced Depth, defensive structure, four-line rotation, and grinding determination. We wear opponents down and win third periods.**
