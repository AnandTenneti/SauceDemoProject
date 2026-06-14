import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.LoginPage import LoginPage
from pages.HeaderPage import HeaderPage
import allure
from utils.common_utils import CommonUtils
import json


class TestLogin:
    @allure.title("Verify successful login")
    @allure.description(
        "Verify that a valid user can login successfully"
    )
    def test_valid_user_login(self, driver):
        driver.get("https://www.saucedemo.com/")

        time.sleep(2)
        login_page = LoginPage(driver)

        login_page.user_login("standard_user", "secret_sauce")
        time.sleep(2)

        assert "Swag Labs" in driver.title
        time.sleep(5)
        header_page = HeaderPage(driver)
        header_page.logout()
        WebDriverWait(driver, 10).until(
            EC.title_contains("Swag Labs"))
        assert "Swag Labs" in driver.title

    @pytest.mark.parametrize("username,password", [
        ("standard_user", "secret_sauce"),
        ("visual_user", "secret_sauce")
    ])
    def test_login_with_valid_credentials(self, driver, username, password):

        driver.get("https://www.saucedemo.com/")

        time.sleep(2)
        login_page = LoginPage(driver)

        login_page.user_login(username, password)
        time.sleep(2)

        assert "Swag Labs" in driver.title
        time.sleep(5)
        header_page = HeaderPage(driver)
        header_page.logout()
        WebDriverWait(driver, 10).until(
            EC.title_contains("Swag Labs"))
        assert "Swag Labs" in driver.title

    valid_users = CommonUtils.open_file("testdata/users.json")

    @pytest.mark.parametrize("data", valid_users)
    def test_login_with_valid_user_types_from_json(self, driver, data):

        driver.get("https://www.saucedemo.com/")

        time.sleep(2)
        login_page = LoginPage(driver)
        username = data["username"]
        password = data["password"]

        login_page.user_login(username, password)
        time.sleep(2)

        assert "Swag Labs" in driver.title
        time.sleep(5)

        header_page = HeaderPage(driver)
        header_page.logout()
        WebDriverWait(driver, 10).until(
            EC.title_contains("Swag Labs"))
        assert "Swag Labs" in driver.title

    def test_login_with_invalid_username(self, driver):
        error_message = "Epic sadface: Username and password do not match any user in this service"

        driver.get("https://www.saucedemo.com/")

        time.sleep(2)
        login_page = LoginPage(driver)

        login_page.user_login("standard_user1", "secret_sauce")
        time.sleep(2)
        assert login_page.get_error_message() == error_message
        time.sleep(10)

   # Data Driven tests

    @pytest.mark.parametrize("username,password,error_message", [
        ("standard_user1", "secret_sauce",
         "Epic sadface: Username and password do not match any user in this service"),
        ("standard_user", "", "Epic sadface: Password is required"),
        ("", "test", "Epic sadface: Username is required")
    ])
    def test_login_validation_for_invalid_credentials(self, driver, username, password, error_message):
        driver.get("https://www.saucedemo.com/")

        time.sleep(2)
        login_page = LoginPage(driver)
        login_page.user_login(username, password)

        assert login_page.get_error_message(
        ) == error_message
        time.sleep(10)

        invalid_users = CommonUtils.open_file("testdata/error_messages.json")

    @pytest.mark.parametrize("user_data", invalid_users)
    def test_login_validation_from_error_data_json(self, driver, user_data):
        driver.get("https://www.saucedemo.com/")

        time.sleep(2)
        login_page = LoginPage(driver)
        username = user_data["username"]
        password = user_data["password"]
        error_message = user_data["error_message"]
        login_page.user_login(username, password)

        assert login_page.get_error_message(
        ) == error_message
        time.sleep(10)
