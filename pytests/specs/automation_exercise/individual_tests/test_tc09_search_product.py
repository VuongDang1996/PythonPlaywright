import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, SEARCH_TERMS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.products
@pytest.mark.python_migration
def test_tc09_search_product(home_page, products_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["product_catalog"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["product_search"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC09")
    AllureHelpers.add_description("Verify user can search for products and see relevant results")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("search")
    AllureHelpers.add_tag("products")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to products page"):
        home_page.click_products()

    with allure.step("Verify all products page is displayed"):
        expect(products_page.all_products_title).to_be_visible()

    with allure.step("Search for products"):
        products_page.search_products(SEARCH_TERMS["shirt"])
        AllureHelpers.add_parameter("Search Term", SEARCH_TERMS["shirt"])

    with allure.step("Verify search results title is displayed"):
        expect(products_page.searched_products_title).to_be_visible()

    with allure.step("Verify search results are displayed"):
        expect(products_page.search_results.first).to_be_visible()
        search_results_count = products_page.get_search_results_count()
        assert search_results_count > 0
        AllureHelpers.add_parameter("Search Results Count", str(search_results_count))
        AllureHelpers.add_screenshot("Search Results", products_page.page.screenshot())
