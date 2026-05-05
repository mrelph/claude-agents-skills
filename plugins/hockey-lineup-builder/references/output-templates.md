# Output Templates — Branded Lineup Documents

**Only generate these documents after the coach explicitly locks the lineup.** Until then, all work stays in plain text or `lineup_generator.py` output. Trigger phrases: "locked", "finalized", "good to go", "that's it", "print it".

Once locked, produce three Word documents using the **Word skill**. If the team has a configured branding skill (see `.claude/hockey-lineup-builder.local.md` → `Branding skill`), apply that skill's color palette, typography, and logo guidance to all three documents. If no branding skill is configured but the user provided custom branding notes, follow those notes. If neither is set, produce clean unbranded documents.

## Document 1: Bench Card

A compact, laminate-ready reference card for the coach to hold on the bench during the game.

**Contents**:
- Game header: opponent, date, time, location
- Forward lines: Line 1-4 with LW / C / RW and line role (Offensive, Two-Way, Energy, Matchup)
- Defense pairs: Pair 1-3 with LD / RD and pair role (Shutdown, Two-Way, Depth)
- Goalies: starter and backup
- Power play units: PP1 and PP2 with players and formation (umbrella / overload)
- Penalty kill units: PK1 and PK2 with players and system (box+1 / passive)
- Goalie rotation notes (if tournament / back-to-back)
- Situational notes: late game (protecting lead / need goal), overtime shifts

**Format**: single page, landscape orientation, dense layout with clear sections. Designed to be printed, laminated, and used on the bench. Large enough font to read at a glance.

## Document 2: Lineup Poster

A locker room display for the team to see before the game.

**Contents**:
- Game header: "[TEAM NAME] vs [OPPONENT]" with date and location
- Forward lines: Line 1-4 with player names and numbers in a clear visual layout
- Defense pairs: Pair 1-3 with player names
- Goalies: starter (highlighted) and backup
- Special teams: PP and PK units
- Game focus: 2-3 tactical bullet points for this game
- Team identity reminder: tagline or motivational message (from `team-strategy.md`)

**Format**: single page, portrait orientation, clean and bold. Designed to be printed large (11x17 or taped to the locker room wall). Player names should be prominent. Apply configured branding throughout.

## Document 3: Coach Strategy Summary

A game plan overview for the head coach and assistant coaches.

**Contents**:
- Game header: opponent, date, time, location, game type (league / tournament / playoff)
- Opponent scouting: their style, strengths, weaknesses, key threats (if known)
- Strategic objectives: 2-3 tactical priorities for this game
- Our response strategy: how the team's identity counters this opponent
- Full lineup: forward lines, defense pairs, goalies with ratings and roles
- Key matchups: which lines to deploy against opponent's top players
- Special teams: PP and PK units with formations
- Deployment plan: ice time targets per line/pair, zone start preferences
- Adjustment triggers: what to watch for and how to respond
- Period-by-period approach: P1 / P2 / P3 plan
- Communication notes: pre-game message, key coaching points

**Format**: 1-2 pages, portrait orientation, detailed but scannable. Sections with headers, bullet points, and tables. Designed for the coach to review before the game and reference during intermissions. Apply branding on header/footer.

## When to Generate Which Documents

| Scenario | Text | Bench Card | Lineup Poster | Strategy Summary |
|----------|------|------------|---------------|------------------|
| Quick lineup check | Yes | No | No | No |
| Standard league game | Yes | Yes | Yes | Optional |
| Rivalry / tough opponent | Yes | Yes | Yes | Yes |
| Tournament game | Yes | Yes | Yes | Yes |
| Playoff game | Yes | Yes | Yes | Yes |
| In-game adjustment | Yes | No | No | No |

## Branding

The skill checks `.claude/hockey-lineup-builder.local.md` for a configured branding source:

- **Branding skill**: a named skill (e.g. `anthropic-skills:jr-kraken-brand`) — invoke that skill before generating documents so its color palette, typography, and logo guidance are loaded.
- **Branding notes**: free-form text describing colors, fonts, taglines — apply manually.
- **None / unbranded**: produce clean, professional documents without team-specific styling.

Always ask the user to confirm the branding choice if it has not been set or if the user requests a one-off override.

## Other Output Formats

For non-standard requests, the skill can also produce:
- **Email templates** — formatted lineup emails with game details, lineup, and tactical focus
- **Spreadsheets** — season tracking, player combinations, ice time analysis (use Excel skill)
- **Presentation slides** — team meetings or parent presentations (use PowerPoint skill)
