#!/usr/bin/env python3
"""Validate the canonical v2 skill routing contract."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_manifest import ManifestError  # noqa: E402
from platform import validate_skill_registry  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        validate_skill_registry(ROOT / "skills/registry.yaml", ROOT, ROOT / "capabilities/registry.yaml")
        print("Skill registry valid")
        return 0
    except (ManifestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
