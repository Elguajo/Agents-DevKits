Use the attached `ADK_PSTACK_RECONSTRUCTION_HANDOFF.md` as the implementation specification for `Elguajo/Agents-DevKits`.

Repository snapshot used when the handoff was written:
- Agents DevKits: `075c8e94fe6198740a494693a4003930bb7c32ec`
- pstack reference: `cursor/plugins`, pstack-path revision `5bf2b1544db739998121a306340631963c2ff3de`

Before editing:

1. Verify the current working directory, branch, HEAD, and worktree status.
2. Read `AGENTS.md`.
3. Load and follow `skills/skill-authoring/SKILL.md` because this task changes reusable skills/workflows.
4. Read:
   - `docs/workflow-maintenance.md`
   - `docs/skill-boundaries.md`
   - `docs/project-runtime.md`
   - `contracts/evidence.yaml`
   - `skills/registry.yaml`
   - the existing owners named by the handoff.
5. Run the current focused repository gate/baseline before making changes.
6. Compare the live repository with the handoff snapshot and produce a compact `EXISTING / PARTIAL / MISSING / REJECTED` gap map. If the repository evolved since the snapshot, reconcile with the current canonical owners instead of overwriting newer architecture.

Then implement the handoff in the dependency-safe milestone order it defines.

Critical constraints:

- Do not import `poteto-mode` or create a second general router.
- Do not create dozens of `principle-*` skills.
- Do not create a new `blast-radius` skill; improve `change-impact-analysis`.
- Keep pre-implementation challenge under `adversarial-decision-review`.
- Keep post-implementation adversarial multi-model review under `code-review`.
- Create only one verification-harness lifecycle owner, not separate create/maintain skills.
- Keep `project.py` deterministic; do not turn it into an LLM/browser scheduler.
- Keep execution evidence honest and ephemeral.
- Do not add permanent execution-history infrastructure.
- Do not add autonomous PR merge/shipping in this pass.
- Do not hard-code Cursor transcript paths, Cursor `/loop`, provider credentials, or model slugs into the portable core.
- Do not edit the Progressive-Context-Kit repository.
- Preserve current Agents DevKits ↔ PCK integration behavior and tests.
- Do not weaken a test, validator, routing rule, evidence rule, or quality threshold to obtain a pass.
- Preserve upstream MIT provenance for any materially adapted pstack content.

For every skill-library change, complete the full current `skill-authoring` procedure: registry, trigger values if needed, boundaries, catalog, handoffs, positive and negative routing scenarios, routing-index regeneration, and gate verification.

Use focused verification after each coherent milestone. Final required checks include:

```bash
python3 scripts/generate_routing_index.py --check
python3 scripts/gate.py
```

Do not claim success unless those commands were actually run and their results are reported.

Final response must contain:
- baseline branch/commit and baseline gate result;
- implemented milestones;
- exact files added/changed;
- architecture/routing decisions;
- pstack concepts reconstructed;
- concepts deliberately rejected/deferred and why;
- exact focused/final verification commands and outputs;
- provenance revision used;
- residual risks and live-eval work still requiring real model runs.
