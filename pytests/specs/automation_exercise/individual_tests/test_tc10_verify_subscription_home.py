import time

import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc10_verify_subscription_in_home_page(home_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["newsletter"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["subscription"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC10")
    AllureHelpers.add_description("Verify user can subscribe to newsletter from home page")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("subscription")
    AllureHelpers.add_tag("newsletter")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Scroll to footer section"):
        home_page.scroll_to_bottom()

    with allure.step("Verify subscription section is visible"):
        expect(home_page.subscription_title).to_be_visible()
        AllureHelpers.add_screenshot("Subscription Section", home_page.page.screenshot())

    with allure.step("Subscribe to newsletter"):
        test_email = f"test{int(time.time() * 1000)}@example.com"
        home_page.subscribe_to_newsletter(test_email)
        AllureHelpers.add_parameter("Test Email", test_email)

    with allure.step("Verify subscription success"):
        expect(home_page.subscription_success_message).to_be_visible()
        expect(home_page.subscription_success_message).to_contain_text(
            "You have been successfully subscribed!"
        )
        AllureHelpers.add_screenshot("Subscription Success", home_page.page.screenshot())
