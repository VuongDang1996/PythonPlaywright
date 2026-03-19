import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA, BRANDS
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc19_view_and_cart_brand_products(home_page, products_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["product_catalog"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["product_browsing"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC19")
    AllureHelpers.add_description("Verify user can browse products by brands")
    AllureHelpers.add_tag("regression")
    AllureHelpers.add_tag("brands")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Navigate to products page"):
        home_page.click_products()

    with allure.step("Verify brands sidebar is visible"):
        expect(home_page.brands_sidebar).to_be_visible()

    with allure.step("Navigate to first brand"):
        home_page.click_brand(BRANDS["polo"])

    with allure.step("Verify first brand page"):
        brand_title = home_page.page.locator(f'h2:has-text("{BRANDS["polo"]}")')
        expect(brand_title).to_be_visible()
        expect(products_page.products_list).to_be_visible()

    with allure.step("Navigate to second brand"):
        home_page.click_brand(BRANDS["h_and_m"])

    with allure.step("Verify second brand page"):
        second_title = home_page.page.locator(f'h2:has-text("{BRANDS["h_and_m"]}")')
        expect(second_title).to_be_visible()
        expect(products_page.products_list).to_be_visible()
