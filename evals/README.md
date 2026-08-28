# Routing activation evals

`scenarios.yaml` is a deterministic contract for registry routing. Each
scenario has positive expectations (`selected`) and explicit negative
expectations (`skipped`), so changes cannot silently under-trigger or
over-trigger a skill for known task facts.

Run it locally with:

```bash
python3 scripts/evaluate_scenarios.py
```

This is not a model benchmark and does not prove that Codex or Claude invokes a
skill in a live session. A future live evaluation may be run only deliberately:
record the runtime/model, prompts, expected activation, retained artifact, and
review rubric outside the required local gate. Never report such a run as a
controlled uplift unless it includes a documented comparison baseline.
