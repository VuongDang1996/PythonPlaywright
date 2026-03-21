from typing import Any

import allure


class AllureHelpers:
    SENSITIVE_MARKERS = ("password", "secret", "token", "api key", "apikey")

    @staticmethod
    def _mask_email(value: str) -> str:
        if "@" not in value:
            return "***"
        local, domain = value.split("@", 1)
        if len(local) <= 2:
            return f"***@{domain}"
        return f"{local[:2]}***@{domain}"

    @staticmethod
    def _safe_parameter_value(name: str, value: Any) -> str:
        value_str = str(value)
        lowered_name = name.strip().lower()

        if any(marker in lowered_name for marker in AllureHelpers.SENSITIVE_MARKERS):
            return "***"

        if "email" in lowered_name:
            return AllureHelpers._mask_email(value_str)

        return value_str

    @staticmethod
    def add_description(description: str) -> None:
        allure.dynamic.description(description)

    @staticmethod
    def add_test_id(test_id: str) -> None:
        allure.dynamic.label("testId", test_id)

    @staticmethod
    def add_story(story: str) -> None:
        allure.dynamic.story(story)

    @staticmethod
    def add_feature(feature: str) -> None:
        allure.dynamic.feature(feature)

    @staticmethod
    def add_epic(epic: str) -> None:
        allure.dynamic.epic(epic)

    @staticmethod
    def add_severity(severity: str) -> None:
        allure.dynamic.severity(severity)

    @staticmethod
    def add_owner(owner: str) -> None:
        allure.dynamic.label("owner", owner)

    @staticmethod
    def add_tag(tag: str) -> None:
        allure.dynamic.tag(tag)

    @staticmethod
    def add_parameter(name: str, value: Any) -> None:
        allure.dynamic.parameter(name, AllureHelpers._safe_parameter_value(name, value))

    @staticmethod
    def add_screenshot(name: str, screenshot: bytes) -> None:
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
