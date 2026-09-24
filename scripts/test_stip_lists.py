#!/usr/bin/env python3
"""Recursive stipulation transport and bounded pinned H4 regressions.

No production records, admission, Oracle implementation or reference parity.
Runtime tests are opt-in with a fresh --evidence directory; all errors retain
raw streams. Unexpected failures stop this bounded run immediately.
"""
import argparse
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import facts as f, runtime
from harness.case_reader import parse_case, read_case
from harness.grounding import CORPUS, GroundingFailure, GroundingSession
from harness.grounding_observations import paragraph_query
from scripts.test_facts import fixtures
from scripts.test_grounding import compare_observations, observation_plan


def wrapped(arg):
    return {"facts": [], "stipulations": [{"pred": "s63_3", "args": [arg]}]}


class StipListTests(unittest.TestCase):
    def test_distinct_event_and_stipulation_types(self):
        nested = f.StipArg("list", (f.StipArg("wild", 7),))
        for action in (
            lambda: f.Term("list", ()), lambda: f.Pat("list", ()),
            lambda: f.Pat("val", nested),
            lambda: f.Fact("purpose_", (nested, f.Term("str", "x"))),
            lambda: f.StipArg("list", [f.StipArg("wild", 7)]),
            lambda: f.StipArg("list", (f.Pat("wild", 7),)),
            lambda: f.Stip("s63_3", (f.Pat("wild", 7),)),
        ):
            with self.subTest(action=action), self.assertRaises(f.TransportError):
                action()

    def test_strict_recursive_decode(self):
        invalid = ([], None, 0, True, "[]", {"list": None}, {"list": {}},
                   {"list": "[]"}, {"val": []}, {"val": {"list": []}},
                   {"list": [], "wild": 0}, {"list": [], "val": 0},
                   {"list": [None]}, {"list": [1]}, {"list": [[1]]},
                   {"list": [{"wild": -1}]}, {"list": [{"wild": True}]},
                   {"list": [{"wild": 1.0}]}, {"list": [{"val": 1.0}]},
                   {"list": [{"val": {"a": "x", "s": "x"}}]},
                   {"list": [{"list": [{"tail": {"wild": 1}}]}]})
        for arg in invalid:
            with self.subTest(arg=arg), self.assertRaises(f.TransportError):
                f.decode(json.dumps(wrapped(arg)))
        for arg in ('{"list":[],"list":[]}', '{"list":[{"wild":1e0}]}',
                    '{"list":[{"val":NaN}]}', '{"list":[{"val":{"s":"\\ud800"}}]}'):
            with self.subTest(arg=arg), self.assertRaises(f.TransportError):
                f.decode('{"facts":[],"stipulations":[{"pred":"s63_3","args":[' + arg + ']}]}')

    def test_lists_rejected_in_event_positions(self):
        for ctor, args in (("birth_", [{"list": []}]),
                           ("purpose_", [{"list": []}, {"s": "x"}])):
            with self.subTest(ctor=ctor), self.assertRaises(f.TransportError):
                f.from_value({"facts": [{"ctor": ctor, "args": args}], "stipulations": []})

    def test_recursive_aliases_tags_order_and_empty_lists(self):
        value = f.from_value(fixtures()[7]["household"])
        a, nested, b, items, _ = value.stipulations[0].args
        self.assertEqual(a, nested.value[0])
        self.assertEqual(b, nested.value[1])
        self.assertEqual(b, nested.value[2].value[0])
        self.assertNotEqual(a, b)
        self.assertEqual(len(set(items.value[:3])), 3)  # [], atom '[]', string "[]"
        self.assertEqual(items.value[-2], items.value[-1])
        self.assertNotEqual(items.value[3], items.value[4])
        self.assertEqual(items.value[5].value.value, 123456789012345678901234567890)
        self.assertEqual(items.value[6].value.value, -123456789012345678901234567890)
        self.assertEqual(f.decode(f.encode(value)), value)
        self.assertIn("[[],'[]',\"[]\"", f.emit_prolog(value))
        self.assertIn("KMLA.StipArg.list", f.emit_lean(value))

    def test_recursive_large_integer_and_wild_id(self):
        big = 10**5000 + 17
        a = f.StipArg("list", (f.StipArg("wild", big), f.StipArg("val", f.Term("int", -big))))
        value = f.Household((), (f.Stip("s63_3", (a, a, f.StipArg("list", ()))),))
        self.assertEqual(f.decode(f.encode(value)), value)
        self.assertIn("_KMLA_W" + f._decimal(big), f.emit_prolog(value))
        self.assertIn("KMLA.StipArg.wild " + f._decimal(big), f.emit_lean(value))

    def test_original_query_modes_do_not_release_bound_arguments(self):
        alice = paragraph_query(read_case(CORPUS / "cases/s63_d_2_pos.pl"))
        self.assertEqual(alice.mode, "bbb")
        self.assertEqual(alice.original_goal, "s63_d_2(alice,[2000],2017)")
        self.assertEqual(alice.request(), "observation('s63_d_2'('alice',[2000],2017),[]).\n")
        bob = paragraph_query(read_case(CORPUS / "cases/s2_a_1_B_pos.pl"))
        self.assertEqual(bob.mode, "bffb")
        self.assertEqual(bob.outputs, ("Q0", "Q1"))
        for goal in ("s63_d_2(alice,_,2017)", "s2_a_1_B(bob,alice,charlie,2016)",
                     "(s63_d_2(alice,[2000],2017),true)"):
            with self.subTest(goal=goal), self.assertRaises(GroundingFailure):
                paragraph_query(parse_case(("% Test\n:- " + goal + ".\n").encode()))


def checked(condition, description):
    if not condition:
        raise GroundingFailure(description)


def integration(evidence, timeout):
    session = GroundingSession(evidence)
    rows, guards, households = [], [], []
    finding = None
    try:
        for name in ("s2_a_1_B_pos.pl", "s63_d_2_pos.pl"):
            case = read_case(CORPUS / "cases" / name)
            row = {"original_case": name, "source_sha256": case.source.sha256,
                   "h4_3_a": "blocked:not-complete", "h4_3_b": "blocked:not-complete"}
            rows.append(row)
            original = session.original(case, timeout=timeout)
            row["original_measurement"] = original.request
            households.append(f.encode(original.household))
            # Exact heads, separately from agreement with the serialized result.
            expected = deepcopy(fixtures()[6]["household"])
            expected["stipulations"] = expected["stipulations"][:4] if name.startswith("s2_") else expected["stipulations"][4:]
            if name.startswith("s63_"):
                expected["stipulations"][0]["args"][3] = {"wild": 0}
            checked(original.household.stipulations == f.from_value(expected).stipulations,
                    name + ": exact original supplied s151 heads differ")
            row["exact_supplied_heads"] = "pass"
            reground = session.reground(case, original.household, timeout=timeout)
            row["reground_measurement"] = reground.request
            row["h4_3_a"] = "pass" if original.household == reground.household else "fail"
            checked(row["h4_3_a"] == "pass", name + ": H4(a) differs")
            plan = observation_plan(case)
            row["query_plan"] = asdict(plan)
            observed = compare_observations(session, plan, original, reground, name=case.source.name.split("/")[-1], timeout=timeout)
            row["h4_3_b"] = observed["status"]
            row["observations"] = observed
            checked(row["h4_3_b"] == "pass", name + ": H4(b) differs")
            checked(bool(observed["original"]["canonical"]), name + ": positive original observation unexpectedly empty")
            if name.startswith("s63_"):
                checked(observed["original"]["canonical"] == [[]], "s63_d_2 bbb must observe one empty tuple")
            runtime.write_json(session.directory / (Path(name).stem + ".status.json"), row)
            print(name + ": exact heads and both H4 checks PASS", flush=True)

        # Two proofs of the same nested head: findall freshens BETWEEN copies,
        # but shared variables within each nested head retain their identity.
        source = '''s151(X,[X,Y,[Y]],Y,[[], '[]', "[]", usa, "usa",123456789012345678901234567890,-123456789012345678901234567890,dup,dup],2015) :- between(1,2,_).
'''
        measured = session.measure(source, candidate="regular", query="none", name="nested aliases and two proof copies", timeout=timeout)
        template = deepcopy(fixtures()[7]["household"])
        second = deepcopy(template["stipulations"][0])
        def fresh(value):
            if isinstance(value, dict):
                return {k: v + 2 if k == "wild" else fresh(v) for k, v in value.items()}
            return [fresh(v) for v in value] if isinstance(value, list) else value
        template["stipulations"].append(fresh(second))
        checked(measured.household == f.from_value(template), "nested aliases/tags/order/copy freshness differ")
        checked(measured.raw["stats"]["wildcard_count"] == 4, "expected two fresh variable pairs")
        repeated = session.measure(f.emit_prolog(measured.household), candidate="regular", query="none", name="nested re-grounding", timeout=timeout)
        checked(repeated.household == measured.household, "nested re-grounding differs")
        guards.append({"name": "nested aliases/tags/largeints/emptylists/copy freshness", "status": "pass",
                       "requests": [measured.request, repeated.request]})
        for label, arg in (("compound", "f(a)"), ("improper", "[a|b]"),
                           ("open_tail", "[a|T]"), ("nested_improper", "[[a|b]]"),
                           ("nested_open_tail", "[[a|T]]"), ("fake_variable_marker", "'$VAR'(7)")):
            try:
                session.measure(f"s151(a,0,{arg},[],2017).\n", candidate="regular", query="none", name=label, timeout=timeout)
            except GroundingFailure:
                stem = f"{session.pinned.log.number:03d}"
                meta = json.loads((session.pinned.log.directory / (stem + ".command.json")).read_text())
                err = (session.pinned.log.directory / (stem + ".stderr")).read_text()
                checked(meta["exit"] == 2 and not meta["timed_out"] and "unsupported_household_term" in err,
                        label + ": wrong rejection")
                guards.append({"name": label, "status": "pass:expected-rejection", "command": meta,
                               "stderr_verbatim": err})
            else:
                raise GroundingFailure(label + ": unsupported value accepted")
    except (runtime.RuntimeFailure, ValueError, TypeError, OSError, KeyError) as error:
        finding = str(error)
        raise
    finally:
        runtime.write_json(session.directory / "summary.json", {
            "scope": "two original H4 checks plus synthetic list guards; no admission/parity",
            "original_case_count": 2, "rows": rows, "guards": guards, "finding": finding,
            "record_count": "not-yet-produced", "distinct_household_count": "not-yet-produced",
            "diagnostic_household_instances": len(households),
            "diagnostic_distinct_ordered_households": len(set(households)),
            "diagnostic_household_sha256": [hashlib.sha256(h).hexdigest() for h in households],
        })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--timeout", type=runtime.positive_seconds, default=60)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(StipListTests))
    if not result.wasSuccessful():
        return 1
    if args.evidence:
        integration(args.evidence, args.timeout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
