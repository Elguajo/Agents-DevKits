# Source note

This is an original local adaptation, not a vendored copy.

- Method inspiration: `Exploratory QA Audit` proposal package for Agents-DevKits, skill `exploratory-qa-audit`
- Upstream license: none declared; the workflow text was rewritten for this repository
- Retrieved: 2026-09-05
- Local changes: condensed the proposal's ten phases into the repository's `Use when` / `Do not use when` / `Workflow` / `Rules` / `Handoffs` / output-contract shape; moved the exhaustive variation lists into `references/exploratory-test-heuristics.md`, charter planning into `references/exploratory-charter.md`, and reproduction, severity, and report fields into `references/defect-evidence.md`; narrowed the declared ownership to discovery of unknown user-observable defects so `debugging` keeps root cause, `playwright-testing` keeps deterministic browser regression, `testing` keeps non-browser coverage, and `ux-usability-audit` keeps usability; converted the proposal's broad handoff list into handoffs plus related skills that the registry can resolve.
