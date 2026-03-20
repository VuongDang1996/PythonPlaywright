from pathlib import Path
from re import Pattern
from typing import Literal

from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.loading_spinner = page.get_by_test_id("loading-spinner")
        self.error_message = page.get_by_role("alert").filter(has_text="error")
        self.success_message = page.get_by_role("alert").filter(has_text="success")
        self.page_title = page.get_by_role("heading", level=1)

    def wait_for_page_load(self) -> None:
        for state in ("networkidle", "domcontentloaded", "load"):
            try:
                self.page.wait_for_load_state(state, timeout=30_000)
                break
            except Exception:
                continue

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

    def get_text_values(self, locator: Locator) -> list[str]:
        values: list[str] = []
        for i in range(locator.count()):
            value = locator.nth(i).text_content()
            if value:
                values.append(value.strip())
        return values

    def get_int_values(self, locator: Locator) -> list[int]:
        values: list[int] = []
        for text in self.get_text_values(locator):
            if text.isdigit():
                values.append(int(text))
        return values

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

    def goto_with_retry(self, url: str, retries: int = 3, timeout: int = 45_000) -> None:
        last_error = None
        wait_states: tuple[Literal["load", "networkidle", "domcontentloaded"], ...] = (
            "load",
            "networkidle",
            "domcontentloaded",
        )

        for attempt in range(1, retries + 1):
            for state in wait_states:
                try:
                    self.page.goto(url, wait_until=state, timeout=timeout)
                    return
                except Exception as error:
                    last_error = error

            if attempt < retries:
                self.page.wait_for_timeout(2_000)

        raise RuntimeError(
            f"Failed to navigate to '{url}' after {retries} attempts: {last_error}"
        ) from last_error

    def click_with_fallback_navigation(
        self,
        locator: Locator,
        fallback_url: str,
        expected_url_fragment: str = "",
        timeout: int = 10_000,
    ) -> None:
        try:
            locator.click(timeout=timeout)
        except Exception:
            self.page.goto(fallback_url, wait_until="domcontentloaded", timeout=30_000)
            return

        if expected_url_fragment and expected_url_fragment not in self.page.url:
            self.page.goto(fallback_url, wait_until="domcontentloaded", timeout=30_000)

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

    def is_current_url(self, url_pattern: str | Pattern[str]) -> bool:
        current_url = self.get_current_url()
        if isinstance(url_pattern, str):
            return url_pattern in current_url
        return bool(url_pattern.search(current_url))
