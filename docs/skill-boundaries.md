# Skill Boundaries and Handoffs

This document prevents skills from competing for the same responsibility.

## Precedence

1. Explicit user request
2. Repository/project instructions (`AGENTS.md`, `CLAUDE.md`, `agents-devkits.yaml`, project docs)
3. Task-specific source of truth (for example Figma, approved screenshots, API contract)
4. Existing project conventions/design system
5. Generic guidance inside these skills

A skill must not override a higher-precedence source.

## Responsibility map

| Skill | Primary responsibility | Handoff / boundary |
|---|---|---|
| `product-spec` | Define what/why, scope, states, acceptance criteria | Technical design → `solution-architecture` |
| `codebase-explorer` | Explain how the relevant existing code works | Future design → `solution-architecture`; defects → `debugging` |
| `solution-architecture` | Decide how a non-trivial change fits the existing system | Product scope → `product-spec`; visual direction → `frontend-design` |
| `feature-development` | Orchestrate a non-trivial feature across specialist skills | Does not replace specialist ownership |
| `frontend-design` | Visual concept/art direction | Existing-system consistency → `design-system`; supplied Figma → `figma-to-code` |
| `design-system` | Reuse existing tokens/components/patterns | Does not invent art direction |
| `figma-to-code` | Translate supplied Figma/reference intent to production code | Post-implementation fidelity → `visual-qa` |
| `responsive-design` | Deliberate layout/content adaptation across viewport sizes | Art direction → `frontend-design`; rendered verification → `visual-qa` |
| `motion-design` | Purposeful transitions, motion, scroll behavior, micro-interactions | Base visual direction → `frontend-design`; runtime cost → `performance-review` |
| `debugging` | Find and fix root causes of incorrect behavior | Behavior-preserving cleanup → `refactor` |
| `refactor` | Improve internal structure while preserving behavior | Unknown defect → `debugging`; material redesign → `solution-architecture` |
| `testing` | Unit/integration/regression test strategy and implementation | Browser E2E → `playwright-testing` |
| `visual-qa` | Compare implemented UI to approved visual intent | Functional browser behavior → `playwright-testing` |
| `playwright-testing` | Browser-level functional/E2E verification | Visual fidelity → `visual-qa`; a11y → `accessibility-review` |
| `accessibility-review` | Accessibility-specific audit/remediation | Does not broadly redesign UI |
| `performance-review` | Evidence-based performance diagnosis | Does not perform speculative architecture rewrites |
| `code-review` | Correctness/regression/maintainability review of a change | Deep security → `security-review` |
| `security-review` | Security/trust-boundary review | General quality → `code-review` |
| `release-check` | Final evidence-based ship/no-ship gate | Material defect → hand back to owning skill |
| `credit-codex-contributor` | Repository attribution workflow | Unrelated to engineering workflow skills |

## Collision rules

### `product-spec` vs `solution-architecture`
`product-spec` owns what must be true for the user/product. `solution-architecture` owns how software should satisfy it. Architecture must not silently narrow or broaden product scope.

### `codebase-explorer` vs `solution-architecture`
`codebase-explorer` answers “how is it built now?” `solution-architecture` answers “how should we change it?” Exploration reports facts and constraints rather than prematurely choosing the future design.

### `feature-development` vs specialist skills
`feature-development` is an orchestrator. It selects justified specialists and preserves their boundaries; it should not mechanically run every skill or override specialist rules.

### `frontend-design` vs `design-system`
`frontend-design` may propose an aesthetic direction when the brief leaves room for one. `design-system` ensures implementation reuses the existing system. If an explicit new design direction intentionally changes the system, the task/user decision wins; do not silently force old tokens back in.

### `frontend-design` vs `figma-to-code`
When Figma or an approved reference is supplied as the source of truth, `figma-to-code` should reproduce it instead of allowing `frontend-design` to reinterpret it. Use `frontend-design` only for unresolved visual choices.

### `responsive-design` vs `visual-qa`
`responsive-design` defines how layout/content should adapt. `visual-qa` checks the rendered result. QA should report discrepancies, not invent a different responsive system.

### `motion-design` vs `performance-review`
`motion-design` owns interaction intent and timing. `performance-review` may identify measured runtime cost and request optimization, but should not remove signature motion solely from preference.

### `debugging` vs `refactor`
`debugging` changes code to correct a known defect after evidence-based diagnosis. `refactor` preserves behavior while improving structure. Do not disguise a behavior change as a refactor.

### `testing` vs `playwright-testing`
`testing` owns unit/integration/regression coverage. `playwright-testing` owns browser E2E flows. Choose the cheapest reliable layer; do not duplicate the same behavior at every layer without reason.

### `visual-qa` vs `playwright-testing`
`visual-qa` answers “does it look right?” `playwright-testing` answers “does it work in a browser?” A single browser session may gather evidence for both, but findings remain classified by owner.

### `code-review` vs `security-review`
`code-review` can flag an obvious security problem, but security-sensitive surfaces should be handed to `security-review` for threat-focused analysis. `security-review` should not fill its report with general formatting or maintainability opinions.

### `release-check` vs every other skill
`release-check` does not redo all prior work. It verifies evidence and delegates material failures back to the relevant owner. It should never claim that an unavailable check passed.

## External skills/plugins

This repository intentionally avoids duplicating provider-specific capabilities when an official external skill/plugin already owns them well. In particular, the existing vendored `frontend-design` remains the sole generic art-direction skill. Provider tools such as Figma MCP/plugins can be used by `figma-to-code`; their configuration and credentials remain outside the portable skill library.
