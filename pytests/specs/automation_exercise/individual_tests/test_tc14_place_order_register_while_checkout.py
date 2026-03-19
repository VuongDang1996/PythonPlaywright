import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import (
    AUTOMATION_EXERCISE_TEST_DATA,
    build_sample_registration_data,
)
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc14_place_order_register_while_checkout(
    home_page, products_page, cart_page, login_page, signup_page
):
    user_data = build_sample_registration_data()
    user_data["email"] = f"test{int(home_page.page.evaluate('Date.now()'))}@example.com"

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["checkout"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["order_placement"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC14")
    AllureHelpers.add_description(
        "Verify user can place order by registering during checkout process"
    )
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("ecommerce")
    AllureHelpers.add_tag("checkout")
    AllureHelpers.add_tag("registration")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

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

    with allure.step("Navigate to registration"):
        cart_page.click_register_login()

    with allure.step("Complete user registration"):
        login_page.signup_user(user_data["name"], user_data["email"])
        expect(signup_page.account_info_title).to_be_visible()

        signup_page.fill_account_information(
            {
                "title": user_data["title"],
                "password": user_data["password"],
                "day": user_data["day"],
                "month": user_data["month"],
                "year": user_data["year"],
                "newsletter": True,
                "offers": True,
            }
        )
        signup_page.fill_address_information(user_data)

    with allure.step("Create account"):
        signup_page.click_create_account()

    with allure.step("Verify account creation"):
        expect(signup_page.account_created_title).to_be_visible()
        signup_page.click_continue()

    with allure.step("Verify user is logged in"):
        expect(home_page.logged_in_as_user).to_be_visible()

    with allure.step("Return to cart"):
        home_page.click_cart()

    with allure.step("Proceed to checkout as logged in user"):
        cart_page.click_proceed_to_checkout()

    with allure.step("Verify checkout page"):
        checkout_page = home_page.page.locator('h2:has-text("Review Your Order")')
        expect(checkout_page).to_be_visible()
        AllureHelpers.add_screenshot("Checkout Page", home_page.page.screenshot())

    with allure.step("Delete test account"):
        home_page.click_delete_account()

    with allure.step("Verify account deletion"):
        expect(signup_page.account_deleted_title).to_be_visible()
        AllureHelpers.add_screenshot("Account Deleted", signup_page.page.screenshot())
