from playwright.sync_api import Page

from pytests.components.base_component import BaseComponent


class SubscriptionComponent(BaseComponent):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.subscription_section = page.locator("#footer")
        self.subscription_title = page.locator('h2:has-text("Subscription")')
        self.subscription_email_input = page.locator("#susbscribe_email")
        self.subscription_submit_button = page.locator("#subscribe")
        self.subscription_success_message = page.locator(".alert-success")

    def scroll_to_subscription(self) -> None:
        self.subscription_section.scroll_into_view_if_needed()

    def subscribe(self, email: str) -> None:
        self.scroll_to_subscription()
        self.subscription_email_input.fill(email)
        self.subscription_submit_button.click()
