#!/usr/bin/env python3
"""Orchestrate project scaffolding from one or two README files."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create/update a project from README source files."
    )
    parser.add_argument("--repo-root", default=".",
                        help="Repository root path.")
    parser.add_argument("--target-slug", required=True,
                        help="Target project slug.")
    parser.add_argument(
        "--source-readme",
        required=True,
        help="Path to source README (README.md or equivalent).",
    )
    parser.add_argument(
        "--source-readme-es",
        default="",
        help="Optional path to Spanish README source.",
    )
    parser.add_argument(
        "--template-url",
        default="https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo",
        help="template_url value for learn.json",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        clean = line.strip()
        if clean.startswith("# "):
            return clean[2:].strip()
    return "Project"


def build_fallback_description(title: str, language: str) -> str:
    if language == "es":
        return f"Completa el proyecto {title} siguiendo las instrucciones del README."
    return f"Complete the {title} project following the README instructions."


def infer_spanish_title(title_en: str) -> str:
    return title_en


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    projects_root = repo_root / "content" / "projects"
    target_dir = projects_root / args.target_slug
    source_readme = Path(args.source_readme).resolve()
    source_readme_es = Path(args.source_readme_es).resolve(
    ) if args.source_readme_es else None

    if not source_readme.exists():
        raise FileNotFoundError(f"Missing source readme: {source_readme}")

    target_dir.mkdir(parents=True, exist_ok=True)
    learn_dir = target_dir / ".learn"
    solution_dir = learn_dir / "solution"
    solution_dir.mkdir(parents=True, exist_ok=True)

    source_name = source_readme.name.lower()
    source_content = read_text(source_readme)

    if source_name.startswith("readme.es"):
        write_text(target_dir / "README.es.md", source_content)
    else:
        write_text(target_dir / "README.md", source_content)

    if source_readme_es and source_readme_es.exists():
        write_text(target_dir / "README.es.md", read_text(source_readme_es))

    if not (target_dir / "README.md").exists():
        # Fallback only; intended to be replaced by proper translation workflow.
        write_text(target_dir / "README.md", source_content)
    if not (target_dir / "README.es.md").exists():
        write_text(target_dir / "README.es.md", source_content)

    readme_en = read_text(target_dir / "README.md")
    readme_es = read_text(target_dir / "README.es.md")
    title_en = first_heading(readme_en)
    title_es = first_heading(readme_es) or infer_spanish_title(title_en)

    learn_json_path = target_dir / "learn.json"
    if learn_json_path.exists():
        learn_data = json.loads(read_text(learn_json_path))
    else:
        learn_data = {}

    base_project_url = (
        "https://github.com/4GeeksAcademy/ai-engineering-syllabus/tree/main/content/projects/"
        f"{args.target_slug}"
    )
    base_solution_url = (
        "https://github.com/4GeeksAcademy/ai-engineering-syllabus/blob/main/content/projects/"
        f"{args.target_slug}/.learn/solution/README.md"
    )
    base_preview_url = (
        "https://raw.githubusercontent.com/4GeeksAcademy/ai-engineering-syllabus/main/content/projects/"
        f"{args.target_slug}/.learn/preview.png"
    )

    learn_data["gitpod"] = learn_data.get("gitpod", True)
    learn_data["title"] = {
        "en": title_en,
        "es": title_es,
    }
    description = learn_data.get("description", {})
    learn_data["description"] = {
        "en": description.get("en") if isinstance(description, dict) and description.get("en") else build_fallback_description(title_en, "en"),
        "es": description.get("es") if isinstance(description, dict) and description.get("es") else build_fallback_description(title_es, "es"),
    }
    learn_data["status"] = learn_data.get("status", "draft")
    learn_data["template_url"] = learn_data.get(
        "template_url", args.template_url)
    learn_data["slug"] = args.target_slug
    learn_data["difficulty"] = learn_data.get("difficulty", "intermediate")
    learn_data["duration"] = learn_data.get("duration", 2)
    learn_data["technologies"] = learn_data.get(
        "technologies",
        ["architecture", "backend-design", "fastapi", "technical-documentation"],
    )
    learn_data["translations"] = ["es", "en"]
    learn_data["projectType"] = "project"
    learn_data["batch"] = learn_data.get(
        "batch", "https://breathecode.herokuapp.com/v1/assignment/me/telemetry?asset_id="
    )
    learn_data["solution"] = base_solution_url
    learn_data["preview"] = base_preview_url
    if "preview_url" in learn_data:
        del learn_data["preview_url"]

    write_text(learn_json_path, json.dumps(
        learn_data, indent=2, ensure_ascii=False) + "\n")

    solution_readme = solution_dir / "README.md"
    if not solution_readme.exists():
        write_text(
            solution_readme,
            (
                f"# {title_en} - Reference Solution\n\n"
                "## Purpose\n\n"
                "This solution documents what a complete submission should contain.\n\n"
                "## Expected Deliverable\n\n"
                "- A complete response aligned with all checklist items from the project README.\n"
                "- Clear architectural reasoning, module boundaries, and risk analysis.\n"
                "- Output quality consistent with evaluation criteria.\n\n"
                "## Validation Notes\n\n"
                "- Compare your submission against the README rubric.\n"
                "- Ensure scope, structure, and decisions are explicit and justified.\n"
            ),
        )

    social_script = (
        repo_root
        / ".cursor"
        / "skills"
        / "generate-project-social-sharing"
        / "scripts"
        / "generate_project_social_assets.py"
    )
    if social_script.exists():
        subprocess.run(
            [
                "python3",
                str(social_script),
                "--project-root",
                str(repo_root),
                "--slug",
                args.target_slug,
                "--sharing-link-template",
                "https://github.com/4GeeksAcademy/ai-engineering-syllabus/tree/main/content/projects/{slug}",
            ],
            check=True,
        )

    print("target_dir", str(target_dir))
    print("project_url", base_project_url)
    print("status", "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
