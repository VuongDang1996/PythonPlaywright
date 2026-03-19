import pytest
from playwright.sync_api import expect


@pytest.mark.authentication
@pytest.mark.regression
@pytest.mark.python_migration
@pytest.mark.parametrize(
    "email,password",
    [
        ("invalid@example.com", "wrongpassword"),
        ("test@example.com", "wrongpassword"),
        ("notfound@example.com", "password123"),
    ],
)
def test_parametrized_invalid_login(home_page, login_page, email, password):
    home_page.navigate_to()
    home_page.click_signup_login()

    expect(login_page.login_to_account_title).to_be_visible()
    login_page.login_user(email, password)

    expect(login_page.login_error_message).to_be_visible()
    expect(login_page.login_error_message).to_contain_text("Your email or password is incorrect!")
