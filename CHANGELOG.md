# Changelog

All notable repository changes are recorded here in addition to Git history. Entries describe user-visible behavior, project assets, workflows, and documentation changes; Git remains the source of exact diffs and authorship.

## [Unreleased]

### Added

- A repository-level changelog for tracking notable additions, changes, fixes, removals, and security updates.
- A validated v2 skill-routing contract with invocation, declarative triggers, capability requirements, input/output, progressive references, verification, and handoff metadata for every portable skill.
- Provider-neutral capability and ephemeral evidence contracts, deterministic routing scenario evals, and a one-command platform gate.
- A cross-platform multi-agent project runtime with version-compatible `agents-devkits.yaml`, Codex/Claude templates, safe instruction adoption, task-aware structured verification, and JSON evidence output.
- Fifteen portable UX/UI skills adapted from `plugin87/ux-ui-agent-skills`: aesthetic direction, brand foundation, tokens, components, UI code, QA/review, Figma integration, governance, image reconstruction, migration, prototypes, redesign, token builds, and UX writing. Existing accessibility and performance specialists remain the single owners of their respective reviews.
- An opt-in `project.py init --ui` profile with a concise project design brief and required visual/accessibility reviews for configured UI changes.
- Eight experimental skill owners for previously unowned concerns: change-impact analysis, durable-data review, data migration, concurrency review, reliability review, observability review, technical project audit, and interdisciplinary project audit. They route at `PROPOSE` or `ASK` until real use supports promotion.
- Twenty-one progressive `references/` protocols under the existing debugging, code-review, testing, performance, refactor, security, release, architecture, and data owners, each declared in the routing registry with the trigger that justifies loading it.
- Deterministic routing scenarios covering every new skill, including negative expectations that keep the two project audits request-only.
- A "Skill map" table in `README.md` and `README.ru.md` (mirroring the existing "Knowledge map") that lists every skill's `use_when` condition grouped by domain, so a reader can pick a skill without leaving the README.

### Changed

- Continuous integration now validates the complete portable skill library and project runtime in addition to the macOS/Codex Devkit layer.
- The debugging, code-review, testing, performance-review, refactor, release-check, security-review, solution-architecture, and feature-development skills now declare progressive references and explicit handoffs to the new specialist owners; their existing workflows, evidence rules, and output contracts are unchanged.
- `project.py route` and `project.py verify` now derive facts for change impact, durable data, migration, concurrency, reliability, and observability from the task description, using whole-word matching so that, for example, `trace` no longer counts as `race`. The two project audits stay request-only and are covered by a negative test.

## History before this changelog

Changes made before 2026-08-11 are preserved in the Git commit history. They are not retroactively assigned release versions.

## Maintenance

- Add an entry under **Unreleased** in the same change that introduces a notable repository update.
- Use the appropriate category: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, or **Security**.
- Describe the outcome for users and contributors, not the implementation detail or every file touched.
- On a release, rename **Unreleased** to a versioned heading with an ISO date and create a fresh **Unreleased** section above it.
- Do not add entries for local experiments, formatting-only edits, or unmerged work.
