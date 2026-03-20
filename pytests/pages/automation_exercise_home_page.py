from pytests.components.navigation_component import NavigationComponent
from pytests.components.subscription_component import SubscriptionComponent
from pytests.pages.base_page import BasePage


class AutomationExerciseHomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.navigation = NavigationComponent(page)
        self.subscription = SubscriptionComponent(page)

        # Backward-compatible aliases to avoid breaking existing tests.
        self.signup_login_link = self.navigation.signup_login_link
        self.contact_us_link = self.navigation.contact_us_link
        self.test_cases_link = self.navigation.test_cases_link
        self.products_link = self.navigation.products_link
        self.cart_link = self.navigation.cart_link
        self.logout_link = self.navigation.logout_link
        self.delete_account_link = self.navigation.delete_account_link
        self.logged_in_as_user = self.navigation.logged_in_as_user
        self.home_page_carousel = page.locator("#slider-carousel")
        self.features_items = page.locator(".features_items")
        self.subscription_section = self.subscription.subscription_section
        self.subscription_title = self.subscription.subscription_title
        self.subscription_email_input = self.subscription.subscription_email_input
        self.subscription_submit_button = self.subscription.subscription_submit_button
        self.subscription_success_message = self.subscription.subscription_success_message
        self.recommended_items = page.locator(".recommended_items")
        self.recommended_items_title = page.locator('h2:has-text("recommended items")')
        self.scroll_up_button = page.locator("#scrollUp")
        self.full_fledged_text = page.locator(
            'h2:has-text("Full-Fledged practice website for Automation Engineers")'
        ).first
        self.categories_sidebar = page.locator(".left-sidebar .panel-group")
        self.women_category = page.locator('a[href="#Women"]')
        self.men_category = page.locator('a[href="#Men"]')
        self.brands_sidebar = page.locator(".brands_products")

    def navigate_to(self) -> None:
        self.goto_with_retry("/", retries=3, timeout=45_000)
        self.wait_for_basic_page_ready()

    def wait_for_basic_page_ready(self) -> None:
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10_000)
            self.page.wait_for_selector("body", timeout=10_000)
            try:
                self.page.wait_for_selector("header, nav, .navbar", timeout=5_000)
            except Exception:
                pass
        except Exception:
            pass

    def click_signup_login(self) -> None:
        self.navigation.click_signup_login()

    def click_contact_us(self) -> None:
        self.navigation.click_contact_us()

    def click_test_cases(self) -> None:
        self.navigation.click_test_cases()

    def click_products(self) -> None:
        self.navigation.click_products()

    def click_cart(self) -> None:
        self.navigation.click_cart()

    def click_logout(self) -> None:
        self.navigation.click_logout()

    def click_delete_account(self) -> None:
        self.navigation.click_delete_account()

    def scroll_to_bottom(self) -> None:
        self.subscription.scroll_to_subscription()

    def subscribe_to_newsletter(self, email: str) -> None:
        self.subscription.subscribe(email)

    def add_recommended_item_to_cart(self, index: int = 0) -> None:
        self.recommended_items.scroll_into_view_if_needed()
        add_to_cart_button = self.recommended_items.locator("a.add-to-cart").nth(index)
        try:
            add_to_cart_button.click(timeout=10_000)
        except Exception:
            add_to_cart_button.click(timeout=10_000, force=True)

    def click_scroll_up_button(self) -> None:
        self.scroll_up_button.click()

    def scroll_to_top(self) -> None:
        self.page.evaluate("window.scrollTo(0, 0)")

    def click_women_category(self) -> None:
        self.women_category.click()

    def click_men_category(self) -> None:
        self.men_category.click()

    def click_women_subcategory(self, subcategory: str) -> None:
        subcategory_link = self.page.locator(
            f'#Women a[href*="/category_products/"]:has-text("{subcategory}")'
        )
        subcategory_link.click()

    def click_men_subcategory(self, subcategory: str) -> None:
        subcategory_link = self.page.locator(
            f'a[href*="/category_products/"]:has-text("{subcategory}")'
        )
        subcategory_link.click()

    def click_brand(self, brand_name: str) -> None:
        brand_link = self.brands_sidebar.locator(f'a:has-text("{brand_name}")')
        brand_link.click()
