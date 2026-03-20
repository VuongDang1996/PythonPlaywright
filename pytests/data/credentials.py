import os
from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    email: str
    password: str


def _from_env(prefix: str, default_email: str, default_password: str) -> UserCredentials:
    return UserCredentials(
        email=os.getenv(f"{prefix}_EMAIL", default_email),
        password=os.getenv(f"{prefix}_PASSWORD", default_password),
    )


def get_valid_user_credentials() -> UserCredentials:
    return _from_env("AE_VALID_USER", "vanvuongbtm@gmail.com", "vanvuongbtm@gmail.com")


def get_invalid_user_credentials() -> UserCredentials:
    return _from_env("AE_INVALID_USER", "invalid@example.com", "wrongpassword")


def get_existing_user_credentials() -> UserCredentials:
    return _from_env("AE_EXISTING_USER", "existing@example.com", "password123")
