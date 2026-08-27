# UI evidence matrix

For each scope item, state the source of truth and observed evidence.

| Concern | Objective evidence | Expert evidence | Owner |
| --- | --- | --- | --- |
| Token use | token/lint command when configured | consistency review | `design-system` |
| Interaction | browser assertion | usability review | `playwright-testing` |
| Accessibility | automated checks when configured | semantic and keyboard review | `accessibility-review` |
| Visual fidelity | screenshot comparison when available | discrepancy review | `visual-qa` |
| Responsive behavior | viewport checks when configured | layout review | `responsive-design` |

Mark every row as `passed`, `failed`, `unavailable`, `not_applicable`, or `inferred` according to the evidence contract. Only executed or authoritatively observed work can support a release decision.
