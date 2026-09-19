#!/usr/bin/env python3
"""Compare validated baseline and candidate run records without scoring models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill_eval import record, validate_run  # noqa: E402

HARD = {"correctness", "safety", "security_authorization", "evidence_truthfulness"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
    try:
        baseline = record(Path(args.baseline), "baseline run record")
        candidate = record(Path(args.candidate), "candidate run record")
        validate_run(baseline)
        validate_run(candidate)
        if baseline["variant"] != "baseline" or candidate["variant"] != "candidate":
            raise ValueError("records must use baseline and candidate variants")
        for key in ("pilot_id",):
            if baseline[key] != candidate[key]:
                raise ValueError(f"records disagree on {key}")
        for key in ("repository_snapshot", "runtime", "task_digest", "acceptance_digest", "tool_profile", "permission_profile"):
            if baseline["environment"][key] != candidate["environment"][key]:
                raise ValueError(f"records disagree on controlled environment: {key}")
        baseline_assertions = {item["id"]: item for item in baseline["assertions"]}
        candidate_assertions = {item["id"]: item for item in candidate["assertions"]}
        if set(baseline_assertions) != set(candidate_assertions):
            raise ValueError("records disagree on assertion IDs")
        changed_classes = sorted(
            identifier
            for identifier, item in baseline_assertions.items()
            if item["class"] != candidate_assertions[identifier]["class"]
        )
        if changed_classes:
            raise ValueError(f"records disagree on assertion classes: {', '.join(changed_classes)}")
        regressions = [
            item["id"] for item in baseline_assertions.values()
            if item["status"] == "passed" and item["class"] in HARD
            and candidate_assertions[item["id"]]["status"] == "failed"
        ]
        print(json.dumps({"pilot_id": baseline["pilot_id"], "hard_regressions": regressions, "promotion_blocked": bool(regressions)}, sort_keys=True))
        return 1 if regressions else 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Live skill-eval analysis error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
