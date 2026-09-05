# Render, Critique, and Fix Loop

The loop exists to check the refinement against the same states that produced
the findings, instead of against memory or intention.

## Pass 1 — Render
Re-capture the baseline set: same screens, same states, same viewports, same theme.
A comparison across different states proves nothing.

## Pass 2 — Compare

For each captured pair, answer:

- Is the hierarchy actually clearer, or only different?
- Did visual noise decrease?
- Is the product still recognizably itself?
- Are spacing and type more coherent across the screen, not just locally?
- Are interactive states complete and consistent?
- Did any important content become harder to find?
- Did the change introduce generic machine-generated premium styling?
- Did responsive behavior regress at the narrow viewport?
- Does motion improve comprehension rather than merely add activity?

Record any regression as a finding, including regressions the plan did not anticipate.

## Pass 3 — Fix
Correct the material discrepancies first. Re-render the affected states.

## When to stop
- Stop when the targeted P0 and P1 findings are resolved or explicitly deferred.
- A second or third pass is often justified; unlimited iteration is not.
- Do not keep polishing details that no finding named.
- Formal final visual evidence belongs to `visual-qa`, not to this loop.

## Reporting
State what was rendered and what was not. An unrendered state is reported as
unverified, never as improved.
