from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.BasePage import BasePage


class HomePage(BasePage):

    class SortOptions(str, Enum):
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
        super().__init__(driver)

    def click_product_by_name(self, product_name):
        product_xpath = f"(//div[@class='inventory_item_name ' and text()='{product_name}']/parent::a)"
        self.find_element((By.XPATH, product_xpath)).click()

    def select_sort_order(self, option):
        dropdown = self.find_element(self.PRODUCTS_SORT_ORDER)
        select = Select(dropdown)
        select.select_by_visible_text(option)

    def get_all_product_names(self):
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [element.text for element in elements]

    def get_all_prices(self):
        prices = self.find_elements(self.PRODUCT_PRICE)

        return [
            float(price.text.replace("$", ""))
            for price in prices
        ]

    def is_sorted_correctly(self, option: SortOptions):
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

    def is_sorted_high_to_low(self):
        prices = self.get_all_prices()
        return prices == sorted(prices, reverse=True)

    def is_sorted_low_to_high(self):
        prices = self.get_all_prices()
        return prices == sorted(prices)

    def rename_text(self, text):
        return text.replace(" ", "-").lower()

    def click_add_to_cart(self, product_name):
        formatted_name = self.rename_text(product_name)

        locator = (
            By.ID,
            f"add-to-cart-{formatted_name}"
        )
        self.click(locator)
