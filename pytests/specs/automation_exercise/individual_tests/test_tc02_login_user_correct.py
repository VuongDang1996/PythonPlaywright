import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, TEST_USERS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.smoke
@pytest.mark.authentication
@pytest.mark.python_migration
def test_tc02_login_user_with_correct_email_and_password(home_page, login_page):
    valid_user = TEST_USERS["valid_user"]

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["authentication"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["login"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC02")
    AllureHelpers.add_description("Verify user can login with correct email and password")
    AllureHelpers.add_tag("smoke")
    AllureHelpers.add_tag("authentication")
    AllureHelpers.add_parameter("User Email", valid_user["email"])

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to login page"):
        home_page.click_signup_login()

    with allure.step("Verify login form is visible"):
        expect(login_page.login_to_account_title).to_be_visible()

    with allure.step("Enter login credentials"):
        login_page.login_user(valid_user["email"], valid_user["password"])

    with allure.step("Verify user is logged in"):
        expect(home_page.logged_in_as_user).to_be_visible()

    with allure.step("Logout user"):
        home_page.click_logout()

    with allure.step("Verify logout successful"):
        expect(login_page.login_to_account_title).to_be_visible()
