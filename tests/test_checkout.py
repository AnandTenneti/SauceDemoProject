

import pytest

from pages.CartPage import CartPage
from pages.CheckoutPage import CheckoutPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from utils.common_utils import CommonUtils


@pytest.mark.checkout
class TestCheckoutPage:
    """
    Test cases related to the checkout functionality.

    These tests validate:
        - Complete checkout workflow
        - Price calculations
        - Order placement
        - Form validation messages
    """

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_checkout_flow(self, cart_with_items, fake):
        """
        Verify that a user can successfully complete the checkout process.

        Test Steps:
            1. Verify cart is initially empty.
            2. Add multiple products to the cart.
            3. Navigate to the cart page.
            4. Proceed to checkout.
            5. Enter valid customer information.
            6. Verify calculated product total matches displayed total.
            7. Complete the order.
            8. Verify order confirmation message.

        Expected Result:
            - Cart count updates correctly.
            - Product total calculation is accurate.
            - Order is placed successfully.
            - Confirmation message is displayed.
        """

        cart_page = cart_with_items.driver
        cart_page.scroll_to_checkout_button()

        cart_page.click_on_checkout()
        checkout_page = CheckoutPage(cart_with_items.driver)

        checkout_page.enter_checkout_details(
            fake.first_name(), fake.last_name(), fake.zipcode())
        checkout_page.click_on_continue_button()
        sum_of_product_prices = checkout_page.calculate_expected_total()
        product_price_total = CommonUtils.extract_value(
            checkout_page.get_total_price())

        assert sum_of_product_prices == product_price_total, (
            f"Product total mismatch. "
            f"Calculated sum={sum_of_product_prices}, "
            f"Displayed total={product_price_total}")

        checkout_page.click_on_finish_button()
        assert checkout_page.get_order_confirmation() == "Thank you for your order!"

    @pytest.mark.regression
    @pytest.mark.parametrize("first_name, last_name, postal_code,error_message",
                             [
                                 ("", "a", 1, "Error: First Name is required"),
                                 ("a", "", 1, "Error: Last Name is required"),
                                 ("a", "b", "", "Error: Postal Code is required")
                             ])
    def test_checkout_details_validation(self, cart_with_items, first_name, last_name, postal_code, error_message):
        """
        Verify validation messages are displayed when mandatory
        checkout fields are left blank.

        Test Scenarios:
            - Missing first name
            - Missing last name
            - Missing postal code

        Expected Result:
            Appropriate validation message is displayed for each
            missing required field.
        """
        cart_page = cart_with_items
        cart_page.scroll_to_checkout_button()

        cart_page.click_on_checkout()
        checkout_page = CheckoutPage(cart_with_items.driver)

        # Enter test data with missing required field
        checkout_page.enter_checkout_details(
            first_name, last_name, postal_code)
        checkout_page.click_on_continue_button()

        # Verify validation message
        assert checkout_page.get_validation_message() == error_message
