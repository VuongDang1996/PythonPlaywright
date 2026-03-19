import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import (
    AUTOMATION_EXERCISE_TEST_DATA,
    SEARCH_TERMS,
    TEST_USERS,
)
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc20_search_products_and_verify_cart_after_login(
    home_page, products_page, cart_page, login_page
):
    valid_user = TEST_USERS["valid_user"]

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["shopping_cart"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["cart_management"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC20")
    AllureHelpers.add_description(
        "Verify cart items persist after login when products are added before login"
    )

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Navigate to products page"):
        home_page.click_products()

    with allure.step("Verify products page is loaded"):
        expect(products_page.all_products_title).to_be_visible()

    with allure.step("Search for products"):
        products_page.search_products(SEARCH_TERMS["shirt"])

    with allure.step("Verify search results are displayed"):
        expect(products_page.searched_products_title).to_be_visible()
        expect(products_page.search_results.first).to_be_visible()

    with allure.step("Add search results to cart"):
        products_page.add_search_results_to_cart(3)

    with allure.step("Verify cart contains products before login"):
        home_page.click_cart()
        expect(cart_page.cart_table).to_be_visible()
        items_before_login = cart_page.get_cart_items_count()
        assert items_before_login > 0

    with allure.step("Login with existing user"):
        home_page.click_signup_login()
        login_page.login_user(valid_user["email"], valid_user["password"])

    with allure.step("Verify cart items persist after login"):
        home_page.click_cart()
        expect(cart_page.cart_table).to_be_visible()
        items_after_login = cart_page.get_cart_items_count()
        assert items_after_login >= items_before_login
