from pytests.pages.base_page import BasePage


class AutomationExerciseLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.new_user_signup_title = page.locator('h2:has-text("New User Signup!")')
        self.login_to_account_title = page.locator('h2:has-text("Login to your account")')
        self.signup_name_input = page.locator('input[data-qa="signup-name"]')
        self.signup_email_input = page.locator('input[data-qa="signup-email"]')
        self.signup_button = page.locator('button[data-qa="signup-button"]')
        self.login_email_input = page.locator('input[data-qa="login-email"]')
        self.login_password_input = page.locator('input[data-qa="login-password"]')
        self.login_button = page.locator('button[data-qa="login-button"]')
        self.login_error_message = page.locator(
            'p:has-text("Your email or password is incorrect!")'
        )
        self.signup_error_message = page.locator('p:has-text("Email Address already exist!")')

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
