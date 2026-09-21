#!/usr/bin/env python3
"""Regression tests for phase counters and shell reporting, not an owner meter.

Execute the verifier's actual reporting/counting fragments in isolation. No
protected artifacts are created, inspected or changed by these tests.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("verify_phase0.sh").read_text(encoding="utf-8")
LATER_MARKER = "# Later checkpoint artifacts are visible but not Checkpoint 0 requirements."
SUMMARY_MARKER = "# Checkpoint 0 summary: later artifacts cannot change these counters or exits."
LATER = SCRIPT.split(LATER_MARKER, 1)[1].split(SUMMARY_MARKER, 1)[0]
SUMMARY = SCRIPT.split(SUMMARY_MARKER, 1)[1]
LATER_FUNCTION = re.search(r"(?ms)^report_later\(\) \{.*?^\}", SCRIPT).group()
PENDING_LINES = "\n".join(line for line in SCRIPT.splitlines()
                          if line.startswith("PENDING="))


def bash(fragment, env=None):
    return subprocess.run(["bash", "-u", "-c", fragment], text=True,
                          capture_output=True, timeout=10,
                          env={**os.environ, **(env or {})})


class PendingTests(unittest.TestCase):
    def count(self, text):
        with tempfile.TemporaryDirectory(prefix="kmla-pending-test-") as work:
            root = Path(work)
            (root / "docs").mkdir()
            (root / "docs/DECISION_LOG.md").write_text(text, encoding="utf-8")
            result = bash(PENDING_LINES + '\nprintf "%s" "$PENDING"\n',
                          {"ROOT": str(root)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_no_matches_is_one_zero_not_two(self):
        self.assertEqual(self.count("## 2026-09-21 — ACCEPTED — example\n"), "0")

    def test_empty_log_is_one_zero(self):
        self.assertEqual(self.count(""), "0")

    def test_only_pending_headings_are_counted(self):
        text = ("Historical PENDING text is not a heading.\n"
                "## 2026-09-21 — PENDING — first\n"
                "## 2026-09-21 — ACCEPTED — other\n"
                "## 2026-09-21 — PENDING — second\n")
        self.assertEqual(self.count(text), "2")


class AccountingTests(unittest.TestCase):
    def run_report(self, *, present=False, strict=True, passed=17, failed=0, outstanding=0):
        # Only the presence query is stubbed. Both real later-checkpoint blocks
        # and the actual summary/exit logic execute; no .lean source is opened.
        setup = (f"PASS={passed}\nFAIL={failed}\nSKIP={outstanding}\n"
                 f"STRICT={int(strict)}\nLATER_PRESENT=0\nLATER_OUTSTANDING=0\n"
                 "ROOT=/unused-kmla-fixture\n"
                 f"compgen() {{ return {0 if present else 1}; }}\n")
        result = bash(setup + LATER_FUNCTION + LATER + SUMMARY)
        self.assertEqual(result.stderr, "")
        return result

    def test_later_missing_is_reported_but_does_not_block_strict_phase_zero(self):
        result = self.run_report()
        self.assertEqual(result.returncode, 0)
        self.assertIn("Checkpoint 0: 17 passed, 0 failed, 0 outstanding", result.stdout)
        self.assertIn("-- Checkpoint 2:", result.stdout)
        self.assertIn("-- Checkpoint 3a:", result.stdout)
        self.assertIn("Checkpoint 2 input outstanding", result.stdout)
        self.assertIn("Checkpoint 3a input outstanding", result.stdout)
        self.assertIn("Later checkpoints: 0 artifact group(s) present, 2 outstanding", result.stdout)
        self.assertIn("requires Dev's explicit sign-off", result.stdout)

    def test_later_present_never_inflates_phase_zero_passes(self):
        result = self.run_report(present=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Checkpoint 0: 17 passed, 0 failed, 0 outstanding", result.stdout)
        self.assertIn("Later checkpoints: 2 artifact group(s) present, 0 outstanding", result.stdout)
        self.assertIn("rejection validation is still required at Checkpoint 2", result.stdout)
        self.assertIn("owner signature/review is still required at Checkpoint 3a", result.stdout)

    def test_current_outstanding_still_blocks_strict(self):
        result = self.run_report(outstanding=1)
        self.assertEqual(result.returncode, 1)
        self.assertIn("17 passed, 0 failed, 1 outstanding", result.stdout)
        self.assertIn("--strict: treating outstanding Checkpoint 0 requirements as a failure", result.stdout)

    def test_non_strict_preserves_existing_exit_behavior_without_claiming_clearance(self):
        result = self.run_report(strict=False, outstanding=1)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Checkpoint 0 requires zero failures, zero outstanding", result.stdout)
        self.assertIn("Dev's sign-off", result.stdout)

    def test_mechanical_failure_still_fails_with_either_later_state(self):
        for present in (False, True):
            with self.subTest(later_present=present):
                result = self.run_report(present=present, strict=False, failed=1)
                self.assertEqual(result.returncode, 1)
                self.assertIn("Checkpoint 0 has NOT passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
