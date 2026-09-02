> Integrated from the v0.1 prompt/skill prototype `release-regression-check`. Load this reference only when its trigger applies.

# Release / Regression Check
## Goal
Decide whether the current version is safe to release and identify release blockers.

## Workflow
1. Understand the release scope and user-visible changes.
2. Identify critical paths, integrations, persistence, migrations, compatibility boundaries, and rollback concerns.
3. Run the project’s relevant test, type, lint, build, packaging, and smoke checks.
4. Verify the most important user flows and changed behavior.
5. Check release-only failures: configuration, environment, versioning, assets, permissions, secrets, migrations, and packaging.
6. Classify findings as blockers or follow-ups.

## Rules
- Do not add speculative features during release review.
- Do not hide failing checks.
- If a required validation cannot be run, treat it as unverified rather than passed.

## Output
READY / READY WITH FOLLOW-UPS / NOT READY, release blockers, verification matrix, and remaining risks.
