> Local protocol informed by Ponytail's over-engineering review concept. Load only for an explicit minimality or over-engineering review of a completed change.

# Minimality and Over-Engineering Review

## Goal

Find concrete, evidence-backed complexity in a completed diff that can be removed, reused, or replaced without weakening required behavior.

## Workflow

1. Read the change goal, project constraints, diff, and enough surrounding code to understand the affected flow.
2. Check whether the diff duplicates repository functionality, a language/standard-library capability, a native platform capability, or an already-installed dependency.
3. Check whether each added dependency, wrapper, abstraction, extension point, configuration layer, state layer, or service has a present consumer or required boundary.
4. Recommend deletion, reuse, or a smaller direct change only when behavior and constraints remain satisfied; otherwise record why the added complexity is justified.
5. Give each finding a location, evidence, the minimal safe alternative, and the consequence of leaving it.

## Rules

- Review a concrete diff, not a repository-wide backlog; repository-wide discovery belongs to `project-audit` and behavior-preserving cleanup belongs to `refactor`.
- Do not optimize for fewest lines, zero dependencies, or personal style.
- Never flag required validation, trust-boundary checks, error/recovery handling, security, accessibility, compatibility, reliability, or data-integrity/data-loss protections as removable complexity.
- Do not apply changes in this review; hand implementation to the appropriate owner.

## Output

Return only actionable findings and justified keeps. Each finding includes location, evidence, minimal safe alternative, and expected maintenance or correctness benefit. If no evidence-backed simplification exists, say so plainly.
