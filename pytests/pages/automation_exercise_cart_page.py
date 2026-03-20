from playwright.sync_api import Page

from pytests.pages.base_page import BasePage


class AutomationExerciseCartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_table = page.locator("#cart_info_table")
        self.cart_items = page.locator("tbody tr")
        self.product_names = page.locator(".cart_description h4 a")
        self.product_prices = page.locator(".cart_price p")
        self.product_quantities = page.locator(".cart_quantity button")
        self.product_totals = page.locator(".cart_total_price")
        self.remove_buttons = page.locator(".cart_quantity_delete")
        self.proceed_to_checkout_button = page.locator('a:has-text("Proceed To Checkout")')
        self.register_login_button = page.locator('u:has-text("Register / Login")')

    def get_cart_items_count(self) -> int:
        return self.cart_items.count()

    def get_product_quantities(self) -> list[int]:
        return self.get_int_values(self.product_quantities)

    def get_product_prices(self) -> list[str]:
        return self.get_text_values(self.product_prices)

    def get_product_totals(self) -> list[str]:
        return self.get_text_values(self.product_totals)

    def click_proceed_to_checkout(self) -> None:
        self.proceed_to_checkout_button.click()

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
