import time
from typing import Any, Dict

import pytest
from dotenv import load_dotenv

from pytests.data.automation_exercise_data import build_sample_registration_data
from pytests.pages.automation_exercise_cart_page import AutomationExerciseCartPage
from pytests.pages.automation_exercise_contact_us_page import AutomationExerciseContactUsPage
from pytests.pages.automation_exercise_home_page import AutomationExerciseHomePage
from pytests.pages.automation_exercise_product_detail_page import AutomationExerciseProductDetailPage
from pytests.pages.automation_exercise_products_page import AutomationExerciseProductsPage
from pytests.pages.auth.automation_exercise_login_page import AutomationExerciseLoginPage
from pytests.pages.auth.automation_exercise_signup_page import AutomationExerciseSignupPage


load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://automationexercise.com"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any], base_url: str) -> Dict[str, Any]:
    return {
        **browser_context_args,
        "base_url": base_url,
        "ignore_https_errors": True,
        "accept_downloads": True,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
    }


@pytest.fixture(autouse=True)
def configure_page(page) -> None:
    page.set_default_timeout(30_000)
    page.set_default_navigation_timeout(60_000)


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
    data = build_sample_registration_data()
    data["email"] = f"test{int(time.time() * 1000)}@example.com"
    return data
