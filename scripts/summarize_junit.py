import argparse
import json
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


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

    for file in xml_files:
        try:
            tree = ET.parse(file)
        except ET.ParseError:
            continue

        root = tree.getroot()

        suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
        for suite in suites:
            totals["tests"] += int(float(suite.attrib.get("tests", "0")))
            totals["failures"] += int(float(suite.attrib.get("failures", "0")))
            totals["errors"] += int(float(suite.attrib.get("errors", "0")))
            totals["skipped"] += int(float(suite.attrib.get("skipped", "0")))
            totals["time"] += float(suite.attrib.get("time", "0") or 0)

            for case in suite.findall("testcase"):
                attempts[_case_key(case)].append(_case_status(case))

    if totals["tests"] == 0 and attempts:
        totals["tests"] = len(attempts)

    totals["passed"] = max(
        totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"],
        0,
    )

    flaky = []
    for test_name, statuses in attempts.items():
        if len(statuses) > 1 and statuses[-1] == "passed":
            flaky.append(
                {
                    "test": test_name,
                    "attempts": len(statuses),
                    "history": statuses,
                }
            )

    summary = {
        "totals": totals,
        "flaky_count": len(flaky),
        "flaky_tests": sorted(flaky, key=lambda item: item["attempts"], reverse=True),
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
        f"| Flaky (pass on retry) | {summary['flaky_count']} |",
        f"| Duration (s) | {totals['time']:.2f} |",
    ]

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
            lines.append(f"| {item['test']} | {item['attempts']} | {history} |")

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
