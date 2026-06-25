"""
Login test suite for SauceDemo application.

This module contains positive and negative login scenarios,
including data-driven tests using parameterization and JSON files.
"""


import allure
import pytest

from selenium.webdriver.support import expected_conditions as EC

from pages.HeaderPage import HeaderPage
from pages.LoginPage import LoginPage
from pages.HomePage import HomePage
from utils.common_utils import CommonUtils
from utils.webdriver_utils import WebDriverUtils
from config.config import settings


@pytest.mark.login
class TestLogin:

    """
    Test cases covering login functionality.

    Includes:
    - Successful login validation
    - Login using multiple valid users
    - Data-driven login tests from JSON
    - Invalid login validations
    - Error message verification
    """

    @allure.title("Verify successful login")
    @allure.description(
        "Verify that a valid user can login successfully"
    )
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_user_login(self, logged_in_driver):
        """
        Verify that a standard user can login and logout successfully.

        Steps:
            1. Open application.
            2. Login using valid credentials.
            3. Verify inventory page is displayed.
            4. Logout successfully.

        Expected Result:
            User is redirected to inventory page after login
            and login page after logout.
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

    @pytest.mark.parametrize("username,password", [
        ("standard_user", "secret_sauce"),
        ("visual_user", "secret_sauce")
    ])
    def test_login_with_valid_credentials(self, logged_in_driver, username, password):
        """
        Verify login functionality for multiple valid users.

        Args:
            username: Valid SauceDemo username.
            password: Valid SauceDemo password.

        Expected Result:
            User should login successfully and logout without errors.
        """

        WebDriverUtils.wait_until(
            logged_in_driver, EC.url_contains("inventory"))
        assert "Swag Labs" in logged_in_driver.title
        header_page = HeaderPage(logged_in_driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            logged_in_driver, header_page.get_logout_link())
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            logged_in_driver, EC.title_contains("Swag Labs"))
        assert "Swag Labs" in logged_in_driver.title

    valid_users = CommonUtils.open_file("testdata/users.json")

    @pytest.mark.parametrize("data", valid_users)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_valid_user_types_from_json(self, logged_in_driver, data):
        """
        Verify login functionality using user credentials
        loaded from a JSON file.

        Args:
            data: Dictionary containing username and password.

        Expected Result:
            User should login successfully and logout.
        """
        WebDriverUtils.wait_until(
            logged_in_driver, EC.url_contains("inventory"))
        home_page = HomePage(logged_in_driver)
        assert "Swag Labs" in home_page.get_title()

        header_page = HeaderPage(logged_in_driver)
        header_page.click_menu_button()
        WebDriverUtils.wait_until_clickable(
            logged_in_driver, header_page.get_logout_link()
        )
        header_page.click_logout_link()
        WebDriverUtils.wait_until(
            logged_in_driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(logged_in_driver)
        assert "Swag Labs" in login_page.get_title()

    def test_login_with_invalid_username(self, driver):
        """
        Verify error message is displayed when
        an invalid username is entered.

        Expected Result:
            Appropriate login error message should be displayed.
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
    def test_login_validation_for_invalid_credentials(self, driver, username, password, error_message):
        """
        Verify validation messages for invalid login scenarios.

        Scenarios:
            - Invalid username
            - Empty password
            - Empty username

        Expected Result:
            Correct validation message should be displayed.
        """
        driver.get(settings["base_url"])

        WebDriverUtils.wait_until(driver, EC.title_contains("Swag Labs"))
        login_page = LoginPage(driver)
        login_page.user_login(username, password)

        assert login_page.get_error_message(
        ) == error_message

    invalid_users = CommonUtils.open_file("testdata/error_messages.json")

    @pytest.mark.parametrize("user_data", invalid_users)
    def test_login_validation_from_error_data_json(self, driver, user_data):
        """
        Verify login validation messages using
        test data loaded from JSON.

        Args:
            user_data: Dictionary containing username,
                       password, and expected error message.

        Expected Result:
            Actual error message should match
            expected error message from test data.
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
