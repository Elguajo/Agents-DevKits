# Codex configuration composition

`devkit.sh install` and `devkit\setup.ps1 install` generate `~/.codex/config.toml` in
this order:

1. `config/portable/base.toml`
2. `config/portable/plugins.toml`
3. each enabled portable MCP definition from `mcp/definitions/`
4. `config/platform/macos.toml` or `config/platform/windows.toml`
5. the ignored `machines/<hostname>/codex.toml`, if present

The generated file is backed up before replacement. Before a macOS replacement,
the installer also adopts trusted projects and observed local app integrations
(Node REPL, computer-use, Pencil, Illustrator, and notifier) into the ignored
machine layer. Sources must not define the same TOML table twice; composition
rejects duplicate tables rather than producing an ambiguous Codex configuration.

`mcp enable <name>` and `mcp disable <name>` write the ignored local
`machines/<hostname>/enabled-mcps.txt`. If it is absent, the tracked
`mcp/profiles/default.txt` is used. Create a machine layer only for local
project trust or verified host-only settings; never place tokens, sessions, or
application cache paths in it.

The portable MCP layer includes the current portable integrations (Context7,
Playwright, Serena, Memory, shadcn, Chrome DevTools, Anytype, Affine,
OpenPencil, and Ideon). Anytype and Affine are emitted with environment
placeholders; Ideon refers to its token by environment-variable name.
The Illustrator MCP is deliberately not copied: its executable is inside a
specific local project and is machine-local. Codex plugins are declared in
`config/portable/plugins.toml`; macOS-only Build macOS Apps stays platform-only.
