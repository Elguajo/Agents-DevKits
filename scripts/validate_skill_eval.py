#!/usr/bin/env python3
"""Deterministically validate live-evaluation packets and JSON records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_manifest import ManifestError, load_yaml_subset  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("eval", "judge", "benchmark", "rubric", "candidate", "baseline", "comparison", "score")
CLASSES = {"correctness", "safety", "security_authorization", "evidence_truthfulness", "efficiency", "other"}


def record(path: Path, kind: str) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ManifestError(f"Invalid {kind} JSON: {error}") from error
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ManifestError(f"{kind} must have schema_version 1")
    return data


def validate_schemas() -> None:
    for name, required in (
        ("RUN_RECORD.schema.json", {"schema_version", "run_id", "pilot_id", "variant"}),
        ("JUDGE_RECORD.schema.json", {"schema_version", "judge_id", "pilot_id", "artifacts"}),
    ):
        try:
            schema = json.loads((ROOT / "evals/live" / name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ManifestError(f"Invalid schema {name}: {error}") from error
        properties = schema.get("properties") if isinstance(schema, dict) else None
        if not isinstance(properties, dict) or not required <= set(properties):
            raise ManifestError(f"Schema {name} is missing required contract fields")


def validate_run(data: dict) -> None:
    required = {"schema_version", "run_id", "pilot_id", "variant", "environment", "assertions", "metrics", "artifacts"}
    if set(data) != required or data["variant"] not in {"baseline", "candidate"}:
        raise ManifestError("run record has invalid fields or variant")
    environment = data["environment"]
    if not isinstance(environment, dict) or set(environment) != {"repository_snapshot", "runtime", "task_digest", "tool_profile", "permission_profile"} or not all(isinstance(value, str) and value for value in environment.values()):
        raise ManifestError("run environment is incomplete")
    assertions = data["assertions"]
    if not isinstance(assertions, list) or not assertions:
        raise ManifestError("run assertions must be non-empty")
    ids = set()
    for item in assertions:
        if not isinstance(item, dict) or set(item) != {"id", "status", "class"} or not isinstance(item["id"], str) or not item["id"] or item["status"] not in {"passed", "failed", "unavailable"} or item["class"] not in CLASSES or item["id"] in ids:
            raise ManifestError("run assertion is invalid or duplicated")
        ids.add(item["id"])
    if not isinstance(data["metrics"], dict) or not isinstance(data["artifacts"], list) or not all(isinstance(item, str) and item for item in data["artifacts"]):
        raise ManifestError("run metrics or artifacts are invalid")


def validate_judge(data: dict) -> None:
    required = {"schema_version", "judge_id", "pilot_id", "artifacts", "dimensions"}
    if set(data) != required:
        raise ManifestError("judge record has invalid fields")
    artifacts = data["artifacts"]
    if not isinstance(artifacts, dict) or set(artifacts) != {"Artifact A", "Artifact B"}:
        raise ManifestError("judge artifacts must use anonymous Artifact A/B labels")
    dimensions = data["dimensions"]
    if not isinstance(dimensions, list) or not dimensions:
        raise ManifestError("judge dimensions must be non-empty")
    for item in dimensions:
        if not isinstance(item, dict) or set(item) != {"name", "winner", "reason"} or item["winner"] not in {"Artifact A", "Artifact B", "tie", "unavailable"}:
            raise ManifestError("judge dimension is invalid")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet")
    parser.add_argument("--run")
    parser.add_argument("--judge")
    args = parser.parse_args()
    try:
        validate_schemas()
        if not any((args.packet, args.run, args.judge)):
            raise ManifestError("Provide --packet, --run, or --judge")
        if args.packet:
            task = Path(args.packet, "TASK.md").read_text(encoding="utf-8").lower()
            if any(word in task for word in FORBIDDEN):
                raise ManifestError("candidate-visible task leaks evaluation intent")
        if args.run:
            data = record(Path(args.run), "run record")
            validate_run(data)
        if args.judge:
            data = record(Path(args.judge), "judge record")
            validate_judge(data)
        print("Live skill-eval contract valid")
        return 0
    except (ManifestError, OSError) as error:
        print(f"Live skill-eval contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
