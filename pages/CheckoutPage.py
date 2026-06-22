from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from utils.common_utils import CommonUtils


class CheckoutPage(BasePage):
    """
    Page Object Model for the SauceDemo checkout workflow.

    This page encapsulates all interactions related to the checkout
    process, including:

        - Entering customer information.
        - Navigating through checkout steps.
        - Completing or cancelling an order.
        - Retrieving order confirmation details.
        - Validating checkout errors.
        - Calculating and verifying order totals.

    The class provides reusable methods for test cases that validate
    successful and unsuccessful checkout scenarios.
    """

    __FIRST_NAME = (By.ID, "first-name")
    __LAST_NAME = (By.ID, "last-name")
    __ZIPCODE = (By.ID, "postal-code")
    __CONTINUE_BUTTON = (By.ID, "continue")
    __FINISH_BUTTON = (By.ID, "finish")
    __ERROR_VALIDATION_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    __CANCEL_BUTTON = (By.ID, "cancel")
    __PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    __TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")
    __ORDER_SUCCESS_HEADER = (By.CSS_SELECTOR, "h2.complete-header")

    def enter_checkout_details(self, firstname, lastname, zipcode):
        """
        Enter customer information required for checkout.

        Args:
            firstname (str): Customer's first name.
            lastname (str): Customer's last name.
            zipcode (str): Customer's postal/ZIP code.
        """

        self.enter_text(self.__FIRST_NAME, firstname)
        self.enter_text(self.__LAST_NAME, lastname)
        self.enter_text(self.__ZIPCODE, zipcode)

    def click_on_continue_button(self):
        """
        Click the Continue button to proceed to the order overview page.
        """
        self.click(self.__CONTINUE_BUTTON)

    def click_on_finish_button(self):
        """
        Click the Finish button to complete the checkout process.
        """
        self.click(self.__FINISH_BUTTON)

    def click_on_cancel_button(self):
        """
        Click the Cancel button to abort the checkout process.
        """
        self.click(self.__CANCEL_BUTTON)

    def get_order_confirmation(self):
        """
        Retrieve the order confirmation message displayed after
        a successful checkout.

        Returns:
            str: Order confirmation text.
        """
        return self.get_text(self.__ORDER_SUCCESS_HEADER)

    def calculate_expected_total(self, tax_percentage=0.08):
        """
        Calculate the expected order total including tax.

        Args:
            tax_percentage (float, optional): Tax rate applied to the
                subtotal. Defaults to 0.08 (8%).

        Returns:
            float: Calculated total amount including tax.
        """
        prices = self.driver.find_elements(*self.__PRODUCT_PRICES)
        subtotal = 0
        for price in prices:
            subtotal += CommonUtils.extract_value(price.text)
        total = round((subtotal+subtotal*tax_percentage), 2)
        return total

    def get_total_price(self):
        """
        Retrieve the total price displayed on the checkout overview page.

        Returns:
            str: Displayed total price.
        """
        return self.get_text(self.__TOTAL_PRICE)

    def get_validation_message(self):
        """
        Retrieve the validation error message displayed when
        mandatory checkout information is missing.

        Returns:
            str: Validation error message.
        """
        return self.get_text(self.__ERROR_VALIDATION_MESSAGE)
