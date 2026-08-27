---
name: design-qa
description: Plan or run a layered design-quality check across token use, accessibility, visual states, responsive behavior, and project-specific automated gates.
---

# Design QA

Use this skill to coordinate UI quality evidence. It does not replace `visual-qa`, `accessibility-review`, browser testing, or project verification commands.

## Workflow

1. Define the rendered scope: pages, components, themes, target viewports, state combinations, and reference source.
2. Separate objective checks (build, token validation, contrast, lint, browser assertions) from expert reviews (visual quality, usability, accessibility judgment).
3. Run only checks declared by the project or already available in its toolchain. If a desired check is unavailable, report `unavailable` with the reason.
4. Use `visual-qa` for reference fidelity, `accessibility-review` for accessibility-specific findings, and `playwright-testing` for browser behavior.
5. Summarize observed results in the evidence format required by `release-check`.

Read [evidence-matrix.md](references/evidence-matrix.md) when defining a QA scope.

## Completion evidence

Return the scoped matrix, executed checks and results, expert-review findings, unavailable coverage, and remaining release risks.
