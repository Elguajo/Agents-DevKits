---
name: playwright-testing
description: Verify web application behavior in a real browser with Playwright-style end-to-end workflows, covering critical user journeys, states, console/network failures, and regressions. Use for functional browser QA after implementation.
---

# Playwright Testing

Own **browser-level functional verification**. Do not own visual art direction.

## Use when
- A feature needs end-to-end or browser-level verification.
- User flows, navigation, forms, authentication, async states, or regressions must be tested in a real browser.
- A build passing is not sufficient evidence that the feature works.

## Do not use when
- The main goal is pixel/visual comparison; use `visual-qa`.
- Unit-level logic is the only thing under test.
- The environment cannot run a browser; state the limitation rather than inventing results.

## Workflow
1. Read existing test conventions and reuse the project's Playwright setup when present.
2. Identify the smallest set of critical user journeys and failure paths.
3. Prefer stable, user-facing selectors: roles, labels, accessible names, test IDs only when necessary.
4. Exercise realistic interactions rather than directly mutating internal state.
5. Check expected UI state after each meaningful action.
6. Inspect browser console and failed network requests for relevant errors.
7. Cover loading, empty, validation, error, permission, and retry states where they matter.
8. Keep tests deterministic; control time/network fixtures when required.
9. Re-run affected tests after fixes and report what was actually executed.

If browser automation is unavailable, do not replace it with source-only claims.
Report the limitation and use the cheapest available non-browser evidence instead.

## Test quality rules
- Test user-observable behavior, not implementation details.
- Do not add brittle waits when a deterministic condition can be awaited.
- Do not create broad suites merely to increase coverage numbers.
- Do not hide product bugs by weakening assertions.

## Handoff
Visual differences belong to `visual-qa`; accessibility-specific failures belong to `accessibility-review`; final ship readiness belongs to `release-check`. Include the exercised artifact/flow, browser checks actually run, results, and remaining coverage gaps in the handoff.
