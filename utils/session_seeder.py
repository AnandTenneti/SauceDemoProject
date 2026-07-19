"""
Session state seeding for SauceDemo.

SauceDemo is an Angular SPA. Its authenticated session is represented by a
``session-username`` cookie that the app reads on load — so an authenticated
session can be seeded directly via cookie injection instead of driving the
login form through the UI on every test that merely *requires* a logged-in
state (as opposed to tests that are actually verifying login behavior).

Note on cart state: unlike the session cookie, SauceDemo's cart contents are
held in the Angular app's in-memory component state rather than being
reliably persisted to localStorage/sessionStorage. Injecting cart state via
``execute_script`` was evaluated and rejected for this reason — it produced
inconsistent results across page loads. Cart setup therefore continues to go
through the UI (see the ``cart_with_items`` fixture in conftest.py), while
login/session setup is seeded directly here.
"""

from config.config import settings


class SessionSeeder:
    """Seeds authenticated browser state for SauceDemo without using the UI."""

    SESSION_COOKIE_NAME = "session-username"

    @staticmethod
    def seed_authenticated_session(driver, username):
        """
        Seed an authenticated session for the given username by injecting
        the session cookie directly, bypassing the login form.

        Args:
            driver: Active Selenium WebDriver instance.
            username (str): SauceDemo username to authenticate as
                (e.g. "standard_user").

        Returns:
            None. The driver is left on the inventory page, authenticated
            as ``username``.

        Notes:
            Cookies can only be set for the domain of the currently loaded
            page, so this first navigates to the base URL (login page),
            injects the cookie, then reloads directly to the inventory page.
        """
        base_url = settings["base_url"]

        # A page from the target domain must be loaded before a cookie
        # for that domain can be added.
        driver.get(base_url)
        driver.add_cookie({
            "name": SessionSeeder.SESSION_COOKIE_NAME,
            "value": username,
        })

        # Reload directly into the authenticated area; the app reads the
        # cookie on load and treats the session as already logged in.
        driver.get(f"{base_url.rstrip('/')}/inventory.html")

    @staticmethod
    def clear_session(driver):
        """
        Clear the seeded session cookie, returning the browser to a
        logged-out state without going through the UI logout flow.

        Args:
            driver: Active Selenium WebDriver instance.
        """
        driver.delete_cookie(SessionSeeder.SESSION_COOKIE_NAME)
