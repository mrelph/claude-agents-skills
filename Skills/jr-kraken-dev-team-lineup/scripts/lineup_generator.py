#!/usr/bin/env python3
"""
Jr Kraken Development Team - Lineup Generator
Generates formatted lineup sheets for game day use
"""

from datetime import datetime
from typing import List, Dict, Optional


class DevTeamLineupGenerator:
    """Generate formatted lineups for Coach Mark's Dev Team"""

    def __init__(self):
        self.forward_lines = []
        self.defense_pairs = []
        self.starting_goalie = None
        self.backup_goalie = None
        self.pp1 = []
        self.pp2 = []
        self.pk1 = []
        self.pk2 = []
        self.notes = []

        # Team roster for reference
        # This will be populated when update_roster.py is run
        self.roster = {
            'goalies': [],
            'elite': [],
            'strong': [],
            'role': []
        }

    def add_line(self, line_number: int, lw: str, center: str, rw: str, role: str = ""):
        """Add a forward line"""
        self.forward_lines.append({
            'number': line_number,
            'lw': lw,
            'center': center,
            'rw': rw,
            'role': role
        })

    def add_defense_pair(self, pair_number: int, ld: str, rd: str, role: str = ""):
        """Add a defense pair"""
        self.defense_pairs.append({
            'number': pair_number,
            'ld': ld,
            'rd': rd,
            'role': role
        })

    def set_goalies(self, starter: str, backup: str):
        """Set starting and backup goalies"""
        self.starting_goalie = starter
        self.backup_goalie = backup

    def set_power_play(self, unit: int, players: List[str]):
        """Set power play unit (1 or 2)"""
        if unit == 1:
            self.pp1 = players
        elif unit == 2:
            self.pp2 = players

    def set_penalty_kill(self, unit: int, players: List[str]):
        """Set penalty kill unit (1 or 2)"""
        if unit == 1:
            self.pk1 = players
        elif unit == 2:
            self.pk2 = players

    def add_note(self, note: str):
        """Add a game note"""
        self.notes.append(note)

    def generate_lineup_sheet(self,
                            opponent: str = "TBD",
                            date: str = None,
                            game_type: str = "League Game",
                            notes: str = None) -> str:
        """Generate complete formatted lineup sheet"""

        if date is None:
            date = datetime.now().strftime("%B %d, %Y")

        output = []
        output.append("=" * 70)
        output.append("JR KRAKEN DEVELOPMENT TEAM - GAME DAY LINEUP")
        output.append("Coach Mark - 'Competitive Excellence' Strategy")
        output.append("=" * 70)
        output.append("")
        output.append(f"OPPONENT: {opponent}")
        output.append(f"DATE: {date}")
        output.append(f"GAME TYPE: {game_type}")
        output.append("")
        output.append("-" * 70)
        output.append("FORWARD LINES")
        output.append("-" * 70)

        for line in sorted(self.forward_lines, key=lambda x: x['number']):
            role_str = f" [{line['role']}]" if line['role'] else ""
            output.append(f"\nLINE {line['number']}{role_str}:")
            output.append(f"  LW: {line['lw']}")
            output.append(f"   C: {line['center']}")
            output.append(f"  RW: {line['rw']}")

        output.append("")
        output.append("-" * 70)
        output.append("DEFENSE PAIRS")
        output.append("-" * 70)

        for pair in sorted(self.defense_pairs, key=lambda x: x['number']):
            role_str = f" [{pair['role']}]" if pair['role'] else ""
            output.append(f"\nPAIR {pair['number']}{role_str}:")
            output.append(f"  LD: {pair['ld']}")
            output.append(f"  RD: {pair['rd']}")

        output.append("")
        output.append("-" * 70)
        output.append("GOALIES")
        output.append("-" * 70)
        output.append(f"STARTING: {self.starting_goalie}")
        output.append(f"BACKUP:   {self.backup_goalie}")

        if self.pp1 or self.pp2:
            output.append("")
            output.append("-" * 70)
            output.append("POWER PLAY UNITS")
            output.append("-" * 70)

            if self.pp1:
                output.append("\nPP1:")
                for player in self.pp1:
                    output.append(f"  • {player}")

            if self.pp2:
                output.append("\nPP2:")
                for player in self.pp2:
                    output.append(f"  • {player}")

        if self.pk1 or self.pk2:
            output.append("")
            output.append("-" * 70)
            output.append("PENALTY KILL UNITS")
            output.append("-" * 70)

            if self.pk1:
                output.append("\nPK1:")
                for player in self.pk1:
                    output.append(f"  • {player}")

            if self.pk2:
                output.append("\nPK2:")
                for player in self.pk2:
                    output.append(f"  • {player}")

        if notes or self.notes:
            output.append("")
            output.append("-" * 70)
            output.append("GAME NOTES")
            output.append("-" * 70)

            if notes:
                output.append(f"\n{notes}")

            for note in self.notes:
                output.append(f"• {note}")

        output.append("")
        output.append("=" * 70)
        output.append("GO DEV TEAM! - Compete Every Shift")
        output.append("=" * 70)

        return "\n".join(output)

    def generate_standard_four_line_lineup(self):
        """Generate standard four-line lineup -- requires roster to be populated"""
        if not self.roster['elite']:
            print("WARNING: Roster is empty. Run update_roster.py first to populate.")
            print("  python3 scripts/update_roster.py <roster_file.xlsx>")
            return

        self.add_note("Roll four lines with purpose -- every line has a mission")
        self.add_note("Deploy by rankings -- top-ranked players anchor key situations")
        self.add_note("Third period is OURS -- depth advantage emerges")

    def generate_competitive_three_line_lineup(self):
        """Generate competitive three-line lineup for close games"""
        if not self.roster['elite']:
            print("WARNING: Roster is empty. Run update_roster.py first to populate.")
            print("  python3 scripts/update_roster.py <roster_file.xlsx>")
            return

        self.add_note("Three-line system -- maximize top-ranked players")
        self.add_note("Spot duty for remaining forwards (5-8 min)")
        self.add_note("Double-shift Line 1 when needed")

    def generate_vs_elite_rival_lineup(self):
        """Generate lineup for playing an elite skill / star-heavy rival"""
        if not self.roster['elite']:
            print("WARNING: Roster is empty. Run update_roster.py first to populate.")
            print("  python3 scripts/update_roster.py <roster_file.xlsx>")
            return

        self.add_note("HEAVY FORECHECK -- Attack their tired D-men")
        self.add_note("ROLL FOUR LINES -- Exploit our depth advantage")
        self.add_note("STRONG PENALTY KILL -- Neutralize their PP, MUST KILL")
        self.add_note("Stay disciplined -- don't give them PP opportunities")
        self.add_note("Third period is OURS -- depth emerges, take control")
        self.add_note("Physical but smart -- make them feel us all game")


def main():
    """Example usage"""

    print("Jr Kraken Development Team - Lineup Generator")
    print("=" * 50)
    print()
    print("To use this generator:")
    print("1. First populate the roster: python3 update_roster.py <roster_file>")
    print("2. Then use the generator in your scripts:")
    print()
    print("  from lineup_generator import DevTeamLineupGenerator")
    print("  lineup = DevTeamLineupGenerator()")
    print("  lineup.add_line(1, 'LW', 'C', 'RW', 'Offensive')")
    print("  lineup.add_defense_pair(1, 'LD', 'RD', 'Shutdown')")
    print("  lineup.set_goalies('Starter', 'Backup')")
    print("  print(lineup.generate_lineup_sheet(opponent='Team', date='March 15, 2026'))")
    print()
    print("See SKILL.md for full usage instructions.")


if __name__ == "__main__":
    main()
