import re

import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.smoke
@pytest.mark.python_migration
def test_tc07_verify_test_cases_page(home_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["navigation"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["page_navigation"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC07")
    AllureHelpers.add_description("Verify user can navigate to test cases page successfully")
    AllureHelpers.add_tag("smoke")
    AllureHelpers.add_tag("navigation")
    AllureHelpers.add_tag("test-cases")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to test cases page"):
        home_page.click_test_cases()

    with allure.step("Verify test cases page is displayed"):
        expect(home_page.page).to_have_url(re.compile(r".*test_cases"))
        test_cases_title = home_page.page.locator('h2:has-text("Test Cases")')
        expect(test_cases_title).to_be_visible()
        AllureHelpers.add_screenshot("Test Cases Page", home_page.page.screenshot())
        AllureHelpers.add_parameter("Test Cases Page URL", home_page.page.url)
