import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc13_verify_product_quantity_in_cart(home_page, product_detail_page, cart_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["shopping_cart"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["cart_management"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC13")
    AllureHelpers.add_description(
        "Verify product quantity is correctly displayed in cart when custom quantity is set"
    )
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("shopping-cart")
    AllureHelpers.add_tag("quantity")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to product detail page"):
        first_product = home_page.page.locator('a:has-text("View Product")').first
        first_product.click()

    with allure.step("Verify product detail page is loaded"):
        expect(product_detail_page.product_name).to_be_visible()

    with allure.step("Set product quantity to 4"):
        product_detail_page.set_quantity(4)
        AllureHelpers.add_parameter("Product Quantity", "4")

    with allure.step("Add product to cart"):
        product_detail_page.add_to_cart()

    with allure.step("Navigate to cart page"):
        view_cart_button = home_page.page.locator('a:has-text("View Cart")').first
        view_cart_button.click()

    with allure.step("Verify product quantity in cart"):
        expect(cart_page.cart_table).to_be_visible()
        quantities = cart_page.get_product_quantities()
        assert quantities[0] == 4
        items_count = cart_page.get_cart_items_count()
        assert items_count == 1
        AllureHelpers.add_parameter("Expected Quantity", "4")
        AllureHelpers.add_parameter("Actual Quantity", str(quantities[0]))
        AllureHelpers.add_parameter("Cart Items Count", str(items_count))
        AllureHelpers.add_screenshot("Cart with Custom Quantity", cart_page.page.screenshot())
