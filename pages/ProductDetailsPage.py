from .BasePage import BasePage
from selenium.webdriver.common.by import By


class ProductDetailsPage(BasePage):

    BACK_TO_PRODUCTS_BUTTON = (By.ID, "back-to-products")
    PRODUCT_NAME = (By.XPATH, "//div[@data-test='inventory-item-name']")
    PRODUCT_DESCRIPTION = (By.XPATH, "//div[@data-test='inventory-item-desc']")
    PRODUCT_PRICE = (By.XPATH, "//div[@data-test='inventory-item-price']")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    REMOVE_BUTTON = (By.ID, "remove")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_name(self):
        return self.find_element(self.PRODUCT_NAME).text

    def get_product_description(self):
        return self.find_element(self.PRODUCT_DESCRIPTION).text

    def get_product_price(self):
        return self.find_element(self.PRODUCT_PRICE).text

    def add_product_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def is_remove_button_displayed(self):
        return self.find_element(
            self.REMOVE_BUTTON
        ).is_displayed()
