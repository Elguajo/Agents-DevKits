---
name: journey-mapping
description: Create evidence-aware customer journey maps, service blueprints, empathy maps, or user story maps that align a specific user scenario with product decisions. Use when a cross-touchpoint experience or service workflow must be understood and prioritized.
---

# Journey Mapping

Own **cross-touchpoint experience mapping and alignment**. A map is a decision
tool, not a decorative deliverable or proof of user research.

## Use when

- A team needs to understand a persona's end-to-end experience, pain points, or
  moments of truth.
- Frontstage UI and backstage processes must be connected before changing a
  service.
- A user workflow must be mapped to prioritize a backlog or expose ownership
  gaps.

## Do not use when

- A single interface flow can be specified directly in a product requirement.
- User evidence must first be planned or synthesized; use `ux-research`.
- The task is a technical system diagram rather than a user/service experience.

## Workflow

1. Define one persona, scenario, time boundary, and decision the map must
   support. Split unrelated journeys rather than merging them into one chart.
2. Choose the smallest useful map:
   - customer journey for a persona's chronological product experience;
   - service blueprint for visible interactions plus delivery operations;
   - empathy map for rapid synthesis of a known user segment;
   - user story map for a workflow-shaped product backlog.
3. Gather available evidence: research, analytics, support themes, operational
   data, and existing flows. Label every row or assertion as observed, inferred,
   or assumed.
4. Build the map with consistent language: actions are verbs, touchpoints are
   nouns, pain points describe friction, and opportunities describe a change.
5. Identify the few moments of truth and prioritize opportunities by user impact,
   confidence, feasibility, and responsible owner. Do not jump from an assumed
   pain point directly to a committed feature.
6. Turn prioritized opportunities into a next decision: research, `product-spec`,
   `information-architecture`, `solution-architecture`, or an implementation
   workflow.

## Map contract

Every map must state:

- persona, scenario, time boundary, and evidence basis;
- phases, user goals/actions, touchpoints, and pain points;
- assumptions and unknowns separately from observed facts;
- owners and next decisions for material opportunities.

For a service blueprint, additionally separate customer action, frontstage,
backstage, and support processes. Do not expose private operational or customer
data in a broadly shared artifact without authorization.

## Output contract

Return:

- Map type and why it fits the decision
- Evidence and assumptions
- Structured map content and moments of truth
- Prioritized opportunities with owners/next decisions
- Recommended handoff
