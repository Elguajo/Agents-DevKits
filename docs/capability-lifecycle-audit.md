# Capability lifecycle audit

Status: scoped architecture audit, 2026-09-28. The [external `claude-skills` repository](https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94) and the supplied capability lifecycle specification are research inputs. They do not replace this repository's architecture contract. No upstream code is copied.

## Decision

Keep Agents DevKits a portable skill and project-workflow library. Improve its existing registry, routing evaluations, and evidence checks when an observed failure warrants a change. Do not add a general context compiler, agent execution controller, persistent session store, or self-editing loop to the core without a concrete use case and a boundary decision. A separately requested agent runtime could consume this library later.

This is a revision of the initial implementation direction. The first foundation attempt added optional `version`, `risk`, `side_effects`, dependency, conflict, priority, script, and runtime metadata, plus a normalized contract export and resolver. No production registry entry used any of those fields. They were removed before landing. A metadata-only routing path was also removed: it reduced a local 30-run median validation from about 21 ms to 14 ms on this machine, while skipping frontmatter and body-handoff checks; it did not reduce model context. The existing native Codex/Claude selection path remains the context-loading boundary.

## Current architecture and strengths

| Concern | Existing owner | Observed behavior |
| --- | --- | --- |
| Skill storage and execution | `skills/<name>/SKILL.md` | 62 bounded skills; bodies and conditional references are read when their workflow is used. |
| Discovery and routing | `skills/registry.yaml` v2, generated `docs/ROUTING.md`, `scripts/platform.py`, `project.py route` | Registry metadata declares triggers (including negative `none` conditions), invocation tier, inputs/outputs, portable capabilities, references, evidence kinds, and handoffs. The diagnostic router evaluates facts; Codex/Claude retain final native selection. |
| Capability vocabulary | `capabilities/registry.yaml` | Portable names and required/preferred/optional fallback semantics; provider configuration stays outside core. |
| Verification | `agents-devkits.yaml`, `project.py verify`, `contracts/evidence.yaml`, `release-check` | Project-owned commands run on explicit request, produce ephemeral evidence, and distinguish passed, failed, unavailable, not-applicable, and inferred results. `release-check` owns the final readiness decision. |
| Orchestration and handoff | `feature-development` and its conditional references | Adaptive human-facing coordination and concise task briefs exist. There is no persistent machine task controller. |
| Adapters | `adapters/codex`, `adapters/claude`, installation scripts | Thin instructions and links; only Codex and Claude are supported targets. |
| Integrity and CI | `scripts/validate_registry.py`, `scripts/evaluate_scenarios.py`, `scripts/gate.py`, `.github/workflows/devkit.yml` | One reproducible gate checks registry/body integrity, routing scenarios, adapters, syntax, installation, secrets, and live-eval contracts. |

The repository's [architecture direction](ai-development-workflow-system.md) explicitly keeps native skill discovery and says the portable project layer is not a runtime engine. The PCK integration remains separate and is outside this work.

## Gap assessment against the supplied specification

| Proposed mechanism | State | Decision now |
| --- | --- | --- |
| Canonical skill/capability contract | Mostly present in registry v2, capability registry, and evidence contract. | Extend only for a real consumer or invalid state the existing validator cannot catch. Avoid fields that would remain unset across all skills. |
| Metadata-first selection and lazy references | Present as registry selection plus native skill activation; reference loading is conditional. CLI full validation reads bodies to check integrity, but does not put them in model context. | Keep full validation. Test actual routing behavior, not file-read count as a context proxy. |
| Routing evaluation | 46 declarative scenarios plus task-description assertions exist. Before this change, expected `selected` entries were only checked as a subset. | This change requires exact selected sets, so an unlisted false activation fails the gate. Two word-boundary false activations found using actual project commit titles are covered in `tests/project-runtime-routing.py`. |
| Conflict resolver and context compiler | Prose ownership/collision rules exist; no general machine resolver or compiler. | Defer. Semantic tool, output, and authorization conflicts cannot be made reliable by unused registry fields alone. |
| Verifier, harness, and human gate | Explicit command verification and evidence rules exist; no persistent controller or structured review store. | A template manifest with no checks returns exit 0 and `{"evidence": [], "required_reviews": []}`. This is a successful CLI invocation, not passed verification; consumers must inspect evidence. No unsupported completion claim was observed. A stateful controller needs a separately justified ownership and recovery model. |
| Handoff and self-improvement | Conditional handoff and post-run-learning procedures exist; live skill evals exist. No session mining or automatic skill edits. | Keep human-reviewed proposals. Do not introduce transcript storage, hooks, or automatic adoption based solely on upstream design. |
| More platform adapters | Codex and Claude are installed targets. | Add a target only with a real consumer and unsupported-feature policy. |

## Upstream fit

At upstream revision `19392f7`, `CONVENTIONS.md`, `SKILL_PIPELINE.md`, `orchestration/ORCHESTRATION.md`, and the nested agent-harness, human-gate, skill-doctor, and handoff skills show useful practices: bounded work, explicit evidence, review blockers, and redaction. Upstream's Claude hooks, persistent session machinery, platform conversion set, and numerical skill thresholds are implementation choices for that project. They should not become Agents DevKits requirements without local evidence. In particular, optional auto-adoption in upstream `skillopt-sleep` is incompatible with this repository's deliberate skill-maintenance workflow.

## Implementation and test map

1. **Current change:** keep this audit, the exact selected-set check in `scripts/evaluate_scenarios.py`, and two narrow fact-matching corrections in `project.py`. Add negative task-description assertions in `tests/project-runtime-routing.py` while preserving positive OAuth and INP routing. Existing `scripts/gate.py` already runs both checks, so no second CI path is needed. `scripts/platform.py`, registry v2, adapters, manifests, and PCK stay unchanged.
2. **Future routing change, only after a reproduced failure:** capture the actual task wording and expected owner in `evals/scenarios.yaml` or `tests/project-runtime-routing.py`; identify whether `project.py task_facts`, a registry trigger, or a skill boundary caused it; change that existing owner and run the gate. A skill edit follows `skills/skill-authoring/SKILL.md` and its required catalog/boundary updates.
3. **Future evidence change, only after a reproduced failure:** record the check, command result, and incorrect completion claim; repair `project.py verify`, `contracts/evidence.yaml`, or `release-check` at the narrowest responsible layer; add an integration test in `tests/project-runtime.sh`. An empty evidence list is explicit in the JSON response and does not prove the underlying task passed.
4. **Larger controller decision:** require a consuming workflow that cannot use native agent execution plus the existing project verification, with acceptance criteria for state ownership, restart, approval, and compatibility. Only then compare an opt-in runner against an external runtime. Keep it outside the default skill library unless that comparison proves a core need.

## Baseline and migration

The existing gate passed before the scoped change. The 46 routing scenarios have exact expected selected sets; the largest currently selects seven skills for a multi-concern OAuth feature, so a fixed low selection cap would reject valid work. Of 20 recent commit titles used as imperfect proxies for actual task wording, two produced clear false activations before the fix: `skill-authoring` matched auth and `input` matched the INP performance metric. The corrected route selects neither specialist for those titles while still selecting security for OAuth and performance for an explicit INP task. Commit titles are not full user requests, so this does not measure model behavior. The scoped change does not alter the registry schema, CLI output shape, project manifest, adapter format, or installed skill paths. No migration is required. Preserve the full validator and existing public interfaces.
