#!/usr/bin/env python3
"""Regression checks for project integration and verification."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectRuntimeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="devkits project runtime ")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        profile = root / "profile"
        self.project = root / "project"
        self.project.mkdir()
        self.bin = root / "bin"
        self.bin.mkdir()
        self.env = {
            **os.environ,
            "HOME": str(profile),
            "USERPROFILE": str(profile),
            "PATH": os.pathsep.join((str(self.bin), str(Path(sys.executable).parent), os.environ["PATH"])),
            "PYTHONUTF8": "1",
        }
        for agent in ("codex", "claude"):
            for skill in ("codebase-explorer", "feature-development", "release-check"):
                source = ROOT / "skills" / skill / "SKILL.md"
                target = profile / f".{agent}" / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                shutil.copyfile(source, target)

    def cli(self, command, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(ROOT / "project.py"), command, "--path", str(self.project), *args],
            cwd=self.project, env=self.env, capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def set_check(self, command, args):
        manifest = (ROOT / "templates/project/agents-devkits.yaml").read_text(encoding="utf-8")
        baseline = (
            "  baseline:\n"
            "    - id: fixture\n"
            f"      command: {command}\n"
            f"      args: {json.dumps(args)}"
        )
        (self.project / "agents-devkits.yaml").write_text(
            manifest.replace("  baseline: []", baseline), encoding="utf-8",
        )

    def verify(self, *args, status, code=0):
        result = self.cli("verify", "--json", *args, code=code)
        self.assertEqual(result.stderr, "")
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["status"], status)
        return envelope

    def test_manual_integration_recognizes_current_and_earlier_snippets(self):
        original = "# Existing project instructions\n"
        for filename in ("AGENTS.md", "CLAUDE.md"):
            (self.project / filename).write_text(original, encoding="utf-8")
        self.cli("init")
        self.assertIn("integration state: pending", self.cli("doctor", code=1).stderr)

        pasted_contents = {}
        for agent, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            instruction = self.project / filename
            self.assertEqual(instruction.read_text(encoding="utf-8"), original)
            snippet = (self.project / ".agents-devkits" / f"{agent}-integration.md").read_text(encoding="utf-8")
            marker = f"<!-- agents-devkits:{agent}:start -->"
            self.assertIn(marker, snippet)
            self.assertIn(f"<!-- agents-devkits:{agent}:end -->", snippet)
            if agent == "claude":
                # Simulate projects that copied the body before markers were added.
                block = "\n".join(line for line in snippet[snippet.index(marker):].splitlines() if not line.startswith("<!--"))
            else:
                block = snippet[snippet.index(marker):].strip()
            pasted_contents[filename] = original + "\n" + block + "\n"
            instruction.write_text(pasted_contents[filename], encoding="utf-8")

        self.assertIn("integration state: active", self.cli("doctor").stdout)
        self.cli("init", "--adopt")
        for filename, content in pasted_contents.items():
            self.assertEqual((self.project / filename).read_text(encoding="utf-8"), content)

    def test_strict_verification_distinguishes_missing_checks_pending_reviews_and_pass(self):
        self.cli("init", "--ui")
        self.verify(status="no_checks")
        self.verify("--strict", status="no_checks", code=1)
        changed = ("--changed", "src/ui/button.tsx")
        envelope = self.verify(*changed, status="reviews_pending")
        self.assertEqual(envelope["required_reviews"], ["accessibility-review", "visual-qa"])
        self.verify(*changed, "--strict", status="reviews_pending", code=1)
        self.set_check(Path(sys.executable).name, ["-c", "print('fixture ran')"])
        envelope = self.verify("--strict", status="passed")
        self.assertEqual(envelope["evidence"][0]["output"]["stdout"].strip(), "fixture ran")

    def test_command_launch_failure_keeps_json_evidence(self):
        name = "devkits-broken-check.exe" if os.name == "nt" else "devkits-broken-check"
        broken = self.bin / name
        broken.write_text("#!/nonexistent-devkits-interpreter\n", encoding="utf-8")
        broken.chmod(0o755)
        self.set_check(name, [])
        check = self.verify(status="failed", code=1)["evidence"][0]
        self.assertEqual(check["status"], "unavailable")
        self.assertIn("could not start command", check["reason"])

    @unittest.skipUnless(os.name == "nt", "requires Windows command shims")
    def test_windows_runs_the_resolved_batch_file_with_literal_arguments(self):
        shim = self.bin / "devkits-npm-fixture.cmd"
        shim.write_text("@echo off\necho %~1 %~2\n", encoding="ascii")
        self.set_check(shim.stem, ["run", "named check"])
        check = self.verify("--strict", status="passed")["evidence"][0]
        self.assertEqual(check["output"]["stdout"].strip(), "run named check")

        self.set_check(shim.stem, ["run", "contains &"])
        check = self.verify(status="failed", code=1)["evidence"][0]
        self.assertEqual(check["status"], "unavailable")
        self.assertIn("Windows batch commands", check["reason"])


if __name__ == "__main__":
    unittest.main()
