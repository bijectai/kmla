#!/usr/bin/env python3
"""A-023's bounded fixed-point/domain/multiplicity checks; no H6 mode changes."""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import facts as f, runtime
from harness.case_reader import read_case
from harness.grounding import CORPUS, GroundingFailure, GroundingSession
from scripts.test_grounding import compare_observations, observation_plan

WITNESS = "s2_b_3_B_pos.pl"
WITNESS_SHA = "cdf109a726f44e6b5aced16ad84354a71ef51bd8b1bc3e8899b4fb81f9ac7f8a"
LEGACY = ROOT / "docs/phase1/stip-list-harness-evidence-2026-09-23/full-audit"


def atom(text):
    return {"a": text}


def fact(ctor, *args):
    return {"ctor": ctor, "args": list(args)}


def witness_expected():
    """Literal source-clause order, with each rule's actual five yearly proofs.

    Independent of the grounder's output, domain code and serializer traversal.
    H1 keeps both payment_/income_ markers and both agent_ rule definitions.
    """
    a, b, c = atom("alice"), atom("bob"), atom("charlie")
    m, d, r = map(atom, ("alice_and_bob", "alice_dies", "charlie_and_bob_residence"))
    rows = [fact("marriage_", m), fact("agent_", m, a), fact("agent_", m, b),
            fact("start_", m, "1992-02-03"), fact("death_", d), fact("agent_", d, a),
            fact("start_", d, "2014-07-09"), fact("end_", d, "2014-07-09"),
            fact("residence_", r), fact("agent_", r, c), fact("agent_", r, b),
            fact("patient_", r, atom("bob_s_house")), fact("start_", r, "2004-01-01"),
            fact("end_", r, "2019-12-31")]
    sources = list(range(1, 15))
    years = list(range(2015, 2020))
    events = [atom(f"bob_maintains_household_{y}") for y in years]
    for source, ctor, values in (
        (16, "payment_", None), (17, "agent_", [b] * 5), (18, "amount_", [1] * 5),
        (19, "purpose_", [atom("bob_s_house")] * 5),
        (20, "start_", [f"{y}-01-01" for y in years]),
        (21, "end_", [f"{y}-12-31" for y in years]),
        (24, "income_", None), (25, "agent_", [b] * 5), (26, "amount_", [300000] * 5),
        (27, "start_", [f"{y}-01-01" for y in years]),
        (28, "end_", [f"{y}-12-31" for y in years]),
    ):
        for i, event in enumerate(events):
            args = [event] if values is None else [event, values[i]]
            if ctor == "purpose_":
                args[0] = {"val": event}
            rows.append(fact(ctor, *args))
            sources.append(source)
    stips = [{"pred": "s152_d_2_H_6", "args": [
        {"val": c}, {"val": b}, {"val": y}, {"wild": i},
        {"val": {"s": f"{y}-01-01"}}, {"val": {"s": f"{y}-12-31"}},
    ]} for i, y in enumerate(years)]
    return f.from_value({"facts": rows, "stipulations": stips}), sources, [m, d, r, *events]


DUPLICATES_SOURCE = '''service_(z).
service_(z).
income_(z).
service_(a) :- between(1,2,_).
agent_(z,p).
agent_(z,p).
patient_(E,V) :- member(E,[a,z]), member(V,[q,p,q]).
amount_(a,7) :- between(1,2,_).
'''


def duplicates_expected():
    z, a, p, q = map(atom, ("z", "a", "p", "q"))
    rows = [fact("service_", z), fact("service_", z), fact("income_", z),
            fact("service_", a), fact("service_", a), fact("agent_", z, p), fact("agent_", z, p)]
    rows += [fact("patient_", event, value) for event in (z, a) for value in (q, p, q)]
    rows += [fact("amount_", a, 7), fact("amount_", a, 7)]
    return f.from_value({"facts": rows, "stipulations": []}), [1,2,3,4,4,5,6] + [7]*6 + [8]*2


TAGS_SOURCE = '''service_("z").
income_(z).
payment_(7).
service_('7').
income_("7").
service_("z").
agent_("z",str_event).
agent_(z,atom_event).
agent_(7,int_event).
agent_('7',atom_number).
agent_("7",string_number).
'''


def tags_expected():
    domain = [{"s": "z"}, atom("z"), 7, atom("7"), {"s": "7"}]
    rows = [fact(ctor, event) for ctor, event in zip(
        ("service_", "income_", "payment_", "service_", "income_", "service_"),
        [*domain, domain[0]])]
    rows += [fact("agent_", event, atom(value)) for event, value in zip(
        domain, ("str_event", "atom_event", "int_event", "atom_number", "string_number"))]
    return f.from_value({"facts": rows, "stipulations": []}), domain


def require(condition, detail):
    if not condition:
        raise GroundingFailure(detail)


def domain_check(measured, expected, unary_proofs):
    require(measured.raw["event_domain"] == expected, "exact tagged first-occurrence domain differs")
    require(measured.raw["stats"]["unary_proofs"] == unary_proofs == len(measured.raw["unary"]),
            "unary_proofs must count all proofs, not distinct events")
    require(measured.raw["stats"]["distinct_event_domain"] == len(expected), "distinct domain count differs")


class EventDomainTests(unittest.TestCase):
    def test_witness_h6_remains_explicitly_unimplemented(self):
        plan = observation_plan(read_case(CORPUS / "cases" / WITNESS))
        self.assertEqual(plan.kind, "unimplemented")
        self.assertIn("s2_b_3_B/3 bbb", plan.reason)
        result = compare_observations(None, plan, None, None, name=WITNESS, timeout=1)
        self.assertEqual(result["status"], "unimplemented:approved-H6-projection-not-implemented")

    def test_literal_witness_retains_two_unary_kinds_and_duplicate_rules(self):
        expected, sources, domain = witness_expected()
        self.assertEqual(len(expected.facts), 69)
        self.assertEqual(len(sources), 69)
        self.assertEqual(len(domain), 8)
        self.assertEqual(sum(len(f.FACT_TYPES[x.ctor]) == 1 for x in expected.facts), 13)
        self.assertEqual(Counter(expected.facts)[f.Fact("agent_", (f.Term("atom", "bob_maintains_household_2015"),
                                                                f.Term("atom", "bob")))], 2)

    def test_fixture_expectations_keep_true_duplicates(self):
        expected, _ = duplicates_expected()
        self.assertEqual(len(expected.facts), 15)
        self.assertEqual(Counter(expected.facts)[f.Fact("service_", (f.Term("atom", "z"),))], 2)
        tags, domain = tags_expected()
        self.assertEqual(len(tags.facts), 11)
        self.assertEqual(len(domain), 5)


def integrate(evidence, timeout):
    session = GroundingSession(evidence)
    rows, guards, households = [], [], []
    finding = None
    runtime.write_json(session.directory / "correction-code.json", {
        "scope": "A-023 domain correction; all stored unary and binary proofs retained",
        "hashes": {name: runtime.sha256(ROOT / name) for name in (
            "harness/grounding.pl", "harness/grounding.py", "harness/facts.py",
            "scripts/test_event_domain.py", "scripts/test_country_grounding.py", "scripts/test_grounding.py")},
    })
    try:
        case = read_case(CORPUS / "cases" / WITNESS)
        require(case.source.sha256 == WITNESS_SHA, "original witness source changed")
        expected, provenance, domain = witness_expected()
        row = {"case": WITNESS, "source_sha256": case.source.sha256,
               "legacy_fact_counts_separate_procedure": [114, 204, 384],
               "corrected_passes": [], "h4_3_a": "not-complete", "h4_3_b": "not-complete"}
        rows.append(row)
        measured = session.original(case, timeout=timeout)
        households.append(f.encode(measured.household))
        for i in range(3):
            if i:
                measured = session.reground(case, measured.household, timeout=timeout)
            row["corrected_passes"].append({"request": measured.request, "stats": measured.raw["stats"],
                "household_sha256": hashlib.sha256(f.encode(measured.household)).hexdigest()})
            require(measured.household == expected, f"witness corrected pass {i+1} differs from exact source expectation")
            require(measured.raw["fact_source_clauses"] == (provenance if i == 0 else list(range(1,70))),
                    "source-clause provenance/order differs")
            domain_check(measured, domain, 13)
        row["h4_3_a"] = "pass:three-corrected-passes"
        plan = observation_plan(case)
        row["query_plan"] = asdict(plan)
        row["h4_3_b"] = compare_observations(session, plan, None, None, name=WITNESS, timeout=timeout)["status"]
        require(row["h4_3_b"].startswith("unimplemented:"), "witness H6 status silently changed")
        runtime.write_json(session.directory / "witness.json", row)
        print(f"{WITNESS}: corrected 69 -> 69 -> 69; 13 unary proofs / 8 distinct events; H4(b) unimplemented", flush=True)

        duplicate_h, duplicate_sources = duplicates_expected()
        tag_h, tag_domain = tags_expected()
        for name, source, exact, sources, expected_domain, proofs in (
            ("true_duplicates_and_multiple_proofs", DUPLICATES_SOURCE, duplicate_h, duplicate_sources, [atom("z"), atom("a")], 5),
            ("tag_sensitive_first_occurrence", TAGS_SOURCE, tag_h, list(range(1,12)), tag_domain, 6),
        ):
            first = session.measure(source, candidate="regular", query="none", name=name, timeout=timeout)
            require(first.household == exact and first.raw["fact_source_clauses"] == sources, name + ": exact ordered proofs differ")
            domain_check(first, expected_domain, proofs)
            second = session.measure(f.emit_prolog(first.household), candidate="regular", query="none", name=name + " serialized", timeout=timeout)
            require(second.household == exact, name + ": ordered fixed point differs")
            domain_check(second, expected_domain, proofs)
            guards.append({"name": name, "status": "pass", "requests": [first.request, second.request],
                           "expected_household": f.to_value(exact), "domain": expected_domain,
                           "unary_proofs": proofs, "distinct_event_domain": len(expected_domain)})

        # A substantial single-kind baseline: every one of tax33's 316 unary
        # proofs has a distinct event. Compare the entire ordered fact wire.
        tax_case = read_case(CORPUS / "cases/tax_case_33.pl")
        original = session.original(tax_case, timeout=timeout)
        households.append(f.encode(original.household))
        reground = session.reground(tax_case, original.household, timeout=timeout)
        require(original.household == reground.household, "tax33 full ordered H4(a) differs")
        observed = compare_observations(session, observation_plan(tax_case), original, reground,
                                        name="tax_case_33", timeout=timeout)
        require(observed["status"] == "pass" and observed["original"]["value"] == 27181,
                "tax33 first-solution H4(b)/fixed value differs")
        legacy_path = LEGACY / "ground-0001.measurement.json"
        old = f.from_value(json.loads(legacy_path.read_text())["household"])
        old_wire, new_wire = [f.encode(f.Household(h.facts, ())) for h in (old, original.household)]
        require(old_wire == new_wire, "single-kind full ordered fact wire changed")
        require(len(original.household.facts) == 1736, "tax33 exact fact count differs")
        require(original.raw["stats"]["unary_proofs"] == original.raw["stats"]["distinct_event_domain"] == 316,
                "tax33 is not the required single-kind/unique-event control")
        require(original.raw["stats"]["candidate"] == {
            "outer_iterations": 316, "inner_distinct_terms": 157,
            "full_two_input_calls": 49612, "successful_proofs": 157}, "tax33 traversal-cost regression differs")
        tax_row = {"case": "tax_case_33.pl", "source_sha256": tax_case.source.sha256,
                   "h4_3_a": "pass", "h4_3_b": observed["status"], "observation": observed,
                   "requests": [original.request, reground.request], "original_stats": original.raw["stats"],
                   "reground_stats": reground.raw["stats"], "legacy_measurement": str(legacy_path.relative_to(ROOT)),
                   "legacy_measurement_sha256": runtime.sha256(legacy_path),
                   "full_ordered_fact_wire_byte_identical": True,
                   "fact_wire_sha256": hashlib.sha256(new_wire).hexdigest()}
        rows.append(tax_row)
        runtime.write_json(session.directory / "tax33-single-kind.json", tax_row)
        print("tax_case_33: both H4 checks PASS; 1736 ordered facts byte-identical; 49612 calls / 157 proofs", flush=True)
    except (runtime.RuntimeFailure, ValueError, TypeError, KeyError, OSError) as error:
        finding = str(error)
        raise
    finally:
        runtime.write_json(session.directory / "summary.json", {
            "scope": "bounded A-023 corrected measurements; no Valid, parity or checkpoint claim",
            "rows": rows, "guards": guards, "finding": finding,
            "original_case_count": 2, "record_count": "not-yet-produced", "distinct_household_count": "not-yet-produced",
            "diagnostic_household_instances": len(households), "diagnostic_distinct_ordered_households": len(set(households)),
        })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--timeout", type=runtime.positive_seconds, default=60)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(EventDomainTests))
    if not result.wasSuccessful():
        return 1
    if args.evidence:
        integrate(args.evidence, args.timeout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
