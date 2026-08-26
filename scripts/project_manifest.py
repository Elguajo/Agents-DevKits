#!/usr/bin/env python3
"""Validate and execute the strict YAML subset used by Agents DevKits projects.

The project manifest intentionally accepts structured commands only. Verification
never evaluates shell snippets from YAML: each command is run through
``subprocess.run`` with a command name and an argument array.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ALLOWED_AGENTS = {"codex", "claude"}
DEFAULT_REQUIREMENTS = {"required", "preferred", "optional"}
DEFAULT_CAPABILITIES = {
    "repository",
    "shell",
    "browser",
    "figma",
    "database",
    "issue-tracker",
}
ALLOWED_ORIGIN_TYPES = {"local", "vendored"}


class ManifestError(ValueError):
    """The manifest is missing required data or uses unsupported YAML."""


def _strip_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, character in enumerate(line):
        if quote:
            if character == quote and not escaped:
                quote = None
            escaped = character == "\\" and not escaped
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    return line.rstrip()


def _split_key_value(content: str) -> tuple[str, str | None]:
    quote: str | None = None
    escaped = False
    for index, character in enumerate(content):
        if quote:
            if character == quote and not escaped:
                quote = None
            escaped = character == "\\" and not escaped
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == ":":
            key = content[:index].strip()
            if not key:
                break
            value = content[index + 1 :].strip()
            return key, value or None
    raise ManifestError(f"Expected a mapping entry, got: {content!r}")


def _parse_scalar(value: str) -> Any:
    if value in {"null", "~"}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError as error:
            raise ManifestError(f"Inline lists must use JSON syntax: {value!r}") from error
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        if value.startswith('"'):
            try:
                return json.loads(value)
            except json.JSONDecodeError as error:
                raise ManifestError(f"Invalid quoted string: {value!r}") from error
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    return value


def load_yaml_subset(path: Path) -> Any:
    """Load the small, documented YAML subset used by registry and manifests.

    It supports mappings, lists, quoted strings, JSON-style inline lists, and
    folded/literal blocks. Anchors, aliases, tabs, flow mappings, and multiline
    quoted values are deliberately rejected to keep project configuration
    portable without a third-party YAML dependency.
    """

    tokens: list[tuple[int, str]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "\t" in raw_line:
            raise ManifestError(f"Tabs are not supported ({path}:{line_number})")
        content = _strip_comment(raw_line)
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        tokens.append((indent, content.strip()))

    if not tokens:
        raise ManifestError(f"Manifest is empty: {path}")

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(tokens) or tokens[index][0] != indent:
            raise ManifestError(f"Expected indentation level {indent}")
        is_list = tokens[index][1].startswith("- ") or tokens[index][1] == "-"
        collection: Any = [] if is_list else {}

        while index < len(tokens):
            current_indent, content = tokens[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ManifestError(f"Unexpected indentation before {content!r}")

            if is_list:
                if not (content.startswith("- ") or content == "-"):
                    break
                item = content[1:].strip()
                index += 1
                if not item:
                    if index >= len(tokens) or tokens[index][0] <= indent:
                        raise ManifestError("List item requires a value")
                    value, index = parse_block(index, tokens[index][0])
                    collection.append(value)
                    continue
                if ":" not in item:
                    collection.append(_parse_scalar(item))
                    continue

                key, raw_value = _split_key_value(item)
                value: Any
                if raw_value in {">-", "|"}:
                    value, index = parse_block_scalar(index, indent + 2, raw_value)
                elif raw_value is None:
                    if index < len(tokens) and tokens[index][0] > indent:
                        value, index = parse_block(index, tokens[index][0])
                    else:
                        value = None
                else:
                    value = _parse_scalar(raw_value)
                mapping: dict[str, Any] = {key: value}
                if index < len(tokens) and tokens[index][0] == indent + 2:
                    extra, index = parse_block(index, indent + 2)
                    if not isinstance(extra, dict):
                        raise ManifestError("List mappings may contain mappings only")
                    mapping.update(extra)
                collection.append(mapping)
                continue

            if content.startswith("- ") or content == "-":
                raise ManifestError("Cannot mix list and mapping entries")
            key, raw_value = _split_key_value(content)
            index += 1
            if raw_value in {">-", "|"}:
                value, index = parse_block_scalar(index, indent + 2, raw_value)
            elif raw_value is None:
                if index < len(tokens) and tokens[index][0] > indent:
                    value, index = parse_block(index, tokens[index][0])
                else:
                    value = None
            else:
                value = _parse_scalar(raw_value)
            if key in collection:
                raise ManifestError(f"Duplicate mapping key: {key}")
            collection[key] = value
        return collection, index

    def parse_block_scalar(index: int, indent: int, marker: str) -> tuple[str, int]:
        lines: list[str] = []
        while index < len(tokens) and tokens[index][0] >= indent:
            current_indent, content = tokens[index]
            lines.append(" " * (current_indent - indent) + content)
            index += 1
        if not lines:
            raise ManifestError("Block scalar requires content")
        return (" ".join(lines) if marker == ">-" else "\n".join(lines)), index

    value, final_index = parse_block(0, tokens[0][0])
    if final_index != len(tokens):
        raise ManifestError("Could not parse all YAML entries")
    return value


def _expect_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ManifestError(f"{label} must be a list")
    return value


def _expect_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{label} must be a non-empty string")
    return value


def _expect_string_list(value: Any, label: str) -> list[str]:
    values = _expect_list(value, label)
    if not all(isinstance(item, str) and item for item in values):
        raise ManifestError(f"{label} must contain non-empty strings")
    return values


def _registry_values(registry: dict[str, Any] | None, key: str, fallback: set[str]) -> set[str]:
    if registry is None:
        return fallback
    return set(_expect_string_list(registry.get(key), f"registry.{key}"))


def _validate_command(command: Any, label: str) -> None:
    if not isinstance(command, dict):
        raise ManifestError(f"{label} must be a mapping with command and args")
    executable = _expect_string(command.get("command"), f"{label}.command")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", executable):
        raise ManifestError(
            f"{label}.command must be a simple command name, not a shell expression or path"
        )
    args = _expect_list(command.get("args"), f"{label}.args")
    if not all(isinstance(argument, str) for argument in args):
        raise ManifestError(f"{label}.args must contain strings only")


def _validate_selected_skills(manifest: dict[str, Any], registry: dict[str, Any]) -> None:
    known_skills = {entry["name"] for entry in registry["skills"]}
    unknown = sorted(set(manifest["skills"]) - known_skills)
    if unknown:
        raise ManifestError(f"Manifest selects unknown skills: {unknown}")


def validate_project_manifest(data: Any, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ManifestError("Manifest root must be a mapping")
    if data.get("schema_version") != 1:
        raise ManifestError("schema_version must be 1")

    agents = _expect_list(data.get("agents"), "agents")
    if not agents or not all(agent in ALLOWED_AGENTS for agent in agents):
        raise ManifestError("agents must contain codex and/or claude")
    if len(set(agents)) != len(agents):
        raise ManifestError("agents must not contain duplicates")

    skills = _expect_list(data.get("skills"), "skills")
    if not all(isinstance(skill, str) and skill for skill in skills):
        raise ManifestError("skills must contain non-empty names")
    if len(set(skills)) != len(skills):
        raise ManifestError("skills must not contain duplicates")

    allowed_capabilities = _registry_values(registry, "capability_values", DEFAULT_CAPABILITIES)
    allowed_requirements = _registry_values(
        registry, "capability_requirement_values", DEFAULT_REQUIREMENTS
    )
    capabilities = _expect_list(data.get("capabilities"), "capabilities")
    seen_capabilities: set[str] = set()
    for index, capability in enumerate(capabilities):
        if not isinstance(capability, dict):
            raise ManifestError(f"capabilities[{index}] must be a mapping")
        name = capability.get("name")
        requirement = capability.get("requirement")
        if name not in allowed_capabilities:
            raise ManifestError(f"capabilities[{index}].name is not supported: {name!r}")
        if requirement not in allowed_requirements:
            raise ManifestError(f"capabilities[{index}].requirement is invalid")
        if name in seen_capabilities:
            raise ManifestError(f"capability is duplicated: {name}")
        seen_capabilities.add(name)

    verification = data.get("verification")
    if not isinstance(verification, dict):
        raise ManifestError("verification must be a mapping")
    required = _expect_list(verification.get("required"), "verification.required")
    conditional = _expect_list(verification.get("conditional"), "verification.conditional")
    for index, command in enumerate(required):
        _validate_command(command, f"verification.required[{index}]")
    for index, entry in enumerate(conditional):
        if not isinstance(entry, dict):
            raise ManifestError(f"verification.conditional[{index}] must be a mapping")
        capability = entry.get("capability")
        if capability not in seen_capabilities:
            raise ManifestError(
                f"verification.conditional[{index}].capability must be declared in capabilities"
            )
        _validate_command(entry, f"verification.conditional[{index}]")
    if registry is not None:
        _validate_selected_skills(data, registry)
    return data


def load_project_manifest(path: Path, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    return validate_project_manifest(load_yaml_subset(path), registry)


def load_registry(path: Path) -> dict[str, Any]:
    data = load_yaml_subset(path)
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        raise ManifestError("Registry root must contain a skills list")
    return data


def validate_registry(registry_path: Path, repo_root: Path) -> None:
    registry = load_registry(registry_path)
    if registry.get("schema_version") != 1:
        raise ManifestError("Registry schema_version must remain 1")
    statuses = set(_expect_list(registry.get("status_values"), "status_values"))
    activation_values = set(_expect_list(registry.get("activation_values"), "activation_values"))
    capability_values = set(_expect_list(registry.get("capability_values"), "capability_values"))
    requirement_values = set(
        _expect_list(registry.get("capability_requirement_values"), "capability_requirement_values")
    )
    names: set[str] = set()
    paths: set[str] = set()

    for entry in registry["skills"]:
        if not isinstance(entry, dict):
            raise ManifestError("Each registry skill must be a mapping")
        name = _expect_string(entry.get("name"), "skills[].name")
        path = _expect_string(entry.get("path"), f"{name}.path")
        if name in names or path in paths:
            raise ManifestError(f"Duplicate registry skill or path: {name}")
        names.add(name)
        paths.add(path)
        if entry.get("status") not in statuses:
            raise ManifestError(f"{name}.status is not declared in status_values")
        if entry.get("activation") not in activation_values:
            raise ManifestError(f"{name}.activation is not declared in activation_values")
        conditions = _expect_string_list(entry.get("conditions", []), f"{name}.conditions")
        if entry["activation"] == "conditional" and not conditions:
            raise ManifestError(f"{name} is conditional but declares no conditions")
        skill_file = repo_root / path
        if not skill_file.is_file():
            raise ManifestError(f"{name}.path does not exist: {path}")
        frontmatter = skill_file.read_text(encoding="utf-8").split("---", 2)
        if len(frontmatter) < 3:
            raise ManifestError(f"{path} has no compatible frontmatter")
        match = re.search(r"^name:\s*(.+?)\s*$", frontmatter[1], re.MULTILINE)
        description = re.search(r"^description:\s*(.+?)\s*$", frontmatter[1], re.MULTILINE)
        if not match or match.group(1).strip().strip('"\'') != name or not description:
            raise ManifestError(f"{path} frontmatter must match registry name and include description")
        origin = entry.get("origin")
        if not isinstance(origin, dict) or not _expect_string(origin.get("type"), f"{name}.origin.type"):
            raise ManifestError(f"{name}.origin must declare type")
        if origin["type"] not in ALLOWED_ORIGIN_TYPES:
            raise ManifestError(f"{name}.origin.type is not supported")
        _expect_string(origin.get("repository"), f"{name}.origin.repository")
        if origin["type"] == "vendored":
            for key in ("repository", "path", "revision", "source_file", "license_file"):
                _expect_string(origin.get(key), f"{name}.origin.{key}")
            for key in ("source_file", "license_file"):
                if not (repo_root / origin[key]).is_file():
                    raise ManifestError(f"{name}.origin.{key} does not exist")
        for relation in ("handoff_to", "related"):
            _expect_string_list(entry.get(relation), f"{name}.{relation}")
        _expect_string_list(entry.get("inputs"), f"{name}.inputs")
        _expect_string_list(entry.get("outputs"), f"{name}.outputs")
        verification = entry.get("verification")
        if not isinstance(verification, dict):
            raise ManifestError(f"{name}.verification must be a mapping")
        _expect_string_list(verification.get("required"), f"{name}.verification.required")
        _expect_string_list(verification.get("conditional"), f"{name}.verification.conditional")
        references = _expect_string_list(entry.get("references"), f"{name}.references")
        for reference in references:
            if not isinstance(reference, str) or not (repo_root / reference).is_file():
                raise ManifestError(f"{name}.references contains a missing path: {reference!r}")
        capabilities = _expect_list(entry.get("capabilities"), f"{name}.capabilities")
        declared_capabilities: set[str] = set()
        for capability in capabilities:
            if not isinstance(capability, dict):
                raise ManifestError(f"{name}.capabilities entries must be mappings")
            capability_name = capability.get("name")
            if capability_name not in capability_values:
                raise ManifestError(f"{name} uses an unknown capability")
            if capability.get("requirement") not in requirement_values:
                raise ManifestError(f"{name} uses an unknown capability requirement")
            if capability_name in declared_capabilities:
                raise ManifestError(f"{name} declares a capability more than once: {capability_name}")
            declared_capabilities.add(capability_name)

    skill_directories = {
        f"skills/{directory.name}/SKILL.md"
        for directory in (repo_root / "skills").iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    }
    if paths != skill_directories:
        missing = sorted(skill_directories - paths)
        extra = sorted(paths - skill_directories)
        raise ManifestError(f"Registry/skill mismatch; missing={missing}, extra={extra}")
    unresolved = sorted(
        relation
        for entry in registry["skills"]
        for relation in [*entry["handoff_to"], *entry["related"]]
        if relation not in names
    )
    if unresolved:
        raise ManifestError(f"Registry points to unknown skills: {unresolved}")


def run_command(entry: dict[str, Any], project_root: Path) -> int:
    command = [entry["command"], *entry["args"]]
    print("==> verification:", " ".join(command))
    try:
        return subprocess.run(command, check=False, cwd=project_root).returncode
    except FileNotFoundError:
        print(f"Missing verification command: {entry['command']}", file=sys.stderr)
        return 127


def command_validate(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    load_project_manifest(Path(args.manifest), registry)
    print(f"Manifest valid: {args.manifest}")
    return 0


def command_registry(args: argparse.Namespace) -> int:
    validate_registry(Path(args.registry), Path(args.repo_root))
    print(f"Registry valid: {args.registry}")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    manifest = load_project_manifest(Path(args.manifest), registry)
    target_root = Path(args.project_root)
    failures = 0
    for agent in manifest["agents"]:
        instruction = target_root / ("AGENTS.md" if agent == "codex" else "CLAUDE.md")
        if instruction.is_file():
            print(f"ok   {agent} instructions: {instruction}")
        else:
            print(f"miss {agent} instructions: {instruction}", file=sys.stderr)
            failures += 1
        skill_root = Path.home() / (".codex/skills" if agent == "codex" else ".claude/skills")
        for skill in manifest["skills"]:
            if (skill_root / skill / "SKILL.md").is_file():
                print(f"ok   {agent} skill: {skill}")
            else:
                print(f"miss {agent} skill: {skill_root / skill}", file=sys.stderr)
                failures += 1
    if failures:
        return 1
    print("Doctor passed.")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    manifest = load_project_manifest(Path(args.manifest), registry)
    requested_capabilities = set(args.with_capability)
    declared_capabilities = {entry["name"] for entry in manifest["capabilities"]}
    unknown = requested_capabilities - declared_capabilities
    if unknown:
        raise ManifestError(f"Unknown requested capability: {sorted(unknown)}")
    commands = list(manifest["verification"]["required"])
    commands.extend(
        entry
        for entry in manifest["verification"]["conditional"]
        if entry["capability"] in requested_capabilities
    )
    if not commands:
        print("No verification commands selected.")
        return 0
    project_root = Path(args.manifest).resolve().parent
    failures = sum(run_command(entry, project_root) != 0 for entry in commands)
    if failures:
        print(f"Verification failed: {failures} command(s) failed.", file=sys.stderr)
        return 1
    print(f"Verification passed: {len(commands)} command(s).")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--manifest", required=True)
    validate.add_argument("--registry", required=True)
    validate.set_defaults(handler=command_validate)

    registry = subparsers.add_parser("registry")
    registry.add_argument("--registry", required=True)
    registry.add_argument("--repo-root", required=True)
    registry.set_defaults(handler=command_registry)

    doctor = subparsers.add_parser("doctor")
    doctor.add_argument("--manifest", required=True)
    doctor.add_argument("--registry", required=True)
    doctor.add_argument("--project-root", required=True)
    doctor.set_defaults(handler=command_doctor)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--manifest", required=True)
    verify.add_argument("--registry", required=True)
    verify.add_argument("--with-capability", action="append", default=[])
    verify.set_defaults(handler=command_verify)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        return args.handler(args)
    except (ManifestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    # Kept as a compatibility entry point for the v1 project runtime. The
    # current v2 validators live in platform.py; project.py owns doctor/verify.
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        sys.argv[1] = "manifest"
    if len(sys.argv) > 1 and sys.argv[1] in {"doctor", "verify"}:
        print("error: use project.py for doctor and verify", file=sys.stderr)
        raise SystemExit(2)
    from platform import main as platform_main

    raise SystemExit(platform_main())
