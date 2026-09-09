# Devkit provenance

The Devkit layer was ported from the private repository
Elguajo/elguajo-devkit at revision
f6f8baa8a7b7549d8d1f53076913fdc87fb9a828 on 2026-09-09.

The public port deliberately excludes the tracked personal Codex configuration,
machine snapshots, generated export archives, local secrets, and host-specific
overrides. Portable configuration, scripts, profiles, tests, and documentation
are maintained here from this point forward. The public layer supports macOS
and native Windows PowerShell; Gstack remains macOS-only because its upstream
installer does not support native PowerShell.
