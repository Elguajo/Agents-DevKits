#!/usr/bin/env python3
"""Prepare an isolated, candidate-blinded packet from a declared pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_manifest import ManifestError, load_yaml_subset  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("eval", "judge", "benchmark", "rubric", "candidate", "baseline", "comparison", "score")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", required=True)
    parser.add_argument("--variant", choices=("baseline", "candidate"), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        data = load_yaml_subset(ROOT / "evals/skill-quality-pilots.yaml")
        pilots = data.get("pilots") if isinstance(data, dict) else None
        pilot = next((item for item in pilots or [] if item.get("id") == args.pilot), None)
        if not isinstance(pilot, dict):
            raise ManifestError(f"Unknown pilot: {args.pilot}")
        task = pilot.get("task")
        if not isinstance(task, str) or not task.strip():
            raise ManifestError(f"{args.pilot}: missing task")
        assertions = pilot.get("assertions")
        if not isinstance(assertions, list) or not assertions or not all(
            isinstance(item, str) and item for item in assertions
        ):
            raise ManifestError(f"{args.pilot}: missing assertions")
        if any(word in task.lower() for word in FORBIDDEN):
            raise ManifestError("Pilot task leaks evaluation intent into candidate-visible context")
        output = Path(args.output).resolve()
        if output.exists() and any(output.iterdir()):
            raise ManifestError("Output directory must be empty")
        output.mkdir(parents=True, exist_ok=True)
        (output / "TASK.md").write_text(f"# Task\n\n{task.strip()}\n", encoding="utf-8")
        digest = hashlib.sha256(task.encode()).hexdigest()
        acceptance_digest = hashlib.sha256(
            json.dumps(assertions, ensure_ascii=False, separators=(",", ":")).encode()
        ).hexdigest()
        # Keep variant, pilot identity, and digest in the controller's output,
        # never in a file the candidate can inspect.
        print(f"Prepared isolated task: {output}")
        print(
            f"pilot_id={args.pilot} variant={args.variant} task_digest={digest} "
            f"acceptance_digest={acceptance_digest}"
        )
        return 0
    except (ManifestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
