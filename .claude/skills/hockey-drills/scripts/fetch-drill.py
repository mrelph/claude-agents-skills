#!/usr/bin/env python3
"""
Fetch detailed information about a specific hockey drill
"""

import sys
import json
from typing import Dict, Optional, List
from auth_helper import IHSAuthenticator

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required", file=sys.stderr)
    print("Install it with: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def parse_drill_page(html: str) -> Optional[Dict]:
    """
    Parse drill details from HTML page
    Args:
        html: HTML content of drill page
    Returns:
        Dictionary with drill details or None if parsing fails
    """
    soup = BeautifulSoup(html, 'html.parser')
    drill = {}

    try:
        # Note: These selectors are placeholders and need to be updated
        # based on the actual HTML structure of icehockeysystems.com
        # Inspect individual drill pages to determine correct selectors

        # Drill title
        title_elem = soup.select_one('h1, .drill-title, .page-title')
        if title_elem:
            drill['title'] = title_elem.get_text(strip=True)

        # Drill objective/description
        objective_elem = soup.select_one('.objective, .description, .summary')
        if objective_elem:
            drill['objective'] = objective_elem.get_text(strip=True)

        # Drill setup/equipment
        setup_elem = soup.select_one('.setup, .equipment, .requirements')
        if setup_elem:
            drill['setup'] = setup_elem.get_text(strip=True)

        # Drill instructions/steps
        instructions = []
        instruction_elems = soup.select('.instruction, .step, ol li, .instructions li')
        for elem in instruction_elems:
            step = elem.get_text(strip=True)
            if step:
                instructions.append(step)
        if instructions:
            drill['instructions'] = instructions

        # Coaching points
        coaching_points = []
        coaching_elems = soup.select('.coaching-point, .tip, .key-point, .notes li')
        for elem in coaching_elems:
            point = elem.get_text(strip=True)
            if point:
                coaching_points.append(point)
        if coaching_points:
            drill['coaching_points'] = coaching_points

        # Variations
        variations_elem = soup.select_one('.variations, .alternatives, .modifications')
        if variations_elem:
            drill['variations'] = variations_elem.get_text(strip=True)

        # Metadata
        metadata = {}

        # Skill level
        level_elem = soup.select_one('.skill-level, .level, .age-group')
        if level_elem:
            metadata['skill_level'] = level_elem.get_text(strip=True)

        # Duration
        duration_elem = soup.select_one('.duration, .time, .length')
        if duration_elem:
            metadata['duration'] = duration_elem.get_text(strip=True)

        # Players needed
        players_elem = soup.select_one('.players, .participants, .team-size')
        if players_elem:
            metadata['players'] = players_elem.get_text(strip=True)

        # Category/tags
        category_elems = soup.select('.category, .tag, .skill-type')
        if category_elems:
            metadata['categories'] = [elem.get_text(strip=True) for elem in category_elems]

        if metadata:
            drill['metadata'] = metadata

        # Diagrams/images
        images = []
        img_elems = soup.select('.drill-diagram img, .diagram img, .illustration img')
        for img in img_elems:
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                images.append({'url': src, 'alt': alt})
        if images:
            drill['diagrams'] = images

        return drill if drill else None

    except Exception as e:
        print(f"Error parsing drill page: {e}", file=sys.stderr)
        return None


def fetch_drill(drill_id: str, url: Optional[str] = None) -> Optional[Dict]:
    """
    Fetch detailed information about a drill
    Args:
        drill_id: Drill ID or slug
        url: Optional full URL to drill page
    Returns:
        Dictionary with drill details or None on error
    """
    auth = IHSAuthenticator()

    # Construct URL if not provided
    if not url:
        # Adjust URL pattern based on actual site structure
        # Common patterns: /drills/{id}, /drill/{slug}, /practice-drills/{id}
        url = f"/drills/{drill_id}"

    print(f"Fetching drill: {drill_id}", file=sys.stderr)

    # Fetch page
    html = auth.get_page(url)

    if not html:
        print(f"Failed to fetch drill: {drill_id}", file=sys.stderr)
        return None

    # Parse drill details
    drill = parse_drill_page(html)

    if not drill:
        print(f"Failed to parse drill page: {drill_id}", file=sys.stderr)
        return None

    # Add ID and URL to result
    drill['id'] = drill_id
    drill['url'] = url

    print(f"Successfully fetched drill: {drill.get('title', drill_id)}", file=sys.stderr)
    return drill


def format_drill(drill: Dict) -> str:
    """Format drill details for display"""
    lines = []
    lines.append("=" * 60)
    lines.append(drill.get('title', 'Unknown Drill'))
    lines.append("=" * 60)
    lines.append("")

    # Metadata
    if 'metadata' in drill:
        meta = drill['metadata']
        if meta.get('skill_level'):
            lines.append(f"Skill Level: {meta['skill_level']}")
        if meta.get('duration'):
            lines.append(f"Duration: {meta['duration']}")
        if meta.get('players'):
            lines.append(f"Players: {meta['players']}")
        if meta.get('categories'):
            lines.append(f"Categories: {', '.join(meta['categories'])}")
        lines.append("")

    # Objective
    if drill.get('objective'):
        lines.append("OBJECTIVE")
        lines.append("-" * 60)
        lines.append(drill['objective'])
        lines.append("")

    # Setup
    if drill.get('setup'):
        lines.append("SETUP & EQUIPMENT")
        lines.append("-" * 60)
        lines.append(drill['setup'])
        lines.append("")

    # Instructions
    if drill.get('instructions'):
        lines.append("INSTRUCTIONS")
        lines.append("-" * 60)
        for i, step in enumerate(drill['instructions'], 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    # Coaching points
    if drill.get('coaching_points'):
        lines.append("COACHING POINTS")
        lines.append("-" * 60)
        for point in drill['coaching_points']:
            lines.append(f"• {point}")
        lines.append("")

    # Variations
    if drill.get('variations'):
        lines.append("VARIATIONS")
        lines.append("-" * 60)
        lines.append(drill['variations'])
        lines.append("")

    # Diagrams
    if drill.get('diagrams'):
        lines.append("DIAGRAMS")
        lines.append("-" * 60)
        for i, img in enumerate(drill['diagrams'], 1):
            lines.append(f"{i}. {img['alt'] or 'Diagram'}: {img['url']}")
        lines.append("")

    # Footer
    lines.append("-" * 60)
    lines.append(f"Drill ID: {drill.get('id', 'N/A')}")
    lines.append(f"URL: {drill.get('url', 'N/A')}")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: fetch-drill.py <drill-id> [--json]")
        print()
        print("Examples:")
        print("  fetch-drill.py 12345")
        print("  fetch-drill.py passing-fundamentals-drill")
        print("  fetch-drill.py 12345 --json")
        return 1

    # Parse arguments
    drill_id = sys.argv[1]
    output_json = '--json' in sys.argv

    # Fetch drill
    drill = fetch_drill(drill_id)

    if not drill:
        print(f"Failed to fetch drill: {drill_id}")
        return 1

    # Output results
    if output_json:
        print(json.dumps(drill, indent=2))
    else:
        print(format_drill(drill))

    return 0


if __name__ == '__main__':
    sys.exit(main())
