# Routing activation evals

`scenarios.yaml` is a deterministic contract for registry routing. Each
scenario has positive expectations (`selected`) and explicit negative
expectations (`skipped`), so changes cannot silently under-trigger or
over-trigger a skill for known task facts.

Every `model`-invocable skill must appear in at least one scenario, as either
`selected` or `skipped`. A skill nothing exercises is unroutable in practice, so
the eval fails rather than letting it accumulate silently. `user`-invocation
skills are exempt because they are never selected by facts alone.

Run it locally with:

```bash
python3 scripts/evaluate_scenarios.py
```

This is not a model benchmark and does not prove that Codex or Claude invokes a
skill in a live session. A future live evaluation may be run only deliberately:
record the runtime/model, prompts, expected activation, retained artifact, and
review rubric outside the required local gate. Never report such a run as a
controlled uplift unless it includes a documented comparison baseline.

## Skill-quality pilots

[`skill-quality-pilots.yaml`](skill-quality-pilots.yaml) defines the first five
deliberate with-skill versus without-skill pilots. The gate validates only that
these experiments remain runnable and reference installed skills; it does not
claim a model-quality result.

For a live run, keep the task and repository fixture identical for both arms,
record the model/runtime and duration, retain artifacts and transcripts, and
grade each listed assertion independently. Compare quality, false activation,
token use, and elapsed time before promoting a workflow based on the result.
