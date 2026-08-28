---
name: ux-research
description: Turn a product uncertainty into a proportionate, decision-oriented UX research plan or evidence synthesis. Use when user behavior, needs, usability, or information scent must be understood before a product or design decision.
---

# UX Research

Own **research design and evidence synthesis for product decisions**. Do not
invent user findings, contact people, or turn assumptions into research results.

## Use when

- A product decision depends on user needs, behavior, usability, or terminology.
- The team needs an interview guide, usability-test plan, research synthesis, or
  a defensible method choice.
- Existing evidence such as support tickets, analytics, notes, or recordings
  needs to be turned into actionable findings.

## Do not use when

- Requirements are already settled and only implementation is needed.
- The task is a UI expert critique without user evidence; use `design-review`.
- The task is to draw a journey or service map; use `journey-mapping` after the
  evidence scope is defined.

## Workflow

1. State the decision that research must inform. If no decision would change,
   recommend not running research.
2. Separate known evidence, assumptions, and unanswered questions. Inspect
   existing project context before proposing a new study.
3. Write a small set of behavior-focused research questions. Avoid questions
   that ask participants to predict preferences or validate a chosen solution.
4. Choose the lightest method that can reduce the uncertainty:
   - exploratory interview or contextual inquiry for unmet needs and workflows;
   - usability test for a design, prototype, or existing flow;
   - analytics or support-data review for observed live behavior;
   - card sorting or tree testing for navigation and terminology;
   - expert review only when direct user research is not justified.
5. Produce a proportionate plan: participant criteria, task scenarios or guide,
   data to capture, success signals, privacy constraints, and analysis method.
6. If evidence is supplied, synthesize it as observation → pattern → insight →
   decision implication. Preserve source links and mark inferences.
7. Prioritize findings by impact and confidence, then hand off to `product-spec`,
   `information-architecture`, `journey-mapping`, `prototype`, or the relevant
   implementation specialist.

## External-action boundary

- Do not recruit, contact participants, access private recordings, submit
  surveys, or upload research data without explicit authorization.
- Minimize and anonymize participant data in outputs. Do not copy personal data
  into a durable project artifact unless the user explicitly requires it.
- A plan, script, or inferred finding is not evidence that research occurred.

## Output contract

Return:

- Decision and uncertainty under study
- Evidence, assumptions, and unanswered questions
- Recommended method and a right-sized study or synthesis plan
- Findings with source/confidence when evidence was provided
- Next decision and specialist handoff
