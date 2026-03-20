import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _format_pass_rate(totals: dict) -> float:
    tests = int(totals.get("tests", 0) or 0)
    passed = int(totals.get("passed", 0) or 0)
    if tests <= 0:
        return 0.0
    return round((passed / tests) * 100, 2)


def _signed(value: float) -> str:
    return f"{value:+.2f}"


def _find_previous_run(runs: list[dict[str, Any]], browser: str) -> dict[str, Any] | None:
    for run in reversed(runs):
        if browser and run.get("browser") != browser:
            continue
        return run

    for run in reversed(runs):
        return run

    return None


def _trend_status(
    pass_rate_delta: float,
    flaky_delta: int,
    failed_delta: int,
    previous_run: dict[str, Any] | None,
) -> str:
    if previous_run is None:
        return "initial"

    improved = pass_rate_delta > 0 or flaky_delta < 0 or failed_delta < 0
    regressed = pass_rate_delta < 0 or flaky_delta > 0 or failed_delta > 0

    if improved and not regressed:
        return "improved"
    if regressed and not improved:
        return "regressed"
    if improved and regressed:
        return "mixed"
    return "flat"


def _build_markdown(trend: dict, max_rows: int = 10) -> str:
    runs = trend.get("runs", [])[-max_rows:]
    latest = runs[-1] if runs else None

    lines = ["## Flaky Trend", ""]

    if latest:
        status = str(latest.get("trend_status", "initial")).upper()
        lines.extend(
            [
                f"### Latest Status: {status}",
                "",
                "| Metric | Current | Delta vs Previous |",
                "| --- | ---: | ---: |",
                f"| Failed (failures + errors) | {latest.get('failed_total', 0)} | {int(latest.get('failed_total_delta', 0)):+d} |",
                f"| Flaky | {latest.get('flaky_count', 0)} | {int(latest.get('flaky_delta', 0)):+d} |",
                f"| Pass Rate (%) | {float(latest.get('pass_rate', 0.0)):.2f} | {_signed(float(latest.get('pass_rate_delta', 0.0)))} |",
                f"| Duration (s) | {float(latest.get('time', 0.0)):.2f} | {_signed(float(latest.get('time_delta', 0.0)))} |",
                "",
            ]
        )

    lines.extend(
        [
            "| Run | Browser | Failed | Flaky | Pass Rate (%) | Delta (%) | Duration (s) | Trend |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )

    for run in reversed(runs):
        run_label = f"#{run.get('run_number') or run.get('run_id', '-')}"
        lines.append(
            "| "
            f"{run_label} | "
            f"{run.get('browser', '-')} | "
            f"{run.get('failed_total', run.get('failures', 0))} | "
            f"{run.get('flaky_count', 0)} | "
            f"{float(run.get('pass_rate', 0.0)):.2f} | "
            f"{float(run.get('pass_rate_delta', 0.0)):+.2f} | "
            f"{float(run.get('time', 0.0)):.2f} | "
            f"{run.get('trend_status', 'initial')} |"
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Update flaky trend file from current summary")
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--trend-file", required=True)
    parser.add_argument("--output-json", default="")
    parser.add_argument("--output-md", default="")
    parser.add_argument("--max-runs", type=int, default=60)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-number", default="")
    parser.add_argument("--workflow", default="")
    parser.add_argument("--ref", default="")
    parser.add_argument("--sha", default="")
    parser.add_argument("--browser", default="")
    parser.add_argument("--event", default="")
    parser.add_argument("--github-summary", action="store_true")
    args = parser.parse_args()

    summary_path = Path(args.summary_json)
    trend_path = Path(args.trend_file)

    summary = _read_json(summary_path)
    totals = summary.get("totals", {})

    trend = _read_json(trend_path)
    runs = trend.get("runs", [])
    if not isinstance(runs, list):
        runs = []

    previous_run = _find_previous_run(runs, args.browser)

    passed = int(totals.get("passed", 0) or 0)
    skipped = int(totals.get("skipped", 0) or 0)
    failures = int(totals.get("failures", 0) or 0)
    errors = int(totals.get("errors", 0) or 0)
    failed_total = failures + errors

    current_pass_rate = _format_pass_rate(totals)
    current_flaky = int(summary.get("flaky_count", 0) or 0)
    current_time = float(totals.get("time", 0.0) or 0.0)

    previous_pass_rate = float(previous_run.get("pass_rate", 0.0) or 0.0) if previous_run else 0.0
    previous_flaky = int(previous_run.get("flaky_count", 0) or 0) if previous_run else 0
    previous_failed = (
        int(previous_run.get("failed_total", previous_run.get("failures", 0)) or 0)
        if previous_run
        else 0
    )
    previous_time = float(previous_run.get("time", 0.0) or 0.0) if previous_run else 0.0

    pass_rate_delta = round(current_pass_rate - previous_pass_rate, 2)
    flaky_delta = current_flaky - previous_flaky
    failed_total_delta = failed_total - previous_failed
    time_delta = round(current_time - previous_time, 2)

    run_entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": args.run_id,
        "run_number": args.run_number,
        "workflow": args.workflow,
        "ref": args.ref,
        "sha": args.sha,
        "browser": args.browser,
        "event": args.event,
        "tests": int(totals.get("tests", 0) or 0),
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "failed_total": failed_total,
        "skipped": skipped,
        "non_passed": failed_total + skipped,
        "flaky_count": current_flaky,
        "pass_rate": current_pass_rate,
        "time": current_time,
        "pass_rate_delta": pass_rate_delta,
        "flaky_delta": flaky_delta,
        "failed_total_delta": failed_total_delta,
        "time_delta": time_delta,
        "trend_status": _trend_status(
            pass_rate_delta=pass_rate_delta,
            flaky_delta=flaky_delta,
            failed_delta=failed_total_delta,
            previous_run=previous_run,
        ),
    }

    runs.append(run_entry)
    if len(runs) > args.max_runs:
        runs = runs[-args.max_runs :]

    trend_out = {"runs": runs}

    trend_path.parent.mkdir(parents=True, exist_ok=True)
    trend_path.write_text(json.dumps(trend_out, indent=2), encoding="utf-8")

    if args.output_json:
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(trend_out, indent=2), encoding="utf-8")

    markdown = _build_markdown(trend_out)
    if args.output_md:
        output_md = Path(args.output_md)
        output_md.parent.mkdir(parents=True, exist_ok=True)
        output_md.write_text(markdown, encoding="utf-8")

    if args.github_summary:
        summary_target = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_target:
            target = Path(summary_target)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as file:
                file.write(markdown)

    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
