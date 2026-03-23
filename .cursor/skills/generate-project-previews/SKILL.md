---
name: generate-project-previews
description: Generate project preview covers for ai-engineering-syllabus projects using the shared HTML template, select a contextual illustration, save the PNG into each project's .learn folder, and update learn.json preview fields. Use when asked to create, refresh, or batch-generate project preview images from learn.json metadata.
---

# Generate Project Previews

## Purpose

Automates preview generation for projects in `content/projects`:

1. Reads each `learn.json`
2. Uses English title (`title.en`) as cover title
3. Selects an image from `assets/cover/images` based on project metadata
4. Generates `preview.png` in the project `.learn` folder
5. Updates `learn.json` preview reference

## Run

From repository root:

```bash
python3 .cursor/skills/generate-project-previews/scripts/generate_project_previews.py
```

Optional flags:

```bash
python3 .cursor/skills/generate-project-previews/scripts/generate_project_previews.py \
  --project-root . \
  --author "by 4Geeks Academy" \
  --preview-filename "preview.png" \
  --preview-key "preview" \
  --absolute-base-url "https://raw.githubusercontent.com/4GeeksAcademy/ai-engineering-syllabus/main" \
  --write-both-preview-keys
```

## Defaults and assumptions

- Cover template path: `assets/cover/cover-template.html`
- Images path: `assets/cover/images`
- Projects path: `content/projects`
- Output image path per project: `.learn/preview.png`
- `learn.json` key updated by default: `preview`
- `preview` is always written as absolute URL based on `--absolute-base-url`
- With `--write-both-preview-keys`, it updates both `preview` and `preview_url`
- English title fallback supports `title.us` when `title.en` is missing

## Image selection heuristic

The script picks an image using `technologies`, `slug`, `title.en`, and `description.en`:

- `command-line.svg` for terminal/CLI/bash topics
- `workflow.svg` for process/modeling/diagram topics
- `ai-communication.svg` for chat/prompt/API communication topics
- `ai-web-development.svg` for web/frontend HTML/CSS/Tailwind topics
- `ai-coding.svg` for coding/programming implementation topics
- `working-with-ai.svg` fallback

## Validation checklist

- Confirm `npx playwright` is available
- Confirm `assets/cover/cover-template.html` exists
- Confirm images exist in `assets/cover/images`
- Verify at least one generated image and updated `learn.json`
