import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import (
    AUTOMATION_EXERCISE_TEST_DATA,
    SAMPLE_REVIEW_DATA,
)
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc21_add_review_on_product(home_page, products_page, product_detail_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["product_catalog"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["reviews"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC21")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Navigate to products page"):
        home_page.click_products()
        expect(products_page.all_products_title).to_be_visible()

    with allure.step("Open first product"):
        products_page.click_view_product(0)
        expect(product_detail_page.product_name).to_be_visible()

    with allure.step("Write product review"):
        product_detail_page.write_review(SAMPLE_REVIEW_DATA)

    with allure.step("Verify review success"):
        expect(product_detail_page.review_success_message).to_be_visible()
        expect(product_detail_page.review_success_message).to_contain_text(
            "Thank you for your review."
        )
