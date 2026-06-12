from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)

    def user_login(self, username, password):

        self.enter_text(self.USERNAME_INPUT, username)

        self.enter_text(self.PASSWORD_INPUT, password)

        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
