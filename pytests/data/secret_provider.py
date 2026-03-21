import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class SecretProvider:
    def get(self, name: str, default: str = "") -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class EnvSecretProvider(SecretProvider):
    def get(self, name: str, default: str = "") -> str:
        return os.getenv(name, default)


@lru_cache(maxsize=1)
def get_secret_provider() -> SecretProvider:
    return EnvSecretProvider()
