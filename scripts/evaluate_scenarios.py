#!/usr/bin/env python3
"""Run deterministic routing contract scenarios; this is not a model benchmark."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_manifest import ManifestError, load_yaml_subset  # noqa: E402
from platform import validate_skill_registry, resolve_route  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        registry = validate_skill_registry(
            ROOT / "skills/registry.yaml", ROOT, ROOT / "capabilities/registry.yaml"
        )
        data = load_yaml_subset(ROOT / "evals/scenarios.yaml")
        if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("scenarios"), list):
            raise ManifestError("Scenario suite schema is invalid")
        failures: list[str] = []
        scenario_ids: set[str] = set()
        exercised: set[str] = set()
        for scenario in data["scenarios"]:
            if not isinstance(scenario, dict):
                raise ManifestError("Each routing scenario must be a mapping")
            identifier = scenario.get("id")
            if not isinstance(identifier, str) or not identifier:
                raise ManifestError("Each routing scenario needs a non-empty id")
            if identifier in scenario_ids:
                raise ManifestError(f"Routing scenario id is duplicated: {identifier}")
            scenario_ids.add(identifier)
            facts = scenario.get("facts")
            expected = scenario.get("expected")
            if not isinstance(facts, list) or not all(isinstance(fact, str) and fact for fact in facts):
                raise ManifestError(f"{identifier}: facts must be non-empty strings")
            if not isinstance(expected, dict):
                raise ManifestError(f"{identifier}: expected must be a mapping")
            selected = expected.get("selected", [])
            skipped = expected.get("skipped", [])
            exercised.update(selected)
            exercised.update(skipped)
            if not all(isinstance(skill, str) and skill for skill in selected + skipped):
                raise ManifestError(f"{identifier}: selected and skipped skills must be non-empty strings")
            if set(selected) & set(skipped):
                raise ManifestError(f"{identifier}: a skill cannot be both selected and skipped")
            expected_routing = expected.get("routing", {})
            if not isinstance(expected_routing, dict) or not set(expected_routing) <= {"auto", "propose", "ask"}:
                raise ManifestError(f"{identifier}: routing must use only auto, propose, and ask")
            for tier, skills in expected_routing.items():
                if not isinstance(skills, list) or not all(isinstance(skill, str) and skill for skill in skills):
                    raise ManifestError(f"{identifier}: routing.{tier} must contain non-empty skill names")
            result = resolve_route(registry, set(facts))
            if result["depth"] != expected["depth"]:
                failures.append(f"{scenario['id']}: expected depth {expected['depth']}, got {result['depth']}")
            for skill in expected.get("selected", []):
                if skill not in result["skills"]:
                    failures.append(f"{scenario['id']}: missing selected skill {skill}")
            for skill in expected.get("skipped", []):
                if skill in result["skills"]:
                    failures.append(f"{scenario['id']}: unexpectedly selected skill {skill}")
            for capability in expected.get("required_capabilities", []):
                if capability not in result["capabilities"]["required"]:
                    failures.append(f"{scenario['id']}: missing required capability {capability}")
            for kind in expected.get("evidence", []):
                if kind not in result["evidence"]:
                    failures.append(f"{scenario['id']}: missing evidence kind {kind}")
            for handoff in expected.get("handoffs", []):
                if handoff not in result["handoffs"]:
                    failures.append(f"{scenario['id']}: missing handoff {handoff}")
            for tier, skills in expected_routing.items():
                for skill in skills:
                    if skill not in result["routing"][tier]:
                        failures.append(f"{scenario['id']}: {skill} is not routed as {tier}")
        known = {entry["name"] for entry in registry["skills"]}
        unknown = sorted(exercised - known)
        if unknown:
            failures.append(f"scenarios reference unknown skills: {unknown}")
        routable = {
            entry["name"] for entry in registry["skills"] if "model" in entry["invocation"]
        }
        unexercised = sorted(routable - exercised)
        if unexercised:
            failures.append(
                "model-invocable skills that no scenario selects or skips: " f"{unexercised}"
            )
        if failures:
            print("Scenario eval failed:", *failures, sep="\n", file=sys.stderr)
            return 1
        print("Scenario evals passed")
        return 0
    except (ManifestError, OSError, KeyError, TypeError) as error:
        print(f"Scenario eval error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
