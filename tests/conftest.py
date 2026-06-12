import allure
import pytest
from selenium import webdriver  # type: ignore[import]
from selenium.webdriver.chrome.service import Service  # type: ignore[import]
# type: ignore[import]
from webdriver_manager.chrome import ChromeDriverManager

from pages.LoginPage import LoginPage
from pages.HeaderPage import HeaderPage
from datetime import datetime
import os


@pytest.fixture
def driver():
    # driver = webdriver.Chrome()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture
def logged_in_driver(driver):

    driver.get("https://www.saucedemo.com/")

    login_page = LoginPage(driver)

    login_page.user_login("standard_user", "secret_sauce")

    yield driver

    header_page = HeaderPage(driver)
    header_page.logout()


os.makedirs("screenshots", exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = next(
            (
                value
                for value in item.funcargs.values()
                if hasattr(value, "save_screenshot")
            ),
            None,
        )

        if driver:

            try:

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                screenshot_name = (
                    f"screenshots/{item.name}_{timestamp}.png"
                )
                allure.attach.file(
                    screenshot_name,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

                driver.save_screenshot(screenshot_name)

                print(f"\nScreenshot saved: {screenshot_name}")

            except Exception as e:

                print(f"\nCould not capture screenshot: {e}")
