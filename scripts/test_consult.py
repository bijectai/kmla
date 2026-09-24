#!/usr/bin/env python3
"""Offline governor-queue checks; no real model or protected artifact is used.

P-ROLES removes (not skips) obsolete Claude spawn/tool-flag, JSON/session-id,
resume/lock, and FABLE_PROMPT-installation tests. Those tested the retired
subprocess channel; its historical smoke evidence and Git history are retained.
The replacement contract is read-only awaiting/delivery, never self-consultation.
"""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


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
        # Any accidental attempt to launch a model is observable and forbidden.
        fake = self.root / "bin/claude"
        fake.write_text("#!/bin/sh\nprintf 'spawned' > \"$CONSULT_SPAWN_MARKER\"\nexit 99\n")
        fake.chmod(0o700)
        self.env = dict(os.environ, PATH=str(fake.parent) + os.pathsep + os.environ["PATH"],
                        CONSULT_SPAWN_MARKER=str(self.root / "spawned"))
        self.question(1)

    def question(self, number):
        path = f"docs/consult/Q-{number:03d}.md"
        (self.root / path).write_text(
            f"# Q-{number:03d}\n\n## Phase\nInfra\n\n## Lane\ninfra\n\n"
            "## Question\nOffline queue fixture, not a design consultation.\n\n"
            "## What was tried\nNone.\n\n## Files involved\nNone.\n\n"
            "## Proposed answer\nNone.\n"
        )
        return path

    def answer(self, number=1):
        path = self.consult / f"A-{number:03d}.md"
        path.write_text(
            f"# A-{number:03d}\n\n## Answer\nOffline delivery fixture.\n\n"
            "## Rationale\nTransport test only.\n\n## Contract change\nNo.\n\n"
            "## Escalate to Dev\nNo.\n\n## Self-review\nNo semantic assumptions.\n"
        )
        path.chmod(0o444)
        return path

    def snapshot(self):
        result = {}
        for path in self.root.rglob("*"):
            rel = str(path.relative_to(self.root))
            if path.is_symlink():
                result[rel] = ("link", os.readlink(path))
            elif path.is_file():
                result[rel] = ("file", path.read_bytes(), path.stat().st_mode & 0o777)
            else:
                result[rel] = ("directory",)
        return result

    def run_consult(self, *args, cwd=None):
        before = self.snapshot()
        result = subprocess.run(
            ["bash", str(self.root / "scripts/consult.sh"), *args],
            cwd=cwd or self.root, env=self.env, capture_output=True, text=True,
        )
        self.assertEqual(self.snapshot(), before, "consult changed repository paths")
        self.assertFalse((self.root / "spawned").exists(), "consult spawned Claude")
        return result

    def assert_failure(self, result, message, status=2):
        self.assertEqual(result.returncode, status, result.stderr)
        self.assertIn(message, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_unanswered_question_halts_without_creating_answer_or_session(self):
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"),
                            "awaiting the governor", status=1)
        self.assertFalse((self.consult / "A-001.md").exists())
        self.assertFalse((self.consult / ".fable_session").exists())

    def test_repeated_poll_is_same_question_not_new_number(self):
        for _ in range(2):
            self.assert_failure(self.run_consult("docs/consult/Q-001.md"),
                                "awaiting the governor", status=1)

    def test_existing_answer_delivered_unchanged_repeatedly(self):
        answer = self.answer()
        for _ in range(2):
            result = self.run_consult("docs/consult/Q-001.md")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, answer.read_text())
            self.assertIn("check escalation", result.stderr)
        self.assertEqual(answer.stat().st_mode & 0o222, 0)

    def test_only_matching_answer_satisfies_question(self):
        self.answer()
        self.assert_failure(self.run_consult(self.question(2)),
                            "awaiting the governor", status=1)

    def test_old_session_lock_and_missing_prompt_are_irrelevant(self):
        (self.consult / ".fable_session").write_text("historical-id\n")
        (self.consult / ".fable_session.lock").mkdir()
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"),
                            "awaiting the governor", status=1)
        self.answer()
        self.assertEqual(self.run_consult("docs/consult/Q-001.md").returncode, 0)

    def test_usage_and_number_grammar(self):
        for args in ((), ("docs/consult/Q-001.md", "extra"),
                     ("docs/consult/Q-000.md",), ("../Q-001.md",),
                     ("docs/consult/Q-01.md",), ("docs/consult/Q-1000.md",),
                     ("docs/consult/Q-abc.md",), ("docs/consult/Q-001.md;false",),
                     ("docs/consult/A-001.md",), ("docs/consult/Q-００１.md",)):
            with self.subTest(args=args):
                self.assertEqual(self.run_consult(*args).returncode, 2)
        self.assert_failure(self.run_consult(self.question(999)),
                            "awaiting the governor", status=1)

    def test_missing_empty_and_directory_questions_rejected(self):
        self.assert_failure(self.run_consult("docs/consult/Q-002.md"), "question is missing")
        question = self.consult / "Q-001.md"
        question.write_text("")
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "question is missing")
        question.unlink()
        question.mkdir()
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "question is missing")

    def test_question_symlink_rejected(self):
        (self.consult / "Q-002.md").symlink_to(self.consult / "Q-001.md")
        self.assert_failure(self.run_consult("docs/consult/Q-002.md"), "question is missing")

    def test_answer_symlinks_rejected_even_dangling(self):
        path = self.consult / "A-001.md"
        path.symlink_to(self.root / "missing")
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "answer must not")
        path.unlink()
        path.symlink_to(self.consult / "Q-001.md")
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "answer must not")

    def test_empty_or_directory_answer_rejected(self):
        path = self.consult / "A-001.md"
        path.write_text("")
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "nonempty regular file")
        path.unlink()
        path.mkdir()
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "nonempty regular file")

    def test_symlinked_consult_directory_rejected(self):
        self.consult.rename(self.root / "moved-consult")
        self.consult.symlink_to(self.root / "moved-consult", target_is_directory=True)
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "directories must not")

    def test_symlinked_docs_directory_rejected(self):
        docs = self.root / "docs"
        docs.rename(self.root / "moved-docs")
        docs.symlink_to(self.root / "moved-docs", target_is_directory=True)
        self.assert_failure(self.run_consult("docs/consult/Q-001.md"), "directories must not")

    def test_other_working_directory(self):
        answer = self.answer()
        result = self.run_consult("docs/consult/Q-001.md", cwd=self.root.parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, answer.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
