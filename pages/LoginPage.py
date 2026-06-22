from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class LoginPage(BasePage):

    """
    Page Object representing the SauceDemo login page.

    This class provides methods to perform user authentication
    and retrieve login validation messages.
    """

    __USERNAME_INPUT = (By.ID, "user-name")
    __PASSWORD_INPUT = (By.ID, "password")
    __LOGIN_BUTTON = (By.ID, "login-button")
    __ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        """
        Initialize the LoginPage.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def enter_username(self, username):
        """Enter text into the username field."""
        self.enter_text(self.__USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter text into the password field."""
        self.enter_text(self.__PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click the Login button."""
        self.click(self.__LOGIN_BUTTON)

    def user_login(self, username, password):
        """
        Perform login using the provided credentials.

        Args:
            username (str): Username used for authentication.
            password (str): Password associated with the user account.
        """

        self.enter_text(self.__USERNAME_INPUT, username)

        self.enter_text(self.__PASSWORD_INPUT, password)

        self.click(self.__LOGIN_BUTTON)

    def get_error_message(self):
        """
        Retrieve the login error message displayed on the page.

        Returns:
            str: Error message text.
        """
        return self.get_text(self.__ERROR_MESSAGE)
