#!/usr/bin/env python3
"""Household transport tests; no production Valid or parity claim."""

import argparse
import datetime
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import facts as f
from harness import runtime

EVIDENCE = None


def fixtures():
    return json.loads((ROOT / "Interface/fixtures/household_wire.json").read_text())["cases"]


def registry_household():
    args = {"Term": f.Term("atom", "event"), "Pat": f.Pat("wild", 7), "Int": -17, "Day": -1}
    return f.Household(
        tuple(f.Fact(name, tuple(args[k] for k in kinds)) for name, kinds in f.FACT_TYPES.items()),
        tuple(f.Stip(name, tuple(f.Pat("val", f.Term("int", i)) for i in range(arity)))
              for name, (_, arity) in f.STIP_SIGNATURES.items()))


class TransportTests(unittest.TestCase):
    def test_shared_fixture_bytes_and_inverse(self):
        for case in fixtures():
            with self.subTest(case=case["name"]):
                value = f.from_value(case["household"])
                self.assertEqual(f.encode(value), case["wire"].encode("utf-8"))
                self.assertEqual(f.decode(f.encode(value)), value)
                self.assertEqual(f.to_value(value), case["household"])

    def test_declared_registries(self):
        text = (ROOT / "Interface/HOUSEHOLD_WIRE.md").read_text()
        fact_text, stip_text = text.split("## Fact registry:")[1].split("## Stipulation registry:")
        actual = {}
        for ctor, name, arity, args in re.findall(r"\| `([^`]+)` \| `([^`]+)/([0-9]+)` \| `([^`]+)` \|", fact_text):
            kinds = tuple(re.findall(r": (Term|Pat|Int|Day)", args))
            self.assertEqual(ctor, name)
            self.assertEqual(int(arity), len(kinds))
            actual[ctor] = kinds
        self.assertEqual(actual, f.FACT_TYPES)
        self.assertEqual(len(actual), 57)
        stips = {ctor: (name, int(arity)) for ctor, name, arity, _ in
                 re.findall(r"\| `([^`]+)` \| `([^`]+)/([0-9]+)` \| ([0-9]+) \|", stip_text)}
        self.assertEqual(stips, f.STIP_SIGNATURES)
        self.assertEqual(len(stips), 31)

    def test_all_constructors_round_trip(self):
        h = registry_household()
        self.assertEqual(f.decode(f.encode(h)), h)

    def test_no_interpreter_decimal_digit_cap(self):
        big = 10**5000 + 17
        h = f.Household((f.Fact("amount_", (f.Term("int", big), -big)),
                         f.Fact("purpose_", (f.Pat("wild", big), f.Term("str", "x")))), ())
        wire = f.encode(h)
        self.assertEqual(f.decode(wire), h)
        self.assertIn(("1" + "0" * 4998 + "17").encode(), wire)
        self.assertIn("_KMLA_W1" + "0" * 4998 + "17", f.emit_prolog(h))
        self.assertIn("KMLA.Pat.wild 1" + "0" * 4998 + "17", f.emit_lean(h))

    def test_admitted_dates_against_standard_calendar(self):
        first, last = datetime.date(1900, 1, 1), datetime.date(2100, 12, 31)
        epoch = datetime.date(1970, 1, 1)
        count = (last - first).days + 1
        self.assertEqual(count, 73414)
        for i in range(count):
            d = first + datetime.timedelta(days=i)
            n = (d - epoch).days
            self.assertEqual(f.day_from_iso(d.isoformat()), n)
            self.assertEqual(f.day_to_iso(n), d.isoformat())

    def test_transport_does_not_apply_v3(self):
        for text in ("1899-12-31", "2101-01-01"):
            self.assertEqual(f.day_to_iso(f.day_from_iso(text)), text)

    def test_dates_not_normalized(self):
        for text in ("1900-02-29", "2017-02-30", "2017-1-1", "2000-00-01", "2000-01-00", "x"):
            with self.subTest(text=text), self.assertRaises(f.TransportError):
                f.day_from_iso(text)

    def test_lossless_stip_list_separate_from_arity(self):
        h = f.Household((), (f.Stip("s63_3", (f.Pat("wild", 17),)),))
        self.assertFalse(h.stipulations[0].well_formed)
        self.assertEqual(f.decode(f.encode(h)), h)
        self.assertIn("KMLA.StipPred.s63_3", f.emit_lean(h))
        with self.assertRaises(f.TransportError):
            f.emit_prolog(h)

    def test_rejects_malformed_shapes_without_defaults(self):
        cases = [None, {}, {"facts": []}, {"facts": [], "stipulations": [], "extra": None},
                 {"facts": None, "stipulations": []},
                 {"facts": [{"ctor": "nope", "args": []}], "stipulations": []},
                 {"facts": [{"ctor": "patient_", "args": []}], "stipulations": []},
                 {"facts": [{"ctor": "birth_", "args": [True]}], "stipulations": []},
                 {"facts": [{"ctor": "birth_", "args": [{"a": "x", "s": "x"}]}], "stipulations": []},
                 {"facts": [{"ctor": "purpose_", "args": [{"wild": -1}, {"s": "x"}]}], "stipulations": []},
                 {"facts": [{"ctor": "purpose_", "args": [{"wild": True}, {"s": "x"}]}], "stipulations": []}]
        for value in cases:
            with self.subTest(value=value), self.assertRaises(f.TransportError):
                f.from_value(value)

    def test_rejects_ambiguous_or_noninteger_json(self):
        for text in ('{"facts":[],"facts":[],"stipulations":[]}',
                     '{"facts":[],"stipulations":[],"ignored":1e0}',
                     '{"facts":[],"stipulations":[],"ignored":NaN}',
                     '{"facts":[{"ctor":"birth_","args":[1.0]}],"stipulations":[]}',
                     '\ufeff{"facts":[],"stipulations":[]}',
                     '{"facts":[],"stipulations":[]} trailing',
                     '{"facts":[{"ctor":"birth_","args":[{"a":"\\ud800"}]}],"stipulations":[]}'):
            with self.subTest(text=text), self.assertRaises(f.TransportError):
                f.decode(text)

    def test_tags_order_duplicates_and_wild_ids_matter(self):
        h = f.from_value(fixtures()[1]["household"])
        self.assertNotEqual(h.facts[0], h.facts[1])
        self.assertEqual(h.facts[0], h.facts[2])
        self.assertEqual(len(h.facts), 7)
        w = f.from_value(fixtures()[4]["household"])
        self.assertEqual(w.stipulations[0], w.stipulations[2])
        self.assertNotEqual(w.stipulations[0], w.stipulations[1])
        self.assertIn("_KMLA_W9007199254740993", f.emit_prolog(w))

    def test_lean_compiles_all_fixtures_and_constructors(self):
        # An independently written TEST observer of the emitted value, confined
        # to this lane. Compare all fields and exact integer/code-point values.
        cases = [f.from_value(c["household"]) for c in fixtures()] + [registry_household()]
        code = (ROOT / "Interface/Household.lean").read_text() + '\n'
        code += '''
def testText (s : String) : String :=
  "[" ++ String.intercalate "," (s.toList.map (fun c => toString c.toNat)) ++ "]"
def testTerm : KMLA.Term → String
  | .atom s => "a" ++ testText s
  | .str s => "s" ++ testText s
  | .int n => "i" ++ toString n
def testPat : KMLA.Pat → String
  | .val t => "v" ++ testTerm t
  | .wild n => "w" ++ toString n
def testFact : KMLA.Fact → String
'''
        for name, kinds in f.FACT_TYPES.items():
            args = [f"a{i}" for i in range(len(kinds))]
            values = [("testTerm " if k == "Term" else "testPat " if k == "Pat" else "toString ") + a
                      for k, a in zip(kinds, args)]
            code += f'  | .{name} {" ".join(args)} => "{name}(" ++ String.intercalate "," [{", ".join(values)}] ++ ")"\n'
        code += 'def testPred : KMLA.StipPred → String\n'
        for name in f.STIP_SIGNATURES:
            code += f'  | .{name} => "{name}"\n'
        code += '''def testStip (s : KMLA.Stip) : String :=
  testPred s.pred ++ "(" ++ String.intercalate "," (s.args.map testPat) ++ ")"
def testHousehold (h : KMLA.Household) : String :=
  String.intercalate ";" (h.facts.map testFact) ++ "|" ++ String.intercalate ";" (h.stipulations.map testStip)
def main : IO Unit := do
'''
        for h in cases:
            code += f"  IO.println (testHousehold {f.emit_lean(h)})\n"
        def term(t):
            return "i" + str(t.value) if t.tag == "int" else ("a" if t.tag == "atom" else "s") + json.dumps(list(map(ord, t.value)), separators=(",", ":"))
        def pat(p):
            return "w" + str(p.value) if p.tag == "wild" else "v" + term(p.value)
        expected = []
        for h in cases:
            fact_rows = [v.ctor + "(" + ",".join(term(a) if k == "Term" else pat(a) if k == "Pat" else str(a)
                         for k, a in zip(f.FACT_TYPES[v.ctor], v.args)) + ")" for v in h.facts]
            stip_rows = [s.pred + "(" + ",".join(map(pat, s.args)) + ")" for s in h.stipulations]
            expected.append(";".join(fact_rows) + "|" + ";".join(stip_rows))
        with tempfile.TemporaryDirectory(prefix="kmla-facts-lean-") as directory:
            path = Path(directory)
            (path / "lean-toolchain").write_text((ROOT / "lean-toolchain").read_text())
            (path / "Transport.lean").write_text(code)
            result = subprocess.run(["lean", "--run", "Transport.lean"], cwd=path,
                                    capture_output=True, text=True, timeout=60)
        if EVIDENCE:
            (EVIDENCE / "Transport.lean").write_text(code)
            (EVIDENCE / "lean.stdout").write_text(result.stdout)
            (EVIDENCE / "lean.stderr").write_text(result.stderr)
            runtime.write_json(EVIDENCE / "lean.json", {
                "argv": ["lean", "--run", "Transport.lean"], "exit": result.returncode,
                "toolchain": (ROOT / "lean-toolchain").read_text().strip(),
                "interface_sha256": runtime.sha256(ROOT / "Interface/Household.lean"),
                "fixture_sha256": runtime.sha256(ROOT / "Interface/fixtures/household_wire.json"),
                "facts_py_sha256": runtime.sha256(ROOT / "harness/facts.py"),
                "scope": "evaluated emitted data; no Valid, H4 grounding, kernel theorem or parity",
            })
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.splitlines(), expected)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--evidence", type=Path)
    opts, rest = parser.parse_known_args()
    if opts.evidence:
        EVIDENCE = runtime.output_path(opts.evidence)
        EVIDENCE.mkdir(parents=True)
        log = io.StringIO()
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(TransportTests))
        report = log.getvalue()
        (EVIDENCE / "tests.txt").write_text(report)
        print(report, end="")
        raise SystemExit(not result.wasSuccessful())
    unittest.main(argv=[sys.argv[0], *rest])
