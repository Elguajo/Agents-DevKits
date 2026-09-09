---
name: notion-markdown-workspace-sync
description: Create and safely synchronize a Notion workspace for editable Markdown documents when a user prefers Notion to local project files. Excludes binary deliverables unless explicitly requested.
metadata:
  short-description: Sync editable Markdown work with Notion
---

# Notion Markdown Workspace Sync

## Use when

The user explicitly wants Notion to be the working editor for an existing project's Markdown documents and requests an on-demand migration, import, export, or reconciliation.

## Do not use when

- The request is to turn a Notion page into an AFFiNE graph, canvas, mind map, or diagram; hand off to `affine-notion-graph-sync`.
- The material is a PDF, PPTX, image, archive, or other binary deliverable; handle it as separately authorized publishing work.
- The user wants a continuously running sync service, webhook, or production integration; hand off its failure and recovery design to `reliability-review`.

## Workflow

1. Establish direction before modifying anything: local Markdown → Notion, Notion → local, or reconciliation. Do not infer a live-sync promise from a one-time import.
2. Read applicable project instructions, inspect the working tree if local files may change, and preserve existing sync-map metadata.
3. Verify the Notion connection and fetch likely workspace destinations before creating pages. If the connection or appropriate destination is unavailable, report that blocker without creating a substitute workspace.
4. Before writing Notion content, read its current enhanced-Markdown specification. Create a parent workspace and one child page per editable document only when the user requested a migration and no suitable mapped page exists.
5. Create or maintain a versioned local sync map containing document title, local path, Notion page URL and ID, editing authority, local SHA-256, and Notion `page_last_edited_at` from the last successful sync.
6. For each mapped document, fetch the Notion page and read the local file. If the page is truncated or includes unsupported blocks, stop that document's sync rather than flattening or losing content.
7. Compare the local hash and Notion edit timestamp with the map:
   - only Notion changed → update local Markdown;
   - only local content changed → update Notion only if the requested direction allows it;
   - both changed → do not overwrite either side; present the conflict and ask which version or merge should win;
   - neither changed → leave it untouched.
8. Update the sync map only after the document is successfully synchronized or verified unchanged.

## Rules

- Preserve headings, lists, tables, links, source references, status labels, and uncertainty markers. Do not reclassify claims while converting formats.
- Keep Notion pages dedicated to their mapped document before replacing whole-page content. Fetch immediately before a Notion write and preserve unrelated child content.
- Never include credentials, temporary signed URLs, or unnecessary workspace identity data in the sync map or report.
- Do not upload or synchronize binary deliverables by default.

## Handoffs

- `affine-notion-graph-sync` for visual graph imports from Notion.
- `reliability-review` for a background, webhook, retry, or recovery design beyond human-invoked sync.
- `data-storage-review` when sync state, retention, or recovery of durable documents becomes the primary concern.

## Output contract

Report the workspace URL, documents considered, sync direction, each successful update or unchanged document, and every skipped or conflicting document. State clearly that the completed work is on-demand, not real-time or scheduled synchronization.
