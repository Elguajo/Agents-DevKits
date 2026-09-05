# Skill Invocation Cookbook

This file is a human-facing **copy-paste prompt cookbook** for the skills shipped by Agents DevKits.

It is intentionally separate from the authoritative routing and execution files:

- [`../SKILLS.md`](../SKILLS.md) — human-readable ownership, triggers, provenance, and handoffs;
- [`registry.yaml`](registry.yaml) — machine-readable routing metadata;
- each `skills/<skill>/SKILL.md` — authoritative execution instructions.

These examples do **not** replace a skill's own instructions. They simply give a practical starting prompt when you want to invoke a skill explicitly.

## Invocation syntax

Use the skill name explicitly when you want a particular workflow.

**Codex**

```text
$skill-name

Your task and context here.
```

**Claude Code**

```text
/skill-name

Your task and context here.
```

If your agent supports automatic skill routing, you can also describe the task normally and let the router choose the relevant skill.

---

## Product, research, architecture, and orchestration

### `product-spec`

```text
$product-spec

Turn this idea into a concise implementation-ready product specification.
Define scope, non-goals, important states, edge cases, constraints, and acceptance criteria.
Do not choose technical architecture yet.

Idea:
[describe the feature or product change]
```

### `ux-research`

```text
$ux-research

Help me answer this product/UX decision with the lightest defensible research approach.
Separate existing evidence from assumptions, identify what we still need to learn, and produce a practical research or synthesis plan.

Decision:
[describe the decision or uncertainty]
```

### `information-architecture`

```text
$information-architecture

Review and improve the information architecture for this product area.
Focus on navigation, content hierarchy, route semantics, labels, and user flows before detailed visual design or implementation.

Context:
[describe the current structure or provide relevant files/screens]
```

### `journey-mapping`

```text
$journey-mapping

Map the end-to-end user journey for this scenario.
Keep observed evidence separate from assumptions, identify important moments of truth, friction, opportunities, and the decisions this journey should inform.

Scenario:
[describe the user, goal, and context]
```

### `codebase-explorer`

```text
$codebase-explorer

Inspect this repository before making changes.
Explain the relevant entry points, data flow, dependencies, conventions, similar implementations, and constraints that matter for this task.
Do not propose a new architecture until the current implementation is understood.

Task:
[describe what I am planning to change]
```

### `project-knowledge`

```text
$project-knowledge

Build a concise source-grounded knowledge reference for this project concern.
Extract verified facts from the repository, clearly separate inference from evidence, and record unresolved questions without inventing answers.

Concern:
[design system / API / data model / project convention / other]
```

### `affine-notion-graph-sync`

```text
$affine-notion-graph-sync

Use this Notion page as the source and create or update the corresponding AFFiNE Edgeless Canvas graph according to the skill workflow.
Preserve existing user-owned state and do not invent relationships that are not supported by the source.

Notion page:
[URL]
```

### `solution-architecture`

```text
$solution-architecture

Design the smallest coherent technical approach for this change.
Account for the current codebase, affected boundaries, dependencies, data flow, risks, implementation order, and verification strategy.
Do not expand product scope or visual direction.

Change:
[describe the requirement]
```

### `feature-development`

```text
$feature-development

Implement this non-trivial feature through the relevant Agents DevKits specialists.
Select only the skills justified by the task, preserve the current architecture where appropriate, and carry the work through implementation and verification.

Feature:
[describe the feature and acceptance criteria]
```

### `change-impact-analysis`

```text
$change-impact-analysis

Analyze the blast radius of this proposed change before implementation.
Find confirmed consumers, hidden coupling, affected contracts or persisted data, and classify the real regression risk with evidence.
Do not implement the change yet.

Proposed change:
[describe the API/schema/component/contract change]
```

---

## Frontend, UX, and design system

### `frontend-design`

```text
$frontend-design

Create a strong visual direction for this interface based on the product, users, and content rather than a generic template.
Define the design intent first, then implement the relevant frontend experience with deliberate typography, layout, hierarchy, and visual character.

Context:
[describe the screen/product and desired outcome]
```

### `apply-aesthetic`

```text
$apply-aesthetic

Apply a coherent visual direction to this existing UI using the current token system and product context.
Improve the aesthetic without creating unrelated one-off styling or bypassing the existing design system.

Target:
[screen/component/area]
```

### `brandkit`

```text
$brandkit

Create a practical visual foundation for this new product.
Define the core brand direction and the minimum reusable visual decisions needed for downstream tokens and implementation.

Product:
[describe product, audience, positioning, and references]
```

### `design-tokens`

```text
$design-tokens

Design or refine the semantic token architecture for this interface system.
Map visual decisions into reusable semantic tokens, preserve meaningful existing conventions, and avoid hardcoded component-specific values where a shared token is justified.

Scope:
[colors / spacing / typography / radii / motion / full token set]
```

### `design-component`

```text
$design-component

Define the reusable contract for this UI component.
Cover its purpose, variants, states, content behavior, accessibility-relevant behavior, and relationship to the existing token/component system before framework implementation.

Component:
[name and context]
```

### `design-code`

```text
$design-code

Implement this UI using the project's existing design tokens, reusable components, and framework conventions.
Keep the implementation consistent with the design system and prepare it for visual and browser verification.

UI requirement:
[describe or link the approved design]
```

### `design-qa`

```text
$design-qa

Build a focused UI evidence and coverage matrix for this design change.
Identify which screens, states, breakpoints, and specialist reviews need evidence before the change can be considered complete.

Change:
[describe the UI work]
```

### `design-review`

```text
$design-review

Review this interface as an expert UI design reviewer.
Assess the current design quality, coherence, hierarchy, consistency, and important weaknesses, and distinguish material issues from subjective preference.

Target:
[URL / screenshots / implementation]
```

### `figma-integration`

```text
$figma-integration

Check and improve parity between Figma and the implemented design system.
Focus on token mapping, variants, component semantics, and places where Figma and code have drifted.

Figma / code context:
[links or relevant files]
```

### `governance`

```text
$governance

Review this design-system change for compatibility, ownership, deprecation, and migration concerns.
Recommend how the system should evolve without silently breaking existing consumers.

Change:
[describe the component/token/API change]
```

### `image-to-code`

```text
$image-to-code

Reconstruct this supplied interface image into maintainable UI code.
Use the image as visual evidence, infer only what can be supported, reuse the project's design system, and do not invent hidden behavior from a static screenshot.

Source image:
[attach image]
```

### `migrate-design-system`

```text
$migrate-design-system

Plan and execute a controlled migration from the current UI system to the target design-system roles.
Preserve compatibility where required, identify affected consumers, and avoid a visual rewrite with no migration strategy.

Current → target:
[describe the migration]
```

### `prototype`

```text
$prototype

Choose and build the lowest useful prototype fidelity for this question.
Make the prototype sufficient to validate the important uncertainty, and state what should be learned before committing to full implementation.

Question to validate:
[describe the idea or risky assumption]
```

### `redesign`

```text
$redesign

Audit this existing interface before changing it, then propose and implement a focused redesign based on the actual problems found.
Preserve what already works and avoid redesigning unrelated areas merely for visual novelty.

Target:
[URL / screen / component]
```

### `token-build`

```text
$token-build

Generate or update the reproducible platform outputs from the approved design-token source.
Preserve the token architecture, report generated artifacts, and surface any incompatible or ambiguous mappings.

Token source / target platforms:
[describe]
```

### `ux-writing`

```text
$ux-writing

Review and improve the interface language for this flow.
Make labels, actions, validation, empty states, errors, and guidance concise, inclusive, consistent, and understandable in the user's terms.

Flow / copy:
[provide current UI text or context]
```

### `design-system`

```text
$design-system

Inspect the existing design system before implementing this UI change.
Identify the tokens, components, patterns, and conventions that should be reused, and recommend the smallest system change only where reuse is insufficient.

UI task:
[describe the target]
```

### `figma-to-code`

```text
$figma-to-code

Implement this supplied Figma/reference design faithfully in the current codebase.
Treat the supplied design as the visual source of truth, reuse the existing design system where compatible, and verify the rendered result afterward.

Figma/reference:
[link]
```

### `responsive-design`

```text
$responsive-design

Audit and implement the cross-viewport behavior for this interface.
Preserve content priority and interaction logic across relevant viewport sizes instead of merely shrinking the desktop layout.

Target:
[screen/component and supported viewports]
```

### `motion-design`

```text
$motion-design

Design the motion and interaction timing for this interface with a clear purpose for every transition.
Use motion to communicate continuity, state, hierarchy, or feedback; avoid decorative animation that slows repeated work.

Target interaction:
[describe the flow/component]
```

### `visual-qa`

```text
$visual-qa

Verify the rendered interface against the intended design and existing visual system.
Use actual browser/screenshots where available, report visible mismatches with evidence, and distinguish regressions from subjective preference.

Target:
[URL / route / reference]
```

### `accessibility-review`

```text
$accessibility-review

Audit this interface for accessibility and remediate the issues that can be verified.
Check the relevant semantic, keyboard, focus, contrast, state, and assistive-technology concerns without claiming passes that were not actually tested.

Target:
[screen/flow/component]
```

### `ux-usability-audit`

```text
$ux-usability-audit

Use the actual interface like a real user and perform a senior usability audit before changing it.
Identify problems in user flows, navigation, hierarchy, interaction logic, states, forms, feedback, and comprehension, grounded in observed evidence.
Use relevant production references where they help explain a stronger pattern.

Target:
[URL / application / flow]
```

---

## Engineering, debugging, testing, and release

### `debugging`

```text
$debugging

Investigate this defect from evidence to root cause before changing code.
Reproduce it where possible, isolate the failing mechanism, make the smallest safe fix, and verify that the underlying repeated or incorrect behavior is actually gone.

Observed behavior:
[describe the bug and reproduction steps]
```

### `refactor`

```text
$refactor

Refactor this area while preserving observable behavior.
Establish the current invariants first, simplify the structure without mixing in unrelated features, and verify that behavior remains unchanged.

Target:
[file/module/component]
```

### `testing`

```text
$testing

Add focused automated coverage for the meaningful behavior in this change.
Prioritize tests that protect real contracts, edge cases, failures, and regressions rather than maximizing test count.

Target behavior:
[describe the feature/bug/change]
```

### `playwright-testing`

```text
$playwright-testing

Verify this web flow in a real browser with Playwright.
Exercise the relevant user path and important states, collect objective evidence, and report failures precisely instead of relying only on code inspection.

Flow:
[URL / route / steps]
```

### `exploratory-qa-audit`

```text
$exploratory-qa-audit

Perform a full exploratory QA pass on this running product.
Use it like a senior QA engineer and actively try to discover defects nobody has reported yet.
Exercise the critical journeys first, then vary inputs, repeat and interrupt actions, use back/forward/refresh/deep links, check loading, error, empty, session and persistence states, and watch the browser console and network for failures tied to what you exercised.
Reproduce each candidate before calling it a defect, and report expected, actual, minimal steps, evidence, severity, confidence, and user impact.
Do not start fixing anything until the discovery evidence is recorded; hand confirmed defects to debugging.

Target:
[URL / local application / scope]
```

### `performance-review`

```text
$performance-review

Investigate this performance concern with evidence before optimizing.
Measure or profile the relevant path, identify the real bottleneck, explain why it degrades, then recommend or implement the smallest justified improvement and verify the result.

Symptom:
[slow startup / interaction / memory / rendering / data growth / other]
```

### `code-review`

```text
$code-review

Review this implementation as an independent senior engineer.
Do not assume the previous implementation is correct. Check correctness, regressions, maintainability, architecture fit, edge cases, and the adequacy of verification using actual code evidence.

Scope:
[current diff / feature / implementation]
```

### `security-review`

```text
$security-review

Perform a focused security review of this change.
Map the relevant trust boundaries and inspect untrusted input, authorization, sensitive data, secrets, injection, unsafe operations, and other concrete risks supported by the implementation.

Scope:
[feature/module/change]
```

### `release-check`

```text
$release-check

Perform the final evidence-based ship/no-ship review for this release.
Use only checks that were actually performed, identify release-blocking risks and remaining uncertainty, and give a clear verdict with the evidence behind it.

Release scope:
[version / branch / feature set]
```

### `concurrency-review`

```text
$concurrency-review

Review this implementation for concurrency, ordering, cancellation, and shared-state problems.
For every suspected issue, describe a plausible execution sequence and distinguish confirmed risk from theoretical possibility.

Target:
[module/flow/async code]
```

### `reliability-review`

```text
$reliability-review

Review this feature for failure, retry, idempotency, recovery, and partial-operation semantics.
Assume dependencies can fail or operations can be interrupted or repeated, and identify where the system could be left inconsistent.

Target:
[feature/integration/job/workflow]
```

### `observability-review`

```text
$observability-review

Audit whether failures in this feature can be diagnosed in production.
Review the available logs, error context, identifiers, state transitions, and other relevant signals, and identify only gaps that would materially hinder debugging.

Target:
[feature/service/module]
```

---

## Durable data

### `data-storage-review`

```text
$data-storage-review

Audit the durable data model and storage behavior for this product area.
Map the source of truth, read/write lifecycle, growth, retention, cleanup, integrity, and recovery expectations, and identify evidence-based risks.

Target data:
[database/storage/preferences/cache/history/etc.]
```

### `data-migration`

```text
$data-migration

Design a safe migration for this persisted schema or data-format change.
Preserve existing user data, define invariants and compatibility expectations, plan rollback or recovery, and verify against representative legacy data.

Migration:
[current format → target format]
```

---

## Project-wide audits and utilities

### `project-audit`

```text
$project-audit

Perform a breadth-first technical health audit of this repository.
Understand the codebase first, identify the concerns that actually need specialist review, prioritize material engineering risks, and avoid turning the audit into a generic wishlist.
Do not implement unrelated changes during the discovery pass.
```

### `interdisciplinary-project-audit`

```text
$interdisciplinary-project-audit

Review this project as an interdisciplinary senior product team and identify blind spots I may not know to ask about.
Use only the disciplines that are relevant, ground findings in the current project, and separate risks, improvements, opportunities, unnecessary complexity, important concepts, and questions that should influence the roadmap.
Do not change the project yet.
```

### `credit-codex-contributor`

```text
$credit-codex-contributor

Apply the repository's safe Codex-contributor attribution workflow to this GitHub change.
Follow the skill's attribution rules exactly and report what metadata or commit/PR information was changed.

Target change:
[commit / branch / pull request]
```

---

## Practical usage patterns

### Let the router choose

For normal work, the best prompt is often simply the task itself:

```text
The settings screen becomes slow after a large history builds up. Investigate the root cause and fix it without losing existing user data.
```

A routing-capable agent can select `debugging`, then hand off to `data-storage-review`, `data-migration`, `performance-review`, or `testing` only if the evidence justifies them.

### Explicitly select one skill

Use explicit invocation when you already know the workflow you want:

```text
$code-review

Review the implementation made by the previous agent. Inspect the actual code and verification evidence; do not assume it is correct.
```

### Combine a skill with task-specific focus

```text
$ux-usability-audit

Audit the current website as a real first-time user.
Focus especially on navigation, discoverability, primary actions, and mobile behavior.
Use strong production references when they clarify a better interaction pattern.
```

### Do not manually chain every skill

Avoid prompts such as:

```text
Run product-spec, architecture, frontend-design, design-system, responsive-design,
motion-design, accessibility, testing, security and release-check for this tiny button change.
```

`feature-development` and the router exist so the agent can select only the specialist workflows justified by the change.
