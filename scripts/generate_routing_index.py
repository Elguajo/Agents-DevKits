#!/usr/bin/env python3
"""Generate the compact, reviewable skill-routing index from the registry."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from platform import routing_tier_for_skill, validate_skill_registry  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/ROUTING.md"


def _escape(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def render() -> str:
    registry = validate_skill_registry(
        ROOT / "skills/registry.yaml", ROOT, ROOT / "capabilities/registry.yaml"
    )
    grouped = {tier: [] for tier in ("auto", "propose", "ask")}
    for entry in registry["skills"]:
        grouped[routing_tier_for_skill(registry, entry)].append(entry)

    lines = [
        "# Skill Routing Index",
        "",
        "<!-- Generated from skills/registry.yaml by scripts/generate_routing_index.py; do not edit manually. -->",
        "",
        "A compact selection aid for Codex and Claude Code. The registry is the machine-readable",
        "source of truth; each selected `SKILL.md` is the execution source of truth.",
        "Project instructions, task-specific source of truth, and an explicit user request take precedence.",
        "",
        "## Selection levels",
        "",
        "- **AUTO** — select only when the task and a skill boundary match; state the selected skills briefly.",
        "- **PROPOSE** — announce the recommended workflow and continue unless the user redirects; this is not an approval gate.",
        "- **ASK** — do not select automatically; require an explicit user request. This tier never overrides separate safety or authorization rules.",
        "",
        "## Index",
        "",
    ]
    for tier in ("auto", "propose", "ask"):
        lines.extend([f"### {tier.upper()}", "", "| Skill | Use when |", "| --- | --- |"])
        for entry in grouped[tier]:
            lines.append(f"| `{entry['name']}` | {_escape(entry['use_when'])} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when docs/ROUTING.md is stale")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
            print(f"Routing index is stale: {OUTPUT}", file=sys.stderr)
            return 1
        print("Routing index is current")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Generated: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
