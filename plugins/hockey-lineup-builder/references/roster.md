# Team Roster

> **This is a starter template.** It is regenerated automatically when you run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py <roster_file.xlsx>` (or `.csv`, or `--json`).
>
> Until you import a roster, the lineup-building workflow has no players to work with. See [`roster-management.md`](roster-management.md) for the import process and expected file format.

## Team Overview

- **Team Name**: _(set in `.claude/hockey-lineup-builder.local.md`)_
- **Total Players**: _(populated after import)_
- **Forwards**: _(populated after import)_
- **Defense**: _(populated after import)_
- **Goalies**: _(populated after import)_

## Player Rating Scale

The default scale is **1.00–3.00 (lower is better)**:

- **1.00**: Elite — top tier for the league/level
- **1.50**: Strong Skilled — solid contributor
- **1.75**: Strong Two-Way — reliable player
- **2.00**: Developing Contributor — consistent middle tier
- **2.50**: Developing — needs sheltered minutes
- **3.00**: Significant Development — requires heavy sheltering

The roster import script also accepts a 1–5 scale; ratings outside 0.50–5.00 generate a warning.

## How to Populate This File

1. Prepare an Excel, CSV, or JSON file with at least `Name` and `Rating` columns. See [`roster-management.md`](roster-management.md) for column aliases and examples.
2. Run the import:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/update_roster.py path/to/roster.xlsx
   ```
3. The script regenerates this file with player tables, positional depth analysis, and tier breakdowns, and updates the roster dict in `scripts/lineup_generator.py`.

For a worked example of what a populated roster looks like, see [`examples/jr-kraken-18u-navy/roster.md`](../examples/jr-kraken-18u-navy/roster.md).
