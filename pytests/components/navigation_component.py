from playwright.sync_api import Page

from pytests.components.base_component import BaseComponent


class NavigationComponent(BaseComponent):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.signup_login_link = page.locator('a[href="/login"]').first
        self.contact_us_link = page.locator('a[href="/contact_us"]').first
        self.test_cases_link = page.locator('a[href="/test_cases"]').first
        self.products_link = page.locator('a[href="/products"]').first
        self.cart_link = page.locator('a[href="/view_cart"]').first
        self.logout_link = page.locator('a[href="/logout"]')
        self.delete_account_link = page.locator('a[href="/delete_account"]')
        self.logged_in_as_user = page.locator('li:has-text("Logged in as")')

    def click_signup_login(self) -> None:
        self.signup_login_link.click()

    def click_contact_us(self) -> None:
        self.contact_us_link.click()

    def click_test_cases(self) -> None:
        self.test_cases_link.click()

    def click_products(self) -> None:
        self.click_or_goto(
            self.products_link,
            fallback_url="/products",
            expected_url_fragment="/products",
        )

    def click_cart(self) -> None:
        self.click_or_goto(
            self.cart_link,
            fallback_url="/view_cart",
            expected_url_fragment="/view_cart",
        )

    def click_logout(self) -> None:
        self.logout_link.click()

    def click_delete_account(self) -> None:
        self.delete_account_link.click()
