# Source note

This is an original local skill, not a vendored copy.

- Motivation: external review of the skill catalog (2026-09-05) recommended a
  `skill-authoring` meta-capability once the repository became a routing system
  rather than a prompt collection.
- Method basis: the decision path already documented in `docs/workflow-maintenance.md`.
- Upstream license: none; the procedure was written against this repository's
  actual registry, boundary, eval, and gate contracts.
- Retrieved: 2026-09-05
- Local changes: restricted to `invocation: [user]` so it cannot be selected
  inside a consuming project, and bound to the concrete file set that
  `scripts/gate.py` verifies.
