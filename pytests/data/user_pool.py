import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from pytests.data.credentials import UserCredentials


@dataclass(frozen=True)
class _UserLease:
    email: str


class FileUserPoolManager:
    def __init__(self, pool_file: str, seed_users: list[UserCredentials]) -> None:
        self.pool_path = Path(pool_file)
        self.lock_path = self.pool_path.with_suffix(f"{self.pool_path.suffix}.lock")
        self.pool_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize(seed_users)

    def _initialize(self, seed_users: list[UserCredentials]) -> None:
        if self.pool_path.exists():
            return

        users = []
        seen: set[str] = set()
        for user in seed_users:
            if user.email in seen:
                continue
            users.append({"email": user.email, "password": user.password, "leased": False})
            seen.add(user.email)

        self.pool_path.write_text(json.dumps({"users": users}, indent=2), encoding="utf-8")

    def _acquire_lock(self, timeout_seconds: float = 15.0) -> None:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.close(fd)
                return
            except FileExistsError:
                time.sleep(0.05)
        raise TimeoutError(f"Timed out acquiring lock for {self.pool_path}")

    def _release_lock(self) -> None:
        try:
            self.lock_path.unlink(missing_ok=True)
        except Exception:
            pass

    def _load(self) -> dict:
        if not self.pool_path.exists():
            return {"users": []}
        return json.loads(self.pool_path.read_text(encoding="utf-8"))

    def _save(self, payload: dict) -> None:
        self.pool_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def acquire(self, fallback: UserCredentials) -> UserCredentials:
        self._acquire_lock()
        try:
            payload = self._load()
            users = payload.get("users", [])
            for user in users:
                if not user.get("leased", False):
                    user["leased"] = True
                    self._save(payload)
                    return UserCredentials(email=user["email"], password=user["password"])
        finally:
            self._release_lock()

        return fallback

    def release(self, user: UserCredentials) -> None:
        self._acquire_lock()
        try:
            payload = self._load()
            users = payload.get("users", [])
            for entry in users:
                if entry.get("email") == user.email:
                    entry["leased"] = False
                    break
            self._save(payload)
        finally:
            self._release_lock()
