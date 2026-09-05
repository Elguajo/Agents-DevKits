---
name: privacy-review
description: Review what personal or sensitive data a system collects, why it exists, where it flows, how long it is kept, and how a user can see or remove it. Use for telemetry, analytics, third-party sharing, profiles, tracking identifiers, and retention or deletion behavior.
---

# Privacy Review

Own **whether personal data should exist at all, and on what terms**. A system can be secure and still handle data badly.

## Use when
- The change collects, derives, stores, exports, or transmits personal, behavioral, location, device, or otherwise sensitive data.
- Telemetry, analytics, crash reporting, session replay, or a third-party SDK is added or expanded.
- Retention, deletion, export, consent, or a data-sharing question is raised.

## Do not use when
- The concern is an attacker reaching the data; use `security-review`.
- The concern is durability, growth, integrity, or recovery of stored data; use `data-storage-review`.
- The concern is whether a production failure can be diagnosed; use `observability-review`, which hands its diagnostic payload here.

## Workflow
1. Inventory the personal or sensitive fields the change actually touches, from the code rather than from the feature description.
2. For each field, record why it exists, who reads it, and what breaks if it is removed.
3. Test minimization: can the purpose be met with a coarser value, a derived aggregate, a client-local value, or nothing.
4. Trace every outbound flow: third-party SDKs, analytics endpoints, crash reporters, logs, URLs and query strings, support tooling, backups.
5. Check identifiers: are stable cross-session or cross-product identifiers used where an ephemeral or scoped one would do.
6. Check retention and deletion: declared lifetime, actual cleanup, orphaned copies in logs, caches, exports, and backups.
7. Check user-facing control: notice at the point of collection, consent where it is required, and a real path to view, export, and delete.
8. Check defaults: whether collection is on by default and whether that default is defensible.
9. Check special categories separately: children's data, health, biometrics, precise location, financial identifiers, and government identifiers.
10. Report findings by severity with the smallest change that removes the exposure.

## Rules
- Data that is never collected needs no policy; prefer removal over control.
- Do not treat encryption or access control as a substitute for minimization.
- Do not assert a legal conclusion; name the obligation class and hand the decision to the owner.
- Logs, analytics, and error payloads are collection, even when they are incidental.
- Do not restate a privacy policy as evidence that behavior matches it; verify the behavior.
- Do not print real personal data in findings; describe the field and its source.

## Handoffs

- Attack path, access control, or secret exposure → `security-review`.
- Retention mechanics, growth, cleanup jobs, and durable-data health → `data-storage-review`.
- Removing a persisted field or shortening retention on existing records → `data-migration`.
- Diagnostic value of a signal that must be reduced or dropped → `observability-review`.
- Ship decision → `release-check`.

## Output contract
Return a data inventory with purpose per field, the flows that leave the system, findings by severity with the minimization or retention fix for each, what remains an owner decision rather than an engineering one, and what was not verified.
