#!/usr/bin/env python3
"""
Test authentication to hockey coaching sites
Verifies credentials and connection are working
"""

import sys
import argparse
from auth_helper import test_authentication, SITES


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Test authentication to hockey coaching sites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Test all configured sites
  %(prog)s ihs          # Test Ice Hockey Systems only
  %(prog)s tcs          # Test The Coaches Site only

Supported sites:
  ihs - Ice Hockey Systems (requires IHS_USERNAME, IHS_PASSWORD)
  tcs - The Coaches Site (requires TCS_USERNAME, TCS_PASSWORD)

Before running, set your credentials:
  export IHS_USERNAME='your-ihs-username'
  export IHS_PASSWORD='your-ihs-password'
  export TCS_USERNAME='your-tcs-username'
  export TCS_PASSWORD='your-tcs-password'
        """
    )

    parser.add_argument('site', nargs='?', choices=list(SITES.keys()),
                        help='Site to test (default: all available)')

    args = parser.parse_args()

    return test_authentication(args.site)


if __name__ == '__main__':
    sys.exit(main())
