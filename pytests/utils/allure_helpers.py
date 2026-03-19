from typing import Any

import allure


class AllureHelpers:
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
        allure.dynamic.parameter(name, str(value))

    @staticmethod
    def add_screenshot(name: str, screenshot: bytes) -> None:
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
