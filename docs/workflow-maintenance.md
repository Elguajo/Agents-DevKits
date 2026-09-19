# Workflow maintenance and external research

Treat an external workflow repository as architecture research, not a prompt
source. Before adopting an idea, identify the exact problem it solves and check
whether Agents DevKits already has an owner.

Use this decision path:

```text
external implementation
        ↓
universal problem and measurable benefit?
        ↓
existing owner, reference, registry field, capability, adapter, validator, or eval
        ↓
regression coverage
```

Review each candidate against these questions:

1. Is it universal rather than domain- or vendor-specific?
2. Does it conflict with bounded ownership or duplicate a project-native tool?
3. Can it be represented declaratively without provider configuration?
4. Does it reduce uncertainty rather than add ceremony?
5. What is the fallback if the capability is unavailable?
6. Does it increase always-loaded context or create another source of truth?
7. What test, gate check, or scenario eval will catch a regression?

For recurring failures, first improve the existing owner: a skill procedure,
conditional reference, registry metadata, capability contract, adapter, validator,
or scenario eval. Create a new skill only when the responsibility is genuinely
distinct. Update the registry, boundaries, and tests in the same change.

Classify a run-derived lesson as **ONE-OFF**, **RECURRING LOCAL**, or
**SYSTEMIC** before making it durable. Prefer, in order, a schema/type/contract
that prevents invalid state; a validator or gate; a canonical helper; a test or
runtime check; then prose when judgment is necessary. A new skill is the last
option. A behavioral improvement claim needs deterministic routing/contract
evidence and, where empirical, a controlled live paired comparison; a routing
scenario pass is not a measured model-behavior result.

For high-risk or process-sensitive workflows, add a `Failure modes /
anti-rationalization` section only when it names realistic, task-specific ways
an agent can bypass the workflow. Do not add generic boilerplate to every skill.

The `skill-authoring` skill executes this decision path and the full change set
it implies. This document stays the policy; the skill stays the procedure.

Overlap that already exists in the library is not found by reading it. These are
enforced deterministically and fail `scripts/gate.py`:

- duplicate ownership between two skills
- empty `non_goals`, which is how a boundary becomes unbounded
- a skill that hands off or relates to itself
- two skills with identical trigger expressions, which routing cannot separate
- `trigger_values` entries no skill uses, excluding the routing depth facts
- `model`-invocable skills that no routing scenario selects or skips
- `model`-invocable skills that no task description reaches through `project.py route`
