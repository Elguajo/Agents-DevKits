> Integrated from the v0.1 prompt/skill prototype `dependency-introduction-review`. Load this reference only when its trigger applies.

# Dependency Introduction Review
## Goal
Determine whether each new dependency is justified and whether its maintenance, security, runtime, and lock-in costs are acceptable.

## Workflow
1. Identify every new/changed dependency and why it was introduced.
2. Check whether the project already provides equivalent functionality.
3. Evaluate maintenance health, security exposure, licensing constraints when relevant, bundle/runtime cost, transitive dependencies, platform compatibility, and lockfile impact.
4. Compare with a simpler native or existing-project solution.
5. Recommend keep/replace/remove based on concrete trade-offs.

## Rules
- Do not optimize for zero dependencies.
- Do not invent package vulnerabilities; verify with available tooling/data.
- Consider operational and upgrade cost, not only code size.

## Output
Per dependency: purpose, benefits, risks, alternatives, recommendation, and migration cost.
