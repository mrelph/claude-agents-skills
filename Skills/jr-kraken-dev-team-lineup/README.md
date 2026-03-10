# Jr Kraken Development Team - Lineup & Strategy Builder Skill

## Overview

This skill provides comprehensive lineup building and game strategy support for Coach Mark's Jr Kraken Development Team. It helps create effective game-day lineups, develop opponent-specific strategies, and make in-game adjustments based on the team's "Competitive Excellence" identity.

## Quick Start

1. **Upload roster** -- run `scripts/update_roster.py` with an Excel/CSV roster file to populate the team
2. **Read** `SKILL.md` -- Main instructions for using this skill
3. **Reference** the files in `references/` folder for detailed information
4. **Generate** lineups using the Python script in `scripts/`

## Team Identity: "Competitive Excellence"

**Coach**: Mark
**Philosophy**: Deploy lines based on rankings, purpose, and game situations
**Style**: Advanced systems with ranking-driven deployment across all four lines
**Strength**: Depth, versatility, and relentless compete level

## Roster

The roster starts empty and must be populated by uploading a player rankings file.

**Upload a roster:**
```bash
python3 scripts/update_roster.py roster.xlsx       # From Excel
python3 scripts/update_roster.py roster.csv        # From CSV
python3 scripts/update_roster.py --dry-run roster.xlsx  # Preview only
```

**Required columns**: Name, Rating (1.00-3.00 scale). Optional: Position, Notes.

## Core Resources

### `/references/roster.md`
Team roster with ratings, positions, and depth analysis. Populated by `update_roster.py`. Read this FIRST when building any lineup.

**Key Info**:
- Player ratings (1.00 = elite, 3.00 = role player)
- Position flexibility (F, D, F/D)
- Tier-based deployment guidelines
- Versatile F/D players

### `/references/coach-strategy.md`
Coach Mark's "Competitive Excellence" philosophy and team identity.

**Key Concepts**:
- Ranking-driven deployment
- Advanced tactical execution
- Four-line purpose and depth
- Compete level as baseline expectation
- Strengths vs weaknesses
- Opponent strategy templates

### `/references/formations.md`
Tactical formations and line deployment strategies.

**Key Systems**:
- Four-line vs three-line forward systems
- Defense pair structures
- Power play formations (umbrella, overload)
- Penalty kill systems (box+1 aggressive)
- Special situations (late game, OT)

### `/references/game-planning.md`
Opponent scouting, lineup construction, and in-game adjustments.

**Key Processes**:
- Pre-game preparation checklist
- Step-by-step lineup construction
- Opponent-specific game plans
- In-game adjustment triggers
- Post-game analysis framework
- Tournament strategy

## Scripts

### `/scripts/update_roster.py`
Python script for refreshing power rankings from an Excel or CSV file. Updates both `references/roster.md` and the roster in `lineup_generator.py`.

### `/scripts/lineup_generator.py`
Python script for generating formatted lineup sheets.

**Usage**:
```python
from lineup_generator import DevTeamLineupGenerator

lineup = DevTeamLineupGenerator()

# Build custom (use names from roster.md)
lineup.add_line(1, "LW_Name", "C_Name", "RW_Name", "Offensive")
lineup.add_defense_pair(1, "LD_Name", "RD_Name", "Shutdown")
lineup.set_goalies("Starter_Name", "Backup_Name")

# Generate output
print(lineup.generate_lineup_sheet(
    opponent="Opponent Name",
    date="March 15, 2026",
    game_type="League Game"
))
```

## Common Workflows

### 1. Build Standard Game Lineup
1. Read `roster.md` -- confirm available players
2. Read `coach-strategy.md` -- align with team philosophy
3. Read `formations.md` -- choose four-line or three-line system
4. Follow process in `game-planning.md` to build lineup
5. Use script to generate formatted output

### 2. Prepare for Elite Skill Rival
1. Read opponent strategy templates in `coach-strategy.md`
2. Review matchup strategy in `game-planning.md`
3. Build lineup focused on exploiting their weaknesses
4. Heavy forecheck, strong PK, roll four lines

### 3. Make In-Game Adjustment
1. Identify problem (see triggers in `game-planning.md`)
2. Review adjustment options in `formations.md`
3. Use F/D versatile players to solve issues
4. Communicate changes clearly to team

### 4. Tournament Planning
1. Review tournament section in `game-planning.md`
2. Plan pool play (four lines, full deployment) vs playoff (three lines) approach
3. Schedule goalie rotation
4. Manage ice time across multiple games

## Key Principles

**Always Remember**:
- Rankings and purpose drive deployment
- Every line has a defined mission
- Advanced systems executed with discipline
- Compete level is the baseline expectation
- Depth is our advantage -- use it

**Core Strategy**:
- Deploy lines with intent based on rankings and game situations
- Roll four lines to maintain freshness and pressure
- Strong penalty kill (defensive depth advantage)
- Physical but disciplined play
- Win through preparation, execution, and relentless effort

## Output Workflow

### Phase 1: Text Lineup (Decision-Making)
Build and iterate on the lineup in plain text using `scripts/lineup_generator.py`. Review with Coach Mark before finalizing.

### Phase 2: Kraken-Branded Word Documents
Once finalized, generate three Word documents using the **Word skill** and **Kraken branding skill**:

1. **Bench Card** -- Compact, laminate-ready coach reference (landscape, single page). Lines, pairs, special teams, deployment notes.
2. **Lineup Poster** -- Locker room display (portrait, bold). Full lineup, game focus bullets, team identity message.
3. **Coach Strategy Summary** -- Game plan for coaches (1-2 pages). Scouting, objectives, full lineup, deployment plan, adjustment triggers, period-by-period approach.

### Other Formats
- **Email**: Lineup distribution (use project email lists)
- **Spreadsheets**: Season tracking (use xlsx/spreadsheet skill)
- **Presentations**: Team meetings (use pptx/slides skill)

## Tips for Success

1. **Start with roster.md** -- Always know who's available
2. **Deploy with purpose** -- Every line has a mission
3. **Use F/D players** -- They solve most problems
4. **Execute advanced systems** -- Trust the players
5. **Stay flexible** -- Adjust based on game flow
6. **Communicate clearly** -- Players and parents understand decisions
7. **Third period focus** -- This is when our advantage emerges
8. **Trust the system** -- "Competitive Excellence" wins games

## Support & Updates

This skill is designed to evolve with the team throughout the season. As you learn what works and what doesn't, update the reference files to reflect successful strategies and combinations.

**Season tracking ideas**:
- Document successful line combinations
- Track player performance vs rankings
- Note opponent-specific strategies that worked
- Record special teams success rates

---

**Remember**: We are Coach Mark's Dev Team. We compete through preparation, ranking-driven deployment, and advanced execution. Every line has a purpose. Every player earns their role. This is how we WIN.
