import os
from dataclasses import dataclass
from functools import lru_cache


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class FrameworkSettings:
    base_url: str
    headless: bool
    slow_mo_ms: int
    default_timeout_ms: int
    element_timeout_ms: int
    hidden_timeout_ms: int
    retry_wait_ms: int
    retry_navigation_timeout_ms: int
    navigation_timeout_ms: int
    viewport_width: int
    viewport_height: int
    locale: str
    timezone_id: str
    user_agent: str
    ignore_https_errors: bool
    accept_downloads: bool
    trace_on_failure: bool
    screenshot_on_failure: bool
    video_on_failure: bool


@lru_cache(maxsize=1)
def load_framework_settings() -> FrameworkSettings:
    return FrameworkSettings(
        base_url=os.getenv("BASE_URL", "https://automationexercise.com").strip(),
        headless=_read_bool("HEADLESS", False),
        slow_mo_ms=_read_int("SLOW_MO_MS", 0),
        default_timeout_ms=_read_int("DEFAULT_TIMEOUT_MS", 30_000),
        element_timeout_ms=_read_int("ELEMENT_TIMEOUT_MS", 10_000),
        hidden_timeout_ms=_read_int("HIDDEN_TIMEOUT_MS", 10_000),
        retry_wait_ms=_read_int("RETRY_WAIT_MS", 2_000),
        retry_navigation_timeout_ms=_read_int("RETRY_NAVIGATION_TIMEOUT_MS", 45_000),
        navigation_timeout_ms=_read_int("NAVIGATION_TIMEOUT_MS", 60_000),
        viewport_width=_read_int("VIEWPORT_WIDTH", 1280),
        viewport_height=_read_int("VIEWPORT_HEIGHT", 720),
        locale=os.getenv("LOCALE", "en-US").strip(),
        timezone_id=os.getenv("TIMEZONE_ID", "America/New_York").strip(),
        user_agent=os.getenv("USER_AGENT", "").strip(),
        ignore_https_errors=_read_bool("IGNORE_HTTPS_ERRORS", True),
        accept_downloads=_read_bool("ACCEPT_DOWNLOADS", True),
        trace_on_failure=_read_bool("TRACE_ON_FAILURE", True),
        screenshot_on_failure=_read_bool("SCREENSHOT_ON_FAILURE", True),
        video_on_failure=_read_bool("VIDEO_ON_FAILURE", True),
    )
