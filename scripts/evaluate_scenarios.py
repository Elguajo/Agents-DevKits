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
        for scenario in data["scenarios"]:
            expected = scenario["expected"]
            result = resolve_route(registry, set(scenario["facts"]))
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
