import argparse
import hashlib
import json
import os
import shutil
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


def _unique_dest(dest_dir: Path, source_name: str, source_path: Path) -> Path:
    candidate = dest_dir / source_name
    if not candidate.exists():
        return candidate

    stem = Path(source_name).stem
    suffix = Path(source_name).suffix
    digest = hashlib.sha1(str(source_path).encode("utf-8")).hexdigest()[:10]
    return dest_dir / f"{stem}_{digest}{suffix}"


def _copy_group(sources: list[Path], dest_dir: Path) -> list[dict[str, str]]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, str]] = []

    for source in sources:
        destination = _unique_dest(dest_dir, source.name, source)
        shutil.copy2(source, destination)
        copied.append(
            {
                "source": str(source).replace("\\", "/"),
                "bundle": str(destination).replace("\\", "/"),
            }
        )

    return copied


def _markdown_manifest(bundle_dir: Path, summary: dict) -> str:
    counts = summary["counts"]
    lines = [
        "# Failure Evidence Bundle",
        "",
        "This bundle is structured to make downloaded artifacts easier to inspect.",
        "",
        "| Type | Count | Folder |",
        "| --- | ---: | --- |",
        f"| Screenshots | {counts['screenshots']} | screenshots/ |",
        f"| Traces | {counts['traces']} | traces/ |",
        f"| Console Logs | {counts['console_logs']} | console-logs/ |",
        f"| Videos | {counts['videos']} | videos/ |",
        f"| Total Files | {counts['total_files']} | . |",
        "",
        "Metadata:",
        "- metadata/manifest.json",
    ]

    return "\n".join(lines) + "\n"


def _summary_markdown(summary: dict, title: str) -> str:
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
        f"| Total Files | {counts['total_files']} |",
        "",
        f"Bundle dir: {summary['bundle_dir']}",
        "",
        "Download and open the failure artifact zip. Then open:",
        "- screenshots/ for images",
        "- videos/ for .webm files",
        "- traces/ for Playwright trace zip files",
        "- console-logs/ for browser console output",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare clean failure evidence bundle")
    parser.add_argument("--artifacts-dir", default="test-results/artifacts")
    parser.add_argument("--videos-dir", default="test-results/videos")
    parser.add_argument("--bundle-dir", default="test-results/failure-evidence")
    parser.add_argument("--output-json", default="")
    parser.add_argument("--output-md", default="")
    parser.add_argument("--title", default="Failure Evidence Bundle")
    parser.add_argument("--github-summary", action="store_true")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    videos_dir = Path(args.videos_dir)
    bundle_dir = Path(args.bundle_dir)

    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)

    screenshots = _collect_files(artifacts_dir, {".png", ".jpg", ".jpeg"})
    traces = _collect_files(artifacts_dir, {".zip"})
    console_logs = _collect_files(artifacts_dir, {".log", ".txt"})
    videos = _collect_files(videos_dir, {".webm", ".mp4", ".mov"})

    copied_screenshots = _copy_group(screenshots, bundle_dir / "screenshots")
    copied_traces = _copy_group(traces, bundle_dir / "traces")
    copied_logs = _copy_group(console_logs, bundle_dir / "console-logs")
    copied_videos = _copy_group(videos, bundle_dir / "videos")

    manifest = {
        "bundle_dir": str(bundle_dir).replace("\\", "/"),
        "source": {
            "artifacts_dir": str(artifacts_dir).replace("\\", "/"),
            "videos_dir": str(videos_dir).replace("\\", "/"),
        },
        "counts": {
            "screenshots": len(copied_screenshots),
            "traces": len(copied_traces),
            "console_logs": len(copied_logs),
            "videos": len(copied_videos),
            "total_files": len(copied_screenshots)
            + len(copied_traces)
            + len(copied_logs)
            + len(copied_videos),
        },
        "files": {
            "screenshots": copied_screenshots,
            "traces": copied_traces,
            "console_logs": copied_logs,
            "videos": copied_videos,
        },
    }

    metadata_dir = bundle_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = metadata_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    readme_path = bundle_dir / "README.md"
    readme_path.write_text(_markdown_manifest(bundle_dir, manifest), encoding="utf-8")

    markdown = _summary_markdown(manifest, args.title)

    if args.output_json:
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

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
