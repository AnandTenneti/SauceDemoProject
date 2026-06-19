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
from faker import Faker
from utils.common_utils import CommonUtils

import pytest


class TestCheckoutPage:
    @pytest.mark.skip(reason="Skipping for now")
    def test_sort_poduct(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        time.sleep(10)
        home_page.select_sort_order(HomePage.SortOptions.NAME_Z_A)
        time.sleep(10)
        assert home_page.is_sorted_correctly(HomePage.SortOptions.NAME_Z_A)
        time.sleep(10)

    @pytest.mark.skip(reason="Skipping for now")
    def test_product_search(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        time.sleep(10)
        product_name = "Sauce Labs Backpack"
        home_page.click_product_by_name(product_name)
        product_page = ProductDetailsPage(logged_in_driver)
        displayed_product_name = product_page.get_product_name()
        assert displayed_product_name == product_name
        product_page.add_product_to_cart()
        assert product_page.is_remove_button_displayed()
        time.sleep(10)

    @pytest.mark.skip(reason="Skipping for now")
    def test_add_multiple_products_to_cart(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0
        time.sleep(10)

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)
            time.sleep(10)

        assert header_page.get_cart_badge_count() == 3
        time.sleep(10)

    @pytest.mark.smoke
    def test_checkout_flow(self, logged_in_driver):
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0
        # time.sleep(10)

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)
            # time.sleep(10)

        assert header_page.get_cart_badge_count() == 3

        header_page.click_cart_icon()

        cart_page = CartPage(logged_in_driver)
        cart_page.scroll_to_checkout_button()
        # time.sleep(10)
        cart_page.click_on_checkout()
        checkout_page = CheckoutPage(logged_in_driver)
        faker = Faker()
        checkout_page.enter_checkout_details(
            faker.first_name(), faker.last_name(), faker.zipcode())
        checkout_page.click_on_continue_button()
        sum_of_product_prices = checkout_page.get_total_product_prices()
        print(sum_of_product_prices)
        product_price_total = CommonUtils.extract_value(
            checkout_page.get_total_price())

        assert sum_of_product_prices == product_price_total, (
            f"Product total mismatch. "
            f"Calculated sum={sum_of_product_prices}, "
            f"Displayed total={product_price_total}")

        checkout_page.click_on_finish_button()
        assert checkout_page.order_confirmation() == "Thank you for your order!"

        # time.sleep(10)

    @pytest.mark.parametrize("first_name, last_name, postal_code,error_message",
                             [
                                 ("", "a", 1, "Error: First Name is required"),
                                 ("a", "", 1, "Error: Last Name is required"),
                                 ("a", "b", "", "Error: Postal Code is required")
                             ])
    def test_checkout_details_validation(self, logged_in_driver, first_name, last_name, postal_code, error_message):
        home_page = HomePage(logged_in_driver)
        header_page = HeaderPage(logged_in_driver)
        assert header_page.get_cart_badge_count() == 0
        time.sleep(10)

        product_list = ["Sauce Labs Backpack",
                        "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        for product in product_list:
            home_page.click_add_to_cart(product)
            time.sleep(10)

        assert header_page.get_cart_badge_count() == 3

        header_page.click_cart_icon()

        cart_page = CartPage(logged_in_driver)
        cart_page.scroll_to_checkout_button()
        time.sleep(10)
        cart_page.click_on_checkout()
        checkout_page = CheckoutPage(logged_in_driver)
        checkout_page.enter_checkout_details(
            first_name, last_name, postal_code)
        checkout_page = CheckoutPage(logged_in_driver)
        checkout_page.click_on_continue_button()
        assert checkout_page.get_validation_message() == error_message
