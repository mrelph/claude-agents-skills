#!/usr/bin/env python3
"""
Hockey Lineup Builder - Lineup Generator

Generates formatted lineup sheets for game day use. Team-agnostic: pass
team_name and tagline at construction time, or leave defaults for a
generic header.
"""

from datetime import datetime
from typing import List, Optional


class LineupGenerator:
    """Generate formatted lineups for any hockey team."""

    def __init__(
        self,
        team_name: str = "Hockey Team",
        tagline: Optional[str] = None,
        closer: Optional[str] = None,
    ):
        self.team_name = team_name
        self.tagline = tagline
        self.closer = closer
        self.forward_lines: List[dict] = []
        self.defense_pairs: List[dict] = []
        self.starting_goalie: Optional[str] = None
        self.backup_goalie: Optional[str] = None
        self.pp1: List[str] = []
        self.pp2: List[str] = []
        self.pk1: List[str] = []
        self.pk2: List[str] = []
        self.notes: List[str] = []

        # Roster is populated by update_roster.py importing a real roster.
        # Empty by default so the generic skill ships clean.
        self.roster = {
            "goalies": [],
            "elite": [],
            "strong": [],
            "development": [],
        }

    def add_line(self, line_number: int, lw: str, center: str, rw: str, role: str = ""):
        self.forward_lines.append({
            "number": line_number,
            "lw": lw,
            "center": center,
            "rw": rw,
            "role": role,
        })

    def add_defense_pair(self, pair_number: int, ld: str, rd: str, role: str = ""):
        self.defense_pairs.append({
            "number": pair_number,
            "ld": ld,
            "rd": rd,
            "role": role,
        })

    def set_goalies(self, starter: str, backup: str):
        self.starting_goalie = starter
        self.backup_goalie = backup

    def set_power_play(self, unit: int, players: List[str]):
        if unit == 1:
            self.pp1 = players
        elif unit == 2:
            self.pp2 = players

    def set_penalty_kill(self, unit: int, players: List[str]):
        if unit == 1:
            self.pk1 = players
        elif unit == 2:
            self.pk2 = players

    def add_note(self, note: str):
        self.notes.append(note)

    def generate_lineup_sheet(
        self,
        opponent: str = "TBD",
        date: Optional[str] = None,
        game_type: str = "League Game",
        notes: Optional[str] = None,
    ) -> str:
        """Generate a complete formatted lineup sheet."""

        if date is None:
            date = datetime.now().strftime("%B %d, %Y")

        header_line = f"{self.team_name.upper()} - GAME DAY LINEUP"
        out: List[str] = []
        out.append("=" * 70)
        out.append(header_line)
        if self.tagline:
            out.append(self.tagline)
        out.append("=" * 70)
        out.append("")
        out.append(f"OPPONENT: {opponent}")
        out.append(f"DATE: {date}")
        out.append(f"GAME TYPE: {game_type}")
        out.append("")
        out.append("-" * 70)
        out.append("FORWARD LINES")
        out.append("-" * 70)

        for line in sorted(self.forward_lines, key=lambda x: x["number"]):
            role_str = f" [{line['role']}]" if line["role"] else ""
            out.append(f"\nLINE {line['number']}{role_str}:")
            out.append(f"  LW: {line['lw']}")
            out.append(f"   C: {line['center']}")
            out.append(f"  RW: {line['rw']}")

        out.append("")
        out.append("-" * 70)
        out.append("DEFENSE PAIRS")
        out.append("-" * 70)

        for pair in sorted(self.defense_pairs, key=lambda x: x["number"]):
            role_str = f" [{pair['role']}]" if pair["role"] else ""
            out.append(f"\nPAIR {pair['number']}{role_str}:")
            out.append(f"  LD: {pair['ld']}")
            out.append(f"  RD: {pair['rd']}")

        out.append("")
        out.append("-" * 70)
        out.append("GOALIES")
        out.append("-" * 70)
        out.append(f"STARTING: {self.starting_goalie}")
        out.append(f"BACKUP:   {self.backup_goalie}")

        if self.pp1 or self.pp2:
            out.append("")
            out.append("-" * 70)
            out.append("POWER PLAY UNITS")
            out.append("-" * 70)

            if self.pp1:
                out.append("\nPP1:")
                for player in self.pp1:
                    out.append(f"  • {player}")

            if self.pp2:
                out.append("\nPP2:")
                for player in self.pp2:
                    out.append(f"  • {player}")

        if self.pk1 or self.pk2:
            out.append("")
            out.append("-" * 70)
            out.append("PENALTY KILL UNITS")
            out.append("-" * 70)

            if self.pk1:
                out.append("\nPK1:")
                for player in self.pk1:
                    out.append(f"  • {player}")

            if self.pk2:
                out.append("\nPK2:")
                for player in self.pk2:
                    out.append(f"  • {player}")

        if notes or self.notes:
            out.append("")
            out.append("-" * 70)
            out.append("GAME NOTES")
            out.append("-" * 70)

            if notes:
                out.append(f"\n{notes}")

            for note in self.notes:
                out.append(f"• {note}")

        out.append("")
        out.append("=" * 70)
        if self.closer:
            out.append(self.closer)
        else:
            out.append(f"GO {self.team_name.upper()}!")
        out.append("=" * 70)

        return "\n".join(out)

    def generate_standard_four_line_lineup(self):
        """Generic four-line template with placeholder names."""
        self.add_line(1, "LW1", "C1", "RW1", "Top/Offensive")
        self.add_line(2, "LW2", "C2", "RW2", "Skilled/Two-Way")
        self.add_line(3, "LW3", "C3", "RW3", "Grind/Energy")
        self.add_line(4, "LW4", "C4", "RW4", "Depth/Development")

        self.add_defense_pair(1, "LD1", "RD1", "Shutdown")
        self.add_defense_pair(2, "LD2", "RD2", "Two-Way")
        self.add_defense_pair(3, "LD3", "RD3", "Sheltered")

        self.set_goalies("Starter", "Backup")

        self.add_note("Roll four lines - keep everyone fresh")
        self.add_note("Shorter shifts on Line 4 (45-60 sec)")
        self.add_note("Development players: shelter and protect")

    def generate_competitive_three_line_lineup(self):
        """Generic three-line template for close games."""
        self.add_line(1, "LW1", "C1", "RW1", "Elite - 45% Ice Time")
        self.add_line(2, "LW2", "C2", "RW2", "Skilled - 40% Ice Time")
        self.add_line(3, "LW3", "C3", "RW3", "Energy - 15% Ice Time")

        self.add_defense_pair(1, "LD1", "RD1", "Shutdown")
        self.add_defense_pair(2, "LD2", "RD2", "Two-Way")
        self.add_defense_pair(3, "LD3", "RD3", "Limited")

        self.set_goalies("Starter", "Backup")

        self.add_note("Three-line system - maximize top players")
        self.add_note("Spot duty for remaining players (3-8 min each)")
        self.add_note("Double-shift Line 1 when needed")


def main():
    """Example usage."""

    print("EXAMPLE 1: STANDARD FOUR-LINE LINEUP")
    print()
    lineup = LineupGenerator(team_name="Example Team", tagline="Generic four-line template")
    lineup.generate_standard_four_line_lineup()
    print(lineup.generate_lineup_sheet(
        opponent="Generic Opponent",
        game_type="League Game",
    ))

    print("\n\n")

    print("EXAMPLE 2: COMPETITIVE THREE-LINE LINEUP")
    print()
    lineup2 = LineupGenerator(team_name="Example Team")
    lineup2.generate_competitive_three_line_lineup()
    print(lineup2.generate_lineup_sheet(
        opponent="Strong Opponent",
        game_type="Playoff Game",
    ))


if __name__ == "__main__":
    main()
