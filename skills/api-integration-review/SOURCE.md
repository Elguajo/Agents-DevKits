# Source note

This is an original local skill, not a vendored copy.

- Motivation: external review of the skill catalog (2026-09-05) proposed an
  API integration owner; the concern was accepted only after a boundary was
  defined that keeps failure semantics with `reliability-review` and credential
  exposure with `security-review`.
- Upstream license: none; the workflow was written for this repository.
- Retrieved: 2026-09-05
- Local changes: rate limits are owned here as a contract fact, while behavior
  when a limit is reached is handed to `reliability-review`.
