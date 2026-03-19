from pytests.pages.base_page import BasePage


class AutomationExerciseSignupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.account_info_title = page.locator('h2:has-text("Enter Account Information")')
        self.title_mr = page.locator("#id_gender1")
        self.title_mrs = page.locator("#id_gender2")
        self.password_input = page.locator("#password")
        self.day_select = page.locator("#days")
        self.month_select = page.locator("#months")
        self.year_select = page.locator("#years")
        self.newsletter_checkbox = page.locator("#newsletter")
        self.offers_checkbox = page.locator("#optin")
        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.company_input = page.locator("#company")
        self.address1_input = page.locator("#address1")
        self.address2_input = page.locator("#address2")
        self.country_select = page.locator("#country")
        self.state_input = page.locator("#state")
        self.city_input = page.locator("#city")
        self.zipcode_input = page.locator("#zipcode")
        self.mobile_number_input = page.locator("#mobile_number")
        self.create_account_button = page.locator('button[data-qa="create-account"]')
        self.account_created_title = page.locator(
            'h2[data-qa="account-created"], h2:has-text("Account Created!")'
        )
        self.continue_button = page.locator('a[data-qa="continue-button"]')
        self.account_deleted_title = page.locator(
            'h2[data-qa="account-deleted"], h2:has-text("Account Deleted!")'
        )

    def fill_account_information(self, account_data: dict) -> None:
        if account_data["title"] == "Mr":
            self.title_mr.check()
        else:
            self.title_mrs.check()

        self.password_input.fill(account_data["password"])
        self.day_select.select_option(account_data["day"])
        self.month_select.select_option(account_data["month"])
        self.year_select.select_option(account_data["year"])

        if account_data.get("newsletter"):
            self.newsletter_checkbox.check()

        if account_data.get("offers"):
            self.offers_checkbox.check()

    def fill_address_information(self, address_data: dict) -> None:
        self.first_name_input.fill(address_data["first_name"])
        self.last_name_input.fill(address_data["last_name"])
        self.company_input.fill(address_data["company"])
        self.address1_input.fill(address_data["address1"])

        if address_data.get("address2"):
            self.address2_input.fill(address_data["address2"])

        self.country_select.select_option(address_data["country"])
        self.state_input.fill(address_data["state"])
        self.city_input.fill(address_data["city"])
        self.zipcode_input.fill(address_data["zipcode"])
        self.mobile_number_input.fill(address_data["mobile_number"])

    def click_create_account(self) -> None:
        self.create_account_button.click()
        self.page.wait_for_load_state("domcontentloaded", timeout=30_000)

    def click_continue(self) -> None:
        self.continue_button.click()
