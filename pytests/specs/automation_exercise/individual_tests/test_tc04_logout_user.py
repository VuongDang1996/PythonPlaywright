import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, TEST_USERS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.smoke
@pytest.mark.authentication
@pytest.mark.python_migration
def test_tc04_logout_user(home_page, login_page):
    valid_user = TEST_USERS["valid_user"]

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["authentication"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["logout"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC04")
    AllureHelpers.add_description("Verify user can successfully logout from the application")
    AllureHelpers.add_tag("smoke")
    AllureHelpers.add_tag("authentication")
    AllureHelpers.add_tag("logout")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to login page"):
        home_page.click_signup_login()

    with allure.step("Verify login section is visible"):
        expect(login_page.login_to_account_title).to_be_visible()

    with allure.step("Login with valid credentials"):
        login_page.login_user(valid_user["email"], valid_user["password"])
        AllureHelpers.add_parameter("Email", valid_user["email"])

    with allure.step("Verify successful login"):
        expect(home_page.logged_in_as_user).to_be_visible()
        AllureHelpers.add_screenshot("User Logged In", home_page.page.screenshot())

    with allure.step("Logout from application"):
        home_page.click_logout()

    with allure.step("Verify successful logout"):
        expect(login_page.login_to_account_title).to_be_visible()
        expect(login_page.new_user_signup_title).to_be_visible()
        AllureHelpers.add_screenshot("User Logged Out", login_page.page.screenshot())
