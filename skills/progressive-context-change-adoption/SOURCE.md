# Source

- **Origin:** Local adaptation.
- **Research source:** `Elguajo/Progressive-Context-Kit`, revision
  `2fc0c752d4b2f7f4bd0be8aae3838c74932b4c2e`, inspected 2026-09-13: root
  router; `existing-project-adoption`,
  `architecture-decision`, `documentation-governance`, `project-doctor`,
  `implementation-execution`, and `session-handoff` skills; project-memory and
  layer-ownership documentation; adoption prompt and Phase/Roadmap templates.
- **Inspiration:** A user-supplied reconciliation workflow for introducing a
  new audit, specification, implementation plan, or substantial change request
  into an already active PCK project.
- **External content copied:** None. The procedure was rewritten against
  Agents DevKits ownership, routing, evidence, and safety contracts.
- **License:** PCK is MIT-licensed; no upstream prompt text was copied. This
  local skill is distributed under this repository's license.
- **Local changes:** Made PCK-specific and user-invoked; bounded the workflow
  to durable-state reconciliation without discovery, architecture choice, or
  implementation; added explicit finding dispositions and canonical-owner
  verification. Since 2026-09-13 it is explicitly the PCK adapter of
  `project-state-change-adoption`, retaining only PCK-specific state rules.
