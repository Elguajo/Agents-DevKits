---
name: readme-architect
description: Inspect an existing repository and its project context, then design, create, structurally rewrite, audit, or synchronize the root README that best fits that specific project. Use for substantial README work where project purpose, audience, workflows, commands, documentation topology, and repository structure must be understood first. Do not use for typos, one-line link fixes, AGENTS.md, CONTRIBUTING.md, API/reference docs, or general documentation work.
---

# README Architect

## Owns

Adaptive root-README architecture, authoring, auditing, and synchronization grounded in the current repository and project evidence.

This skill does **not** choose a universal README template. It determines what the README must do for the specific project, selects only the sections that earn their place, writes the artifact, and verifies factual claims against the project.

The core transformation is:

```text
repository + project context
        ↓
evidence-backed project model
        ↓
README job and audience
        ↓
conditional section architecture
        ↓
README content
        ↓
verification
```

## Use when

- A repository needs a new root `README.md`.
- An existing README needs a substantial rewrite or structural improvement.
- The user asks to audit whether a README is useful, accurate, navigable, or appropriate for the project.
- The README must be synchronized with the current repository after meaningful project changes.
- A generic or AI-generated-looking README should be replaced with a project-specific one.
- A monorepo, CLI, library, application, plugin, framework, service, knowledge repository, template, research project, or other repository needs a README suited to its actual role.

## Do not use when

- The requested change is a typo, spelling correction, one-line wording fix, badge replacement, or isolated link repair.
- The target is `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, an API reference, a docs site, release notes, or general project documentation.
- The user only wants the repository explained and does not want a README artifact; use `codebase-explorer`.
- The task is a broad project-health audit; use `project-audit`.
- The task is to record durable recurring project facts for agents; use `project-knowledge`.
- The project behavior or implementation must change so that a desired README claim becomes true. README work documents reality; it does not change product reality.

## Modes

Infer the narrowest mode from the request. Do not ask the user to choose a mode when the intent is already clear.

### CREATE
No adequate root README exists. Inspect the project and create one.

### REBUILD
A README exists, but its information architecture or content is substantially wrong, generic, stale, or mismatched to the project. Preserve verified project-specific material and intentional identity while rebuilding the structure.

### SYNC
The README is broadly sound but no longer matches the repository. Update only what current evidence justifies.

### AUDIT
Evaluate the README and report findings without editing it unless the user explicitly asks for changes.

A small local edit is not a mode of this skill; it is ordinary documentation work.

## Core principles

1. **Project-fit over template-fit.** Repository characteristics determine the README; archetypes are hints, never templates.
2. **Human-first, AI-readable.** Optimize for a person arriving at the repository while using explicit structure, terminology, commands, and links that are also easy for agents to parse.
3. **Evidence before prose.** Never invent commands, package names, versions, screenshots, badges, compatibility claims, benchmarks, roadmaps, support channels, or architecture.
4. **Progressive disclosure.** Help the reader understand the project before asking them to absorb internals.
5. **README as map, not encyclopedia.** Route deeper material to its canonical owner instead of duplicating entire docs.
6. **Fast path to success.** When the project is runnable or installable, minimize the distance between understanding it and achieving a first valid result.
7. **Conditional sections only.** A section exists because the project needs it, not because a template lists it.
8. **Preservation on update.** Do not erase correct, intentionally authored identity, visuals, language, acknowledgements, or project-specific explanations merely to normalize style.

## Workflow

### 1. Establish scope and precedence

Read the task and project instructions first.

Apply this precedence:

1. explicit user request;
2. repository/project instructions such as `AGENTS.md`, `CLAUDE.md`, or declared project policy;
3. authoritative project artifacts and executable configuration;
4. existing project conventions;
5. this skill's generic guidance.

For REBUILD or SYNC, identify what must be preserved before editing:
- verified meaning and project identity;
- intentional branding and visual assets;
- language/localization structure;
- accurate links and acknowledgements;
- user-authored sections that remain useful.

Do not expand the task into other documentation or product changes.

### 2. Inspect the project breadth-first, then target only what matters

Do not read the entire repository mechanically. Build an initial map, then inspect the sources that can answer README-relevant questions.

Prioritize, when present:

- repository/project instructions;
- existing `README*` files and package/module READMEs;
- package/build manifests such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, workspace manifests, lockfiles, and equivalent metadata;
- executable entry points, CLI command definitions, application startup paths, plugin manifests, and public package exports;
- build, run, test, lint, development, bootstrap, and release scripts;
- examples, demos, fixtures, sample configuration, and starter projects;
- `docs/`, architecture documents, contribution guides, security policy, changelog, release configuration, and license;
- CI workflows and deployment/package publication configuration;
- screenshots, diagrams, logos, recordings, or other project-owned media;
- monorepo package boundaries and the relationship between the root repository and child packages.

Use `codebase-explorer` when the repository is too large or ambiguous to establish the relevant structure efficiently. Do not duplicate a full codebase audit inside this skill.

### 3. Build an internal evidence map

Before designing the README, establish the following facts where applicable:

- **Identity:** what the project actually is.
- **Repository role:** whole product, package, SDK, plugin, monorepo root, template, examples repo, research artifact, knowledge collection, or another role.
- **Primary audience:** end users, developers integrating the project, contributors, operators, researchers, designers, or a mix.
- **Primary job:** the main thing a visitor should be able to understand or do.
- **Value / reason to exist:** what problem it solves or what capability it provides.
- **Distribution:** package registry, binary, container, plugin marketplace, source checkout, hosted product, library import, or none.
- **Prerequisites:** only real requirements.
- **Install / setup / run / test / build:** exact project-supported commands.
- **First-success path:** the smallest legitimate result a new user can achieve.
- **Core workflows:** the few tasks that best explain actual use.
- **Configuration:** only settings needed for successful adoption or common operation.
- **Documentation topology:** what belongs in README versus canonical external/local docs.
- **Architecture / repository structure:** only what helps the intended README audience.
- **Project status and compatibility:** only when verified and useful.
- **Contribution / support / security / license:** where those responsibilities actually live.
- **Proof claims:** benchmarks, performance, adoption, compatibility, screenshots, demos, or badges must have evidence.

Classify candidate claims internally as:
- `VERIFIED` — directly supported by current project evidence;
- `INFERRED` — plausible but not authoritative;
- `UNKNOWN` — insufficient evidence.

Write factual README claims from `VERIFIED` evidence. Do not silently promote `INFERRED` or `UNKNOWN` claims into facts.

### 4. Characterize the project without forcing an archetype

Identify characteristics that affect README design, for example:

- end-user product vs developer tool;
- library/SDK vs CLI vs app/service vs plugin/extension;
- framework/platform vs single-purpose package;
- monorepo vs standalone repository;
- visual product vs non-visual infrastructure;
- executable vs reference/knowledge repository;
- public open source vs internal project;
- external documentation available vs README as primary documentation;
- simple onboarding vs configuration-heavy setup;
- stable/mature project vs prototype/research artifact.

Archetypes may suggest patterns, but never select a fixed template solely because a project resembles a CLI, library, app, plugin, or monorepo.

### 5. Define the README's job

Determine:

- primary reader;
- secondary reader, if materially different;
- primary action the reader should take;
- what must be understood before that action;
- what should be delegated to deeper docs.

Use this internal success ladder where applicable:

```text
~10 seconds  → understand what the project is
~30 seconds  → understand why it may matter and whether it fits
~2 minutes   → reach a first valid success path
~5 minutes   → know where to go for deeper use, development, or contribution
```

Do not force these timings onto projects where "first success" is not an execution task, such as catalogs, research artifacts, or knowledge repositories. Preserve the intent: rapid orientation followed by purposeful navigation.

### 6. Design the section architecture

Select modules conditionally. Typical candidates include:

- project identity / one-line explanation;
- status or useful badges;
- screenshot, demo, diagram, or hero media;
- why / problem / positioning;
- highlights or major capabilities;
- installation or setup;
- quick start;
- usage examples or common workflows;
- configuration;
- compatibility / supported environments;
- documentation navigation;
- architecture overview;
- semantic repository map;
- development workflow;
- testing;
- deployment / operations;
- contributing;
- security;
- roadmap/status;
- support;
- acknowledgements;
- license;
- FAQ.

These are **components, not a required order**.

Apply these rules:

- Identity belongs near the top.
- Installation belongs early only when installation is a primary adoption step.
- Quick start should lead to a real result, not repeat installation.
- Features belong only when a scannable capability summary improves comprehension.
- Architecture belongs only when the README audience benefits from it and a dedicated architecture doc is not a better owner.
- A repository tree must be semantic, not an `ls` dump.
- A roadmap belongs only when a canonical, maintained roadmap exists and surfacing it in README is useful.
- FAQ belongs only when recurring questions are evidenced.
- A manual table of contents is useful mainly for long/reference-style READMEs; GitHub already exposes a heading outline.
- In a monorepo, the root README should explain the system and route readers to package-level sources instead of duplicating every package README.

### 7. Write for comprehension, not decoration

Use the project's language and established tone unless the user requests a change.

Prefer:
- a precise project name and one-sentence explanation;
- short, information-dense paragraphs;
- task-oriented headings;
- exact commands in fenced code blocks;
- minimal examples that demonstrate the real happy path;
- concise tables only when comparison or structured lookup benefits from them;
- links to canonical deeper documentation;
- clear terminology used consistently throughout.

Avoid:
- generic marketing filler;
- repetitive "Features / Technologies Used / Future Improvements" boilerplate;
- emoji-heavy headings unless the project already uses that style intentionally;
- badge walls;
- giant raw directory trees;
- duplicated API/config/reference documentation;
- invented social/support links;
- unverifiable "fast", "production-ready", "enterprise-grade", "best", or similar claims;
- internal chain-of-thought, agent prompts, secrets, or operational instructions that belong in `AGENTS.md`/`CLAUDE.md`.

### 8. Use visuals only when they improve understanding

A visual is justified when it helps the target reader understand the product, workflow, output, or architecture faster than prose.

Rules:
- use only project-owned or otherwise authorized existing assets unless the user explicitly asks to create new visuals;
- do not invent screenshots, logos, diagrams, demo URLs, or image paths;
- visual products may benefit from a screenshot/demo near the top;
- architecture-heavy systems may benefit more from a diagram than a screenshot;
- non-visual libraries and utilities often need no hero image;
- preserve intentionally authored visuals during updates unless they are broken, stale, or explicitly in scope.

### 9. Treat badges as status signals, not decoration

Include a badge only when:
- its target is real and verifiable;
- the information materially helps a visitor;
- it is likely to remain maintained.

Typical useful signals can include build/status, package/version, documentation, or license. Do not add a large generic badge set merely because popular repositories use badges.

### 10. Separate README from companion sources

Use the README to orient and route.

Do not copy entire contents from:
- `AGENTS.md` / `CLAUDE.md`;
- `CONTRIBUTING.md`;
- `SECURITY.md`;
- full API references;
- architecture decision records;
- long configuration references;
- full release history.

These sources may inform the README. Their detailed instructions remain with their canonical owners.

### 11. Verify before finalizing

Perform proportionate verification.

At minimum:
- confirm referenced local files and asset paths exist;
- confirm install/package identifiers from authoritative project metadata;
- confirm commands exist in manifests/scripts or documented project tooling;
- confirm entry points and example imports match the current project;
- confirm license wording against the actual license file;
- confirm support, compatibility, and status claims have evidence;
- confirm relative Markdown links target real paths;
- confirm the README does not contradict higher-precedence project instructions;
- confirm there are no unresolved template placeholders such as `TODO`, `<project-name>`, fake URLs, or example badges accidentally presented as real;
- check that information intentionally delegated to docs is linked rather than redundantly copied.

When shell execution is available and safe:
- prefer cheap, non-destructive verification;
- execute commands only when doing so materially increases confidence;
- do not install dependencies, mutate external systems, publish artifacts, deploy, or run destructive operations merely to validate README prose;
- report commands as source-verified rather than execution-verified when they were not actually run.

For multilingual README sets:
- determine the project's source-language convention;
- preserve translation links and structure;
- update multiple language variants only when requested or when project instructions require synchronized copies;
- otherwise report possible translation drift instead of silently rewriting unrelated translations.

### 12. Final quality pass

Check the finished README against these questions:

- Can a new reader state what the project is after the opening section?
- Is the primary audience obvious from the content and actions?
- Is the most important next action easy to find?
- Can a new adopter reach the first legitimate result without unnecessary detours?
- Are commands, names, paths, links, and factual claims grounded in the repository?
- Does the README expose only the architecture detail the reader needs?
- Does it route deeper material to the correct source of truth?
- Is every section justified by the project?
- Could any paragraph be removed without losing useful information?
- Does it look intentionally authored for this project rather than generated from a standard template?

## Section-selection heuristics

Use these as decision rules, not as a fixed template.

| Module | Include when | Omit or link out when |
|---|---|---|
| Identity / summary | Always | Never omit project identity |
| Visual/demo | It materially clarifies a visual product or output | No useful verified asset exists |
| Why / problem | Value is not obvious from the identity | The project is self-explanatory and the section would repeat the intro |
| Highlights | Several major capabilities need scanning | It becomes a dump of every feature |
| Installation | Users must install something | Hosted/reference-only project |
| Quick start | A first valid result can be demonstrated compactly | Setup cannot be represented safely/accurately in a short path |
| Usage/examples | Examples explain real workflows | Full examples already have a better canonical home |
| Configuration | Common setup depends on it | Large reference belongs in docs |
| Compatibility | Versions/platforms materially affect adoption | No verified constraint |
| Architecture | Contributors/operators need a compact mental model | Dedicated architecture docs are the better owner |
| Repository map | Directory roles are non-obvious and useful | It would only repeat folder names |
| Development/testing | Contributors are an intended audience | End-user-only README with dedicated contributor docs |
| Deployment/operations | Operators are an intended audience and no better owner exists | Full runbook/deploy docs exist |
| Contributing/security | Public collaboration/security routes matter | Dedicated files can simply be linked |
| Roadmap | A canonical maintained roadmap is useful to readers | Aspirational or stale plan |
| FAQ | Recurring questions are evidenced | Generic guessed questions |
| License | License is known | Never invent a license |

## Failure modes / anti-rationalization

Do not justify a weak README with any of these shortcuts:

- **"This is the standard README structure."** There is no universal section order; derive the structure from the project.
- **"The command is obvious from the framework."** Verify it from the repository.
- **"Top repositories use many badges."** Popularity does not make decorative badges useful.
- **"Longer looks more professional."** Length must be earned by reader needs.
- **"The repo has this folder, so it belongs in the tree."** Show structure only when the role of that structure helps the reader.
- **"There is no documentation, so I will fill the gaps with likely defaults."** Missing evidence stays missing; do not fabricate.
- **"The old README is poor, so everything should be replaced."** Preserve correct project-specific content and identity unless the request changes it.
- **"A benchmark sounds persuasive."** Never claim performance without actual evidence.
- **"AI agents need instructions in README."** Keep README human-first and machine-readable; operational agent rules belong in their own files.
- **"I should fix the product so the README can say this."** Documentation must describe the project, not silently change it.

## Handoffs

- Repository structure or behavior cannot be understood efficiently → `codebase-explorer`.
- Recurring project facts are conflicting, dispersed, or need a durable internal reference → `project-knowledge`.
- The request is a broad technical health review rather than README-specific work → `project-audit`.
- The task expands from README into product behavior or architecture changes → hand off to the owner of that change; do not implement it under this skill.
- The target is another documentation artifact → leave this skill and use direct documentation work or the artifact's owning skill.

## Output contract

For `CREATE`, `REBUILD`, or `SYNC`:

1. produce or update the requested README;
2. preserve accurate out-of-scope content and project conventions;
3. base factual claims on verified project evidence;
4. report the important verification performed;
5. name unresolved facts that materially limited the README;
6. do not claim commands were executed when they were only source-verified.

For `AUDIT`:

1. do not edit the README unless explicitly asked;
2. identify high-value problems with evidence;
3. distinguish factual inaccuracies from information-architecture or presentation improvements;
4. propose the project-fit section architecture;
5. identify stale, unverifiable, duplicated, or missing material;
6. state what would need verification before a rewrite.
