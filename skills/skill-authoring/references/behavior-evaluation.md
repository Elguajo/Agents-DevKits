> Local protocol informed by Superpowers behavior-driven skill authoring. Load only when a proposed rule or workflow claims to prevent a specific agent failure.

# Behavior Evaluation

## Goal

Show that a skill-library change addresses a concrete observed failure without adding routing noise, generic boilerplate, or an unsupported benchmark claim.

## Workflow

1. State the observed failure in a reproducible task or routing scenario, including the unsafe or incorrect behavior it permits today.
2. Define the smallest rule, reference, metadata change, or evaluation that should prevent it. Do not add a new skill before excluding an existing owner.
3. Add a positive scenario or pilot that asserts the required behavior and a near-miss or negative scenario that prevents over-triggering, bypass, or safety regression.
4. Run the deterministic registry/routing checks and the relevant focused test. Treat pilot assertions as a contract, not a measured model result.
5. Keep the evidence with the change and report what was observed, unavailable, or still requires a real-world model evaluation.

## Rules

- Do not claim an agent behavior improved without a baseline failure, reproducible task, or explicit limitation.
- Do not turn every documentation edit into a model benchmark or a new test framework.
- A passing router scenario proves routing only; it does not prove that a model followed the full workflow.
- Preserve existing safety, authorization, and precedence rules while testing an adaptation.

## Output

Return the baseline failure, minimal intervention, positive and negative evidence, commands run, observed result, and remaining model-evaluation limitation.
