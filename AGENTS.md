# Agents DevKits library instructions

This repository is the source of truth for the Agents DevKits skill library.

When a user asks in natural language to create, add, change, retire, remove, or
turn a prompt or workflow into a reusable Agent Skill for Codex, Claude Code,
or this library, load `skills/skill-authoring/SKILL.md` before making library
edits. This includes requests such as “создай скилл”, “добавь skill”, and
“сделай из этого workflow skill”; an explicit `$skill-authoring` mention is not
required.

Do not apply that rule to a product capability merely described as a “skill” or
“ability” inside a consuming application. In that case, use the skill that owns
the product work instead.

When a user asks in natural language to incorporate or reconcile an audit,
specification, implementation plan, architecture review, or substantial change
request into an already active Progressive Context Kit project's canonical
state, load `skills/progressive-context-change-adoption/SKILL.md` before
changing PCK Brief, Architecture, Roadmap, Phase, ADR, or NEXT_SESSION state.
An explicit `$progressive-context-change-adoption` mention is not required.
Do not use this route for initial PCK adoption, discovery-only audits,
architecture decisions, or implementation.

When a user asks in natural language to incorporate or reconcile an audit,
specification, implementation plan, architecture review, or substantial change
request into a non-PCK project's declared durable planning state without
implementation, load `skills/project-state-change-adoption/SKILL.md`. An
explicit `$project-state-change-adoption` mention is not required. Do not
invent a planning system where the project has not declared canonical owners.

## Agent handoffs

When delegating or transferring work to another agent, provide a self-contained
handoff. Do not assume the receiving agent can see the current conversation,
documents, or working-tree changes.

Before handing work off:

- verify the working directory, branch, and availability of every required file;
- name mandatory documents using verified paths;
- summarize relevant changes already made or still outstanding;
- state the current objective, constraints, acceptance criteria, and any prior
  directions that no longer apply;
- give enough context for the receiver to continue without access to this
  conversation.

If context availability has not been verified, state that limitation explicitly.
Do not present the handoff as ready to execute until the required context is
available.
