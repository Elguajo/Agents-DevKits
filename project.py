#!/usr/bin/env python3
"""Cross-platform project runtime for Agents DevKits."""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from project_manifest import ManifestError, load_yaml_subset  # noqa: E402
from platform import (  # noqa: E402
    REQUIREMENT_KEYS,
    load_capability_registry,
    resolve_route,
    validate_project_manifest,
    validate_skill_registry,
    version_is_compatible,
)

PCK_AGENT_SENTINEL = "\n\n<!-- PROJECT-SPECIFIC-INSTRUCTIONS -->\n\n"
PCK_VERSION_REQUIREMENT = ">=1.6 <3.0"
INTEGRATION_PROVIDERS = {
    "standard": "agents-devkits",
    "progressive": "progressive-context-kit",
}


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


def detect_project_mode(target: Path) -> str:
    """Identify the PCK project runtime without inspecting its project memory."""

    return "progressive" if (target / ".progressive/VERSION").is_file() else "standard"


def resolve_project_mode(target: Path, requested: str, raw_manifest: dict | None = None) -> str:
    if requested != "auto":
        return requested
    integration = raw_manifest.get("integration") if isinstance(raw_manifest, dict) else None
    if isinstance(integration, dict) and integration.get("mode") in INTEGRATION_PROVIDERS:
        return integration["mode"]
    return detect_project_mode(target)


def validate_progressive_target(target: Path) -> str:
    """Validate the stable PCK Runtime contract needed by the bridge."""

    metadata = target / ".progressive"
    version_file = metadata / "VERSION"
    if not version_file.is_file():
        raise ManifestError("Progressive mode requires the canonical .progressive/VERSION marker.")
    version = version_file.read_text(encoding="utf-8").strip()
    if not version_is_compatible(version, PCK_VERSION_REQUIREMENT):
        raise ManifestError(
            f"PCK Runtime {version} is outside the supported range {PCK_VERSION_REQUIREMENT}."
        )
    profile = (metadata / "PROFILE").read_text(encoding="utf-8").strip() if (metadata / "PROFILE").is_file() else ""
    if profile not in {"standalone", "personal"}:
        raise ManifestError("Progressive mode requires .progressive/PROFILE to be standalone or personal.")
    adoption_state = (
        (metadata / "ADOPTION_STATE").read_text(encoding="utf-8").strip()
        if (metadata / "ADOPTION_STATE").is_file()
        else ""
    )
    if adoption_state != "ready":
        raise ManifestError(
            "PCK adoption must be ready before DevKits integration; finish PCK adoption first."
        )
    if not (target / "AGENTS.md").is_file():
        raise ManifestError("Progressive mode requires the PCK root AGENTS.md entrypoint.")
    return version


def backup_instruction(target: Path, instruction: Path) -> Path:
    backup_dir = target / ".agents-devkits/backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    backup = backup_dir / f"{instruction.name}.{stamp}.backup"
    shutil.copyfile(instruction, backup)
    return backup


def persist_manifest_integration(manifest: Path, mode: str) -> None:
    provider = INTEGRATION_PROVIDERS[mode]
    block = f"integration:\n  mode: {mode}\n  provider: {provider}\n"
    content = manifest.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^integration:\n  mode: (?:standard|progressive)\n"
        r"  provider: (?:agents-devkits|progressive-context-kit)\n",
        re.MULTILINE,
    )
    if pattern.search(content):
        updated = pattern.sub(block, content, count=1)
    elif re.search(r"^integration:\s*$", content, re.MULTILINE):
        raise ManifestError("Existing manifest integration block is not in the supported shape.")
    elif re.search(r"^agents:\s*$", content, re.MULTILINE):
        updated = re.sub(r"^agents:\s*$", f"{block}agents:", content, count=1, flags=re.MULTILINE)
    else:
        raise ManifestError("Existing manifest has no agents block for integration metadata.")
    manifest.write_text(updated, encoding="utf-8")


def write_snippet(target: Path, agent: str, instruction_name: str, template_name: str = "INTEGRATION.md.template") -> None:
    snippet_dir = target / ".agents-devkits"
    snippet_dir.mkdir(exist_ok=True)
    content = (ROOT / "templates/project" / template_name).read_text(encoding="utf-8")
    content = content.replace("{{INSTRUCTION_FILE}}", instruction_name)
    content = content.replace("{{MANIFEST_PATH}}", "agents-devkits.yaml")
    (snippet_dir / f"{agent}-integration.md").write_text(content, encoding="utf-8")


def install_routing_index(target: Path, refresh: bool) -> None:
    """Install the generated routing snapshot without maintaining it by hand."""

    destination = target / ".agents-devkits/ROUTING.md"
    destination.parent.mkdir(exist_ok=True)
    if destination.exists() and not refresh:
        current = ROOT / "docs/ROUTING.md"
        status = "current" if destination.read_bytes() == current.read_bytes() else "stale"
        print(f"Kept existing routing index ({status}): {destination}")
        return
    shutil.copyfile(ROOT / "docs/ROUTING.md", destination)
    print(f"{'Refreshed' if destination.exists() and refresh else 'Created'} routing index: {destination}")


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
    backup = backup_instruction(target, instruction)
    managed = "\n".join(template.read_text(encoding="utf-8").splitlines()[1:])
    instruction.write_text(f"{content.rstrip()}\n\n{marker_start}\n{managed}\n{marker_end}\n", encoding="utf-8")
    print(f"Backed up: {instruction} -> {backup}")
    print(f"Adopted: {instruction}")


def install_progressive_bridge(target: Path, adopt: bool) -> None:
    """Add a narrow, managed reference to DevKits without replacing PCK routing."""

    instruction = target / "AGENTS.md"
    marker_start = "<!-- agents-devkits:progressive:start -->"
    marker_end = "<!-- agents-devkits:progressive:end -->"
    if not adopt:
        write_snippet(target, "progressive", "AGENTS.md", "PROGRESSIVE-BRIDGE.md.template")
        print("Left PCK AGENTS.md unchanged; wrote progressive bridge snippet.")
        return
    content = instruction.read_text(encoding="utf-8")
    if (marker_start in content) != (marker_end in content):
        raise ManifestError("Progressive bridge markers are incomplete; reconcile AGENTS.md manually.")
    marker_pattern = re.compile(
        rf"\n?{re.escape(marker_start)}\n.*?\n{re.escape(marker_end)}\n?",
        re.DOTALL,
    )
    if (
        marker_start in content
        and PCK_AGENT_SENTINEL in content
        and content.find(PCK_AGENT_SENTINEL) < content.find(marker_start)
    ):
        print(f"Already adopted progressive bridge: {instruction}")
        return
    backup = backup_instruction(target, instruction)
    migrated = marker_start in content
    if migrated:
        content = marker_pattern.sub("\n", content, count=1).rstrip()
    if "<!-- PROJECT-SPECIFIC-INSTRUCTIONS -->" in content and PCK_AGENT_SENTINEL not in content:
        raise ManifestError("PCK preservation sentinel has incompatible whitespace in AGENTS.md.")
    if PCK_AGENT_SENTINEL not in content:
        content = f"{content.rstrip()}{PCK_AGENT_SENTINEL}"
    bridge = (ROOT / "templates/project/PROGRESSIVE-BRIDGE.md.template").read_text(encoding="utf-8")
    instruction.write_text(
        f"{content}{marker_start}\n{bridge.rstrip()}\n{marker_end}\n",
        encoding="utf-8",
    )
    print(f"Backed up: {instruction} -> {backup}")
    print(f"{'Migrated' if migrated else 'Adopted'} progressive bridge: {instruction}")


def command_init(args: argparse.Namespace) -> int:
    target = project_path(args.path)
    manifest = target / "agents-devkits.yaml"
    raw_manifest = load_yaml_subset(manifest) if manifest.is_file() else None
    if manifest.is_file():
        registry, capabilities = paths()
        validate_project_manifest(manifest, registry, capabilities)
    mode = resolve_project_mode(target, args.mode, raw_manifest)
    if mode == "progressive":
        pck_version = validate_progressive_target(target)
        print(f"PCK Runtime: {pck_version}")
    print(f"Project mode: {mode}")
    agents = ("codex", "claude") if args.agent == "both" else (args.agent,)
    if mode == "progressive":
        install_progressive_bridge(target, args.adopt)
    else:
        for agent in agents:
            install_instruction(target, agent, args.adopt)
    install_routing_index(target, args.refresh_routing)
    if not manifest.exists():
        template_name = "agents-devkits.ui.yaml" if args.ui else "agents-devkits.yaml"
        content = (ROOT / "templates/project" / template_name).read_text(encoding="utf-8")
        if args.agent != "both":
            content = content.replace("agents:\n  - codex\n  - claude", f"agents:\n  - {args.agent}")
        manifest.write_text(content, encoding="utf-8")
        print(f"Created: {manifest}")
    else:
        print(f"Kept existing manifest: {manifest}")
    persist_manifest_integration(manifest, mode)
    if args.ui:
        design_brief = target / "DESIGN.md"
        if design_brief.exists():
            print(f"Kept existing design brief: {design_brief}")
        else:
            template = ROOT / "templates/project/DESIGN.md.template"
            shutil.copyfile(template, design_brief)
            print(f"Created: {design_brief}")
    return 0


def project_relative_path(target: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts or value == ".":
        raise ManifestError("Knowledge source must be a non-empty path relative to the project root.")
    resolved = (target / candidate).resolve()
    if not resolved.is_relative_to(target):
        raise ManifestError("Knowledge source must remain inside the project root.")
    return resolved


def command_knowledge_init(args: argparse.Namespace) -> int:
    target = project_path(args.path)
    manifest = target / "agents-devkits.yaml"
    if not manifest.is_file():
        raise ManifestError("Initialize the project runtime before creating a knowledge pack.")
    registry, capabilities = paths()
    manifest_data = validate_project_manifest(manifest, registry, capabilities)
    if "legacy_schema_version" in manifest_data:
        raise ManifestError("Upgrade the project manifest before adding a knowledge pack.")
    sources = [project_relative_path(target, source) for source in args.source]
    missing = [str(source.relative_to(target)) for source in sources if not source.exists()]
    if missing:
        raise ManifestError(f"Knowledge source does not exist: {', '.join(missing)}")
    content = manifest.read_text(encoding="utf-8")
    empty_knowledge = "knowledge:\n  packs: []"
    if "\nknowledge:" in f"\n{content}" and empty_knowledge not in content:
        raise ManifestError("Manifest already declares knowledge; add or update packs deliberately.")
    pack_path = target / ".agents-devkits/knowledge/design-system.md"
    if pack_path.exists():
        raise ManifestError(f"Knowledge pack already exists: {pack_path}")
    pack_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "templates/project/knowledge-design-system.md.template", pack_path)
    source_lines = "\n".join(f"        - {source.relative_to(target)}" for source in sources)
    declaration = f"knowledge:\n  packs:\n    - id: design-system\n      kind: design-system\n      path: .agents-devkits/knowledge/design-system.md\n      sources:\n{source_lines}"
    manifest.write_text(
        f"{content.replace(empty_knowledge, declaration).rstrip()}\n"
        if empty_knowledge in content
        else f"{content.rstrip()}\n{declaration}\n",
        encoding="utf-8",
    )
    print(f"Created: {pack_path}")
    print(f"Declared design-system knowledge pack in: {manifest}")
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


def standard_instruction_is_active(target: Path, agent: str) -> bool:
    template, name = adapter_for(agent)
    instruction = target / name
    if not instruction.is_file():
        return False
    content = instruction.read_text(encoding="utf-8")
    marker_start = f"<!-- agents-devkits:{agent}:start -->"
    marker_end = f"<!-- agents-devkits:{agent}:end -->"
    if (marker_start in content) != (marker_end in content):
        return False
    if marker_start in content:
        return True
    return template.read_text(encoding="utf-8").strip() in content


def integration_state(target: Path, manifest: dict) -> tuple[str, list[str]]:
    """Return the strict project integration state and actionable reasons."""

    states: list[str] = []
    details: list[str] = []
    routing = target / ".agents-devkits/ROUTING.md"
    if not routing.is_file():
        states.append("broken")
        details.append("routing snapshot is missing")
    elif routing.read_bytes() != (ROOT / "docs/ROUTING.md").read_bytes():
        states.append("stale")
        details.append("routing snapshot differs from this DevKits version")

    mode = manifest["integration"]["mode"]
    if mode == "progressive":
        try:
            validate_progressive_target(target)
        except ManifestError as error:
            states.append("broken")
            details.append(str(error))
        instruction = target / "AGENTS.md"
        content = instruction.read_text(encoding="utf-8") if instruction.is_file() else ""
        marker_start = "<!-- agents-devkits:progressive:start -->"
        marker_end = "<!-- agents-devkits:progressive:end -->"
        if marker_start not in content and marker_end not in content:
            snippet = target / ".agents-devkits/progressive-integration.md"
            states.append("pending" if snippet.is_file() else "broken")
            details.append("progressive bridge has not been adopted")
        elif (
            marker_start not in content
            or marker_end not in content
            or PCK_AGENT_SENTINEL not in content
            or content.find(PCK_AGENT_SENTINEL) > content.find(marker_start)
        ):
            states.append("broken")
            details.append("progressive bridge is outside the PCK-preserved suffix")
    else:
        for agent in manifest["agents"]:
            if standard_instruction_is_active(target, agent):
                continue
            snippet = target / f".agents-devkits/{agent}-integration.md"
            states.append("pending" if snippet.is_file() else "broken")
            details.append(f"{agent} instructions do not activate DevKits")

    if not states:
        return "active", details
    for state in ("broken", "pending", "stale"):
        if state in states:
            return state, details
    raise AssertionError("Unknown integration state")


def command_doctor(args: argparse.Namespace) -> int:
    target = project_path(args.path)
    registry, capabilities = paths()
    manifest = validate_project_manifest(target / "agents-devkits.yaml", registry, capabilities)
    mode = manifest["integration"]["mode"]
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    failures = 0
    print(f"ok   project mode: {mode}")
    state, state_details = integration_state(target, manifest)
    if state == "active":
        print("ok   integration state: active")
    else:
        print(f"miss integration state: {state}", file=sys.stderr)
        for detail in state_details:
            print(f"     {detail}", file=sys.stderr)
        failures += 1
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
    for pack in manifest.get("knowledge", {}).get("packs", []):
        pack_path = project_relative_path(target, pack["path"])
        if pack_path.is_file():
            print(f"ok   knowledge pack: {pack_path}")
        else:
            print(f"miss knowledge pack: {pack_path}", file=sys.stderr)
            failures += 1
        for source in pack["sources"]:
            source_path = project_relative_path(target, source)
            if source_path.exists():
                print(f"ok   knowledge source: {source_path}")
            else:
                print(f"miss knowledge source: {source_path}", file=sys.stderr)
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
    init.add_argument("--ui", action="store_true", help="add the opt-in UI brief and UI quality profile")
    init.add_argument("--refresh-routing", action="store_true", help="replace the generated project routing snapshot")
    init.add_argument("--mode", choices=("auto", "progressive", "standard"), default="auto", help="auto-detect Progressive Context Kit or select an integration mode")
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
    knowledge = commands.add_parser("knowledge")
    knowledge_actions = knowledge.add_subparsers(dest="knowledge_action", required=True)
    knowledge_init = knowledge_actions.add_parser("init", help="create an opt-in design-system knowledge-pack scaffold")
    knowledge_init.add_argument("--path", default=".")
    knowledge_init.add_argument("--source", action="append", required=True, help="project-relative design-system source path; repeatable")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "knowledge":
            return {"init": command_knowledge_init}[args.knowledge_action](args)
        return {"init": command_init, "doctor": command_doctor, "verify": command_verify, "route": command_route}[args.command](args)
    except (ManifestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
