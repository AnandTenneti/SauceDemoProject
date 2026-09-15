import pytest
from pages.LoginPage import LoginPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.CartPage import CartPage
from selenium.webdriver.support import expected_conditions as EC
from utils.webdriver_utils import WebDriverUtils
from utils.common_utils import CommonUtils


@pytest.mark.cart
class TestCartPage:
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_removing_item_from_cart(self, cart_with_items):
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_item_from_cart("Sauce Labs Backpack")

        assert cart_page.get_cart_item_count() == 2

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_remove_all_items_from_cart(self, cart_with_items):
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_all_items()
        assert cart_page.get_cart_item_count() == 0

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_add_item_to_cart(self, seeded_driver):
        home_page = HomePage(seeded_driver)
        header_page = HeaderPage(seeded_driver)
        assert header_page.get_cart_badge_count() == 0

        product = "Sauce Labs Backpack"
        home_page.click_add_to_cart(product)
        assert header_page.get_cart_badge_count() == 1
        header_page.click_cart_icon()
        cart_page = CartPage(seeded_driver)
        assert cart_page.get_cart_item_count() == 1

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_cart_persists_after_page_refresh(self, seeded_driver):
        """
        Verify that cart contents survive a browser page refresh.

        Steps:
        1. Validate cart badge is initially empty.
        2. Add a product to the cart and verify the badge count updates.
        3. Navigate to the cart page and verify the item count.
        4. Refresh the page.
        5. Verify the item count is unchanged after refresh.

        Expected Result:
            Cart item count should remain the same before and after a page
        refresh, confirming cart state is not held only in transient
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

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_cart_persists_on_relogin(self, seeded_driver):
        """
        Verify that cart contents survive a logout/login cycle.

        Steps:
        1. Validate cart badge is initially empty.
        2. Add a product to the cart and verify the badge count updates.
        3. Navigate to the cart page and verify the item count.
        4. Log out, then log back in as the same user.
        5. Navigate to the cart page and verify the item count is
            still unchanged.

        Expected Result:
        Cart item count should remain the same across a logout/login cycle,
        confirming cart state is tied to the user's account/session rather
        than a single browser session.
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
        users = CommonUtils.open_file("testdata/users.json")
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

    def test_add_multiple_products_to_cart(self, seeded_driver):
        """
        Verify multiple products can be added to the cart.

        Steps:
        1. Validate cart is initially empty.
        2. Add multiple products.
        3. Verify cart badge count is updated.

        Expected Result:
        Cart badge count should match the number of added products.
        """
