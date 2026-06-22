from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class CartPage(BasePage):
    """
    Page Object Model for the SauceDemo shopping cart page.

    This page encapsulates interactions available within the
    shopping cart, including:

        - Continuing shopping from the cart.
        - Proceeding to the checkout process.
        - Scrolling to cart action buttons when required.

    The methods provided by this class enable test cases to
    navigate between the inventory, cart, and checkout pages
    while maintaining clean separation of page-specific logic.
    """

    __CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    __CHECKOUT_BUTTON = (By.ID, "checkout")

    def click_on_continue_shopping(self):
        """
        Click the Continue Shopping button to return to
        the inventory page and continue browsing products.
        """
        self.click(self.__CONTINUE_SHOPPING_BUTTON)

    def click_on_checkout(self):
        """
        Click the Checkout button to proceed to the
        checkout information page.
        """
        self.click(self.__CHECKOUT_BUTTON)

    def scroll_to_checkout_button(self):
        """
        Scroll the page until the Checkout button is visible.

        This method is useful when running tests on smaller
        screen resolutions where the button may not be
        immediately visible within the viewport.
        """
        self.scroll_to_element(self.__CHECKOUT_BUTTON)
