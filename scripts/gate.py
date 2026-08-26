#!/usr/bin/env python3
"""Run the reproducible Agents DevKits platform gate."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(identifier: str, command: list[str]) -> tuple[str, str] | None:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode == 0:
        return None
    return identifier, (result.stdout + result.stderr).strip()


def main() -> int:
    checks = [
        ("python-syntax", [sys.executable, "-c", "from pathlib import Path; [compile(path.read_text(), str(path), 'exec') for path in Path('.').rglob('*.py') if '.git' not in path.parts]" ]),
        ("shell-syntax", ["bash", "-c", "find . -type f -name '*.sh' -not -path '*/.git/*' -print0 | xargs -0 bash -n"]),
        ("capabilities", [sys.executable, "scripts/platform.py", "capabilities"]),
        ("evidence-contract", [sys.executable, "scripts/platform.py", "evidence"]),
        ("skill-registry", [sys.executable, "scripts/validate_registry.py"]),
        ("adapter-parity", ["bash", "tests/adapter-parity.sh"]),
        ("secret-guard", ["bash", "devkit/scripts/secret-guard.sh", "."]),
        ("installer-fixtures", ["bash", "tests/platform.sh"]),
        ("project-runtime", ["bash", "tests/project-runtime.sh"]),
        ("routing-evals", [sys.executable, "scripts/evaluate_scenarios.py"]),
    ]
    for identifier, command in checks:
        failure = run(identifier, command)
        if failure:
            print("AGENTS DEVKITS GATE: FAIL")
            print(f"failed check: {failure[0]}")
            if failure[1]:
                print(failure[1], file=sys.stderr)
            return 1
    print("AGENTS DEVKITS GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
