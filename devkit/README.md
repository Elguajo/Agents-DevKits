# Agents DevKits developer-machine DevKit

Portable, safe developer-machine bootstrap for macOS and Windows 11. It
recreates the portable parts of a Codex/AI development environment without
copying sessions, credentials, private keys, caches, or trusted project paths.

## Supported platforms

- macOS: native shell with Homebrew.
- Windows 11: native PowerShell with winget. Git Bash and WSL are not required
  for DevKit itself.
- Linux is intentionally unsupported.

## Quick start

macOS:

```sh
git clone https://github.com/Elguajo/Agents-DevKits.git
cd Agents-DevKits
./devkit.sh doctor
./devkit.sh bootstrap --profile base --profile web --profile ai
```

Windows PowerShell:

```powershell
git clone https://github.com/Elguajo/Agents-DevKits.git
cd Agents-DevKits
.\devkit\setup.ps1 doctor
.\devkit\setup.ps1 bootstrap --profile base --profile web --profile ai
```

Preview meaningful changes first:

```sh
./devkit.sh bootstrap --profile base --profile web --profile ai --dry-run
```

```powershell
.\devkit\setup.ps1 bootstrap --profile base --profile web --profile ai --dry-run
```

`devkit.sh` is the macOS entrypoint; use `.\devkit\setup.ps1` for the native Windows entrypoint.
See [Windows DevKit notes](../docs/devkit-windows.md) for first-run validation,
permissions, CLI-path diagnostics, and Windows-specific maintenance rules.

## Prerequisites

On macOS, install [Homebrew](https://brew.sh) before running `bootstrap`.
On Windows, install **App Installer** so that `winget` is available. If
PowerShell blocks a checked-out script, run the current process with:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Then rerun the DevKit command. This changes no machine-wide execution policy.

## Architecture

The generated `~/.codex/config.toml` is composed rather than copied:

```text
config/portable/base.toml + config/portable/plugins.toml
  + enabled mcp/definitions/*.toml
  + config/platform/<macos|windows>.toml
  + machines/<hostname>/codex.toml (ignored)
```

Composition rejects duplicate TOML tables. The installer always creates a
timestamped backup before replacing Codex or Serena configuration. Run
`./devkit.sh backup` or `.\devkit\setup.ps1 backup` to safely capture only local
Codex project-trust entries into the ignored machine layer; it does not copy
the entire application configuration back into Git.

`config/portable/` contains only shared settings and the Codex plugin
declarations present in the source environment. `config/platform/macos.toml`
contains the macOS-only plugin declaration; application-binary integrations
are preserved only in the ignored machine layer. The Windows layer remains
intentionally empty until a native Windows integration is verified.

To add a verified host-only setting, create the ignored file below. Do not add
an MCP table already defined by a portable layer: composition will reject it.

```text
machines/<hostname>/codex.toml
```

## Profiles and dependencies

Profile intent is shared in `profiles/manifest.tsv`; platform adapters choose
the package manager. macOS keeps its existing Brewfiles. Windows maps the same
intent to winget IDs.

| Profile | Capabilities |
| --- | --- |
| `base` | Git, GitHub CLI, ripgrep, uv, shell utilities |
| `web` | Node LTS, pnpm, Yarn, Corepack |
| `ai` | Python 3.12 and Bun |
| `db` | PostgreSQL, Redis, SQLite |
| `mobile` | SwiftLint on macOS; intentionally skipped on Windows |
| `macos` | macOS developer defaults only |

The doctor reports package manager, core command availability, Codex config,
Serena/MCP runtime readiness, Gstack state, unresolved secret placeholders,
and Windows symlink capability. It is read-only.

## Codex plugins and MCP

Portable plugin declarations include the current GitHub, Linear, Figma,
documents, spreadsheets, presentations, PDF, template creator, Chrome,
computer-use, visualize, browser, Sites, Codex app tools, and unified
computer-use plugins. These depend on Codex marketplaces/runtimes being
available, so doctor treats absent app-provided runtime support as a warning.
Build macOS Apps remains macOS-only.

No MCP server is enabled by default. The portable registry offers Sequential
Thinking, DuckDuckGo, Context7, Playwright, Serena, Memory, shadcn, Chrome
DevTools, Anytype, Affine, OpenPencil, and Ideon. Manage a machine's selection
without editing tracked config:

```sh
./devkit.sh mcp list
./devkit.sh mcp disable affine
./devkit.sh mcp enable affine
./devkit.sh mcp doctor
./devkit.sh install
```

PowerShell uses the same commands after `.\devkit\setup.ps1 mcp`. The local selection
file is ignored by Git. Context7, Anytype, and Affine use placeholders from
`secrets.local.env`; copy and edit the example first when needed. Do not commit
that file. Chrome DevTools requires an independently running local endpoint.
The Illustrator MCP is intentionally not managed: the observed executable is
inside a personal project and is machine-local.

## Serena

Installation preserves an existing Serena configuration, backs it up, and
adopts only `web_dashboard: true` and `web_dashboard_open_on_launch: false`.
The tracked config is portable across the supported platforms.

## Gstack

On macOS, `./devkit.sh gstack install`, `update`, and `status` use a pinned
commit in `config/external-tools/gstack.conf`, verify the expected Git remote,
and refuse updates when tracked local changes exist. The installation lives at
`~/.gstack/repos/gstack`; it does not enable hooks or automatic updates.

Gstack does **not** have an upstream native PowerShell installer today. The
Windows doctor reports it as skipped rather than pretending it works. Upstream
requires Git Bash/MSYS (or WSL) for its setup script, which is deliberately
outside DevKit's native PowerShell path.

## Other commands

```text
doctor      read-only health report
bootstrap   install profile packages, compose config, and adopt Serena safely
install     install config only (supports --dry-run)
auth        interactive GitHub CLI login
backup      capture only safe, local project trust
snapshot    safe CLI and package inventory
restore     create a local secrets file if needed, then bootstrap
export      safe archive (`.tar.gz` on macOS, `.zip` on Windows)
guard       scan tracked workspace content for obvious secrets
test        non-destructive script and composition validation
```

For Gstack on macOS:

```sh
./devkit.sh gstack status
./devkit.sh gstack install
./devkit.sh gstack update
```

macOS snapshots record Homebrew, Node package managers, GitHub extensions, a
whitelisted Git config subset, and CLI versions. Windows snapshots record OS
metadata, CLI versions, and winget inventory. Neither includes credentials,
auth state, SSH keys, browser data, sessions, or caches.

## What is intentionally not portable

- Codex auth/session/log/cache data and desktop marketplace cache metadata.
- Trusted project paths, host overrides, application-install paths, and local
  app binaries.
- API keys, OAuth tokens, password values, private environment files, and SSH
  material.
- macOS defaults and macOS-only Codex integrations.
- Native Windows Gstack setup, until upstream implements it.

## Validation

`./devkit.sh test` checks shell syntax, secret guard, MCP definitions,
deterministic composition, bootstrap dry runs, and safe snapshot generation.
GitHub Actions runs that check on macOS and parses/composes/tests `devkit/setup.ps1`
on `windows-latest`.

## Troubleshooting

- `MISSING winget`: install or update Microsoft App Installer, reopen
  PowerShell, and rerun `.\devkit\setup.ps1 doctor`.
- `MISSING uvx` or `npx`: rerun the relevant `base` or `web` profile after
  opening a new terminal so the freshly installed executable is on `PATH`.
- An unresolved placeholder in Codex config means its value was omitted from
  `secrets.local.env`; add it there and rerun `install`.
- `chrome-devtools` and `ideon` warnings mean their local HTTP service is not
  running. Disable either integration with `mcp disable <name>` if unused.
- If Serena still opens a browser tab, rerun `install` and restart Codex.
- `symlink creation unavailable`: enable **Developer Mode** in Windows Settings
  (`System > For developers`; on Windows 11 25H2+: `System > Advanced > For
  developers`), then open PowerShell with **Run as administrator** and rerun
  `./devkit/setup.ps1 doctor`. The final line should report `OK symlink
  capability`. See [Windows DevKit notes](../docs/devkit-windows.md) for
  Corepack, Codex CLI, Python-version, and manifest troubleshooting.
