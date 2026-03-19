import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, CATEGORIES
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc18_view_category_products(home_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["product_catalog"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["product_browsing"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC18")
    AllureHelpers.add_description("Verify user can browse products by categories")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("categories")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify categories sidebar is visible"):
        expect(home_page.categories_sidebar).to_be_visible()

    with allure.step("Navigate to Women category"):
        home_page.click_women_category()

    with allure.step("Navigate to Women Dress subcategory"):
        home_page.click_women_subcategory(CATEGORIES["women"]["dress"])

    with allure.step("Verify women dress category page"):
        category_title = home_page.page.locator('h2:has-text("Women -"), h2:has-text("Dress")')
        expect(category_title).to_be_visible()

    with allure.step("Navigate to Men category"):
        home_page.click_men_category()
        home_page.click_men_subcategory(CATEGORIES["men"]["tshirts"])

    with allure.step("Verify men t-shirts category page"):
        men_title = home_page.page.locator('h2:has-text("Men -"), h2:has-text("Tshirts")')
        expect(men_title).to_be_visible()
