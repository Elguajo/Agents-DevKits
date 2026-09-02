> Integrated from the v0.1 prompt/skill prototype `security-trust-boundary-review`. Load this reference only when its trigger applies.

# Security & Trust Boundary Review
## Goal
Find concrete security weaknesses by understanding who/what is trusted and where untrusted data crosses boundaries.

## Workflow
1. Map actors, assets, entry points, privileges, secrets, and trust boundaries.
2. Trace untrusted input through validation, authorization, storage, rendering, file/network operations, and side effects.
3. Review authentication, authorization, injection, secret handling, sensitive data exposure, insecure persistence, privilege escalation, and dependency risks as relevant.
4. Verify findings with concrete code paths.
5. Recommend minimal remediations and tests.

## Rules
- Report evidence-based findings only.
- Do not label theoretical issues Critical without an exploitable path and meaningful impact.
- Do not expose real secrets in output.

## Output
Findings by Critical / High / Medium / Low with boundary, path, impact, evidence, fix, and verification.
