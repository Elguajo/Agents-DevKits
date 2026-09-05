# Exploratory Charter

A charter turns "click around and see" into a bounded, prioritized session. Write it before exploring, keep it short, and revise it when the product teaches you something.

## One charter per area

For each important area, record six lines:

- **Goal** — what a user is trying to accomplish here.
- **Risks** — what could plausibly go wrong, expressed as user consequence.
- **States** — the states the flow can legitimately enter.
- **Variables** — what a user can change: inputs, order, timing, entry point, permissions, data volume.
- **Interruptions** — what can happen mid-flow: refresh, navigation, cancellation, network loss, session expiry, a second tab.
- **Evidence** — what is observable: rendered state, persisted data, console, network, stored files, notifications.

## Prioritize by consequence

Rank areas by what a failure costs the user or the business, not by how many screens they contain:

1. irreversible or destructive operations (delete, publish, pay, send);
2. flows that persist user work;
3. authentication, session, and permission boundaries;
4. the primary conversion or task-completion path;
5. flows recently changed or built;
6. flows with known past defects;
7. everything else.

An area nobody can reach and nobody depends on is a poor use of a session.

## Time-box each charter

Give each charter a rough budget and a stop condition ("stop when the three highest risks are exercised or two Critical defects are found"). When a charter overruns because it keeps producing defects, record that as a finding about the area, not only as individual bugs.

## Track what the charter did not cover

Every charter ends with an explicit untested list: dimensions skipped, states the environment could not produce, and scenarios that were unsafe to run. This list belongs in the final report; without it, the audit implies coverage it does not have.

## Revise, do not improvise

New information is a reason to update the charter, not to abandon it. When exploration reveals an unexpected state, a hidden entry point, or a second source of truth, add it to States or Variables so the coverage claim stays honest.
