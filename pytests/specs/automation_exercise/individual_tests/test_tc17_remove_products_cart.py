import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc17_remove_products_from_cart(home_page, products_page, cart_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["shopping_cart"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["cart_management"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC17")
    AllureHelpers.add_description("Verify user can remove products from shopping cart")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("shopping-cart")
    AllureHelpers.add_tag("product-removal")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Add multiple products to cart"):
        home_page.click_products()
        products_page.hover_and_add_to_cart(0)
        products_page.click_continue_shopping()
        products_page.hover_and_add_to_cart(1)

    with allure.step("Navigate to cart"):
        products_page.click_view_cart()

    with allure.step("Verify cart page and initial product count"):
        expect(cart_page.cart_table).to_be_visible()
        initial_items_count = cart_page.get_cart_items_count()
        assert initial_items_count > 0
        AllureHelpers.add_parameter("Initial Items Count", str(initial_items_count))

    with allure.step("Remove product from cart"):
        cart_page.remove_product(0)

    with allure.step("Verify product removal"):
        final_items_count = cart_page.get_cart_items_count()
        assert final_items_count == initial_items_count - 1
        AllureHelpers.add_parameter("Final Items Count", str(final_items_count))
        AllureHelpers.add_screenshot("Cart After Product Removal", cart_page.page.screenshot())
