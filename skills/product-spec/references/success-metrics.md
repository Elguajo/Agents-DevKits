> Local reference for `product-spec`. Load only when the spec must define how success is measured, not merely what is built.

# Success Metrics and Product Instrumentation
## Goal
Define the smallest set of measurements that would show whether the specified behavior achieved its intended outcome.

## Workflow
1. Restate the user outcome the feature claims to produce.
2. Choose one primary success measure tied to that outcome, not to activity volume.
3. Add a counter-metric that would reveal harm the primary measure could hide, such as increased task time, abandonment, or support load.
4. Define the decision: what result would justify keeping, changing, or removing the feature, and by when.
5. Derive only the events required by those measures. Name each event, its trigger point, and its properties.
6. Check whether the project already emits an equivalent event before adding a new one.
7. State the baseline: the current value, or that no baseline exists and the first period is measurement only.
8. Record the minimum data needed per event, and hand personal or behavioral fields to `privacy-review` before they are specified as collected.

## Rules
- A metric without a decision attached is instrumentation debt; drop it.
- Do not specify a funnel that no one has agreed to act on.
- Vanity counts of clicks, sessions, or page views are not outcomes.
- Collect the least data that supports the decision; instrumentation is data collection.
- Do not claim a baseline or a target that no evidence supports.

## Handoffs
- Personal, behavioral, or third-party analytics fields → `privacy-review`.
- Whether the event can actually be observed in production → `observability-review`.
- Understanding why a metric moved → `ux-research`.

## Output
Outcome, primary measure, counter-metric, decision and timeframe, the event list with properties, baseline status, and the fields that require a privacy decision.
