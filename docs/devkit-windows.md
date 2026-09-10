# Windows DevKit notes

This guide covers the native PowerShell DevKit entry point:

```powershell
.\devkit\setup.ps1 bootstrap --profile base --profile web --profile ai
```

It is separate from the repository skill installer, `./bootstrap.sh`, which
uses Git Bash on Windows and creates links for Codex and Claude skills.

## First-run validation

Run the non-mutating checks before and after bootstrap:

```powershell
.\devkit\setup.ps1 bootstrap --dry-run
.\devkit\setup.ps1 test
.\devkit\setup.ps1 doctor
```

`--dry-run` must print only `DRY-RUN` package commands and must not invoke
`winget` installs, change Git configuration, or replace Codex/Serena config.
The normal bootstrap backs up an existing `~/.codex/config.toml` before
installing the composed configuration.

## Windows-specific conditions

### Symbolic links

If `doctor` reports `WARN symlink creation unavailable`, enable **Developer
Mode** in Windows Settings:

- Windows 11 before 25H2: `System > For developers`.
- Windows 11 25H2 and later: `System > Advanced > For developers`.

Then open PowerShell with **Run as administrator** and rerun:

```powershell
cd D:\path\to\Agents-DevKits
.\devkit\setup.ps1 doctor
```

Success is reported as `OK symlink capability`. A separately elevated terminal
does not elevate an already-running Codex process; restart Codex as
administrator only when its own terminal must create links.

### Corepack permissions

The `web` profile runs `corepack enable`. Node installed under `Program Files`
may reject that operation with `EPERM` when the shell is not elevated. This
does not by itself mean pnpm is unusable; check it first:

```powershell
pnpm --version
```

If pnpm is unavailable and Corepack is required, rerun `corepack enable` from
an elevated PowerShell, then open a new terminal.

### Codex CLI shown as missing

`doctor` can show `MISSING codex` in an ordinary or elevated external
PowerShell even when Codex Desktop and its installed configuration work. That
means only that this shell does not resolve the `codex` executable through
`PATH`; it does not invalidate `~/.codex/config.toml`. Restart the terminal
after a Codex CLI installation before treating the warning as a failed DevKit
installation.

### Python version checks

`doctor` verifies that a `python` command exists, not that it selects the
profile's Python 3.12 installation. When several Python versions are present,
verify the requested interpreter explicitly:

```powershell
py -3.12 --version
```

## Expected warnings

- Unset `CONTEXT7_API_KEY`, `ANYTYPE_HEADERS`, `AFFINE_BASE_URL`,
  `AFFINE_TOOL_PROFILE`, or `IDEON_MCP_TOKEN` leave their optional values
  unresolved. Add only the values needed in `devkit/secrets.local.env`, then
  rerun `install`; never commit that file.
- Native Windows Gstack is intentionally skipped because its upstream
  installer requires Git Bash/MSYS or WSL.

## Maintainer notes

`devkit/profiles/manifest.tsv` is parsed by PowerShell `Import-Csv` with a tab
delimiter. It must contain literal tab characters, not the two-character text
sequence `\t`; validate it with `bootstrap --dry-run` after editing or moving
the file between platforms.

PowerShell reserves the automatic `$args` variable. DevKit command handlers
must use an explicit parameter such as `$CommandArgs`, so options including
`--dry-run`, `--profile`, and `mcp enable` are honored.
