# Company financial dashboard context project - Reference solution

This README defines what a correct reference delivery should include for the **"Company financial dashboard context project"**.

The goal is not to rebuild the app. The goal is to produce a reliable repository handover package based on evidence from the codebase.

## Expected deliverables

A valid solution should include all of the following:

- A validated project summary generated with AI and corrected against the real repository.
- A commit history that separates each major phase into an individual commit.
- A documented set of repository rules under `.agents/rules`.
- A `memory-bank` directory with clear project memory artifacts.

## Phase 1 - Understanding and verification

The solution should demonstrate:

- Fork and local setup of `ai-eng-financial-dashboard-context-project`.
- Inspection of the repository structure (frontend, backend, key config files, and runtime flow).
- An AI-generated summary.
- A verification pass where the generated content is read and checked against what was actually understood from the project.
- Corrections to the summary where mismatches are found.

## Phase 2 - Good and bad practices analysis

The analysis should contain concrete findings, not generic statements.

Minimum expected:

- At least 5 good practices observed in the repository.
- At least 5 bad practices or risks observed in the repository.
- Findings grouped by category (for example: architecture, naming, testing, docs, operational workflow).
- Rule proposals that connect directly to those findings.

## Phase 3 - Rules implementation under `.agents/rules`

A reference-quality solution should:

- Create `.agents/rules` if missing.
- Add rule files with explicit purpose and practical scope.
- Use naming that makes each rule easy to discover and apply.
- Validate each rule against a real project task (for example: making documentation changes, creating commits, updating backend routes, or changing frontend behavior).
- Refine rules that are too broad, ambiguous, or disconnected from reality.

## Phase 4 - `memory-bank` generation

The `memory-bank` folder should include at least:

- `product-overview.md` (what the repository delivers and for whom).
- `tech-stack.md` (frameworks, languages, execution model, tooling, and key dependencies).
- `current-status.md` (what is implemented, known limitations, and next priorities).

Quality expectations:

- Statements should be traceable to the repository.
- No invented roadmap or unsupported product claims.
- Clear and maintainable writing style for future contributors.

## Validation checklist

Use this checklist to review submissions:

- [ ] AI summary exists and was verified against repository reality.
- [ ] Generated content was explicitly reviewed and aligned with student understanding.
- [ ] Corrections were applied when generated content was inaccurate or incomplete.
- [ ] Commits are split by phase (not a single bundled commit).
- [ ] Good and bad practices include concrete evidence.
- [ ] `.agents/rules` exists with actionable, project-specific rules.
- [ ] Rules were validated with real repository workflows.
- [ ] `memory-bank` exists and includes product, stack, and current-status documents.
- [ ] Documentation is clear, specific, and maintainable.

## Notes for reviewers

- Styling changes and feature expansion are optional and should not be the evaluation focus.
- Prioritize evidence quality, rule applicability, and long-term maintainability artifacts.
