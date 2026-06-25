from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HeaderPage(BasePage):
    """
    Page Object representing the header section of the SauceDemo application.

    Provides actions and validations related to:
    - Navigation menu
    - Shopping cart
    - User logout functionality
    """

    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    __LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        """
        Initialize HeaderPage with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def click_menu_button(self):
        """Click the hamburger menu button."""
        self.click(self.MENU_BUTTON)

    def click_logout_link(self):
        """Click the logout link from the side menu."""
        self.click(self.__LOGOUT_LINK)

    def click_cart_icon(self):
        """Navigate to the shopping cart page."""
        self.click(self.CART_ICON)

    def is_shopping_cart_badge_displayed(self):
        """
        Check whether the shopping cart badge is present.

        Returns:
            list: List of matching badge elements.
        """
        return self.find_elements(self.SHOPPING_CART_BADGE)

    def get_cart_badge_count(self):
        """
        Get the number displayed on the shopping cart badge.

        Returns:
            int: Number of items in the cart. Returns 0 if badge is not present.
        """
        badges = self.find_elements(self.SHOPPING_CART_BADGE)

        if not badges:
            return 0

        return int(badges[0].text)

    def logout(self):
        """
        Log out the currently logged-in user.

        Opens the menu and clicks the logout link.
        """
        self.click_menu_button()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(self.__LOGOUT_LINK))
        self.click_logout_link()

    def is_logout_visible(self):
        """
        Return the logout link locator.

        Intended for use with explicit waits or visibility checks.

        Returns:
            tuple: Selenium locator for the logout link.
        """
        return self.__LOGOUT_LINK
