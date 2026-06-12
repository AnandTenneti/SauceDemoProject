from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
import time


class CartPage(BasePage):

    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def click_on_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def click_on_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def scroll_to_checkout_button(self):
        self.scroll_to_element(self.CHECKOUT_BUTTON)
