#!/usr/bin/env python3
"""Portable contracts and deterministic diagnostics for Agents DevKits.

This module validates declarative platform metadata. It deliberately does not
schedule agents or invoke provider-specific tools.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
import re
import sys
from typing import Any

from project_manifest import ManifestError, load_yaml_subset


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENT_KEYS = ("required", "preferred", "optional")
INVOCATION_VALUES = {"user", "model"}


def expect_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError(f"{label} must be a mapping")
    return value


def expect_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ManifestError(f"{label} must be a list")
    return value


def expect_strings(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    values = expect_list(value, label)
    if not allow_empty and not values:
        raise ManifestError(f"{label} must not be empty")
    if not all(isinstance(item, str) and item for item in values):
        raise ManifestError(f"{label} must contain non-empty strings")
    return values


def expect_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{label} must be a non-empty string")
    return value


def load_document(path: Path) -> dict[str, Any]:
    return expect_mapping(load_yaml_subset(path), str(path))


def load_capability_registry(path: Path) -> dict[str, Any]:
    data = load_document(path)
    if data.get("schema_version") != 1:
        raise ManifestError("Capability registry schema_version must be 1")
    requirements = expect_strings(data.get("requirement_values"), "capability requirement_values")
    if set(requirements) != set(REQUIREMENT_KEYS):
        raise ManifestError("Capability requirement_values must be required, preferred, optional")
    expect_mapping(data.get("fallback_contract"), "capability fallback_contract")
    capabilities = expect_mapping(data.get("capabilities"), "capabilities")
    if not capabilities:
        raise ManifestError("Capability registry must declare capabilities")
    for name, definition in capabilities.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise ManifestError(f"Invalid capability name: {name!r}")
        expect_string(expect_mapping(definition, f"capability {name}").get("description"), f"capability {name}.description")
    return data


def load_evidence_contract(path: Path) -> dict[str, Any]:
    data = load_document(path)
    if data.get("schema_version") != 1:
        raise ManifestError("Evidence contract schema_version must be 1")
    for key in ("status_values", "source_values", "kind_values", "required_fields", "rules"):
        expect_strings(data.get(key), f"evidence.{key}", allow_empty=False)
    return data


def _frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ManifestError(f"{path} has no compatible frontmatter")
    name = re.search(r"^name:\s*(.+?)\s*$", match.group(1), re.MULTILINE)
    description = re.search(r"^description:\s*(.+?)\s*$", match.group(1), re.MULTILINE)
    if not name or not description:
        raise ManifestError(f"{path} frontmatter requires name and description")
    return name.group(1).strip().strip("\"'")


def _validate_trigger_expression(value: Any, label: str, trigger_values: set[str]) -> None:
    expression = expect_mapping(value, label)
    unknown_keys = set(expression) - {"any", "all", "none"}
    if unknown_keys:
        raise ManifestError(f"{label} uses unsupported operators: {sorted(unknown_keys)}")
    if not expression:
        raise ManifestError(f"{label} must declare at least one operator")
    for operator, values in expression.items():
        for trigger in expect_strings(values, f"{label}.{operator}"):
            if trigger not in trigger_values:
                raise ManifestError(f"{label} uses unknown trigger: {trigger}")


def _validate_capability_requirements(value: Any, label: str, known_capabilities: set[str]) -> None:
    requirements = expect_mapping(value, label)
    if set(requirements) != set(REQUIREMENT_KEYS):
        raise ManifestError(f"{label} must contain required, preferred, and optional")
    seen: set[str] = set()
    for requirement in REQUIREMENT_KEYS:
        for capability in expect_strings(requirements[requirement], f"{label}.{requirement}"):
            if capability not in known_capabilities:
                raise ManifestError(f"{label} uses unknown capability: {capability}")
            if capability in seen:
                raise ManifestError(f"{label} declares capability more than once: {capability}")
            seen.add(capability)


def _validate_references(entry: dict[str, Any], skill_file: Path, trigger_values: set[str]) -> None:
    references = expect_list(entry.get("references"), f"{entry['name']}.references")
    for index, reference in enumerate(references):
        reference_map = expect_mapping(reference, f"{entry['name']}.references[{index}]")
        path = expect_string(reference_map.get("path"), f"{entry['name']}.references[{index}].path")
        if not (skill_file.parent / path).is_file():
            raise ManifestError(f"{entry['name']}.references[{index}] path does not exist: {path}")
        when = reference_map.get("when")
        if when is not None and when not in trigger_values:
            raise ManifestError(f"{entry['name']}.references[{index}] uses unknown trigger: {when}")


def validate_skill_registry(
    registry_path: Path,
    repo_root: Path,
    capability_registry_path: Path,
) -> dict[str, Any]:
    capabilities = load_capability_registry(capability_registry_path)
    data = load_document(registry_path)
    if data.get("schema_version") != 2:
        raise ManifestError("Skill registry schema_version must be 2")
    status_values = set(expect_strings(data.get("status_values"), "status_values"))
    trigger_values = set(expect_strings(data.get("trigger_values"), "trigger_values"))
    if not trigger_values:
        raise ManifestError("trigger_values must not be empty")
    evidence_values = set(load_evidence_contract(repo_root / "contracts/evidence.yaml")["kind_values"])
    known_capabilities = set(expect_mapping(capabilities["capabilities"], "capabilities"))
    names: set[str] = set()
    paths: set[str] = set()
    entries = expect_list(data.get("skills"), "skills")

    for raw_entry in entries:
        entry = expect_mapping(raw_entry, "skills[]")
        name = expect_string(entry.get("name"), "skills[].name")
        path = expect_string(entry.get("path"), f"{name}.path")
        if name in names or path in paths:
            raise ManifestError(f"Duplicate registry skill or path: {name}")
        names.add(name)
        paths.add(path)
        if entry.get("status") not in status_values:
            raise ManifestError(f"{name}.status is not declared in status_values")
        invocation = set(expect_strings(entry.get("invocation"), f"{name}.invocation", allow_empty=False))
        if not invocation <= INVOCATION_VALUES:
            raise ManifestError(f"{name}.invocation uses unsupported values")
        _validate_trigger_expression(entry.get("triggers"), f"{name}.triggers", trigger_values)
        expect_strings(entry.get("inputs"), f"{name}.inputs")
        expect_strings(entry.get("outputs"), f"{name}.outputs")
        _validate_capability_requirements(entry.get("capabilities"), f"{name}.capabilities", known_capabilities)
        skill_file = repo_root / path
        if not skill_file.is_file():
            raise ManifestError(f"{name}.path does not exist: {path}")
        if _frontmatter_name(skill_file) != name:
            raise ManifestError(f"{path} frontmatter name does not match registry")
        _validate_references(entry, skill_file, trigger_values)
        verification = expect_mapping(entry.get("verification"), f"{name}.verification")
        for evidence_kind in expect_strings(verification.get("produces"), f"{name}.verification.produces"):
            if evidence_kind not in evidence_values:
                raise ManifestError(f"{name}.verification.produces uses unknown evidence kind")
        for relation in ("handoff_to", "related"):
            expect_strings(entry.get(relation), f"{name}.{relation}")
        origin = expect_mapping(entry.get("origin"), f"{name}.origin")
        origin_type = expect_string(origin.get("type"), f"{name}.origin.type")
        expect_string(origin.get("repository"), f"{name}.origin.repository")
        if origin_type not in {"local", "vendored"}:
            raise ManifestError(f"{name}.origin.type is not supported")
        if origin_type == "vendored":
            for field in ("path", "revision", "source_file", "license_file"):
                expect_string(origin.get(field), f"{name}.origin.{field}")
            for field in ("source_file", "license_file"):
                if not (repo_root / origin[field]).is_file():
                    raise ManifestError(f"{name}.origin.{field} does not exist")

    directories = {
        f"skills/{directory.name}/SKILL.md"
        for directory in (repo_root / "skills").iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    }
    if paths != directories:
        raise ManifestError(
            f"Registry/skill mismatch; missing={sorted(directories - paths)}, extra={sorted(paths - directories)}"
        )
    unresolved = sorted(
        related
        for entry in entries
        for related in [*entry["handoff_to"], *entry["related"]]
        if related not in names
    )
    if unresolved:
        raise ManifestError(f"Registry points to unknown skills: {unresolved}")
    return data


def _normalise_v1_manifest(data: dict[str, Any]) -> dict[str, Any]:
    grouped = {key: [] for key in REQUIREMENT_KEYS}
    for item in expect_list(data.get("capabilities"), "capabilities"):
        item_map = expect_mapping(item, "capabilities[]")
        grouped[expect_string(item_map.get("requirement"), "capability.requirement")].append(
            expect_string(item_map.get("name"), "capability.name")
        )
    baseline = []
    for index, command in enumerate(expect_list(expect_mapping(data.get("verification"), "verification").get("required"), "verification.required")):
        command_map = expect_mapping(command, "verification.required[]")
        baseline.append({"id": f"required-{index + 1}", "kind": "test", **command_map})
    conditions = []
    for index, command in enumerate(expect_list(expect_mapping(data.get("verification"), "verification").get("conditional"), "verification.conditional")):
        command_map = expect_mapping(command, "verification.conditional[]")
        capability = expect_string(command_map.get("capability"), "verification.conditional[].capability")
        conditions.append({"when": {"capabilities": [capability]}, "run": [{"id": f"conditional-{index + 1}", "kind": "test", **command_map}]})
    return {
        "schema": 1,
        "platform": {"version": ">=1.0 <2.0"},
        "agents": data.get("agents"),
        "skills": {"include": data.get("skills")},
        "capabilities": grouped,
        "verification": {"baseline": baseline, "conditions": conditions},
        "legacy_schema_version": 1,
    }


def normalise_project_manifest(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") == 1:
        return _normalise_v1_manifest(data)
    return data


def _validate_command(value: Any, label: str) -> None:
    command = expect_mapping(value, label)
    executable = expect_string(command.get("command"), f"{label}.command")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", executable):
        raise ManifestError(f"{label}.command must be a simple command name")
    if not all(isinstance(arg, str) for arg in expect_list(command.get("args", []), f"{label}.args")):
        raise ManifestError(f"{label}.args must contain strings")


def validate_project_manifest(
    manifest_path: Path,
    registry: dict[str, Any],
    capabilities: dict[str, Any],
) -> dict[str, Any]:
    data = normalise_project_manifest(load_document(manifest_path))
    if data.get("schema") != 1:
        raise ManifestError("Project manifest schema must be 1")
    platform = expect_mapping(data.get("platform"), "platform")
    expect_string(platform.get("version"), "platform.version")
    agents = set(expect_strings(data.get("agents"), "agents", allow_empty=False))
    if not agents <= {"codex", "claude"}:
        raise ManifestError("agents must contain codex and/or claude")
    selected = expect_strings(expect_mapping(data.get("skills"), "skills").get("include"), "skills.include")
    known_skills = {entry["name"] for entry in registry["skills"]}
    unknown_skills = sorted(set(selected) - known_skills)
    if unknown_skills:
        raise ManifestError(f"Manifest selects unknown skills: {unknown_skills}")
    known_capabilities = set(capabilities["capabilities"])
    manifest_capabilities = expect_mapping(data.get("capabilities"), "capabilities")
    if set(manifest_capabilities) != set(REQUIREMENT_KEYS):
        raise ManifestError("manifest capabilities must contain required, preferred, and optional")
    declared: set[str] = set()
    for level in REQUIREMENT_KEYS:
        for capability in expect_strings(manifest_capabilities[level], f"capabilities.{level}"):
            if capability not in known_capabilities:
                raise ManifestError(f"Manifest declares unknown capability: {capability}")
            if capability in declared:
                raise ManifestError(f"Manifest declares capability more than once: {capability}")
            declared.add(capability)
    verification = expect_mapping(data.get("verification"), "verification")
    baseline = expect_list(verification.get("baseline"), "verification.baseline")
    conditions = expect_list(verification.get("conditions"), "verification.conditions")
    for index, check in enumerate(baseline):
        _validate_command(check, f"verification.baseline[{index}]")
        expect_string(expect_mapping(check, "check").get("id"), f"verification.baseline[{index}].id")
    for index, condition in enumerate(conditions):
        condition_map = expect_mapping(condition, f"verification.conditions[{index}]")
        when = expect_mapping(condition_map.get("when"), f"verification.conditions[{index}].when")
        if not set(when) <= {"paths", "risks", "capabilities"} or not when:
            raise ManifestError(f"verification.conditions[{index}].when is invalid")
        for key in ("paths", "risks", "capabilities"):
            if key in when:
                values = expect_strings(when[key], f"verification.conditions[{index}].when.{key}")
                if key == "capabilities" and not set(values) <= declared:
                    raise ManifestError(f"verification.conditions[{index}] uses undeclared capability")
        for check_index, check in enumerate(expect_list(condition_map.get("run", []), f"verification.conditions[{index}].run")):
            _validate_command(check, f"verification.conditions[{index}].run[{check_index}]")
        reviews = expect_strings(condition_map.get("require_reviews", []), f"verification.conditions[{index}].require_reviews")
        if not set(reviews) <= known_skills:
            raise ManifestError(f"verification.conditions[{index}] requires unknown review")
    return data


def version_is_compatible(version: str, requirement: str) -> bool:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ManifestError(f"Platform VERSION is invalid: {version!r}")
    current = tuple(map(int, match.groups()))
    for operator, value in re.findall(r"(>=|<=|>|<|=)?\s*(\d+\.\d+(?:\.\d+)?)", requirement):
        target = tuple(map(int, (value + ".0.0").split(".")[:3]))
        operator = operator or "="
        if not {">=": current >= target, "<=": current <= target, ">": current > target, "<": current < target, "=": current == target}[operator]:
            return False
    return bool(re.findall(r"\d+\.\d+", requirement))


def trigger_matches(expression: dict[str, Any], facts: set[str]) -> bool:
    any_values = set(expression.get("any", []))
    all_values = set(expression.get("all", []))
    none_values = set(expression.get("none", []))
    return (not any_values or bool(any_values & facts)) and all_values <= facts and not (none_values & facts)


def resolve_route(registry: dict[str, Any], facts: set[str]) -> dict[str, Any]:
    if facts & {"task.security_sensitive", "surface.auth", "surface.permissions", "surface.secrets", "surface.untrusted_input", "surface.payments", "surface.migration", "surface.destructive", "surface.public_api"}:
        depth = "FULL"
    elif facts == {"task.documentation"}:
        depth = "DIRECT"
    else:
        depth = "FOCUSED"
    selected = [
        entry for entry in registry["skills"]
        if "model" in entry["invocation"] and trigger_matches(entry["triggers"], facts)
    ]
    capabilities = {level: set() for level in REQUIREMENT_KEYS}
    evidence: set[str] = set()
    handoffs: set[str] = set()
    for entry in selected:
        for level in REQUIREMENT_KEYS:
            capabilities[level].update(entry["capabilities"][level])
        evidence.update(entry["verification"]["produces"])
        handoffs.update(entry["handoff_to"])
    return {"depth": depth, "skills": [entry["name"] for entry in selected], "capabilities": {key: sorted(value) for key, value in capabilities.items()}, "evidence": sorted(evidence), "handoffs": sorted(handoffs)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("registry", "capabilities", "evidence", "manifest", "route"))
    parser.add_argument("--registry", default=str(ROOT / "skills/registry.yaml"))
    parser.add_argument("--capabilities", default=str(ROOT / "capabilities/registry.yaml"))
    parser.add_argument("--evidence", default=str(ROOT / "contracts/evidence.yaml"))
    parser.add_argument("--manifest")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--fact", action="append", default=[])
    args = parser.parse_args()
    try:
        capability_data = load_capability_registry(Path(args.capabilities))
        if args.command == "capabilities":
            print("Capability registry valid")
            return 0
        if args.command == "evidence":
            load_evidence_contract(Path(args.evidence))
            print("Evidence contract valid")
            return 0
        registry = validate_skill_registry(Path(args.registry), Path(args.repo_root), Path(args.capabilities))
        if args.command == "registry":
            print("Skill registry valid")
            return 0
        if args.command == "manifest":
            if not args.manifest:
                raise ManifestError("--manifest is required")
            validate_project_manifest(Path(args.manifest), registry, capability_data)
            print("Project manifest valid")
            return 0
        print(json.dumps(resolve_route(registry, set(args.fact)), sort_keys=True))
        return 0
    except (ManifestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
