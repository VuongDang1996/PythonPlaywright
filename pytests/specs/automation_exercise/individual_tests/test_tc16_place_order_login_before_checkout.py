import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, TEST_USERS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc16_place_order_login_before_checkout(home_page, login_page, products_page, cart_page):
    valid_user = TEST_USERS["valid_user"]

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["checkout"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["order_placement"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC16")
    AllureHelpers.add_description("Verify user can place order by logging in before checkout process")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("checkout")
    AllureHelpers.add_tag("login")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to login page"):
        home_page.click_signup_login()

    with allure.step("Login with existing user"):
        login_page.login_user(valid_user["email"], valid_user["password"])
        AllureHelpers.add_parameter("User Email", valid_user["email"])

    with allure.step("Verify user is logged in"):
        expect(home_page.logged_in_as_user).to_be_visible()
        AllureHelpers.add_screenshot("User Logged In", home_page.page.screenshot())

    with allure.step("Add products to cart"):
        home_page.click_products()
        products_page.hover_and_add_to_cart(0)
        products_page.click_continue_shopping()

    with allure.step("Navigate to cart"):
        home_page.click_cart()

    with allure.step("Verify cart page is displayed"):
        expect(cart_page.cart_table).to_be_visible()
        AllureHelpers.add_screenshot("Cart with Products", cart_page.page.screenshot())

    with allure.step("Proceed to checkout"):
        cart_page.click_proceed_to_checkout()

    with allure.step("Verify checkout page"):
        checkout_page = home_page.page.locator('h2:has-text("Review Your Order")')
        expect(checkout_page).to_be_visible()
        AllureHelpers.add_screenshot("Checkout Page", home_page.page.screenshot())
