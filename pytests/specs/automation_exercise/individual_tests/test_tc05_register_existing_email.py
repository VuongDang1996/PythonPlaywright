import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, TEST_USERS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.authentication
@pytest.mark.python_migration
def test_tc05_register_user_with_existing_email(home_page, login_page):
    existing_user = TEST_USERS["existing_user"]

    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["authentication"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["registration"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC05")
    AllureHelpers.add_description(
        "Verify error message is displayed when user tries to register with existing email"
    )
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("authentication")
    AllureHelpers.add_tag("negative-test")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to signup page"):
        home_page.click_signup_login()

    with allure.step("Verify signup section is visible"):
        expect(login_page.new_user_signup_title).to_be_visible()

    with allure.step("Enter existing email for signup"):
        login_page.signup_user("Test User", existing_user["email"])
        AllureHelpers.add_parameter("Test Name", "Test User")
        AllureHelpers.add_parameter("Existing Email", existing_user["email"])

    with allure.step("Verify error message for existing email"):
        expect(login_page.signup_error_message).to_be_visible()
        expect(login_page.signup_error_message).to_contain_text("Email Address already exist!")
        AllureHelpers.add_screenshot("Existing Email Error", login_page.page.screenshot())
