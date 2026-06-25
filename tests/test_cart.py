import pytest


@pytest.mark.cart
class TestCartPage:
    @pytest.mark.regression
    def test_removing_item_from_cart(self, cart_with_items):
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_item_from_cart("Sauce Labs Backpack")

        assert cart_page.get_cart_item_count() == 2

    @pytest.mark.regression
    def test_remove_all_items_from_cart(self, cart_with_items):
        cart_page = cart_with_items
        assert cart_page.get_cart_item_count() == 3
        cart_page.remove_all_items()
        assert cart_page.get_cart_item_count() == 0
