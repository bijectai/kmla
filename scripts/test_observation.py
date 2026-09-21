#!/usr/bin/env python3
"""Black-box JSON checks for the shared Lean observation encoder, not parity."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def lean_string(text):
    """Construct a string without assuming Lean and JSON share escape syntax."""
    return "String.ofList [" + ", ".join(f"Char.ofNat {ord(c)}" for c in text) + "]"


class ObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="kmla-observation-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.directory = Path(cls.tmp.name)
        (cls.directory / "Interface").mkdir()
        # Running in ROOT selects the committed toolchain instead of elan's default.
        compiled = subprocess.run(
            ["lean", "-o", str(cls.directory / "Interface/Household.olean"),
             "Interface/Household.lean"], cwd=ROOT, capture_output=True, text=True,
            timeout=120, check=False,
        )
        if compiled.returncode:
            raise AssertionError(compiled.stdout + compiled.stderr)

    def evaluate(self, expressions):
        source = self.directory / "Probe.lean"
        source.write_text(
            "import Interface.Household\nopen KMLA\ndef main : IO Unit := do\n"
            + "".join(f"  IO.println ({expression})\n" for expression in expressions),
            encoding="utf-8",
        )
        env = dict(os.environ, LEAN_PATH=str(self.directory))
        result = subprocess.run(
            ["lean", "--run", str(source)], cwd=ROOT, env=env,
            capture_output=True, text=True, timeout=120, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_all_control_characters_round_trip_as_json(self):
        value = "prefix" + "".join(chr(n) for n in range(32)) + "suffix"
        output = self.evaluate([f"Obs.encode (.atom ({lean_string(value)}))"])
        # Only the print terminator may be a literal control character in this JSON.
        self.assertTrue(output.endswith("\n"))
        self.assertTrue(all(ord(c) >= 32 for c in output[:-1]), repr(output))
        self.assertEqual(json.loads(output), {"a": value})

    def test_existing_tags_unicode_and_numeric_precision(self):
        value = 'quote" backslash\\ café Ελληνικά 🙂'
        rows = self.evaluate([
            "Obs.encode .null",
            "Obs.encode (.num (-9007199254740993))",
            f"Obs.encode (.atom ({lean_string(value)}))",
            f"Obs.encode (.str ({lean_string(value)}))",
            "Obs.encode (.day 0)",
            'Obs.encode (.arr [.num 1, .str "usa", .atom "usa", .null])',
        ]).splitlines()
        self.assertEqual(len(rows), 6)
        self.assertEqual([json.loads(row) for row in rows], [
            None, -9007199254740993, {"a": value}, {"s": value}, "1970-01-01",
            [1, {"s": "usa"}, {"a": "usa"}, None],
        ])
        self.assertEqual(rows[1], "-9007199254740993")
        self.assertEqual(rows[5], '[1,{"s":"usa"},{"a":"usa"},null]')

    def test_solution_set_sorts_and_deduplicates_encoded_tuples(self):
        output = self.evaluate([
            '"[" ++ String.intercalate "," (observe '
            '[[.num 2], [.num 10], [.num 2], [.atom "usa"], [.str "usa"]]) ++ "]"',
        ])
        rows = json.loads(output)
        self.assertEqual(rows, [[10], [2], [{"a": "usa"}], [{"s": "usa"}]])
        self.assertEqual(output, '[[10],[2],[{"a":"usa"}],[{"s":"usa"}]]\n')


if __name__ == "__main__":
    unittest.main(verbosity=2)
