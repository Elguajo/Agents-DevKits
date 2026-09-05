# Defect Evidence and Reproduction

A suspicious observation is a candidate, not a defect. This protocol is what turns one into a report another engineer can act on.

## Reproduction protocol

1. Return to a known start state: fresh session, known data, known route.
2. Repeat the sequence exactly as observed.
3. Remove steps one at a time until only the steps that still cause the failure remain.
4. State the expected behavior and its source: product requirement, existing behavior elsewhere in the product, or a clear user-facing contract.
5. Capture the strongest evidence available at the moment of failure.
6. Determine stability: deterministic, intermittent with a rate, or environment-specific.

If step 1 is impossible because the product cannot be reset, say so in the report; it changes how the defect must be investigated.

## Confidence

- **High** — reproduced reliably, and the expected/actual mismatch is unambiguous.
- **Medium** — reproduced, but the expectation, data, or environment carries real uncertainty.
- **Low** — observed once or intermittently and not reliably reproduced.

Low-confidence items go in the "suspicious, not reproduced" section. Never promote a Low item to a confirmed defect to make a report look stronger.

## Evidence quality

Prefer, in order: a recording or screenshot at the moment of failure; the persisted state after the failure; the failed request with its status and response; the console error with its stack; a precise textual description of what was seen.

Rules:
- Evidence must be tied to the exercised flow and to a user-visible consequence.
- Unrelated console noise, third-party warnings, and expected handled errors are not evidence.
- Do not paste secrets, tokens, personal data, or production customer records into a report; redact them.

## Severity

Severity describes consequence, not effort or code quality.

- **Critical** — data loss or corruption, a security-sensitive user-visible failure, the core product unusable, or a broad irreversible incorrect operation.
- **High** — a critical flow cannot be completed, saved work is lost, a repeated action causes seriously wrong behavior, or a common navigation/session failure blocks work.
- **Medium** — a real feature malfunction with a workaround, or incorrect state, validation, or error handling on a less common path.
- **Low** — a minor functional inconsistency or a low-impact edge case with an easy workaround.

Visual polish, wording preference, and interaction confusion are not functional severities; route them to `visual-qa`, `ux-writing`, or `ux-usability-audit`.

## Report fields

```text
Title        one observable failure, no root-cause guess
Severity     Critical | High | Medium | Low
Confidence   High | Medium | Low
Area/flow    where it occurs
Preconditions   required starting state, account, data, permissions
Steps        minimal numbered sequence
Expected     behavior plus the source of that expectation
Actual       what was observed
Evidence     screenshot, recording, console error, request/response, persisted state
Frequency    always | intermittent (rate) | once | unknown
User impact  concrete consequence for a real user
Handoff      debugging, or the specialist owner when the concern is primarily theirs
```

Do not include a root cause unless the evidence already establishes it. A plausible mechanism belongs in the handoff note as a hypothesis, clearly labelled.

## Re-verification after a fix

Repeat the exact original steps, then the nearby happy path, then one or two adjacent high-risk variations, then re-check runtime evidence. Report the re-verification result explicitly; an unrepeated reproduction is unverified, not fixed.
