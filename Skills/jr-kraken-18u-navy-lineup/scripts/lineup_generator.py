#!/usr/bin/env python3
"""
Jr Kraken 18U C Navy Team - Lineup Generator
Generates formatted lineup sheets for game day use
"""

from datetime import datetime
from typing import List, Dict, Optional


class NavyLineupGenerator:
    """Generate formatted lineups for Coach Mark's Navy team"""
    
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
        self.roster = {
            'goalies': [
                {'name': 'Cas Haffey', 'rating': 2.00, 'can_play': 'F'},
                {'name': 'Gregor Schuchart', 'rating': 2.00, 'can_play': 'D'}
            ],
            'elite': [
                {'name': 'Massey Relph', 'rating': 1.00, 'position': 'F/D'},
                {'name': 'Shaya Marsh', 'rating': 1.00, 'position': 'F/D'},
                {'name': 'Thad Freeman', 'rating': 1.50, 'position': 'F/D'},
                {'name': 'Easton Klakring', 'rating': 1.50, 'position': 'F'},
                {'name': 'Samuel Silliker', 'rating': 1.50, 'position': 'F/D'}
            ],
            'strong': [
                {'name': 'Max McCredy', 'rating': 1.75, 'position': 'F'},
                {'name': 'Zachary Young', 'rating': 1.75, 'position': 'D'},
                {'name': 'Dylan Bagga', 'rating': 2.00, 'position': 'F'},
                {'name': 'George Berry', 'rating': 2.00, 'position': 'F/D'},
                {'name': 'Miles Butler', 'rating': 2.00, 'position': 'D'},
                {'name': 'Aleksander Herrick', 'rating': 2.00, 'position': 'F'},
                {'name': 'Hayden Jaeger', 'rating': 2.00, 'position': 'F'},
                {'name': 'Henry Tegart', 'rating': 2.00, 'position': 'F/D'}
            ],
            'development': [
                {'name': 'Ender Cram', 'rating': 2.50, 'position': 'F'},
                {'name': 'Timothy Thompson', 'rating': 3.00, 'position': 'D'}
            ]
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
        output.append("JR KRAKEN 18U C NAVY - GAME DAY LINEUP")
        output.append("Coach Mark - 'Balanced Depth' Strategy")
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
        output.append("GO NAVY! - Defense Wins Championships")
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def generate_standard_four_line_lineup(self):
        """Generate standard four-line lineup with full roster"""
        self.add_line(1, "Marsh", "Relph", "Freeman", "Elite/Offensive")
        self.add_line(2, "Klakring", "Silliker", "McCredy", "Skilled/Two-Way")
        self.add_line(3, "Bagga", "Herrick", "Jaeger", "Grind/Energy")
        self.add_line(4, "Berry", "Cram", "Tegart", "Development/Sheltered")
        
        self.add_defense_pair(1, "Young", "Berry", "Shutdown")
        self.add_defense_pair(2, "Butler", "Freeman", "Two-Way")
        self.add_defense_pair(3, "Thompson", "Silliker", "Sheltered")
        
        self.set_goalies("Haffey", "Schuchart")
        
        self.set_power_play(1, ["Marsh", "Relph", "Freeman", "Klakring", "Young"])
        self.set_power_play(2, ["Silliker", "McCredy", "Herrick", "Bagga", "Berry"])
        
        self.set_penalty_kill(1, ["Silliker", "Tegart", "Young", "Butler"])
        self.set_penalty_kill(2, ["Herrick", "Jaeger", "Berry", "Freeman"])
        
        self.add_note("Roll four lines - keep everyone fresh")
        self.add_note("Cram: Offensive zone starts, shorter shifts (45-60 sec)")
        self.add_note("Thompson: Always with strong partner, limit critical situations")
        self.add_note("Third period is OURS - depth advantage emerges")
    
    def generate_competitive_three_line_lineup(self):
        """Generate competitive three-line lineup for close games"""
        self.add_line(1, "Marsh", "Relph", "Freeman", "Elite - 45% Ice Time")
        self.add_line(2, "Klakring", "Silliker", "McCredy", "Skilled - 40% Ice Time")
        self.add_line(3, "Bagga", "Herrick", "Jaeger", "Energy - 15% Ice Time")
        
        self.add_defense_pair(1, "Young", "Berry", "Shutdown")
        self.add_defense_pair(2, "Butler", "Tegart", "Two-Way")
        self.add_defense_pair(3, "Thompson", "Silliker", "Limited")
        
        self.set_goalies("Haffey", "Schuchart")
        
        self.set_power_play(1, ["Marsh", "Relph", "Freeman", "Klakring", "Young"])
        self.set_penalty_kill(1, ["Silliker", "Tegart", "Young", "Butler"])
        
        self.add_note("Three-line system - maximize top players")
        self.add_note("Spot duty: Tegart (5-8 min), Cram (3-5 min)")
        self.add_note("Thompson: Very limited minutes, strong partner always")
        self.add_note("Double-shift Line 1 when needed")
    
    def generate_vs_paul_lineup(self):
        """Generate lineup specifically for playing Paul's White team"""
        self.add_line(1, "Marsh", "Relph", "Freeman", "Elite - Match Their Top")
        self.add_line(2, "Klakring", "Silliker", "McCredy", "Skilled - Key Line")
        self.add_line(3, "Bagga", "Herrick", "Jaeger", "Grind - Wear Them Down")
        self.add_line(4, "Berry", "Cram", "Tegart", "Depth - Fresh Legs")
        
        self.add_defense_pair(1, "Young", "Berry", "Shutdown Their Elite")
        self.add_defense_pair(2, "Butler", "Tegart", "Attack Their Tired D")
        self.add_defense_pair(3, "Thompson", "Silliker", "Sheltered")
        
        self.set_goalies("Haffey", "Schuchart")
        
        self.set_power_play(1, ["Marsh", "Relph", "Freeman", "Klakring", "Young"])
        self.set_penalty_kill(1, ["Silliker", "Tegart", "Young", "Butler"])
        self.set_penalty_kill(2, ["Herrick", "Jaeger", "Berry", "Freeman"])
        
        self.add_note("⭐ HEAVY FORECHECK - Attack their 6 tired D-men")
        self.add_note("⭐ ROLL FOUR LINES - Our 9 D vs their 6 is HUGE advantage")
        self.add_note("⭐ STRONG PENALTY KILL - They have dangerous PP, MUST KILL")
        self.add_note("Stay disciplined - don't give them PP opportunities")
        self.add_note("Third period is OURS - depth emerges, take control")
        self.add_note("Physical but smart - make them feel us all game")


def main():
    """Example usage"""
    
    # Example 1: Standard Four-Line Lineup
    print("EXAMPLE 1: STANDARD FOUR-LINE LINEUP")
    print()
    lineup = NavyLineupGenerator()
    lineup.generate_standard_four_line_lineup()
    print(lineup.generate_lineup_sheet(
        opponent="Generic Opponent",
        date="October 26, 2025",
        game_type="League Game"
    ))
    
    print("\n\n")
    
    # Example 2: Competitive Three-Line Lineup
    print("EXAMPLE 2: COMPETITIVE THREE-LINE LINEUP")
    print()
    lineup2 = NavyLineupGenerator()
    lineup2.generate_competitive_three_line_lineup()
    print(lineup2.generate_lineup_sheet(
        opponent="Strong Opponent",
        date="October 27, 2025",
        game_type="Playoff Game"
    ))
    
    print("\n\n")
    
    # Example 3: vs Paul's Team
    print("EXAMPLE 3: LINEUP VS PAUL'S WHITE TEAM")
    print()
    lineup3 = NavyLineupGenerator()
    lineup3.generate_vs_paul_lineup()
    print(lineup3.generate_lineup_sheet(
        opponent="Paul's White Team",
        date="October 28, 2025",
        game_type="League Game - Navy vs White"
    ))


if __name__ == "__main__":
    main()
