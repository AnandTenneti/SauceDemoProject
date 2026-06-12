from selenium.webdriver.common.by import By
from .BasePage import BasePage
import time


class HeaderPage(BasePage):

    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        super().__init__(driver)

    def click_menu_button(self):
        self.click(self.MENU_BUTTON)

    def click_logout_link(self):
        self.click(self.LOGOUT_LINK)

    def click_cart_icon(self):
        self.click(self.CART_ICON)

    def is_shopping_cart_badge_displayed(self):
        return self.find_elements(self.SHOPPING_CART_BADGE)

    def get_cart_badge_count(self):
        badges = self.find_elements(self.SHOPPING_CART_BADGE)

        if not badges:
            return 0

        return int(badges[0].text)

    def logout(self):
        self.click_menu_button()
        time.sleep(10)
        self.click_logout_link()
