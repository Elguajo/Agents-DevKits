---
name: quality-constraints
description: Define or revise a durable, project-specific, machine-checkable quality contract without weakening it to obtain a passing result. Use when a project needs an enforceable quality bar or a proposed change would relax that bar.
---

# Quality Constraints

Own **the durable project-specific quality contract**. Do not own test implementation, CI provider configuration, specialist review, or a release decision.

## Use when

- A project needs explicit, reproducible checks and thresholds before autonomous implementation or release work.
- Existing quality rules, budgets, exceptions, or their enforcement commands need to be established or revised.
- A failing check prompts a proposal to lower a threshold, skip/delete a test, add a suppression, remove an assertion, or otherwise weaken the quality bar.

## Do not use when

- A task only needs tests for one behavior; use `testing`.
- A completed change needs a ship/no-ship decision; use `release-check`.
- A specialist must assess accessibility, performance, security, or API correctness; use that specialist.
- The task only changes CI syntax or a deployment provider without changing the quality contract.

## Workflow

1. Read the project instructions, existing scripts, CI configuration, and any current quality document. Establish the observed baseline before proposing a target.
2. Define only relevant dimensions: objective checks, their commands, where they run, baseline/ratchet or approved threshold, rationale, owner, and exception expiry. Do not invent universal numeric defaults.
3. Make one durable project-owned document the source of truth; scripts and CI must reference or mirror it rather than become competing policy sources.
4. Prefer an existing project checker or authoritative external rule. Place fast checks in the edit loop and expensive checks in task/CI stages.
5. Add a diff-aware floor guard or equivalent review rule for bar-lowering moves: lowered thresholds, disabled/deleted/eased tests, new suppressions, removed assertions, unfinished stubs, and unowned exceptions. Tightening is silent; relaxation requires an explicit, reviewed exception with an owner and expiry.
6. Verify the proposed contract against the current branch. If the baseline cannot meet a desired target, use a measured baseline plus a non-regression ratchet instead of creating a permanently failing gate.
7. Hand behavior coverage to `testing`, specialist dimensions to their owners, pipeline implementation to the project’s normal implementation workflow, and final evidence to `release-check`.

## Rules

- A green result obtained by weakening a check is not a pass.
- Never silently add a suppression, skip, deleted assertion, stub, or lowered threshold to make a change pass.
- Exceptions must name the rule, reason, owner, and expiry; an exception is visible technical debt, not a hidden bypass.
- Keep the contract stack- and project-specific. Report a check as unavailable when its tooling or environment is unavailable.
- Treat CI as enforcement of the declared contract, not as a second authority for what quality means.

## Failure modes / anti-rationalization

- “The test is flaky, so skip it” → identify and fix or explicitly time-box the flake; do not make an invisible bypass.
- “Coverage is too low, lower the target” → preserve the current measured baseline and use an approved ratchet.
- “This suppression is harmless” → make the exception visible, scoped, owned, and expiring, or fix the underlying issue.
- “CI is slow, remove the check” → move costly checks to an appropriate stage before considering a policy change.

## Handoffs

- Behavior/regression coverage → `testing`.
- Security, accessibility, performance, or API quality dimension → the matching specialist review.
- CI/deployment implementation that realizes an agreed contract → `feature-development` or the project’s established workflow.
- Final aggregation and release decision → `release-check`.

## Output contract

Return the quality-contract location, observed baseline, checks and execution stages, explicit exceptions, floor-guard result, contract changes, evidence actually run, and unresolved limitations.
