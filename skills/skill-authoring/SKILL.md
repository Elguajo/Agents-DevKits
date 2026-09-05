---
name: skill-authoring
description: Add, change, retire, or reject a skill in this repository's skill library without breaking bounded ownership, routing, or the reproducible gate. Use when a prompt, workflow, or external idea is proposed as a new skill or reference.
---

# Skill Authoring

Own **the procedure for changing the skill library itself**. This is a maintenance capability of `Agents-DevKits`, not a workflow for product repositories.

## Use when
- A prompt, workflow, external repository, or recurring instruction is proposed as a new skill.
- An existing skill must change ownership, triggers, status, references, or handoffs.
- A skill should be deprecated or removed.

## Do not use when
- The task is product or application work in a consuming repository.
- The change is a documentation-only edit that does not touch ownership, routing, or the registry.
- The question is whether the current library already has overlap or dead routing; that is `scripts/validate_registry.py` plus `scripts/evaluate_scenarios.py`, run through `scripts/gate.py`.

## Decision first: skill, reference, or nothing

Follow [`docs/workflow-maintenance.md`](../../docs/workflow-maintenance.md), then answer in order:

1. Is the responsibility universal, or domain- and vendor-specific?
2. Does an existing skill in [`SKILLS.md`](../../SKILLS.md) already own this concern?
3. If an owner exists, is this a scenario protocol rather than a concern? Then it is a `references/` file inside that owner, not a skill.
4. Can it be expressed as declarative registry metadata, a capability, or an eval instead of prose?
5. What is the smallest change that removes the recurring failure?

Create a first-class skill only when the responsibility is genuinely distinct and no existing owner can absorb it without becoming unbounded. Reject rather than expand a skill until it overlaps everything else.

## Workflow

Every accepted change touches this exact set. A partial change fails the gate.

1. `skills/<name>/SKILL.md` — frontmatter `name` must equal the directory name and the registry name. Include `Use when`, `Do not use when`, `Workflow`, `Rules`, `Handoffs`, and an output contract.
2. `skills/<name>/SOURCE.md` — required for vendored origin; write one for local adaptations too, recording inspiration, retrieval date, and local changes.
3. `skills/registry.yaml` — add the full entry: `name`, `path`, `category`, `status`, `inputs`, `outputs`, `verification.produces` (kinds from [`contracts/evidence.yaml`](../../contracts/evidence.yaml)), `capabilities` (names from [`capabilities/registry.yaml`](../../capabilities/registry.yaml)), `references`, `origin`, `owns`, `use_when`, `produces`, `non_goals`, `handoff_to`, `related`, `invocation`, `triggers`.
4. `skills/registry.yaml` → `trigger_values` — declare any new fact before using it.
5. `skills/registry.yaml` → `routing.overrides` — an `experimental` skill is routed `propose` or `ask`, never silent `auto`.
6. Cross-links — update `handoff_to` and `related` on the neighbouring skills that now hand work to or from this one.
7. [`SKILLS.md`](../../SKILLS.md) — quick-registry row plus a catalog entry with path, origin, status, use-when, produces, non-goals, and handoff.
8. [`docs/skill-boundaries.md`](../../docs/skill-boundaries.md) — responsibility-map row, a collision rule against every skill it could be confused with, and a `Progressive references` bullet when it owns references.
9. [`evals/scenarios.yaml`](../../evals/scenarios.yaml) — at least one scenario listing the skill under `selected`, and a scenario listing it under `skipped` where over-triggering is plausible.
10. Regenerate the routing index: `python3 scripts/generate_routing_index.py`.
11. Run `python3 scripts/gate.py` and report its real output.

## Rules
- One skill owns one primary concern. If a candidate needs two `owns` sentences, it is two skills or none.
- `use_when` must be falsifiable. A description that matches most tasks is a routing collision, not a capable skill.
- `non_goals` must name the neighbouring owners the skill will be confused with. An empty or generic `non_goals` is rejected.
- Repository-maintenance and vendor-specific skills use `invocation: [user]` so they cannot be selected inside a consuming project.
- A new skill starts `experimental`. Promotion to `active` requires real use, not review confidence.
- Do not copy upstream prompt text without a `SOURCE.md` and a license check.
- Do not report the gate as passing unless it was executed and printed `PASS`.

## Handoffs

- The candidate is really a project-specific fact pack → `project-knowledge`.
- The candidate is really documentation or a policy decision → `docs/workflow-maintenance.md`, not a skill.
- The change alters public repository behavior for consumers → `change-impact-analysis`.

## Output contract
Return the decision (`new skill`, `reference inside <owner>`, `registry-only change`, `reject`), the reasoning against existing owners, the exact files changed, the routing tier and status chosen, the collision rules added, and the observed `scripts/gate.py` result.
