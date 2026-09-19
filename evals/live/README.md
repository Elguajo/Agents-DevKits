# Deliberate live behavioral evaluations

This directory supports controlled, opt-in with-skill comparisons. It is not a
model benchmark and `scripts/gate.py` never invokes a live model.

Use `prepare_skill_eval.py` with one pilot from `../skill-quality-pilots.yaml`
to create separate baseline and candidate packets. Candidate-visible
`TASK.md` contains only the organic task; it must not disclose evaluation,
judging, scoring, baseline/candidate identity, or a rubric. Keep rubrics and
records outside candidate-visible workspace context.

Capture actual artifacts, commands, and authorized tool output in run records;
do not score self-report alone. Keep model/runtime, repository snapshot, task,
acceptance criteria, tools, permissions, and environment fixed where practical.
Record digests for both task wording and pilot acceptance criteria so the
analyzer can reject an uncontrolled comparison.
Metrics not provided by a runtime are `unavailable`, not estimated.

Validate records with `validate_skill_eval.py`, then compare assertion outcomes
with `analyze_skill_eval.py`. A baseline passed → candidate failed regression in
correctness, safety, security/authorization, or evidence truthfulness is hard
and cannot be offset by efficiency. Both variants must use the identical
assertion IDs and classes; a missing or reclassified assertion invalidates the
comparison rather than hiding a regression. Store retained records deliberately outside
the portable core; no permanent execution-history system is created here.
