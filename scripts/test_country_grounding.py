#!/usr/bin/env python3
"""A-021's narrow 14-case measurement, not a producer or all-376 certificate.

Run without --evidence for Python unit checks; with it, verify the full pinned
identity and retain every request/stream, both per-case H4 statuses, direct
country preservation, and separate adversarial transport/grounding guards.
"""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import facts, runtime
from harness.case_reader import parse_case, read_case
from harness.grounding import CORPUS, GroundingFailure, GroundingSession, Measurement, tax_inputs
from harness.grounding_observations import canonical, observe, paragraph_query


NAMES = tuple(f"s3306_c_{s}_{p}.pl" for s in ("A", "B", "1", "1_A_i", "1_B")
              for p in ("pos", "neg")) + tuple(f"tax_case_{i}.pl" for i in (4, 51, 81, 82))


def supplied_countries(case):
    """Independent source-AST extraction; no event universe or grounder output."""
    found = []
    for index, clause in enumerate(case.clauses, 1):
        head = clause.head
        if head.tag != "compound" or head.value != "country_" or len(head.args) != 2:
            continue
        if clause.kind != "fact" or any(n.tag not in ("atom", "str", "int") for n in head.args):
            raise GroundingFailure("country rule/non-ground/unsupported term is not covered")
        fact = facts.Fact("country_", tuple(facts.Term(n.tag, n.value) for n in head.args))
        found.append((index, fact))
    return found


def country_check(case, measurement):
    supplied = supplied_countries(case)
    country_facts = tuple(f for f in measurement.household.facts if f.ctor == "country_")
    sources = measurement.raw["fact_source_clauses"]
    if len(sources) != len(measurement.household.facts):
        raise GroundingFailure("fact provenance length mismatch")
    actual_indices = [i for i, f in zip(sources, measurement.household.facts) if f.ctor == "country_"]
    expected = tuple(f for _, f in supplied)
    return {
        "status": "pass" if country_facts == expected and actual_indices == [i for i, _ in supplied] else "fail",
        "supplied_source_indices": [i for i, _ in supplied],
        "emitted_source_indices": actual_indices,
        "emitted_fact_positions_1based": [i for i, f in enumerate(measurement.household.facts, 1)
                                          if f.ctor == "country_"],
        "supplied": facts.to_value(facts.Household(expected, ()))['facts'],
        "emitted": facts.to_value(facts.Household(country_facts, ()))['facts'],
    }


def assert_observation_anchor(name, original, serialized, control=None):
    """Fixed independently recorded regressions, not only mutual equality."""
    if name == "s3306_c_A_pos.pl":
        expected = [[{"a":"alice"}, {"a":"bob"}]]
        if original["canonical"] != expected or serialized["canonical"] != expected:
            raise GroundingFailure("A-pos original AND serialized must equal the fixed alice/bob observation")
    elif name in ("s3306_c_B_pos.pl", "s3306_c_B_neg.pl"):
        positive = name == "s3306_c_B_pos.pl"
        expected = [[{"a":"alice"}, {"a":"bob"}, {"s":"caracas, venezuela"}]] if positive else []
        omitted = [[{"a":"alice"}, {"a":"bob"}, None]] if positive else []
        if (original["canonical"] != expected or serialized["canonical"] != expected or
                control is None or control["canonical"] != omitted):
            raise GroundingFailure(f"{name}: fixed original/serialized/omission observations differ")
        count = 1 if positive else 0
        if any(value["proof_count"] != count for value in (original, serialized, control)):
            raise GroundingFailure(f"{name}: measured proof-count regression differs")
    else:
        raise GroundingFailure("no fixed observation anchor for this original")


class CountryTests(unittest.TestCase):
    def query(self, text):
        return paragraph_query(parse_case(("% Test\n:- " + text + ".\n").encode()))

    def test_all_ten_exact_modes(self):
        self.assertEqual([paragraph_query(read_case(CORPUS / "cases" / n)).mode for n in NAMES[:10]],
                         ["bff", "bff", "bfff", "fbbf", "bb", "bb", "bfbfb", "bfbfb", "bf", "bf"])

    def test_outer_naf_only_and_bound_inputs_unchanged(self):
        q = self.query(r"\+ s3306_c_B(_,alice,bob,_)")
        self.assertTrue(q.outer_naf)
        self.assertEqual(q.request(), "observation('s3306_c_B'(Q0,'alice','bob',Q1),[Q0,Q1]).\n")

    def test_bound_list_is_not_scalar_or_free(self):
        positive, negative = [paragraph_query(read_case(CORPUS / "cases" / n)) for n in NAMES[6:8]]
        self.assertIn("['bob']", positive.goal)
        self.assertIn(",'bob',", negative.goal)
        self.assertEqual(positive.outputs, ("Q0", "Q1"))

    def test_variable_sharing_and_anonymous_freshness(self):
        self.assertEqual(self.query("s3306_c_A(x,X,X)").outputs, ("Q0", "Q0"))
        self.assertEqual(self.query("s3306_c_A(x,_,_)").outputs, ("Q0", "Q1"))

    def test_no_extra_conjunct_or_unknown_mode_guess(self):
        for text in ("(s3306_c_A(x,X,Y),X=alice)", "s3306_c_A(x,alice,bob)", "s151_a(alice,4000,2015)"):
            with self.subTest(text=text), self.assertRaises(GroundingFailure):
                self.query(text)

    def test_tax_uses_only_person_and_year(self):
        for name in NAMES[10:]:
            case = read_case(CORPUS / "cases" / name)
            self.assertEqual(tax_inputs(case).count(","), 1)
            with self.assertRaises(GroundingFailure):
                paragraph_query(case)  # never allow tax/3 through findall

    def test_canonicalization_only_at_observation_boundary(self):
        rows = [[{"s": "x"}], [None], [{"a": "x"}], [{"s": "x"}], [[{"a": "x"}]]]
        before = json.dumps(rows)
        self.assertEqual(len(canonical(rows)), 4)
        self.assertNotEqual(canonical([[{"a": "x"}]]), canonical([[{"s": "x"}]]))
        self.assertEqual(json.dumps(rows), before)

    def test_country_source_tags_order_duplicates(self):
        case = parse_case(b'country_("p","c").\nservice_(e).\ncountry_(p,"c").\ncountry_("p","c").\n')
        pairs = supplied_countries(case)
        self.assertEqual([i for i, _ in pairs], [1, 3, 4])
        self.assertEqual(pairs[0][1], pairs[2][1])
        self.assertNotEqual(pairs[0][1], pairs[1][1])

    def test_country_source_fails_closed(self):
        for text in ('country_(p,"c") :- true.', 'country_(p,"c") :- fail.',
                     'country_(_,"c").', 'country_(p,X).'):
            with self.subTest(text=text), self.assertRaises(GroundingFailure):
                supplied_countries(parse_case(text.encode()))

    def test_a_anchor_checks_both_not_just_mutual_equality(self):
        good = {"canonical":[[{"a":"alice"}, {"a":"bob"}]]}
        wrong = {"canonical":[]}
        assert_observation_anchor("s3306_c_A_pos.pl", good, good)
        for left, right in ((wrong, wrong), (good, wrong), (wrong, good)):
            with self.subTest(left=left,right=right), self.assertRaises(GroundingFailure):
                assert_observation_anchor("s3306_c_A_pos.pl", left, right)

    def test_b_anchors_require_measured_full_output_and_proof_counts(self):
        good = {"canonical":[[{"a":"alice"}, {"a":"bob"}, {"s":"caracas, venezuela"}]], "proof_count":1}
        omitted = {"canonical":[[{"a":"alice"}, {"a":"bob"}, None]], "proof_count":1}
        empty = {"canonical":[], "proof_count":0}
        assert_observation_anchor("s3306_c_B_pos.pl", good, good, omitted)
        assert_observation_anchor("s3306_c_B_neg.pl", empty, empty, empty)
        for name, left, right, control in (
            ("s3306_c_B_pos.pl", omitted, omitted, omitted),
            ("s3306_c_B_pos.pl", good, good, good),
            ("s3306_c_B_pos.pl", good, good, {**omitted,"proof_count":2}),
            ("s3306_c_B_neg.pl", empty, empty, omitted),
        ):
            with self.subTest(name=name,control=control), self.assertRaises(GroundingFailure):
                assert_observation_anchor(name,left,right,control)


GUARD_SOURCE = '''country_("p","c").
service_(e).
agent_(e,a).
country_(p,"c").
service_(e).
country_("p","c").
patient(e,x).
patient_(e,"x").
purpose_(_,"agricultural labor").
medical_institution_(clinic).
retirement_(r).
'''


def integration_guards(session, timeout):
    """Fixtures are not admitted originals, records, or preservation claims."""
    reports = []
    first = session.measure(GUARD_SOURCE, candidate="regular", query="none",
                            name="synthetic order/tag/duplicate/inert/event guard", timeout=timeout)
    atom = lambda s: facts.Term("atom", s)
    string = lambda s: facts.Term("str", s)
    f = facts.Fact
    expected = facts.Household((
        f("country_", (string("p"), string("c"))), f("service_", (atom("e"),)),
        f("agent_", (atom("e"), atom("a"))),
        f("country_", (atom("p"), string("c"))), f("service_", (atom("e"),)),
        f("country_", (string("p"), string("c"))),
        f("patient", (atom("e"), atom("x"))),
        f("patient_", (atom("e"), string("x"))),
        f("purpose_", (facts.Pat("wild", 0), string("agricultural labor"))),
        f("medical_institution_", (atom("clinic"),)), f("retirement_", (atom("r"),)),
    ), ())
    if first.household != expected or first.raw["fact_source_clauses"] != list(range(1,12)):
        raise GroundingFailure("synthetic exact order/tag/duplicate/inert/event guard failed")
    direct = country_check(parse_case(GUARD_SOURCE.encode()), first)
    if direct["status"] != "pass":
        raise GroundingFailure("synthetic country direct comparison failed")
    again = session.measure(facts.emit_prolog(first.household), candidate="regular", query="none",
                            name="synthetic A-023 distinct-event traversal", timeout=timeout)
    counts = {p: sum(x.ctor == p for x in again.household.facts)
              for p in ("agent_", "patient", "patient_", "country_", "purpose_")}
    if counts != {"agent_":1, "patient":1, "patient_":1, "country_":3, "purpose_":1}:
        raise GroundingFailure("ordinary event traversal or wildcard changed")
    if again.household != expected or again.raw["fact_source_clauses"] != list(range(1,12)):
        raise GroundingFailure("A-023 exact ordered fixed point failed")
    # A-023 withdraws the old multiset-domain expectation (2 -> 4 copies of
    # single binary clauses). Old source, assertions and runtime evidence are
    # retained in event-domain-harness-evidence-2026-09-23/baseline.json and the
    # untouched stip-list-harness-evidence-2026-09-23/country-final/ directory.
    # Both genuine service_(e) clauses and all three country clauses stay here.
    reports.append({"guard":"tags/order/duplicates/inert/wildcard/ordinary-event", "status":"pass",
                    "requests":[first.request,again.request], "direct_country":direct,
                    "reground_predicate_counts":counts,
                    "fixture_h4_3_a":"equal under A-023; both stored unary duplicates retained"})
    only = session.measure('country_("p","c").\ncountry_("p","c").\n', candidate="regular",
                           query="none", name="synthetic zero-event country guard", timeout=timeout)
    if len(only.household.facts) != 2 or only.raw["stats"]["unary_proofs"] != 0:
        raise GroundingFailure("country incorrectly depends on nonempty event domain")
    reports.append({"guard":"country without unary events", "status":"pass", "request":only.request})
    for label, source, marker in (
        ("rule_true", 'country_(p,"c") :- true.', "country_rule_not_covered"),
        ("rule_fail", 'country_(p,"c") :- fail.', "country_rule_not_covered"),
        ("free_place", 'country_(_,"c").', "nonground_country_not_covered"),
        ("free_country", 'country_(p,X).', "nonground_country_not_covered"),
    ):
        try:
            session.measure(source + "\n", candidate="regular", query="none", name=label, timeout=timeout)
        except GroundingFailure as error:
            stem = f"{session.pinned.log.number:03d}"
            metadata = json.loads((session.pinned.log.directory / (stem + ".command.json")).read_text())
            stderr = (session.pinned.log.directory / (stem + ".stderr")).read_text()
            if metadata["exit"] != 2 or metadata["timed_out"] or marker not in stderr:
                raise GroundingFailure(f"wrong failure for {label}: {error}") from error
            reports.append({"guard":label,"status":"pass:expected-rejection", "command":metadata,
                            "stderr_verbatim":stderr})
        else:
            raise GroundingFailure(f"country fail-closed guard unexpectedly accepted {label}")
    return reports


def omission_control(session, measurement, query, name, timeout):
    """Diagnostic loss control ONLY; not a changed original or production input.

    A-021's opposite-sign claim needs a measured omitted-country comparator.
    Never use this Household for either H4 pass or the direct retention check.
    """
    control = facts.Household(tuple(f for f in measurement.household.facts if f.ctor != "country_"),
                              measurement.household.stipulations)
    request = session.pinned.requests / f"{name}.omission-control.pl"
    with request.open("x", encoding="utf-8") as stream:
        stream.write(facts.emit_prolog(control))
    return observe(session, Measurement(control, {}, request.name), query,
                   label=name + "-omission-control", timeout=timeout)


def audit(evidence, timeout):
    rows = [{"original_case":name, "h4_3_a":"blocked:not-run", "h4_3_b":"blocked:not-run",
             "direct_country":"blocked:not-run"} for name in NAMES]
    session = GroundingSession(evidence)
    runtime.write_json(session.directory / "slice-code.json", {
        "hashes": {p:runtime.sha256(ROOT / p) for p in
                   ("harness/grounding.pl", "harness/grounding.py", "harness/grounding_observations.pl",
                    "harness/grounding_observations.py", "scripts/test_country_grounding.py")},
        "scope":"A-021 14-case measurement only; no Valid or parity records",
        "mode_authority":"H6.5 and explicit owner direction: source bound/free args; tax first solution unbound amount",
    })
    started = time.monotonic()
    finding = None
    guards = []
    households = []
    active = None
    try:
        for row in rows:
            active = row
            name = row["original_case"]
            case = read_case(CORPUS / "cases" / name)
            row["source_sha256"] = case.source.sha256
            row["h4_3_a"] = "error:in-progress"
            row["h4_3_b"] = "blocked:grounding-incomplete"
            query = None if name.startswith("tax_case_") else paragraph_query(case)
            row["query"] = asdict(query) if query else {"tax_inputs":tax_inputs(case),"amount":"unbound; first solution only"}
            original = session.original(case, timeout=timeout)
            households.append(facts.encode(original.household))
            row["original_request"] = original.request
            row["original_stats"] = original.raw["stats"]
            row["direct_country"] = country_check(case, original)
            reground = session.reground(case, original.household, timeout=timeout)
            row["reground_request"] = reground.request
            row["reground_stats"] = reground.raw["stats"]
            row["h4_3_a"] = "pass" if original.household == reground.household else "fail"
            row["h4_3_b"] = "error:observation-in-progress"
            if query is None:
                left, right = original.raw["tax"], reground.raw["tax"]
                equal = left["value"] == right["value"]
            else:
                left = observe(session, original, query, label=case_name(name) + "-original", timeout=timeout)
                right = observe(session, reground, query, label=case_name(name) + "-serialized", timeout=timeout)
                equal = left["canonical"] == right["canonical"]
            row["original_observation"], row["serialized_observation"] = left, right
            row["h4_3_b"] = "pass" if equal else "fail"
            if (row["h4_3_a"] != "pass" or row["h4_3_b"] != "pass" or row["direct_country"]["status"] != "pass"):
                raise GroundingFailure(f"{name}: H4 or direct-country mismatch; no remedy applied")
            if name == "s3306_c_A_pos.pl":
                row["anchored_regression"] = "error:in-progress"
                assert_observation_anchor(name, left, right)
                row["anchored_regression"] = "pass"
            if name in ("s3306_c_B_pos.pl", "s3306_c_B_neg.pl"):
                lost = omission_control(session, original, query, case_name(name), timeout)
                row["diagnostic_omission_control"] = lost
                normal_set = {json.dumps(r, sort_keys=True) for r in left["canonical"]}
                lost_set = {json.dumps(r, sort_keys=True) for r in lost["canonical"]}
                row["omission_effect"] = {"added_solutions":len(lost_set-normal_set),
                                          "lost_solutions":len(normal_set-lost_set)}
                row["anchored_regression"] = "error:in-progress"
                assert_observation_anchor(name, left, right, lost)
                expected_change = 1 if name == "s3306_c_B_pos.pl" else 0
                if row["omission_effect"] != {"added_solutions":expected_change, "lost_solutions":expected_change}:
                    raise GroundingFailure(f"{name}: measured omission-effect regression differs")
                row["anchored_regression"] = "pass"
            runtime.write_json(session.directory / (name + ".status.json"), row)
            print(f"{name}: H4.3(a)={row['h4_3_a']} H4.3(b)={row['h4_3_b']} country={row['direct_country']['status']}", flush=True)
        active = None
        guards = integration_guards(session, timeout)
    except (GroundingFailure, runtime.RuntimeFailure, ValueError, TypeError, OSError, KeyError, KeyboardInterrupt) as error:
        finding = {"case":active["original_case"] if active else None,
                   "error":str(error) or "interrupted; no completion claim"}
        print("FINDING: " + str(finding), flush=True)
    finally:
        for row in rows:
            for key in ("h4_3_a", "h4_3_b"):
                if row[key] == "error:in-progress" or row[key] == "error:observation-in-progress":
                    row[key] = "error:incomplete"
        runtime.write_json(session.directory / "all-14-statuses.json", rows)
        runtime.write_json(session.directory / "guards.json", guards)
        summary = {
            "scope":"country-only slice; not all-376 completion, Valid, parity, production records or CP1",
            "original_case_count":len(rows), "completed_original_count":sum(r["h4_3_a"] == r["h4_3_b"] == "pass" for r in rows),
            "h4_3_a_pass":sum(r["h4_3_a"] == "pass" for r in rows),
            "h4_3_b_pass":sum(r["h4_3_b"] == "pass" for r in rows),
            "anchored_regressions_pass":sum(r.get("anchored_regression") == "pass" for r in rows),
            "record_count":"not-yet-produced", "distinct_household_count":"not-yet-produced (production records absent)",
            "diagnostic_household_instances":len(households), "diagnostic_distinct_ordered_households":len(set(households)),
            "diagnostic_household_sha256":[hashlib.sha256(h).hexdigest() for h in households],
            "guard_count":len(guards), "elapsed_wall_seconds":time.monotonic()-started, "finding":finding,
        }
        runtime.write_json(session.directory / "summary.json", summary)
        print(json.dumps(summary, indent=2), flush=True)
    return 1 if finding or summary["completed_original_count"] != 14 else 0


def case_name(name):
    return Path(name).stem


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--timeout", type=runtime.positive_seconds, default=60)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CountryTests))
    if not result.wasSuccessful():
        return 1
    return audit(args.evidence, args.timeout) if args.evidence else 0


if __name__ == "__main__":
    raise SystemExit(main())
