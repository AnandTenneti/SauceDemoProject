from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import settings


class WebDriverUtils:
    @staticmethod
    def wait_until_visible(driver, locator):

        return WebDriverWait(driver, settings["timeout"]).until(EC.visibility_of_element_located(locator))

    @staticmethod
    def wait_until_elements_visible(driver, locator):
        return WebDriverWait(driver, settings["timeout"]).until(EC.visibility_of_all_elements_located(locator))

    @staticmethod
    def wait_until_clickable(driver, locator):
        return WebDriverWait(driver, settings["timeout"]).until(EC.element_to_be_clickable(locator))

    @staticmethod
    def wait_until(driver, condition, timeout=None):
        t = timeout if timeout is not None else settings["timeout"]
        return WebDriverWait(driver, t).until(condition)
