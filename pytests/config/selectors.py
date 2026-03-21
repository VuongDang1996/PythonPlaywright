import re
from dataclasses import dataclass
from typing import Pattern


@dataclass(frozen=True)
class LoginPageSelectors:
    new_user_signup_title_role: tuple[str, str] = ("heading", "New User Signup!")
    login_to_account_title_role: tuple[str, str] = ("heading", "Login to your account")
    signup_name_input: str = 'input[data-qa="signup-name"]'
    signup_email_input: str = 'input[data-qa="signup-email"]'
    signup_button: str = 'button[data-qa="signup-button"]'
    login_email_input: str = 'input[data-qa="login-email"]'
    login_password_input: str = 'input[data-qa="login-password"]'
    login_button: str = 'button[data-qa="login-button"]'
    login_error_text: str = "Your email or password is incorrect!"
    signup_error_text: str = "Email Address already exist!"


@dataclass(frozen=True)
class CartPageSelectors:
    cart_table: str = "#cart_info_table"
    cart_items: str = "tbody tr"
    product_names: str = ".cart_description h4 a"
    product_prices: str = ".cart_price p"
    product_quantities: str = ".cart_quantity button"
    product_totals: str = ".cart_total_price"
    remove_buttons: str = ".cart_quantity_delete"
    proceed_to_checkout_button_role: tuple[str, Pattern[str]] = (
        "link",
        re.compile(r"^\s*Proceed\s+To\s+Checkout\s*$", re.IGNORECASE),
    )
    register_login_button_role: tuple[str, Pattern[str]] = (
        "link",
        re.compile(r"^\s*Register\s*/\s*Login\s*$", re.IGNORECASE),
    )


LOGIN_PAGE_SELECTORS = LoginPageSelectors()
CART_PAGE_SELECTORS = CartPageSelectors()