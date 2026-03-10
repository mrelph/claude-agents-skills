# Jr. Kraken Development Team Roster - Coach Mark

## Team Overview
- **Head Coach**: Mark
- **Team Identity**: "Competitive Excellence"
- **Total Players**: -- (upload roster to populate)
- **Forwards**: --
- **Defense**: --
- **Goalies**: --
- **Average Rating**: --

> **This roster is empty.** Upload an Excel (.xlsx) or CSV file with player ratings to populate this roster.
>
> Run: `python3 scripts/update_roster.py <path_to_roster_file>`
>
> See `SKILL.md` for expected file format and column details.

## Player Rating Scale
- **1.00**: Elite - Top performer
- **1.50**: Strong Skilled - Consistent high-level contributor
- **1.75**: Strong Two-Way - Reliable player
- **2.00**: Solid Contributor - Consistent middle tier
- **2.50**: Role Player - Situational contributor with defined assignments
- **3.00**: Role Player - Specific role, targeted deployment

---

## How to Populate This Roster

### Option 1: Excel or CSV File

Prepare a file with at minimum these columns:

| Column | Required | Example |
|--------|----------|---------|
| Name | Yes | Player Name |
| Rating | Yes | 1.50 |
| Position | No (defaults to F) | F, D, F/D, G |
| Notes | No | Strong two-way player |

Then run:
```bash
python3 scripts/update_roster.py <path_to_file.xlsx>
```

### Option 2: JSON Inline

```bash
python3 scripts/update_roster.py --json '{"players": [
  {"name": "Player One", "position": "F/D", "rating": 1.00, "notes": "Elite"},
  {"name": "Player Two", "position": "D", "rating": 1.75, "notes": "Reliable defender"}
]}'
```

### Option 3: Dry Run (Preview)

```bash
python3 scripts/update_roster.py --dry-run <path_to_file.xlsx>
```

---

**Once populated, this file will contain**: Full player roster organized by tier, positional depth analysis, F/D versatile player list, special teams personnel, line combination templates, and absence contingency plans.
