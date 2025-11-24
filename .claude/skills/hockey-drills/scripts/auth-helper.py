#!/usr/bin/env python3
"""
Multi-site authentication helper for hockey coaching sites
Supports Ice Hockey Systems and The Coaches Site
"""

import os
import sys
import requests
from typing import Optional, Tuple
from abc import ABC, abstractmethod


class BaseAuthenticator(ABC):
    """Base class for site authenticators"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.authenticated = False

    @abstractmethod
    def get_credentials(self) -> Tuple[str, str]:
        """Get credentials from environment"""
        pass

    @abstractmethod
    def login(self) -> bool:
        """Authenticate to the site"""
        pass

    @abstractmethod
    def get_site_name(self) -> str:
        """Return human-readable site name"""
        pass

    def get_page(self, url: str) -> Optional[str]:
        """
        Fetch a page with authentication
        Args:
            url: Full URL or path relative to BASE_URL
        Returns:
            Page content as string, or None on error
        """
        if not self.authenticated:
            if not self.login():
                return None

        try:
            # Make URL absolute if needed
            if not url.startswith('http'):
                url = f"{self.BASE_URL}{url}"

            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text

        except requests.RequestException as e:
            print(f"Error fetching page: {e}", file=sys.stderr)
            return None

    def search(self, query: str) -> Optional[str]:
        """
        Perform a search on the site
        Args:
            query: Search query string
        Returns:
            Search results page content, or None on error
        """
        if not self.authenticated:
            if not self.login():
                return None

        try:
            search_url = f"{self.BASE_URL}/search"
            params = {'q': query, 'type': 'drills'}

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            return response.text

        except requests.RequestException as e:
            print(f"Error performing search: {e}", file=sys.stderr)
            return None


class IHSAuthenticator(BaseAuthenticator):
    """Handles authentication to Ice Hockey Systems"""

    BASE_URL = "https://www.icehockeysystems.com"
    LOGIN_URL = f"{BASE_URL}/members/home"

    def get_site_name(self) -> str:
        return "Ice Hockey Systems"

    def get_credentials(self) -> Tuple[str, str]:
        """
        Retrieve credentials from environment variables
        Returns: (username, password) tuple
        Raises: ValueError if credentials not found
        """
        username = os.getenv('IHS_USERNAME')
        password = os.getenv('IHS_PASSWORD')

        if not username or not password:
            raise ValueError(
                "Ice Hockey Systems credentials not found!\n"
                "Please set the following environment variables:\n"
                "  export IHS_USERNAME='your-username'\n"
                "  export IHS_PASSWORD='your-password'"
            )

        return username, password

    def login(self) -> bool:
        """
        Authenticate to Ice Hockey Systems
        Returns: True if successful, False otherwise
        """
        try:
            username, password = self.get_credentials()

            print(f"Accessing {self.get_site_name()} login page...", file=sys.stderr)
            response = self.session.get(self.LOGIN_URL, timeout=10)
            response.raise_for_status()

            # NOTE: This is a placeholder implementation
            # The actual login form structure needs to be inspected on the live site
            # to determine the correct field names and endpoints
            login_data = {
                'username': username,
                'password': password,
                # Add CSRF tokens or other fields as needed
            }

            print(f"Authenticating to {self.get_site_name()} as {username}...", file=sys.stderr)

            login_response = self.session.post(
                self.LOGIN_URL,
                data=login_data,
                timeout=10,
                allow_redirects=True
            )

            # Check for successful authentication
            if login_response.status_code == 200:
                if 'logout' in login_response.text.lower() or 'sign out' in login_response.text.lower():
                    self.authenticated = True
                    print(f"✓ {self.get_site_name()} authentication successful!", file=sys.stderr)
                    return True
                else:
                    print(f"✗ {self.get_site_name()} authentication failed: Invalid credentials", file=sys.stderr)
                    return False
            else:
                print(f"✗ {self.get_site_name()} authentication failed: HTTP {login_response.status_code}", file=sys.stderr)
                return False

        except ValueError as e:
            print(f"Configuration error: {e}", file=sys.stderr)
            return False
        except requests.RequestException as e:
            print(f"Network error during authentication: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Unexpected error during authentication: {e}", file=sys.stderr)
            return False


class TCSAuthenticator(BaseAuthenticator):
    """Handles authentication to The Coaches Site"""

    BASE_URL = "https://members.thecoachessite.com"
    LOGIN_URL = f"{BASE_URL}/login"

    def get_site_name(self) -> str:
        return "The Coaches Site"

    def get_credentials(self) -> Tuple[str, str]:
        """
        Retrieve credentials from environment variables
        Returns: (username, password) tuple
        Raises: ValueError if credentials not found
        """
        username = os.getenv('TCS_USERNAME')
        password = os.getenv('TCS_PASSWORD')

        if not username or not password:
            raise ValueError(
                "The Coaches Site credentials not found!\n"
                "Please set the following environment variables:\n"
                "  export TCS_USERNAME='your-username'\n"
                "  export TCS_PASSWORD='your-password'"
            )

        return username, password

    def login(self) -> bool:
        """
        Authenticate to The Coaches Site
        Returns: True if successful, False otherwise
        """
        try:
            username, password = self.get_credentials()

            print(f"Accessing {self.get_site_name()} login page...", file=sys.stderr)
            response = self.session.get(self.LOGIN_URL, timeout=10)
            response.raise_for_status()

            # NOTE: This is a placeholder implementation
            # The actual login form structure needs to be inspected on the live site
            # Common fields might include: email, username, password, remember_me, csrf_token
            login_data = {
                'email': username,  # Some sites use email instead of username
                'password': password,
                # Add CSRF tokens or other fields as needed
            }

            print(f"Authenticating to {self.get_site_name()} as {username}...", file=sys.stderr)

            login_response = self.session.post(
                self.LOGIN_URL,
                data=login_data,
                timeout=10,
                allow_redirects=True
            )

            # Check for successful authentication
            if login_response.status_code == 200:
                if 'logout' in login_response.text.lower() or 'sign out' in login_response.text.lower():
                    self.authenticated = True
                    print(f"✓ {self.get_site_name()} authentication successful!", file=sys.stderr)
                    return True
                else:
                    print(f"✗ {self.get_site_name()} authentication failed: Invalid credentials", file=sys.stderr)
                    return False
            else:
                print(f"✗ {self.get_site_name()} authentication failed: HTTP {login_response.status_code}", file=sys.stderr)
                return False

        except ValueError as e:
            print(f"Configuration error: {e}", file=sys.stderr)
            return False
        except requests.RequestException as e:
            print(f"Network error during authentication: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Unexpected error during authentication: {e}", file=sys.stderr)
            return False


# Site registry
SITES = {
    'ihs': IHSAuthenticator,
    'tcs': TCSAuthenticator,
}


def get_authenticator(site_code: str) -> Optional[BaseAuthenticator]:
    """
    Get an authenticator for the specified site
    Args:
        site_code: Site code ('ihs' or 'tcs')
    Returns:
        Authenticator instance or None if site not found
    """
    auth_class = SITES.get(site_code.lower())
    if not auth_class:
        print(f"Unknown site code: {site_code}", file=sys.stderr)
        print(f"Available sites: {', '.join(SITES.keys())}", file=sys.stderr)
        return None
    return auth_class()


def get_available_sites() -> list:
    """
    Get list of sites with configured credentials
    Returns:
        List of site codes that have credentials set
    """
    available = []

    # Check IHS
    if os.getenv('IHS_USERNAME') and os.getenv('IHS_PASSWORD'):
        available.append('ihs')

    # Check TCS
    if os.getenv('TCS_USERNAME') and os.getenv('TCS_PASSWORD'):
        available.append('tcs')

    return available


def test_authentication(site_code: Optional[str] = None):
    """
    Test authentication for one or all sites
    Args:
        site_code: Specific site to test, or None for all available
    Returns:
        Exit code (0 = success, 1 = failure)
    """
    print("=" * 60)
    print("Hockey Sites Authentication Test")
    print("=" * 60)
    print()

    if site_code:
        # Test specific site
        sites_to_test = [site_code]
    else:
        # Test all available sites
        sites_to_test = get_available_sites()
        if not sites_to_test:
            print("No credentials found!")
            print()
            print("Please set environment variables for at least one site:")
            print("  - Ice Hockey Systems: IHS_USERNAME, IHS_PASSWORD")
            print("  - The Coaches Site: TCS_USERNAME, TCS_PASSWORD")
            return 1

    all_passed = True

    for site in sites_to_test:
        print(f"Testing {site.upper()}...")
        print("-" * 60)

        auth = get_authenticator(site)
        if not auth:
            all_passed = False
            continue

        try:
            username, password = auth.get_credentials()
            print(f"  Username: {username}")
            print(f"  Password: {'*' * len(password)}")
        except ValueError as e:
            print(f"  ✗ {e}")
            all_passed = False
            continue

        if auth.login():
            print(f"  ✓ Successfully authenticated to {auth.get_site_name()}!")
            print(f"  Session cookies: {len(auth.session.cookies)} cookie(s)")
        else:
            print(f"  ✗ Authentication failed for {auth.get_site_name()}")
            all_passed = False

        print()

    print("=" * 60)
    if all_passed:
        print("✓ All authentication tests passed!")
    else:
        print("✗ Some authentication tests failed")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == '__main__':
    # Allow testing specific site via command line
    site = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(test_authentication(site))
