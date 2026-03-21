from playwright.sync_api import Page

from pytests.config.selectors import CART_PAGE_SELECTORS
from pytests.pages.base_page import BasePage


class AutomationExerciseCartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_table = page.locator(CART_PAGE_SELECTORS.cart_table)
        self.cart_items = page.locator(CART_PAGE_SELECTORS.cart_items)
        self.product_names = page.locator(CART_PAGE_SELECTORS.product_names)
        self.product_prices = page.locator(CART_PAGE_SELECTORS.product_prices)
        self.product_quantities = page.locator(CART_PAGE_SELECTORS.product_quantities)
        self.product_totals = page.locator(CART_PAGE_SELECTORS.product_totals)
        self.remove_buttons = page.locator(CART_PAGE_SELECTORS.remove_buttons)
        self.proceed_to_checkout_button = page.get_by_role(
            CART_PAGE_SELECTORS.proceed_to_checkout_button_role[0],
            name=CART_PAGE_SELECTORS.proceed_to_checkout_button_role[1],
        )
        self.proceed_to_checkout_button_fallback = page.locator(
            'a:has-text("Proceed To Checkout")'
        ).first
        self.register_login_button = page.get_by_role(
            CART_PAGE_SELECTORS.register_login_button_role[0],
            name=CART_PAGE_SELECTORS.register_login_button_role[1],
        )

    def get_cart_items_count(self) -> int:
        return self.cart_items.count()

    def get_product_quantities(self) -> list[int]:
        return self.get_int_values(self.product_quantities)

    def get_product_prices(self) -> list[str]:
        return self.get_text_values(self.product_prices)

    def get_product_totals(self) -> list[str]:
        return self.get_text_values(self.product_totals)

    def click_proceed_to_checkout(self) -> None:
        try:
            self.proceed_to_checkout_button.click(timeout=self.settings.element_timeout_ms)
            return
        except Exception:
            pass

        self.proceed_to_checkout_button_fallback.scroll_into_view_if_needed()
        self.proceed_to_checkout_button_fallback.click(
            timeout=self.settings.element_timeout_ms, force=True
        )

    def click_register_login(self) -> None:
        self.register_login_button.click()

    def remove_product(self, index: int) -> None:
        initial_count = self.get_cart_items_count()
        self.remove_buttons.nth(index).click()
        expected_count = max(initial_count - 1, 0)
        self.page.wait_for_function(
            "(count) => document.querySelectorAll('tbody tr').length === count",
            arg=expected_count,
            timeout=10_000,
        )
