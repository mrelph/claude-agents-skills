---
name: jr-kraken-18u-navy-lineup
description: Comprehensive lineup building and game strategy system for Jr. Kraken 18U C Navy Team (Coach Mark). Use when creating game day lineups, planning strategies against opponents, making in-game adjustments, or optimizing player combinations. Includes roster knowledge, "Balanced Depth" coaching philosophy, formation strategies, special teams planning, and development player management for 18U C level competitive hockey.
allowed-tools: Read, Bash, Write, Glob, Grep, AskUserQuestion
---

# Jr. Kraken 18U C Navy - Lineup & Strategy Builder

This skill helps build effective lineups and game strategies for Coach Mark's Jr. Kraken 18U C Navy Team. It provides structured guidance for line combinations, defensive pairings, special teams, opponent analysis, and in-game adjustments tailored to the team's "Balanced Depth" identity.

## Quick Start

For any lineup or strategy request:

1. **Read roster information**: Start by reviewing `references/roster.md` to understand the 17-player roster, ratings (1.00-3.00 scale), and capabilities
2. **Understand team identity**: Review `references/mark-strategy.md` to understand the "Balanced Depth" coaching philosophy
3. **Consider the context**: Game importance? Opponent style (especially Paul's team)? Player availability? Tournament vs regular season?
4. **Select formation strategy**: Review `references/formations.md` for 3-line vs 4-line approaches and defensive pairing philosophies
5. **Build the lineup**: Use principles from `references/game-planning.md` to construct optimal combinations
6. **Generate output**: Use `scripts/lineup_generator.py` for formatted lineup sheets, or create custom artifacts

## Core Resources

### Roster Reference (`references/roster.md`)

**When to read**: ALWAYS read first when building lineups or discussing player deployment

Contains:
- Complete 17-player roster organized by position
- Player ratings (1.00-3.00 scale, where 1.00 = elite, 3.00 = significant development needed)
- Positional flexibility indicators (F, D, F/D)
- Depth analysis for each position
- Goalie capabilities (both can play out if needed)

**Key roster features**:
- **17 total players** (15 skaters + 2 goalies)
- **Two 1.00 elite players**: Marsh and Relph (team leaders)
- **Five 1.50 strong players**: Freeman, Klakring, Silliker (solid core)
- **Eight 1.75-2.00 players**: Consistent middle tier (team backbone)
- **Two development players**: Cram (2.50), Thompson (3.00) - need sheltering
- **9 defensive-capable players**: Major strategic advantage
- **12 forward-capable players**: Allows 4-line rotation

### Team Strategy Philosophy (`references/mark-strategy.md`)

**When to read**: When planning game strategy, making lineup decisions, or explaining team identity

Contains:
- "Balanced Depth" coaching philosophy
- Four-line rotation principles
- Defensive structure priorities
- Grinding style tactics
- Development player protection strategies
- Strengths and weaknesses vs Paul's team
- Special teams approach (strong PK focus)

**Core identity**:
- Win through depth, defense, and attrition
- Wear opponents down over three periods
- Everyone contributes, four lines all matter
- Strong third-period team
- Protect developing players while giving them opportunities

### Formations & Strategy (`references/formations.md`)

**When to read**: When deciding on line structure, special teams, or tactical approach for 18U C level

Contains:
- 4-line vs 3-line forward rotation strategies (18U C level)
- Defense pairing philosophies (leveraging 9 D-capable players)
- Line composition principles and chemistry factors
- Special teams formations (power play umbrella, penalty kill box+1)
- Game situation adjustments (score-based, period-specific)
- Line change best practices
- Goalie rotation strategy
- Development player deployment (Cram, Thompson)

### Game Planning (`references/game-planning.md`)

**When to read**: When preparing for specific opponents or planning tournament strategy

Contains:
- Pre-game opponent scouting checklist
- Step-by-step lineup construction process
- Lineup templates for documentation
- In-game adjustment triggers and strategies
- Post-game analysis framework
- Tournament multi-game strategy
- Special considerations for games vs Paul's team
- Managing missing players (common at 18U level)

## Common Workflows

### Workflow 1: Build Game Day Lineup

**Scenario**: Creating lineup for an upcoming game

**Steps**:
1. Read `references/roster.md` to confirm available players
2. Review `references/mark-strategy.md` to align with team philosophy
3. Determine if 3-line or 4-line approach (read relevant section in `references/formations.md`)
4. Follow the step-by-step process in `references/game-planning.md`:
   - Confirm availability (18U players often have conflicts)
   - Build top forward line (Marsh-Relph-Freeman core)
   - Construct defense pairs (leverage 9 D-capable players)
   - Fill remaining lines (balance talent distribution)
   - Assign special teams (PK priority)
   - Identify situational players
   - Shelter Cram and Thompson appropriately
5. Generate formatted output using `scripts/lineup_generator.py` or create custom artifact

**Output**: Complete lineup with forward lines, defense pairs, goalies, special teams, sheltering notes

### Workflow 2: Strategic Game Planning vs Opponent

**Scenario**: Preparing strategy against specific opponent (especially Paul's team)

**Steps**:
1. Read opponent scouting checklist in `references/game-planning.md`
2. If playing Paul's team, review head-to-head section in `references/mark-strategy.md`
3. Review relevant tactical concepts in `references/formations.md`
4. Determine strategic objectives (2-3 focus areas)
5. Plan line deployment and matchups using roster knowledge
6. Prepare adjustment scenarios (if losing, if winning, special teams struggling)
7. Identify how to exploit opponent weaknesses (e.g., Paul's limited D depth)

**Output**: Game plan document with scouting notes, strategic objectives, lineup, and contingency plans

### Workflow 3: In-Game Adjustments

**Scenario**: Lines aren't working during game, need to adjust

**Steps**:
1. Identify the problem (review adjustment triggers in `references/game-planning.md`)
2. Consider common adjustment options (line shuffles, pair changes, special teams modifications)
3. Reference formation principles to maintain balance
4. Leverage F/D versatile players to solve problems
5. Communicate changes clearly to coaching staff/players

**Output**: Revised lineup with rationale for changes

### Workflow 4: Special Teams Optimization

**Scenario**: Setting up power play or penalty kill units

**Steps**:
1. Read special teams section in `references/formations.md`
2. Review roster for best suited players (`references/roster.md`)
3. **Power Play**: Utilize skill players (Marsh, Relph, Freeman, Klakring)
4. **Penalty Kill**: Leverage defensive depth (Berry, Butler, Silliker, Tegart)
5. Plan backup units (important with player absences)

**Output**: Special teams units with formations and player positioning

### Workflow 5: Tournament Planning

**Scenario**: Planning lineup strategy for multi-game weekend

**Steps**:
1. Review tournament considerations in `references/game-planning.md`
2. Plan game-by-game approach (balanced early, competitive later)
3. Consider goalie rotation (Haffey/Schuchart split)
4. Build depth charts for each game
5. Plan ice time management strategy (four-line depth is advantage)
6. Ensure development players get opportunities in appropriate games

**Output**: Tournament game plans with adjusted lineups for each game

### Workflow 6: Managing Player Absences

**Scenario**: Key players unavailable for game (common at 18U)

**Steps**:
1. Assess which position is affected
2. Use F/D versatile players to fill gaps (9 D-capable players is key advantage)
3. Promote from lower lines
4. Adjust strategy based on available personnel
5. Communicate lineup changes to team

**Output**: Modified lineup that maintains competitive balance despite absences

## Lineup Building Principles

### Always Consider

**Team Identity - "Balanced Depth"**:
- Spread talent across all four lines (don't overload top line)
- Everyone contributes meaningfully
- Wear opponents down over 60 minutes
- Third period is our period (depth advantage emerges)
- Defense-first structure

**Development Focus**:
- This is C-level competitive hockey - balance winning with growth
- Rotate players through different line positions
- Provide opportunities in appropriate situations
- Everyone gets meaningful ice time (especially tournaments)
- **Critical**: Shelter Cram (2.50) and Thompson (3.00) but give them chances

**Strategic Assets**:
- **9 defensive-capable players** - biggest advantage, use it!
- **6 F/D versatile players** - maximize flexibility
- **Four-line capability** - can roll lines when others can't
- **Strong penalty kill foundation** - defensive depth pays off

**Chemistry Indicators**:
- Players who've succeeded together before
- Complementary playing styles
- Communication on ice
- Work rate matching
- Speed/skill/size balance

### Avoid

- Overloading top line (spread the wealth)
- Same combinations every game (explore options)
- Ignoring F/D versatile players (they're strategic gold)
- Forgetting about special teams when building 5v5 lines
- Making too many changes at once (adjust gradually)
- Overexposing Cram or Thompson in tough situations
- Trying to match Paul's elite speed (play to our strengths)

## Special Considerations

### Top Elite Players (1.00 Rating)

**Shaya Marsh (F/D, 1.00)** and **Massey Relph (F/D, 1.00)**:
- Core of top line and special teams units
- Most ice time in critical situations
- Both can play forward OR defense (huge flexibility)
- Leadership roles on ice
- Coach's son (Relph) - balanced treatment, high expectations

### Development Players (2.50+)

**Ender Cram (F, 2.50)**:
- Needs sheltered minutes with strong linemates
- Pair with 1.50-1.75 players for support
- Third/fourth line deployment
- Offensive zone starts when possible
- Give chances to develop, but protect from tough matchups

**Timothy Thompson (D, 3.00)**:
- Needs significant sheltering and skating development
- Always pair with strong, experienced D partner
- Limited ice time in critical situations
- Third defense pair typically
- Focus on simple, structured play
- Extra practice time on skating recommended

### Versatile F/D Players (Strategic Gold)

Six players can play both forward AND defense:
- **Marsh (1.00)** - elite at both, can solve any problem
- **Relph (1.00)** - elite at both, ultimate flexibility
- **Freeman (1.50)** - strong at both positions
- **Berry (2.00)** - solid depth at both
- **Silliker (1.50)** - can help on defense if needed
- **Tegart (2.00)** - versatile depth player

**Strategic Uses**:
- Fill gaps when injuries/absences occur (huge at 18U level)
- Create unique matchup advantages
- Provide rest to tired position groups
- Experiment with different combinations
- Add depth where needed most in specific games
- **This is our biggest advantage** - 9 D-capable players vs most teams' 6

### Goalie Management

**Two capable goalies**:
- **Cas Haffey** - Can also play forward if desperate
- **Gregor Schuchart** - Can also play defense if desperate

**Season strategy**:
- Roughly 50/50 game split
- Both get tournament experience
- Consider opponent strength, back-to-backs
- Communicate starter 24-48 hours ahead
- Emergency skater flexibility unique advantage

## Using the Lineup Generator Script

The `scripts/lineup_generator.py` tool creates formatted lineup sheets for the 18U Navy team.

**Basic usage**:
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

**When to use**:
- Creating official lineup sheets for games
- Generating multiple lineup scenarios for comparison
- Documenting lineup decisions
- Sharing with assistant coaches/parents

## Output Formats

Depending on the request, create outputs in the most appropriate format:

**Text-based lineups**: Simple, clear text format using the script or manual formatting

**Document artifacts**: Word/PDF documents for printing and distribution (use brand colors from project files)

**Interactive artifacts**: React components for lineup experimentation and visualization

**Spreadsheets**: Excel files for tracking lineups across season, analyzing player combinations

**Presentation slides**: PowerPoint for team meetings or parent presentations

**Email templates**: Formatted lineup emails using team contact lists from project files

## Common Questions & Scenarios

**Q: How do I balance development vs winning at 18U C level?**
- League games: 4 lines, balanced ice time, focus on structure
- Close games: 3 lines, best players more ice time, but everyone plays
- Tournaments: Pool play = development, playoffs = competitive
- Always shelter Cram and Thompson, but give them opportunities

**Q: When should I use 3 vs 4 forward lines?**
- **4 lines**: Most games (our strength!), when depth wears opponents down, balanced skill distribution
- **3 lines**: Very close playoff games, when opponents are very weak (maximize top players' growth), short-handed due to absences

**Q: How do I leverage our 9 D-capable players advantage?**
- Fresh legs on defense all game (opponents tire faster)
- Aggressive forechecking (know we have D depth)
- Match lines - put defensive-minded forwards against tough opponents
- Cover absences easily (biggest advantage at 18U level)
- Move players around based on opponent style

**Q: What if key players are absent?** (common at 18U)
- **Use F/D players**: Move Marsh, Relph, Freeman, Berry, Silliker, Tegart where needed
- **Promote from lower lines**: 2.00 players step up
- **Adjust strategy**: More defensive, structured approach
- **Don't panic**: Depth is our strength, we can handle it

**Q: How do I handle Cram and Thompson?**
- **Cram (2.50)**: Third/fourth line, pair with 1.50+ players, offensive zone starts, limited PK
- **Thompson (3.00)**: Third pair D, always with strong partner (Young, Berry, Butler), limited critical situations, simple assignments
- **Both**: Give opportunities to develop, but protect from overwhelming situations

**Q: What's our strategy against Paul's team?**
- **Their strength**: Elite top-6 forwards (four 1.25 players)
- **Their weakness**: Only 6 D-capable players (vs our 9)
- **Our approach**: 
  - Grind them down with four lines
  - Heavy forecheck (force their tired D to make mistakes)
  - Strong penalty kill (they'll try to use PP)
  - Third period is ours (depth advantage emerges)
  - Match our top line against their top line, wear them with depth

**Q: Which goalie should start?**
- Recent performance matters most
- Consider opponent strength (Haffey for skill teams, Schuchart for physical)
- Back-to-back games: split duty
- Communicate decision 24-48 hours ahead
- Both goalies always prepare fully

## Tips for Success

1. **Embrace four-line depth**: It's our identity and biggest strength
2. **Trust the system**: Defense-first structure, grind it out, win third periods
3. **Leverage versatility**: 6 F/D players = problem-solving capability
4. **Track what works**: Keep notes on successful combinations
5. **Communicate clearly**: Explain changes to players and parents
6. **Stay flexible**: Be ready to adjust based on game flow and absences
7. **Protect developing players**: Give Cram and Thompson opportunities in right situations
8. **Focus on structure**: We win through team defense, not just skill
9. **Plan for absences**: At 18U, always have backup plan
10. **Review regularly**: Assess lineup effectiveness after games

## Matchup Strategy: Navy vs White (Paul's Team)

When playing Paul's team, consider:

**What we do better**:
- Four-line depth (we can roll, they need their top 6)
- Defensive depth (9 vs 6 D-capable)
- Grinding, physical style
- Third period stamina
- Penalty kill depth

**What they do better**:
- Elite top-6 skill (four 1.25 players)
- Speed-based offense
- Power play weapons
- Offensive talent concentration

**Our winning strategy**:
1. Heavy forecheck - force turnovers from their tired D
2. Roll four lines - wear them down
3. Strong penalty kill - neutralize their PP advantage
4. Physical play - make them earn everything
5. Control third period - depth advantage emerges
6. Exploit their six D-man limitation - they have no injury margin

## Integration with Other Team Functions

This skill complements other aspects of team management:
- **Schedule planning**: Understanding lineup fatigue over season
- **Player development**: Targeted ice time in specific situations
- **Team communication**: Explaining lineup philosophy to parents
- **Tournament selection**: Knowing lineup depth for different competition levels
- **Email communication**: Use project email lists for lineup distribution
- **Brand consistency**: Use Kraken colors from project files for materials

## Additional Notes

- **Practice application**: Use practice time to test new line combinations
- **Video review**: Record and analyze successful/struggling line combinations
- **Player feedback**: Regular check-ins help understand comfort levels
- **Parent communication**: Be transparent about ice time philosophy and lineup decisions (especially for development players)
- **Seasonal progression**: Lineups should evolve as players develop and chemistry builds
- **Absence planning**: CRITICAL at 18U - always have contingency plans
- **Development tracking**: Monitor Cram and Thompson progress throughout season

When building lineups, always remember: **We are Coach Mark's Navy team. We win through Balanced Depth, defensive structure, four-line rotation, and grinding determination. We wear opponents down and win third periods.**
