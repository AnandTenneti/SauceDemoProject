from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.find_element_with_fallback(locator).click()

    def enter_text(self, locator, text):
        element = self.find_element_with_fallback(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element_with_fallback(locator).text

    def wait_until(self, timeout, condition):
        return WebDriverWait(self.driver, timeout).until(condition)

    def scroll_to_element(self, locator):
        self.driver.execute_script(
            'arguments[0].scrollIntoView(true)', self.find_element_with_fallback(locator))

    def find_element_with_fallback(self, locators):

        if len(locators) == 2 and isinstance(locators[0], str):
            return self.driver.find_element(*locators)

        for locator in locators:
            try:
                print(f"Found element using: {locator}")
                return self.driver.find_element(*locator)
            except Exception:
                continue

            raise NoSuchElementException(
                f"Element not found using any of {len(locator)} fallback locators")
