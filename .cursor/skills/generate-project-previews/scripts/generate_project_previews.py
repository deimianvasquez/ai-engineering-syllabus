#!/usr/bin/env python3
"""Generate preview covers for projects and update learn.json."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote


IMAGE_MAP = {
    "command-line": "command-line.svg",
    "workflow": "workflow.svg",
    "ai-communication": "ai-communication.svg",
    "ai-web-development": "ai-web-development.svg",
    "ai-coding": "ai-coding.svg",
    "working-with-ai": "working-with-ai.svg",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate project cover previews from learn.json metadata."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Repository root path (default: current directory).",
    )
    parser.add_argument(
        "--cover-template",
        default="assets/cover/cover-template.html",
        help="Relative path from project root to cover template HTML.",
    )
    parser.add_argument(
        "--images-dir",
        default="assets/cover/images",
        help="Relative path from project root to SVG image directory.",
    )
    parser.add_argument(
        "--projects-dir",
        default="content/projects",
        help="Relative path from project root to projects directory.",
    )
    parser.add_argument(
        "--author",
        default="by 4Geeks Academy",
        help="Author subtitle shown on covers.",
    )
    parser.add_argument(
        "--preview-filename",
        default="preview.png",
        help="Filename generated inside each project's .learn folder.",
    )
    parser.add_argument(
        "--preview-key",
        default="preview",
        help="learn.json key used to store preview path.",
    )
    parser.add_argument(
        "--absolute-base-url",
        default="https://raw.githubusercontent.com/4GeeksAcademy/ai-engineering-syllabus/main",
        help="Absolute base URL used to build preview URLs.",
    )
    parser.add_argument(
        "--write-both-preview-keys",
        action="store_true",
        help="Also write the alternate preview key (preview or preview_url).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned operations without writing files.",
    )
    return parser.parse_args()


def choose_image_filename(learn_data: dict) -> str:
    technologies = " ".join(learn_data.get("technologies", []))
    title_obj = learn_data.get("title", {}) or {}
    description_obj = learn_data.get("description", {}) or {}
    title_en = title_obj.get("en", "") or title_obj.get("us", "")
    description_en = description_obj.get(
        "en", "") or description_obj.get("us", "")
    slug = learn_data.get("slug", "")
    haystack = " ".join([technologies, title_en, description_en, slug]).lower()

    if any(
        token in haystack
        for token in ["workflow", "process", "diagram", "modeling", "class diagram", "uml"]
    ):
        return IMAGE_MAP["workflow"]

    if any(
        token in haystack
        for token in ["chat", "prompt", "conversation", "api", "communication", "llm"]
    ):
        return IMAGE_MAP["ai-communication"]

    if any(token in haystack for token in ["bash", "shell", "terminal", "cli", "command line"]):
        return IMAGE_MAP["command-line"]

    if any(
        token in haystack
        for token in ["html", "css", "tailwind", "frontend", "dashboard", "web"]
    ):
        return IMAGE_MAP["ai-web-development"]

    if any(
        token in haystack
        for token in ["python", "javascript", "typescript", "coding", "code", "programming"]
    ):
        return IMAGE_MAP["ai-coding"]

    return IMAGE_MAP["working-with-ai"]


def encode_query(params: dict[str, str]) -> str:
    query_parts = []
    for key, value in params.items():
        query_parts.append(f"{quote(key, safe='')}={quote(value, safe='')}")
    return "&".join(query_parts)


def run_playwright_screenshot(page_url: str, output_file: Path, dry_run: bool) -> None:
    cmd = [
        "npx",
        "playwright",
        "screenshot",
        "--viewport-size=1024,576",
        page_url,
        str(output_file),
    ]
    if dry_run:
        print("dry_run_command", " ".join(cmd))
        return
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    template_file = root / args.cover_template
    images_dir = root / args.images_dir
    projects_dir = root / args.projects_dir

    if not template_file.exists():
        print(f"Template not found: {template_file}")
        return 1
    if not images_dir.exists():
        print(f"Images directory not found: {images_dir}")
        return 1
    if not projects_dir.exists():
        print(f"Projects directory not found: {projects_dir}")
        return 1

    learn_files = sorted(projects_dir.glob("*/learn.json"))
    if not learn_files:
        print(f"No learn.json files found in: {projects_dir}")
        return 1

    generated = 0
    updated = 0
    skipped = 0

    for learn_file in learn_files:
        with learn_file.open("r", encoding="utf-8") as f:
            learn_data = json.load(f)

        title_obj = learn_data.get("title", {}) or {}
        title_en = title_obj.get("en") or title_obj.get("us")
        if not title_en:
            print("skip_missing_title_en", str(learn_file))
            skipped += 1
            continue

        image_name = choose_image_filename(learn_data)
        image_path = images_dir / image_name
        if not image_path.exists():
            print("skip_missing_image", str(image_path))
            skipped += 1
            continue

        project_dir = learn_file.parent
        learn_dir = project_dir / ".learn"
        output_file = learn_dir / args.preview_filename
        preview_rel_path = str(Path(".learn") / args.preview_filename)
        project_rel_dir = project_dir.relative_to(root).as_posix()
        base_url = args.absolute_base_url.rstrip("/")
        preview_absolute_url = f"{base_url}/{project_rel_dir}/{preview_rel_path}"

        query = encode_query(
            {
                "title": title_en,
                "author": args.author,
                "image": f"./images/{image_name}",
            }
        )
        page_url = f"file://{template_file}?{query}"

        print("generate_preview", str(project_dir), "using_image", image_name)
        if not args.dry_run:
            learn_dir.mkdir(parents=True, exist_ok=True)
        run_playwright_screenshot(page_url, output_file, args.dry_run)
        generated += 1

        learn_data[args.preview_key] = preview_absolute_url
        if args.write_both_preview_keys:
            alternate = "preview" if args.preview_key == "preview_url" else "preview_url"
            learn_data[alternate] = preview_absolute_url

        if args.dry_run:
            print("dry_run_update_json", str(learn_file),
                  args.preview_key, preview_absolute_url)
        else:
            with learn_file.open("w", encoding="utf-8") as f:
                json.dump(learn_data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        updated += 1

    print("summary_generated", generated)
    print("summary_updated", updated)
    print("summary_skipped", skipped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
