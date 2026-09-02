# Skill Catalog & Field Notes

This is the canonical human-readable registry for the skills in this repository.

Use it to answer four questions quickly:

1. **What does this skill own?**
2. **When should I use it?**
3. **Where did it come from?**
4. **What should it hand off to instead of doing itself?**

For machine-readable metadata, see [`skills/registry.yaml`](skills/registry.yaml). For precedence and collision rules, see [`docs/skill-boundaries.md`](docs/skill-boundaries.md).

## Reading the catalog

- **Origin: local** — maintained in this repository.
- **Origin: vendored** — copied from an upstream project; check the skill's `SOURCE.md` and license before modifying or redistributing it.
- **Tooling: optional** — the skill can still provide workflow guidance without the tool, but becomes stronger when that tool is available.
- **Invocation, triggers, and capabilities** — `skills/registry.yaml` separates `user`/`model` invocation from declarative trigger expressions. [`capabilities/registry.yaml`](capabilities/registry.yaml) defines portable requirement and fallback semantics. They guide routing but do not replace agent judgment or project instructions.
- **Completion evidence** — orchestration and review skills report decisions, affected artifacts, checks actually performed, results, and remaining risks. Expert review is not a substitute for objective checks.
- A skill owns one primary concern. If the task crosses concerns, prefer a handoff instead of expanding one skill until it overlaps everything else.
- **Status** — `active` is the current stable owner. `experimental` marks a skill introduced by the v0.2 skills migration; it is routed at `PROPOSE` or `ASK` and should be exercised on real work before promotion.
- **Progressive references** — a skill's `references/` files are scenario-specific protocols. They are declared in `skills/registry.yaml` with the trigger that justifies loading them, and must not be read by default.

## Quick registry

| Skill | Owns | Origin | Best paired with |
|---|---|---|---|
| `product-spec` | Product intent, scope, states, acceptance criteria | local | `solution-architecture` |
| `ux-research` | Decision-oriented UX research plans and evidence synthesis | local adaptation | `product-spec`, `journey-mapping` |
| `information-architecture` | Navigation, content hierarchy, route semantics, user flows | local adaptation | `design-system`, `solution-architecture` |
| `journey-mapping` | Evidence-aware experience and service maps | local adaptation | `ux-research`, `product-spec` |
| `codebase-explorer` | Understanding existing implementation and constraints | local | `solution-architecture`, `debugging` |
| `project-knowledge` | Source-grounded project-specific factual references | local | `design-system`, `solution-architecture` |
| `affine-notion-graph-sync` | Read-only Notion to self-hosted AFFiNE Edgeless Canvas imports | local | `data-storage-review`, `reliability-review` |
| `solution-architecture` | Technical approach and implementation boundaries | local | `codebase-explorer`, `feature-development` |
| `feature-development` | Orchestration of non-trivial feature work | local | relevant specialists only |
| `frontend-design` | Visual concept and art direction | vendored: Anthropic | `design-system`, `responsive-design`, `motion-design` |
| `apply-aesthetic` | Token-aware visual direction | adapted: plugin87 | `design-tokens`, `design-code` |
| `brandkit` | New-product visual foundation | adapted: plugin87 | `design-tokens`, `token-build` |
| `design-tokens` | Semantic token architecture | adapted: plugin87 | `token-build`, `design-component` |
| `design-component` | Reusable component contract | adapted: plugin87 | `design-code`, `accessibility-review` |
| `design-code` | Token-driven framework UI | adapted: plugin87 | `visual-qa`, `playwright-testing` |
| `design-qa` | UI evidence matrix and coverage | adapted: plugin87 | specialist QA/review skills |
| `design-review` | Expert UI-quality assessment | adapted: plugin87 | `redesign`, `release-check` |
| `figma-integration` | Figma/code token and variant parity | adapted: plugin87 | `figma-to-code`, `design-tokens` |
| `governance` | Design-system compatibility and deprecation | adapted: plugin87 | `design-tokens`, `release-check` |
| `image-to-code` | Safe screenshot-to-UI reconstruction | adapted: plugin87 | `design-code`, `visual-qa` |
| `migrate-design-system` | Role-based UI-system migration | adapted: plugin87 | `design-tokens`, `design-code` |
| `prototype` | Lowest-useful fidelity and validation plan | adapted: plugin87 | `product-spec`, `feature-development` |
| `redesign` | Audit-first UI improvement | adapted: plugin87 | `design-review`, `visual-qa` |
| `token-build` | Reproducible token-platform outputs | adapted: plugin87 | `design-tokens`, `release-check` |
| `ux-writing` | Inclusive, state-aware interface language | adapted: plugin87 | `design-code`, `accessibility-review` |
| `design-system` | Reuse of existing tokens, components and UI conventions | local | `frontend-design`, `figma-to-code` |
| `figma-to-code` | Translating supplied Figma/reference intent into code | local | Figma tooling, `design-system`, `visual-qa` |
| `responsive-design` | Cross-viewport layout/content/interaction behavior | local | `frontend-design`, `visual-qa` |
| `motion-design` | Purposeful UI motion and interaction timing | local | `frontend-design`, `performance-review` |
| `debugging` | Evidence-based root-cause diagnosis and bug fixing | local | `codebase-explorer`, `testing` |
| `refactor` | Behavior-preserving structural cleanup | local | `testing`, `code-review` |
| `testing` | Unit/integration/regression coverage | local | `debugging`, `release-check` |
| `playwright-testing` | Browser functional/E2E verification | local | Playwright/browser tooling, `visual-qa` |
| `visual-qa` | Visual fidelity and visible regression checking | local | browser/screenshots, `figma-to-code` |
| `accessibility-review` | Accessibility audit/remediation | local | `playwright-testing`, `release-check` |
| `performance-review` | Evidence-based performance diagnosis | local | profiling/browser tooling, `release-check` |
| `code-review` | Correctness, regressions, maintainability review | local | `security-review`, `release-check` |
| `security-review` | Security and trust-boundary review | local | `code-review`, `release-check` |
| `release-check` | Final evidence-based ship/no-ship gate | local | all relevant verification skills |
| `change-impact-analysis` | Blast radius of a proposed change | local (experimental) | `solution-architecture`, `data-migration` |
| `data-storage-review` | Durable data health, growth, retention, recovery | local (experimental) | `data-migration`, `performance-review` |
| `data-migration` | Safe persisted schema/format transitions | local (experimental) | `testing`, `release-check` |
| `concurrency-review` | Concurrency, ordering, cancellation, shared state | local (experimental) | `debugging`, `testing` |
| `reliability-review` | Failure, retry, idempotency, recovery semantics | local (experimental) | `debugging`, `observability-review` |
| `observability-review` | Production diagnoseability of failures | local (experimental) | `debugging`, `security-review` |
| `project-audit` | Breadth-first technical health orchestration | local (experimental) | `codebase-explorer`, specialist reviews |
| `interdisciplinary-project-audit` | Cross-discipline blind-spot discovery | local (experimental) | `project-audit`, `product-spec` |
| `credit-codex-contributor` | Safe GitHub attribution workflow for Codex | local utility | none |

---

## Product and architecture

### `product-spec`

**Path:** [`skills/product-spec/SKILL.md`](skills/product-spec/SKILL.md)  
**Origin:** local  
**Use when:** an idea is vague, broad, missing states, edge cases, constraints, or acceptance criteria.  
**Produces:** a concise implementation-ready definition of **what** should exist and **why**.  
**Take from it:** scope framing, non-goals, states, edge cases, acceptance criteria.  
**Do not take from it:** framework choices, database schema, component architecture, visual direction.  
**Handoff:** `solution-architecture` once behavior is defined.

### `ux-research`

**Path:** [`skills/ux-research/SKILL.md`](skills/ux-research/SKILL.md)<br>
**Origin:** local adaptation; [source note](skills/ux-research/SOURCE.md)<br>
**Use when:** a product or UX decision needs behavior evidence, an interview or
usability-test plan, or synthesis of existing research.<br>
**Produces:** the lightest defensible method, sourced findings when evidence is
provided, and a decision handoff.<br>
**Important:** a research plan or inference is never presented as evidence that
participants were contacted or research occurred.<br>
**Handoff:** `product-spec`, `information-architecture`, `journey-mapping`, or
`prototype`.

### `information-architecture`

**Path:** [`skills/information-architecture/SKILL.md`](skills/information-architecture/SKILL.md)<br>
**Origin:** local adaptation; [source note](skills/information-architecture/SOURCE.md)<br>
**Use when:** navigation, content hierarchy, route semantics, labels, or user
flows must be decided before detailed UI implementation.<br>
**Produces:** a structural model tied to existing routes, layouts, content, and
growth constraints.<br>
**Do not use it for:** visual direction, component implementation, or general
software architecture.<br>
**Handoff:** `design-system`, `design-code`, `product-spec`, or
`solution-architecture`.

### `journey-mapping`

**Path:** [`skills/journey-mapping/SKILL.md`](skills/journey-mapping/SKILL.md)<br>
**Origin:** local adaptation; [source note](skills/journey-mapping/SOURCE.md)<br>
**Use when:** an end-to-end persona journey, service flow, empathy map, or user
story map must inform prioritization.<br>
**Produces:** an evidence-aware map with moments of truth, owned opportunities,
and a next decision.<br>
**Important:** assumptions remain labelled; a map is a decision tool, not proof
of user research.<br>
**Handoff:** `ux-research`, `product-spec`, `information-architecture`, or
`solution-architecture`.

### `codebase-explorer`

**Path:** [`skills/codebase-explorer/SKILL.md`](skills/codebase-explorer/SKILL.md)  
**Origin:** local  
**Use when:** an existing repository must be understood before changing it.  
**Produces:** relevant entry points, data flow, dependencies, conventions, similar implementations, and constraints.  
**Take from it:** factual understanding of **how the system works now**.  
**Do not take from it:** the future architecture decision.  
**Handoff:** `solution-architecture` for design decisions; `debugging` for an observed defect.

### `project-knowledge`

**Path:** [`skills/project-knowledge/SKILL.md`](skills/project-knowledge/SKILL.md)<br>
**Origin:** local<br>
**Use when:** recurring repository facts need a concise, durable reference for
other skills without making a new generic skill.<br>
**Produces:** a project-local knowledge pack with declared source paths,
verified facts, inferences, and open questions.<br>
**Take from it:** source-grounded extraction and provenance for local design
systems, APIs, or implementation conventions.<br>
**Do not use it to:** invent behavior, duplicate a project instruction, or keep
execution history.<br>
**Handoff:** `design-system`, `figma-to-code`, `design-code`, or
`solution-architecture` once the factual reference is ready.

### `affine-notion-graph-sync`

**Path:** [`skills/affine-notion-graph-sync/SKILL.md`](skills/affine-notion-graph-sync/SKILL.md)<br>
**Origin:** local<br>
**Use when:** the user provides a Notion page URL and asks for an AFFiNE
graph, canvas, mind map, flow, or block diagram.<br>
**Produces:** a deterministic Edgeless Canvas in self-hosted AFFiNE, with
explicit link edges, local ignored blueprint/state, and validation evidence.<br>
**Do not use it to:** store data in AFFiNE Cloud, invent relationships from
prose, or delete/reseed user-owned canvas state during a conflict.<br>
**Handoff:** `data-storage-review` for durable-data concerns or
`reliability-review` for failure, retry, and recovery semantics.

### `solution-architecture`

**Path:** [`skills/solution-architecture/SKILL.md`](skills/solution-architecture/SKILL.md)  
**Origin:** local  
**Use when:** a non-trivial change crosses modules, data flows, integrations, persistence, or architectural boundaries.  
**Produces:** the smallest coherent technical approach, affected boundaries, risks, implementation order, and verification strategy.  
**Take from it:** technical decision-making and trade-offs.  
**Do not take from it:** product scope or visual art direction.  
**Pairs well with:** `codebase-explorer`, then `feature-development` or direct implementation.

### `feature-development`

**Path:** [`skills/feature-development/SKILL.md`](skills/feature-development/SKILL.md)  
**Origin:** local  
**Use when:** a feature needs several phases and more than one specialist skill.  
**Produces:** an orchestrated path from definition through implementation and verification.  
**Take from it:** sequencing and specialist selection.  
**Important:** it is an **orchestrator**, not a super-skill. It should not mechanically invoke every skill or override specialist boundaries.

### `change-impact-analysis`

**Path:** [`skills/change-impact-analysis/SKILL.md`](skills/change-impact-analysis/SKILL.md)<br>
**Origin:** local; [source note](skills/change-impact-analysis/SOURCE.md)<br>
**Status:** experimental<br>
**Use when:** a shared API, schema, persisted identifier, event contract, or core
component is about to change and its consumers are unclear.<br>
**Produces:** confirmed consumers, hidden coupling, risk classification, and the
containment or sequencing steps a change needs.<br>
**Take from it:** blast radius grounded in real references and data paths.<br>
**Do not take from it:** the technical approach itself, or the change.<br>
**Handoff:** `solution-architecture` for the approach; `data-migration` for a
persisted transition.

---

## Data

### `data-storage-review`

**Path:** [`skills/data-storage-review/SKILL.md`](skills/data-storage-review/SKILL.md)<br>
**Origin:** local; [source note](skills/data-storage-review/SOURCE.md)<br>
**Status:** experimental<br>
**Use when:** durable application data needs review of its source of truth,
growth, retention, cleanup, integrity, or recovery expectations.<br>
**Produces:** a storage map, retention and growth risks, and integrity or
recovery concerns.<br>
**Take from it:** health of data at rest and in normal read/write use.<br>
**Do not use it to:** execute a schema transition, or tune a measured slowdown.<br>
**Handoff:** `data-migration` for transitions; `performance-review` for measured
symptoms.

### `data-migration`

**Path:** [`skills/data-migration/SKILL.md`](skills/data-migration/SKILL.md)<br>
**Origin:** local; [source note](skills/data-migration/SOURCE.md)<br>
**Status:** experimental<br>
**Use when:** a persisted schema, format, identifier, preference, or sync
contract changes and existing user data must survive.<br>
**Produces:** a migration plan, invariants, compatibility matrix, rollback
strategy, and tests against representative legacy data.<br>
**Take from it:** backward compatibility and mixed-version safety.<br>
**Do not use it to:** claim a migration is complete without legacy-data tests.<br>
**Handoff:** `testing` for coverage; `release-check` for the ship decision.

---

## Frontend and design

### `frontend-design`

**Path:** [`skills/frontend-design/SKILL.md`](skills/frontend-design/SKILL.md)  
**Origin:** vendored from Anthropic  
**Upstream metadata:** [`skills/frontend-design/SOURCE.md`](skills/frontend-design/SOURCE.md)  
**License:** retained in the skill directory.  
**Use when:** visual direction must be invented or significantly shaped.  
**Produces:** distinctive art direction, typography, palette, layout concept, visual signature, and design critique.  
**Take from it:** aesthetic reasoning and anti-template design guidance.  
**Do not use it to:** reinterpret approved Figma/reference designs.  
**Handoff:** `design-system` for implementation consistency; `responsive-design` and `motion-design` for their specific concerns.

### UX/UI extension

The following 15 skills are local adaptations of the capability boundaries in [`plugin87/ux-ui-agent-skills`](https://github.com/plugin87/ux-ui-agent-skills), pinned at the revision and declared-MIT notice in [`third_party/plugin87-ux-ui-agent-skills/`](third_party/plugin87-ux-ui-agent-skills/). Each has a local [`SOURCE.md`](skills/apply-aesthetic/SOURCE.md) and uses the same portable registry, capability, and evidence contracts as every other skill.

| Skill | Use when | Boundary / handoff |
| --- | --- | --- |
| `apply-aesthetic` | visual direction is unresolved | direction only → `design-tokens` / `design-code` |
| `brandkit` | a new product needs an accessible visual foundation | generated targets → `token-build` |
| `design-tokens` | token roles or themes must change | platform outputs → `token-build` |
| `design-component` | a reusable UI element needs a complete contract | implementation → `design-code` |
| `design-code` | approved UI intent needs framework code | visual/a11y/browser checks → specialists |
| `design-qa` | UI evidence must be planned or consolidated | it coordinates; it does not replace reviewers |
| `design-review` | independent UI-quality critique is needed | exact reference fidelity → `visual-qa` |
| `figma-integration` | Figma/code tokens or variants must stay aligned | direct implementation → `figma-to-code` / `design-code` |
| `governance` | design-system compatibility or deprecation is at stake | implementation → tokens/components |
| `image-to-code` | a screenshot or mockup is the visual source | protected assets are substituted; fidelity → `visual-qa` |
| `migrate-design-system` | systems need a semantic crosswalk and rollout | implementation → tokens/components/code |
| `prototype` | a product question should be tested before build | research/external sharing requires authorization |
| `redesign` | a working UI needs an audit-first improvement | behavior remains preserved by default |
| `token-build` | token source must produce platform artifacts | dependency/CI changes remain project decisions |
| `ux-writing` | UI copy needs creation or review | implementation and a11y effects → specialists |

### `design-system`

**Path:** [`skills/design-system/SKILL.md`](skills/design-system/SKILL.md)  
**Origin:** local  
**Use when:** the repository already has tokens, components, variants, themes, patterns, or `DESIGN.md`.  
**Produces:** implementation aligned with the existing design system.  
**Take from it:** component reuse rules, token discipline, consistency checks.  
**Do not use it to:** invent the art direction.  
**Conflict rule:** explicit new design intent wins over generic old defaults; do not silently force old tokens when the design system itself is intentionally changing.

### `figma-to-code`

**Path:** [`skills/figma-to-code/SKILL.md`](skills/figma-to-code/SKILL.md)  
**Origin:** local  
**Optional tooling:** Figma MCP/plugin or equivalent design-context access.  
**Use when:** Figma, frames, nodes, screenshots, or another approved reference is the source of truth.  
**Produces:** repository-native production UI matching the supplied design intent.  
**Take from it:** mapping reference structure/assets/states to existing components.  
**Do not use it to:** invent a replacement visual direction.  
**Handoff:** `visual-qa` after implementation.

### `responsive-design`

**Path:** [`skills/responsive-design/SKILL.md`](skills/responsive-design/SKILL.md)  
**Origin:** local  
**Use when:** layout, typography, navigation, content priority, density, or interactions must adapt across viewport sizes.  
**Produces:** deliberate responsive behavior rather than a single mobile breakpoint patch.  
**Take from it:** breakpoint reasoning, fluid behavior, touch/overflow/content-priority rules.  
**Handoff:** `visual-qa` for rendered verification.

### `motion-design`

**Path:** [`skills/motion-design/SKILL.md`](skills/motion-design/SKILL.md)  
**Origin:** local  
**Use when:** transitions, micro-interactions, scroll effects, or signature motion materially improve the interaction.  
**Produces:** purposeful motion with timing, reduced-motion behavior, and performance constraints.  
**Take from it:** interaction intent, timing, easing, hierarchy of motion.  
**Do not use it to:** animate everything by default.  
**Handoff:** `performance-review` if runtime cost becomes material.

---

## Implementation quality

### `debugging`

**Path:** [`skills/debugging/SKILL.md`](skills/debugging/SKILL.md)  
**Origin:** local  
**Use when:** observed behavior is incorrect and the root cause is unknown.  
**Produces:** reproduction, evidence, hypothesis, root cause, focused fix, regression verification.  
**Take from it:** disciplined diagnosis instead of random edits.  
**Do not confuse with:** `refactor`, which must preserve behavior.

### `refactor`

**Path:** [`skills/refactor/SKILL.md`](skills/refactor/SKILL.md)  
**Origin:** local  
**Use when:** behavior is correct but internal structure is unnecessarily complex, duplicated, or difficult to maintain.  
**Produces:** incremental behavior-preserving cleanup with verification.  
**Take from it:** safe structural simplification.  
**Do not use it to:** hide feature changes or bug fixes inside a "cleanup".

### `concurrency-review`

**Path:** [`skills/concurrency-review/SKILL.md`](skills/concurrency-review/SKILL.md)<br>
**Origin:** local; [source note](skills/concurrency-review/SOURCE.md)<br>
**Status:** experimental<br>
**Use when:** async tasks, threads, actors, queues, jobs, event handlers, or
shared mutable state create ordering, duplication, or cancellation risk.<br>
**Produces:** the concrete interleaving that causes each failure, the affected
state, a minimal synchronization fix, and a test strategy.<br>
**Take from it:** race reasoning backed by a plausible execution path.<br>
**Do not use it to:** report speculative races, or to solve everything with a
global lock.<br>
**Handoff:** `debugging` for an evidence-based fix; `reliability-review` for
retry and recovery semantics.

---

## Testing and QA

### `testing`

**Path:** [`skills/testing/SKILL.md`](skills/testing/SKILL.md)  
**Origin:** local  
**Use when:** meaningful behavior needs unit, integration, or regression coverage.  
**Produces:** focused tests at the cheapest reliable layer.  
**Take from it:** behavior-oriented test selection.  
**Do not use it to:** duplicate the same scenario at every test layer.  
**Handoff:** browser E2E behavior → `playwright-testing`.

### `playwright-testing`

**Path:** [`skills/playwright-testing/SKILL.md`](skills/playwright-testing/SKILL.md)  
**Origin:** local  
**Optional tooling:** Playwright/browser automation.  
**Use when:** real browser flows, navigation, forms, browser state, network interactions, or end-to-end behavior must be verified.  
**Produces:** browser-level evidence and reproducible E2E checks.  
**Take from it:** functional browser verification.  
**Do not confuse with:** `visual-qa`, which owns whether the rendered UI looks right.

### `visual-qa`

**Path:** [`skills/visual-qa/SKILL.md`](skills/visual-qa/SKILL.md)  
**Origin:** local  
**Optional tooling:** browser rendering, screenshots, reference images.  
**Use when:** implemented UI must be compared against Figma, screenshots, `DESIGN.md`, or approved visual intent.  
**Produces:** visible discrepancy findings and evidence-driven iteration.  
**Take from it:** spacing, hierarchy, typography, overflow, breakpoint and visual-regression checks.  
**Do not use it to:** invent a new design because the reviewer personally prefers one.

### `accessibility-review`

**Path:** [`skills/accessibility-review/SKILL.md`](skills/accessibility-review/SKILL.md)  
**Origin:** local  
**Use when:** interactive UI needs semantic HTML, keyboard, focus, labeling, contrast, touch target, screen-reader, or reduced-motion review.  
**Produces:** accessibility-specific findings and remediation.  
**Take from it:** accessibility audit discipline.  
**Do not use it to:** broadly redesign unrelated visual choices.

### `performance-review`

**Path:** [`skills/performance-review/SKILL.md`](skills/performance-review/SKILL.md)  
**Origin:** local  
**Optional tooling:** browser profiler, framework profiler, bundle analysis, metrics.  
**Use when:** performance is a stated concern or evidence indicates a bottleneck.  
**Produces:** measured diagnosis and prioritized fixes.  
**Take from it:** evidence-based performance work.  
**Do not use it to:** propose speculative rewrites without measurements.

---

## Review and release

### `code-review`

**Path:** [`skills/code-review/SKILL.md`](skills/code-review/SKILL.md)  
**Origin:** local  
**Use when:** a completed change needs correctness, regression, maintainability, error handling, type, or meaningful quality review.  
**Produces:** confidence-weighted actionable findings.  
**Take from it:** defect-oriented review, not stylistic churn.  
**Handoff:** security-sensitive findings → `security-review`.

### `security-review`

**Path:** [`skills/security-review/SKILL.md`](skills/security-review/SKILL.md)  
**Origin:** local  
**Use when:** a change touches authentication, authorization, secrets, untrusted input, trust boundaries, uploads, sensitive APIs, permissions, or other security-relevant surfaces.  
**Produces:** threat-focused security findings and mitigations.  
**Take from it:** security-specific review.  
**Do not use it to:** fill a report with general style and maintainability opinions.

### `release-check`

**Path:** [`skills/release-check/SKILL.md`](skills/release-check/SKILL.md)  
**Origin:** local  
**Use when:** implementation and focused reviews are complete and the change may be ready to merge/deploy/release.  
**Produces:** `SHIP`, `SHIP WITH KNOWN RISKS`, or `NO-SHIP`, backed by checks actually run or authoritatively observed.  
**Take from it:** final evidence aggregation and release gating.  
**Do not use it to:** redo architecture, design, implementation, or pretend unavailable checks passed.

### `reliability-review`

**Path:** [`skills/reliability-review/SKILL.md`](skills/reliability-review/SKILL.md)<br>
**Origin:** local; [source note](skills/reliability-review/SOURCE.md)<br>
**Status:** experimental<br>
**Use when:** a networked, persistent, transactional, background, or multi-step
workflow must survive timeouts, restarts, cancellation, duplicate delivery, or
partial failure.<br>
**Produces:** failure scenarios, current behavior, inconsistency risk,
recommended recovery semantics, and verification.<br>
**Take from it:** what happens when the happy path does not hold.<br>
**Do not use it to:** diagnose an already observed defect, or optimize latency.<br>
**Handoff:** `debugging` for a reproducible failure; `observability-review` when
the failure would be invisible.

### `observability-review`

**Path:** [`skills/observability-review/SKILL.md`](skills/observability-review/SKILL.md)<br>
**Origin:** local; [source note](skills/observability-review/SOURCE.md)<br>
**Status:** experimental<br>
**Use when:** production failures, background jobs, integrations, or async
workflows are hard to reproduce or explain.<br>
**Produces:** diagnostic blind spots, the minimum additional signals worth
adding, and the privacy or noise trade-offs they carry.<br>
**Take from it:** whether a real failure could be understood after the fact.<br>
**Do not use it to:** justify more logging as an end in itself, or to log secrets
and unnecessary personal data.<br>
**Handoff:** `debugging` once a defect becomes reproducible; `security-review`
when diagnostic output exposes sensitive data.

---

## Project audits

### `project-audit`

**Path:** [`skills/project-audit/SKILL.md`](skills/project-audit/SKILL.md)<br>
**Origin:** local; [source note](skills/project-audit/SOURCE.md)<br>
**Status:** experimental; `ASK` routing, explicit request only<br>
**Use when:** the user asks for project-wide engineering risks, debt, or rework
exposure rather than one change or one defect.<br>
**Produces:** evidence-backed findings by severity, the specialist handoffs it
used, and a Now/Next/Later technical roadmap.<br>
**Take from it:** breadth-first discovery of where deeper review is justified.<br>
**Do not use it to:** replace specialist depth, produce a lint report, or
implement broad fixes during discovery.<br>
**Handoff:** the specialist owner for each deep dive.

### `interdisciplinary-project-audit`

**Path:** [`skills/interdisciplinary-project-audit/SKILL.md`](skills/interdisciplinary-project-audit/SKILL.md)<br>
**Origin:** local; [source note](skills/interdisciplinary-project-audit/SOURCE.md)<br>
**Status:** experimental; `ASK` routing, explicit request only<br>
**Use when:** the owner wants to know what they may not realize they should be
asking, across product, UX, engineering, operations, data, and business.<br>
**Produces:** risks and blind spots, improvements, opportunities,
simplifications, and a Now/Next/Later/Avoid roadmap.<br>
**Take from it:** cross-discipline blind spots grounded in the actual product.<br>
**Do not use it to:** generate a generic feature wishlist, or to change the
project during the audit.<br>
**Handoff:** `project-audit` for technical depth; `product-spec` once a direction
is chosen.

---

## Utility

### `credit-codex-contributor`

**Path:** [`skills/credit-codex-contributor/SKILL.md`](skills/credit-codex-contributor/SKILL.md)  
**Origin:** local utility  
**Use when:** the user explicitly wants Codex to appear in GitHub's Contributors list through a co-authored commit.  
**Produces:** one safe empty attribution commit and push under strict repository-state rules.  
**Take from it:** the exact attribution workflow only.  
**Do not generalize it to:** README credits, other contributors, history rewrites, or unrelated Git operations.

---

## How to add notes for a new skill

When adding a new skill, add it to both this file and [`skills/registry.yaml`](skills/registry.yaml). Record at least:

- name and path
- category
- primary responsibility
- origin/provenance
- use-when trigger
- what it produces
- important non-goals
- optional/required tooling
- handoffs / related skills
- status (`active`, `experimental`, `deprecated`)

If imported from upstream, also add a `SOURCE.md` next to the skill with repository, path, revision, retrieval date, local modifications, and license notes.

## Maintenance rule

`SKILL.md` is the authority for execution instructions. This catalog is the authority for **discovery, provenance, relationships, and human/AI navigation**. If they disagree, fix the catalog rather than silently changing the skill's runtime behavior here.
