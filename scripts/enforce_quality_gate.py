import argparse
import json
import os
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _append_summary(lines: list[str]) -> None:
    summary_target = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if not summary_target:
        return

    target = Path(summary_target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def _write_markdown(path_value: str, lines: list[str]) -> None:
    if not path_value:
        return

    path = Path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Enforce CI quality thresholds")
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--trend-json", default="")
    parser.add_argument("--min-pass-rate", type=float, default=95.0)
    parser.add_argument("--max-failed-total", type=int, default=0)
    parser.add_argument("--max-flaky", type=int, default=5)
    parser.add_argument("--enabled", default="false")
    parser.add_argument("--output-md", default="")
    args = parser.parse_args()

    enabled = str(args.enabled).strip().lower() in {"1", "true", "yes", "on"}
    if not enabled:
        lines = [
            "## Quality Gate",
            "",
            "Status: SKIPPED (gate is disabled)",
        ]
        _append_summary(lines)
        _write_markdown(args.output_md, lines)
        print("Quality gate skipped: disabled")
        return 0

    summary = _read_json(Path(args.summary_json))
    trend = _read_json(Path(args.trend_json)) if args.trend_json else {}

    totals = summary.get("totals", {})
    pass_rate = float(totals.get("pass_rate", 0.0) or 0.0)
    failed_total = int(totals.get("failures", 0) or 0) + int(totals.get("errors", 0) or 0)
    flaky_count = int(summary.get("flaky_count", 0) or 0)

    if trend and isinstance(trend.get("runs"), list) and trend["runs"]:
        latest = trend["runs"][-1]
        flaky_count = int(latest.get("flaky_count", flaky_count) or 0)

    violations: list[str] = []
    if pass_rate < args.min_pass_rate:
        violations.append(
            f"Pass rate below threshold: {pass_rate:.2f}% < {args.min_pass_rate:.2f}%"
        )
    if failed_total > args.max_failed_total:
        violations.append(
            f"Failed total above threshold: {failed_total} > {args.max_failed_total}"
        )
    if flaky_count > args.max_flaky:
        violations.append(f"Flaky count above threshold: {flaky_count} > {args.max_flaky}")

    lines = [
        "## Quality Gate",
        "",
        f"Configured thresholds: pass_rate >= {args.min_pass_rate:.2f}%, failed_total <= {args.max_failed_total}, flaky <= {args.max_flaky}",
        f"Measured metrics: pass_rate = {pass_rate:.2f}%, failed_total = {failed_total}, flaky = {flaky_count}",
        "",
    ]

    if violations:
        lines.append("Status: FAILED")
        lines.append("")
        lines.append("Violations:")
        for violation in violations:
            lines.append(f"- {violation}")
        _append_summary(lines)
        _write_markdown(args.output_md, lines)
        print("Quality gate failed")
        for violation in violations:
            print(f"- {violation}")
        return 1

    lines.append("Status: PASSED")
    _append_summary(lines)
    _write_markdown(args.output_md, lines)
    print("Quality gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
