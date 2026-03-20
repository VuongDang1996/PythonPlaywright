from playwright.sync_api import Page

from pytests.components.base_component import BaseComponent


class CartModalComponent(BaseComponent):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.continue_shopping_button = page.locator('button:has-text("Continue Shopping")')
        self.view_cart_button = page.locator('a:has-text("View Cart")').first

    def click_continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    def click_view_cart(self) -> None:
        self.click_or_goto(
            self.view_cart_button,
            fallback_url="/view_cart",
            expected_url_fragment="/view_cart",
        )
