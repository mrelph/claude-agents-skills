# Changelog - Jr Kraken Dev Team Lineup Skill

All notable changes to the jr-kraken-dev-team-lineup skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-03-09

### Added

- Initial release of jr-kraken-dev-team-lineup skill
- Duplicated from jr-kraken-18u-navy-lineup and adapted for the Dev Team
- "Competitive Excellence" coaching philosophy (replaces "Balanced Depth")
  - Ranking-driven deployment: lines built by player rankings, purpose, and game situations
  - Advanced tactical execution across all lines
  - Every line has a defined mission
  - Merit-based ice time driven by performance and rankings
  - No sheltering/protecting language -- all players compete for their role
- Empty roster template -- ready for roster upload
  - Upload via Excel, CSV, or JSON
  - `scripts/update_roster.py` populates roster and lineup generator
  - Tier naming: Elite, Strong, Role (replaces Elite, Strong, Development)
- Comprehensive lineup building system
  - 3-line vs 4-line forward rotation guidance
  - Defense pairing philosophies
  - Special teams formations (PP umbrella/overload, PK box+1/passive)
  - Line deployment by zone and game situation
- Game planning framework
  - Pre-game preparation checklist
  - Opponent scouting framework
  - Step-by-step lineup construction (8 steps)
  - Game strategy templates (vs elite skill, vs physical, vs weak, vs unknown)
  - In-game adjustment triggers and strategies
  - Post-game analysis framework with ranking review
  - Tournament strategy (pool play vs playoffs)
- TeamSnap MCP integration for RSVP checking
- Python lineup generator script (`DevTeamLineupGenerator`)
- Kraken-branded document output (bench card, lineup poster, coach strategy summary)

### Changed from Navy Skill

- Team identity: "Competitive Excellence" (was "Balanced Depth")
- Removed all "developing players" / sheltering / isolating language
- Removed player protection guidelines and sheltering sections
- Role players have "defined roles" instead of "sheltered minutes"
- Bottom tier renamed from "Development" to "Role Players"
- Strategy focuses on advanced play and system execution
- Lines driven by rankings and purpose, not balanced development
- Removed development progression goals (replaced with role execution)
- Communication messaging emphasizes compete level and accountability
- Roster starts empty (vs pre-populated with 18U C Navy roster)

### Tool Access

- Read: Loading roster and reference documents
- Bash: Running lineup generator scripts
- Write: Creating lineup sheets and game plans
- Glob: Finding project files
- Grep: Searching through team information
- AskUserQuestion: Clarifying availability, opponent info, strategic preferences
- mcp__teamsnap__*: TeamSnap RSVP integration

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for roster changes or philosophy shifts
- MINOR version for new features or significant strategy additions
- PATCH version for minor updates, corrections, or documentation improvements

See also: SKILL.md for detailed workflow and usage instructions
