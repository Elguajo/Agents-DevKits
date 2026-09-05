---
name: exploratory-qa-audit
description: Actively exercise a runnable website or application to discover unknown user-observable functional defects, reproduce them, and report calibrated evidence before any fix is attempted. Use when the product should be explored and challenged for unknown bugs rather than checked against a predefined test case.
---

# Exploratory QA Audit

## Goal
Discover **unknown, user-observable functional defects** in a product that can actually be run, then hand each confirmed defect to `debugging` with a minimal reproduction, evidence, severity, and confidence.

This skill owns discovery and reproducible evidence. It does not diagnose root causes and does not repair implementation.

Pair it with `ux-usability-audit`:

```text
exploratory-qa-audit → Does it work correctly?
ux-usability-audit   → Is it understandable and usable?
```

## Primary ownership
This skill owns **discovery of unknown functional defects by exercising a real product**:
- exploration of critical user journeys beyond the happy path;
- input, action, navigation, state, timing, interruption, persistence, and multi-context variation;
- state-transition, validation, and error-handling failures observed in use;
- console, runtime, and network failures tied to an exercised flow and a user-visible consequence;
- reproduction, severity triage, and confidence calibration;
- the explicit untested/blocked list that bounds the audit.

It does **not** own root-cause diagnosis, deterministic browser regression automation, automated non-browser coverage, usability quality, visual fidelity, accessibility criteria, performance diagnosis, security testing, or the ship decision. Hand those to the owners listed under [Handoffs](#handoffs).

## Use when
- The user wants the application or website actively tested like a senior QA engineer.
- The user wants bugs they do not already know about, or asks to "try to break it".
- Edge cases, interrupted operations, or unusual sequences should be exercised before release.
- A report is vague ("something feels buggy") and no single defect is reproduced yet.
- A recently built or recently changed product needs a pre-release exploratory pass.

## Do not use when
- One concrete defect is already reproduced and the user wants it fixed → `debugging`.
- The task is to automate or re-verify known flows → `playwright-testing`.
- The concern is comprehension, ease of use, or interaction logic → `ux-usability-audit`.
- The task is a repository-wide technical health audit of source code → `project-audit`.
- No runnable or rendered product exists and only source is available. Say so; source review is not exploratory QA.

## Operating modes

**Audit only** — the default when the user asks to inspect, test, audit, or find bugs. Do not modify the implementation.

**Audit then repair handoff** — only when the user explicitly asked to find and fix. Discovery and evidence still complete first; then hand each confirmed defect to `debugging`, re-run the original reproduction after the fix, and hand regression protection to `testing` or `playwright-testing` where it is justified. Never fix a defect that is still a hypothesis.

## Workflow

Sequence: **Understand → Charter → Baseline → Explore → Observe → Reproduce → Triage → Report → Handoff → Re-verify**. Do not start from code guesses.

### 1. Understand the product
Establish enough context to know what "correct" means: product purpose, users, critical journeys, authentication and session model, important persistent data, navigation model, forms and mutations, async work, integrations, and known constraints.

Identify the critical user journeys first (sign-in, onboarding, create/edit/delete, search and filter, upload, save and restore, checkout, settings, deep links, permission-dependent actions, recovery and retry).

Do not invent requirements. When the expected behavior is genuinely unclear, record it as `Expectation unclear` instead of reporting a defect.

### 2. Build a compact charter
Before exploring, write a small risk-based charter: for each important area, the user goal, what could go wrong, the states the flow can enter, what can be varied, what can interrupt it, and what evidence is observable. Prioritize by user and business consequence, not by screen count.

Use `references/exploratory-charter.md` when the product has several flows.

### 3. Establish a baseline
Run each critical happy path once and record the starting state, inputs, expected outcome, observed outcome, resulting persisted state, and console/network health where tooling allows. Edge cases are only interpretable against a baseline, so do not start with extreme cases.

### 4. Explore systematically
Exercise the product as a person would, choosing the dimensions that fit the flow rather than mechanically running every idea: input variation, repeated and interrupted actions, back/forward/refresh/deep links, first-time and returning and empty and error states, slow or failing responses, persistence across reload, and multi-tab behavior.

Use `references/exploratory-test-heuristics.md` for the dimension catalogue.

Do not send destructive or abusive payloads to production or third-party systems, and do not claim a condition was tested when the environment could not produce it.

### 5. Observe runtime evidence
Where browser or runtime tooling is available, watch for uncaught errors, unhandled rejections, failed or unexpectedly repeated network requests, mishandled response statuses, infinite loading, and unexpected remounts or navigation while the flow runs.

A console warning is not automatically a defect, and a failed request that is expected and handled correctly is not a defect. Tie every piece of runtime evidence to an exercised flow and a user-visible consequence.

### 6. Reproduce before claiming
A suspicious observation is not yet a defect. Reset to a known start state, repeat the minimal sequence, remove irrelevant steps, confirm the expected/actual mismatch, capture the strongest available evidence, and establish whether the failure is deterministic, intermittent, or environment-specific.

Classify confidence as High (reproduced reliably with a clear mismatch), Medium (reproduced, but expectation or environment is uncertain), or Low (not reliably reproduced). Low-confidence observations are reported separately and never as confirmed defects.

Use `references/defect-evidence.md` for the reproduction protocol, severity definitions, and the defect report fields.

### 7. Triage and report
Severity follows user and business consequence, not code quality: Critical (data loss or corruption, core product unusable, broad irreversible wrong operation), High (a critical flow cannot be completed, saved work is lost, a common navigation or session failure blocks work), Medium (a real malfunction with a workaround, or an incorrect state on a less common path), Low (minor functional inconsistency with an easy workaround).

Report each confirmed defect with title, severity, confidence, area, preconditions, minimal steps, expected, actual, evidence, frequency, user impact, and suggested handoff. Do not guess a root cause the evidence has not established, and do not classify visual polish or preference as a functional defect.

### 8. Hand off and re-verify
Route each finding to its owner (see [Handoffs](#handoffs)). If a fix lands, repeat the exact original reproduction, repeat the nearby happy path, exercise one or two adjacent high-risk variations, and re-check runtime evidence. A code diff without a repeated reproduction is **unverified**, not fixed.

## Safety and environment
- Prefer local, staging, or test environments for anything destructive.
- Do not create charges, send real messages, delete production data, or trigger irreversible third-party effects in order to "test thoroughly".
- Use test accounts and test data where they exist, and respect the authorization the user actually gave.
- If a risky scenario cannot be tested safely, list it as untested rather than simulating a result.

## Rules
- Discovery before repair: record evidence before any code changes.
- Reproduce before reporting; keep unreproduced observations in a separate section.
- Never report a passed check, a tested condition, or a defect that was not actually observed.
- Expected behavior must come from product requirements, existing behavior, or a clear user-facing contract, never from preference.
- Runtime noise is not evidence unless it is tied to an exercised flow and a consequence.
- State what was not covered; an audit without an untested list overstates itself.
- Do not become a super-debugger: the mechanism behind a defect belongs to its specialist owner.

## Handoffs
- Confirmed defect needing root cause and a fix → `debugging`.
- Deterministic browser regression coverage for the reproduction → `playwright-testing`.
- Unit or integration regression coverage → `testing`.
- Confusing but functionally correct interaction → `ux-usability-audit`.
- Visible mismatch against approved visual intent → `visual-qa`.
- Accessibility criteria → `accessibility-review`.
- Failure that appears to depend on interleaving or shared state → `concurrency-review`.
- Retry, idempotency, partial-state, or recovery semantics → `reliability-review`.
- Durable data integrity, growth, or loss beyond the observed symptom → `data-storage-review`.
- Performance-only symptom → `performance-review`.
- Security-sensitive behavior → `security-review`.
- The failure cannot be explained from available production signals → `observability-review`.
- Ship or no-ship decision → `release-check`.

## Output contract
1. **QA verdict** — short assessment of current functional reliability.
2. **Coverage performed** — flows and dimensions actually exercised.
3. **Confirmed defects** — prioritized reports with the fields from step 7.
4. **Suspicious, not reproduced** — kept separate from confirmed defects.
5. **No issue found** — only for important areas that were actually exercised.
6. **Untested or blocked** — what could not be verified, and why.
7. **Recommended handoffs** — which finding goes to which owner.

Do not pad the report with speculative issues.
