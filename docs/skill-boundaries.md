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
| `apple-quality-interface-refinement` | Preservation-first craft, state, and coherence pass on an existing UI | Direction change → `redesign`; new art direction → `frontend-design`; final visual evidence → `visual-qa` |
| `debugging` | Find and fix root causes of incorrect behavior | Behavior-preserving cleanup → `refactor` |
| `refactor` | Improve internal structure while preserving behavior | Unknown defect → `debugging`; material redesign → `solution-architecture` |
| `testing` | Unit/integration/regression test strategy and implementation | Browser E2E → `playwright-testing` |
| `visual-qa` | Compare implemented UI to approved visual intent | Functional browser behavior → `playwright-testing` |
| `playwright-testing` | Browser-level functional/E2E verification | Visual fidelity → `visual-qa`; a11y → `accessibility-review` |
| `accessibility-review` | Accessibility-specific audit/remediation | Does not broadly redesign UI |
| `ux-usability-audit` | Human-centered usability and interaction logic of an exercised interface | Structural model → `information-architecture`; broad rework → `redesign`; accessibility criteria → `accessibility-review` |
| `performance-review` | Evidence-based performance diagnosis | Does not perform speculative architecture rewrites |
| `code-review` | Correctness/regression/maintainability review of a change | Deep security → `security-review` |
| `security-review` | Security/trust-boundary review | General quality → `code-review` |
| `release-check` | Final evidence-based ship/no-ship gate | Material defect → hand back to owning skill |
| `change-impact-analysis` | Map what a proposed change can affect before an approach is chosen | Approach → `solution-architecture`; persisted transition → `data-migration` |
| `data-storage-review` | Durable data health at rest and in normal read/write use | Format transition → `data-migration`; measured slowness → `performance-review` |
| `data-migration` | Transition between persisted schemas, formats, and versions | Storage health → `data-storage-review`; ship decision → `release-check` |
| `concurrency-review` | Concurrency, ordering, cancellation, reentrancy, shared-state correctness | Observed defect → `debugging`; recovery semantics → `reliability-review` |
| `reliability-review` | Failure, retry, idempotency, partial-state and recovery semantics | Reproducible failure → `debugging`; visibility → `observability-review` |
| `observability-review` | Whether production behavior and failures can be diagnosed | Reproducible defect → `debugging`; sensitive output → `security-review` |
| `project-audit` | Breadth-first technical health orchestration across a repository | Each deep dive → the specialist owner |
| `interdisciplinary-project-audit` | Cross-discipline blind spots across product, UX, business, operations, data, engineering | Technical depth → `project-audit`; committed direction → `product-spec` |
| `credit-codex-contributor` | Repository attribution workflow | Unrelated to engineering workflow skills |

## Progressive references

Some skills carry scenario-specific protocols under `references/`. A reference is
part of its owner, never a competing skill, and is loaded only when the trigger
declared in `skills/registry.yaml` applies.

- `solution-architecture` owns `implementation-preflight` (plan safely before editing) and `solution-challenge` (only when several materially different approaches are genuinely viable).
- `code-review` owns `independent-implementation-review`, `recent-changes-review`, `dependency-introduction-review`, `architecture-fit-review`, and `quick-check`.
- `debugging` owns `root-cause-debugging`, `related-bug-hunt`, `duplicate-work-investigation`, `state-consistency-audit`, and `lifecycle-resource-cleanup-audit`.
- `testing` owns `regression-test-builder`, `test-gap-analysis`, and `edge-case-hardening`.
- `performance-review` owns `performance-degradation-investigation` and `startup-initialization-audit`.
- `refactor` owns `behavior-preserving-refactor`; `release-check` owns `release-regression-check`; `security-review` owns `web-surface-triage` and `security-trust-boundary-review`; `data-storage-review` owns `large-dataset-handling`.

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

### `apple-quality-interface-refinement` vs `redesign` vs `frontend-design`
All three improve an interface, and they differ by how much license they have
over the existing direction. `apple-quality-interface-refinement` keeps the
current visual language and raises execution quality inside it: hierarchy,
spacing and type coherence, component states, surface craft, purposeful motion,
and a before/after render loop. `redesign` is the owner when the direction
itself may change, and `frontend-design` is the owner when a new visual concept
must be invented. Apple's HIG is used by the refinement pass as a quality
benchmark only; importing Apple controls, materials, or token values to look
like Apple is out of scope for all three. Final visual evidence stays with
`visual-qa`, deep usability diagnosis with `ux-usability-audit`, and
accessibility criteria with `accessibility-review`.

### `debugging` vs `refactor`
`debugging` changes code to correct a known defect after evidence-based diagnosis. `refactor` preserves behavior while improving structure. Do not disguise a behavior change as a refactor.

### `testing` vs `playwright-testing`
`testing` owns unit/integration/regression coverage. `playwright-testing` owns browser E2E flows. Choose the cheapest reliable layer; do not duplicate the same behavior at every layer without reason.

### `visual-qa` vs `playwright-testing`
`visual-qa` answers “does it look right?” `playwright-testing` answers “does it work in a browser?” A single browser session may gather evidence for both, but findings remain classified by owner.

### `ux-usability-audit` vs `design-review` vs `redesign` vs `information-architecture`
`ux-usability-audit` audits a product that was actually exercised and reports
task-level usability evidence: comprehension, discoverability, states, recovery,
efficiency, and microcopy. `design-review` is expert critique of UI quality and
trade-offs, including a design artifact that cannot be exercised.
`redesign` executes a broad, behavior-preserving UI improvement once the
direction is agreed; a usability audit implements only local, high-confidence
interaction fixes and hands larger rework over. `information-architecture` owns
deciding navigation, hierarchy, and route semantics; the audit reports observed
structural problems rather than redefining the sitemap. None of them may present
expert observation as user research; that remains `ux-research`.

### `code-review` vs `security-review`
`code-review` can flag an obvious security problem, but security-sensitive surfaces should be handed to `security-review` for threat-focused analysis. `security-review` should not fill its report with general formatting or maintainability opinions.

### `release-check` vs every other skill
`release-check` does not redo all prior work. It verifies evidence and delegates material failures back to the relevant owner. It should never claim that an unavailable check passed.

### `debugging` vs `concurrency-review` vs `reliability-review` vs `observability-review`
An observed defect starts in `debugging`. Hand off only when evidence shows the
primary mechanism belongs to a specialist: plausible interleaving of concurrent
actors → `concurrency-review`; retry, idempotency, partial-state, or recovery
semantics → `reliability-review`; the failure cannot be understood from available
production signals → `observability-review`. A proactive review of one of those
concerns may start directly in the specialist without an observed defect.

### `data-storage-review` vs `data-migration` vs `performance-review`
`data-storage-review` owns durable data in normal operation: source of truth,
integrity, growth, retention, cleanup, and recovery. `data-migration` owns the
transition between persisted schemas, formats, or versions, including legacy
records, mixed versions, interruption, and rollback. `performance-review` owns a
measured performance symptom even when data volume contributes. None of them may
silently delete durable user data to improve a metric.

### `change-impact-analysis` vs `solution-architecture` vs `code-review`
`change-impact-analysis` answers "what could this break?" before an approach is
chosen; it does not design or implement. `solution-architecture` chooses the
approach. `code-review` judges an already implemented change, including its
architecture fit. Blast-radius findings must distinguish confirmed dependencies
from plausible but unverified risk.

### `project-audit` vs `interdisciplinary-project-audit` vs specialist reviews
`project-audit` is a breadth-first technical orchestrator; it discovers where a
specialist review is justified rather than performing every discipline at full
depth. `interdisciplinary-project-audit` covers cross-discipline blind spots
including product, UX, business, operations, and support. Both are `ASK`-tier:
they require an explicit user request, and neither may implement broad changes
during discovery.

### Experimental skills
Skills marked `experimental` in `skills/registry.yaml` are routed at `PROPOSE` or
`ASK` so their selection is announced or requested rather than silent. Promotion
to `active` requires real-world use; status is not evidence of quality.

## External skills/plugins

This repository intentionally avoids duplicating provider-specific capabilities when an official external skill/plugin already owns them well. Provider tools such as Figma MCP/plugins can be used by `figma-to-code` and `figma-integration`; their configuration and credentials remain outside the portable skill library.
