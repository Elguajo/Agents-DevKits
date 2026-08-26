---
name: security-review
description: Perform a focused security review of implemented application code and configuration, covering trust boundaries, authentication, authorization, validation, secrets, injection, browser threats, SSRF, file handling, dependencies, and abuse controls. Use for security-sensitive changes or pre-release review.
---

# Security Review

Own **security risk analysis of concrete code/configuration**. Do not replace a general code review.

## Use when
- Changes touch authentication, authorization, payments, user data, uploads, APIs, admin actions, secrets, external requests, or other trust boundaries.
- The user explicitly requests a security audit/review.
- A release needs targeted security verification.

## Do not use when
- The task is ordinary maintainability/correctness review; use `code-review`.
- There is no code/configuration to inspect and the user only wants architecture; use `solution-architecture` and include security constraints there.

## Workflow
1. Identify assets, actors, trust boundaries, privileged operations, and untrusted inputs relevant to the change.
2. Inspect authentication and session assumptions.
3. Verify authorization at the server/data boundary, not only in UI controls.
4. Check validation/encoding around user-controlled input and output.
5. Check injection classes relevant to the stack: SQL/NoSQL, command, template, path, header, and XSS.
6. Check CSRF/cross-origin assumptions for state-changing browser flows where applicable.
7. Check SSRF/open redirect risks around user-influenced URLs and server-side requests.
8. Review file upload/download handling, path traversal, type/size limits, and storage exposure when relevant.
9. Check secrets, logging, error messages, environment/configuration, and accidental sensitive-data exposure.
10. Review rate limits, replay/idempotency, abuse controls, and privilege escalation for sensitive operations.
11. Inspect dependency/configuration risk when it is part of the changed surface.
12. Recommend verification tests for high-impact findings.

Load [`references/web-surface-triage.md`](references/web-surface-triage.md) only
when the changed surface involves authentication, permissions, untrusted input,
webhooks, uploads/downloads, or outbound requests.

## Rules
- Tie every finding to a plausible attack path; avoid checklist theater.
- Do not claim a system is "secure" because no issue was found in a limited review.
- Distinguish confirmed vulnerabilities from hypotheses requiring runtime/infrastructure verification.
- Prefer fixes at the trust boundary over client-side mitigations.
- Do not expose real secrets in output.

## Output contract
For each finding include severity, affected trust boundary, attack scenario, evidence, impact, and minimal remediation. End with the reviewed artifact, review decision, checks actually run or inspected, and residual areas that were not verified.
