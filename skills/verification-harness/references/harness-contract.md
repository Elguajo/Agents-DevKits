# Project verification-harness contract

Store the project-local contract at `.agents-devkits/verification/HARNESS.md`.
It must be understandable by an agent without prior project context and contain:

## Surface

Name the primary user-observable surface (web UI, CLI/TUI, desktop, API/service,
mobile, or executable library contract), and name secondary surfaces only when
they affect the proof.

## Launch

Use exact repository-grounded prerequisites and commands. Do not infer them.

## Readiness / Doctor

Define a read-only condition that shows the launched instance is the intended
one and is worth driving: for example, owned port/process, expected build,
valid session prerequisite, or version endpoint.

## Drive

Describe a real interaction using stable semantic selectors/routes, CLI or PTY
commands, HTTP requests, or already-owned automation. Avoid coordinates and
brittle ordering.

## Evidence

For each applicable proof preserve the relationship:

```text
user action → observable result → relevant side effect
```

Use screenshots/routes/persisted state, terminal output/exit code/generated
file, or API response/object-state change as appropriate. A mock is not proof
of a real boundary unless that mock is the intentionally owned contract.

## Isolation and cleanup

Name how ports, profiles, tenants, temporary data, schemas, or worktrees avoid
other user and agent state. Clean up only resources created by the run; track
an exact process, pid, or session rather than killing by generic name. Retain
evidence after cleanup.

## Feature map

`features/README.md` indexes small records with these semantics:

```text
User outcome
Entry path
Drive procedure
Proof of success
Side effects
Prerequisites / gotchas
```

When maintenance reveals a mismatch, classify it before editing: documentation
or harness drift, harness capability gap, product defect, or unavailable
environment. Only the first two belong in this harness.
