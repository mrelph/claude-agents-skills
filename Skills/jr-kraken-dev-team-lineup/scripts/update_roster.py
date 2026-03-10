#!/usr/bin/env python3
"""
Jr Kraken Development Team - Roster & Power Rankings Updater

Reads an Excel (.xlsx) or CSV file containing updated player ratings/positions
and regenerates references/roster.md and the roster dict in lineup_generator.py.

Supports both 1-3 and 1-5 rating scales (auto-detected from data).

Expected columns (case-insensitive, flexible matching):
  - Name (or Player, Player Name)
  - Position (or Pos) — F, D, F/D, G
  - Rating (or Power Ranking, Rank, Score) — 1-3 or 1-5 scale
  - Notes (optional)
  - Can Also Play (optional, for goalies)

Usage:
  python3 update_roster.py <path_to_file.xlsx>
  python3 update_roster.py <path_to_file.csv>
  python3 update_roster.py --json '{"players": [...]}'
  python3 update_roster.py --scale 5 <path_to_file.xlsx>   # Force 1-5 scale
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ROSTER_MD = SKILL_DIR / "references" / "roster.md"
LINEUP_GEN = SCRIPT_DIR / "lineup_generator.py"

# Column name aliases (lowercase)
NAME_COLS = {"name", "player", "player name", "player_name", "playername"}
POS_COLS = {"position", "pos", "pos."}
RATING_COLS = {"rating", "power ranking", "power_ranking", "rank", "score", "powerranking"}
NOTES_COLS = {"notes", "note", "comments", "comment"}
ALT_POS_COLS = {"can also play", "can_also_play", "alt position", "alt_position", "alternate"}

# --- Rating scale definitions ---
# Each scale defines tier boundaries and labels.
# Lower rating = better player on both scales.

SCALES = {
    3: {
        "name": "1-3",
        "max": 3.00,
        "elite_top_max": 1.00,
        "elite_strong_max": 1.50,
        "strong_twoway_max": 1.75,
        "strong_middle_max": 2.00,
        "role_situational_max": 2.50,
        # role_specific = everything above role_situational_max
        "labels": [
            ("1.00", "Elite - Top performer"),
            ("1.50", "Strong Skilled - Consistent high-level contributor"),
            ("1.75", "Strong Two-Way - Reliable player"),
            ("2.00", "Solid Contributor - Consistent middle tier"),
            ("2.50", "Role Player - Situational contributor with defined assignments"),
            ("3.00", "Role Player - Specific role, targeted deployment"),
        ],
        "elite_range": "1.00-1.50",
        "strong_range": "1.75-2.00",
        "role_range": "2.50+",
        "elite_depth_max": 1.50,
        "strong_depth_max": 2.00,
        "good_avg_threshold": 2.00,
        "warn_low": 0.50,
        "warn_high": 5.00,
    },
    5: {
        "name": "1-5",
        "max": 5.00,
        "elite_top_max": 1.50,
        "elite_strong_max": 2.50,
        "strong_twoway_max": 3.00,
        "strong_middle_max": 3.50,
        "role_situational_max": 4.25,
        "labels": [
            ("1.00-1.50", "Elite - Top performer"),
            ("1.75-2.50", "Strong Skilled - Consistent high-level contributor"),
            ("2.75-3.00", "Strong Two-Way - Reliable player"),
            ("3.25-3.50", "Solid Contributor - Consistent middle tier"),
            ("3.75-4.25", "Role Player - Situational contributor with defined assignments"),
            ("4.50-5.00", "Role Player - Specific role, targeted deployment"),
        ],
        "elite_range": "1.00-2.50",
        "strong_range": "2.75-3.50",
        "role_range": "3.75+",
        "elite_depth_max": 2.50,
        "strong_depth_max": 3.50,
        "good_avg_threshold": 3.33,
        "warn_low": 0.50,
        "warn_high": 7.00,
    },
}


def detect_scale(players: List[Dict]) -> int:
    """Auto-detect rating scale from player data. Returns 3 or 5."""
    max_rating = max(p["rating"] for p in players) if players else 1.0
    return 5 if max_rating > 3.0 else 3


def find_column(headers: List[str], aliases: set) -> Optional[int]:
    """Find column index matching any alias."""
    for i, h in enumerate(headers):
        if h.strip().lower() in aliases:
            return i
    return None


def read_csv(path: str) -> List[Dict]:
    """Read players from CSV file."""
    players = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        name_i = find_column(headers, NAME_COLS)
        pos_i = find_column(headers, POS_COLS)
        rating_i = find_column(headers, RATING_COLS)
        notes_i = find_column(headers, NOTES_COLS)
        alt_i = find_column(headers, ALT_POS_COLS)

        if name_i is None or rating_i is None:
            print(f"ERROR: Could not find required columns. Found headers: {headers}")
            print(f"  Need a 'Name' column (tried: {NAME_COLS})")
            print(f"  Need a 'Rating' column (tried: {RATING_COLS})")
            sys.exit(1)

        for row in reader:
            if not row or not row[name_i].strip():
                continue
            player = {
                "name": row[name_i].strip(),
                "position": row[pos_i].strip() if pos_i is not None and pos_i < len(row) else "F",
                "rating": float(row[rating_i].strip()),
                "notes": row[notes_i].strip() if notes_i is not None and notes_i < len(row) else "",
                "can_also_play": row[alt_i].strip() if alt_i is not None and alt_i < len(row) else "",
            }
            players.append(player)
    return players


def read_excel(path: str) -> List[Dict]:
    """Read players from Excel file. Requires openpyxl."""
    try:
        import openpyxl
    except ImportError:
        print("ERROR: openpyxl is required to read Excel files.")
        print("  Install with: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("ERROR: Excel file is empty.")
        sys.exit(1)

    headers = [str(h) if h else "" for h in rows[0]]
    name_i = find_column(headers, NAME_COLS)
    pos_i = find_column(headers, POS_COLS)
    rating_i = find_column(headers, RATING_COLS)
    notes_i = find_column(headers, NOTES_COLS)
    alt_i = find_column(headers, ALT_POS_COLS)

    if name_i is None or rating_i is None:
        print(f"ERROR: Could not find required columns. Found headers: {headers}")
        print(f"  Need a 'Name' column (tried: {NAME_COLS})")
        print(f"  Need a 'Rating' column (tried: {RATING_COLS})")
        sys.exit(1)

    players = []
    for row in rows[1:]:
        if not row[name_i]:
            continue
        player = {
            "name": str(row[name_i]).strip(),
            "position": str(row[pos_i]).strip() if pos_i is not None and row[pos_i] else "F",
            "rating": float(row[rating_i]),
            "notes": str(row[notes_i]).strip() if notes_i is not None and row[notes_i] else "",
            "can_also_play": str(row[alt_i]).strip() if alt_i is not None and row[alt_i] else "",
        }
        players.append(player)

    wb.close()
    return players


def read_json_string(json_str: str) -> List[Dict]:
    """Read players from a JSON string."""
    data = json.loads(json_str)
    if isinstance(data, dict) and "players" in data:
        data = data["players"]
    if not isinstance(data, list):
        print("ERROR: JSON must be a list of players or {\"players\": [...]}.")
        sys.exit(1)
    players = []
    for p in data:
        players.append({
            "name": p["name"],
            "position": p.get("position", "F"),
            "rating": float(p["rating"]),
            "notes": p.get("notes", ""),
            "can_also_play": p.get("can_also_play", ""),
        })
    return players


def categorize_players(players: List[Dict], scale: int) -> Dict:
    """Categorize players into tiers and positions using scale-appropriate boundaries."""
    s = SCALES[scale]
    goalies = [p for p in players if p["position"].upper() == "G"]
    skaters = [p for p in players if p["position"].upper() != "G"]

    elite_top = [p for p in skaters if p["rating"] <= s["elite_top_max"]]
    elite_strong = [p for p in skaters if s["elite_top_max"] < p["rating"] <= s["elite_strong_max"]]
    strong_twoway = [p for p in skaters if s["elite_strong_max"] < p["rating"] <= s["strong_twoway_max"]]
    strong_middle = [p for p in skaters if s["strong_twoway_max"] < p["rating"] <= s["strong_middle_max"]]
    role_situational = [p for p in skaters if s["strong_middle_max"] < p["rating"] <= s["role_situational_max"]]
    role_specific = [p for p in skaters if p["rating"] > s["role_situational_max"]]

    fd_versatile = [p for p in skaters if p["position"].upper() == "F/D"]
    forwards = [p for p in skaters if "F" in p["position"].upper()]
    defense = [p for p in skaters if "D" in p["position"].upper()]

    avg_rating = sum(p["rating"] for p in skaters) / len(skaters) if skaters else 0

    return {
        "goalies": goalies,
        "skaters": skaters,
        "elite_top": elite_top,
        "elite_strong": elite_strong,
        "strong_twoway": strong_twoway,
        "strong_middle": strong_middle,
        "role_situational": role_situational,
        "role_specific": role_specific,
        "fd_versatile": fd_versatile,
        "forwards": forwards,
        "defense": defense,
        "avg_rating": avg_rating,
        "scale": scale,
    }


def generate_roster_md(players: List[Dict], scale: int) -> str:
    """Generate the full roster.md content from player data."""
    s = SCALES[scale]
    cats = categorize_players(players, scale)
    goalies = cats["goalies"]
    skaters = cats["skaters"]
    fd = cats["fd_versatile"]

    total = len(players)
    skater_count = len(skaters)
    goalie_count = len(goalies)
    fwd_count = len(cats["forwards"])
    def_count = len(cats["defense"])
    fd_count = len(fd)
    dedicated_f = fwd_count - fd_count
    dedicated_d = def_count - fd_count

    lines = []
    lines.append("# Jr. Kraken Development Team Roster - Coach Mark")
    lines.append("")
    lines.append("## Team Overview")
    lines.append(f"- **Head Coach**: Mark")
    lines.append(f'- **Team Identity**: "Competitive Excellence"')
    lines.append(f"- **Rating Scale**: {s['name']} (lower is better)")
    lines.append(f"- **Total Players**: {total} ({skater_count} skaters + {goalie_count} goalies)")
    lines.append(f"- **Forwards**: {dedicated_f} dedicated + {fd_count} F/D versatile = **{fwd_count} capable forwards**")
    lines.append(f"- **Defense**: {dedicated_d} dedicated + {fd_count} F/D versatile = **{def_count} capable defensemen**" + (" -- DEPTH ADVANTAGE" if def_count >= 8 else ""))
    lines.append(f"- **Goalies**: {goalie_count} ({', '.join(g['name'] for g in goalies)})")
    lines.append(f"- **Average Rating**: {cats['avg_rating']:.3f}" + (" (strong balance)" if cats['avg_rating'] < s['good_avg_threshold'] else ""))
    lines.append("")
    lines.append(f"> **Last updated**: This roster was auto-generated by `scripts/update_roster.py` using the **{s['name']}** rating scale.")
    lines.append("> To refresh, run: `python3 scripts/update_roster.py <roster_file.xlsx>`")
    lines.append("")
    lines.append("## Player Rating Scale")
    for val, desc in s["labels"]:
        lines.append(f"- **{val}**: {desc}")
    lines.append("")
    lines.append("---")

    # Goalies section
    if goalies:
        lines.append("")
        lines.append(f"## GOALIES ({goalie_count})")
        lines.append("")
        lines.append("| Name | Rating | Notes | Can Also Play |")
        lines.append("|------|--------|-------|---------------|")
        for g in goalies:
            lines.append(f"| **{g['name']}** | {g['rating']:.2f} | {g['notes']} | {g['can_also_play']} |")
        lines.append("")
        lines.append("**Goalie Strategy**: ")
        lines.append("- Starts based on performance, opponent strength, and game situation")
        lines.append("- Both get tournament experience")
        lines.append("- Communicate starter 24-48 hours ahead")
        lines.append("")
        lines.append("---")

    # Elite players
    def _player_table(group, pos_col=True):
        tbl = []
        if pos_col:
            tbl.append("| Name | Position | Rating | Notes |")
            tbl.append("|------|----------|--------|-------|")
            for p in sorted(group, key=lambda x: x["rating"]):
                tbl.append(f"| **{p['name']}** | {p['position']} | {p['rating']:.2f} | {p['notes']} |")
        else:
            tbl.append("| Name | Rating | Notes |")
            tbl.append("|------|--------|-------|")
            for p in sorted(group, key=lambda x: x["rating"]):
                tbl.append(f"| **{p['name']}** | {p['rating']:.2f} | {p['notes']} |")
        return tbl

    elite_all = cats["elite_top"] + cats["elite_strong"]
    if elite_all:
        lines.append("")
        lines.append(f"## ELITE PLAYERS ({s['elite_range']}) - {len(elite_all)} Players")
        if cats["elite_top"]:
            lines.append("")
            lines.append(f"### Top Tier (≤{s['elite_top_max']:.2f}) - {len(cats['elite_top'])} Players")
            lines.append("")
            lines.extend(_player_table(cats["elite_top"]))
            lines.append("")
            lines.append("**Deployment**: Core of top line and all special teams, most ice time in critical situations")
        if cats["elite_strong"]:
            lines.append("")
            lines.append(f"### Strong Skilled (≤{s['elite_strong_max']:.2f}) - {len(cats['elite_strong'])} Players")
            lines.append("")
            lines.extend(_player_table(cats["elite_strong"]))
            lines.append("")
            lines.append("**Deployment**: Top two lines, power play, penalty kill, high-leverage ice time")
        lines.append("")
        lines.append("---")

    # Strong players
    strong_all = cats["strong_twoway"] + cats["strong_middle"]
    if strong_all:
        lines.append("")
        lines.append(f"## STRONG PLAYERS ({s['strong_range']}) - {len(strong_all)} Players")
        if cats["strong_twoway"]:
            lines.append("")
            lines.append(f"### Two-Way Contributors (≤{s['strong_twoway_max']:.2f}) - {len(cats['strong_twoway'])} Players")
            lines.append("")
            lines.extend(_player_table(cats["strong_twoway"]))
        if cats["strong_middle"]:
            lines.append("")
            lines.append(f"### Solid Contributors (≤{s['strong_middle_max']:.2f}) - {len(cats['strong_middle'])} Players")
            lines.append("")
            lines.extend(_player_table(cats["strong_middle"]))
        lines.append("")
        lines.append(f"**Deployment**: These {len(strong_all)} players form the reliable core -- second and third lines, second and third defense pairs, consistent contributors who make four-line depth possible")
        lines.append("")
        lines.append("---")

    # Role players
    role_all = cats["role_situational"] + cats["role_specific"]
    if role_all:
        lines.append("")
        lines.append(f"## ROLE PLAYERS ({s['role_range']}) - {len(role_all)} Players")
        if cats["role_situational"]:
            lines.append("")
            lines.append(f"### Situational Contributors (≤{s['role_situational_max']:.2f})")
            lines.append("")
            lines.extend(_player_table(cats["role_situational"]))
            for p in cats["role_situational"]:
                lines.append("")
                lines.append(f"**{p['name'].split()[-1]} Role**:")
                lines.append("- Defined situational deployment")
                lines.append("- Play to specific strengths")
                lines.append("- Contribute within their role when called upon")
        if cats["role_specific"]:
            lines.append("")
            lines.append(f"### Targeted Role (>{s['role_situational_max']:.2f})")
            lines.append("")
            lines.extend(_player_table(cats["role_specific"]))
            for p in cats["role_specific"]:
                lines.append("")
                lines.append(f"**{p['name'].split()[-1]} Role**:")
                if "D" in p["position"].upper():
                    lines.append("- Depth defense pair deployment")
                    lines.append("- Pair with strong, experienced partner")
                    lines.append("- Defined, focused defensive assignments")
                else:
                    lines.append("- Depth forward deployment")
                    lines.append("- Defined role with clear assignments")
                    lines.append("- Contribute energy and compete level")
        lines.append("")
        lines.append("---")

    # Positional depth
    elite_max = s["elite_depth_max"]
    strong_max = s["strong_depth_max"]

    lines.append("")
    lines.append("## POSITIONAL DEPTH ANALYSIS")
    lines.append("")
    lines.append(f"### Forward Capability ({fwd_count} players)")
    lines.append("")
    lines.append("| Tier | Players |")
    lines.append("|------|---------|")
    elite_fwd = [p for p in cats["forwards"] if p["rating"] <= elite_max]
    strong_fwd = [p for p in cats["forwards"] if elite_max < p["rating"] <= strong_max]
    role_fwd = [p for p in cats["forwards"] if p["rating"] > strong_max]
    if elite_fwd:
        lines.append(f"| **Elite ({s['elite_range']})** | {', '.join(p['name'].split()[-1] for p in elite_fwd)} |")
    if strong_fwd:
        lines.append(f"| **Strong ({s['strong_range']})** | {', '.join(p['name'].split()[-1] for p in strong_fwd)} |")
    if role_fwd:
        lines.append(f"| **Role ({s['role_range']})** | {', '.join(p['name'].split()[-1] for p in role_fwd)} |")
    lines.append("")
    lines.append(f"**Four-Line Capability**: {'YES - Core strength' if fwd_count >= 12 else 'Possible with adjustments' if fwd_count >= 9 else 'Limited'}")

    lines.append("")
    lines.append(f"### Defensive Capability ({def_count} players)" + (" -- DEPTH ADVANTAGE" if def_count >= 8 else ""))
    lines.append("")
    lines.append("| Tier | Players |")
    lines.append("|------|---------|")
    elite_def = [p for p in cats["defense"] if p["rating"] <= elite_max]
    strong_def = [p for p in cats["defense"] if elite_max < p["rating"] <= strong_max]
    role_def = [p for p in cats["defense"] if p["rating"] > strong_max]
    if elite_def:
        lines.append(f"| **Elite ({s['elite_range']})** | {', '.join(p['name'].split()[-1] for p in elite_def)} |")
    if strong_def:
        lines.append(f"| **Strong ({s['strong_range']})** | {', '.join(p['name'].split()[-1] for p in strong_def)} |")
    if role_def:
        lines.append(f"| **Role ({s['role_range']})** | {', '.join(p['name'].split()[-1] for p in role_def)} |")

    lines.append("")
    lines.append(f"### Versatile F/D Players ({fd_count})" + (" -- CRITICAL ASSET" if fd_count >= 4 else ""))
    lines.append("")
    lines.append("| Name | Rating | Notes |")
    lines.append("|------|--------|-------|")
    for p in sorted(fd, key=lambda x: x["rating"]):
        lines.append(f"| **{p['name']}** | {p['rating']:.2f} | {p['notes']} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## ABSENCE CONTINGENCY PLANS")
    lines.append("")
    lines.append("Player absences are common. Key principles:")
    lines.append("")
    if fd_count >= 4:
        lines.append(f"- **{fd_count} F/D versatile players** can cover any positional shortage")
    lines.append(f"- **{def_count} D-capable players** means defense absences are manageable")
    lines.append("- Use F/D players to fill gaps instantly")
    lines.append("- Adjust strategy based on who's missing")
    lines.append("- Always have a contingency lineup ready")
    lines.append("- Promote by ranking when moving players between lines")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f'**REMEMBER**: This roster\'s greatest strength is its depth and versatility. We have {def_count} defensive-capable players, {fd_count} F/D versatile players, and ranking-driven deployment. We compete through preparation, advanced execution, and relentless effort. Every line has a purpose. Every player earns their role. This is "Competitive Excellence" -- this is Dev Team hockey!')
    lines.append("")

    return "\n".join(lines)


def generate_lineup_generator_roster(players: List[Dict], scale: int) -> str:
    """Generate the roster dict block for lineup_generator.py."""
    cats = categorize_players(players, scale)

    lines = []
    lines.append("        self.roster = {")

    # Goalies
    lines.append("            'goalies': [")
    for g in cats["goalies"]:
        cap = g.get("can_also_play", "")
        lines.append(f"                {{'name': '{g['name']}', 'rating': {g['rating']:.2f}, 'can_play': '{cap}'}},")
    lines.append("            ],")

    # Elite
    lines.append("            'elite': [")
    for p in sorted(cats["elite_top"] + cats["elite_strong"], key=lambda x: x["rating"]):
        lines.append(f"                {{'name': '{p['name']}', 'rating': {p['rating']:.2f}, 'position': '{p['position']}'}},")
    lines.append("            ],")

    # Strong
    lines.append("            'strong': [")
    for p in sorted(cats["strong_twoway"] + cats["strong_middle"], key=lambda x: x["rating"]):
        lines.append(f"                {{'name': '{p['name']}', 'rating': {p['rating']:.2f}, 'position': '{p['position']}'}},")
    lines.append("            ],")

    # Role
    lines.append("            'role': [")
    for p in sorted(cats["role_situational"] + cats["role_specific"], key=lambda x: x["rating"]):
        lines.append(f"                {{'name': '{p['name']}', 'rating': {p['rating']:.2f}, 'position': '{p['position']}'}},")
    lines.append("            ]")

    lines.append("        }")
    return "\n".join(lines)


def update_lineup_generator(players: List[Dict], scale: int):
    """Update the roster dict inside lineup_generator.py."""
    if not LINEUP_GEN.exists():
        print(f"WARNING: {LINEUP_GEN} not found, skipping lineup generator update.")
        return

    content = LINEUP_GEN.read_text()

    # Find and replace the self.roster block
    pattern = r"(\s+self\.roster\s*=\s*\{).*?(\n\s+\})"
    new_block = generate_lineup_generator_roster(players, scale)

    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + "\n" + new_block + content[match.end():]
        LINEUP_GEN.write_text(content)
        print(f"  Updated: {LINEUP_GEN}")
    else:
        print(f"WARNING: Could not find self.roster block in {LINEUP_GEN}")


def main():
    parser = argparse.ArgumentParser(
        description="Update Jr Kraken Dev Team roster and power rankings from Excel, CSV, or JSON."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to Excel (.xlsx) or CSV (.csv) roster file",
    )
    parser.add_argument(
        "--json",
        help='JSON string with player data: \'{"players": [{"name": "...", "position": "F", "rating": 1.50}, ...]}\'',
    )
    parser.add_argument(
        "--scale",
        type=int,
        choices=[3, 5],
        help="Force rating scale (3 or 5). If omitted, auto-detected from data.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated roster.md without writing files",
    )
    args = parser.parse_args()

    if not args.file and not args.json:
        parser.print_help()
        print("\nExample CSV format (1-3 scale):")
        print("  Name,Position,Rating,Notes")
        print("  Player One,F/D,1.00,\"Elite at both positions\"")
        print("  Player Two,F/D,1.00,\"Elite talent, leadership\"")
        print("  Goalie One,G,2.00,\"Reliable starter\"")
        print("\nExample CSV format (1-5 scale):")
        print("  Name,Position,Rating,Notes")
        print("  Player One,F/D,1.50,\"Elite at both positions\"")
        print("  Player Two,F/D,2.00,\"Strong skilled forward\"")
        print("  Player Three,D,4.00,\"Role player, situational\"")
        sys.exit(1)

    # Read players
    if args.json:
        players = read_json_string(args.json)
        print(f"Read {len(players)} players from JSON input.")
    elif args.file:
        ext = Path(args.file).suffix.lower()
        if ext == ".csv":
            players = read_csv(args.file)
        elif ext in (".xlsx", ".xls"):
            players = read_excel(args.file)
        else:
            print(f"ERROR: Unsupported file type '{ext}'. Use .xlsx or .csv.")
            sys.exit(1)
        print(f"Read {len(players)} players from {args.file}.")
    else:
        sys.exit(1)

    # Validate
    if not players:
        print("ERROR: No players found in input.")
        sys.exit(1)

    # Detect or use forced scale
    scale = args.scale if args.scale else detect_scale(players)
    s = SCALES[scale]
    print(f"Rating scale: {s['name']} ({'forced' if args.scale else 'auto-detected'})")

    for p in players:
        if not (s["warn_low"] <= p["rating"] <= s["warn_high"]):
            print(f"WARNING: {p['name']} has unusual rating {p['rating']:.2f} (expected {s['name']} scale)")

    # Categorize and report
    cats = categorize_players(players, scale)
    goalies = cats["goalies"]
    skaters = cats["skaters"]
    print(f"\nRoster summary:")
    print(f"  Goalies: {len(goalies)}")
    print(f"  Skaters: {len(skaters)}")
    print(f"  Elite ({s['elite_range']}): {len(cats['elite_top']) + len(cats['elite_strong'])}")
    print(f"  Strong ({s['strong_range']}): {len(cats['strong_twoway']) + len(cats['strong_middle'])}")
    print(f"  Role ({s['role_range']}): {len(cats['role_situational']) + len(cats['role_specific'])}")
    print(f"  F/D Versatile: {len(cats['fd_versatile'])}")
    print(f"  Forward-capable: {len(cats['forwards'])}")
    print(f"  Defense-capable: {len(cats['defense'])}")
    print(f"  Average rating: {cats['avg_rating']:.3f}")

    # Generate roster.md
    roster_content = generate_roster_md(players, scale)

    if args.dry_run:
        print("\n--- DRY RUN: Generated roster.md ---\n")
        print(roster_content)
        return

    # Write files
    print(f"\nWriting files:")
    ROSTER_MD.write_text(roster_content)
    print(f"  Updated: {ROSTER_MD}")

    update_lineup_generator(players, scale)

    print(f"\nDone! Power rankings updated successfully.")
    print(f"Review the changes in:")
    print(f"  - {ROSTER_MD}")
    print(f"  - {LINEUP_GEN}")


if __name__ == "__main__":
    main()
