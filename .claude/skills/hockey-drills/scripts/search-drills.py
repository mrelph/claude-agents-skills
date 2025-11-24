#!/usr/bin/env python3
"""
Search for hockey drills across multiple authenticated sites
"""

import sys
import json
import argparse
from typing import List, Dict
from auth_helper import get_authenticator, get_available_sites, SITES

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required", file=sys.stderr)
    print("Install it with: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def parse_search_results(html: str, site_code: str) -> List[Dict[str, str]]:
    """
    Parse search results from HTML
    Args:
        html: HTML content from search results page
        site_code: Site code for proper parsing
    Returns:
        List of drill dictionaries with id, title, description, url, site
    """
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    # Note: These selectors are placeholders and need to be updated
    # based on the actual HTML structure of each site
    # Inspect the sites to determine the correct CSS selectors

    # Example structure (adjust as needed):
    drill_items = soup.select('.drill-item, .search-result, article, .post, .entry')

    for item in drill_items:
        try:
            # Extract drill information
            # Adjust selectors based on actual site structure
            title_elem = item.select_one('h2, h3, .drill-title, .title, .entry-title')
            link_elem = item.select_one('a')
            desc_elem = item.select_one('.description, .excerpt, p, .summary')

            if title_elem and link_elem:
                drill = {
                    'title': title_elem.get_text(strip=True),
                    'url': link_elem.get('href', ''),
                    'description': desc_elem.get_text(strip=True) if desc_elem else '',
                    'id': extract_drill_id(link_elem.get('href', '')),
                    'site': site_code
                }
                results.append(drill)
        except Exception as e:
            print(f"Warning: Error parsing drill item: {e}", file=sys.stderr)
            continue

    return results


def extract_drill_id(url: str) -> str:
    """
    Extract drill ID from URL
    Args:
        url: Drill URL
    Returns:
        Drill ID string
    """
    # Extract ID from URL pattern (adjust based on actual URLs)
    # Example: /drills/123 or /drill/passing-drill-123
    parts = url.strip('/').split('/')
    return parts[-1] if parts else url


def search_site(site_code: str, query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search a single site for drills
    Args:
        site_code: Site code ('ihs', 'tcs')
        query: Search query string
        max_results: Maximum number of results to return
    Returns:
        List of drill dictionaries
    """
    auth = get_authenticator(site_code)
    if not auth:
        return []

    print(f"Searching {auth.get_site_name()} for: {query}", file=sys.stderr)

    # Perform search
    html = auth.search(query)

    if not html:
        print(f"Search failed on {auth.get_site_name()}", file=sys.stderr)
        return []

    # Parse results
    results = parse_search_results(html, site_code)

    if not results:
        print(f"No drills found on {auth.get_site_name()}", file=sys.stderr)
        return []

    # Limit results
    results = results[:max_results]

    print(f"Found {len(results)} drill(s) on {auth.get_site_name()}", file=sys.stderr)
    return results


def search_all_sites(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search all available sites for drills
    Args:
        query: Search query string
        max_results: Maximum results per site
    Returns:
        Combined list of drill dictionaries
    """
    available = get_available_sites()

    if not available:
        print("No sites available - please configure credentials", file=sys.stderr)
        return []

    all_results = []

    for site in available:
        results = search_site(site, query, max_results)
        all_results.extend(results)

    return all_results


def format_results(results: List[Dict[str, str]]) -> str:
    """Format search results for display"""
    if not results:
        return "No results found."

    # Group by site
    by_site = {}
    for drill in results:
        site = drill['site']
        if site not in by_site:
            by_site[site] = []
        by_site[site].append(drill)

    output = []
    output.append(f"Found {len(results)} drill(s) across {len(by_site)} site(s):\n")

    for site_code, drills in by_site.items():
        site_name = site_code.upper()
        output.append(f"\n--- {site_name} ({len(drills)} drills) ---")

        for i, drill in enumerate(drills, 1):
            output.append(f"\n{i}. {drill['title']}")
            output.append(f"   Site: {drill['site']}")
            output.append(f"   ID: {drill['id']}")
            if drill['description']:
                desc = drill['description'][:150]
                if len(drill['description']) > 150:
                    desc += "..."
                output.append(f"   {desc}")
            output.append(f"   URL: {drill['url']}")

    return "\n".join(output)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Search for hockey drills across authenticated sites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 'passing drills'
  %(prog)s 'youth skating' --site ihs
  %(prog)s 'power play' --json
  %(prog)s 'breakout drills' --site tcs --max 5

Supported sites:
  ihs - Ice Hockey Systems (requires IHS_USERNAME, IHS_PASSWORD)
  tcs - The Coaches Site (requires TCS_USERNAME, TCS_PASSWORD)
        """
    )

    parser.add_argument('query', help='Search query')
    parser.add_argument('--site', choices=list(SITES.keys()),
                        help='Search specific site (default: all available)')
    parser.add_argument('--max', type=int, default=10,
                        help='Maximum results per site (default: 10)')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')

    args = parser.parse_args()

    # Search for drills
    if args.site:
        results = search_site(args.site, args.query, args.max)
    else:
        results = search_all_sites(args.query, args.max)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))

    return 0 if results else 1


if __name__ == '__main__':
    sys.exit(main())
