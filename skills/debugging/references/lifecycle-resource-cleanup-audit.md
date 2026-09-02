> Integrated from the v0.1 prompt/skill prototype `lifecycle-resource-cleanup-audit`. Load this reference only when its trigger applies.

# Lifecycle & Resource Cleanup Audit
## Goal
Ensure every long-lived resource has clear ownership, correct lifetime, and deterministic cleanup.

## Workflow
1. Map creation, ownership, reuse, and disposal of relevant resources.
2. Trace mount/unmount, focus/blur, background/foreground, start/stop, reconnect, and restart transitions as relevant.
3. Look for duplicate listeners/subscriptions, orphaned tasks, unreleased handles, retained closures, stale caches, and repeated object creation.
4. Verify cleanup is idempotent and occurs on all exit paths.
5. Add lifecycle-focused regression tests where practical.

## Rules
- Do not dispose intentionally shared resources without understanding ownership.
- Distinguish harmless re-renders from actual resource recreation.
- Check both leaks and premature cleanup.

## Output
Ownership map, lifecycle defects, fix, verification, and residual leak risk.
