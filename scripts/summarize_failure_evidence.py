import argparse
import json
import os
from pathlib import Path


def _collect_files(path: Path, extensions: set[str]) -> list[Path]:
    if not path.exists() or not path.is_dir():
        return []

    files = [
        file_path
        for file_path in path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in extensions
    ]
    return sorted(files)


def _to_rel(paths: list[Path], base: Path) -> list[str]:
    rel = []
    for path in paths:
        try:
            rel.append(str(path.relative_to(base)).replace("\\", "/"))
        except ValueError:
            rel.append(str(path).replace("\\", "/"))
    return rel


def build_summary(artifacts_dir: Path, videos_dir: Path, project_root: Path, sample_limit: int) -> dict:
    screenshots = _collect_files(artifacts_dir, {".png", ".jpg", ".jpeg"})
    traces = _collect_files(artifacts_dir, {".zip"})
    console_logs = _collect_files(artifacts_dir, {".log", ".txt"})
    videos = _collect_files(videos_dir, {".webm", ".mp4", ".mov"})

    summary = {
        "counts": {
            "screenshots": len(screenshots),
            "traces": len(traces),
            "console_logs": len(console_logs),
            "videos": len(videos),
            "total": len(screenshots) + len(traces) + len(console_logs) + len(videos),
        },
        "paths": {
            "artifacts_dir": str(artifacts_dir).replace("\\", "/"),
            "videos_dir": str(videos_dir).replace("\\", "/"),
        },
        "samples": {
            "screenshots": _to_rel(screenshots[:sample_limit], project_root),
            "traces": _to_rel(traces[:sample_limit], project_root),
            "console_logs": _to_rel(console_logs[:sample_limit], project_root),
            "videos": _to_rel(videos[:sample_limit], project_root),
        },
    }
    return summary


def to_markdown(summary: dict, title: str) -> str:
    counts = summary["counts"]
    lines = [
        f"## {title}",
        "",
        "| Evidence Type | Count |",
        "| --- | ---: |",
        f"| Screenshots | {counts['screenshots']} |",
        f"| Traces | {counts['traces']} |",
        f"| Console Logs | {counts['console_logs']} |",
        f"| Videos | {counts['videos']} |",
        f"| Total Files | {counts['total']} |",
        "",
        f"Artifacts dir: {summary['paths']['artifacts_dir']}",
        f"Videos dir: {summary['paths']['videos_dir']}",
    ]

    for section_title, key in (
        ("Screenshot Samples", "screenshots"),
        ("Trace Samples", "traces"),
        ("Video Samples", "videos"),
        ("Console Log Samples", "console_logs"),
    ):
        samples = summary["samples"].get(key, [])
        if not samples:
            continue

        lines.extend(["", f"### {section_title}", ""])
        for sample in samples:
            lines.append(f"- {sample}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize failure evidence artifacts")
    parser.add_argument("--artifacts-dir", default="test-results/artifacts")
    parser.add_argument("--videos-dir", default="test-results/videos")
    parser.add_argument("--output-json", default="")
    parser.add_argument("--output-md", default="")
    parser.add_argument("--title", default="Failure Evidence Summary")
    parser.add_argument("--sample-limit", type=int, default=10)
    parser.add_argument("--github-summary", action="store_true")
    args = parser.parse_args()

    project_root = Path.cwd()
    artifacts_dir = Path(args.artifacts_dir)
    videos_dir = Path(args.videos_dir)

    summary = build_summary(
        artifacts_dir=artifacts_dir,
        videos_dir=videos_dir,
        project_root=project_root,
        sample_limit=max(args.sample_limit, 1),
    )

    markdown = to_markdown(summary, args.title)

    if args.output_json:
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

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
