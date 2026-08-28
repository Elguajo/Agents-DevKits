# Skill Boundaries and Handoffs

This document prevents skills from competing for the same responsibility.

## Precedence

1. Explicit user request
2. Repository/project instructions (`AGENTS.md`, `CLAUDE.md`, `agents-devkits.yaml`, project docs)
3. Task-specific source of truth (for example Figma, approved screenshots, API contract)
4. Existing project conventions/design system
5. Generic guidance inside these skills

A skill must not override a higher-precedence source.

## Selection levels

The generated [`ROUTING.md`](ROUTING.md) is a compact index derived from the
registry; it never replaces the registry or a selected `SKILL.md`.

- `AUTO` selects a skill only when its trigger and ownership boundary both fit.
- `PROPOSE` announces the recommended workflow and continues unless the user redirects; it is not an approval gate.
- `ASK` requires an explicit user request before selection.

These levels govern candidate selection only. They never replace authorization,
safety checks, or higher-precedence project instructions.

## Responsibility map

| Skill | Primary responsibility | Handoff / boundary |
|---|---|---|
| `product-spec` | Define what/why, scope, states, acceptance criteria | Technical design → `solution-architecture` |
| `ux-research` | Plan research or synthesize user evidence for a decision | Journey/service map → `journey-mapping`; product scope → `product-spec` |
| `information-architecture` | Decide navigation, hierarchy, route semantics, and structural flows | UI implementation → `design-system` / `design-code`; technical modules → `solution-architecture` |
| `journey-mapping` | Map a cross-touchpoint user/service scenario to prioritize decisions | Research design → `ux-research`; committed behavior → `product-spec` |
| `codebase-explorer` | Explain how the relevant existing code works | Future design → `solution-architecture`; defects → `debugging` |
| `project-knowledge` | Maintain a concise, source-grounded project-specific reference | Project-local facts → owning specialist; one-time exploration → `codebase-explorer` |
| `solution-architecture` | Decide how a non-trivial change fits the existing system | Product scope → `product-spec`; visual direction → `frontend-design` |
| `feature-development` | Orchestrate a non-trivial feature across specialist skills | Does not replace specialist ownership |
| `frontend-design` | Visual concept/art direction | Existing-system consistency → `design-system`; supplied Figma → `figma-to-code` |
| `apply-aesthetic` | Reusable visual-direction decisions | Broad concept → `frontend-design`; system implementation → `design-tokens` / `design-code` |
| `brandkit` | New-product token and theme foundation | Platform artifacts → `token-build` |
| `design-tokens` | Token layers, themes, and compatibility | Generated outputs → `token-build`; components → `design-component` |
| `design-component` | Reusable component anatomy, states, and behavior contract | Framework code → `design-code` |
| `design-code` | Token-aware framework implementation | Fidelity/a11y/behavior checks → QA specialists |
| `design-qa` | UI evidence plan and consolidated coverage | Does not replace `visual-qa`, `accessibility-review`, or browser testing |
| `design-review` | Expert review of UI quality and trade-offs | Exact visual match → `visual-qa`; remediation → owning specialist |
| `figma-integration` | Figma/code parity contract | Figma-driven UI implementation → `figma-to-code` |
| `governance` | Design-system compatibility/deprecation | General project governance remains outside this skill |
| `image-to-code` | Safe reference-image reconstruction | Figma source → `figma-to-code`; visual comparison → `visual-qa` |
| `migrate-design-system` | Role-by-role UI-system mapping and rollout | Token/component/code changes → specialist owners |
| `prototype` | Prototype fidelity and learning plan | Production work → `feature-development` / `design-code` |
| `redesign` | Audit-first, behavior-preserving UI improvement | Product behavior changes → `product-spec` / `solution-architecture` |
| `token-build` | Deterministic token transformations | Source changes → `design-tokens`; release evidence → `release-check` |
| `ux-writing` | State-aware interface language | Product requirements → `product-spec`; semantic effects → `accessibility-review` |
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

### `ux-research` vs `design-review` vs `product-spec`
`ux-research` plans or synthesizes evidence about user behavior. `design-review`
is expert evaluation when such evidence is unavailable or not required.
`product-spec` decides the committed product behavior after the relevant evidence
and trade-offs are understood; none of these skills may present assumptions as
user research.

### `information-architecture` vs `design-system` vs `solution-architecture`
`information-architecture` owns the user-facing structure: navigation, content
hierarchy, labels, routes, and critical flows. `design-system` implements that
structure with existing UI conventions. `solution-architecture` owns software
module boundaries and integrations, not the product's sitemap.

### `journey-mapping` vs `ux-research`
`journey-mapping` turns existing evidence and explicitly labelled assumptions
into a shared experience/service model. `ux-research` determines how missing
evidence should be obtained or synthesized. A map does not establish that a
research study happened.

### `codebase-explorer` vs `solution-architecture`
`codebase-explorer` answers “how is it built now?” `solution-architecture` answers “how should we change it?” Exploration reports facts and constraints rather than prematurely choosing the future design.

### `project-knowledge` vs `codebase-explorer`

`project-knowledge` creates or updates a durable, opt-in project reference only
when facts recur across tasks. `codebase-explorer` maps the smallest relevant
area for the current task and should not create persistent documentation merely
because it inspected files.

### `feature-development` vs specialist skills
`feature-development` is an orchestrator. It selects justified specialists and preserves their boundaries; it should not mechanically run every skill or override specialist rules.

### `frontend-design` vs `design-system`
`frontend-design` may propose an aesthetic direction when the brief leaves room for one. `design-system` ensures implementation reuses the existing system. If an explicit new design direction intentionally changes the system, the task/user decision wins; do not silently force old tokens back in.

### `frontend-design` vs `apply-aesthetic` vs `design-system`
`frontend-design` establishes a broad visual concept. `apply-aesthetic` turns an approved direction into reusable token and layout implications. `design-system` keeps implementation consistent with the current system. A supplied brand, Figma file, or approved reference remains higher precedence than all three.

### `design-tokens` vs `token-build` vs `design-component`
`design-tokens` owns source-layer roles and compatibility. `token-build` owns deterministic target generation. `design-component` owns how a reusable component consumes tokens. None may quietly redefine another layer.

### `design-component` vs `design-code`
`design-component` describes reusable anatomy, variants, states, and accessible behavior. `design-code` implements that contract in the repository's framework. Rendered correctness belongs to `visual-qa`, `accessibility-review`, and browser testing.

### `design-review` vs `design-qa` vs specialist QA
`design-review` is expert judgment. `design-qa` scopes and consolidates evidence. `visual-qa`, `accessibility-review`, and `playwright-testing` own their individual findings. Expert review is not a substitute for executed checks.

### `figma-integration` vs `figma-to-code` vs `image-to-code`
`figma-integration` owns token/component parity across Figma and code. `figma-to-code` implements from an approved Figma source. `image-to-code` reconstructs an image reference and must substitute protected identity assets. Neither implies that an image proves interaction or accessibility behavior.

### `redesign` vs product work
`redesign` improves an existing UI while preserving approved behavior. Changes to product scope, routes, data behavior, or user promises belong to `product-spec` and `solution-architecture` first.

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

This repository intentionally avoids duplicating provider-specific capabilities when an official external skill/plugin already owns them well. Provider tools such as Figma MCP/plugins can be used by `figma-to-code` and `figma-integration`; their configuration and credentials remain outside the portable skill library.
