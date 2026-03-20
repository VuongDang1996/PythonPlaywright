from playwright.sync_api import Page

from pytests.components.cart_modal_component import CartModalComponent
from pytests.pages.base_page import BasePage


class AutomationExerciseProductDetailPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_modal = CartModalComponent(page)
        self.product_name = page.locator(".product-information h2")
        self.product_category = page.locator('.product-information p:has-text("Category:")')
        self.product_price = page.locator(".product-information span span")
        self.product_availability = page.locator('.product-information p:has-text("Availability:")')
        self.product_condition = page.locator('.product-information p:has-text("Condition:")')
        self.product_brand = page.locator('.product-information p:has-text("Brand:")')
        self.quantity_input = page.locator("#quantity")
        self.add_to_cart_button = page.locator(".btn.btn-default.cart")
        self.write_review_tab = page.locator('a:has-text("Write Your Review")')
        self.review_name_input = page.locator("#name")
        self.review_email_input = page.locator("#email")
        self.review_textarea = page.locator("#review")
        self.review_submit_button = page.locator("#button-review")
        self.review_success_message = page.locator('span:has-text("Thank you for your review.")')
        self.view_cart_button = self.cart_modal.view_cart_button

    def set_quantity(self, quantity: int) -> None:
        self.quantity_input.clear()
        self.quantity_input.fill(str(quantity))

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    def click_view_cart(self) -> None:
        self.cart_modal.click_view_cart()

    def write_review(self, review_data: dict) -> None:
        self.write_review_tab.click()
        self.review_name_input.fill(review_data["name"])
        self.review_email_input.fill(review_data["email"])
        self.review_textarea.fill(review_data["review"])
        self.review_submit_button.click()
