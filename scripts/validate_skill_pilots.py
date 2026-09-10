#!/usr/bin/env python3
"""Validate deliberately runnable skill-quality pilot definitions."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_manifest import ManifestError, load_yaml_subset  # noqa: E402
from platform import validate_skill_registry  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def require_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ManifestError(f"{label} must contain non-empty strings")
    return value


def main() -> int:
    try:
        registry = validate_skill_registry(
            ROOT / "skills/registry.yaml", ROOT, ROOT / "capabilities/registry.yaml"
        )
        data = load_yaml_subset(ROOT / "evals/skill-quality-pilots.yaml")
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ManifestError("Skill pilot schema_version must be 1")
        pilots = data.get("pilots")
        if not isinstance(pilots, list) or not pilots:
            raise ManifestError("Skill pilots must be a non-empty list")
        known_skills = {entry["name"] for entry in registry["skills"]}
        identifiers: set[str] = set()
        for pilot in pilots:
            if not isinstance(pilot, dict):
                raise ManifestError("Each skill pilot must be a mapping")
            identifier = pilot.get("id")
            if not isinstance(identifier, str) or not identifier:
                raise ManifestError("Each skill pilot needs a non-empty id")
            if identifier in identifiers:
                raise ManifestError(f"Skill pilot id is duplicated: {identifier}")
            identifiers.add(identifier)
            if pilot.get("skill") not in known_skills:
                raise ManifestError(f"{identifier}: skill is not installed")
            if pilot.get("baseline") != "without-skill":
                raise ManifestError(f"{identifier}: baseline must be without-skill")
            if not isinstance(pilot.get("task"), str) or not pilot["task"]:
                raise ManifestError(f"{identifier}: task must be a non-empty string")
            require_strings(pilot.get("assertions"), f"{identifier}.assertions")
        print("Skill quality pilot contract valid")
        return 0
    except (ManifestError, OSError, KeyError, TypeError) as error:
        print(f"Skill quality pilot contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
