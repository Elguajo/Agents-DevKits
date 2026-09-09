# MCP checks

`mcp/definitions/*.toml` are portable MCP source layers. `devkit.sh install`
and `devkit\setup.ps1 install` compose the enabled definitions into Codex config.
`mcp/profiles/default.txt` is the fresh-machine selection; a local selection in
`machines/<hostname>/enabled-mcps.txt` overrides it without being tracked.

## Run

```sh
./devkit.sh mcp list
./devkit.sh mcp enable affine
./devkit.sh mcp disable affine
./devkit.sh mcp doctor
```

## Known MCP servers

| MCP server | Runtime | Notes |
| --- | --- | --- |
| `sequential-thinking` | `npx` | Uses `@modelcontextprotocol/server-sequential-thinking`. |
| `duckduckgo-search` | `npx` | Uses `duckduckgo-mcp-server`. |
| `context7` | `npx` | Requires `CONTEXT7_API_KEY` at install time or keeps a placeholder. |
| `chrome_devtools` | HTTP | Expects an external endpoint at `http://localhost:3000/mcp`. |
| `playwright` | `npx` | Uses `@playwright/mcp@latest`. |
| `anytype` | `npx` | Optional `ANYTYPE_HEADERS` placeholder. |
| `affine` | `affine-mcp` | Optional local executable and Affine environment placeholders. |
| `open-pencil` | `openpencil-mcp` | Requires the OpenPencil CLI. |
| `ideon` | HTTP | Requires its local endpoint and `IDEON_MCP_TOKEN` environment variable. |
| `serena` | `uvx` | Uses Serena from GitHub and keeps dashboard auto-open disabled. |
| `memory` | `npx` | Uses `@modelcontextprotocol/server-memory`. |
| `shadcn` | `npx` | Uses `shadcn@latest mcp`. |
| `pencil` / `node_repl` | macOS app binaries | Machine-local; preserved during macOS migration, not ported. |

## Security stance

- Auth tokens are not stored in this repo.
- `context7` uses a placeholder in tracked config and gets its real key from `secrets.local.env` or the shell.
- Local app paths are checked but not installed automatically.
