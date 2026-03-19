import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc12_add_products_in_cart(home_page, products_page, cart_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["shopping_cart"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["cart_management"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC12")
    AllureHelpers.add_description("Verify user can add multiple products to cart")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("shopping-cart")
    AllureHelpers.add_tag("products")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to products page"):
        home_page.click_products()

    with allure.step("Add first product to cart"):
        products_page.hover_and_add_to_cart(0)
        AllureHelpers.add_parameter("First Product", "Product at index 0")

    with allure.step("Continue shopping after first product"):
        products_page.click_continue_shopping()

    with allure.step("Add second product to cart"):
        products_page.hover_and_add_to_cart(1)
        AllureHelpers.add_parameter("Second Product", "Product at index 1")

    with allure.step("View cart"):
        products_page.click_view_cart()

    with allure.step("Verify cart contents"):
        expect(cart_page.cart_table).to_be_visible()

    with allure.step("Verify product details in cart"):
        cart_items = cart_page.get_cart_items_count()
        assert cart_items == 2
        quantities = cart_page.get_product_quantities()
        assert len(quantities) == 2
        assert quantities[0] == 1
        assert quantities[1] == 1
        prices = cart_page.get_product_prices()
        assert len(prices) == 2
        totals = cart_page.get_product_totals()
        assert len(totals) == 2
        AllureHelpers.add_parameter("Cart Items Count", str(cart_items))
        AllureHelpers.add_screenshot("Cart Contents", cart_page.page.screenshot())
