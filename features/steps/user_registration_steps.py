from behave import given, then, when


@given("I navigate to the home page")
def step_navigate_home(context):
    context.home_page.navigate_to()


@when("I verify that home page is visible successfully")
def step_verify_home_visible(context):
    assert context.home_page.home_page_carousel.is_visible(), "Home page carousel is not visible"


@when("I click on 'Signup / Login' button")
def step_click_signup_login(context):
    context.home_page.click_signup_login()


@then("I should see 'New User Signup!' is visible")
def step_verify_new_signup_visible(context):
    assert context.login_page.new_user_signup_title.is_visible(), "New User Signup title is not visible"


@when('I enter name "{name}" and email address')
def step_fill_name_email(context, name):
    context.user_data["name"] = name
    context.login_page.fill_signup_name_and_email(name, context.user_data["email"])


@when("I click 'Signup' button")
def step_click_signup(context):
    context.login_page.click_signup_button()


@then("I should see 'ENTER ACCOUNT INFORMATION' is visible")
def step_verify_account_info_visible(context):
    assert context.signup_page.account_info_title.is_visible(), "Enter Account Information is not visible"


@when('I fill in the account information with title "{title}", password "{password}"')
def step_fill_account_info(context, title, password):
    context.user_data["title"] = title
    context.user_data["password"] = password


@when('I select date of birth "{day}", "{month}", "{year}"')
def step_select_dob(context, day, month, year):
    context.signup_page.fill_account_information(
        {
            "title": context.user_data["title"],
            "password": context.user_data["password"],
            "day": day,
            "month": month,
            "year": year,
            "newsletter": False,
            "offers": False,
        }
    )


@when("I check newsletter and offers checkboxes")
def step_check_news_and_offers(context):
    if not context.signup_page.newsletter_checkbox.is_checked():
        context.signup_page.newsletter_checkbox.check()
    if not context.signup_page.offers_checkbox.is_checked():
        context.signup_page.offers_checkbox.check()


@when("I fill in address information")
def step_fill_address_info(context):
    row = context.table[0]
    address_data = {
        "first_name": row["firstName"],
        "last_name": row["lastName"],
        "company": row["company"],
        "address1": row["address1"],
        "address2": context.user_data.get("address2", ""),
        "country": row["country"],
        "state": row["state"],
        "city": row["city"],
        "zipcode": row["zipcode"],
        "mobile_number": row["mobileNumber"],
    }
    context.signup_page.fill_address_information(address_data)


@when("I click 'Create Account' button")
def step_click_create_account(context):
    context.signup_page.click_create_account()


@then("I should see 'ACCOUNT CREATED!' is visible")
def step_verify_account_created(context):
    assert context.signup_page.account_created_title.is_visible(), "Account Created title is not visible"


@when("I click 'Continue' button")
def step_click_continue(context):
    if context.signup_page.continue_button.is_visible():
        context.signup_page.click_continue()


@then("I click 'Continue' button")
def step_then_click_continue(context):
    step_click_continue(context)


@then("I should see 'Logged in as username' is visible")
def step_verify_logged_in(context):
    assert context.home_page.logged_in_as_user.is_visible(), "Logged in label is not visible"


@when("I click 'Delete Account' button")
def step_click_delete_account(context):
    context.home_page.click_delete_account()


@then("I should see 'ACCOUNT DELETED!' is visible")
def step_verify_account_deleted(context):
    assert context.signup_page.account_deleted_title.is_visible(), "Account Deleted title is not visible"
