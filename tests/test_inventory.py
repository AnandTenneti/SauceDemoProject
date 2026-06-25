

from faker import Faker
import pytest

from pages.CartPage import CartPage
from pages.CheckoutPage import CheckoutPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from pages.ProductDetailsPage import ProductDetailsPage
from utils.webdriver_utils import WebDriverUtils


@pytest.mark.inventory
class TestHomePage:
    """
    Test suite for validating inventory and shopping cart functionality.

    Preconditions:
    - User must be logged in successfully.
    - The `logged_in_driver` fixture provides an authenticated session.
    """

    def test_sort_product(self, logged_in_driver):
        """
        Verify that products can be sorted correctly.

        Steps:
        1. Wait for inventory items to load.
        2. Select sorting option (Name Z to A).
        3. Validate products are displayed in the expected order.

        Expected Result:
        Products should be sorted in descending alphabetical order.
        """
        home_page = HomePage(logged_in_driver)
        WebDriverUtils.wait_until_elements_visible(logged_in_driver,
                                                   home_page.inventory_list_loaded())
        home_page.select_sort_order(HomePage.SortOptions.NAME_Z_A)
        assert home_page.is_sorted_correctly(HomePage.SortOptions.NAME_Z_A)

    def test_product_search(self, logged_in_driver):
        """
        Verify product navigation and add-to-cart functionality.

        Steps:
        1. Wait for inventory items to load.
        2. Open a specific product.
        3. Validate product details page.
        4. Add the product to the cart.
        5. Verify the Remove button is displayed.

        Expected Result:
        Product details should match the selected product and
        the product should be added successfully to the cart.
        """
        home_page = HomePage(logged_in_driver)
        WebDriverUtils.wait_until_elements_visible(logged_in_driver,
                                                   home_page.inventory_list_loaded())
        product_name = "Sauce Labs Backpack"
        home_page.click_product_by_name(product_name)
        product_page = ProductDetailsPage(logged_in_driver)
        displayed_product_name = product_page.get_product_name()
        assert displayed_product_name == product_name
        product_page.add_product_to_cart()
        assert product_page.is_remove_button_displayed()

    def test_add_multiple_products_to_cart(self, logged_in_driver):
        """
        Verify multiple products can be added to the cart.

        Steps:
        1. Validate cart is initially empty.
        2. Add multiple products.
        3. Verify cart badge count is updated.

        Expected Result:
        Cart badge count should match the number of added products.
        """
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)
        assert header_page.get_cart_badge_count() == 3
