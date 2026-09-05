---
name: apple-quality-interface-refinement
description: Audit and materially refine an existing web or app interface whose product direction already exists but whose visual hierarchy, interaction quality, states, motion, responsiveness, or overall craft feel unfinished; use Apple Human Interface Guidelines as a quality benchmark without cloning Apple UI, starting from rendered evidence and the existing product language.
---

# Apple-Quality Interface Refinement

## Primary responsibility

Own the **refinement pass for an existing interface**.

The interface already exists. The goal is to preserve its product identity and
working behavior while raising its clarity, coherence, responsiveness, state
quality, interaction feedback, and visual craft to a much higher standard.

"Apple-quality" is a **quality bar**, not a visual preset.

Do not automatically make the interface look like iOS, macOS, Apple.com,
Liquid Glass, or any Apple product.

---

## Boundary inside Agents-DevKits

This skill owns:

- reconstructing the current interface language;
- identifying visible quality gaps in an existing UI;
- deciding what to preserve, refine, replace, remove, or add;
- synthesizing a coherent refinement direction;
- implementing an in-scope refinement pass when the user asked for changes;
- driving a render, critique, and fix loop until the targeted quality gaps are resolved.

It does **not** replace:

- `frontend-design` — new art direction or a substantially new visual concept;
- `redesign` — broad rework that is allowed to change the existing direction rather than preserve it;
- `design-system` — system-wide token/component architecture;
- `design-review` — independent expert critique of UI quality, including artifacts that cannot be exercised;
- `responsive-design` — dedicated cross-viewport architecture;
- `motion-design` — nontrivial motion systems or signature motion;
- `ux-usability-audit` — deep user-flow, information-architecture, or heuristic usability diagnosis;
- `accessibility-review` — specialist accessibility audit and remediation;
- `visual-qa` — final evidence-driven visual regression and fidelity verification;
- `playwright-testing` — browser end-to-end behavior;
- `performance-review` — measured runtime and performance investigation.

The distinction against `redesign` is preservation. This skill keeps the
existing visual direction and raises execution quality inside it. When the
direction itself is the problem, hand off instead of quietly redesigning.

If one of those concerns becomes primary, hand off instead of expanding this
skill until it owns everything.

---

## Operating modes

Infer the mode from the user's request.

### Audit only

Use when the user asks to inspect, critique, assess, or suggest improvements.

Do not modify code.

### Audit and refine

Default when the user explicitly asks to improve, update, polish, modernize,
refine, or make the existing interface substantially better.

Audit first, then implement the high-confidence in-scope refinement.

### Reference-led refinement

Use when the user supplies screenshots, Figma, websites, products, moodboards,
or other references.

Treat supplied references as stronger intent than generic Apple guidance.

Extract transferable principles; do not clone unrelated composition or branding.

---

## Non-negotiable sequence

**Observe, understand, baseline, audit, references, plan, implement, render,
critique, fix, verify.**

Do not jump directly from "make it Apple-like" to CSS changes.

---

## Phase 0 — Establish evidence

Before making design claims, determine what evidence is actually available.

Possible evidence:

- rendered live interface;
- screenshots;
- browser automation;
- repository code;
- Figma or reference images;
- existing design tokens;
- product and design documentation.

Label important findings as:

- **Observed, rendered**: directly visible in the UI;
- **Observed, code**: directly confirmed in implementation;
- **Inferred**: plausible but not directly verified;
- **Not assessable**: unavailable with current evidence.

Rules:

- Never state hover, focus, animation, keyboard behavior, latency, or screen-reader
  behavior as fact from a static screenshot.
- Never invent unreadable text or hidden states.
- If a claim cannot be verified, say what would need to be checked.
- Prefer fewer strong findings over a padded audit.

Read `references/evidence-and-baseline.md`.

---

## Phase 1 — Understand the product before the style

Identify:

- what the product is;
- who uses it;
- the primary jobs people are trying to accomplish;
- primary screens and flows;
- frequency of use;
- target device and input contexts;
- current brand personality;
- any supplied visual references;
- technical constraints.

Then answer:

**What should this product feel like when it is working at its best?**

Examples are emotional and functional qualities, not styles:

- calm and precise;
- fast and professional;
- expressive and creative;
- trustworthy and restrained;
- dense but effortless;
- premium but not ornamental.

Do not assume every product should feel minimal.

---

## Phase 2 — Reconstruct the current visual language

Before changing it, infer the system that already exists.

Create a concise **Current Interface Model**:

- visual character;
- information density;
- geometry;
- spacing rhythm;
- type hierarchy;
- color hierarchy;
- surfaces and materials;
- borders and depth;
- icon language;
- interaction state language;
- motion language;
- content and microcopy tone;
- responsive behavior;
- strengths worth preserving;
- inconsistencies;
- unfinished areas.

For each important existing pattern classify:

- **Preserve** — already strong and aligned;
- **Refine** — correct concept, weak execution;
- **Replace** — actively harms clarity or coherence;
- **Remove** — unnecessary UI or decorative complexity;
- **Missing** — needed state, feedback, hierarchy, or behavior.

Do not "improve" a component merely because another product uses a different pattern.

Read `references/current-interface-model.md`.

---

## Phase 3 — Capture a baseline

When rendering or browser tooling is available, capture the current interface before editing.

Prioritize:

- primary page or screen;
- one important workflow;
- key open and closed states;
- empty, loading, and error states when relevant;
- mobile and desktop when relevant.

Keep the baseline small and representative.

If screenshots are already supplied, use them as baseline evidence.

The baseline exists so that later claims like "better hierarchy" can be checked
against the same state instead of relying on memory.

---

## Phase 4 — Audit in passes

Run the audit as several deliberate passes.

### Pass A — Goal walk

Walk the interface as the intended user pursuing the primary task.

Look for:

- uncertainty;
- competing actions;
- hidden next steps;
- lost context;
- unnecessary decisions;
- weak feedback;
- awkward state transitions.

If deep flow or information-architecture problems dominate, hand off to
`ux-usability-audit`.

### Pass B — Hierarchy and composition

Evaluate focal point, primary versus secondary actions, grouping through
spacing, content priority, density, container overuse, empty space, alignment,
optical balance, and responsive composition.

### Pass C — Typography and content

Evaluate type hierarchy, reading measure, weights and contrast, label clarity,
action wording, errors and empty states, truncation and wrapping, and whether
interface text speaks in user concepts rather than implementation jargon.

### Pass D — Components and states

For relevant interactive components inspect default, hover, focus-visible,
pressed, selected, disabled, loading, success, empty, and error states.

A polished interface is often distinguished by coherent state behavior, not by
more decoration.

### Pass E — Surface and craft

Evaluate radii, borders, shadows, depth, materials, icon proportions, baseline
alignment, visual noise, contrast, repeated magic values, and inconsistent
component proportions.

### Pass F — Motion and continuity

Evaluate only what can actually be observed.

Ask whether motion explains origin, destination, or state; whether transitions
are abrupt where continuity would help; whether animation delays repetitive
work; whether motion is consistent; whether reduced motion is respected; and
whether there is obvious jank.

For a substantial motion system, hand off to `motion-design`.

### Pass G — Adaptability

Evaluate whether hierarchy and interaction remain good across relevant viewport
sizes and input modes.

If responsive behavior itself requires redesign, hand off to `responsive-design`.

---

## Phase 5 — Apple-quality benchmark

Use Apple's Human Interface Guidelines primarily as a decision framework.

Evaluate the interface against:

- **Purpose** — the experience is clearly oriented around what matters;
- **Agency** — people remain informed, in control, and able to recover;
- **Responsibility** — clarity, safety, privacy, accessibility, and performance are not traded for novelty;
- **Familiarity** — established concepts and patterns are used consistently;
- **Flexibility** — the experience adapts to different contexts and needs;
- **Simplicity** — unnecessary complexity is removed without hiding necessary capability;
- **Craft** — details feel intentional and durable;
- **Delight** — character and feedback enrich the task instead of distracting from it.

For actual Apple-platform applications, platform HIG may carry stronger weight.

For web products, preserve web conventions and product identity. Do not import
Apple-specific controls, token values, materials, or platform behavior merely
to achieve visual resemblance.

Read `references/apple-quality-benchmark.md`.

---

## Phase 6 — Research references deliberately

Use this precedence:

1. explicit user-provided reference or approved Figma;
2. current product identity and existing design system;
3. production products solving the same user problem;
4. strong examples of the same interaction pattern;
5. Apple interfaces and HIG where relevant;
6. general design inspiration.

For each useful reference extract the problem being solved, the information
hierarchy, the interaction model, the density and spacing logic, the component
and state behavior, the motion and continuity behavior, what transfers to this
product, and what does not.

Do not collect a moodboard of attractive screenshots with no design reasoning.

Use a small number of relevant references rather than many weak ones.

Read `references/reference-research.md`.

---

## Phase 7 — Define the refinement direction before code

Produce a concise **Refinement Plan**.

For each meaningful change record: Problem, Evidence, Why it matters, Preserve,
Proposed change, Principle or reference, Priority, and Confidence.

Priority:

- **P0** — broken or seriously harmful;
- **P1** — major clarity, hierarchy, or interaction improvement;
- **P2** — meaningful craft or consistency improvement;
- **P3** — optional polish or delight.

Confidence: High, Medium, or Low.

Then define:

### Design intent

One short paragraph describing the refined interface.

### System delta

What changes in typography, spacing, geometry, color, surfaces, components,
states, and motion.

Prefer a small coherent system change over dozens of unrelated local tweaks.

### Signature

Optionally identify **one** defining visual or interaction moment that makes the
product feel intentional and memorable.

Do not force a signature element when the product should remain quiet and utilitarian.

### Scope guard

Explicitly list what will **not** be redesigned in this pass.

---

## Phase 8 — Implementation

Only implement if the user's request authorizes changes.

Order work by leverage:

1. structure and hierarchy;
2. shared typography, spacing, and tokens;
3. component proportions and states;
4. surfaces and depth;
5. content and microcopy;
6. motion;
7. micro-polish.

Rules:

- preserve working behavior unless a change is explicitly justified;
- reuse repository-native components;
- use existing tokens first;
- if a token needs changing system-wide, coordinate with `design-system`;
- do not scatter one-off values when a shared primitive is appropriate;
- do not add blur, glass, gradient, shadow, or rounding by default;
- do not replace system or brand fonts merely to look more "designed";
- do not hide important actions to create empty space;
- do not add animation to every element;
- keep inputs and controls predictable;
- keep important interaction feedback immediate;
- avoid expensive effects when equivalent visual quality can be achieved more cheaply;
- preserve keyboard and focus behavior;
- respect reduced-motion settings;
- do not change unrelated product scope.

Read `references/implementation-rules.md`.

---

## Phase 9 — Render, critique, and fix loop

This is mandatory when rendered UI access exists.

### Pass 1 — Render

Capture the same baseline screens and states after implementation.

### Pass 2 — Compare

Critique before versus after:

- Is hierarchy actually clearer?
- Did visual noise decrease?
- Did the product retain its identity?
- Are spacing and type more coherent?
- Are interactive states complete?
- Did any important content become harder to find?
- Did the refinement introduce generic machine-generated premium styling?
- Did responsive behavior regress?
- Did motion improve comprehension rather than merely increase activity?

### Pass 3 — Fix

Correct the most important discrepancies.

Repeat only while there are clear material issues. Do not endlessly polish
low-impact details.

A second or third visual pass is often justified; unlimited iteration is not.

For formal final visual evidence, hand off to `visual-qa`.

Read `references/critique-loop.md`.

---

## Anti-patterns

Do not:

- clone Apple.com or macOS and iOS screens;
- apply Liquid Glass simply because Apple uses it;
- replace product identity with Apple identity;
- add large radii, blur, gradients, shadows, or translucent cards everywhere;
- make every layout sparse;
- automatically treat system fonts or common fonts as low quality;
- redesign the information architecture during a visual polish pass without evidence;
- infer interaction behavior from static screenshots;
- claim accessibility or performance passed without testing;
- add decorative animation that slows frequent actions;
- create a different local styling language on every screen;
- use references as permission to plagiarize composition or branding;
- keep tweaking after the material problems are already fixed.

---

## Completion criteria

The skill is complete only when the requested mode is satisfied.

For an implementation pass, verify that:

- the original product identity is still recognizable;
- primary task hierarchy is clearer;
- targeted P0 and P1 issues are resolved or explicitly deferred;
- shared visual rules are more coherent;
- relevant component states are intentional;
- key responsive states still work;
- motion is purposeful and optional where appropriate;
- no known functional regression was introduced;
- the rendered after-state was reviewed when rendering was available;
- unverified claims are explicitly marked as such.

---

## Output contract

Keep the final report concise.

### Style understood
What the original interface language was.

### Preserved
What was intentionally kept.

### Problems found
Only material, evidence-based findings.

### Direction
The refinement logic and important references.

### Implemented
What actually changed.

### Verification
What was rendered or tested and what was not.

### Remaining
Only high-value remaining opportunities.
