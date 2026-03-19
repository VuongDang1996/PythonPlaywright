import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc25_verify_scroll_up_using_arrow_button(home_page):
    allure.dynamic.epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    allure.dynamic.feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["navigation"])
    allure.dynamic.story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["page_navigation"])

    home_page.navigate_to()
    expect(home_page.home_page_carousel).to_be_visible()
    home_page.scroll_to_bottom()
    expect(home_page.subscription_title).to_be_visible()
    home_page.click_scroll_up_button()
    expect(home_page.full_fledged_text).to_be_visible()
    AllureHelpers.add_screenshot("Page Scrolled to Top", home_page.page.screenshot())
