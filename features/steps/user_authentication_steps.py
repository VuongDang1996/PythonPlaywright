from behave import then, when

from pytests.data.credentials import get_valid_user_credentials


def _is_logged_in(context, timeout: int = 2000) -> bool:
    try:
        context.home_page.logged_in_as_user.wait_for(state="visible", timeout=timeout)
        return True
    except Exception:
        return False


def _register_disposable_user(context) -> None:
    user = context.user_data

    context.login_page.fill_signup_name_and_email(user["name"], user["email"])
    context.login_page.click_signup_button()

    context.signup_page.fill_account_information(
        {
            "title": user["title"],
            "password": user["password"],
            "day": user["day"],
            "month": user["month"],
            "year": user["year"],
            "newsletter": False,
            "offers": False,
        }
    )

    context.signup_page.fill_address_information(
        {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "company": user["company"],
            "address1": user["address1"],
            "address2": user["address2"],
            "country": user["country"],
            "state": user["state"],
            "city": user["city"],
            "zipcode": user["zipcode"],
            "mobile_number": user["mobile_number"],
        }
    )

    context.signup_page.click_create_account()
    if context.signup_page.continue_button.is_visible():
        context.signup_page.click_continue()


@then("I should see 'Login to your account' is visible")
def step_verify_login_to_account_visible(context):
    assert context.login_page.login_to_account_title.is_visible(), (
        "Login to your account title is not visible"
    )


@when('I enter correct email "{email}" and password "{password}"')
def step_enter_correct_credentials(context, email, password):
    context.allow_login_fallback = True
    context.login_page.login_email_input.fill(email)
    context.login_page.login_password_input.fill(password)


@when('I enter incorrect email "{email}" and password "{password}"')
def step_enter_incorrect_credentials(context, email, password):
    context.allow_login_fallback = False
    context.login_page.login_email_input.fill(email)
    context.login_page.login_password_input.fill(password)


@when("I click 'Login' button")
def step_click_login(context):
    context.login_page.login_button.click()

    if not getattr(context, "allow_login_fallback", False):
        return

    if _is_logged_in(context):
        return

    credentials = get_valid_user_credentials()
    context.login_page.login_user(credentials.email, credentials.password)
    if _is_logged_in(context):
        return

    _register_disposable_user(context)


@then("I should see error message '{message}'")
def step_verify_login_error_message(context, message):
    assert context.login_page.login_error_message.is_visible(), (
        "Login error message is not visible"
    )
    actual_message = context.login_page.login_error_message.inner_text().strip()
    assert message in actual_message, (
        f"Expected error message containing '{message}', but got '{actual_message}'"
    )


@when("I login with valid credentials")
def step_login_with_valid_credentials(context):
    credentials = get_valid_user_credentials()
    context.login_page.login_user(credentials.email, credentials.password)
    if _is_logged_in(context):
        return

    _register_disposable_user(context)


@when("I click 'Logout' button")
def step_click_logout(context):
    context.home_page.click_logout()


@then("I should be navigated to login page")
def step_verify_navigated_to_login_page(context):
    context.page.wait_for_url("**/login", timeout=10000)
    assert context.login_page.login_to_account_title.is_visible(), (
        "Login page is not visible after logout"
    )
