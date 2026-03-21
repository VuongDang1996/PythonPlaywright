from pytests.data.credentials import UserCredentials
from pytests.pages.auth.automation_exercise_login_page import AutomationExerciseLoginPage
from pytests.pages.auth.automation_exercise_signup_page import AutomationExerciseSignupPage
from pytests.pages.automation_exercise_home_page import AutomationExerciseHomePage


class AuthFlow:
    def login_from_home(
        self,
        home_page: AutomationExerciseHomePage,
        login_page: AutomationExerciseLoginPage,
        credentials: UserCredentials,
    ) -> None:
        home_page.navigate_to()
        home_page.click_signup_login()
        login_page.login_user(credentials.email, credentials.password)

    def logout(self, home_page: AutomationExerciseHomePage) -> None:
        home_page.click_logout()

    def ensure_logged_in(
        self,
        home_page: AutomationExerciseHomePage,
        login_page: AutomationExerciseLoginPage,
        signup_page: AutomationExerciseSignupPage,
        preferred_credentials: UserCredentials,
        registration_data: dict[str, str],
    ) -> UserCredentials:
        home_page.navigate_to()
        home_page.click_signup_login()
        login_page.login_user(preferred_credentials.email, preferred_credentials.password)

        if home_page.logged_in_as_user.is_visible(timeout=7_000):
            return preferred_credentials

        login_page.signup_user(registration_data["name"], registration_data["email"])
        signup_page.fill_account_information(
            {
                "title": registration_data["title"],
                "password": registration_data["password"],
                "day": registration_data["day"],
                "month": registration_data["month"],
                "year": registration_data["year"],
                "newsletter": True,
                "offers": True,
            }
        )
        signup_page.fill_address_information(registration_data)
        signup_page.click_create_account()
        try:
            signup_page.click_continue()
        except Exception:
            home_page.goto_with_retry("/", retries=2)

        if not home_page.logged_in_as_user.is_visible(timeout=7_000):
            home_page.click_signup_login()
            login_page.login_user(registration_data["email"], registration_data["password"])

        return UserCredentials(
            email=registration_data["email"], password=registration_data["password"]
        )
