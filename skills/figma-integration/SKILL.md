---
name: figma-integration
description: Keep Figma variables, component variants, and repository design tokens aligned through one declared source of truth and provider-neutral Figma capability checks.
---

# Figma Integration

Use this skill when design tokens or component contracts cross the Figma/code boundary. It does not configure credentials or assume a Figma provider is available.

## Workflow

1. Identify the authoritative side for this scope: code-to-Figma or Figma-to-code. Do not hand-edit both representations without a reconciliation plan.
2. Map primitive, semantic, and component roles to Figma collections, modes, variables, and component properties where the project supports them.
3. If Figma capability is available, use the provider's native workflow to inspect or update the declared target. If unavailable, produce a mapping artifact and report the limitation.
4. Compare component variants, states, names, and token references on both sides. Hand repository implementation to `figma-to-code` or `design-code`.
5. Preserve project instructions and approved files as the source of truth over generic mapping guidance.

Read [sync-contract.md](references/sync-contract.md) for a minimal sync record.

## Completion evidence

Return the authoritative direction, mapped collections/modes, parity gaps, observed sync results, and unavailable provider operations.
