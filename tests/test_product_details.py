import pytest

from pages.HeaderPage import HeaderPage
from pages.HomePage import HomePage
from pages.ProductDetailsPage import ProductDetailsPage

from utils.common_utils import CommonUtils
from utils.webdriver_utils import WebDriverUtils


class TestProductDetails:
    """
   Test suite for validating the Product Details page functionality.

   The tests verify:
   - Navigation from the inventory page to the product details page.
   - Correct display of product information.
   - Ability to add a product to the shopping cart.
   - Data-driven validation using JSON test data.
   """

    def test_product_details(self, logged_in_driver):
        """
        Verify that the Product Details page displays the expected information
        for a selected product and allows the product to be added to the cart.

        Test Steps:
        1. Navigate to the inventory page.
        2. Wait for the inventory list to load.
        3. Open the 'Sauce Labs Backpack' product.
        4. Verify the displayed product name.
        5. Add the product to the shopping cart.
        6. Verify that the 'Remove' button is displayed.

        Expected Result:
        - The Product Details page displays the correct product information.
        - The product is successfully added to the cart.
        - The 'Remove' button replaces the 'Add to Cart' button.
        """
        home_page = HomePage(logged_in_driver)
        home_page.is_inventory_page_loaded()
        WebDriverUtils.wait_until_elements_visible(logged_in_driver,
                                                   home_page.inventory_list_loaded())
        home_page.click_product_by_name("Sauce Labs Backpack")
        product_details_page = ProductDetailsPage(logged_in_driver)
        print(f"Product name is {product_details_page.get_product_name()}")
        print(
            f"Product description is {product_details_page.get_product_description()}")
        print(f"Product price is {product_details_page.get_product_price()}")
        assert product_details_page.get_product_name() == "Sauce Labs Backpack"
        product_details_page.add_product_to_cart()
        assert product_details_page.is_remove_button_displayed(
        ), "Remove button is not displayed"

    product_data = CommonUtils.open_file("testdata/products.json")

    @pytest.mark.parametrize("products", product_data)
    def test_product_details_from_json(self, logged_in_driver, products):
        """
        Verify that multiple products display the correct details using
        JSON-based test data.

        Test Steps:
        1. Navigate to the inventory page.
        2. Wait until the product list is loaded.
        3. Read product information from the JSON file.
        4. Open the corresponding product details page.
        5. Verify the displayed product name.
        6. Add the product to the shopping cart.
        7. Verify that the 'Remove' button is displayed.

        Test Data:
        - Product name
        - Product description
        - Product price

        Expected Result:
        - Each product details page displays the correct product information.
        - The selected product is successfully added to the cart.
        - The 'Remove' button is displayed after adding the product.
        """
        home_page = HomePage(logged_in_driver)
        home_page.is_inventory_page_loaded()
        WebDriverUtils.wait_until_elements_visible(logged_in_driver,
                                                   home_page.inventory_list_loaded())
        product_name = products["name"]
        home_page.click_product_by_name(product_name)
        product_details_page = ProductDetailsPage(logged_in_driver)

        product_description = products["description"]
        product_price = products["price"]
        print(f"Product name is {product_name}")
        print(
            f"Product description is {product_description}")
        print(f"Product price is {product_price}")
        assert product_details_page.get_product_name() == product_name
        product_details_page.add_product_to_cart()
        assert product_details_page.is_remove_button_displayed(
        ), "Remove button is not displayed"
