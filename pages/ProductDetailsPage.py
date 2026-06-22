from .BasePage import BasePage
from selenium.webdriver.common.by import By


class ProductDetailsPage(BasePage):
    """
    Page Object Model for the SauceDemo product details page.

    This page encapsulates interactions and validations related to
    an individual product, including:

        - Retrieving product information.
        - Adding a product to the shopping cart.
        - Verifying cart-related actions.
        - Navigating back to the inventory page.

    The methods provided by this class support test scenarios that
    validate product details and cart functionality from the product
    details view.
    """

    __BACK_TO_PRODUCTS_BUTTON = (By.ID, "back-to-products")
    __PRODUCT_NAME = (By.XPATH, "//div[@data-test='inventory-item-name']")
    __PRODUCT_DESCRIPTION = (
        By.XPATH, "//div[@data-test='inventory-item-desc']")
    __PRODUCT_PRICE = (By.XPATH, "//div[@data-test='inventory-item-price']")
    __ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    __REMOVE_BUTTON = (By.ID, "remove")

    def __init__(self, driver):
        """
        Initialize the ProductDetailsPage object.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def get_product_name(self):
        """
        Retrieve the product name displayed on the page.

        Returns:
            str: Product name.
        """
        return self.find_element(self.__PRODUCT_NAME).text

    def get_product_description(self):
        """
        Retrieve the product description displayed on the page.

        Returns:
            str: Product description.
        """
        return self.find_element(self.__PRODUCT_DESCRIPTION).text

    def get_product_price(self):
        """
        Retrieve the product price displayed on the page.

        Returns:
            str: Product price.
        """

        return self.find_element(self.__PRODUCT_PRICE).text

    def add_product_to_cart(self):
        """
        Add the currently displayed product to the shopping cart.
        """
        self.click(self.__ADD_TO_CART_BUTTON)

    def is_remove_button_displayed(self):
        """
        Verify that the Remove button is displayed.

        The Remove button is typically shown after a product
        has been successfully added to the cart.

        Returns:
            bool: True if the Remove button is displayed,
                  otherwise False.
        """
        return self.find_element(
            self.__REMOVE_BUTTON
        ).is_displayed()

    def click_back_to_products(self):
        """
        Navigate back to the inventory page.
        """
        self.click(self.__BACK_TO_PRODUCTS_BUTTON)
