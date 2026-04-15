# Enhacing development with agent skills - Financial dashboard — Reference solution

This README defines what a correct reference delivery should include for the **Enhacing development with agent skills - Financial dashboard**.

The goal is not to rebuild the dashboard. The goal is **targeted improvements** driven by agent skills, plus a transferable custom skill and updated project memory.

## Expected deliverables

A valid solution should include all of the following:

- Branch `feature/agent-skills` (or equivalent) with commits that map to skill applications where possible.
- Measurable accessibility improvements aligned with the `accessibility` skill (keyboard use, `aria-*`, `alt`, contrast).
- Deployment-oriented React/Next.js improvements aligned with `vercel-react-best-practices` (`next/image`, metadata API, reduced layout shift, clean build).
- Evidence of exploring the ecosystem: at least two `npx skills find <topic>` explorations and **at least one additional** applied skill with a short written justification (PR comment, commit message, or `memory-bank`).
- A **custom skill file** under `.skills/` with objective, inputs, outputs, and acceptance criteria specific to this financial dashboard.
- Updated `memory-bank/progress.md` (or equivalent) describing skills used, changes made, and the authored skill.

## Phase 1 — Load and apply required skills

The solution should demonstrate:

- Discovery via `npx skills find accessibility` and `npx skills find vercel-react-best-practices` before loading them into the agent.
- Agent-led audit and fixes traceable to those skills (not unrelated refactors).

## Phase 2 — Ecosystem exploration

Minimum expected:

- At least two topic searches with `npx skills find` relevant to the project (e.g. performance, seo, forms, typescript).
- At least one extra skill installed or applied beyond the two required, with justification.

## Phase 3 — Author a project-specific skill

The custom skill should:

- Address a gap not covered by off-the-shelf skills (naming, data formatting, dashboard conventions, API usage patterns, etc.).
- Be short, precise, and verifiable — not generic boilerplate.

## Phase 4 — Memory bank and submission

- `memory-bank` reflects the session accurately.
- Pull request opened against `main` with a clear description linking changes to skills.

## Validation checklist

Use this checklist to review submissions:

- [ ] `accessibility` skill was applied; keyboard navigation and assistive-tech basics hold up in manual checks.
- [ ] `vercel-react-best-practices` skill was applied; `npm run build` succeeds without new unjustified warnings.
- [ ] At least two `npx skills find` topic searches were performed; at least one extra skill was applied with justification.
- [ ] `.skills/` contains a well-structured custom skill with project-specific guidance.
- [ ] Memory bank updated; branch/PR workflow followed.
- [ ] No full-dashboard rewrite; changes remain traceable to skill instructions.

## Notes for reviewers

- Prefer evidence (PR description, commit messages, memory bank) over volume of code churn.
- The custom skill should be **specific**; penalize copy-pasted generic checklists disguised as a skill.
