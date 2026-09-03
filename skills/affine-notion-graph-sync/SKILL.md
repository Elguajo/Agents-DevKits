---
name: affine-notion-graph-sync
description: Turn a Notion page URL into a deterministic Edgeless Canvas in the user's self-hosted AFFiNE workspace using the local affine-notion-graph-sync repository.
metadata:
  short-description: Build an AFFiNE graph from a Notion link
---

# Notion link to AFFiNE graph

Use this skill when the user provides a `notion.so` or `app.notion.com` page link and asks to make a graph, mind map, flow, block diagram, or Edgeless Canvas.

## Source and destination

- Notion is the read-only source for the requested import.
- The destination is the user's self-hosted AFFiNE server, not AFFiNE Cloud.
- Run the repository commands from `/Users/elguajo/Documents/DEV/aposter-affine-business-map` (or locate the checkout by finding `package.json` with name `affine-notion-graph-sync`).
- Generated blueprints and opaque canvas state are local ignored runtime files. Never stage or commit them, and never put Notion tokens in a prompt, command argument, or file tracked by Git.

## Execution

For an explicit request to create the graph, first verify the local prerequisites without exposing credentials:

```sh
affine-mcp status
affine-mcp doctor
```

If `NOTION_API_TOKEN` is not already present in the environment, stop and ask the user to configure it in the ignored root `.env`; never ask them to paste the token into chat. The Notion integration should have only **Read content** access to the requested page tree.

Then run the safe first-import workflow:

```sh
cd /Users/elguajo/Documents/DEV/aposter-affine-business-map
npm run notion:sync -- --url '<user-provided Notion URL>'
```

This recursively reads the page, turns headings into frames, textual blocks into nodes, and Notion/text links into `references` connectors. It writes the generated local blueprint below `blueprints/notion/` and seeds a new canvas with the default title `Notion — <page title>`, unless the user specifies another title.

After seeding, verify the canvas using the exact generated blueprint, document title, and state path printed by the importer. Report only counts, target title, and validation status; do not paste the full imported content into chat.

For a preview request, use `npm run notion:blueprint ... --dry-run` and summarize the generated counts rather than reproducing all notes. For a requested additive change to an existing canvas, use the repository's `update:affine` patch workflow after reviewing exact labels.

## Safety boundaries

- Never use `--reflow`, delete, or replacement operations to resolve a sync conflict.
- If a seeded blueprint changed, the seeder may refuse to mutate the existing canvas. Preserve `state/`, explain the conflict, and propose an explicit additive patch; do not delete state or force a reseed.
- Linked target pages are represented as reference nodes unless the user explicitly requests importing them as additional roots. Do not invent semantic business relationships from prose; use explicit Notion relations or labels.
- Repeat the command when the user asks to refresh. A local webhook endpoint is not configured, and the local machine must not be exposed directly to the public internet.
- For recovery, use `npm run backup:affine:offsite` only after the user has configured an encrypted restic repository and password file outside the repository.

## Response

State what was created or verified, the AFFiNE document title, frame/node/edge counts, and any source links that could not be dereferenced. If credentials, workspace selection, or a public webhook deployment is missing, identify that exact blocker and the next local configuration step.
