---
name: token-build
description: Transform a validated design-token source of truth into platform-specific theme artifacts while preserving aliases, themes, reproducibility, and change detection.
---

# Token Build

Use this skill to design or operate a token build pipeline. Do not introduce a new production dependency or rewrite a project's build system without an explicit implementation decision.

## Workflow

1. Identify the token source format, target platforms, existing build tooling, generated-file policy, and theme requirements.
2. Define deterministic transformations for semantic and component roles. Keep primitives internal unless a platform explicitly requires them.
3. Generate only the targets requested by the project, such as CSS variables, Tailwind theme values, typed code, iOS resources, or Android/Compose values.
4. Add or use validation that detects malformed tokens, unresolved aliases, stale generated output, and contrast regressions where applicable.
5. Hand source changes to `design-tokens`; require project-level approval before adding dependencies or altering a shared CI pipeline.

Read [build-contract.md](references/build-contract.md) when defining a new target.

## Completion evidence

Return source and generated artifacts, command results, target/theme coverage, reproducibility status, and any dependency or CI decision still needed.
