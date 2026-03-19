import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.smoke
@pytest.mark.products
@pytest.mark.python_migration
def test_tc08_verify_all_products_and_product_detail_page(
    home_page, products_page, product_detail_page
):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["product_catalog"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["product_browsing"])
    AllureHelpers.add_severity("critical")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC08")
    AllureHelpers.add_description(
        "Verify all products page and product detail page display correct information"
    )
    AllureHelpers.add_tag("smoke")
    AllureHelpers.add_tag("products")
    AllureHelpers.add_tag("product-details")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Verify home page is visible"):
        expect(home_page.home_page_carousel).to_be_visible()

    with allure.step("Navigate to products page"):
        home_page.click_products()

    with allure.step("Verify all products page is displayed"):
        expect(products_page.all_products_title).to_be_visible()

    with allure.step("Verify products list is visible"):
        expect(products_page.products_list).to_be_visible()
        AllureHelpers.add_screenshot("All Products Page", products_page.page.screenshot())

    with allure.step("Navigate to first product detail"):
        products_page.click_view_product(0)
        AllureHelpers.add_parameter("Product Index", "0 (first product)")

    with allure.step("Verify product detail page is loaded"):
        expect(product_detail_page.product_name).to_be_visible()

    with allure.step("Verify all product details are visible"):
        expect(product_detail_page.product_name).to_be_visible()
        expect(product_detail_page.product_category).to_be_visible()
        expect(product_detail_page.product_price).to_be_visible()
        expect(product_detail_page.product_availability).to_be_visible()
        expect(product_detail_page.product_condition).to_be_visible()
        expect(product_detail_page.product_brand).to_be_visible()

        product_name = product_detail_page.product_name.text_content() or "N/A"
        product_price = product_detail_page.product_price.text_content() or "N/A"
        product_category = product_detail_page.product_category.text_content() or "N/A"

        AllureHelpers.add_parameter("Product Name", product_name)
        AllureHelpers.add_parameter("Product Price", product_price)
        AllureHelpers.add_parameter("Product Category", product_category)
        AllureHelpers.add_screenshot("Product Detail Page", product_detail_page.page.screenshot())
