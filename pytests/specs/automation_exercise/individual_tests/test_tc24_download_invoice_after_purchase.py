import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import (
    AUTOMATION_EXERCISE_TEST_DATA,
    build_sample_registration_data,
)


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc24_download_invoice_after_purchase_order(
    home_page, products_page, cart_page, login_page, signup_page
):
    user_data = build_sample_registration_data()
    user_data["email"] = f"test{int(home_page.page.evaluate('Date.now()'))}@example.com"

    allure.dynamic.epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    allure.dynamic.feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["checkout"])
    allure.dynamic.story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["order_placement"])

    home_page.navigate_to()
    expect(home_page.home_page_carousel).to_be_visible()
    home_page.click_products()
    products_page.hover_and_add_to_cart(0)
    products_page.click_continue_shopping()
    home_page.click_cart()
    expect(cart_page.cart_table).to_be_visible()
    cart_page.click_proceed_to_checkout()
    cart_page.click_register_login()

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
    home_page.click_cart()
    cart_page.click_proceed_to_checkout()
    checkout_page = home_page.page.locator('h2:has-text("Review Your Order")')
    expect(checkout_page).to_be_visible()

    home_page.click_delete_account()
    expect(signup_page.account_deleted_title).to_be_visible()
