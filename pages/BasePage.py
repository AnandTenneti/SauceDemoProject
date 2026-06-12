from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.find_element(locator).click()

    def enter_text(self, locator, text):
        self.find_element(locator).send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def wait_until(self, timeout, condition):
        return WebDriverWait(self.driver, timeout).until(condition)

    def scroll_to_element(self, locator):
        self.driver.execute_script(
            'arguments[0].scrollIntoView(true)', self.find_element(locator))

    def get_self_healed_locator(self, driver, locators):
        for locator in locators:
            try:
                element = driver.find_element(*locator)
                print(f"Found element using locator: {locator}")
                return element
            except Exception:
                continue

        raise Exception("Element not found using any locator")
