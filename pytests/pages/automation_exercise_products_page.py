from playwright.sync_api import Page

from pytests.components.cart_modal_component import CartModalComponent
from pytests.pages.base_page import BasePage


class AutomationExerciseProductsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_modal = CartModalComponent(page)
        self.all_products_title = page.locator(
            'h2:has-text("All Products"), h2.title.text-center:has-text("All Products")'
        )
        self.products_list = page.locator(".features_items")
        self.view_product_links = page.locator('a:has-text("View Product")')
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_title = page.locator('h2:has-text("Searched Products")')
        self.search_results = page.locator(".features_items .product-image-wrapper")
        self.continue_shopping_button = self.cart_modal.continue_shopping_button
        self.view_cart_button = self.cart_modal.view_cart_button

    def click_view_product(self, index: int = 0) -> None:
        self.view_product_links.nth(index).click()

    def search_products(self, search_term: str) -> None:
        self.search_input.fill(search_term)
        self.search_button.click()

    def get_search_results_count(self) -> int:
        return self.search_results.count()

    def hover_and_add_to_cart(self, product_index: int) -> None:
        product = self.products_list.locator(".product-image-wrapper").nth(product_index)
        try:
            product.hover()
            product.locator(".overlay-content .add-to-cart").click(timeout=10_000)
            return
        except Exception:
            pass

        # Fallback for cases where overlay is unstable or obscured by sticky elements.
        fallback_button = self.page.locator(
            ".features_items .product-image-wrapper .add-to-cart"
        ).nth(product_index)
        fallback_button.click(timeout=10_000, force=True)

    def click_continue_shopping(self) -> None:
        self.cart_modal.click_continue_shopping()

    def click_view_cart(self) -> None:
        self.cart_modal.click_view_cart()

    def add_search_results_to_cart(self, product_count: int | None = None) -> None:
        count = product_count or self.get_search_results_count()
        for i in range(count):
            try:
                self.search_results.nth(i).hover()
                self.page.wait_for_timeout(500)
                self.search_results.nth(i).locator(".overlay-content .add-to-cart").click(
                    timeout=10_000
                )
                self.click_continue_shopping()
                self.page.wait_for_timeout(1_000)
            except Exception:
                continue
