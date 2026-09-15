from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BasePage():

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.find_element_with_fallback(locator).click()

    def enter_text(self, locator, text):
        element = self.find_element_with_fallback(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element_with_fallback(locator).text

    def scroll_to_element(self, locator):
        self.driver.execute_script(
            'arguments[0].scrollIntoView(true)', self.find_element_with_fallback(locator))

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def find_element_with_fallback(self, locators, timeout=10, fallback_timeout=3):
        """
        Find an element, waiting for it to be present in the DOM rather than
        checking once. Supports either a single locator tuple or a list of
        fallback locator tuples tried in order.

        Args:
            locators: A single (By, value) tuple, or a list of such tuples
                to try in order until one succeeds.
            timeout: Seconds to wait for a single locator.
            fallback_timeout: Seconds to wait per locator when trying a
                fallback list — kept shorter since later tiers are expected
                to usually not be needed.

        Returns:
            WebElement: The first element found.

        Raises:
            NoSuchElementException: If no locator resolves within its timeout.
        """
        # Single locator
        if (
            isinstance(locators, tuple)
            and len(locators) == 2
            and isinstance(locators[0], str)
        ):
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locators)
                )
            except TimeoutException:
                raise NoSuchElementException(f"Element not found: {locators}")

        # Fallback locators
        failed = []

        for locator in locators:
            try:
                element = WebDriverWait(self.driver, fallback_timeout).until(
                    EC.presence_of_element_located(locator)
                )
                print(f"✓ Found element using: {locator}")
                return element
            except TimeoutException:
                failed.append(locator)

        raise NoSuchElementException(
            f"Element not found. Tried locators: {failed}"
        )

    def find_elements(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return []
        return self.driver.find_elements(*locator)

    def refresh_page(self):
        self.driver.refresh()
