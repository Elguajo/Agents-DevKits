# Safety-proof ladder for impact analysis

For a risky proposed change, name the one or two claims whose truth makes the
change safe. Record the strongest level actually reached:

1. Assertion only.
2. Source evidence from callers, schemas, paths, configuration, or data.
3. Failure-path reasoning that considers counterexamples and hidden coupling.
4. Executable proof through a focused command, test, static check, or fixture.
5. Runtime reproduction at the relevant real boundary.

Proportion matters: do not manufacture a runtime environment. But unavailable
executable or runtime proof leaves the safety claim unproven or partially proven.
Separate that uncertainty from cleared risks and confirmed consumers. This
pre-implementation proof map does not replace post-change `testing`,
`debugging`, or `code-review`.
