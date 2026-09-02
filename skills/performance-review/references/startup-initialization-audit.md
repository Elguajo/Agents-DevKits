> Integrated from the v0.1 prompt/skill prototype `startup-initialization-audit`. Load this reference only when its trigger applies.

# Startup / Initialization Audit
## Goal
Minimize work required before the application or feature becomes usable while preserving required initialization semantics.

## Workflow
1. Trace the startup/initialization path end to end.
2. Measure or identify blocking I/O, storage reads, migrations, network requests, parsing, cache building, dependency construction, and repeated setup.
3. Separate required-before-ready work from work that can be lazy, deferred, cached, or incremental.
4. Check whether initialization accidentally reruns on focus/navigation/lifecycle events.
5. Implement or recommend the smallest scheduling/lifecycle fix and verify readiness behavior.

## Rules
- Do not defer work required for correctness without a safe dependency boundary.
- Do not mask startup with fake loading delays.
- Consider first-run/migration behavior separately from steady-state startup.

## Output
Critical path, unnecessary work, proposed sequencing, before/after verification, and first-run caveats.
