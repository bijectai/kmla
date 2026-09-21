#!/usr/bin/env python3
"""Regression checks for launching the staged stub, never an owner meter.

These are builder CLI tests, not additional parity fixtures or a comparator.
"""
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import parity_conformance as suite


class InvocationTests(unittest.TestCase):
    def test_relative_path_invokes_the_real_staged_stub(self):
        root = Path(__file__).resolve().parents[1]
        stub = root / "docs/contracts/parity/check.py"
        relative = Path("docs/contracts/parity/check.py")
        case = next(c for c in suite.build_cases()
                    if c.name == "empty-input-population")
        original_run = subprocess.run
        calls = []

        def observe(*args, **kwargs):
            result = original_run(*args, **kwargs)
            calls.append((args[0], result))
            return result

        self.assertEqual(Path.cwd(), root, "run this test from the repo root")
        with tempfile.TemporaryDirectory() as work:
            with patch.object(suite.subprocess, "run", side_effect=observe):
                ok, detail = suite.run_case(relative, case, Path(work))
        self.assertTrue(ok, detail)
        self.assertEqual(calls[0][0][2], str(stub))
        self.assertIn("unimplemented", calls[0][1].stderr)
        self.assertNotIn("can't open file", calls[0][1].stderr)

    def test_file_open_failure_is_not_a_passing_exit_two_fixture(self):
        stub = Path("docs/contracts/parity/check.py").resolve()
        case = next(c for c in suite.build_cases()
                    if c.name == "empty-input-population")
        failed = subprocess.CompletedProcess([], 2, "",
            f"python: can't open file '{stub}': [Errno 2] No such file or directory\n")
        with tempfile.TemporaryDirectory() as work:
            with patch.object(suite.subprocess, "run", return_value=failed):
                with self.assertRaisesRegex(suite.InvocationError, "WRONG-REASON"):
                    suite.run_case(stub, case, Path(work))

    def test_process_launch_failure_is_a_harness_error(self):
        with patch.object(suite.subprocess, "run", side_effect=OSError("launch failed")):
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                code = suite.main(["--meter", "docs/contracts/parity/check.py"])
        self.assertEqual(code, 2)
        self.assertIn("HARNESS ERROR", stderr.getvalue())

    def test_only_owner_authorized_fixture_is_promoted(self):
        cases = suite.build_cases()
        self.assertEqual(len(cases), 20)
        self.assertEqual({c.name for c in cases if c.informational},
                         {"absent-key-is-not-null", "no-number-coercion"})
        invalid = next(c for c in cases if c.name == "invalid-input-id")
        self.assertEqual(invalid.expect_exit, 2)
        self.assertTrue(invalid.expect_stderr)


if __name__ == "__main__":
    unittest.main()
