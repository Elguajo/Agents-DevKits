> Integrated from the v0.1 prompt/skill prototype `architecture-fit-review`. Load this reference only when its trigger applies.

# Architecture Fit Review
## Goal
Evaluate structural fit without replacing a working design merely for aesthetic purity.

## Workflow
1. Understand current module/layer boundaries and ownership.
2. Trace where business rules, persistence, UI state, networking, and orchestration currently live.
3. Compare the implementation with existing patterns and dependency direction.
4. Identify duplicated domain logic, inappropriate coupling, cyclic dependencies, boundary leaks, or abstractions with no clear owner.
5. Estimate the cost of leaving it vs moving it now.
6. Recommend no change when the architecture cost is low.

## Rules
- Working code is not automatically architecturally wrong.
- Do not propose a rewrite without a concrete maintenance or correctness benefit.
- Prefer incremental boundary corrections.

## Output
Fit assessment, evidence, debt/impact, recommended action, and timing: Now / Next / Later.
