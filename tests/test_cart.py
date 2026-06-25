

from pages.CartPage import CartPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage


import pytest


@pytest.mark.cart
class TestCartPage:

    def test_add_multiple_products_to_cart(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)

        assert header_page.get_cart_badge_count() == 3

        header_page.click_cart_icon()
        cart_page = CartPage(logged_in_driver)
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_item_from_cart("Sauce Labs Backpack")

        assert cart_page.get_cart_item_count() == 2

    def test_remove_all_products_from_cart(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)

        assert header_page.get_cart_badge_count() == 3
        header_page.click_cart_icon()
        cart_page = CartPage(logged_in_driver)
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_all_items()
        # time.sleep(10)
        assert cart_page.get_cart_item_count() == 0
