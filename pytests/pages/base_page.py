from pathlib import Path

from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.loading_spinner = page.get_by_test_id("loading-spinner")
        self.error_message = page.get_by_role("alert").filter(has_text="error")
        self.success_message = page.get_by_role("alert").filter(has_text="success")
        self.page_title = page.get_by_role("heading", level=1)

    def wait_for_page_load(self) -> None:
        try:
            self.page.wait_for_load_state("networkidle", timeout=30_000)
        except Exception:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=30_000)
            except Exception:
                self.page.wait_for_load_state("load", timeout=30_000)

        try:
            self.loading_spinner.wait_for(state="hidden", timeout=10_000)
        except Exception:
            pass

    def get_page_title(self) -> str:
        return self.page.title()

    def get_page_heading(self) -> str:
        text = self.page_title.text_content()
        return text or ""

    def has_error(self) -> bool:
        try:
            return self.error_message.is_visible()
        except Exception:
            return False

    def get_error_message(self) -> str:
        if self.has_error():
            text = self.error_message.text_content()
            return text or ""
        return ""

    def has_success(self) -> bool:
        try:
            return self.success_message.is_visible()
        except Exception:
            return False

    def get_success_message(self) -> str:
        if self.has_success():
            text = self.success_message.text_content()
            return text or ""
        return ""

    def wait_for_element(self, locator: Locator, timeout: int = 10_000) -> None:
        locator.wait_for(state="visible", timeout=timeout)

    def wait_for_element_hidden(self, locator: Locator, timeout: int = 10_000) -> None:
        locator.wait_for(state="hidden", timeout=timeout)

    def scroll_to_element(self, locator: Locator) -> None:
        locator.scroll_into_view_if_needed()

    def take_screenshot(self, name: str = "") -> bytes:
        screenshot_name = name or f"screenshot-{int(self.page.evaluate('Date.now()'))}"
        screenshot_dir = Path("test-results") / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"{screenshot_name}.png"
        return self.page.screenshot(path=str(screenshot_path), full_page=True)

    def wait_for_navigation(self, url: str = "") -> None:
        if url:
            self.page.wait_for_url(url)
        else:
            self.page.wait_for_load_state("networkidle")

    def refresh_page(self) -> None:
        self.page.reload()
        self.wait_for_page_load()

    def go_back(self) -> None:
        self.page.go_back()
        self.wait_for_page_load()

    def go_forward(self) -> None:
        self.page.go_forward()
        self.wait_for_page_load()

    def get_current_url(self) -> str:
        return self.page.url

    def is_current_url(self, url_pattern) -> bool:
        current_url = self.get_current_url()
        if isinstance(url_pattern, str):
            return url_pattern in current_url
        return bool(url_pattern.search(current_url))
