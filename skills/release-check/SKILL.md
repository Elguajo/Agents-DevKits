---
name: release-check
description: Perform the final evidence-based ship/no-ship check for a completed software change by running or verifying the project's required build, type, lint, test, browser, accessibility, performance, security, migration, configuration, and deployment checks. Use only after implementation and focused reviews are complete.
---

# Release Check

Own **final readiness verification**. This is a gate, not another design or implementation phase.

## Use when
- A feature or release candidate is believed to be complete.
- The user asks whether a change is ready to ship, merge, deploy, or release.
- A final pre-merge/pre-deploy verification is needed.

## Do not use when
- The feature is still being designed or implemented.
- A focused review has not yet been done where clearly required.
- The user only wants one specific test; use the relevant testing/review skill directly.

## Workflow
1. Read project-defined completion criteria first (`AGENTS.md`, `CLAUDE.md`, `agents-devkits.yaml` when present, CI config, package scripts, contributing docs).
2. Inspect the final diff and identify affected surfaces.
3. Run or verify the narrowest authoritative checks required by the project, expanding when the change warrants it.
4. Typical evidence may include:
   - typecheck
   - lint
   - unit/integration tests
   - production build
   - browser/E2E checks via `playwright-testing`
   - visual comparison via `visual-qa` for UI work
   - accessibility review for interactive UI
   - performance review when performance-sensitive
   - security review for trust-boundary changes
   - migrations/schema compatibility
   - environment variables/configuration
   - deploy/rollback considerations
5. Inspect browser console/network errors for web UI when feasible.
6. Distinguish checks actually executed from checks inferred from CI or not available locally.
7. Produce a ship/no-ship decision based on evidence.

## Progressive references

Load only the reference that matches the release in front of you.

- [`references/release-regression-check.md`](references/release-regression-check.md) — detailed final regression and readiness matrix for a broad release candidate.
- [`references/production-readiness.md`](references/production-readiness.md) — the change is deployed to a real environment and needs configuration, secret delivery, ordering, rollback, health, and incident-path verification.

## Gate rules
- Never say "ready" solely because code compiles.
- Never claim a check passed if it was not run or authoritatively observed.
- Accept specialist evidence only when it identifies its artifact/check, `status`, and `source`. `unavailable` and `inferred` evidence remain limitations, not passes.
- A project manifest may name structured verification commands, but execute them only when the user asks for verification or release readiness.
- Do not silently redesign, re-architect, or broaden scope during this gate.
- Small mechanical fixes discovered here may be applied when safe; material defects should fail the gate and hand back to the appropriate skill.
- Project-specific release rules override this generic checklist.

## Output contract
Return:
- Decision: `SHIP`, `SHIP WITH KNOWN RISKS`, or `NO-SHIP`
- Artifact summary: final files/surfaces and specialist decisions considered
- Evidence: checks run and results
- Blocking issues, if any
- Known residual risks / checks not performed
- Minimal next action needed to reach `SHIP`
