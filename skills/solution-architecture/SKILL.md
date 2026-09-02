---
name: solution-architecture
description: Design the smallest clean technical approach for a feature by inspecting the existing codebase, identifying affected boundaries, comparing viable options, and producing an implementation plan. Use after requirements are clear and before non-trivial implementation.
---

# Solution Architecture

Own **how the feature should fit into the existing system**. Do not redefine product scope or visual direction.

## Use when
- A change affects multiple modules, data flows, integrations, or architectural boundaries.
- The repository has existing patterns that should be understood before implementation.
- There are meaningful trade-offs between implementation approaches.

## Do not use when
- The task is a trivial isolated fix.
- Requirements are still ambiguous; use `product-spec` first.
- The task is primarily visual design; defer to `frontend-design` and design-system guidance.

## Workflow
1. Read project instructions and architecture docs.
2. Inspect relevant code before proposing changes.
3. Find similar existing features and reusable abstractions.
4. Map affected modules, data flow, interfaces, persistence, external services, and failure boundaries.
5. Identify constraints: compatibility, performance, security, migrations, deployment, and testing.
6. Prefer the smallest coherent change that matches existing patterns.
7. Compare alternatives only when trade-offs are real; avoid ceremonial option lists.
8. Produce an ordered implementation plan with verification points.

## Progressive references

Load only the matching reference when it applies.

- [`references/implementation-preflight.md`](references/implementation-preflight.md) — understand enough to plan safely before touching code.
- [`references/solution-challenge.md`](references/solution-challenge.md) — challenge a proposed approach when several materially different options are genuinely viable.

## Architecture rules
- Reuse existing conventions unless there is a concrete reason not to.
- Do not introduce a new dependency, service, abstraction, or state layer without justification.
- Avoid speculative generalization for hypothetical future requirements.
- Preserve backward compatibility unless the task explicitly changes it.
- Surface risky assumptions instead of silently choosing business behavior.

## Output contract
Include:
- Current-system findings relevant to the change
- Recommended approach and why
- Affected files/modules or boundaries
- Data/control flow where useful
- Risks and migration considerations
- Implementation sequence
- Verification strategy

## Handoff
Implementation should follow the chosen architecture. UI implementation may additionally use `frontend-design`, `design-system`, or `figma-to-code`; verification belongs to the dedicated review/testing skills.
