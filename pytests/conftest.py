import os
import re
import hashlib
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from dotenv import load_dotenv

from pytests.config.settings import FrameworkSettings, load_framework_settings

from pytests.data.credentials import (
    UserCredentials,
    get_existing_user_credentials,
    get_invalid_user_credentials,
    get_valid_user_credentials,
)
from pytests.data.factories import build_registration_data
from pytests.data.user_pool import FileUserPoolManager
from pytests.flows.auth_flow import AuthFlow
from pytests.flows.cart_flow import CartFlow
from pytests.pages.automation_exercise_cart_page import AutomationExerciseCartPage
from pytests.pages.automation_exercise_contact_us_page import AutomationExerciseContactUsPage
from pytests.pages.automation_exercise_home_page import AutomationExerciseHomePage
from pytests.pages.automation_exercise_product_detail_page import (
    AutomationExerciseProductDetailPage,
)
from pytests.pages.automation_exercise_products_page import AutomationExerciseProductsPage
from pytests.pages.auth.automation_exercise_login_page import AutomationExerciseLoginPage
from pytests.pages.auth.automation_exercise_signup_page import AutomationExerciseSignupPage

allure: Any = None
try:
    import allure as _allure

    allure = _allure
except Exception:  # pragma: no cover - attachment is optional during local runs
    allure = None


load_dotenv()


def _safe_artifact_name(nodeid: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    if len(safe) <= 90:
        return safe

    digest = hashlib.sha1(nodeid.encode("utf-8")).hexdigest()[:12]
    return f"{safe[:70]}_{digest}"


def _get_worker_id() -> str:
    worker_id = os.getenv("PYTEST_XDIST_WORKER")
    return worker_id or "master"


def _is_ci_environment() -> bool:
    return os.getenv("CI", "").strip().lower() in {"1", "true", "yes", "on"}


def _worker_artifact_dir() -> Path:
    worker_id = _get_worker_id()
    if worker_id == "master":
        return Path("test-results") / "artifacts"
    return Path("test-results") / "artifacts" / worker_id


def _worker_safe_artifact_name(nodeid: str) -> str:
    safe_name = _safe_artifact_name(nodeid)
    worker_id = _get_worker_id()
    if worker_id == "master":
        return safe_name
    return f"{worker_id}_{safe_name}"


def _allure_video_attachment_type() -> Any:
    if not allure:
        return None

    return getattr(
        allure.attachment_type,
        "WEBM",
        getattr(allure.attachment_type, "MP4", allure.attachment_type.TEXT),
    )


@pytest.fixture(scope="session")
def framework_settings() -> FrameworkSettings:
    return load_framework_settings()


@pytest.fixture(scope="session")
def base_url(framework_settings: FrameworkSettings) -> str:
    return framework_settings.base_url


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: Dict[str, Any],
    framework_settings: FrameworkSettings,
    pytestconfig,
) -> Dict[str, Any]:
    headed_requested = bool(pytestconfig.getoption("headed"))
    headless = framework_settings.headless

    if headed_requested:
        headless = False
    elif _is_ci_environment():
        # CI runners typically have no display server, so force headless.
        headless = True

    return {
        **browser_type_launch_args,
        "headless": headless,
        "slow_mo": framework_settings.slow_mo_ms,
    }


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: Dict[str, Any],
    base_url: str,
    framework_settings: FrameworkSettings,
) -> Dict[str, Any]:
    context_args = {
        **browser_context_args,
        "base_url": base_url,
        "ignore_https_errors": framework_settings.ignore_https_errors,
        "accept_downloads": framework_settings.accept_downloads,
        "viewport": {
            "width": framework_settings.viewport_width,
            "height": framework_settings.viewport_height,
        },
        "locale": framework_settings.locale,
        "timezone_id": framework_settings.timezone_id,
    }

    if framework_settings.user_agent:
        context_args["user_agent"] = framework_settings.user_agent

    if framework_settings.video_on_failure:
        worker_id = _get_worker_id()
        video_dir = Path("test-results") / "videos" / worker_id
        video_dir.mkdir(parents=True, exist_ok=True)
        context_args["record_video_dir"] = str(video_dir)

    return context_args


@pytest.fixture(autouse=True)
def configure_page(page, framework_settings: FrameworkSettings) -> None:
    page.set_default_timeout(framework_settings.default_timeout_ms)
    page.set_default_navigation_timeout(framework_settings.navigation_timeout_ms)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def capture_artifacts_on_failure(request, page, context, framework_settings: FrameworkSettings):
    console_messages: list[str] = []

    def _on_console_message(message) -> None:
        console_messages.append(f"[{message.type}] {message.text}")

    page.on("console", _on_console_message)

    if framework_settings.trace_on_failure:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    page.remove_listener("console", _on_console_message)

    call_report = getattr(request.node, "rep_call", None)
    failed = bool(call_report and call_report.failed)

    if failed:
        artifact_dir = _worker_artifact_dir()
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_name = _worker_safe_artifact_name(request.node.nodeid)

        if framework_settings.screenshot_on_failure:
            screenshot_path = artifact_dir / f"{artifact_name}.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path), full_page=True)
            if allure:
                allure.attach.file(
                    str(screenshot_path),
                    name="failure-screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

        if console_messages:
            console_path = artifact_dir / f"{artifact_name}.console.log"
            console_path.parent.mkdir(parents=True, exist_ok=True)
            console_path.write_text("\n".join(console_messages), encoding="utf-8")
            if allure:
                allure.attach.file(
                    str(console_path),
                    name="browser-console",
                    attachment_type=allure.attachment_type.TEXT,
                )

    if framework_settings.trace_on_failure:
        if failed:
            artifact_dir = _worker_artifact_dir()
            artifact_dir.mkdir(parents=True, exist_ok=True)
            trace_path = artifact_dir / f"{_worker_safe_artifact_name(request.node.nodeid)}.zip"
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            context.tracing.stop(path=str(trace_path))
            if allure:
                allure.attach.file(
                    str(trace_path),
                    name="playwright-trace",
                    attachment_type=allure.attachment_type.ZIP,
                )
        else:
            context.tracing.stop()

    if failed and framework_settings.video_on_failure and allure:
        try:
            video = page.video
            if video:
                # Ensure the page is finalized so Playwright writes the video file.
                if not page.is_closed():
                    page.close()

                video_path = Path(video.path())
                if video_path.exists():
                    allure.attach.file(
                        str(video_path),
                        name="failure-video",
                        attachment_type=_allure_video_attachment_type(),
                    )
        except Exception:
            # Video attachment is best-effort and should never break test teardown.
            pass


@pytest.fixture
def home_page(page) -> AutomationExerciseHomePage:
    return AutomationExerciseHomePage(page)


@pytest.fixture
def login_page(page) -> AutomationExerciseLoginPage:
    return AutomationExerciseLoginPage(page)


@pytest.fixture
def signup_page(page) -> AutomationExerciseSignupPage:
    return AutomationExerciseSignupPage(page)


@pytest.fixture
def contact_page(page) -> AutomationExerciseContactUsPage:
    return AutomationExerciseContactUsPage(page)


@pytest.fixture
def products_page(page) -> AutomationExerciseProductsPage:
    return AutomationExerciseProductsPage(page)


@pytest.fixture
def product_detail_page(page) -> AutomationExerciseProductDetailPage:
    return AutomationExerciseProductDetailPage(page)


@pytest.fixture
def cart_page(page) -> AutomationExerciseCartPage:
    return AutomationExerciseCartPage(page)


@pytest.fixture
def registration_data() -> Dict[str, str]:
    return build_registration_data()


@pytest.fixture(scope="session")
def valid_user_credentials() -> UserCredentials:
    return get_valid_user_credentials()


@pytest.fixture(scope="session")
def invalid_user_credentials() -> UserCredentials:
    return get_invalid_user_credentials()


@pytest.fixture(scope="session")
def existing_user_credentials() -> UserCredentials:
    return get_existing_user_credentials()


@pytest.fixture(scope="session")
def user_pool_manager(valid_user_credentials: UserCredentials) -> FileUserPoolManager:
    extra_users_raw = os.getenv("AE_USER_POOL_USERS", "").strip()
    extra_users: list[UserCredentials] = []

    if extra_users_raw:
        for pair in extra_users_raw.split(";"):
            parts = pair.strip().split(":", 1)
            if len(parts) == 2 and parts[0] and parts[1]:
                extra_users.append(UserCredentials(email=parts[0].strip(), password=parts[1].strip()))

    seed_users = [valid_user_credentials, *extra_users]
    pool_file = os.getenv("AE_USER_POOL_FILE", "test-results/state/user_pool.json")
    return FileUserPoolManager(pool_file=pool_file, seed_users=seed_users)


@pytest.fixture
def leased_valid_user_credentials(
    user_pool_manager: FileUserPoolManager, valid_user_credentials: UserCredentials
) -> Generator[UserCredentials, None, None]:
    leased_user = user_pool_manager.acquire(fallback=valid_user_credentials)
    try:
        yield leased_user
    finally:
        user_pool_manager.release(leased_user)


@pytest.fixture
def auth_flow() -> AuthFlow:
    return AuthFlow()


@pytest.fixture
def cart_flow() -> CartFlow:
    return CartFlow()


@pytest.fixture
def authenticated_home_page(
    auth_flow: AuthFlow,
    home_page: AutomationExerciseHomePage,
    login_page: AutomationExerciseLoginPage,
    leased_valid_user_credentials: UserCredentials,
) -> AutomationExerciseHomePage:
    auth_flow.login_from_home(home_page, login_page, leased_valid_user_credentials)
    return home_page


@pytest.fixture
def checkout_ready_cart(
    home_page: AutomationExerciseHomePage,
    products_page: AutomationExerciseProductsPage,
    cart_page: AutomationExerciseCartPage,
) -> AutomationExerciseCartPage:
    home_page.navigate_to()
    home_page.click_products()
    products_page.hover_and_add_to_cart(0)
    products_page.click_view_cart()
    return cart_page
