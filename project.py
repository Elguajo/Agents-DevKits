#!/usr/bin/env python3
"""Cross-platform project runtime for Agents DevKits."""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from project_manifest import ManifestError  # noqa: E402
from platform import (  # noqa: E402
    REQUIREMENT_KEYS,
    load_capability_registry,
    resolve_route,
    validate_project_manifest,
    validate_skill_registry,
    version_is_compatible,
)


def paths() -> tuple[dict, dict]:
    capabilities = load_capability_registry(ROOT / "capabilities/registry.yaml")
    registry = validate_skill_registry(
        ROOT / "skills/registry.yaml", ROOT, ROOT / "capabilities/registry.yaml"
    )
    return registry, capabilities


def project_path(raw_path: str) -> Path:
    value = Path(raw_path).resolve()
    if not value.is_dir():
        raise ManifestError("Project path does not exist. Create it first or pass an existing --path.")
    return value


def adapter_for(agent: str) -> tuple[Path, str]:
    if agent == "codex":
        return ROOT / "adapters/codex/AGENTS.template.md", "AGENTS.md"
    return ROOT / "adapters/claude/CLAUDE.template.md", "CLAUDE.md"


def write_snippet(target: Path, agent: str, instruction_name: str) -> None:
    snippet_dir = target / ".agents-devkits"
    snippet_dir.mkdir(exist_ok=True)
    content = (ROOT / "templates/project/INTEGRATION.md.template").read_text(encoding="utf-8")
    content = content.replace("{{INSTRUCTION_FILE}}", instruction_name)
    content = content.replace("{{MANIFEST_PATH}}", "agents-devkits.yaml")
    (snippet_dir / f"{agent}-integration.md").write_text(content, encoding="utf-8")


def install_instruction(target: Path, agent: str, adopt: bool) -> None:
    template, name = adapter_for(agent)
    instruction = target / name
    marker_start = f"<!-- agents-devkits:{agent}:start -->"
    marker_end = f"<!-- agents-devkits:{agent}:end -->"
    if not instruction.exists():
        shutil.copyfile(template, instruction)
        print(f"Created: {instruction}")
        return
    if not adopt:
        write_snippet(target, agent, name)
        print(f"Left existing {instruction} unchanged; wrote integration snippet.")
        return
    content = instruction.read_text(encoding="utf-8")
    if marker_start in content:
        print(f"Already adopted: {instruction}")
        return
    backup_dir = target / ".agents-devkits/backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = backup_dir / f"{name}.{stamp}.backup"
    shutil.copyfile(instruction, backup)
    managed = "\n".join(template.read_text(encoding="utf-8").splitlines()[1:])
    instruction.write_text(f"{content.rstrip()}\n\n{marker_start}\n{managed}\n{marker_end}\n", encoding="utf-8")
    print(f"Backed up: {instruction} -> {backup}")
    print(f"Adopted: {instruction}")


def command_init(args: argparse.Namespace) -> int:
    target = project_path(args.path)
    agents = ("codex", "claude") if args.agent == "both" else (args.agent,)
    for agent in agents:
        install_instruction(target, agent, args.adopt)
    manifest = target / "agents-devkits.yaml"
    if not manifest.exists():
        content = (ROOT / "templates/project/agents-devkits.yaml").read_text(encoding="utf-8")
        if args.agent != "both":
            content = content.replace("agents:\n  - codex\n  - claude", f"agents:\n  - {args.agent}")
        manifest.write_text(content, encoding="utf-8")
        print(f"Created: {manifest}")
    else:
        print(f"Kept existing manifest: {manifest}")
    return 0


def declared_available(args: argparse.Namespace, target: Path) -> set[str]:
    available = {"repository"}
    if shutil.which("sh"):
        available.add("shell")
    available.update(args.capability)
    available.update(filter(None, (item.strip() for item in __import__("os").environ.get("AGENTS_DEVKITS_CAPABILITIES", "").split(","))))
    return available


def check_command(command: dict) -> bool:
    return shutil.which(command["command"]) is not None


def all_declared_checks(manifest: dict) -> list[dict]:
    checks = list(manifest["verification"]["baseline"])
    for condition in manifest["verification"]["conditions"]:
        checks.extend(condition.get("run", []))
    return checks


def command_doctor(args: argparse.Namespace) -> int:
    target = project_path(args.path)
    registry, capabilities = paths()
    manifest = validate_project_manifest(target / "agents-devkits.yaml", registry, capabilities)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    failures = 0
    if version_is_compatible(version, manifest["platform"]["version"]):
        print(f"ok   platform version: {version}")
    else:
        print(f"miss platform version: {version} does not satisfy {manifest['platform']['version']}", file=sys.stderr)
        failures += 1
    available = declared_available(args, target)
    for level in REQUIREMENT_KEYS:
        for capability in manifest["capabilities"][level]:
            if capability in available:
                print(f"ok   {level} capability: {capability}")
            elif level == "required":
                print(f"miss required capability: {capability}", file=sys.stderr)
                failures += 1
            else:
                print(f"warn {level} capability unavailable: {capability}")
    for agent in manifest["agents"]:
        _, name = adapter_for(agent)
        instruction = target / name
        if instruction.is_file():
            print(f"ok   {agent} instructions: {instruction}")
        else:
            print(f"miss {agent} instructions: {instruction}", file=sys.stderr)
            failures += 1
        skill_root = Path.home() / (".codex/skills" if agent == "codex" else ".claude/skills")
        for skill in manifest["skills"]["include"]:
            if (skill_root / skill / "SKILL.md").is_file():
                print(f"ok   {agent} skill: {skill}")
            else:
                print(f"miss {agent} skill: {skill_root / skill}", file=sys.stderr)
                failures += 1
    for check in all_declared_checks(manifest):
        if check_command(check):
            print(f"ok   verification command: {check['command']}")
        else:
            print(f"miss verification command: {check['command']}", file=sys.stderr)
            failures += 1
    if failures:
        return 1
    print("Doctor passed.")
    return 0


def task_facts(task: str, changed: list[str], risks: list[str]) -> set[str]:
    text = task.lower()
    facts = {f"risk.{risk}" for risk in risks}
    if any(word in text for word in ("readme", "documentation", "typo")):
        facts.add("task.documentation")
    if any(word in text for word in ("oauth", "auth", "permission", "secret", "payment")):
        facts.add("task.security_sensitive")
    if "oauth" in text or "auth" in text:
        facts.add("surface.auth")
    if "figma" in text:
        facts.add("task.design_reference")
    if any(word in text for word in ("bug", "broken", "regression")):
        facts.add("task.bug")
    if any(word in text for word in ("test", "coverage")):
        facts.add("task.testing")
    if any(path.startswith(("src/ui/", "app/ui/", "components/")) for path in changed):
        facts.add("task.ui")
    return facts


def condition_matches(condition: dict, changed: list[str], risks: set[str], available: set[str]) -> bool:
    when = condition["when"]
    if "paths" in when and not any(fnmatch.fnmatch(path, pattern) for path in changed for pattern in when["paths"]):
        return False
    if "risks" in when and not set(when["risks"]) <= risks:
        return False
    return "capabilities" not in when or set(when["capabilities"]) <= available


def evidence_item(check: dict, status: str, source: str, reason: str | None = None) -> dict:
    item = {"id": check["id"], "kind": check.get("kind", "test"), "status": status, "source": source, "command": [check["command"], *check.get("args", [])]}
    if reason:
        item["reason"] = reason
    return item


def command_verify(args: argparse.Namespace) -> int:
    target = project_path(args.path)
    registry, capabilities = paths()
    manifest = validate_project_manifest(target / "agents-devkits.yaml", registry, capabilities)
    available = declared_available(args, target)
    facts = task_facts(args.task, args.changed, args.risk)
    risks = set(args.risk)
    if "task.security_sensitive" in facts:
        risks.add("security")
    if "task.ui" in facts:
        risks.add("ui")
    selected = list(manifest["verification"]["baseline"])
    reviews: set[str] = set()
    for condition in manifest["verification"]["conditions"]:
        if condition_matches(condition, args.changed, risks, available):
            selected.extend(condition.get("run", []))
            reviews.update(condition.get("require_reviews", []))
    evidence = []
    for check in selected:
        if not check_command(check):
            evidence.append(evidence_item(check, "unavailable", "environment", "command is not on PATH"))
            continue
        result = subprocess.run([check["command"], *check.get("args", [])], cwd=target, check=False)
        evidence.append(evidence_item(check, "passed" if result.returncode == 0 else "failed", "executed"))
    envelope = {"evidence": evidence, "required_reviews": sorted(reviews)}
    if args.json:
        print(json.dumps(envelope, sort_keys=True))
    else:
        for item in evidence:
            print(f"{item['status']}: {item['id']}")
        if reviews:
            print("Required specialist reviews:", ", ".join(sorted(reviews)))
        if not evidence:
            print("No verification commands selected.")
    return 1 if any(item["status"] in {"failed", "unavailable"} for item in evidence) else 0


def command_route(args: argparse.Namespace) -> int:
    registry, _ = paths()
    facts = task_facts(args.task, args.changed, args.risk)
    facts.update(args.fact)
    print(json.dumps({"facts": sorted(facts), **resolve_route(registry, facts)}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "doctor", "verify"):
        command = commands.add_parser(name)
        command.add_argument("--path", default=".")
        command.add_argument("--capability", action="append", default=[])
        command.add_argument("--with-capability", dest="capability", action="append")
    init = commands.choices["init"]
    init.add_argument("--agent", choices=("codex", "claude", "both"), default="both")
    init.add_argument("--adopt", action="store_true")
    verify = commands.choices["verify"]
    verify.add_argument("--changed", action="append", default=[])
    verify.add_argument("--risk", action="append", default=[])
    verify.add_argument("--task", default="")
    verify.add_argument("--json", action="store_true")
    route = commands.add_parser("route")
    route.add_argument("--task", default="")
    route.add_argument("--changed", action="append", default=[])
    route.add_argument("--risk", action="append", default=[])
    route.add_argument("--fact", action="append", default=[])
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return {"init": command_init, "doctor": command_doctor, "verify": command_verify, "route": command_route}[args.command](args)
    except (ManifestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
