---
name: information-architecture
description: "Define or revise a product's structural model: navigation, content hierarchy, route semantics, and critical user flows. Use when a site or product structure must be designed before detailed UI implementation."
---

# Information Architecture

Own **the structural layer of a product experience**. Do not choose visual art
direction, reimplement routes, or replace product scope.

## Use when

- Navigation, page hierarchy, labels, route patterns, or user flows are unclear.
- A content-heavy product needs a findable structure that can grow safely.
- An existing application needs a structural change that must respect current
  routing, layouts, content models, and user behavior.

## Do not use when

- The task is a component-level layout decision; use `design-component` or
  `design-code`.
- The user needs research planning rather than an architecture decision; use
  `ux-research`.
- The task is implementation architecture across software modules; use
  `solution-architecture`.

## Workflow

1. Read product requirements, project instructions, `DESIGN.md` when present,
   and existing evidence about users and content.
2. Inspect the current route tree, navigation, layouts, URL conventions, content
   model, and search/filter behavior. Extend viable conventions instead of
   proposing a parallel structure.
3. Identify primary user jobs, entry points, high-frequency destinations,
   distinct audiences, and expected content growth.
4. Make the smallest set of structural decisions needed for the change:
   sitemap or view hierarchy, navigation tiers, route semantics, content
   priority, labels, and critical flows with states/decision points.
5. For a material structural choice, state the alternative, the user impact, and
   the evidence or assumption behind the recommendation.
6. Produce an IA artifact that links each decision to affected routes, shared
   layouts, content types, or reusable navigation components.
7. Hand design-system implementation to `design-system`/`design-code`, product
   behavior to `product-spec`, and cross-module technical work to
   `solution-architecture`.

## Output contract

Return:

- Existing structural constraints and evidence used
- Sitemap/view hierarchy and URL or route rules
- Navigation model and content priority
- Critical user flows, labels, and growth implications
- Assumptions, open questions, and handoffs
