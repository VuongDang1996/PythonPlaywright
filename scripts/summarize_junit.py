import argparse
import json
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any


def _collect_xml_files(path: Path) -> list[Path]:
    if path.is_file() and path.suffix.lower() == ".xml":
        return [path]
    if path.is_dir():
        return sorted(path.rglob("*.xml"))
    return []


def _case_key(case: ET.Element) -> str:
    class_name = case.attrib.get("classname", "")
    name = case.attrib.get("name", "")
    return f"{class_name}::{name}" if class_name else name


def _case_status(case: ET.Element) -> str:
    if case.find("error") is not None:
        return "error"
    if case.find("failure") is not None:
        return "failed"
    if case.find("skipped") is not None:
        return "skipped"
    return "passed"


def _safe_int(value: Any) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def _safe_float(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _message_from_node(node: ET.Element | None) -> str:
    if node is None:
        return ""

    raw = (node.attrib.get("message") or node.text or "").strip()
    if not raw:
        return ""

    for line in raw.splitlines():
        text = line.strip()
        if text:
            return text
    return ""


def _pass_rate(passed: int, tests: int) -> float:
    if tests <= 0:
        return 0.0
    return round((passed / tests) * 100, 2)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _classify_failure_message(message: str, final_status: str) -> str:
    text = (message or "").lower()

    if "targetclosederror" in text or "browser has been closed" in text:
        return "browser_crash_or_launch"
    if "timeout" in text:
        return "timeout"
    if "filenotfounderror" in text:
        return "artifact_or_file_path"
    if "assertionerror" in text or "expected" in text:
        return "assertion"
    if "google_vignette" in text or "vignette" in text:
        return "site_interstitial_or_popup"
    if "locator" in text and "not found" in text:
        return "locator_not_found"
    if "network" in text or "connection" in text:
        return "network_or_connectivity"
    if final_status == "error":
        return "setup_or_runtime_error"
    return "other"


def build_summary(xml_files: list[Path]) -> dict:
    totals = {
        "files": len(xml_files),
        "tests": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "passed": 0,
        "time": 0.0,
    }

    attempts: dict[str, list[str]] = defaultdict(list)
    durations: dict[str, list[float]] = defaultdict(list)
    failure_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"failed": 0, "errors": 0}
    )
    failure_messages: dict[str, str] = {}
    suite_rollup: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "suite": "",
            "tests": 0,
            "passed": 0,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "time": 0.0,
            "pass_rate": 0.0,
        }
    )

    for file in xml_files:
        try:
            tree = ET.parse(file)
        except ET.ParseError:
            continue

        root = tree.getroot()

        suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
        for suite in suites:
            suite_name = suite.attrib.get("name") or f"suite@{file.name}"
            suite_tests = _safe_int(suite.attrib.get("tests", "0"))
            suite_failures = _safe_int(suite.attrib.get("failures", "0"))
            suite_errors = _safe_int(suite.attrib.get("errors", "0"))
            suite_skipped = _safe_int(suite.attrib.get("skipped", "0"))
            suite_time = _safe_float(suite.attrib.get("time", "0"))
            suite_passed = max(
                suite_tests - suite_failures - suite_errors - suite_skipped,
                0,
            )

            totals["tests"] += suite_tests
            totals["failures"] += suite_failures
            totals["errors"] += suite_errors
            totals["skipped"] += suite_skipped
            totals["time"] += suite_time

            suite_data = suite_rollup[suite_name]
            suite_data["suite"] = suite_name
            suite_data["tests"] += suite_tests
            suite_data["passed"] += suite_passed
            suite_data["failures"] += suite_failures
            suite_data["errors"] += suite_errors
            suite_data["skipped"] += suite_skipped
            suite_data["time"] += suite_time

            for case in suite.findall("testcase"):
                key = _case_key(case)
                status = _case_status(case)
                attempts[key].append(status)
                durations[key].append(_safe_float(case.attrib.get("time", "0")))

                if status == "failed":
                    failure_counts[key]["failed"] += 1
                    failure_messages[key] = _message_from_node(case.find("failure"))
                elif status == "error":
                    failure_counts[key]["errors"] += 1
                    failure_messages[key] = _message_from_node(case.find("error"))

    if totals["tests"] == 0 and attempts:
        totals["tests"] = len(attempts)

    totals["passed"] = max(
        totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"],
        0,
    )
    totals["pass_rate"] = _pass_rate(totals["passed"], totals["tests"])

    flaky = []
    for test_name, statuses in attempts.items():
        if len(statuses) > 1 and statuses[-1] == "passed" and any(
            status != "passed" for status in statuses[:-1]
        ):
            flaky.append(
                {
                    "test": test_name,
                    "attempts": len(statuses),
                    "history": statuses,
                    "duration_total": round(sum(durations.get(test_name, [])), 3),
                }
            )

    top_failing_tests = []
    for test_name, statuses in attempts.items():
        final_status = statuses[-1]
        if final_status not in {"failed", "error"}:
            continue

        counts = failure_counts.get(test_name, {"failed": 0, "errors": 0})
        top_failing_tests.append(
            {
                "test": test_name,
                "final_status": final_status,
                "attempts": len(statuses),
                "failed_attempts": counts["failed"],
                "error_attempts": counts["errors"],
                "duration_total": round(sum(durations.get(test_name, [])), 3),
                "last_message": failure_messages.get(test_name, ""),
            }
        )

    top_failing_tests.sort(
        key=lambda item: (
            item["failed_attempts"] + item["error_attempts"],
            item["attempts"],
            item["duration_total"],
        ),
        reverse=True,
    )

    failure_categories: dict[str, int] = defaultdict(int)
    for item in top_failing_tests:
        category = _classify_failure_message(item.get("last_message", ""), item["final_status"])
        failure_categories[category] += 1

    categorized_failures = [
        {"category": category, "count": count}
        for category, count in sorted(
            failure_categories.items(),
            key=lambda pair: pair[1],
            reverse=True,
        )
    ]

    top_slowest_tests = []
    for test_name, values in durations.items():
        if not values:
            continue
        statuses = attempts.get(test_name, ["passed"])
        top_slowest_tests.append(
            {
                "test": test_name,
                "final_status": statuses[-1],
                "attempts": len(statuses),
                "duration_total": round(sum(values), 3),
                "duration_max": round(max(values), 3),
            }
        )

    top_slowest_tests.sort(
        key=lambda item: (item["duration_total"], item["duration_max"]),
        reverse=True,
    )

    passed_tests = []
    for test_name, statuses in attempts.items():
        final_status = statuses[-1]
        if final_status != "passed":
            continue

        passed_tests.append(
            {
                "test": test_name,
                "attempts": len(statuses),
                "duration_total": round(sum(durations.get(test_name, [])), 3),
            }
        )

    passed_tests.sort(
        key=lambda item: (item["duration_total"], item["attempts"]),
        reverse=True,
    )

    suite_breakdown = []
    for suite_data in suite_rollup.values():
        tests = int(suite_data["tests"])
        passed = int(suite_data["passed"])
        suite_data["pass_rate"] = _pass_rate(passed, tests)
        suite_data["time"] = round(float(suite_data["time"]), 3)
        suite_breakdown.append(suite_data)

    suite_breakdown.sort(key=lambda item: (item["tests"], item["time"]), reverse=True)

    summary = {
        "totals": totals,
        "failure_breakdown": {
            "failed": totals["failures"],
            "errors": totals["errors"],
        },
        "flaky_count": len(flaky),
        "flaky_tests": sorted(flaky, key=lambda item: item["attempts"], reverse=True),
        "top_failing_tests": top_failing_tests[:20],
        "failure_categories": categorized_failures,
        "top_slowest_tests": top_slowest_tests[:20],
        "passed_tests": passed_tests[:50],
        "suite_breakdown": suite_breakdown,
    }
    return summary


def to_markdown(summary: dict, title: str) -> str:
    totals = summary["totals"]
    lines = [
        f"## {title}",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| XML Files | {totals['files']} |",
        f"| Tests | {totals['tests']} |",
        f"| Passed | {totals['passed']} |",
        f"| Failed | {totals['failures']} |",
        f"| Errors | {totals['errors']} |",
        f"| Skipped | {totals['skipped']} |",
        f"| Pass Rate (%) | {totals['pass_rate']:.2f} |",
        f"| Flaky (pass on retry) | {summary['flaky_count']} |",
        f"| Duration (s) | {totals['time']:.2f} |",
    ]

    if summary.get("top_failing_tests"):
        lines.extend(
            [
                "",
                "### Top Failing Tests",
                "",
                "| Test | Final Status | Attempts | Failed | Errors | Message |",
                "| --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for item in summary["top_failing_tests"][:10]:
            message = _escape_cell(item.get("last_message") or "-")
            lines.append(
                f"| {_escape_cell(item['test'])} | {item['final_status']} | {item['attempts']} | "
                f"{item['failed_attempts']} | {item['error_attempts']} | {message} |"
            )

    if summary.get("failure_categories"):
        lines.extend(
            [
                "",
                "### Failure Categories",
                "",
                "| Category | Count |",
                "| --- | ---: |",
            ]
        )
        for item in summary["failure_categories"]:
            lines.append(f"| {_escape_cell(item['category'])} | {item['count']} |")

    if summary["flaky_tests"]:
        lines.extend(
            [
                "",
                "### Flaky Tests",
                "",
                "| Test | Attempts | History |",
                "| --- | ---: | --- |",
            ]
        )
        for item in summary["flaky_tests"][:20]:
            history = " -> ".join(item["history"])
            lines.append(
                f"| {_escape_cell(item['test'])} | {item['attempts']} | {_escape_cell(history)} |"
            )

    if summary.get("top_slowest_tests"):
        lines.extend(
            [
                "",
                "### Slowest Tests",
                "",
                "| Test | Final Status | Attempts | Total Duration (s) | Max Attempt (s) |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for item in summary["top_slowest_tests"][:10]:
            lines.append(
                f"| {_escape_cell(item['test'])} | {item['final_status']} | {item['attempts']} | "
                f"{item['duration_total']:.2f} | {item['duration_max']:.2f} |"
            )

    if summary.get("suite_breakdown"):
        lines.extend(
            [
                "",
                "### Suite Breakdown",
                "",
                "| Suite | Tests | Passed | Failed | Errors | Skipped | Pass Rate (%) | Duration (s) |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for item in summary["suite_breakdown"][:15]:
            lines.append(
                f"| {_escape_cell(item['suite'])} | {item['tests']} | {item['passed']} | "
                f"{item['failures']} | {item['errors']} | {item['skipped']} | "
                f"{item['pass_rate']:.2f} | {item['time']:.2f} |"
            )

    if summary.get("passed_tests"):
        lines.extend(
            [
                "",
                "### Passed Tests (sample)",
                "",
                "| Test | Attempts | Total Duration (s) |",
                "| --- | ---: | ---: |",
            ]
        )
        for item in summary["passed_tests"][:20]:
            lines.append(
                f"| {_escape_cell(item['test'])} | {item['attempts']} | {item['duration_total']:.2f} |"
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create summary from JUnit XML reports")
    parser.add_argument("--input", default="test-results", help="JUnit XML file or directory")
    parser.add_argument("--output-json", default="test-results/summary.json")
    parser.add_argument("--output-md", default="test-results/summary.md")
    parser.add_argument("--title", default="Python Test Summary")
    parser.add_argument("--github-summary", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    xml_files = _collect_xml_files(input_path)

    summary = build_summary(xml_files)
    markdown = to_markdown(summary, args.title)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(markdown, encoding="utf-8")

    if args.github_summary:
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            target = Path(summary_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as file:
                file.write(markdown)

    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
