#!/usr/bin/env python3
"""Retain a concrete H3 country omission and its full H6.5 observation mismatch.

This is a failing diagnostic of the UNCHANGED grounder, not a semantic remedy.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import facts, runtime
from harness.case_reader import read_case
from harness.grounding import CORPUS, IMAGE, GroundingSession


def observe(session, request):
    result, out, err = runtime.container(
        session.pinned.log, IMAGE,
        ["swipl", "-q", "-f", "none", "-s", "/harness/grounding_findings.pl",
         "-g", "country_probe", "-t", "halt", "--", "/requests/" + request],
        mounts=[(CORPUS,"/corpus",True), (ROOT / "harness","/harness",True),
                (session.pinned.requests,"/requests",True)], timeout=60)
    if result["timed_out"] or result["exit"] != 0 or b"ERROR:" in err:
        raise RuntimeError(f"observation failure: {result}; raw streams retained")
    raw = json.loads(out)
    # H6.2 canonicalizes encoded positional solutions, not household facts.
    canonical = [json.loads(s) for s in sorted({json.dumps(row,ensure_ascii=False,separators=(",",":")) for row in raw})]
    return {"raw_solutions":raw,"canonical":canonical,"command":result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence",required=True,type=Path)
    args = parser.parse_args()
    session = GroundingSession(args.evidence)
    case = read_case(CORPUS / "cases/s3306_c_A_pos.pl")
    original = session.original(case)
    reground = session.reground(case,original.household)
    before, after = observe(session,original.request), observe(session,reground.request)
    omitted = facts.Fact("country_",(facts.Term("str","baltimore, maryland, usa"),facts.Term("str","usa")))
    report = {
        "original_case": "s3306_c_A_pos.pl", "source_sha256":case.source.sha256,
        "supplied_country_fact": facts.to_value(facts.Household((omitted,),()))["facts"][0],
        "country_retained": omitted in original.household.facts,
        "h4_3_a": "pass" if original.household == reground.household else "fail",
        "observation_authority":"H6.5 s3306_c_A/3 bff; inputs [alice_employer], outputs [Employer,Employee]",
        "original_observation":before,"regrounded_observation":after,
        "h4_3_b":"pass" if before["canonical"] == after["canonical"] else "fail",
        "scope":"unchanged-grounder finding; no preservation fix or alternative traversal",
        "helper_sha256":runtime.sha256(ROOT / "harness/grounding_findings.pl"),
        "script_sha256":runtime.sha256(Path(__file__)),
    }
    runtime.write_json(session.directory / "finding.json",report)
    print(json.dumps({k:v for k,v in report.items() if k not in ("original_observation","regrounded_observation")},indent=2))
    print("original canonical:",json.dumps(before["canonical"],separators=(",",":")))
    print("regrounded canonical:",json.dumps(after["canonical"],separators=(",",":")))
    return 1 if not report["country_retained"] or report["h4_3_a"] != "pass" or report["h4_3_b"] != "pass" else 0


if __name__ == "__main__":
    raise SystemExit(main())
