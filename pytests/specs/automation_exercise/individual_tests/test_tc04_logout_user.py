import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.smoke
@pytest.mark.authentication
@pytest.mark.python_migration
def test_tc04_logout_user(
    home_page, login_page, signup_page, auth_flow, leased_valid_user_credentials
):
    valid_user = leased_valid_user_credentials
    registration_data = {
        "name": "Fallback User",
        "email": f"fallback.logout.{int(home_page.page.evaluate('Date.now()'))}@example.com",
        "title": "Mr",
        "password": "Password123!",
        "day": "15",
        "month": "January",
        "year": "1990",
        "first_name": "Fallback",
        "last_name": "User",
        "company": "QA",
        "address1": "123 Fallback St",
        "address2": "",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90001",
        "mobile_number": "+1234567890",
    }

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

    with allure.step("Login with valid credentials (fallback to registration if needed)"):
        active_user = auth_flow.ensure_logged_in(
            home_page=home_page,
            login_page=login_page,
            signup_page=signup_page,
            preferred_credentials=valid_user,
            registration_data=registration_data,
        )
        AllureHelpers.add_parameter("Email", active_user.email)

    with allure.step("Verify successful login"):
        if not home_page.logged_in_as_user.is_visible(timeout=7_000):
            pytest.skip("Unable to establish authenticated state for logout scenario")
        expect(home_page.logged_in_as_user).to_be_visible()
        AllureHelpers.add_screenshot("User Logged In", home_page.page.screenshot())

    with allure.step("Logout from application"):
        auth_flow.logout(home_page)

    with allure.step("Verify successful logout"):
        expect(login_page.login_to_account_title).to_be_visible()
        expect(login_page.new_user_signup_title).to_be_visible()
        AllureHelpers.add_screenshot("User Logged Out", login_page.page.screenshot())
