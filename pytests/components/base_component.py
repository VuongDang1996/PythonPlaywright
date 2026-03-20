from playwright.sync_api import Locator, Page


class BaseComponent:
    def __init__(self, page: Page) -> None:
        self.page = page

    def wait_visible(self, locator: Locator, timeout: int = 10_000) -> None:
        locator.wait_for(state="visible", timeout=timeout)

    def click_or_goto(
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
