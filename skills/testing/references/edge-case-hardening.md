> Integrated from the v0.1 prompt/skill prototype `edge-case-hardening`. Load this reference only when its trigger applies.

# Edge Case Hardening
## Goal
Find realistic cases that can break a working implementation before users do.

## Workflow
1. Understand the feature’s normal behavior and invariants.
2. Enumerate realistic boundaries: empty, minimum/maximum, malformed, duplicate, delayed, interrupted, repeated, old-version, offline, permission denied, partial data, and rapid user actions as relevant.
3. Trace each through actual code.
4. Prioritize by likelihood × impact.
5. Fix or add tests for high-value cases only.

## Rules
- Avoid hypothetical edge-case spam.
- Prefer cases supported by architecture, input domain, or known operational conditions.
- Do not over-engineer low-impact impossibilities.

## Output
High-value edge cases, current behavior, risk, recommended handling, and tests.
