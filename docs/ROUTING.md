# Skill Routing Index

<!-- Generated from skills/registry.yaml by scripts/generate_routing_index.py; do not edit manually. -->

A compact selection aid for Codex and Claude Code. The registry is the machine-readable
source of truth; each selected `SKILL.md` is the execution source of truth.
Project instructions, task-specific source of truth, and an explicit user request take precedence.

## Selection levels

- **AUTO** — select only when the task and a skill boundary match; state the selected skills briefly.
- **PROPOSE** — announce the recommended workflow and continue unless the user redirects; this is not an approval gate.
- **ASK** — do not select automatically; require an explicit user request. This tier never overrides separate safety or authorization rules.

## Index

### AUTO

| Skill | Use when |
| --- | --- |
| `product-spec` | requirements are ambiguous, broad, or incomplete |
| `ux-research` | user needs to reduce product or UX uncertainty with research, usability evidence, or a defensible research plan |
| `information-architecture` | product or site structure must be defined or revised before detailed UI implementation |
| `journey-mapping` | a persona journey, service delivery flow, empathy map, or user story map must inform prioritization or structural decisions |
| `codebase-explorer` | an existing repository must be understood before changing or debugging it |
| `project-knowledge` | recurring project facts should be recorded in a source-grounded pack without creating a new generic skill |
| `solution-architecture` | a change crosses modules, data flows, integrations, persistence, or architectural boundaries |
| `frontend-design` | visual direction must be invented or significantly shaped |
| `design-system` | the repository already has a design system, DESIGN.md, theme tokens, or established UI patterns |
| `figma-to-code` | Figma frames, nodes, screenshots, or approved references are the source of truth |
| `responsive-design` | a UI must adapt across viewport sizes or input modes |
| `motion-design` | motion materially improves interaction or visual communication |
| `debugging` | observed behavior is wrong and the root cause is unknown |
| `testing` | meaningful behavior needs automated non-browser coverage |
| `playwright-testing` | navigation, forms, browser state, network interactions, or end-to-end flows must be verified |
| `visual-qa` | rendered UI must match Figma, screenshots, DESIGN.md, or approved visual intent |
| `accessibility-review` | interactive UI needs semantic, keyboard, focus, labels, contrast, touch target, screen-reader, or reduced-motion review |
| `performance-review` | performance is a stated concern or measurements indicate a bottleneck |
| `code-review` | a completed change needs independent engineering review |
| `security-review` | a change touches auth, authorization, secrets, untrusted input, uploads, permissions, sensitive APIs, or other security-relevant surfaces |
| `release-check` | implementation and focused reviews are complete and a change may be ready to merge, deploy, or release |
| `apply-aesthetic` | a UI needs deliberate visual character without overriding an approved reference or brand |
| `design-code` | a component or screen must be implemented in a specific framework |
| `design-component` | a UI primitive needs explicit anatomy, variants, states, tokens, and accessible interaction behavior |
| `design-qa` | a UI needs a deliberate quality-gate plan or a consolidated QA report |
| `design-review` | a design needs structured critique beyond exact reference-fidelity checking |
| `design-tokens` | design tokens need to be created, extended, audited, or migrated |
| `figma-integration` | a project needs to synchronize tokens or component variants between Figma and code |
| `token-build` | validated tokens must generate one or more platform-specific theme outputs |
| `ux-writing` | buttons, labels, errors, empty states, notifications, or other UI copy needs creation or review |
| `affine-notion-graph-sync` | the user provides a Notion page link and asks for an AFFiNE graph, canvas, mind map, flow, or block diagram |

### PROPOSE

| Skill | Use when |
| --- | --- |
| `feature-development` | a feature benefits from definition, exploration, architecture, implementation, verification, and review |
| `ux-usability-audit` | a real website or application must be reviewed or improved as a human user would experience it, beyond visual fidelity and functional correctness |
| `apple-quality-interface-refinement` | an existing interface already has product and design direction but feels unfinished, inconsistent, visually weak, static, or less polished than intended, especially when Apple-level clarity, restraint, or craft is requested |
| `change-impact-analysis` | a shared API, schema, persisted identifier, event contract, or core component is about to change and its consumers are unclear |
| `data-storage-review` | durable application data needs review of source of truth, growth, retention, integrity, or recovery |
| `data-migration` | a persisted schema, format, identifier, preference, or sync contract changes and existing data must survive |
| `concurrency-review` | async tasks, threads, actors, queues, jobs, event handlers, or shared mutable state create ordering or duplication risk |
| `reliability-review` | a networked, persistent, transactional, background, or multi-step workflow must survive timeouts, restarts, duplicates, or partial failure |
| `observability-review` | important failures, background jobs, integrations, or async workflows are hard to reproduce or explain |

### ASK

| Skill | Use when |
| --- | --- |
| `refactor` | behavior is correct but implementation is unnecessarily complex, duplicated, or difficult to maintain |
| `credit-codex-contributor` | the user explicitly requests Codex contributor attribution |
| `brandkit` | a product needs an accessible token foundation before screen-level design |
| `governance` | a token or component contract changes in a way that affects reuse, versioning, or migration |
| `image-to-code` | an image or mockup is the main visual reference for a requested UI implementation |
| `migrate-design-system` | a project must adopt, bridge, or migrate a component or token system |
| `prototype` | an uncertain product or interaction question should be tested before production implementation |
| `redesign` | an existing product UI needs deliberate quality improvement without an implicit feature rewrite |
| `project-audit` | the user explicitly asks for project-wide engineering risks, debt, or rework exposure rather than one change or one defect |
| `interdisciplinary-project-audit` | the user explicitly asks what they may not realize they should be asking before continuing development |
