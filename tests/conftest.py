import os
from datetime import datetime


import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from faker import Faker

from config.config import settings
from pages.HeaderPage import HeaderPage
from pages.LoginPage import LoginPage
from pages.HomePage import HomePage
from pages.CartPage import CartPage
from utils.webdriver_utils import WebDriverUtils


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome"
    )
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Execution environment: local or remote"
    )


@pytest.fixture
def driver(request):
    browserName = request.config.getoption("browser")
    env = request.config.getoption("env")
    match browserName:
        case "chrome":
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")

            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False
            }

            chrome_options.add_experimental_option("prefs", prefs)
            if env == "remote":
                driver = webdriver.Remote(
                    command_executor="http://selenium-hub:4444/wd/hub",
                    options=chrome_options
                )
            else:
                driver = webdriver.Chrome(options=chrome_options)

        case "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            if env == "remote":
                driver = webdriver.Remote(
                    command_executor="http://selenium-hub:4444/wd/hub",
                    options=firefox_options
                )
            else:
                driver = webdriver.Firefox(options=firefox_options)
        case "edge":
            edge_options = EdgeOptions()
            edge_options.add_argument("--headless")
            if env == "remote":
                driver = webdriver.Remote(
                    command_executor="http://selenium-hub:4444/wd/hub",
                    options=edge_options
                )
            else:
                driver = webdriver.Edge(options=edge_options)

        case _:
            raise ValueError(f"Unsupported browser: {browserName}")
    driver.maximize_window()
    capabilities = driver.capabilities
    allure.attach(
        f"Browser: {capabilities['browserName']}\n"
        f"Version: {capabilities['browserVersion']}",
        name="Execution Details",
        attachment_type=allure.attachment_type.TEXT
    )
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):

    driver.get(settings["base_url"])

    login_page = LoginPage(driver)

    login_page.user_login("standard_user", "secret_sauce")

    yield driver
    try:
        header_page = HeaderPage(driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            driver, header_page.get_logout_link())
        header_page.click_logout_link()
    except Exception:
        pass


@pytest.fixture
def cart_with_items(logged_in_driver):
    home_page = HomePage(logged_in_driver)
    for product in ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]:
        home_page.click_add_to_cart(product)
    HeaderPage(logged_in_driver).click_cart_icon()
    return CartPage(logged_in_driver)


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
                os.makedirs("screenshots", exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = (
                    f"screenshots/{item.name}_{timestamp}.png"
                )

                # Save first
                driver.save_screenshot(screenshot_name)

                # Then attach
                allure.attach.file(
                    screenshot_name,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

                print(f"\nScreenshot saved: {screenshot_name}")

            except Exception as e:
                print(f"\nCould not capture screenshot: {e}")


@pytest.fixture(scope="session")
def fake():
    faker = Faker()
    faker.seed_instance(42)
    return faker
