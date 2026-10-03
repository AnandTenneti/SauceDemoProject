"""
Cart test suite for the SauceDemo application.

Covers adding and removing items, cart total calculation, and
persistence of cart contents across page refresh and logout/login.
"""


import allure
import pytest

from config.paths import USERS_JSON
from pages.CartPage import CartPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from utils.common_utils import CommonUtils
from utils.webdriver_utils import WebDriverUtils


@pytest.mark.cart
class TestCartPage:

    """
    Test cases covering cart functionality.

    Includes:
        - Adding an item to the cart
        - Removing one or all items from the cart
        - Cart total calculation, including after removing an item
        - Cart persistence across page refresh and logout/login
    """

    # ------------------------------------------------------------------
    # Add to cart
    # ------------------------------------------------------------------

    @allure.title("Verify adding an item to the cart")
    @allure.description(
        "Verify that adding a product updates the cart badge "
        "and the item count on the cart page."
    )
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_add_item_to_cart_updates_badge_and_cart_count(self, seeded_driver):
        """
        Verify that adding a product updates the cart badge and cart page.

        Args:
            seeded_driver: WebDriver fixture logged in with an empty cart.

        Steps:
            1. Verify the cart badge is initially empty.
            2. Add "Sauce Labs Backpack" to the cart.
            3. Verify the cart badge shows 1.
            4. Open the cart page.

        Expected Result:
            Cart badge count is 1 and the cart page lists exactly one item.
        """
        home_page = HomePage(seeded_driver)
        header_page = HeaderPage(seeded_driver)
        assert header_page.get_cart_badge_count() == 0

        product = "Sauce Labs Backpack"
        home_page.click_add_to_cart(product)
        assert header_page.get_cart_badge_count() == 1
        header_page.click_cart_icon()
        cart_page = CartPage(seeded_driver)
        assert cart_page.get_cart_item_count() == 1

    @allure.title("Verify adding an item to the cart")
    @allure.description(
        "Verify that adding a product updates the cart badge "
        "and the item count on the cart page."
    )
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_add_all_items_to_cart_updates_cart_count(self, cart_with_all_items):
        """
        Verify that adding all products updates the cart badge to reflect the total count.

        Args:
        cart_with_all_items: Cart page fixture with every product already added.

        Steps:
        1. Load the cart page with all items added via the fixture.
        2. Read the cart item count.

        Expected Result:
        Cart item count equals the total number of products (6).
    """

        cart_page = cart_with_all_items
        assert cart_page.get_cart_item_count() == 6

    # ------------------------------------------------------------------
    # Remove from cart
    # ------------------------------------------------------------------

    @allure.title("Verify removing an item from the cart")
    @allure.description(
        "Verify that removing one product reduces the cart item count by one."
    )
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_remove_item_from_cart_decreases_item_count(self, cart_with_items):
        """
        Verify that removing a single product reduces the cart item count.

        Args:
            cart_with_items: Cart page fixture pre-seeded with 3 items.

        Steps:
            1. Verify the cart contains 3 items.
            2. Remove "Sauce Labs Backpack" from the cart.

        Expected Result:
            Cart item count drops from 3 to 2.
        """
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_item_from_cart("Sauce Labs Backpack")

        assert cart_page.get_cart_item_count() == 2

    @allure.title("Verify removing all items from the cart")
    @allure.description(
        "Verify that removing every product leaves the cart empty."
    )
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_remove_all_items_from_cart_empties_cart(self, cart_with_items):
        """
        Verify that removing all products leaves the cart empty.

        Args:
            cart_with_items: Cart page fixture pre-seeded with 3 items.

        Steps:
            1. Verify the cart contains 3 items.
            2. Remove all items from the cart.

        Expected Result:
            Cart item count is 0.
        """
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_all_items()
        assert cart_page.get_cart_item_count() == 0

    # ------------------------------------------------------------------
    # Cart total
    # ------------------------------------------------------------------

    @allure.title("Verify cart total matches sum of item prices")
    @allure.description(
        "Verify that the sum of the item prices shown in the cart "
        "equals the expected total."
    )
    def test_cart_total_matches_sum_of_item_prices(self, cart_with_items):
        """
        Verify that the sum of the individual item prices in the cart
        matches the expected total.

        Args:
            cart_with_items: Cart page fixture pre-seeded with 3 items
                (backpack, bike light, fleece jacket).

        Steps:
            1. Verify the cart contains 3 items.
            2. Read each product's displayed price from the cart page.
            3. Sum the individual prices.

        Expected Result:
            The sum of the individual prices equals 89.97.
        """
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        sum_of_product_prices = 0.0
        total_price = 89.97
        cart_prices = cart_page.get_cart_total()
        for cart_price in cart_prices:
            sum_of_product_prices += float(
                cart_price.text.replace("$", "").strip())

        assert sum_of_product_prices == total_price

    @allure.title("Verify cart total updates after removing an item")
    @allure.description(
        "Verify that the cart total decreases by the removed item's price."
    )
    def test_cart_total_updates_after_removing_item(self, cart_with_items):
        """
        Verify that the cart total is reduced by the price of a
        removed item.

        Args:
            cart_with_items: Cart page fixture pre-seeded with 3 items
                (backpack, bike light, fleece jacket).

        Steps:
            1. Verify the cart contains 3 items and the total is 89.97.
            2. Read the price of "Sauce Labs Backpack".
            3. Remove "Sauce Labs Backpack" from the cart.

        Expected Result:
            Cart contains 2 items and the total equals 89.97 minus the
            removed item's price.
        """
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        assert cart_page.get_cart_total_amount() == 89.97
        item_price = cart_page.get_item_price_in_cart("Sauce Labs Backpack")

        item_price = float(item_price.replace("$", "").strip())

        cart_page.remove_item_from_cart("Sauce Labs Backpack")

        assert cart_page.get_cart_item_count() == 2
        assert cart_page.get_cart_total_amount() == round(89.97 - item_price, 2)

    # ------------------------------------------------------------------
    # Cart persistence
    # ------------------------------------------------------------------

    @allure.title("Verify cart persists after page refresh")
    @allure.description(
        "Verify that cart contents survive a browser page refresh."
    )
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_cart_persists_after_page_refresh(self, seeded_driver):
        """
        Verify that cart contents survive a browser page refresh.

        Args:
            seeded_driver: WebDriver fixture logged in with an empty cart.

        Steps:
            1. Verify the cart badge is initially empty.
            2. Add a product to the cart and verify the badge count updates.
            3. Navigate to the cart page and verify the item count.
            4. Refresh the page.
            5. Verify the item count is unchanged after the refresh.

        Expected Result:
            Cart item count is the same before and after a page refresh,
            confirming cart state is not held only in transient
            client-side JS state.
        """
        home_page = HomePage(seeded_driver)
        header_page = HeaderPage(seeded_driver)
        assert header_page.get_cart_badge_count() == 0

        product = "Sauce Labs Backpack"
        home_page.click_add_to_cart(product)
        assert header_page.get_cart_badge_count() == 1
        header_page.click_cart_icon()
        cart_page = CartPage(seeded_driver)
        assert cart_page.get_cart_item_count() == 1
        cart_page.refresh_page()
        assert cart_page.get_cart_item_count() == 1

    @allure.title("Verify cart persists after logout and login")
    @allure.description(
        "Verify that cart contents survive a logout/login cycle "
        "for the same user."
    )
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_cart_persists_after_relogin(self, seeded_driver):
        """
        Verify that cart contents survive a logout/login cycle.

        Args:
            seeded_driver: WebDriver fixture logged in with an empty cart.

        Steps:
            1. Verify the cart badge is initially empty.
            2. Add a product to the cart and verify the badge count updates.
            3. Navigate to the cart page and verify the item count.
            4. Log out, then log back in as the same user.
            5. Navigate to the cart page and verify the item count.

        Expected Result:
            Cart item count is the same across a logout/login cycle,
            confirming cart state is tied to the user's account/session
            rather than a single browser session.
        """
        home_page = HomePage(seeded_driver)
        header_page = HeaderPage(seeded_driver)
        assert header_page.get_cart_badge_count() == 0

        product = "Sauce Labs Backpack"
        home_page.click_add_to_cart(product)
        assert header_page.get_cart_badge_count() == 1
        header_page.click_cart_icon()
        cart_page = CartPage(seeded_driver)
        assert cart_page.get_cart_item_count() == 1
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            seeded_driver, header_page.get_logout_link())
        header_page.click_logout_link()
        users = CommonUtils.open_file(USERS_JSON)
        user = next(
            (u for u in users if u["username"] == "standard_user"), None)
        assert user is not None, "standard_user not found in testdata/users.json"

        login_page = LoginPage(seeded_driver)
        login_page.user_login(user["username"], user["password"])

        home_page = HomePage(seeded_driver)
        header_page = HeaderPage(seeded_driver)
        header_page.click_cart_icon()
        cart_page = CartPage(seeded_driver)
        assert cart_page.get_cart_item_count() == 1
