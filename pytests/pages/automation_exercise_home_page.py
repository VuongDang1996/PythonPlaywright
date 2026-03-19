from pytests.pages.base_page import BasePage


class AutomationExerciseHomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.signup_login_link = page.locator('a[href="/login"]').first
        self.contact_us_link = page.locator('a[href="/contact_us"]').first
        self.test_cases_link = page.locator('a[href="/test_cases"]').first
        self.products_link = page.locator('a[href="/products"]').first
        self.cart_link = page.locator('a[href="/view_cart"]').first
        self.logout_link = page.locator('a[href="/logout"]')
        self.delete_account_link = page.locator('a[href="/delete_account"]')
        self.logged_in_as_user = page.locator('li:has-text("Logged in as")')
        self.home_page_carousel = page.locator("#slider-carousel")
        self.features_items = page.locator(".features_items")
        self.subscription_section = page.locator("#footer")
        self.subscription_title = page.locator('h2:has-text("Subscription")')
        self.subscription_email_input = page.locator("#susbscribe_email")
        self.subscription_submit_button = page.locator("#subscribe")
        self.subscription_success_message = page.locator(".alert-success")
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
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                try:
                    self.page.goto("/", wait_until="load", timeout=45_000)
                except Exception:
                    try:
                        self.page.goto("/", wait_until="networkidle", timeout=45_000)
                    except Exception:
                        self.page.goto("/", wait_until="domcontentloaded", timeout=30_000)
                break
            except Exception as error:
                if attempt == max_retries:
                    raise RuntimeError(
                        f"Failed to navigate to home page after {max_retries} attempts: {error}"
                    ) from error
                self.page.wait_for_timeout(2_000)

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
        self.signup_login_link.click()

    def click_contact_us(self) -> None:
        self.contact_us_link.click()

    def click_test_cases(self) -> None:
        self.test_cases_link.click()

    def click_products(self) -> None:
        try:
            self.products_link.click(timeout=10_000)
        except Exception:
            self.page.goto("/products", wait_until="domcontentloaded", timeout=30_000)
            return

        if "/products" not in self.page.url:
            self.page.goto("/products", wait_until="domcontentloaded", timeout=30_000)

    def click_cart(self) -> None:
        try:
            self.cart_link.click(timeout=10_000)
        except Exception:
            self.page.goto("/view_cart", wait_until="domcontentloaded", timeout=30_000)
            return

        if "/view_cart" not in self.page.url:
            self.page.goto("/view_cart", wait_until="domcontentloaded", timeout=30_000)

    def click_logout(self) -> None:
        self.logout_link.click()

    def click_delete_account(self) -> None:
        self.delete_account_link.click()

    def scroll_to_bottom(self) -> None:
        self.subscription_section.scroll_into_view_if_needed()

    def subscribe_to_newsletter(self, email: str) -> None:
        self.subscription_section.scroll_into_view_if_needed()
        self.subscription_email_input.fill(email)
        self.subscription_submit_button.click()

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
