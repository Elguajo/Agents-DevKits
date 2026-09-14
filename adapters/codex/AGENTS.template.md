# Agents DevKits project brief

Use native Codex skill discovery and only select an installed Agents DevKits
skill when its registry trigger and `SKILL.md` procedure fit the task. Project
instructions and the explicit user request override generic skill guidance.

Before adding code, dependencies, abstractions, services, wrappers, state, or
infrastructure, check whether the behavior is needed, already exists in the
repository, is covered by the language/standard library or native platform, is
available from an installed dependency, or can be met by a small direct change.
Only then add the minimum justified implementation. This is not code golf:
preserve required validation, trust-boundary checks, error/recovery handling,
security, accessibility, compatibility, reliability, and data integrity.

For multi-step changes or release work:

1. Read project instructions and `agents-devkits.yaml` when present.
2. Use the generated `.agents-devkits/ROUTING.md` snapshot when present to find
   candidates and selection levels, then consult the canonical `skills/registry.yaml` for full metadata.
3. Apply levels consistently: `AUTO` selects only a justified boundary; `PROPOSE`
   announces the workflow and continues unless redirected; `ASK` needs an explicit user request.
   Levels do not override safety or authorization rules.
4. Select only justified skills, then load their `SKILL.md` and declared references on demand.
5. When `agents-devkits.yaml` declares project knowledge packs, load only the
   pack relevant to the task and treat its declared sources as provenance.
6. Resolve generic capabilities through available Codex tools; do not assume unavailable tools exist.
7. Collect observed evidence and hand off to the relevant specialist or `release-check`.

Treat objective checks and expert review separately. Do not run manifest commands
unless verification was explicitly requested, and do not claim unavailable work
passed.
