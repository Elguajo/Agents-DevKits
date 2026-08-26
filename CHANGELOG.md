# Changelog

All notable repository changes are recorded here in addition to Git history. Entries describe user-visible behavior, project assets, workflows, and documentation changes; Git remains the source of exact diffs and authorship.

## [Unreleased]

### Added

- A repository-level changelog for tracking notable additions, changes, fixes, removals, and security updates.
- A validated v2 skill-routing contract with invocation, declarative triggers, capability requirements, input/output, progressive references, verification, and handoff metadata for every portable skill.
- Provider-neutral capability and ephemeral evidence contracts, deterministic routing scenario evals, and a one-command platform gate.
- A cross-platform multi-agent project runtime with version-compatible `agents-devkits.yaml`, Codex/Claude templates, safe instruction adoption, task-aware structured verification, and JSON evidence output.

### Changed

- Continuous integration now validates the complete portable skill library and project runtime in addition to the macOS/Codex Devkit layer.

## History before this changelog

Changes made before 2026-08-11 are preserved in the Git commit history. They are not retroactively assigned release versions.

## Maintenance

- Add an entry under **Unreleased** in the same change that introduces a notable repository update.
- Use the appropriate category: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, or **Security**.
- Describe the outcome for users and contributors, not the implementation detail or every file touched.
- On a release, rename **Unreleased** to a versioned heading with an ISO date and create a fresh **Unreleased** section above it.
- Do not add entries for local experiments, formatting-only edits, or unmerged work.
