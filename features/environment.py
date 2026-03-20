import os
import time

from playwright.sync_api import sync_playwright

from pytests.data.automation_exercise_data import build_sample_registration_data
from pytests.pages.auth.automation_exercise_login_page import AutomationExerciseLoginPage
from pytests.pages.auth.automation_exercise_signup_page import AutomationExerciseSignupPage
from pytests.pages.automation_exercise_cart_page import AutomationExerciseCartPage
from pytests.pages.automation_exercise_home_page import AutomationExerciseHomePage
from pytests.pages.automation_exercise_product_detail_page import (
    AutomationExerciseProductDetailPage,
)
from pytests.pages.automation_exercise_products_page import AutomationExerciseProductsPage


def before_all(context):
    context.playwright = sync_playwright().start()
    browser_name = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    launcher = getattr(context.playwright, browser_name)
    context.browser = launcher.launch(headless=headless)


def before_scenario(context, scenario):
    base_url = os.getenv("BASE_URL", "https://automationexercise.com")
    context.browser_context = context.browser.new_context(
        base_url=base_url,
        ignore_https_errors=True,
        accept_downloads=True,
        viewport={"width": 1280, "height": 720},
        locale="en-US",
        timezone_id="America/New_York",
    )
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(30000)
    context.page.set_default_navigation_timeout(60000)

    context.home_page = AutomationExerciseHomePage(context.page)
    context.login_page = AutomationExerciseLoginPage(context.page)
    context.signup_page = AutomationExerciseSignupPage(context.page)
    context.products_page = AutomationExerciseProductsPage(context.page)
    context.product_detail_page = AutomationExerciseProductDetailPage(context.page)
    context.cart_page = AutomationExerciseCartPage(context.page)

    context.user_data = build_sample_registration_data()
    context.user_data["email"] = f"bdd{int(time.time() * 1000)}@example.com"


def after_scenario(context, scenario):
    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
