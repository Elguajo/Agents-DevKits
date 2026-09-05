# Current Interface Model

Reconstruct the system that already exists before proposing changes to it. The
model is a working description, not a document to hand to the user in full.

## Dimensions to describe

- **Visual character** — what the interface is trying to be, in one line.
- **Density** — how much information a screen carries and whether that suits the task frequency.
- **Geometry** — radii, corner treatment, edge alignment, grid or lack of one.
- **Spacing rhythm** — the increments actually in use, and where they break down.
- **Type hierarchy** — how many distinct sizes and weights exist, and which levels are actually distinguishable.
- **Color hierarchy** — how emphasis, state, and meaning are encoded.
- **Surfaces and materials** — layering, elevation, borders versus fills.
- **Icon language** — set, weight, size relationship to text.
- **Interaction state language** — how the interface signals hover, focus, pressed, selected, disabled, busy.
- **Motion language** — what moves, why, and how consistently.
- **Content tone** — labels, actions, errors, and empty states.
- **Responsive behavior** — what adapts, what merely stacks, what breaks.

## Classification

Every important existing pattern gets exactly one verdict:

| Verdict | Meaning | Bar for using it |
| --- | --- | --- |
| Preserve | Strong and aligned with product intent | The default verdict |
| Refine | Right concept, weak execution | Name the specific execution defect |
| Replace | Actively harms clarity or coherence | Name the harm, not the preference |
| Remove | Adds no information or function | Show that nothing depends on it |
| Missing | A needed state, feedback, or hierarchy level does not exist | Show where the gap is felt |

## Rules
- The burden of proof is on changing something, not on keeping it.
- Difference from another product is not a defect.
- A pattern used consistently across the product is stronger evidence of intent
  than a pattern used once; a single inconsistent instance is usually the bug.
- Record what is intentionally load-bearing for brand identity so a later pass
  does not sand it off.
