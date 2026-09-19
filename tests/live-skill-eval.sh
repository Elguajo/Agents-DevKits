#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
tmp_root="$(mktemp -d)"
trap 'rm -rf "$tmp_root"' EXIT

echo "==> live skill-eval packets are blinded and deterministic"
python3 "$repo_root/scripts/prepare_skill_eval.py" \
  --pilot debugging-root-cause --variant baseline --output "$tmp_root/packet"
python3 "$repo_root/scripts/validate_skill_eval.py" --packet "$tmp_root/packet"
test "$(find "$tmp_root/packet" -type f | wc -l | tr -d ' ')" = "1"
if rg -i 'eval|judge|benchmark|rubric|candidate|baseline|comparison|score' "$tmp_root/packet/TASK.md"; then
  echo 'Candidate-visible task leaked evaluation intent' >&2
  exit 1
fi

python3 - "$tmp_root" <<'PY'
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
environment = {
    "repository_snapshot": "test-sha",
    "runtime": "test-runtime",
    "task_digest": "test-digest",
    "acceptance_digest": "test-acceptance-digest",
    "tool_profile": "test-tools",
    "permission_profile": "test-permissions",
}
base = {
    "schema_version": 1,
    "run_id": "base-1",
    "pilot_id": "debugging-root-cause",
    "variant": "baseline",
    "environment": environment,
    "assertions": [{"id": "root-cause", "status": "passed", "class": "correctness"}],
    "metrics": {"turns": "unavailable"},
    "artifacts": ["diff.patch"],
}
candidate = {**base, "run_id": "candidate-1", "variant": "candidate"}
(root / "baseline.json").write_text(json.dumps(base))
(root / "candidate.json").write_text(json.dumps(candidate))
candidate["assertions"] = [{"id": "root-cause", "status": "failed", "class": "correctness"}]
(root / "regression.json").write_text(json.dumps(candidate))
candidate["assertions"] = [{"id": "different-check", "status": "passed", "class": "correctness"}]
(root / "missing-assertion.json").write_text(json.dumps(candidate))
candidate["assertions"] = [{"id": "root-cause", "status": "passed", "class": "correctness"}]
candidate["environment"] = {**environment, "acceptance_digest": "different-acceptance-digest"}
(root / "different-acceptance.json").write_text(json.dumps(candidate))
judge = {
    "schema_version": 1,
    "judge_id": "reviewer-1",
    "pilot_id": "debugging-root-cause",
    "artifacts": {"Artifact A": "run-a", "Artifact B": "run-b"},
    "dimensions": [{"name": "correctness", "winner": "Artifact A", "reason": "Observed artifact evidence."}],
}
(root / "judge.json").write_text(json.dumps(judge))
PY
python3 "$repo_root/scripts/validate_skill_eval.py" --run "$tmp_root/baseline.json" --judge "$tmp_root/judge.json"
python3 "$repo_root/scripts/analyze_skill_eval.py" --baseline "$tmp_root/baseline.json" --candidate "$tmp_root/candidate.json" | grep -q '"promotion_blocked": false'
if python3 "$repo_root/scripts/analyze_skill_eval.py" --baseline "$tmp_root/baseline.json" --candidate "$tmp_root/regression.json" >/tmp/agents-devkits-live-eval-regression.json; then
  echo 'Expected hard regression to block promotion' >&2
  exit 1
fi
grep -q 'root-cause' /tmp/agents-devkits-live-eval-regression.json
if python3 "$repo_root/scripts/analyze_skill_eval.py" --baseline "$tmp_root/baseline.json" --candidate "$tmp_root/missing-assertion.json" >/tmp/agents-devkits-live-eval-missing.log 2>&1; then
  echo 'Expected assertion-set mismatch to invalidate the comparison' >&2
  exit 1
fi
grep -q 'assertion IDs' /tmp/agents-devkits-live-eval-missing.log
if python3 "$repo_root/scripts/analyze_skill_eval.py" --baseline "$tmp_root/baseline.json" --candidate "$tmp_root/different-acceptance.json" >/tmp/agents-devkits-live-eval-acceptance.log 2>&1; then
  echo 'Expected changed acceptance criteria to invalidate the comparison' >&2
  exit 1
fi
grep -q 'acceptance_digest' /tmp/agents-devkits-live-eval-acceptance.log

echo "live skill-eval tests passed"
