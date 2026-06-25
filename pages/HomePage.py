from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.BasePage import BasePage
from utils.common_utils import CommonUtils


class HomePage(BasePage):
    """
    Page Object Model for the SauceDemo inventory (home) page.

    This page encapsulates interactions related to product browsing
    and inventory management, including:

        - Viewing available products.
        - Selecting products by name.
        - Adding products to the shopping cart.
        - Sorting products by name or price.
        - Retrieving product names and prices.
        - Validating sorting functionality.

    The methods in this class support test scenarios that verify
    inventory display, product selection, cart operations, and
    sorting behavior within the application.
    """

    class SortOptions(str, Enum):
        """
        Supported product sorting options available on the inventory page.
        """
        PRICE_LOW_TO_HIGH = "Price (low to high)"
        PRICE_HIGH_TO_LOW = "Price (high to low)"
        NAME_A_Z = "Name (A to Z)"
        NAME_Z_A = "Name (Z to A)"

    PRODUCTS = (By.CSS_SELECTOR, "div.inventory_list div.inventory_item")
    PRODUCT_PRICE = (
        By.CSS_SELECTOR, "div.inventory_item div.inventory_item_price")
    PRODUCT_NAMES = (
        By.CSS_SELECTOR, "div.inventory_item div.inventory_item_name")
    PRODUCTS_SORT_ORDER = (By.CLASS_NAME, "product_sort_container")

    def __init__(self, driver):
        """
        Initialize the HomePage object.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def click_product_by_name(self, product_name):
        """
        Open the product details page for the specified product.

        Args:
            product_name (str): Name of the product to select.
        """
        product_xpath = f"(//div[@class='inventory_item_name ' and text()='{product_name}']/parent::a)"
        self.find_element((By.XPATH, product_xpath)).click()

    def select_sort_order(self, option):
        """
        Select a sorting option from the product sort dropdown.

        Args:
            option (str): Visible text of the sorting option.
        """
        dropdown = self.find_element(self.PRODUCTS_SORT_ORDER)
        select = Select(dropdown)
        select.select_by_visible_text(option)

    def get_all_product_names(self):
        """
        Retrieve the names of all displayed products.

        Returns:
            list[str]: List of product names.
        """
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [element.text for element in elements]

    def get_all_prices(self):
        """
        Retrieve the prices of all displayed products.

        Returns:
            list[float]: List of product prices.
        """
        prices = self.find_elements(self.PRODUCT_PRICE)

        return [
            float(price.text.replace("$", ""))
            for price in prices
        ]

    def is_sorted_correctly(self, option: SortOptions):
        """
        Verify that products are sorted according to the specified option.

        Args:
            option (SortOptions): Expected sorting order.

        Returns:
            bool: True if products are sorted correctly, otherwise False.
        """
        prices = self.get_all_prices()
        names = self.get_all_product_names()
        match option:

            case self.SortOptions.PRICE_LOW_TO_HIGH:
                return prices == sorted(prices)

            case self.SortOptions.PRICE_HIGH_TO_LOW:
                return prices == sorted(prices, reverse=True)

            case self.SortOptions.NAME_A_Z:
                return names == sorted(names)

            case self.SortOptions.NAME_Z_A:
                return names == sorted(names, reverse=True)
        return False

    def click_add_to_cart(self, product_name):
        """
        Add the specified product to the shopping cart.

        Args:
            product_name (str): Name of the product to add.
        """
        formatted_name = CommonUtils.format_product_id(product_name)

        locator = (
            By.ID,
            f"add-to-cart-{formatted_name}"
        )
        self.click(locator)

    def inventory_list_loaded(self):
        """
        Return the inventory list locator for use in page load
        validation or explicit wait conditions.

        Returns:
            tuple: Locator representing the inventory list.
        """
        return self.PRODUCTS

    def is_inventory_page_loaded(self):
        return "inventory" in self.get_current_url()
