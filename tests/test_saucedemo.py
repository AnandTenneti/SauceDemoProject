# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from pages.LoginPage import LoginPage
# from pages.HeaderPage import HeaderPage
# from pages.HomePage import HomePage
# from pages.ProductDetailsPage import ProductDetailsPage
# import json

# import pytest


# class TestSeleniumAgent:

#     # @pytest.mark.smoke
#     @pytest.mark.skip(reason="Skipping this test for now")
#     def test_launch_application(self, driver):

#         driver.get("https://www.saucedemo.com/")

#         time.sleep(2)

#         assert "Swag Labs" in driver.title
#     with open("testdata/testdata.json") as f:
#         test_data = json.load(f)

#     @pytest.mark.parametrize("data", test_data)
#     def test_login_data_driven_json(self, driver, data):
#         username = data["username"]
#         password = data["password"]

#         driver.get("https://www.saucedemo.com/")

#         time.sleep(2)
#         login_page = LoginPage(driver)

#         login_page.user_login(username, password)
#         time.sleep(2)
#         print(f"Logging in as {data["username"]}")
#         assert "Swag Labs" in driver.title
#         time.sleep(5)
#         header_page = HeaderPage(driver)
#         header_page.logout()

#     @pytest.mark.skip(reason="Skipping for now")
#     @pytest.mark.parametrize("username,password", [
#         ("standard_user", "secret_sauce"),
#         ("visual_user", "secret_sauce"),
#         ("problem_user", "secret_sauce")
#     ])
#     def test_login_data_driven(self, driver, username, password):

#         driver.get("https://www.saucedemo.com/")

#         time.sleep(2)
#         login_page = LoginPage(driver)

#         login_page.user_login(username, password)
#         time.sleep(2)

#         assert "Swag Labs" in driver.title
#         time.sleep(5)
#         header_page = HeaderPage(driver)
#         header_page.logout()

#         # menu_button = driver.find_element(By.ID, "react-burger-menu-btn")

#         # menu_button.click()
#         # time.sleep(5)
#         # logout_button = driver.find_element(
#         #     By.CSS_SELECTOR, "#logout_sidebar_link")
#         # logout_button.click()
#         # WebDriverWait(driver, 10).until(
#         #     EC.title_contains("Swag Labs"))
#         # assert "Swag Labs" in driver.title

#     @pytest.mark.skip(reason="skipping it for now")
#     def test_login(self, driver):

#         driver.get("https://www.saucedemo.com/")

#         time.sleep(2)
#         login_page = LoginPage(driver)

#         login_page.user_login("standard_user", "secret_sauce")
#         time.sleep(2)

#         assert "Swag Labs" in driver.title
#         time.sleep(5)

#         menu_button = driver.find_element(By.ID, "react-burger-menu-btn")

#         menu_button.click()
#         time.sleep(5)
#         logout_button = driver.find_element(
#             By.CSS_SELECTOR, "#logout_sidebar_link")
#         logout_button.click()
#         WebDriverWait(driver, 10).until(
#             EC.title_contains("Swag Labs"))
#         assert "Swag Labs" in driver.title

#     @pytest.mark.skip(reason="Skipping it for now")
#     def test_sort_poduct(self, logged_in_driver):
#         home_page = HomePage(logged_in_driver)
#         time.sleep(10)
#         home_page.select_sort_order(HomePage.SortOptions.PRICE_LOW_TO_HIGH)
#         time.sleep(10)
#         assert home_page.is_sorted_low_to_high()
#         time.sleep(10)
#         # header_page = HeaderPage(logged_in_driver)
#         # header_page.logout()

#     @pytest.mark.skip(reason="Skipping it for now")
#     def test_product_search(self, logged_in_driver):
#         home_page = HomePage(logged_in_driver)
#         time.sleep(10)
#         product_name = "Sauce Labs Backpack"
#         home_page.click_product_by_name(product_name)
#         product_page = ProductDetailsPage(logged_in_driver)
#         displayed_product_name = product_page.get_product_name()
#         assert displayed_product_name == product_name
#         product_page.add_product_to_cart()
#         assert product_page.is_remove_button_displayed()
#         time.sleep(10)

#     @pytest.mark.skip(reason="Skipping it for now")
#     def test_add_multiple_products_to_cart(self, logged_in_driver):
#         home_page = HomePage(logged_in_driver)
#         header_page = HeaderPage(logged_in_driver)
#         assert header_page.get_cart_badge_count() == 0
#         time.sleep(10)

#         product_list = ["Sauce Labs Backpack",
#                         "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
#         for product in product_list:
#             home_page.click_add_to_cart(product)
#             time.sleep(10)

#         assert header_page.get_cart_badge_count() == 3
#         time.sleep(10)
