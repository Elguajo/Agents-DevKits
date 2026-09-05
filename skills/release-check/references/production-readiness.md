> Local reference for `release-check`. Load only when a change reaches a real deployment rather than a merge.

# Production Readiness
## Goal
Confirm that a change which passed its quality checks can also be deployed, operated, and reversed.

## Workflow
1. Identify the deployment unit and the environments it passes through before users see it.
2. Check configuration: every new or changed environment variable, feature flag, and default is declared for each environment and has a defined value in production.
3. Check secret delivery: how the credential reaches the runtime, who can rotate it, and what fails if it is absent. Never inspect or print the secret value itself.
4. Check ordering: whether the release requires a migration, a flag flip, a cache invalidation, or a client update, and in which order they must happen.
5. Check backward compatibility during the rollout window, when old and new versions run at the same time.
6. Check rollback: whether reverting the deployment is sufficient, or whether data written by the new version makes rollback lossy.
7. Check health and startup: readiness signals, failed-start behavior, and whether a bad deploy is detected automatically or by a user report.
8. Check the incident path: who is alerted, what the first diagnostic step is, and whether that signal exists today.
9. Record which of these were verified and which are stated intentions.

## Rules
- Deployment readiness is separate from code correctness; a green test suite is not a rollout plan.
- A rollback that loses user data is not a rollback; say so explicitly.
- Do not invent infrastructure the project does not have; report the gap instead.
- An unverifiable operational claim is a residual risk, not a pass.

## Handoffs
- Persisted-format transitions and their reversibility → `data-migration`.
- Missing production signals and diagnoseability → `observability-review`.
- Behavior during partial rollout and dependency failure → `reliability-review`.

## Output
Deployment unit, configuration and secret deltas, required ordering, rollback assessment, health and incident path, verified versus stated items, and blockers.
