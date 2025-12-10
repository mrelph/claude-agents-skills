# Jr Kraken 18U C Navy - Lineup & Strategy Builder Skill

## Overview

This skill provides comprehensive lineup building and game strategy support for Coach Mark's Jr Kraken 18U C Navy Team. It helps create effective game-day lineups, develop opponent-specific strategies, and make in-game adjustments based on the team's "Balanced Depth" identity.

## Quick Start

1. **Read** `SKILL.md` - Main instructions for using this skill
2. **Reference** the files in `references/` folder for detailed information
3. **Generate** lineups using the Python script in `scripts/`

## Team Identity: "Balanced Depth"

**Coach**: Mark  
**Philosophy**: Win through depth, defense, and determination - not individual stars  
**Style**: Four-line grinding hockey with strong defensive structure  
**Strength**: 9 defensive-capable players (vs most teams' 6)

## Roster Quick Reference

- **Total Players**: 17 (15 skaters + 2 goalies)
- **Elite (1.00-1.50)**: Marsh, Relph, Freeman, Klakring, Silliker
- **Strong (1.75-2.00)**: McCredy, Young, Bagga, Berry, Butler, Herrick, Jaeger, Tegart
- **Development (2.50-3.00)**: Cram (needs sheltering), Thompson (needs heavy sheltering)
- **Key Advantage**: 9 D-capable players, 6 F/D versatile players

## Core Resources

### `/references/roster.md`
Complete 17-player roster with ratings, positions, and depth analysis. Read this FIRST when building any lineup.

**Key Info**:
- Player ratings (1.00 = elite, 3.00 = significant development)
- Position flexibility (F, D, F/D)
- Special considerations (Cram/Thompson sheltering needs)
- Versatile F/D players (Marsh, Relph, Freeman, Silliker, Berry, Tegart)

### `/references/mark-strategy.md`
Coach Mark's "Balanced Depth" philosophy and team identity.

**Key Concepts**:
- Four-line depth approach
- Defense-first structure
- Grinding style
- Third-period dominance
- Strengths vs weaknesses
- Strategy vs Paul's team

### `/references/formations.md`
Tactical formations and line deployment strategies for 18U C level.

**Key Systems**:
- Four-line vs three-line forward systems
- Three-pair defense structure
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

### `/scripts/lineup_generator.py`
Python script for generating formatted lineup sheets.

**Usage**:
```python
from lineup_generator import NavyLineupGenerator

lineup = NavyLineupGenerator()

# Pre-built templates
lineup.generate_standard_four_line_lineup()
lineup.generate_competitive_three_line_lineup()
lineup.generate_vs_paul_lineup()

# Or build custom
lineup.add_line(1, "Marsh", "Relph", "Freeman", "Elite")
lineup.add_defense_pair(1, "Young", "Berry", "Shutdown")
lineup.set_goalies("Haffey", "Schuchart")

# Generate output
print(lineup.generate_lineup_sheet(
    opponent="Opponent Name",
    date="October 26, 2025",
    game_type="League Game"
))
```

**Run Examples**:
```bash
cd /mnt/skills/user/jr-kraken-18u-navy-lineup/scripts
python3 lineup_generator.py
```

## Common Workflows

### 1. Build Standard Game Lineup
1. Read `roster.md` - confirm available players
2. Read `mark-strategy.md` - align with team philosophy
3. Read `formations.md` - choose four-line or three-line system
4. Follow process in `game-planning.md` to build lineup
5. Use script to generate formatted output

### 2. Prepare for Paul's Team
1. Read opponent section in `mark-strategy.md`
2. Review matchup strategy in `game-planning.md`
3. Use `generate_vs_paul_lineup()` in script
4. Focus on exploiting their 6 D-men weakness

### 3. Make In-Game Adjustment
1. Identify problem (see triggers in `game-planning.md`)
2. Review adjustment options in `formations.md`
3. Use F/D versatile players to solve issues
4. Communicate changes clearly to team

### 4. Tournament Planning
1. Review tournament section in `game-planning.md`
2. Plan pool play (four lines) vs playoff (three lines) approach
3. Schedule goalie rotation
4. Manage ice time across multiple games

## Key Principles

**Always Remember**:
- ⭐ **9 D-capable players** = Our biggest advantage
- Four-line depth is our identity
- Defense-first, offense comes from defense
- Third period is OUR period (depth emerges)
- Shelter Cram (2.50) and Thompson (3.00)
- Everyone contributes, everyone matters

**Core Strategy**:
- Grind opponents down over 60 minutes
- Roll four lines to maintain freshness
- Strong penalty kill (defensive depth advantage)
- Physical but disciplined play
- Win through collective effort, not individual stars

## vs Paul's White Team (Key Rivalry)

**Their Strengths**: 4 elite forwards (1.25), speed, skill, strong PP  
**Their Weakness**: Only 6 D-capable players (we have 9)  

**Our Strategy**:
1. Heavy forecheck - attack their tired D-men
2. Roll four lines - wear them down
3. Strong PK - neutralize their PP
4. Physical play - make them work
5. Third period dominance - our depth emerges

## Important Notes

### Development Players
- **Cram (2.50)**: Third/fourth line, strong linemates, offensive zone starts, limited critical minutes
- **Thompson (3.00)**: Third D-pair, ALWAYS with strong partner, very limited critical minutes, focus on skating development

### Versatile F/D Players (Strategic Gold)
- Marsh (1.00), Relph (1.00), Freeman (1.50) - elite at both
- Silliker (1.50), Berry (2.00), Tegart (2.00) - solid at both
- Use them to cover absences and solve in-game problems

### Player Absences (Common at 18U)
- Use F/D players to fill gaps instantly
- We have 9 D-capable players - can handle multiple D absences
- Adjust strategy based on who's missing
- Always have contingency plans

## Integration with Project Files

This skill works with your project documents:
- Uses roster from `Jr_Kraken_18U_Master_Team_Document.md`
- References team balance analysis
- Can pull email lists for lineup distribution
- Aligns with Kraken brand colors for materials

## Output Formats

Create outputs in various formats:
- **Text**: Simple formatted lineups (using script)
- **Documents**: Word/PDF for printing (use docx skill)
- **Spreadsheets**: Season tracking (use xlsx skill)
- **Presentations**: Team meetings (use pptx skill)
- **Email**: Lineup distribution (use project email lists)

## Tips for Success

1. **Start with roster.md** - Always know who's available
2. **Trust the depth** - Four-line system is our strength
3. **Use F/D players** - They solve most problems
4. **Shelter development players** - Protect Cram and Thompson
5. **Stay flexible** - Adjust based on game flow
6. **Communicate clearly** - Players and parents understand decisions
7. **Third period focus** - This is when our advantage emerges
8. **Trust the system** - "Balanced Depth" wins games

## Support & Updates

This skill is designed to evolve with the team throughout the season. As you learn what works and what doesn't, update the reference files to reflect successful strategies and combinations.

**Season tracking ideas**:
- Document successful line combinations
- Track Cram and Thompson development
- Note opponent-specific strategies that worked
- Record special teams success rates

---

**Remember**: We are Coach Mark's Navy Team. We win through Balanced Depth, defensive structure, and determination. We don't win the sprint - we win the marathon. This is how we WIN.

🏒 GO NAVY! 🏒
