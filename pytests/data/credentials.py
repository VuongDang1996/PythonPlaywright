from dataclasses import dataclass

from pytests.data.secret_provider import get_secret_provider


@dataclass(frozen=True)
class UserCredentials:
    email: str
    password: str

    def masked_email(self) -> str:
        if "@" not in self.email:
            return "***"
        local, domain = self.email.split("@", 1)
        if len(local) <= 2:
            return f"***@{domain}"
        return f"{local[:2]}***@{domain}"

    def masked(self) -> "UserCredentials":
        return UserCredentials(email=self.masked_email(), password="***")


def _from_env(prefix: str, default_email: str, default_password: str) -> UserCredentials:
    provider = get_secret_provider()
    return UserCredentials(
        email=provider.get(f"{prefix}_EMAIL", default_email),
        password=provider.get(f"{prefix}_PASSWORD", default_password),
    )


def get_valid_user_credentials() -> UserCredentials:
    return _from_env("AE_VALID_USER", "vanvuongbtm@gmail.com", "vanvuongbtm@gmail.com")


def get_invalid_user_credentials() -> UserCredentials:
    return _from_env("AE_INVALID_USER", "invalid@example.com", "wrongpassword")


def get_existing_user_credentials() -> UserCredentials:
    return _from_env("AE_EXISTING_USER", "existing@example.com", "password123")
