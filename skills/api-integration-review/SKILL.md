---
name: api-integration-review
description: Review how the project consumes an external or third-party API: contract fidelity, authentication and credential lifecycle, versioning and provider change, pagination and completeness, rate limits and quota, and environment separation. Use when integrating or changing a dependency on an API the project does not control.
---

# API Integration Review

Own **the contract with an API the project does not control**, and the assumptions that break when the provider changes.

## Use when
- A third-party or cross-service API is introduced, upgraded, or replaced.
- Data from an external API is parsed, cached, persisted, or shown to users.
- Provider auth, quota, pagination, webhook, or versioning behavior is unclear.

## Do not use when
- The concern is behavior when the call fails, times out, or runs twice; use `reliability-review`.
- The concern is credential exposure, SSRF, or an attack path; use `security-review`.
- The project owns both sides of the interface and the question is module boundaries; use `solution-architecture`.
- The project owns both sides and consumers of a changing contract must be found; use `change-impact-analysis`.

## Workflow
1. Identify each external endpoint the change depends on and the authoritative provider documentation for it.
2. Compare the code's assumed request and response shape against the documented contract: required fields, optional fields, nullability, enum values, units, and time zones.
3. Check parsing strictness: whether an unknown field, a missing optional, or a changed type degrades safely or throws in production.
4. Review the auth model: credential type, scope, expiry, refresh, rotation, and what happens on revocation. Hand storage and exposure of the credential to `security-review`.
5. Check versioning and provider change surface: pinned version, deprecation notices, breaking-change policy, and how the project would learn about a change before users do.
6. Check completeness: pagination, cursors, limits, ordering guarantees, and whether partial pages are silently treated as complete results.
7. Check rate limits and quota as a contract fact: documented limits, the project's actual call volume, batching, caching, and cost. Hand the behavior when a limit is hit to `reliability-review`.
8. Check environment separation: sandbox versus production endpoints, test credentials, and any request that could reach production data from a non-production run.
9. Check inbound direction where present: webhook authenticity, delivery guarantees, ordering, and replay expectations.
10. Verify test coverage does not depend on the live provider, and that recorded fixtures match the current contract.

## Rules
- The provider's current documentation outranks the code's assumptions and outranks memory of the API.
- An undocumented field observed in a response is not a contract; do not build on it without saying so.
- Do not conflate a provider outage with a contract defect; classify each finding.
- Do not send real credentials or customer data to a provider during review.
- State explicitly when a finding could not be verified without live calls.

## Handoffs

- Timeout, retry, backoff, idempotency, and partial-failure semantics → `reliability-review`.
- Credential storage, scope, SSRF, and untrusted response handling → `security-review`.
- Whether an integration failure would be visible in production → `observability-review`.
- Persisted copies of provider data and their retention → `data-storage-review`.
- Fixtures and contract regression coverage → `testing`.

## Output contract
Return the endpoints and provider docs consulted, contract mismatches with evidence, auth and quota assumptions, provider-change exposure, findings by severity with the minimal fix, and what could not be verified without live access.
