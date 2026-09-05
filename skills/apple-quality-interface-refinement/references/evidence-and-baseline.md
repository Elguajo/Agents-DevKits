# Evidence and Baseline

A refinement claim is only as strong as the evidence behind it. Establish what
you can actually observe before writing findings.

## Evidence classes

| Class | Meaning | Typical source |
| --- | --- | --- |
| Observed, rendered | Visible in the running interface | live render, browser automation, screenshot |
| Observed, code | Confirmed in the implementation | component source, tokens, stylesheets |
| Inferred | Plausible from surrounding evidence, not confirmed | a hover style read from CSS but never triggered |
| Not assessable | Cannot be checked with current access | screen-reader output with no assistive tooling |

Label every important finding. An audit that mixes the classes silently is not reviewable.

## What a static image cannot prove
- hover, focus-visible, pressed, or selected appearance;
- transition duration, easing, or jank;
- keyboard order and focus trapping;
- loading, latency, and perceived responsiveness;
- screen-reader names, roles, and states;
- reduced-motion behavior;
- what happens below the fold or after interaction.

If the request depends on any of these and rendering is unavailable, say so and
name the check that would settle it.

## Baseline capture

Capture before editing. Keep it small and representative:

- the primary screen at the default viewport;
- one complete workflow, including its intermediate state;
- open and closed states of the most important disclosure or overlay;
- empty, loading, and error states when they exist;
- one narrow viewport when responsive behavior is in scope.

Record for each capture what page, state, viewport, and theme it represents.
A baseline whose state is undocumented cannot be compared later.

## Rules
- Never state a measured value you did not measure.
- Never invent text that is unreadable in the evidence.
- Prefer a short list of well-evidenced findings over a padded audit.
- When evidence and code disagree, trust the render and investigate the difference.
