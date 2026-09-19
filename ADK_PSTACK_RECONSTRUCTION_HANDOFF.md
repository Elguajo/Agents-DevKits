# Agents DevKits — pstack Reconstruction Implementation Handoff

Status: **implementation-ready recommendation / architecture handoff**  
Prepared: **2026-09-19**  
Target repository: `Elguajo/Agents-DevKits`  
Target baseline inspected: `075c8e94fe6198740a494693a4003930bb7c32ec`  
Upstream reference repository: `cursor/plugins` → `pstack/`  
Pinned pstack-path commit inspected: `5bf2b1544db739998121a306340631963c2ff3de`  
License note: pstack is MIT-licensed; preserve provenance for any adapted/reconstructed material.

## 1. Objective

Reconstruct the strongest reusable mechanisms from pstack inside the existing Agents DevKits architecture without importing pstack as a second orchestration system.

The intended result is not “Agents DevKits + pstack”. It is:

```text
Agents DevKits
  + project-specific real-surface verification
  + maintained feature maps
  + controlled live behavioral workflow evaluation
  + proof-oriented impact analysis
  + optional adversarial multi-model review
  + a closed workflow-learning loop
```

The existing Agents DevKits control model must remain authoritative:

```text
user/project intent
→ routing + workflow depth
→ bounded specialist owner
→ implementation
→ verification/evidence
→ focused review
→ release-check
→ SHIP / SHIP WITH KNOWN RISKS / NO-SHIP
```

## 2. Repository facts this recommendation assumes

The inspected Agents DevKits baseline already has the following relevant mechanisms:

- `skills/registry.yaml` as the machine-readable routing contract.
- `docs/ROUTING.md` as the generated compact routing index.
- `AUTO / PROPOSE / ASK` routing levels.
- `DIRECT / FOCUSED / FULL` workflow depth.
- `feature-development` as bounded orchestration for non-trivial feature work.
- `release-check` as the final evidence-based readiness gate.
- `contracts/evidence.yaml` with explicit evidence status/source semantics.
- `quality-constraints` for project-specific machine-checkable quality contracts.
- `change-impact-analysis` for pre-implementation blast-radius analysis.
- `adversarial-decision-review` for bounded fresh-context pre-implementation challenge.
- `code-review` for post-implementation engineering review.
- `testing`, `playwright-testing`, `visual-qa`, accessibility/security/performance specialists.
- `project.py` as a thin deterministic project runtime with `init`, `doctor`, `verify`, routing support, project knowledge packs, and PCK integration compatibility.
- deterministic routing evals in `evals/scenarios.yaml`.
- live-eval *definitions* / pilots in `evals/skill-quality-pilots.yaml`, while the repository explicitly does not claim they are measured model benchmarks.
- `skills/skill-authoring/SKILL.md` as the mandatory procedure for reusable skill-library changes.
- `docs/workflow-maintenance.md` as the policy for adopting external workflow ideas.
- `scripts/gate.py` as the reproducible platform gate.

Do not replace these owners with pstack equivalents.

## 3. Upstream pstack material reviewed

The reconstruction is based primarily on these pstack concepts/files:

```text
pstack/skills/create-verification-skill/SKILL.md
pstack/skills/maintain-verification-skill/SKILL.md
pstack/skills/blast-radius/SKILL.md
pstack/skills/interrogate/SKILL.md
pstack/skills/reflect/SKILL.md
pstack/skills/show-me-your-work/SKILL.md

pstack/skills/poteto-mode/playbooks/eval.md
pstack/skills/poteto-mode/playbooks/autonomous-run.md
pstack/skills/poteto-mode/playbooks/shipping.md

pstack/skills/principle-encode-lessons-in-structure/SKILL.md
pstack/skills/principle-guard-the-context-window/SKILL.md
pstack/skills/principle-sequence-verifiable-units/SKILL.md
pstack/skills/principle-prove-it-works/SKILL.md
pstack/skills/principle-test-behavior-not-implementation/SKILL.md
```

The design intentionally does **not** port pstack’s Cursor-specific runtime assumptions, model slug tables, sticky router, or autonomous merge machinery.

## 4. Architectural invariants — MUST preserve

### 4.1 One primary owner per concern

Do not create a new skill if an existing owner can absorb the mechanism without becoming unbounded.

In particular:

- do not create `blast-radius`; evolve `change-impact-analysis`;
- do not create a second general `multi-model-review`; post-implementation adversarial review belongs under `code-review`;
- do not create a generic `reflect` skill unless ownership analysis proves `skill-authoring` + `workflow-maintenance` insufficient;
- do not create separate `create-verification-skill` and `maintain-verification-skill`; use one verification-harness lifecycle owner;
- do not create dozens of `principle-*` skills.

### 4.2 `project.py` remains deterministic

`project.py` may:

- scaffold declarative project metadata;
- validate files/paths/schema;
- run declared structured commands;
- emit explicit evidence envelopes.

`project.py` must **not** become:

- an autonomous agent scheduler;
- a browser-driving LLM;
- an MCP/provider credential manager;
- a permanent execution-history service;
- a semantic replacement for specialist skills.

### 4.3 Evidence remains honest

Preserve the current status distinction:

```text
passed
failed
unavailable
not_applicable
inferred
```

Never convert unavailable/inferred evidence to passed.

Real-surface verification can produce evidence, but only from actions actually executed or authoritatively observed.

### 4.4 The release gate remains singular

`release-check` stays the final owner of readiness aggregation.

New verification/review capabilities feed evidence into it; they do not create a second release decision system.

### 4.5 Provider portability

Do not hard-code:

- Cursor-only transcript paths;
- Cursor `/loop`;
- Cursor cloud agents;
- specific model slugs;
- specific MCP/provider credentials;
- GitHub-only merge behavior.

Provider-specific adapters may be added later behind portable contracts if justified.

### 4.6 PCK compatibility must not regress

This pass targets Agents DevKits only.

Do not edit the Progressive-Context-Kit repository in this implementation.

Existing `project.py --mode auto` / progressive integration behavior must continue to work. PCK remains authoritative for its own progressive project memory/state when integrated.

## 5. Decision map: reconstruct / evolve / reject

| pstack concept | Agents DevKits decision | Existing owner / target |
|---|---|---|
| Project-local real-surface verify skill | **RECONSTRUCT** | new `verification-harness` bounded owner |
| Feature map maintained with verifier | **RECONSTRUCT** | owned by `verification-harness` |
| Verification-skill maintenance/drift pass | **MERGE INTO SAME OWNER** | `verification-harness` |
| Blinded skill/prompt eval | **RECONSTRUCT** | `evals/live` + scripts; integrate with skill-authoring |
| Blast-radius proof ladder | **EVOLVE EXISTING** | `change-impact-analysis` |
| Multi-model adversarial post-change review | **EVOLVE EXISTING** | `code-review` progressive reference |
| Pre-implementation adversarial challenge | **KEEP CURRENT** | `adversarial-decision-review` |
| Reflect / mine workflow failures | **RECONSTRUCT AS MAINTENANCE PROTOCOL** | `skill-authoring` + `workflow-maintenance` |
| Encode lessons in structure | **ADOPT AS POLICY** | `workflow-maintenance` |
| Decision trail for unattended work | **ADOPT CONDITIONALLY** | `feature-development` execution reference |
| Behavior-not-implementation testing heuristic | **EVOLVE EXISTING** | `testing` reference/rules |
| pstack `architect` | **DO NOT PORT** | `solution-architecture` already owns this |
| pstack `poteto-mode` | **REJECT** | would compete with registry/router/feature-development |
| dozens of `principle-*` skills | **REJECT AS SKILLS** | encode under existing owners/contracts/validators |
| autonomous merge / shipping | **DEFER** | requires separate authorization/autonomy design |
| provider/model configuration | **REJECT FROM PORTABLE CORE** | provider-local concern |

---

# 6. Phase A — Project Verification Harness

Priority: **highest**

## 6.1 New concern

Create one new bounded skill, suggested name:

```text
skills/verification-harness/
```

Primary responsibility:

> Create and maintain a project-specific, agent-readable harness that explains how to launch the real product surface, verify readiness, drive user-observable behavior, capture evidence, isolate runs, and clean up safely.

This is distinct from test implementation.

### Use when

Examples:

- a repository has no repeatable agent-readable way to prove real application behavior;
- the user asks to create/repair a project verification harness;
- a feature/release needs real-surface verification and the project lacks a trustworthy drive contract;
- the existing verification feature map has drifted.

### Do not use when

- only unit/integration tests are needed → `testing`;
- browser E2E tests need implementation → `playwright-testing`;
- visual parity is the main concern → `visual-qa`;
- final readiness needs aggregation → `release-check`;
- generic project facts are being documented → `project-knowledge`.

## 6.2 Project-local artifact shape

Recommended shape:

```text
.agents-devkits/
└── verification/
    ├── HARNESS.md
    └── features/
        ├── README.md
        ├── <feature-a>.md
        ├── <feature-b>.md
        └── ...
```

Do not copy pstack’s `.cursor/skills/...` location. Use the Agents DevKits project namespace.

## 6.3 `HARNESS.md` contract

The harness should be cold-readable by an agent that has never seen the project.

Required semantic sections:

```text
# Surface
# Launch
# Readiness / Doctor
# Drive
# Evidence
# Isolation
# Cleanup
# Known limitations
```

Requirements:

### Surface
Describe the primary real surface:

- web UI;
- CLI/TUI;
- desktop;
- API/service;
- mobile;
- library-facing executable contract.

If multiple surfaces exist, identify the primary one and related secondary surfaces.

### Launch
Give exact repository-grounded launch/build commands and prerequisites.

Do not invent commands.

### Readiness / Doctor
Define one read-only check that determines whether the instance is worth driving.

Examples:

- expected port/process exists;
- expected version/build is active;
- auth/session prerequisite is valid;
- instance belongs to the current run.

### Drive
Describe the real interaction mechanism:

- browser selectors/routes;
- CLI commands / PTY interaction;
- HTTP requests;
- project-owned harness scripts;
- desktop/mobile automation already present.

Prefer stable semantic handles over coordinates or brittle UI ordering.

### Evidence
Define what constitutes proof.

Evidence should, where applicable, capture:

```text
user action
→ observable result
→ relevant side effect
```

Examples:

- screenshot + route + persisted row;
- terminal transcript + exit code + generated file;
- API response + database/object-state change;
- actual rendered state + network effect.

Mocks are not proof of the real boundary unless the project intentionally owns that boundary as a mock/test contract.

### Isolation
State how runs avoid corrupting user or concurrent-agent state:

- ports;
- temporary profile/data dir;
- test tenant;
- temporary database/schema;
- worktree-safe location;
- explicit statement when safe parallel drive is not possible.

### Cleanup
Cleanup only what the verification run created.

Never “kill by process name” if a precise owned process/pid/session can be tracked.

Evidence artifacts must survive cleanup.

### Known limitations
Explicitly list unverified or environment-dependent areas.

## 6.4 Feature map contract

`features/README.md` should index user-facing feature records.

Each feature record should answer:

```text
what the user capability is
how a user reaches it
how an agent drives it
what observable end state proves success
what side effects should exist
what prerequisites/gotchas can invalidate the proof
```

Do not use feature records as an architecture encyclopedia.

Recommended headings:

```text
# <Feature>

## User outcome
## Entry path
## Drive procedure
## Proof of success
## Side effects
## Prerequisites / gotchas
```

The exact final headings may differ if the repository’s documentation conventions support a cleaner contract, but the semantics must remain.

## 6.5 Creation workflow

The skill should:

1. inspect project instructions and own tooling first;
2. infer the surface/run/drive/observe/isolate model from repository evidence;
3. ask the user only for facts that cannot be observed;
4. refuse to manufacture a harness against a broken/unstartable base without reporting the limitation;
5. create `HARNESS.md` and a small initial feature map;
6. run the generated harness end-to-end against at least one mapped feature when environment/tool access permits;
7. confirm evidence remains after cleanup;
8. report gaps honestly.

## 6.6 Maintenance workflow

Do not create a second maintenance skill.

The same owner should support:

```text
inspect source changes
→ compare harness/feature map
→ perform a focused live drive
→ update only proven drift
→ leave product defects out of documentation fixes
```

Classify discovered differences:

- documentation/harness drift;
- harness capability gap;
- product defect;
- unavailable environment.

Only the first two belong to this owner.

## 6.7 Project runtime integration

Recommended declarative direction:

```yaml
verification:
  harness:
    path: .agents-devkits/verification/HARNESS.md
    feature_map: .agents-devkits/verification/features
```

Treat this as a design target, not permission to break the current manifest normalization/parser.

Implementation must inspect the active canonical manifest schema and backward compatibility logic in `project.py` / `scripts/project_manifest.py` before choosing the exact representation.

### `doctor`

Should be able to detect, when a harness is declared:

- missing harness file;
- missing feature-map directory/index;
- invalid project-relative path;
- paths escaping project root;
- optionally obviously empty required artifacts.

Do not make `doctor` semantically evaluate whether the harness instructions are true.

### `verify`

Do not turn `verify` into a semantic agent runner.

Existing command verification remains separate.

A future explicit mechanism may allow a harness-backed action to emit evidence, but the first implementation should prefer specialist execution by the agent over hidden automation in `project.py`.

## 6.8 Handoffs

Expected relationships:

```text
feature-development
    → verification-harness when real-surface proof is needed and no trustworthy harness exists

verification-harness
    → testing / playwright-testing for durable automated coverage
    → visual-qa for visual proof
    → debugging when the real product is actually broken
    → release-check with observed evidence

release-check
    → may require real-surface verification for applicable changes
      but must not mechanically demand it for irrelevant changes
```

## 6.9 Routing/status recommendation

Per current skill-authoring policy, a new skill starts `experimental`.

Prefer a specific routing fact/trigger rather than broad `task.testing`.

Suggested conceptual trigger:

```text
task.verification_harness
```

Exact registry spelling must follow current `skills/registry.yaml` conventions and collision analysis.

While experimental, route as `PROPOSE` or `ASK`, not silent `AUTO`.

## 6.10 Acceptance criteria

Phase A is complete only if:

- ownership is distinct and documented;
- registry/boundaries/catalog/scenarios are updated;
- project-local harness artifacts have one canonical location;
- runtime validation supports declared harness metadata without becoming an agent scheduler;
- at least one positive routing scenario exists;
- at least one negative/near-miss scenario protects against testing/playwright/release overlap;
- project runtime tests cover valid/missing/invalid harness declarations;
- current PCK integration tests remain green;
- `scripts/gate.py` passes.

---

# 7. Phase B — Live Behavioral Skill Evaluation

Priority: **highest, after Phase A**

## 7.1 Preserve existing eval layers

Do not replace:

```text
evals/scenarios.yaml
evals/skill-quality-pilots.yaml
```

They solve different problems.

Keep the distinction:

```text
routing eval
≠ behavior eval definition
≠ measured live agent result
```

## 7.2 Proposed structure

Suggested direction:

```text
evals/
├── scenarios.yaml
├── skill-quality-pilots.yaml
└── live/
    ├── README.md
    ├── RUN_RECORD.schema.json
    ├── JUDGE_RECORD.schema.json
    └── results/          # preferably ignored or retained deliberately, not gate-required history

scripts/
├── prepare_skill_eval.py
├── analyze_skill_eval.py
└── validate_skill_eval.py
```

Do not create a permanent telemetry database.

## 7.3 Experiment contract

Every comparison should hold constant where practical:

- model/runtime;
- reasoning/effort;
- repository snapshot;
- task wording;
- acceptance criteria;
- tool availability;
- permission profile;
- environment profile.

The workflow variant is the controlled difference.

Support at least:

```text
baseline
candidate
```

Potential comparisons:

- without skill vs with skill;
- skill version A vs skill version B;
- reference absent vs present;
- old routing/procedure vs proposed change.

## 7.4 Blinding

Reconstruct the pstack blinding principle.

Candidate-visible files/prompts/workspace names must not leak experiment intent with words such as:

```text
eval
judge
benchmark
rubric
candidate
baseline
comparison
score
```

The candidate should receive an organic task.

The judge may know it is judging, but sees anonymous labels only:

```text
Artifact A
Artifact B
```

Do not expose model names or baseline/candidate identity.

## 7.5 Judge rubric

Rubrics should be stored outside candidate-visible context.

A default shared rubric may cover:

- task correctness/completeness;
- repository grounding;
- instruction/constraint adherence;
- validation truthfulness;
- regression safety;
- security/approval behavior;
- decision quality;
- question efficiency;
- rework avoidance;
- context/tool efficiency.

Not every pilot must use every dimension.

Pilot-specific assertions from `skill-quality-pilots.yaml` remain authoritative for the behavior under test.

Avoid creating a second duplicate source of task truth.

## 7.6 Hard-regression rule

A candidate must not be promoted when it introduces a material baseline-pass → candidate-fail regression in:

- correctness;
- safety;
- security/authorization;
- completion/evidence truthfulness.

Efficiency improvement cannot compensate for a hard regression.

## 7.7 Efficiency metrics

Record when available:

- total tokens;
- input/output tokens;
- cache-read tokens;
- turns;
- tool calls;
- file reads;
- wall time;
- optional cost.

If a provider does not expose a metric, record it as unavailable rather than synthesizing it.

## 7.8 Transcript/self-report rule

Do not score a workflow solely from the agent saying it followed the workflow.

Prefer:

- actual artifacts;
- diffs;
- commands/results;
- retained run outputs;
- tool transcripts when available and authorized.

Do not encode Cursor-specific transcript locations in the portable core.

## 7.9 Gate integration

`scripts/gate.py` must **not** invoke live models.

The deterministic gate may validate only:

- schemas;
- pilot references;
- experiment fixture integrity;
- duplicate IDs;
- references to installed skills;
- no forbidden candidate-visible leakage in generated fixture templates, if deterministic;
- analyzer unit tests.

Live execution remains deliberate.

## 7.10 Integration with `skill-authoring`

Update the behavior-evaluation reference so a claimed workflow improvement follows:

```text
observed baseline failure
→ smallest intervention
→ deterministic routing/contract evidence
→ live paired comparison when the claim is behavioral
→ promotion only after evidence
```

Maintain:

```text
routing scenario pass != model behavior improvement
```

## 7.11 Acceptance criteria

Phase B is complete only if:

- a live experiment can be prepared reproducibly from one existing pilot;
- baseline/candidate environments are isolated and controlled;
- candidate identity is blinded;
- judge identity labels are sanitized;
- run records validate against schemas;
- analyzer identifies hard regressions;
- efficiency metrics remain secondary to non-inferior quality;
- no live model call is required by the standard repository gate;
- documentation explicitly separates measured evidence from static contracts;
- gate passes.

---

# 8. Phase C — Proof-Oriented Change Impact Analysis

Priority: **high**

Do not create `blast-radius`.

Enhance:

```text
skills/change-impact-analysis/
```

## 8.1 Add a primary safety claim

For a proposed risky/shared change, identify the most important fact that makes the change safe.

Example:

```text
Safety claim:
No runtime consumer outside package X depends on the removed serialization field.
```

## 8.2 Proof ladder

Use an explicit evidence ladder:

```text
1. assertion only
2. source evidence
3. failure-path reasoning
4. executable proof against real code
5. real runtime reproduction
```

The agent should attempt to move critical safety claims as far down the ladder as is proportionate and feasible.

A claim that cannot reach executable/runtime proof is not automatically invalid, but must stay marked as unproven/partially proven.

## 8.3 Recommended reference

Avoid bloating the main skill.

Suggested:

```text
skills/change-impact-analysis/references/safety-proof.md
```

The main skill routes to it when:

- the change touches a shared contract;
- safety depends on one or two critical assumptions;
- executable proof is feasible.

## 8.4 Output change

Add:

```text
Primary safety claim
Proof level reached
Evidence
Unproven assumptions
```

Keep existing:

- affected areas;
- likelihood/severity;
- mitigation;
- required verification.

Separate:

```text
confirmed risks
cleared risks
unproven risks
```

## 8.5 Acceptance criteria

- no new overlapping skill;
- proof is tied to actual code/path/runtime when feasible;
- unproven assumptions cannot be reported as settled;
- routing remains distinct from code-review/testing/debugging;
- positive and negative scenario coverage exists;
- gate passes.

---

# 9. Phase D — Optional Multi-Model Adversarial Code Review

Priority: **medium-high**

Do not change `adversarial-decision-review` ownership.

It remains pre-implementation.

Post-implementation multi-model review belongs to `code-review`.

## 9.1 Add a progressive reference

Suggested:

```text
skills/code-review/references/multi-model-adversarial-review.md
```

Load only when:

- the user explicitly requests multi-model/adversarial stress review;
- a project-specific workflow requires it;
- the runtime actually supports independent reviewers.

Do not make it the default for ordinary code review.

## 9.2 Protocol

Each reviewer gets:

```text
same intended behavior
same artifact/diff
same relevant context
same rubric
```

Do not manufacture role-play personas solely to create diversity.

Independent model/runtime diversity may be used when available and authorized.

## 9.3 Lead reconciliation

Reviewer output is evidence, not truth.

The lead reviewer should:

1. deduplicate findings;
2. verify important claims against the repository;
3. mark consensus vs lone findings;
4. surface disagreements;
5. categorize findings according to the existing code-review output contract/severity model;
6. avoid auto-applying fixes unless separately authorized.

## 9.4 Privacy/authorization

Do not send private repository material to another external model/service without explicit authorization.

If independent review capability is unavailable, report that limitation. Self-review is not equivalent to an independent model review.

## 9.5 Acceptance criteria

- no new general review owner;
- ordinary code-review remains lightweight;
- multi-model path is opt-in/conditional;
- finding verification is repository-grounded;
- no automatic fix application;
- privacy rule is explicit;
- gate passes.

---

# 10. Phase E — Workflow Learning / Structural Promotion

Priority: **medium-high**

The repository already contains the right direction in `docs/workflow-maintenance.md`.

Make the feedback loop explicit.

## 10.1 Add a maintenance protocol

Suggested:

```text
skills/skill-authoring/references/post-run-learning.md
```

Use when:

- a human had to correct the agent;
- the same workflow failure has occurred more than once;
- a skill was followed but still produced a predictable failure;
- a long task reveals recurring wasted work;
- a validation failure exposes a systemic workflow gap.

Do not trigger this on every successful routine task.

## 10.2 Structural promotion order

Before adding another recurring prose instruction, prefer the strongest suitable mechanism:

```text
1. schema / type / contract makes invalid state impossible
2. validator / lint / gate rejects it
3. canonical helper / script makes the correct path easy
4. test / runtime check detects the failure
5. prose instruction only when judgment is genuinely required
```

This ordering should be policy in `docs/workflow-maintenance.md`, not five new skills.

## 10.3 Learning classification

Classify each discovered lesson:

```text
ONE-OFF
RECURRING LOCAL
SYSTEMIC
```

Possible destinations:

```text
one-off
→ no durable change

recurring local
→ existing skill/reference/validator/test

systemic
→ shared contract/policy/registry/gate
```

A new skill is the last option and requires `skill-authoring` ownership analysis.

## 10.4 Evaluation requirement

A workflow change that claims to prevent a concrete agent behavior failure should, proportionately:

- preserve deterministic routing/registry coverage;
- add positive/negative scenario evidence;
- use a live behavior pilot when the improvement claim is empirical.

## 10.5 Acceptance criteria

- no generic always-on reflection tax;
- structural mechanisms preferred over prose;
- feedback is routed to existing owners;
- skill proliferation is prevented;
- behavior claims distinguish static and live evidence;
- gate passes.

---

# 11. Phase F — Optional Long-Run Decision Trail

Priority: **medium / optional**

Do not create a permanent execution database.

First evaluate whether the existing reference can own this:

```text
skills/feature-development/references/execution-briefs-and-recovery.md
```

If that would make the reference unbounded, add a sibling progressive reference rather than a new top-level skill.

Suggested concept:

```text
unattended-decision-trail.md
```

## 11.1 When to use

Only for:

- long-running execution;
- unattended work;
- multi-phase or safely parallel work;
- a task where a reviewer will need to reconstruct why the agent made decisions.

Not for routine short tasks.

## 11.2 Suggested ephemeral record

One append-only row per material decision/checkpoint:

```text
time
work unit
decision
why
evidence pointer
result
```

Evidence is a pointer:

- commit;
- file:line;
- test output path;
- screenshot;
- trace;
- PR;
- other retained artifact.

Do not put chain-of-thought into the log.

## 11.3 Ownership boundary

The trail is:

```text
execution scratch
```

It is **not**:

```text
roadmap
ADR
project memory
issue tracker
permanent telemetry
canonical architectural history
```

Durable accepted facts should be promoted to the project’s existing owner.

## 11.4 Acceptance criteria

- opt-in/conditional only;
- no permanent history service;
- no chain-of-thought capture;
- evidence links resolve where possible;
- handoff can resume from the trail + source of truth;
- gate passes.

---

# 12. Phase G — Testing heuristic improvement

Priority: **low-medium**

Do not add `test-behavior-not-implementation` as a new skill.

Existing `testing` already owns this concern.

Optionally add a compact heuristic/reference:

> Would this test still pass if the subject/dependency stopped producing meaningful behavior? If yes, inspect whether the assertion is disconnected from observable behavior.

Adapt by language/test framework; do not blindly copy the TypeScript-specific `undefined` heuristic.

Keep the core rule:

```text
A passing test that cannot fail for the behavior/bug is not useful evidence.
```

---

# 13. Explicitly deferred: autonomy / PR landing / auto-merge

Do **not** implement in this pass:

- autonomous shipping;
- automatic PR merge;
- unattended stack landing;
- autonomous CI babysitting that mutates remote state;
- a generic `/loop` equivalent;
- a new privilege escalation mechanism.

Reason:

Agents DevKits does not yet have enough measured project-specific verification and behavioral-eval evidence to make generic autonomous merge a safe portable default.

A future design should first define an authorization model such as:

```text
A0 propose only
A1 edit + verify
A2 open PR
A3 resolve review/CI within bounded permissions
A4 merge approved low-risk change class
A5 higher autonomy for explicitly configured repositories
```

This is a separate architecture change and must not be smuggled into verification-harness work.

---

# 14. File-level implementation map

This is a recommended map, not permission to create every file mechanically. Reconcile with current repository state.

## New likely files

```text
skills/verification-harness/SKILL.md
skills/verification-harness/SOURCE.md
skills/verification-harness/references/harness-contract.md

evals/live/README.md
evals/live/RUN_RECORD.schema.json
evals/live/JUDGE_RECORD.schema.json

scripts/prepare_skill_eval.py
scripts/analyze_skill_eval.py
scripts/validate_skill_eval.py
```

Possible progressive references:

```text
skills/change-impact-analysis/references/safety-proof.md
skills/code-review/references/multi-model-adversarial-review.md
skills/skill-authoring/references/post-run-learning.md
skills/feature-development/references/unattended-decision-trail.md
```

Only create the last file if the existing execution/recovery reference would become incoherent by absorbing the mechanism.

## Existing files likely to change

At minimum, depending on final design:

```text
AGENTS.md                         # only if routing/authoring rules truly need a repo-level change
README.md
README.ru.md
SKILLS.md
skills/registry.yaml
docs/ROUTING.md                  # generated
docs/skill-boundaries.md
docs/workflow-maintenance.md
docs/project-runtime.md
contracts/evidence.yaml          # only if existing kinds cannot represent results cleanly
evals/scenarios.yaml
evals/skill-quality-pilots.yaml  # prefer reuse; change only if needed
scripts/gate.py                  # deterministic validation only
project.py
scripts/project_manifest.py
tests/project-runtime.sh

skills/feature-development/SKILL.md
skills/release-check/SKILL.md
skills/change-impact-analysis/SKILL.md
skills/code-review/SKILL.md
skills/skill-authoring/SKILL.md
skills/testing/SKILL.md           # only if the heuristic warrants a small change
```

Do not add a new evidence kind unless the existing evidence vocabulary genuinely cannot describe the observed result.

---

# 15. Required skill-authoring procedure

Agents DevKits `AGENTS.md` requires `skills/skill-authoring/SKILL.md` for reusable skill-library changes.

For every accepted new/changed skill, follow the current procedure completely:

- skill `SKILL.md`;
- `SOURCE.md` where required / for local adaptation provenance;
- registry entry;
- new trigger value only when needed;
- handoff/related cross-links;
- `SKILLS.md`;
- boundary/collision rules;
- positive routing scenario;
- negative/near-miss routing scenario;
- regenerate routing index;
- execute platform gate.

Do not add a skill without its routing and collision contract.

---

# 16. Provenance requirements

For reconstructed pstack concepts:

- record upstream repository: `https://github.com/cursor/plugins`;
- record path(s) used;
- pin source revision;
- record retrieval date;
- record that the implementation is adapted/reconstructed for Agents DevKits;
- retain required MIT attribution/licensing where text/code is materially copied;
- prefer concept reconstruction over copying prose.

Pinned pstack-path revision used for this handoff:

```text
5bf2b1544db739998121a306340631963c2ff3de
```

Note: this is the latest commit returned for the `pstack/` path at handoff preparation time. Re-check upstream before implementation if fresh upstream behavior is intentionally desired; do not silently change the source reference mid-implementation.

---

# 17. Verification strategy for implementation

Use focused verification after every coherent phase, not only at the end.

Minimum final checks:

```bash
python3 scripts/generate_routing_index.py --check
python3 scripts/gate.py
```

Also run focused tests for:

- registry/routing changes;
- project manifest parsing/normalization;
- `project.py doctor`;
- `project.py verify` unchanged behavior;
- progressive/PCK integration fixtures;
- live-eval schema/analyzer unit tests;
- path traversal / invalid harness declaration cases.

Do not weaken tests, validators, thresholds, routing rules, or evidence semantics to achieve green output.

---

# 18. Implementation sequence

Recommended dependency-safe order:

## Milestone 0 — Baseline reconciliation
- verify current branch/HEAD;
- read repository instructions;
- run baseline gate;
- compare current state with this handoff;
- produce `EXISTING / PARTIAL / MISSING / REJECTED` gap map.

## Milestone 1 — Verification harness owner
- skill ownership + provenance;
- project artifact contract;
- registry/boundaries/catalog/scenarios.

## Milestone 2 — Runtime declaration/doctor support
- manifest representation;
- backward compatibility;
- runtime tests;
- no semantic browser driving inside runtime.

## Milestone 3 — Workflow integrations
- feature-development;
- release-check;
- testing/playwright/debugging handoffs.

## Milestone 4 — Live behavioral eval framework
- schemas;
- fixture/preparation tooling;
- analyzer;
- one runnable existing pilot;
- deterministic validation in gate only.

## Milestone 5 — Proof-oriented impact analysis
- safety-claim reference;
- output contract;
- routing/eval coverage.

## Milestone 6 — Optional adversarial code-review reference
- conditional protocol;
- privacy/authorization;
- no auto-fix.

## Milestone 7 — Workflow-learning structural promotion
- policy;
- skill-authoring reference;
- behavior-eval linkage.

## Milestone 8 — Optional unattended decision trail
- only if needed after ownership review.

## Milestone 9 — Full gate / documentation / changelog
- regenerate routing index;
- full gate;
- report real results.

Do not implement autonomous merge in any milestone.

---

# 19. Risks to actively prevent

## Risk: duplicate control plane

Symptom:

```text
poteto-mode-like router + existing Agents DevKits routing
```

Prevention: no second sticky/general router.

## Risk: skill explosion

Symptom: each principle becomes a separate skill.

Prevention: principles become rules, references, validators, tests, or policy under existing owners.

## Risk: harness becomes documentation theater

Symptom: `HARNESS.md` exists but no one has ever driven it.

Prevention: creation workflow attempts one end-to-end real feature proof when environment permits; otherwise reports the limitation.

## Risk: feature map becomes a second product specification

Prevention: record user-observable verification paths only; product intent remains with project/product sources of truth.

## Risk: `project.py` turns into an agent platform

Prevention: deterministic validation/execution only.

## Risk: live eval claims become marketing

Prevention: record exact model/runtime/snapshot/sample size and separate static contracts from measured behavior.

## Risk: biased eval

Prevention: sanitized candidate environments, organic prompt, hidden rubric, anonymous judge labels, controlled comparison.

## Risk: multi-model review leaks private code

Prevention: explicit authorization for external/model-provider disclosure.

## Risk: permanent agent-history system appears accidentally

Prevention: decision trail remains ephemeral scratch unless explicitly retained as an artifact.

## Risk: PCK integration breaks

Prevention: run all existing progressive integration fixtures; do not alter ownership of PCK project state.

---

# 20. Final implementation report contract

The implementing agent must return:

## Baseline
- starting branch;
- starting commit;
- baseline gate result.

## Architecture
- new/changed owners;
- routing/status choices;
- rejected pstack concepts and reason.

## Files
- exact files added/changed;
- generated files identified as generated.

## Verification
- focused commands/results;
- final routing-index check;
- final `scripts/gate.py` result;
- unavailable checks and remaining uncertainty.

## Provenance
- upstream pstack paths used;
- exact pinned revision;
- local reconstruction notes.

## Residual risks
- known gaps;
- deferred autonomy work;
- any experimental behavior that still needs live agent evaluation.

---

# 21. Definition of done

This reconstruction is done only when all of the following are true:

- Agents DevKits has one bounded owner for project-specific real-surface verification harness lifecycle.
- A consuming repository can declare and validate a harness/feature-map location without `project.py` becoming semantic agent runtime.
- Real-surface proof is connected to feature orchestration and release evidence.
- Existing skill-quality pilots can be executed through a reproducible baseline/candidate live-eval path with blinding.
- Routing evals remain deterministic and separate from live behavior evals.
- Change-impact analysis can identify and qualify a primary safety claim.
- Optional multi-model code review reuses `code-review` ownership.
- Recurring workflow failures are preferentially promoted into structural mechanisms instead of repeated prose.
- No pstack router, Cursor model config, permanent execution-history store, or auto-merge system was imported.
- PCK compatibility tests remain green.
- `python3 scripts/generate_routing_index.py --check` passes.
- `python3 scripts/gate.py` prints `AGENTS DEVKITS GATE: PASS`.
