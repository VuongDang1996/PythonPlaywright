import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _format_pass_rate(totals: dict) -> float:
    tests = totals.get("tests", 0) or 0
    passed = totals.get("passed", 0) or 0
    if tests <= 0:
        return 0.0
    return round((passed / tests) * 100, 2)


def _build_markdown(trend: dict, max_rows: int = 10) -> str:
    runs = trend.get("runs", [])[-max_rows:]
    lines = [
        "## Flaky Trend",
        "",
        "| Run | Browser | Failed | Flaky | Pass Rate (%) | Duration (s) |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for run in reversed(runs):
        run_label = f"#{run.get('run_number') or run.get('run_id', '-') }"
        lines.append(
            "| "
            f"{run_label} | "
            f"{run.get('browser', '-')} | "
            f"{run.get('failures', 0)} | "
            f"{run.get('flaky_count', 0)} | "
            f"{run.get('pass_rate', 0.0):.2f} | "
            f"{run.get('time', 0.0):.2f} |"
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
    args = parser.parse_args()

    summary_path = Path(args.summary_json)
    trend_path = Path(args.trend_file)

    summary = _read_json(summary_path)
    totals = summary.get("totals", {})

    trend = _read_json(trend_path)
    runs = trend.get("runs", [])
    if not isinstance(runs, list):
        runs = []

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
        "passed": int(totals.get("passed", 0) or 0),
        "failures": int(totals.get("failures", 0) or 0) + int(totals.get("errors", 0) or 0),
        "skipped": int(totals.get("skipped", 0) or 0),
        "flaky_count": int(summary.get("flaky_count", 0) or 0),
        "pass_rate": _format_pass_rate(totals),
        "time": float(totals.get("time", 0.0) or 0.0),
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

    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
