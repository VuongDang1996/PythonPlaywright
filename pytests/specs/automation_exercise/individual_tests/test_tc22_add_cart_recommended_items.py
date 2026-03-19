import allure
import pytest
from playwright.sync_api import expect

from pytests.data.automation_exercise_data import AUTOMATION_EXERCISE_TEST_DATA
from pytests.utils.allure_helpers import AllureHelpers


@pytest.mark.regression
@pytest.mark.python_migration
def test_tc22_add_to_cart_from_recommended_items(home_page, cart_page):
    AllureHelpers.add_epic(AUTOMATION_EXERCISE_TEST_DATA["epic"])
    AllureHelpers.add_feature(AUTOMATION_EXERCISE_TEST_DATA["features"]["shopping_cart"])
    AllureHelpers.add_story(AUTOMATION_EXERCISE_TEST_DATA["stories"]["cart_management"])
    AllureHelpers.add_severity("normal")
    AllureHelpers.add_owner("QA Team")
    AllureHelpers.add_test_id("TC22")

    with allure.step("Navigate to home page"):
        home_page.navigate_to()

    with allure.step("Scroll to bottom and verify recommended items"):
        home_page.scroll_to_bottom()
        expect(home_page.recommended_items_title).to_be_visible()

    with allure.step("Add recommended item to cart"):
        home_page.add_recommended_item_to_cart(0)

    with allure.step("Open cart"):
        modal_view_cart = home_page.page.locator(
            '.modal-content a[href="/view_cart"]'
        ).first
        try:
            modal_view_cart.click(timeout=7_000)
        except Exception:
            home_page.page.goto("/view_cart", wait_until="domcontentloaded", timeout=30_000)

    with allure.step("Verify item in cart"):
        items_count = cart_page.get_cart_items_count()
        if items_count == 0:
            home_page.page.goto("/", wait_until="domcontentloaded", timeout=30_000)
            home_page.scroll_to_bottom()
            home_page.add_recommended_item_to_cart(0)
            modal_view_cart = home_page.page.locator(
                '.modal-content a[href="/view_cart"]'
            ).first
            try:
                modal_view_cart.click(timeout=7_000)
            except Exception:
                home_page.page.goto(
                    "/view_cart", wait_until="domcontentloaded", timeout=30_000
                )
            items_count = cart_page.get_cart_items_count()

        assert items_count > 0
