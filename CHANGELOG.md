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
- A portable `affine-notion-graph-sync` integration skill for turning a Notion page URL into a verified graph in self-hosted AFFiNE without exposing tokens or deleting existing canvas state.
- Deterministic routing scenarios covering every new skill, including negative expectations that keep the two project audits request-only.
- An experimental `ux-usability-audit` owner for human-centered usability and interaction logic of a product that was actually exercised: journeys, discoverability, states, microcopy, cognitive load, and reference-guided improvement. It routes at `PROPOSE`, and its boundaries keep the structural model with `information-architecture`, artifact-level critique with `design-review`, broad rework with `redesign`, accessibility criteria with `accessibility-review`, and real user evidence with `ux-research`.
- An experimental `apple-quality-interface-refinement` owner for the preservation-first craft pass on an interface whose product and design direction already exist: current-interface reconstruction, evidence-classified findings, a prioritized refinement plan with a scope guard, and a render/critique/fix loop. It uses Apple HIG as a quality benchmark rather than a visual template, routes at `PROPOSE`, declares six progressive references, and its boundaries keep direction-changing rework with `redesign`, new art direction with `frontend-design`, and final visual evidence with `visual-qa`.
- A "Skill map" table in `README.md` and `README.ru.md` (mirroring the existing "Knowledge map") that lists every skill's `use_when` condition grouped by domain, so a reader can pick a skill without leaving the README.
- Two experimental review owners for concerns the library did not cover: `privacy-review` for whether personal or sensitive data should be collected at all, how far it travels, and how long it is kept; and `api-integration-review` for the consumed contract of an API the project does not control. Both route at `PROPOSE`. Their boundaries keep attack paths with `security-review`, durable-data health with `data-storage-review`, and failure, retry, and idempotency semantics with `reliability-review`.
- An experimental `skill-authoring` maintenance capability that decides whether a proposed capability becomes a skill, a reference inside an existing owner, registry metadata, or nothing, and then carries out the complete registry, catalog, boundary, and eval change set. It is `user`-invocation only, so it is never selected inside a repository that merely consumes the library.
- Two progressive references under existing owners instead of new skills: `production-readiness` under `release-check` for configuration, secret delivery, rollout ordering, rollback, health, and the incident path; and `success-metrics` under `product-spec` for the measurement and instrumentation a spec should define.
- Deterministic skill-library audit checks in the platform gate: duplicate ownership between skills, empty `non_goals`, self-referencing handoffs, identical trigger expressions that routing cannot separate, `trigger_values` entries no skill uses, and `model`-invocable skills that no routing scenario exercises.
- Routing scenarios for `apply-aesthetic`, `design-qa`, `figma-integration`, `playwright-testing`, `token-build`, `ux-writing`, `privacy-review`, and `api-integration-review`, so every `model`-invocable skill now has at least one positive or negative expectation.

### Changed

- Continuous integration now validates the complete portable skill library and project runtime in addition to the macOS/Codex Devkit layer.
- The debugging, code-review, testing, performance-review, refactor, release-check, security-review, solution-architecture, and feature-development skills now declare progressive references and explicit handoffs to the new specialist owners; their existing workflows, evidence rules, and output contracts are unchanged.
- `security-review`, `observability-review`, `data-storage-review`, `reliability-review`, `product-spec`, and `release-check` now declare handoffs or related links to the new privacy and API-integration owners; their existing workflows, evidence rules, and output contracts are unchanged.
- `docs/workflow-maintenance.md` now separates policy from procedure: it remains the decision path, `skill-authoring` executes it, and the checks that catch library drift are listed as gate-enforced rather than review-enforced.
- `project.py route` now derives the privacy and API-integration facts from a task description. A generic collection term such as `analytics` or `tracking` requires a personal-data subject (`personal`, `pii`, `device id`, `cookie`, `advertising id`, `ip address`, and similar) before it selects `privacy-review`, so product-analytics and issue-tracking work does not trigger a privacy review.
- `project.py route` and `project.py verify` now derive facts for change impact, durable data, migration, concurrency, reliability, and observability from the task description, using whole-word matching so that, for example, `trace` no longer counts as `race`. The two project audits stay request-only and are covered by a negative test.

## History before this changelog

Changes made before 2026-08-11 are preserved in the Git commit history. They are not retroactively assigned release versions.

## Maintenance

- Add an entry under **Unreleased** in the same change that introduces a notable repository update.
- Use the appropriate category: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, or **Security**.
- Describe the outcome for users and contributors, not the implementation detail or every file touched.
- On a release, rename **Unreleased** to a versioned heading with an ISO date and create a fresh **Unreleased** section above it.
- Do not add entries for local experiments, formatting-only edits, or unmerged work.
