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
