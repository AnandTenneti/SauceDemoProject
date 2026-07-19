import os
from datetime import datetime

# Third-party
import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Local application
from config.config import settings
from pages.CartPage import CartPage
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from utils.common_utils import CommonUtils
from utils.webdriver_utils import WebDriverUtils
from utils.session_seeder import SessionSeeder


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
    users = CommonUtils.open_file("testdata/users.json")

    user = next((
        u for u in users
        if u["username"] == "standard_user"
    ), None)
    assert user is not None, "standard_user not found in testdata/users.json"
    login_page.user_login(user["username"], user["password"])

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
def seeded_driver(driver):
    """
    Authenticated driver via cookie-injection state seeding, bypassing the
    login UI entirely.

    Use this instead of `logged_in_driver` for tests that merely *require*
    an authenticated session (cart, inventory, product details) but are not
    themselves verifying login behavior — it skips two page loads and a
    form submission per test. Tests that verify login/logout behavior
    itself should keep using `logged_in_driver`, since that fixture
    exercises the real UI flow.
    """
    users = CommonUtils.open_file("testdata/users.json")
    user = next((u for u in users if u["username"] == "standard_user"), None)
    assert user is not None, "standard_user not found in testdata/users.json"

    SessionSeeder.seed_authenticated_session(driver, user["username"])
    yield driver


@pytest.fixture
def cart_with_items(seeded_driver):
    home_page = HomePage(seeded_driver)
    for product in ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]:
        home_page.click_add_to_cart(product)
    HeaderPage(seeded_driver).click_cart_icon()
    yield CartPage(seeded_driver)


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


@pytest.fixture(scope="function")
def fake():
    faker = Faker()
    faker.seed_instance(42)
    return faker
