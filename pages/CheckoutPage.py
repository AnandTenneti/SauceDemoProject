from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    ZIPCODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")
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
