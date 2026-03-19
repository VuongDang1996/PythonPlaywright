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
def test_tc23_verify_address_details_in_checkout_page(
    home_page, login_page, signup_page, products_page, cart_page
):
    user_data = build_sample_registration_data()
    user_data["email"] = f"test{int(home_page.page.evaluate('Date.now()'))}@example.com"

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["checkout"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["order_placement"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC23")

    home_page.navigate_to()
    expect(home_page.home_page_carousel).to_be_visible()
    home_page.click_signup_login()

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
    signup_page.click_create_account()
    expect(signup_page.account_created_title).to_be_visible()
    signup_page.click_continue()

    expect(home_page.logged_in_as_user).to_be_visible()
    home_page.click_products()
    products_page.hover_and_add_to_cart(0)
    products_page.click_continue_shopping()
    home_page.click_cart()
    expect(cart_page.cart_table).to_be_visible()
    cart_page.click_proceed_to_checkout()

    delivery_address = home_page.page.locator("#address_delivery")
    expect(delivery_address).to_contain_text(user_data["first_name"])
    expect(delivery_address).to_contain_text(user_data["last_name"])
    expect(delivery_address).to_contain_text(user_data["address1"])
    expect(delivery_address).to_contain_text(user_data["city"])

    billing_address = home_page.page.locator("#address_invoice")
    expect(billing_address).to_contain_text(user_data["first_name"])
    expect(billing_address).to_contain_text(user_data["last_name"])
    expect(billing_address).to_contain_text(user_data["address1"])
    expect(billing_address).to_contain_text(user_data["city"])

    home_page.click_delete_account()
    expect(signup_page.account_deleted_title).to_be_visible()
