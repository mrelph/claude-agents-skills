# Changelog - Jr Kraken 18U Navy Lineup Skill

All notable changes to the jr-kraken-18u-navy-lineup skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-03-09

### Changed

- **Dynamic roster**: Player names and ratings are no longer hardcoded in strategy/planning files
  - `references/roster.md` is now the single source of truth for all player names and ratings
  - `references/game-planning.md` references players by tier/rating (e.g., "elite tier", "1.50-rated F/D player") instead of by name
  - `references/coach-strategy.md` (renamed from `mark-strategy.md`) uses tier-based language throughout
  - `README.md` and `SKILL.md` reference `roster.md` instead of listing names inline
- Renamed `references/mark-strategy.md` to `references/coach-strategy.md`
- Generalized opponent strategy sections — removed all references to specific rival teams; replaced with generic templates (vs elite skill, vs physical, vs speed, vs weak, vs unknown)
- Generalized `examples/sample_lineup_request.md` to use generic opponent and role references
- Renamed `generate_vs_paul_lineup()` to `generate_vs_elite_rival_lineup()` in lineup generator

### Added

- **TeamSnap MCP integration** for real-time RSVP checking
  - Uses `mcp__teamsnap__*` tools when available to pull game RSVPs
  - Maps RSVP statuses (Yes/No/Maybe/No Response) to roster for lineup building
  - Graceful fallback to manual availability check when TeamSnap MCP is not configured
  - Added `mcp__teamsnap__*` to allowed-tools
- **Roster update script** (`scripts/update_roster.py`)
  - Reads Excel (.xlsx), CSV, or inline JSON with updated player ratings/positions
  - Auto-generates `references/roster.md` with tier groupings, positional depth analysis, and deployment notes
  - Updates the internal roster dict in `scripts/lineup_generator.py` to stay in sync
  - Flexible column name matching (Name/Player, Rating/Power Ranking/Score, etc.)
  - Supports `--dry-run` for previewing changes without writing files
  - Validates ratings and warns on unusual values
- **Strategy file update capability**
  - Skill can now edit `coach-strategy.md` and `game-planning.md` when asked
  - Documented common update scenarios (add opponent, update PK/PP, post-game learnings, evolving identity)
  - Rules enforce name-free edits, targeted changes, and user confirmation before writing

## [1.0.0] - 2025-12-09

### Added

- Initial release of jr-kraken-18u-navy-lineup skill
- Comprehensive lineup building system for Jr. Kraken 18U C Navy Team (Coach Mark)
- Complete 17-player roster knowledge
  - 15 skaters (12 forwards, 9 defense-capable players)
  - 2 goalies (both can play out if needed)
  - Player ratings on 1.00-3.00 scale (1.00 = elite, 3.00 = development)
  - Positional flexibility tracking (F, D, F/D)
- "Balanced Depth" coaching philosophy
  - Four-line rotation strategy
  - Defense-first structure
  - Grinding, attrition-based style
  - Third-period strength through depth
- Line combination and pairing strategies
  - 3-line vs 4-line forward rotation guidance
  - Defense pairing philosophies
  - Chemistry factor considerations
  - Line composition principles for 18U C level
- Special teams planning
  - Power play formations (umbrella setup)
  - Penalty kill structures (box+1)
  - Unit depth and backup planning
  - PK-focused approach (leveraging defensive depth)
- Game planning framework
  - Pre-game opponent scouting checklist
  - Step-by-step lineup construction process
  - In-game adjustment triggers and strategies
  - Post-game analysis framework
- Tournament strategy
  - Multi-game lineup planning
  - Ice time management across games
  - Development player opportunities in appropriate games
  - Goalie rotation strategy
- Player management
  - Development player sheltering (Cram 2.50, Thompson 3.00)
  - F/D versatile player deployment (6 players)
  - Managing player absences (common at 18U)
  - Balanced ice time distribution
- Head-to-head strategy vs Paul's White Team
  - Exploiting opponent weaknesses (limited D depth)
  - Leveraging Navy's advantages (9 D-capable vs 6)
  - Four-line grinding approach
  - Heavy forecheck tactics
- Python lineup generator script
  - Formatted lineup sheet creation
  - Multiple scenario comparison
  - Documentation and sharing capabilities
- Reference documentation
  - roster.md: Complete player profiles and ratings
  - mark-strategy.md: Coaching philosophy and team identity
  - formations.md: Line structures and special teams
  - game-planning.md: Pre-game, in-game, post-game processes

### Features

- **Strategic Asset Utilization**: 9 defensive-capable players (vs typical 6)
- **Versatility**: 6 F/D players for maximum flexibility
- **Development Focus**: Balanced winning with player growth at C-level
- **Four-Line Capability**: Depth advantage in wearing down opponents
- **Special Situations**: Strong penalty kill foundation
- **Adaptability**: Handling frequent player absences at 18U level
- **Multiple Output Formats**: Text, Word/PDF, interactive, spreadsheets, presentations, emails

### Workflows

1. **Game Day Lineup Building**: Complete lineup with forward lines, defense pairs, special teams
2. **Strategic Game Planning**: Opponent-specific strategies and matchup plans
3. **In-Game Adjustments**: Line shuffles and tactical changes during games
4. **Special Teams Optimization**: PP and PK unit construction
5. **Tournament Planning**: Multi-game strategy and depth chart management
6. **Managing Player Absences**: Lineup modifications for unavailable players

### Tool Access

- Read: Loading roster and reference documents
- Bash: Running lineup generator scripts
- Write: Creating lineup sheets and game plans
- Glob: Finding project files (contact lists, brand assets)
- Grep: Searching through team information
- AskUserQuestion: Clarifying availability, opponent info, strategic preferences

### Target Users

- Coach Mark (Jr Kraken 18U C Navy)
- Assistant coaches and team staff
- Team management and administration
- Parents (for lineup communication)

### Key Team Attributes

- **17 total players**: 15 skaters + 2 goalies
- **Elite players**: Marsh (F/D, 1.00), Relph (F/D, 1.00)
- **Strong core**: Freeman, Klakring, Silliker (1.50)
- **Solid middle tier**: 8 players at 1.75-2.00
- **Development players**: Cram (F, 2.50), Thompson (D, 3.00)
- **Defensive depth**: 9 D-capable players (major advantage)
- **Forward depth**: 12 F-capable players (enables 4-line rotation)

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for roster changes or philosophy shifts
- MINOR version for new features or significant strategy additions
- PATCH version for minor updates, corrections, or documentation improvements

See also: SKILL.md for detailed workflow and usage instructions
