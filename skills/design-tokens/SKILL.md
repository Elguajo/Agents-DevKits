---
name: design-tokens
description: Create, extend, or audit portable design tokens using primitive, semantic, and component layers without leaking one-off visual values into application code.
---

# Design Tokens

Maintain the design-system source of truth. Use this skill for token architecture and token changes, not for arbitrary CSS cleanup.

## Workflow

1. Inspect the repository's current token format, consumers, themes, and build pipeline before modifying values or names.
2. Keep primitive values separate from semantic roles and component scopes. Consumers should normally use semantic or component tokens, never raw palette values.
3. Define theme, density, brand, and state differences as deliberate overrides rather than duplicating whole systems.
4. Update aliases, documentation, and generated targets through the project pipeline. A token rename or removal must include a migration path.
5. Validate available token schemas and contrast-sensitive roles. Hand target generation to `token-build` and component consequences to `design-component`.

Read [token-schema.md](references/token-schema.md) when introducing or restructuring token files.

## Completion evidence

Report source files changed, semantic roles affected, compatibility implications, validation results, and remaining consumer migrations.
