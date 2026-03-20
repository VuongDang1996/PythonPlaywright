import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        item = value.strip()
        return [item] if item else []
    return []


def _as_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def build_pytest_command(config: dict[str, Any]) -> list[str]:
    cmd: list[str] = [sys.executable, "-m", "pytest"]

    paths = _as_list(config.get("paths")) or ["pytests/specs"]
    cmd.extend(paths)

    for ignored in _as_list(config.get("exclude_paths")):
        cmd.extend(["--ignore", ignored])

    markers = _as_optional_str(config.get("markers"))
    if markers:
        cmd.extend(["-m", markers])

    keyword = _as_optional_str(config.get("keyword"))
    if keyword:
        cmd.extend(["-k", keyword])

    for browser in _as_list(config.get("browsers")):
        cmd.extend(["--browser", browser])

    browser_channel = _as_optional_str(config.get("browser_channel"))
    if browser_channel:
        cmd.extend(["--browser-channel", browser_channel])

    workers = _as_optional_str(config.get("workers"))
    if workers:
        cmd.extend(["-n", workers])

    if _as_bool(config.get("headed"), default=False):
        cmd.append("--headed")

    if _as_bool(config.get("quiet"), default=True):
        cmd.append("-q")

    maxfail = config.get("maxfail")
    if isinstance(maxfail, int) and maxfail > 0:
        cmd.append(f"--maxfail={maxfail}")

    allure_dir = _as_optional_str(config.get("allure_dir"))
    if allure_dir:
        cmd.append(f"--alluredir={allure_dir}")

    junit_xml = _as_optional_str(config.get("junit_xml"))
    if junit_xml:
        junit_path = Path(junit_xml)
        if junit_path.parent:
            junit_path.parent.mkdir(parents=True, exist_ok=True)
        cmd.append(f"--junitxml={junit_xml}")

    cmd.extend(_as_list(config.get("extra_args")))

    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run pytest using a JSON suite config file (TestNG-XML style)."
    )
    parser.add_argument(
        "--suite",
        required=True,
        help="Path to suite JSON file, for example test-suites/cross-browser.json",
    )
    args = parser.parse_args()

    suite_path = Path(args.suite)
    if not suite_path.exists():
        print(f"Suite file not found: {suite_path}")
        return 2

    try:
        config = json.loads(suite_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid suite JSON in {suite_path}: {exc}")
        return 2

    command = build_pytest_command(config)
    print("Running suite:", suite_path)
    print("Command:", " ".join(command))

    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
