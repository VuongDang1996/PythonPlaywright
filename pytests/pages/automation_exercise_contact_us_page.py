from pytests.pages.base_page import BasePage


class AutomationExerciseContactUsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.get_in_touch_title = page.locator('h2:has-text("Get In Touch")')
        self.name_input = page.locator('input[data-qa="name"]')
        self.email_input = page.locator('input[data-qa="email"]')
        self.subject_input = page.locator('input[data-qa="subject"]')
        self.message_textarea = page.locator('textarea[data-qa="message"]')
        self.file_upload_input = page.locator('input[name="upload_file"]')
        self.submit_button = page.locator('input[data-qa="submit-button"]')
        self.success_message = page.locator(
            '.status.alert.alert-success, '
            'div:has-text("Success! Your details have been submitted successfully")'
        )
        self.home_button = page.locator(
            'a:has-text("Home"), .btn.btn-success:has-text("Home")'
        ).first

    def fill_contact_form(self, contact_data: dict) -> None:
        self.name_input.fill(contact_data["name"])
        self.email_input.fill(contact_data["email"])
        self.subject_input.fill(contact_data["subject"])
        self.message_textarea.fill(contact_data["message"])

        if contact_data.get("file_path"):
            self.file_upload_input.set_input_files(contact_data["file_path"])

    def submit_form(self) -> None:
        dialog_handled = False

        def dialog_handler(dialog):
            nonlocal dialog_handled
            dialog_handled = True
            dialog.accept()

        self.page.on("dialog", dialog_handler)

        try:
            try:
                with self.page.expect_response(
                    lambda response: "contact_us" in response.url
                    and response.request.method == "POST",
                    timeout=10_000,
                ):
                    self.submit_button.click()
            except Exception:
                self.submit_button.click()

            self.page.wait_for_timeout(2_000)
            if not dialog_handled:
                pass
        finally:
            self.page.remove_listener("dialog", dialog_handler)

    def click_home(self) -> None:
        self.home_button.click()
