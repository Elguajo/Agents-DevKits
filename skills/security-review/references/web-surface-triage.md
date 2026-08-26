# Web-surface triage

Load this reference only when a changed surface handles identity, permissions,
untrusted input, external callbacks, file transfer, or server-side outbound
requests. It helps focus the review; it does not replace project-specific threat
models or runtime verification.

| Surface | First questions | Evidence to seek |
|---|---|---|
| Authentication and sessions | Who establishes identity and how is it renewed or revoked? | Server-side identity checks and relevant tests. |
| Authorization | Is permission enforced at the data or action boundary? | Denied-path and cross-tenant behavior where applicable. |
| Untrusted input | Where is validation, encoding, and parsing performed? | Input-boundary tests and sink-specific review. |
| Webhooks and callbacks | Is origin/authenticity verified and replay handled? | Signature, timestamp, idempotency, and failure-path evidence. |
| Uploads and downloads | Are type, size, path, and access controls enforced? | Boundary validation and storage exposure review. |
| Outbound requests | Can user input influence host, protocol, or redirects? | SSRF/redirect validation at the server boundary. |

Record a limitation as `unavailable` or `inferred` evidence when the required
runtime or infrastructure check cannot be observed.
