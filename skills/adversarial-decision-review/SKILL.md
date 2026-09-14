---
name: adversarial-decision-review
description: Challenge a non-trivial pre-implementation decision with one bounded fresh-context adversarial review. Use when a high-impact decision needs disproof before it becomes implementation.
---

# Adversarial Decision Review

Own **one bounded fresh-context adversarial review of a non-trivial decision before implementation**. Do not own solution design, final code review, or recursive multi-agent orchestration.

## Use when

- A decision changes an architectural boundary, public contract, authorization semantics, irreversible operation, or another invariant ordinary checks cannot prove.
- An unfamiliar or high-blast-radius approach needs an independent attempt to disprove it before implementation starts.

## Do not use when

- The operation is mechanical, local, and reversible.
- A concrete implementation needs post-change review; use `code-review`.
- The open work is choosing the technical approach; use `solution-architecture` first.
- The decision is already directly falsified by a focused test or authoritative evidence.

## Workflow

1. State the decision claim, why it matters, and the contract it must satisfy.
2. Extract the smallest reviewable artifact: proposal, relevant diff, or invariant plus the necessary constraints. Exclude the author’s conclusion.
3. Request exactly one fresh-context reviewer with an adversarial prompt that asks for contract violations, unstated assumptions, failure paths, hidden coupling, and counterexamples. Provide artifact and contract, not the claim.
4. Reconcile each finding as contract gap, actionable defect, accepted tradeoff, or noise. Correct the artifact or contract when the evidence warrants it.
5. Stop after one review/reconciliation cycle. A second cycle is permitted only after a material artifact change; stop and escalate after two total cycles, when findings are non-material, or when the user makes the tradeoff.
6. If fresh context is unavailable, report that limitation and hand the decision to a human or available independent reviewer; do not present self-critique as an independent review.

## Rules

- Never invoke this workflow from inside its reviewer. Reviewers do not spawn reviewers.
- Do not send private repository material to another model or external service without explicit authorization.
- Reviewer output is evidence, not a verdict; re-check it against the artifact and stated contract.
- Keep the artifact small. Decompose instead of increasing review cycles.

## Failure modes / anti-rationalization

- “A final code review will catch it” → course correction is cheaper before the decision is embedded in implementation.
- “I am confident” → confidence is not independent evidence for a high-impact invariant.
- “More reviewers are safer” → unbounded review creates noise and delay; use the stated stop condition.
- “I can review my own reasoning independently” → fresh context is the point; label any fallback as unavailable rather than equivalent.

## Handoffs

- Technical approach and alternatives → `solution-architecture`.
- Shared-contract blast radius → `change-impact-analysis`.
- Version-sensitive factual claim → `source-driven-implementation`.
- Concrete implementation review → `code-review`.
- Security, data migration, reliability, or concurrency concerns → the matching specialist.

## Output contract

Return the claim, artifact/contract scope, reviewer availability, findings with their reconciliation, stop condition reached, decision, and residual risks.
