import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.smoke
@pytest.mark.user_registration
@pytest.mark.python_migration
def test_tc01_register_user(home_page, login_page, signup_page, registration_data):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["user_management"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["registration"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC01")
    AllureHelpers.add_description("Verify user can successfully register with valid details")
    AllureHelpers.add_tag("smoke")
    AllureHelpers.add_tag("user-registration")
    AllureHelpers.add_parameter("User Email", registration_data["email"])
    AllureHelpers.add_parameter("User Name", registration_data["name"])

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()
        expect(home_page.features_items).to_be_visible()

    with allure.step("Navigate to signup page"):
        home_page.click_signup_login()

    with allure.step("Verify signup form is visible"):
        expect(login_page.new_user_signup_title).to_be_visible()

    with allure.step("Enter signup details"):
        login_page.signup_user(registration_data["name"], registration_data["email"])

    with allure.step("Verify account information form"):
        expect(signup_page.account_info_title).to_be_visible()

    with allure.step("Fill account information"):
        signup_page.fill_account_information(
            {
                "title": registration_data["title"],
                "password": registration_data["password"],
                "day": registration_data["day"],
                "month": registration_data["month"],
                "year": registration_data["year"],
                "newsletter": True,
                "offers": True,
            }
        )

    with allure.step("Fill address information"):
        signup_page.fill_address_information(registration_data)

    with allure.step("Create account"):
        signup_page.click_create_account()

    with allure.step("Verify account creation"):
        expect(signup_page.account_created_title).to_be_visible()

    with allure.step("Continue after account creation"):
        signup_page.click_continue()

    with allure.step("Verify user is logged in"):
        expect(home_page.logged_in_as_user).to_be_visible()
        expect(home_page.logged_in_as_user).to_contain_text(registration_data["name"])

    with allure.step("Delete account"):
        home_page.click_delete_account()

    with allure.step("Verify account deletion"):
        expect(signup_page.account_deleted_title).to_be_visible()
        signup_page.click_continue()
