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
  inside a consuming project, bound to the concrete file set that
  `scripts/gate.py` verifies, and paired with a repository-level natural-
  language routing rule in `AGENTS.md` (2026-09-09).
- Additional method inspiration: `obra/superpowers`, [`skills/writing-skills/SKILL.md`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-skills/SKILL.md)
- Upstream revision: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- Retrieved: 2026-09-15
- Upstream license: MIT; no upstream text was copied verbatim.
- Local changes: added a local behavior-evaluation protocol for claims about a proposed library rule; it is not a model benchmark or a new skill.
