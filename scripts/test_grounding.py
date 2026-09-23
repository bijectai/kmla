#!/usr/bin/env python3
"""Measure the exact reviewed candidate, retaining both H4 statuses for all 376.

The first reproducible process/comparison failure stops this audit; remaining
originals stay explicitly blocked. No result is a production reference answer.
"""

import argparse
from dataclasses import asdict
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
             "h4_3_b": "blocked:not-yet-run"} for p in paths]
    if len(paths) != 376:
        raise GroundingFailure(f"original population differs: {len(paths)}; no filtering permitted")
    session = GroundingSession(evidence)
    started = time.monotonic()
    failure = None
    by_name = {row["original_case"]: row for row in rows}
    # Establish the exact endorsed candidate before any generic corpus result.
    ordered = [CORPUS / "cases" / CANDIDATE_NAME] + [p for p in paths if p.name != CANDIDATE_NAME]
    attempted = 0
    try:
        for path in ordered:
            row = by_name[path.name]
            attempted += 1
            row["h4_3_a"] = "error:in-progress"
            row["h4_3_b"] = "blocked:grounding-not-complete"
            case = read_case(path)
            row["source_sha256"] = case.source.sha256
            row["reader_exceptions"] = [asdict(e) | {"inserted": e.inserted.decode()}
                                         for e in case.source.edits]
            query = tax_inputs(case)
            row["h6_observation"] = ("tax/3 first solution, amount unbound" if query != "none" else
                                     "unimplemented H6 projection; absence of a machine-readable map is not an owner-choice blocker")
            original = session.original(case, timeout=timeout)
            row["original_measurement"] = original.request
            row["original_stats"] = original.raw["stats"]
            reground = session.reground(case, original.household, timeout=timeout)
            row["reground_measurement"] = reground.request
            row["reground_stats"] = reground.raw["stats"]
            difference = first_difference(original.household, reground.household)
            row["h4_3_a"] = "fail" if difference else "pass"
            if difference:
                row["ordered_difference"] = difference
            if query != "none":
                left, right = original.raw["tax"], reground.raw["tax"]
                row["h4_3_b"] = "pass" if left["value"] == right["value"] else "fail"
                row["tax_first_solution"] = {"original": left, "regrounded": right}
            else:
                row["h4_3_b"] = "blocked:unimplemented-approved-H6-projection"
            runtime.write_json(session.directory / (path.stem + ".status.json"), row)
            print(f"{path.name}: H4.3(a)={row['h4_3_a']} H4.3(b)={row['h4_3_b']}", flush=True)
            if row["h4_3_a"] == "fail" or row["h4_3_b"] == "fail":
                failure = {"case": path.name, "kind": "H4 comparison failure", "details": row}
                print("FINDING: stopping affected verification; no comparison or grounding change", flush=True)
                break
    except KeyboardInterrupt:
        row["h4_3_a"] = "blocked:interrupted"
        row["h4_3_b"] = "blocked:interrupted"
        failure = {"case": row["original_case"], "kind": "audit interrupted; no completion claim"}
        print("STOP: audit interrupted; retained partial measurements and all case statuses", flush=True)
    except (GroundingFailure, ValueError, OSError, KeyError) as error:
        row["h4_3_a"] = "error"
        row["error"] = str(error)
        failure = {"case": row["original_case"], "kind": "execution/decode failure", "error": str(error)}
        print("FINDING: " + str(error), flush=True)
    finally:
        for row in rows:
            if row["h4_3_a"] == "blocked:not-yet-run":
                row["h4_3_a"] = "blocked:halt-after-finding" if failure else "blocked:not-produced"
                row["h4_3_b"] = "blocked:halt-after-finding" if failure else "blocked:not-produced"
        runtime.write_json(session.directory / "all-376-statuses.json", rows)
        runtime.write_json(session.directory / "summary.json", {
            "scope": "candidate measurement only; no production records, Valid, parity or checkpoint claim",
            "original_case_count": len(rows), "attempted_original_count": attempted,
            "record_count": "not-yet-produced", "distinct_household_count": "not-yet-produced",
            "h4_3_a_pass": sum(r["h4_3_a"] == "pass" for r in rows),
            "h4_3_b_pass": sum(r["h4_3_b"] == "pass" for r in rows),
            "elapsed_wall_seconds": time.monotonic()-started, "finding": failure,
        })
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
