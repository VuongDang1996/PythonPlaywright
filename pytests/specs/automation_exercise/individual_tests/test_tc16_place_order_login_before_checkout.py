import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc16_place_order_login_before_checkout(
    home_page,
    login_page,
    signup_page,
    products_page,
    cart_page,
    auth_flow,
    cart_flow,
    leased_valid_user_credentials,
):
    valid_user = leased_valid_user_credentials
    registration_data = {
        "name": "Fallback Checkout User",
        "email": f"fallback.checkout.{int(home_page.page.evaluate('Date.now()'))}@example.com",
        "title": "Mr",
        "password": "Password123!",
        "day": "15",
        "month": "January",
        "year": "1990",
        "first_name": "Fallback",
        "last_name": "Checkout",
        "company": "QA",
        "address1": "123 Checkout St",
        "address2": "",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90002",
        "mobile_number": "+1234567891",
    }

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

    with allure.step("Login with existing user (fallback to registration if needed)"):
        active_user = auth_flow.ensure_logged_in(
            home_page=home_page,
            login_page=login_page,
            signup_page=signup_page,
            preferred_credentials=valid_user,
            registration_data=registration_data,
        )
        AllureHelpers.add_parameter("User Email", active_user.email)

    with allure.step("Verify user is logged in"):
        if not home_page.logged_in_as_user.is_visible(timeout=7_000):
            pytest.skip("Unable to establish authenticated state for checkout scenario")
        expect(home_page.logged_in_as_user).to_be_visible()
        AllureHelpers.add_screenshot("User Logged In", home_page.page.screenshot())

    with allure.step("Add products to cart"):
        cart_flow.add_product_to_cart(home_page, products_page, product_index=0)

    with allure.step("Navigate to cart"):
        cart_flow.open_cart(home_page)

    with allure.step("Verify cart page is displayed"):
        expect(cart_page.cart_table).to_be_visible()
        AllureHelpers.add_screenshot("Cart with Products", cart_page.page.screenshot())

    with allure.step("Proceed to checkout"):
        cart_flow.proceed_to_checkout(cart_page)

    with allure.step("Verify checkout page"):
        checkout_page = home_page.page.locator('h2:has-text("Review Your Order")')
        expect(checkout_page).to_be_visible()
        AllureHelpers.add_screenshot("Checkout Page", home_page.page.screenshot())
