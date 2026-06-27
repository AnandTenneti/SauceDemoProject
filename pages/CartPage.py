from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from utils.common_utils import CommonUtils


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
    __CART_ITEMS = (By.XPATH, "//div[@class='cart_item']")

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

    def get_cart_items(self):
        """
        Retrieve all cart item elements currently displayed in the cart.

        Returns:
        list[WebElement]: List of cart item web elements.
        """
        return self.find_elements(self.__CART_ITEMS)

    def get_cart_item_count(self):
        """
        Get the total number of products currently present in the cart.

        Returns:
        int: Number of items currently in the cart.
        """
        return len(self.find_elements(self.__CART_ITEMS))

    def remove_item_from_cart(self, product_name):
        """
        Remove a specific product from the shopping cart.

        Args:
        product_name(str): Product name as displayed in the application.

        Example:
        remove_item_from_cart("Sauce Labs Backpack")
        """
        formatted_name = CommonUtils.format_product_id(product_name)
        locator = (
            By.ID,
            f"remove-{formatted_name}"
        )
        self.click(locator)

    def remove_all_items(self):
        """
        Remove all products currently present in the shopping cart.

        Iteratively clicks the remove button for each cart item until
        the cart becomes empty.

        Notes:
        - Useful for test cleanup.
        - Safe to call when the cart is already empty.
        """
        locator = (By.XPATH, "//div[@class='cart_item']//button")

        while self.find_elements(locator):
            self.find_element(locator).click()

    def get_cart_total(self):
        """
        Calculate the total price of all products currently present
        in the shopping cart.

        Returns:
        float: Sum of all product prices.
        """
        raise NotImplementedError("Needs to be implemented")
