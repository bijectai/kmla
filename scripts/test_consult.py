#!/usr/bin/env python3
"""Offline wrapper checks in temporary repos; never invokes the real Claude CLI."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SESSION = "11111111-2222-4333-8444-555555555555"
OTHER_SESSION = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
FAKE_CLI = r'''
import json, os, pathlib, re, sys
args = sys.argv[1:]
pathlib.Path("last-call.json").write_text(json.dumps(args))
mode = os.environ.get("CONSULT_TEST_MODE", "success")
if mode == "bad-json":
    print("not JSON")
    raise SystemExit(0)
prompt = args[args.index("-p") + 1]
answer = re.search(r"Write your answer to (docs/consult/A-\d{3}\.md)", prompt)[1]
if mode not in {"no-answer", "cli-error"}:
    pathlib.Path(answer).write_text("Offline fixture answer.\n")
value = {"type": "result", "subtype": "success", "is_error": False,
         "result": answer, "session_id": os.environ["CONSULT_TEST_SESSION"]}
if mode == "no-session":
    del value["session_id"]
if mode in {"error-json", "cli-error"}:
    value.update(is_error=True, subtype="error_during_execution")
print(json.dumps(value))
raise SystemExit(7 if mode == "cli-error" else 0)
'''


class ConsultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kmla-consult-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.consult = self.root / "docs/consult"
        self.consult.mkdir(parents=True)
        (self.root / "scripts").mkdir()
        (self.root / "bin").mkdir()
        shutil.copyfile(REPO / "scripts/consult.sh", self.root / "scripts/consult.sh")
        # Copy Dev's real prompt unchanged; do not author a substitute prompt.
        shutil.copyfile(REPO / "docs/consult/FABLE_PROMPT.md", self.consult / "FABLE_PROMPT.md")
        fake = self.root / "bin/claude"
        fake.write_text("#!" + sys.executable + "\n" + FAKE_CLI)
        fake.chmod(0o700)
        self.env = dict(os.environ, PATH=str(fake.parent) + os.pathsep + os.environ["PATH"],
                        TMPDIR=str(self.root), CONSULT_TEST_SESSION=SESSION)
        self.question(1)

    def question(self, number):
        path = f"docs/consult/Q-{number:03d}.md"
        (self.root / path).write_text("Offline transport fixture, not a design consultation.\n")
        return path

    def run_consult(self, *args, mode="success", session=SESSION, cwd=None):
        env = dict(self.env, CONSULT_TEST_MODE=mode, CONSULT_TEST_SESSION=session)
        return subprocess.run(
            ["bash", str(self.root / "scripts/consult.sh"), *args],
            cwd=cwd or self.root, env=env, capture_output=True, text=True,
        )

    def assert_failure(self, result, message):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertFalse((self.consult / ".fable_session.lock").exists())

    def test_fresh_session_and_exact_tool_boundary(self):
        result = self.run_consult("docs/consult/Q-001.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Offline fixture answer.\n")
        saved = self.consult / ".fable_session"
        self.assertEqual(saved.read_text(), SESSION + "\n")
        self.assertEqual(saved.stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.consult / "A-001.md").stat().st_mode & 0o222, 0)
        args = json.loads((self.root / "last-call.json").read_text())
        for flag in ("--tools", "--allowedTools"):
            self.assertEqual(args[args.index(flag) + 1], "Read,Glob,Grep,Write,Edit")
        self.assertEqual(args[args.index("--permission-mode") + 1], "acceptEdits")
        self.assertEqual(args[args.index("--output-format") + 1], "json")
        self.assertEqual(args[args.index("--disallowedTools") + 1], "Bash,mcp__*")
        self.assertIn("--strict-mcp-config", args)
        self.assertIn("--disable-slash-commands", args)
        self.assertEqual(json.loads(args[args.index("--mcp-config") + 1]), {"mcpServers": {}})
        self.assertEqual(args[args.index("--append-system-prompt") + 1],
                         (self.consult / "FABLE_PROMPT.md").read_text().rstrip("\n"))
        self.assertNotIn("--resume", args)
        self.assertFalse((self.consult / ".fable_session.lock").exists())

    def test_resume_keeps_id_and_prior_answer(self):
        self.assertEqual(self.run_consult("docs/consult/Q-001.md").returncode, 0)
        old_answer = (self.consult / "A-001.md").read_bytes()
        result = self.run_consult(self.question(2))
        self.assertEqual(result.returncode, 0, result.stderr)
        args = json.loads((self.root / "last-call.json").read_text())
        self.assertEqual(args[args.index("--resume") + 1], SESSION)
        self.assertEqual((self.consult / ".fable_session").read_text(), SESSION + "\n")
        self.assertEqual((self.consult / "A-001.md").read_bytes(), old_answer)

    def test_existing_answer_is_not_reused(self):
        self.assertEqual(self.run_consult("docs/consult/Q-001.md").returncode, 0)
        before = (self.root / "last-call.json").read_bytes()
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "answer already exists")
        self.assertEqual((self.root / "last-call.json").read_bytes(), before)

    def test_missing_answer_fails_even_on_success_json(self):
        self.assert_failure(self.run_consult("docs/consult/Q-001.md", mode="no-answer"),
                            "answer was not created")
        self.assertFalse((self.consult / ".fable_session").exists())

    def test_missing_session_warns_but_returns_answer(self):
        result = self.run_consult("docs/consult/Q-001.md", mode="no-session")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("warning: session_id missing", result.stderr)
        self.assertEqual(result.stdout, "Offline fixture answer.\n")
        self.assertFalse((self.consult / ".fable_session").exists())

    def test_missing_session_on_resume_preserves_previous_id(self):
        self.assertEqual(self.run_consult("docs/consult/Q-001.md").returncode, 0)
        result = self.run_consult(self.question(2), mode="no-session")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("warning: session_id missing", result.stderr)
        self.assertEqual((self.consult / ".fable_session").read_text(), SESSION + "\n")

    def test_malformed_saved_id_stops_before_cli(self):
        (self.consult / ".fable_session").write_text("not-a-session-id\n")
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "saved session id")
        self.assertFalse((self.root / "last-call.json").exists())

    def test_existing_lock_is_preserved_and_stops_before_cli(self):
        lock = self.consult / ".fable_session.lock"
        lock.mkdir()
        result = self.run_consult("docs/consult/Q-001.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("another consult is active", result.stderr)
        self.assertTrue(lock.is_dir())
        self.assertFalse((self.root / "last-call.json").exists())

    def test_changed_resume_id_fails_without_replacing_saved_id(self):
        self.assertEqual(self.run_consult("docs/consult/Q-001.md").returncode, 0)
        result = self.run_consult(self.question(2), session=OTHER_SESSION)
        self.assert_failure(result, "different session id")
        self.assertEqual((self.consult / ".fable_session").read_text(), SESSION + "\n")

    def test_cli_error_is_propagated(self):
        result = self.run_consult("docs/consult/Q-001.md", mode="cli-error")
        self.assert_failure(result, "claude exited 7")
        self.assertEqual(result.returncode, 7)
        self.assertIn("answer was not created", result.stderr)

    def test_malformed_and_error_json_fail(self):
        for mode, message in (("bad-json", "invalid CLI JSON"),
                              ("error-json", "failed or unexpected result")):
            with self.subTest(mode=mode):
                self.assert_failure(self.run_consult("docs/consult/Q-001.md", mode=mode), message)

    def test_missing_prompt_stops_before_cli(self):
        (self.consult / "FABLE_PROMPT.md").unlink()
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "FABLE_PROMPT.md not installed")
        self.assertFalse((self.root / "last-call.json").exists())

    def test_invalid_paths_and_usage_stop_before_cli(self):
        for args in ((), ("docs/consult/Q-000.md",), ("../Q-001.md",),
                     ("docs/consult/Q-001.md;false",)):
            with self.subTest(args=args):
                self.assertNotEqual(self.run_consult(*args).returncode, 0)
        self.assertFalse((self.root / "last-call.json").exists())

    def test_answer_symlink_is_rejected(self):
        (self.consult / "A-001.md").symlink_to(self.root / "missing-target")
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "answer already exists")
        self.assertFalse((self.root / "last-call.json").exists())

    def test_other_working_directory(self):
        result = self.run_consult("docs/consult/Q-001.md", cwd=self.root.parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.consult / ".fable_session").read_text(), SESSION + "\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
