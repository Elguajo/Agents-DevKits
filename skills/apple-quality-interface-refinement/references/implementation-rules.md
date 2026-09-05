# Implementation Rules

Refinement is a preservation-first change. Every edit either resolves a named
finding from the plan or does not belong in this pass.

## Order of work

Work top-down by leverage; a fix at a lower level rarely rescues a problem above it.

1. structure and hierarchy;
2. shared typography, spacing, and tokens;
3. component proportions and states;
4. surfaces and depth;
5. content and microcopy;
6. motion;
7. micro-polish.

## Repository-native first
- Reuse existing components before writing new ones.
- Use existing tokens before introducing values.
- If a token itself must change across the system, that is a `design-system`
  decision; coordinate rather than forking a local copy.
- Do not scatter one-off values where a shared primitive already exists.

## Restraint defaults
- Do not add blur, glass, gradient, shadow, or larger radii by default.
- Do not swap system or brand fonts to look more designed.
- Do not create empty space by hiding actions people need.
- Do not animate every element; motion is added where it explains something.
- Do not introduce an expensive effect when a cheaper one reads the same.

## Behavior is load-bearing
- Preserve working behavior unless a change is explicitly justified in the plan.
- Preserve keyboard order, focus-visible treatment, and focus management.
- Keep interaction feedback immediate; never place an animation in front of a
  frequent action.
- Respect reduced-motion preferences with a real fallback, not a shortened animation.
- Do not change product scope, copy meaning, or data behavior during a visual pass.

## Stop conditions
Stop and hand off when the work turns into new art direction (`frontend-design`),
direction-changing rework (`redesign`), system-wide token architecture
(`design-system`), a responsive architecture problem (`responsive-design`), or a
real motion system (`motion-design`).
