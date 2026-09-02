> Integrated from the v0.1 prompt/skill prototype `root-cause-debugging`. Load this reference only when its trigger applies.

# Root Cause Debugging
## Goal
Establish the actual root cause with evidence, implement the smallest correct fix, and verify the underlying problem is gone.

## Workflow
1. Understand the affected architecture, data/state/event flow, lifecycle, and relevant files.
2. Reproduce the issue and establish a baseline.
3. Instrument only what is needed to distinguish competing hypotheses.
4. Separate symptoms from mechanisms: re-render vs remount, retry vs duplicate invocation, cache hit vs refetch, stale state vs reinitialization, frontend symptom vs backend cause.
5. Identify the smallest responsible mechanism and the evidence that confirms it.
6. Implement the smallest architecturally correct fix.
7. Re-run the original scenario and relevant checks.
8. Add or update a regression test when practical.

## Rules
- Investigate before editing.
- Treat proposed causes as hypotheses until proven.
- Do not hide symptoms with delays, retries, CSS, forced refreshes, swallowed errors, or disabled synchronization unless that behavior is the correct design.
- Preserve legitimate updates and unrelated behavior.
- If reproduction or verification is impossible, state that explicitly.

## Output
Report: root cause, evidence, relevant files, change made, verification, regression coverage, and remaining risks.
