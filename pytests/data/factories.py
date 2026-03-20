import time
from copy import deepcopy
from typing import Any

from pytests.data.automation_exercise_data import (
    SAMPLE_CONTACT_DATA,
    SAMPLE_REVIEW_DATA,
    build_sample_registration_data,
)


def build_unique_email(prefix: str = "test", domain: str = "example.com") -> str:
    return f"{prefix}{int(time.time() * 1000)}@{domain}"


def build_registration_data(overrides: dict[str, Any] | None = None) -> dict[str, str]:
    data = build_sample_registration_data()
    data["email"] = build_unique_email()
    if overrides:
        for key, value in overrides.items():
            data[key] = str(value)
    return data


def build_contact_data(overrides: dict[str, Any] | None = None) -> dict[str, str]:
    data = deepcopy(SAMPLE_CONTACT_DATA)
    if overrides:
        for key, value in overrides.items():
            data[key] = str(value)
    return data


def build_review_data(overrides: dict[str, Any] | None = None) -> dict[str, str]:
    data = deepcopy(SAMPLE_REVIEW_DATA)
    if overrides:
        for key, value in overrides.items():
            data[key] = str(value)
    return data
