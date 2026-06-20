from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.LoginPage import LoginPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.ProductDetailsPage import ProductDetailsPage
from pages.CartPage import CartPage
from pages.CheckoutPage import CheckoutPage
from utils.webdriver_utils import WebDriverUtils


import pytest


@pytest.mark.inventory
class TestHomePage:

    def test_sort_poduct(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        WebDriverUtils.wait_until_elements_visible(logged_in_driver,
                                                   home_page.inventory_list_loaded())
        home_page.select_sort_order(HomePage.SortOptions.NAME_Z_A)
        assert home_page.is_sorted_correctly(HomePage.SortOptions.NAME_Z_A)

    def test_product_search(self, logged_in_driver):
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
        time.sleep(10)

    def test_add_multiple_products_to_cart(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0
        time.sleep(10)

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)
        assert header_page.get_cart_badge_count() == 3

    def test_checkout_flow(self, logged_in_driver):
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
        cart_page.scroll_to_checkout_button()
        cart_page.click_on_checkout()
        checkout_page = CheckoutPage(logged_in_driver)
        checkout_page.enter_checkout_details("Anand", "Kiran", 530043)
        checkout_page.click_on_continue_button()
        checkout_page.click_on_finish_button()
        assert checkout_page.order_confirmation() == "Thank you for your order!"
