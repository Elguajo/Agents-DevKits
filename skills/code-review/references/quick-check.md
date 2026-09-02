> Integrated from the v0.1 prompt/skill prototype `quick-check`. Load this reference only when its trigger applies.

# Quick Check
## Goal
Catch obvious correctness or regression issues with minimal overhead.

## Workflow
1. Read the requested change and the directly affected code.
2. Check that the implementation matches the requirement.
3. Inspect immediate call sites or dependencies likely to regress.
4. Run the smallest relevant test/type/build checks available.
5. Flag any reason the change requires a deeper review.

## Rules
- Keep scope local.
- Do not turn this into a full-project audit.
- Escalate when the change touches data migrations, authentication, concurrency, public APIs, or shared architecture.

## Output
PASS / NEEDS REVIEW, followed by concise findings and checks performed.
