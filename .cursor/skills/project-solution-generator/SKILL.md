---
name: project-solution-file
description: Define and maintain a canonical solution file per project under .learn/solution and link it from the project's learn.json via a solution attribute. Use when creating or updating project solutions so students and LLMs can compare their work against a reference implementation.
---

# Project Solution File

## Purpose

Use this skill to ensure each project has one canonical reference solution under `.learn/solution/`, documented with a README, and linked from `learn.json` using `solution`.

This enables:

- Students to compare their submission against a clear reference, including what a correct deliverable looks like in practice.
- LLM-based evaluators to contrast submissions with a canonical solution and expected outputs.

## When to use

Use this skill whenever:

- You create a new evaluable project (milestones, guided projects, collaborative projects).
- You add or update a reference solution for an existing project.
- You audit whether a project has a valid solution link in `learn.json`.

## Required conventions

1. **Solution location**
   - Keep all reference solution files in `.learn/solution/` at project root.
   - Example: `content/projects/<project-slug>/.learn/solution/`

2. **Mandatory README**
   - Always include `.learn/solution/README.md` (or `README.html` only if explicitly needed).
   - The README is the canonical entry point and must explain:
     - Solution structure and purpose of each file
     - Key implementation decisions and trade-offs
     - How solution files connect and interact
     - **Indicative examples** of what a correct deliverable looks like — e.g., expected output samples, sample API responses, annotated screenshots, or representative code snippets that illustrate the expected behavior. These help students self-assess and give LLM evaluators concrete anchors.
     - **Solution architecture** when the project involves multiple services or components (e.g., message queues, background workers, agent orchestration, multi-service pipelines, LLM tool-use flows). In these cases include:
       - A brief description or ASCII/Mermaid diagram of how services interact
       - Data flow between components (inputs, outputs, events)
       - Component responsibilities and boundaries
       - Any relevant deployment or infrastructure considerations

3. **`learn.json` linkage**
   - Add/update `"solution"` in `learn.json`.
   - The value must be the **full URL in the repository** pointing to `.learn/solution/README.*` (not a relative path).
   - Example: `"solution": "https://github.com/ORG/REPO/blob/BRANCH/path/to/project/.learn/solution/README.md"`
   - Use the repository's canonical pattern consistently.

4. **One canonical solution per project**
   - Avoid multiple competing reference implementations.
   - If there are auxiliary files, reference them from `.learn/solution/README.*`.
   - If you find multiple `solution` attributes in `learn.json`, unify them.

5. **Language**
   - Human-readable explanatory content inside the solution (README/comments/documentation) must always be in English, regardless of the project's README or UI language.
   - Code identifiers and literals follow the project's requirements.

## Allowed solution formats

### 1) HTML/CSS/JS solution

Use when the deliverable is a web interface, layout, or page.

Requirements:

- Semantic HTML structure (`header`, `main`, `section`, `footer`, `article`, etc.) when applicable.
- Include all elements/attributes specifically assessed in the project (e.g., schema.org markup, accessibility metadata, headings hierarchy, `lang` attribute, alt text).
- Keep non-obvious comments only — don't narrate every line.
- README should include a screenshot or description of the expected rendered result so students know what "done" looks like.

Recommended files in `.learn/solution/`:

- `README.md` (mandatory)
- `solution.html`
- `styles.css`
- `script.js`

### 2) Source-code solution (`.py`, `.js`, `.ts`, etc.)

Use when the deliverable is programming logic, scripts, modules, or backend code (automation, data processing, CLI tools, backend modules, etc.).

Supported file types include, but are not limited to: `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.sh`.

Requirements:

- Complete, readable implementation covering expected grading criteria.
- Uses data structures, algorithms, or patterns that serve as model examples for students.
- Reasonable validations/error handling where relevant.
- Optional helper utilities (e.g., under `if __name__ == "__main__":` in Python).
- README should include sample inputs and their expected outputs (e.g., function call → return value, CLI invocation → stdout) so students and evaluators can verify behavior without running code.

For projects with multiple interacting services or background processing:

- Document the architecture clearly: which service does what, how they communicate (HTTP, queues, events), and the expected data flow.
- Include a Mermaid diagram or ASCII flow in the README when component interaction is non-trivial.

Recommended files in `.learn/solution/`:

- `README.md` (mandatory)
- `solution.py` / `solution.ts` / `solution.js` (or split files like `main.ts`, `utils.ts`)
- Architecture diagram (inline in README or as a separate `architecture.md`) when applicable

### 3) Explanatory solution (`.md`)

Use when there is no single valid implementation and the key is evaluating criteria or approach.

Should include:

- Expected visual, structural, and code criteria.
- Recommended algorithms, data structures, or design patterns.
- Small snippets for key points (a full line-by-line solution is not necessary).
- At least one concrete example demonstrating what an acceptable deliverable looks like vs. a common mistake or incomplete attempt.
- For complex systems, a description of the expected architecture (components, responsibilities, interactions) even if no single implementation is prescribed.

Recommended files in `.learn/solution/`:

- `README.md` (mandatory)
- Optional auxiliary example files

## Workflow (create/update)

1. **Identify project root**
   - Locate project folder under `content/projects/...`.

2. **Ensure `.learn/solution/` exists**
   - Create `.learn/` and `.learn/solution/` if missing.

3. **Choose format**
   - Always include `.learn/solution/README.md`.
   - If the main deliverable is a web page or UI → add `solution.html` (and CSS/JS as needed).
   - If a concrete script is required → add `solution.py`, `solution.ts`, etc.
   - If the key is to describe criteria or patterns → document in `README.md` with optional partial examples.

4. **Create/update solution files**
   - Keep all solution files inside `.learn/solution/`.
   - Ensure README explains structure, key decisions, and how files connect.
   - Include indicative examples (sample outputs, screenshots, annotated snippets) that make the expected result concrete.
   - If the project involves multiple services, queues, agent pipelines, or background processing, add an architecture section to the README.

5. **Link in `learn.json`**
   - Add/update `"solution"` with the full repository URL to `README.*`.
   - Ensure no duplicated or conflicting `solution` entries.

6. **Consistency review**
   - Verify project README/context and solution are aligned.
   - Ensure no missing evaluated requirements in the reference solution.
   - If the project has multiple language versions (`README.md`, `README.es.md`), confirm the solution is valid for all.
   - Confirm that indicative examples match the actual solution behavior.
   - Confirm that architecture documentation (if applicable) reflects the actual component design.

## LLM and student usage guidance

- **Students**: use as a comparison reference, not copy-paste output. Pay attention to indicative examples to self-assess whether your deliverable matches the expected behavior. Ask yourself: "Am I covering all the key points in the solution?" and "Is my structure reasonably similar, even if the code isn't identical?"
- **LLM evaluators**: treat the solution as the golden reference for criteria coverage. Use indicative examples as concrete anchors when assessing whether a submission meets expectations. For multi-service projects, use the architecture description to verify that the student's design choices are coherent.

When evaluating:

1. Read project instructions/context and `learn.json`.
2. Read `.learn/solution/README.*` as the primary reference.
3. Compare submission against required aspects from the reference solution.
4. Use indicative examples to assess correctness of outputs or behavior.
5. For architecture-based projects, verify component responsibilities, data flow, and service boundaries match the described solution.

## Quick checklist

- [ ] Project has `.learn/` and `learn.json`.
- [ ] Project has `.learn/solution/`.
- [ ] `.learn/solution/README.md` exists and is clear.
- [ ] All solution files are inside `.learn/solution/`.
- [ ] `learn.json` includes a valid `"solution"` attribute with a full repository URL pointing to `README.*`.
- [ ] Solution covers all evaluated project requirements.
- [ ] README includes indicative examples of correct deliverables (sample outputs, snippets, screenshots).
- [ ] README includes architecture documentation if the project involves multiple services, queues, agent orchestration, or background processing.
- [ ] All human-readable content in the solution (README, comments, prose) is in English.
