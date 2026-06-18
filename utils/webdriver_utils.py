from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverUtils:
    @staticmethod
    def wait_until_visible(driver, locator):

        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))

    @staticmethod
    def wait_until_clickable(driver, locator):
        return WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))

    @staticmethod
    def wait_until(driver, condition, timeout=10):
        return WebDriverWait(driver, timeout).until(condition)
