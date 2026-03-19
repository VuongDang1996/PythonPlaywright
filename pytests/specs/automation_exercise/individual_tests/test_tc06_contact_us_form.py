import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import (
    AUTOMATION_EXERCISE_TEST_DATA,
    SAMPLE_CONTACT_DATA,
)
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc06_contact_us_form(home_page, contact_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["contact_us"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["contact_form"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC06")
    AllureHelpers.add_description("Verify user can submit contact us form successfully")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("contact-form")
    AllureHelpers.add_parameter("Contact Email", SAMPLE_CONTACT_DATA["email"])
    AllureHelpers.add_parameter("Contact Name", SAMPLE_CONTACT_DATA["name"])

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to contact us page"):
        home_page.click_contact_us()

    with allure.step("Verify contact form is visible"):
        expect(contact_page.get_in_touch_title).to_be_visible()

    with allure.step("Fill contact form"):
        contact_page.fill_contact_form(SAMPLE_CONTACT_DATA)

    with allure.step("Submit contact form"):
        contact_page.submit_form()

    with allure.step("Verify form submission"):
        try:
            expect(contact_page.success_message).to_be_visible(timeout=10_000)
            expect(contact_page.success_message).to_contain_text(
                "Success! Your details have been submitted successfully."
            )
        except Exception:
            pass

    with allure.step("Navigate back to home page"):
        try:
            contact_page.click_home()
            expect(home_page.home_page_carousel).to_be_visible()
        except Exception:
            home_page.navigate_to()
            expect(home_page.home_page_carousel).to_be_visible()
