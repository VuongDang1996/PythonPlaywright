from pytests.pages.base_page import BasePage
from pytests.config.selectors import LOGIN_PAGE_SELECTORS


class AutomationExerciseLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.new_user_signup_title = page.get_by_role(
            LOGIN_PAGE_SELECTORS.new_user_signup_title_role[0],
            name=LOGIN_PAGE_SELECTORS.new_user_signup_title_role[1],
        )
        self.login_to_account_title = page.get_by_role(
            LOGIN_PAGE_SELECTORS.login_to_account_title_role[0],
            name=LOGIN_PAGE_SELECTORS.login_to_account_title_role[1],
        )
        self.signup_name_input = page.locator(LOGIN_PAGE_SELECTORS.signup_name_input)
        self.signup_email_input = page.locator(LOGIN_PAGE_SELECTORS.signup_email_input)
        self.signup_button = page.locator(LOGIN_PAGE_SELECTORS.signup_button)
        self.login_email_input = page.locator(LOGIN_PAGE_SELECTORS.login_email_input)
        self.login_password_input = page.locator(LOGIN_PAGE_SELECTORS.login_password_input)
        self.login_button = page.locator(LOGIN_PAGE_SELECTORS.login_button)
        self.login_error_message = page.get_by_text(LOGIN_PAGE_SELECTORS.login_error_text)
        self.signup_error_message = page.get_by_text(LOGIN_PAGE_SELECTORS.signup_error_text)

    def signup_user(self, name: str, email: str) -> None:
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()

    def fill_signup_name_and_email(self, name: str, email: str) -> None:
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)

    def click_signup_button(self) -> None:
        self.signup_button.click()

    def login_user(self, email: str, password: str) -> None:
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()
