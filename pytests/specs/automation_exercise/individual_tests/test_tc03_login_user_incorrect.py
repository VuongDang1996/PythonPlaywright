import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, TEST_USERS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.authentication
@pytest.mark.python_migration
def test_tc03_login_user_with_incorrect_email_and_password(home_page, login_page):
    invalid_user = TEST_USERS["invalid_user"]

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["authentication"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["login"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC03")
    AllureHelpers.add_description(
        "Verify error message is displayed when user tries to login with incorrect credentials"
    )
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("authentication")
    AllureHelpers.add_tag("negative-test")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to login page"):
        home_page.click_signup_login()

    with allure.step("Verify login section is visible"):
        expect(login_page.login_to_account_title).to_be_visible()

    with allure.step("Enter incorrect login credentials"):
        login_page.login_user(invalid_user["email"], invalid_user["password"])
        AllureHelpers.add_parameter("Invalid Email", invalid_user["email"])
        AllureHelpers.add_parameter("Invalid Password", "[MASKED]")

    with allure.step("Verify error message is displayed"):
        expect(login_page.login_error_message).to_be_visible()
        expect(login_page.login_error_message).to_contain_text(
            "Your email or password is incorrect!"
        )
        AllureHelpers.add_screenshot("Login Error Message", login_page.page.screenshot())
