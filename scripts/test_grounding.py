#!/usr/bin/env python3
"""Measure the exact reviewed candidate, retaining both H4 statuses for all 376.

The first reproducible process/comparison failure stops this audit; remaining
originals stay explicitly blocked. No result is a production reference answer.
"""

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
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
from harness.grounding import (CANDIDATE_NAME, CORPUS, GroundingFailure, GroundingSession,
                              candidate_mode, tax_inputs)
from harness.grounding_observations import Query, observe, paragraph_query
from scripts.test_country_grounding import country_check


@dataclass(frozen=True)
class ObservationPlan:
    kind: str
    query: Query | None = None
    tax_input: str | None = None
    reason: str | None = None


def observation_plan(case):
    """Dispatch only existing implementations; a rejected mode is not inferred.

    An unimplemented paragraph projection is a coverage gap, not an answer or
    an owner-choice blocker. Malformed inputs to the implemented scalar mode
    remain errors from tax_inputs; do not silently fall back to another mode.
    """
    scalar = tax_inputs(case)
    if scalar != "none":
        return ObservationPlan("tax_first_solution", tax_input=scalar)
    try:
        query = paragraph_query(case)
    except GroundingFailure as error:
        return ObservationPlan("unimplemented", reason=str(error))
    return ObservationPlan("paragraph", query=query)


def compare_observations(session, plan, original, reground, *, name, timeout):
    """Never run or call an unavailable mode; do not use ground expected truth."""
    if plan.kind == "unimplemented":
        return {"status":"unimplemented:approved-H6-projection-not-implemented",
                "reason":plan.reason, "owner_choice_blocker":False}
    if plan.kind == "tax_first_solution" and plan.tax_input:
        left, right = original.raw["tax"], reground.raw["tax"]
        if left["status"] != "first_solution" or right["status"] != "first_solution":
            raise GroundingFailure("tax first-solution observation missing; no alternate comparison")
        equal = left["value"] == right["value"]
    elif plan.kind == "paragraph" and plan.query is not None:
        # The constructor used by dispatch above enforces the existing modes;
        # the pinned observer independently checks the mode and output tuple.
        left = observe(session, original, plan.query, label=name + "-original", timeout=timeout)
        right = observe(session, reground, plan.query, label=name + "-serialized", timeout=timeout)
        equal = left["canonical"] == right["canonical"]
    else:
        raise GroundingFailure("invalid observation dispatch; no fallback")
    return {"status":"pass" if equal else "fail", "original":left, "serialized":right}


class RecognitionTests(unittest.TestCase):
    def test_exact_original(self):
        self.assertEqual(candidate_mode(read_case(CORPUS / "cases" / CANDIDATE_NAME)), "tax_case_33")

    def test_digest_mismatch_has_no_fallback(self):
        case = read_case(CORPUS / "cases" / CANDIDATE_NAME)
        changed = parse_case(case.source.original + b"\n", source_name=CANDIDATE_NAME)
        with self.assertRaisesRegex(GroundingFailure, "digest mismatch"):
            candidate_mode(changed)

    def test_same_digest_different_name_rejected(self):
        case = read_case(CORPUS / "cases" / CANDIDATE_NAME)
        renamed = parse_case(case.source.original, source_name="another.pl")
        with self.assertRaisesRegex(GroundingFailure, "different original filename"):
            candidate_mode(renamed)

    def test_other_case_is_regular(self):
        case = read_case(CORPUS / "cases/tax_case_32.pl")
        self.assertEqual(candidate_mode(case), "regular")

    def test_scalar_input_does_not_include_expected_answer(self):
        case = read_case(CORPUS / "cases" / CANDIDATE_NAME)
        self.assertEqual(tax_inputs(case), "tax_inputs('alice',2015)")
        self.assertNotIn("27181", tax_inputs(case))

    def test_non_tax_mode_is_not_guessed(self):
        case = read_case(CORPUS / "cases/s151_a_pos.pl")
        self.assertEqual(tax_inputs(case), "none")


def first_difference(before, after):
    a, b = facts.to_value(before), facts.to_value(after)
    for field in ("facts", "stipulations"):
        for i in range(max(len(a[field]), len(b[field]))):
            left = a[field][i] if i < len(a[field]) else {"missing": True}
            right = b[field][i] if i < len(b[field]) else {"missing": True}
            if left != right:
                return {"field": field, "index": i, "original_grounding": left,
                        "regrounding": right, "original_length": len(a[field]),
                        "regrounded_length": len(b[field])}
    return None


def audit(evidence, timeout):
    paths = sorted((CORPUS / "cases").glob("*.pl"))
    rows = [{"original_case": p.name, "h4_3_a": "blocked:not-yet-run",
             "h4_3_b": "blocked:not-yet-run", "direct_country":{"status":"blocked:not-yet-run"}}
            for p in paths]
    if len(paths) != 376:
        raise GroundingFailure(f"original population differs: {len(paths)}; no filtering permitted")
    started = time.monotonic()
    failure = None
    session = None
    active = None
    stage = "preflight"
    households = []
    by_name = {row["original_case"]: row for row in rows}
    # Establish the exact endorsed candidate before any generic corpus result.
    ordered = [CORPUS / "cases" / CANDIDATE_NAME] + [p for p in paths if p.name != CANDIDATE_NAME]
    attempted = 0
    try:
        session = GroundingSession(evidence)
        runtime.write_json(session.directory / "audit-code.json", {
            "scope":"A-023 distinct-event audit restarted from source; eight explicit paragraph modes plus tax first solution only",
            "hashes":{name:runtime.sha256(ROOT / name) for name in (
                "scripts/test_grounding.py", "scripts/test_grounding_dispatch.py", "scripts/test_country_grounding.py",
                "harness/grounding.py", "harness/grounding.pl", "harness/grounding_observations.py",
                "harness/grounding_observations.pl", "harness/facts.py",
                "scripts/test_stip_lists.py", "scripts/test_event_domain.py")},
            "execution_order":[p.name for p in ordered],
            "source_files_sha256":{p.name:runtime.sha256(p) for p in paths},
        })
        for path in ordered:
            row = by_name[path.name]
            active = row
            stage = "source/observation-dispatch"
            attempted += 1
            row["h4_3_a"] = "error:in-progress"
            row["h4_3_b"] = "blocked:grounding-not-complete"
            case = read_case(path)
            row["source_sha256"] = case.source.sha256
            row["reader_exceptions"] = [asdict(e) | {"inserted": e.inserted.decode()}
                                         for e in case.source.edits]
            plan = observation_plan(case)
            row["h6_observation"] = asdict(plan)
            row["original_queries"] = [case.original_text(q.goal) for q in case.queries]
            stage = "original-grounding"
            original = session.original(case, timeout=timeout)
            row["original_measurement"] = original.request
            row["original_stats"] = original.raw["stats"]
            households.append(facts.encode(original.household))
            stage = "direct-country-preservation"
            direct = country_check(case, original)
            row["direct_country"] = direct
            if direct["status"] != "pass":
                row["h4_3_a"] = "blocked:country-preservation-failure"
                row["h4_3_b"] = "blocked:country-preservation-failure"
                failure = {"case":path.name,"kind":"direct country preservation failure","details":direct}
            elif not direct["supplied"]:
                row["direct_country"]["status"] = "not-applicable:no-supplied-country"
            if failure:
                runtime.write_json(session.directory / (path.stem + ".status.json"), row)
                print("FINDING: " + json.dumps(failure), flush=True)
                break
            stage = "regrounding"
            reground = session.reground(case, original.household, timeout=timeout)
            row["reground_measurement"] = reground.request
            row["reground_stats"] = reground.raw["stats"]
            difference = first_difference(original.household, reground.household)
            row["h4_3_a"] = "fail" if difference else "pass"
            if difference:
                row["ordered_difference"] = difference
                row["h4_3_b"] = "blocked:ordered-list-comparison-failure"
                failure = {"case":path.name,"kind":"H4.3(a) ordered comparison failure","details":difference}
            else:
                stage = "H6-observation"
                row["h4_3_b"] = "error:in-progress"
                observed = compare_observations(session, plan, original, reground,
                                                name=path.stem, timeout=timeout)
                row["h4_3_b"] = observed["status"]
                row["observation_comparison"] = observed
                if row["h4_3_b"] == "fail":
                    failure = {"case":path.name,"kind":"H4.3(b) observation comparison failure","details":observed}
            runtime.write_json(session.directory / (path.stem + ".status.json"), row)
            print(f"{path.name}: H4.3(a)={row['h4_3_a']} H4.3(b)={row['h4_3_b']}", flush=True)
            if failure:
                print("FINDING: " + json.dumps(failure), flush=True)
                break
    except (runtime.RuntimeFailure, ValueError, TypeError, OSError, KeyError, KeyboardInterrupt) as error:
        interrupted = isinstance(error, KeyboardInterrupt)
        failure = {"case":active["original_case"] if active else None, "stage":stage,
                   "kind":"interrupted" if interrupted else "execution/dispatch/decode failure",
                   "error":str(error) or "interrupted; no completion claim"}
        if active is not None:
            active["error"] = failure
            # Do not erase an already completed H4(a) result when H6 raises.
            for field in ("h4_3_a", "h4_3_b"):
                if active[field] == "error:in-progress":
                    active[field] = "blocked:interrupted" if interrupted else "error:" + stage
            if active["direct_country"]["status"] == "blocked:not-yet-run":
                active["direct_country"]["status"] = "blocked:" + stage
            runtime.write_json(Path(evidence) / (Path(active["original_case"]).stem + ".status.json"), active)
        print("FINDING: " + json.dumps(failure), flush=True)
    finally:
        for row in rows:
            if row["h4_3_a"] == "blocked:not-yet-run":
                row["h4_3_a"] = "blocked:halt-after-finding" if failure else "blocked:not-produced"
                row["h4_3_b"] = "blocked:halt-after-finding" if failure else "blocked:not-produced"
                row["direct_country"]["status"] = "blocked:halt-after-finding" if failure else "blocked:not-produced"
        directory = session.directory if session else Path(evidence)
        runtime.write_json(directory / "all-376-statuses.json", rows)
        summary = {
            "scope": "candidate measurement only; no production records, Valid, parity or checkpoint claim",
            "original_case_count": len(rows), "attempted_original_count": attempted,
            "record_count": "not-yet-produced", "distinct_household_count": "not-yet-produced",
            "h4_3_a_pass": sum(r["h4_3_a"] == "pass" for r in rows),
            "h4_3_b_pass": sum(r["h4_3_b"] == "pass" for r in rows),
            "h4_3_a_counts":dict(Counter(r["h4_3_a"] for r in rows)),
            "h4_3_b_counts":dict(Counter(r["h4_3_b"] for r in rows)),
            "direct_country_counts":dict(Counter(r["direct_country"]["status"] for r in rows)),
            "diagnostic_household_instances":len(households),
            "diagnostic_distinct_ordered_households":len(set(households)),
            "diagnostic_household_sha256":[hashlib.sha256(h).hexdigest() for h in households],
            "all_originals_visited":attempted == len(rows),
            "audit_pass":not failure and all(r["h4_3_a"] == r["h4_3_b"] == "pass" for r in rows),
            "elapsed_wall_seconds": time.monotonic()-started, "finding": failure,
        }
        runtime.write_json(directory / "summary.json", summary)
        print(json.dumps({k:v for k,v in summary.items() if k != "diagnostic_household_sha256"}, indent=2), flush=True)
    return 1 if failure or any(r["h4_3_b"] != "pass" for r in rows) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--timeout", type=runtime.positive_seconds, default=60)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RecognitionTests))
    if not result.wasSuccessful():
        return 1
    return audit(args.evidence, args.timeout) if args.evidence else 0


if __name__ == "__main__":
    raise SystemExit(main())
