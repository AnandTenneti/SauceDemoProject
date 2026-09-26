"""
Login test suite for the SauceDemo application.

Covers positive and negative login scenarios, including logout
verification and data-driven variants fed by inline parameters
and JSON, CSV and XLSX test data.
"""


import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC

from config.config import settings
from config.paths import USERS_CSV, USERS_JSON, USERS_XLSX
from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from utils.common_utils import CommonUtils
from utils.webdriver_utils import WebDriverUtils


@pytest.mark.login
class TestLogin:

    """
    Test cases covering login functionality.

    Includes:
        - Successful login and logout for a standard user
        - Login with multiple valid users (inline, JSON, CSV, XLSX data)
        - Invalid login validation (wrong username, empty fields)
        - Error message verification, inline and from JSON test data
    """

    @allure.title("Verify successful login")
    @allure.description(
        "Verify that a valid user can login successfully"
    )
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_user_login(self, logged_in_driver):
        """
        Verify that an already logged-in standard user can reach the
        inventory page and log out.

        Args:
            logged_in_driver: WebDriver fixture authenticated before the test.

        Steps:
            1. Wait for the inventory page to load.
            2. Verify the URL contains "inventory".
            3. Open the menu and click Logout.

        Expected Result:
            Inventory page is shown after login and the login page
            (title "Swag Labs") is shown after logout.
        """
        WebDriverUtils.wait_until(
            logged_in_driver, EC.url_contains("inventory"))
        home_page = HomePage(logged_in_driver)

        assert "inventory" in home_page.get_current_url()
        header_page = HeaderPage(logged_in_driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            logged_in_driver, header_page.get_logout_link())
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            logged_in_driver, EC.title_contains("Swag Labs"))
        assert "Swag Labs" in logged_in_driver.title

    @allure.title("Verify login with valid user credentials")
    @allure.description(
        "Verify that users with valid credentials can log in successfully "
        "and are redirected to the inventory page."
    )
    @pytest.mark.parametrize("username,password", [
        ("standard_user", "secret_sauce"),
        ("visual_user", "secret_sauce")
    ])
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, driver, username, password):
        """
        Verify login and logout for multiple valid users.

        Args:
            driver: WebDriver fixture.
            username: Valid SauceDemo username (standard_user, visual_user).
            password: Valid SauceDemo password.

        Steps:
            1. Open the application base URL.
            2. Login with the given credentials.
            3. Verify the inventory page title.
            4. Logout via the menu.

        Expected Result:
            User logs in successfully, lands on the inventory page
            and returns to the login page after logout.
        """

        driver.get(settings["base_url"])

        login_page = LoginPage(driver)

        login_page.user_login(username, password)
        WebDriverUtils.wait_until(
            driver, EC.url_contains("inventory"))
        home_page = HomePage(driver)
        assert "Swag Labs" in home_page.get_title()
        header_page = HeaderPage(driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            driver, header_page.get_logout_link())
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            driver, EC.title_contains("Swag Labs"))
        assert "Swag Labs" in driver.title

    valid_users = CommonUtils.open_filetype(USERS_JSON)

    @allure.title("Verify successful login")
    @allure.description(
        "Verify that a valid user can login successfully"
    )
    @pytest.mark.parametrize("data", valid_users)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.datadriven
    def test_login_with_valid_user_types_from_json(self, driver, data):
        """
        Verify login and logout using credentials loaded from a JSON file.

        Args:
            driver: WebDriver fixture.
            data: Dictionary with "username" and "password" keys,
                one entry per user type from the users JSON file.

        Expected Result:
            User logs in successfully and returns to the login page
            after logout.
        """
        driver.get(settings["base_url"])

        login_page = LoginPage(driver)
        username = data["username"]
        password = data["password"]
        login_page.user_login(username, password)
        WebDriverUtils.wait_until(
            driver, EC.url_contains("inventory"))
        home_page = HomePage(driver)
        assert "Swag Labs" in home_page.get_title()

        header_page = HeaderPage(driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            driver, header_page.get_logout_link()
        )
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)
        assert "Swag Labs" in login_page.get_title()

    @allure.title("Verify unsuccessful login")
    @allure.description(
        "Verify error message is displayed on entering invalid user details"
    )
    @pytest.mark.smoke
    def test_login_with_invalid_username(self, driver):
        """
        Verify the error message shown for an unknown username.

        Args:
            driver: WebDriver fixture.

        Steps:
            1. Open the application base URL.
            2. Login with username "standard_user1" and a valid password.

        Expected Result:
            Error "Username and password do not match any user in this
            service" is displayed.
        """
        error_message = "Epic sadface: Username and password do not match any user in this service"

        driver.get(settings["base_url"])

        WebDriverUtils.wait_until(driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)

        login_page.user_login("standard_user1", "secret_sauce")
        assert login_page.get_error_message() == error_message

   # Data Driven tests

    @pytest.mark.parametrize("username,password,error_message", [
        ("standard_user1", "secret_sauce",
         "Epic sadface: Username and password do not match any user in this service"),
        ("standard_user", "", "Epic sadface: Password is required"),
        ("", "test", "Epic sadface: Username is required")
    ])
    @pytest.mark.regression
    def test_login_validation_for_invalid_credentials(self, driver, username, password, error_message):
        """
        Verify validation messages for invalid login inputs.

        Args:
            driver: WebDriver fixture.
            username: Username to enter (may be empty).
            password: Password to enter (may be empty).
            error_message: Expected error text for this combination.

        Scenarios:
            - Unknown username with valid password
            - Valid username with empty password
            - Empty username with any password

        Expected Result:
            Displayed error message matches error_message exactly.
        """
        driver.get(settings["base_url"])

        WebDriverUtils.wait_until(driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)
        login_page.user_login(username, password)

        assert login_page.get_error_message(
        ) == error_message

    invalid_users = CommonUtils.open_filetype("testdata/error_messages.json")

    @pytest.mark.parametrize("user_data", invalid_users)
    @pytest.mark.regression
    @pytest.mark.datadriven
    def test_login_validation_from_error_data_json(self, driver, user_data):
        """
        Verify login validation messages using data-driven JSON test data.

        Args:
            driver: WebDriver fixture.
            user_data: Dictionary with "username", "password" and
                "error_message" keys from error_messages.json.

        Expected Result:
            Displayed error message matches the expected message
            from the test data.
        """
        driver.get(settings["base_url"])

        WebDriverUtils.wait_until(driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)
        username = user_data["username"]
        password = user_data["password"]
        error_message = user_data["error_message"]
        login_page.user_login(username, password)

        assert login_page.get_error_message(
        ) == error_message

    valid_users = CommonUtils.open_filetype(USERS_CSV)

    @allure.title("Verify successful login")
    @allure.description(
        "Verify that a valid user can login successfully"
    )
    @pytest.mark.parametrize("username,password", valid_users)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_valid_user_types_from_csv(self, driver, username, password):
        """
        Verify login and logout using credentials loaded from a CSV file.

        Args:
            driver: WebDriver fixture.
            username: Valid username from a row of the users CSV.
            password: Valid password from the same row.

        Expected Result:
            User logs in successfully and returns to the login page
            after logout.
        """
        driver.get(settings["base_url"])

        login_page = LoginPage(driver)
        login_page.user_login(username, password)
        WebDriverUtils.wait_until(
            driver, EC.url_contains("inventory"))
        home_page = HomePage(driver)
        assert "Swag Labs" in home_page.get_title()

        header_page = HeaderPage(driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            driver, header_page.get_logout_link()
        )
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)
        assert "Swag Labs" in login_page.get_title()

    valid_users = CommonUtils.open_filetype(USERS_XLSX)

    @allure.title("Verify successful login")
    @allure.description(
        "Verify that a valid user can login successfully"
    )
    @pytest.mark.parametrize("username,password", valid_users)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.datadriven
    def test_login_with_valid_user_types_from_xlsx(self, driver, username, password):
        """
        Verify login and logout using credentials loaded from an Excel file.

        Args:
            driver: WebDriver fixture.
            username: Valid username from a row of the users XLSX sheet.
            password: Valid password from the same row.

        Expected Result:
            User logs in successfully and returns to the login page
            after logout.
        """
        driver.get(settings["base_url"])

        login_page = LoginPage(driver)
        login_page.user_login(username, password)
        WebDriverUtils.wait_until(
            driver, EC.url_contains("inventory"))
        home_page = HomePage(driver)
        assert "Swag Labs" in home_page.get_title()

        header_page = HeaderPage(driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            driver, header_page.get_logout_link()
        )
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)
        assert "Swag Labs" in login_page.get_title()
