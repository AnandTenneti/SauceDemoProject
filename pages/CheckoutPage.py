from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from utils.common_utils import CommonUtils


class CheckoutPage(BasePage):

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    ZIPCODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")
    ORDER_SUCCESS_HEADER = (By.CSS_SELECTOR, "h2.complete-header")

    def enter_checkout_details(self, firstname, lastname, zipcode):
        self.enter_text(self.FIRST_NAME, firstname)
        self.enter_text(self.LAST_NAME, lastname)
        self.enter_text(self.ZIPCODE, zipcode)

    def click_on_continue_button(self):
        self.click(self.CONTINUE_BUTTON)

    def click_on_finish_button(self):
        self.click(self.FINISH_BUTTON)

    def click_on_cancel_button(self):
        self.click(self.CANCEL_BUTTON)

    def order_confirmation(self):
        return self.get_text(self.ORDER_SUCCESS_HEADER)

    def get_total_product_prices(self, tax_percentage=0.08):
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        subtotal = 0
        for price in prices:
            subtotal += CommonUtils.extract_value(price.text)
        total = round((subtotal+subtotal*tax_percentage), 2)
        return total

    def get_total_price(self):
        return self.get_text(self.TOTAL_PRICE)
