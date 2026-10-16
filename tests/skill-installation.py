#!/usr/bin/env python3
"""Exercise installation with and without native symlink support."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash") or "bash"


class InstallationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="agents-devkits installer ")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.repo = self.directory / "repo with spaces"
        self.home = self.directory / "home with spaces"
        self.repo.mkdir()
        (self.repo / "scripts").mkdir()
        for relative in ("bootstrap.sh", "scripts/install.sh", "scripts/relocate_skill_links.py"):
            if (ROOT / relative).exists():
                shutil.copyfile(ROOT / relative, self.repo / relative)
                (self.repo / relative).chmod(0o755)
        self.source = self.repo / "skills/demo"
        (self.source / "references").mkdir(parents=True)
        (self.source / "references/local.md").write_text("Local reference\n", encoding="utf-8")
        (self.repo / "docs").mkdir()
        (self.repo / "docs/guide.md").write_text("# Section\n", encoding="utf-8")
        self.original = (
            "---\nname: demo\ndescription: Installation fixture.\n---\n"
            "[Guide](../../docs/guide.md#section)\n"
            "[Local](references/local.md)\n"
            "[Remote](https://example.com/guide)\n[Anchor](#section)\n"
        )
        (self.source / "SKILL.md").write_text(self.original, encoding="utf-8")
        self.environment = os.environ.copy()
        self.environment["HOME"] = self.home.as_posix()

    def fake_command(self, name: str, body: str) -> None:
        binaries = self.directory / "bin"
        binaries.mkdir()
        command = binaries / name
        command.write_text("#!/usr/bin/env bash\nset -euo pipefail\n" + body + "\n", encoding="utf-8")
        command.chmod(0o755)
        self.environment["PATH"] = str(binaries) + os.pathsep + self.environment["PATH"]

    def install(self, *arguments: str) -> str:
        result = subprocess.run(
            [BASH, (self.repo / "bootstrap.sh").as_posix(), *arguments],
            env=self.environment, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def assert_copy(self, agent: str = "codex") -> None:
        target = self.home / f".{agent}/skills/demo"
        self.assertFalse(target.is_symlink())
        content = (target / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(f"[Guide](<{(self.repo / 'docs/guide.md').resolve().as_posix()}#section>)", content)
        self.assertIn("[Local](references/local.md)", content)
        self.assertIn("[Remote](https://example.com/guide)", content)
        self.assertIn("[Anchor](#section)", content)
        self.assertEqual((self.source / "SKILL.md").read_text(encoding="utf-8"), self.original)

    def test_silent_ln_copy_is_reported_and_relocated(self) -> None:
        self.fake_command("ln", 'cp -a "$2" "$3"')
        output = self.install()
        self.assertIn("linked=0 copied=2", output)
        self.assert_copy()
        self.assert_copy("claude")

    def test_link_failure_falls_back_to_a_usable_copy(self) -> None:
        self.fake_command("ln", "exit 1")
        output = self.install()
        self.assertIn("linked=0 copied=2", output)
        self.assert_copy()

    def test_codex_only_copy_preserves_claude_and_existing_skills(self) -> None:
        sentinel = self.home / ".codex/skills/.system/sentinel"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_text("keep", encoding="utf-8")
        output = self.install("--copy-codex", "--agent", "codex")
        self.assertIn("linked=0 copied=1", output)
        self.assertFalse((self.home / ".claude").exists())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assert_copy()
        (self.home / ".codex/skills/demo/sentinel").write_text("user change", encoding="utf-8")
        output = self.install("--copy-codex", "--agent", "codex")
        self.assertIn("skipped=1", output)
        self.assertTrue((self.home / ".codex/skills/demo/sentinel").is_file())

    def test_adopt_keeps_a_recoverable_backup(self) -> None:
        target = self.home / ".codex/skills/demo"
        target.mkdir(parents=True)
        (target / "sentinel").write_text("original", encoding="utf-8")
        output = self.install("--copy-codex", "--agent", "codex", "--adopt")
        self.assertIn("backed-up=1", output)
        self.assert_copy()
        backups = list((self.home / ".agent-skills-backups").glob("*/.codex/demo/sentinel"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "original")
        self.install("--copy-codex", "--agent", "codex", "--adopt")
        self.assertEqual(len(list((self.home / ".agent-skills-backups").iterdir())), 2)

    def test_unusable_python3_alias_uses_working_python(self) -> None:
        self.fake_command("python3", "exit 1")
        self.install("--copy-codex", "--agent", "codex")
        self.assert_copy()
        result = subprocess.run(
            [BASH, (ROOT / "project.sh").as_posix(), "--help"],
            env=self.environment, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("usage:", result.stdout)

    def test_invalid_agent_is_rejected_before_installation(self) -> None:
        result = subprocess.run(
            [BASH, (self.repo / "bootstrap.sh").as_posix(), "--agent", "unknown"],
            env=self.environment, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.home.exists())

    def test_native_links_remain_idempotent_when_available(self) -> None:
        try:
            (self.directory / "probe").symlink_to(self.source, target_is_directory=True)
        except OSError:
            self.skipTest("Native symlink creation is unavailable to this process")
        self.environment["MSYS"] = "winsymlinks:nativestrict"
        output = self.install()
        self.assertIn("linked=2 copied=0", output)
        self.assertTrue((self.home / ".codex/skills/demo").is_symlink())
        output = self.install()
        self.assertIn("already-linked=2", output)
        output = self.install("--copy-codex", "--agent", "codex")
        self.assertIn("migrated=1", output)
        self.assert_copy()
        self.assertTrue((self.home / ".claude/skills/demo").is_symlink())


if __name__ == "__main__":
    unittest.main()
