---
name: design-component
description: Specify a reusable UI component's anatomy, variants, states, token roles, accessibility behavior, and implementation contract before code is written.
---

# Design Component

Design a reusable component contract, not an isolated mockup. Use it when a UI element needs explicit behavior and consistency before implementation.

## Workflow

1. Check whether an existing primitive already satisfies the need. Prefer extending a stable component over creating a near-duplicate.
2. Define the component's purpose, anatomy, public variants, sizes, content constraints, and applicable interaction states.
3. Map each visual decision to semantic or component tokens. Specify responsive, loading, empty, error, and overflow behavior where relevant.
4. Describe accessible semantics, keyboard behavior, focus management, announcements, and touch-target requirements. Use `accessibility-review` for a formal audit.
5. Hand the approved specification to `design-code`; use `visual-qa` to inspect the rendered result.

For the detailed specification checklist, read [component-contract.md](references/component-contract.md).

## Completion evidence

Return a component contract, explicitly list non-applicable states, identify existing primitives reused, and note tests or reviews needed after implementation.
