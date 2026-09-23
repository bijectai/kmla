#!/usr/bin/env python3
"""Combine retained partial measurements without editing any original evidence.

The broad run was deliberately interrupted for H3/bodyless-domain review. Its
finally block predates explicit interrupt reporting; its null finding and
in-progress row are preserved as raw history, qualified here rather than erased.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from harness import runtime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",type=Path,required=True)
    parser.add_argument("--finding",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args = parser.parse_args()
    raw = json.loads((args.run / "all-376-statuses.json").read_text())
    finding = json.loads(args.finding.read_text())
    rows = copy.deepcopy(raw)
    for row in rows:
        row["raw_status_source"] = str(args.run / "all-376-statuses.json")
        if row["h4_3_a"].startswith(("blocked:","error:in-progress")):
            row["h4_3_a"] = "blocked:general-traversal-halted-for-review"
        if row["h4_3_b"] == "blocked:unimplemented-approved-H6-projection":
            row["h4_3_b"] = "unimplemented:H6-observation"
            row["h6_observation"] = "Implementation gap; no general missing-owner-choice claim"
        elif row["h4_3_b"].startswith("blocked:"):
            row["h4_3_b"] = "blocked:general-traversal-halted-for-review"
        row["qualification"] = "H4.3(a) pass records exact ordered equality for the measured traversal, not source preservation or both H4 checks"
        if row["original_case"] == finding["original_case"]:
            row.update({"h4_3_a":finding["h4_3_a"],"h4_3_b":finding["h4_3_b"],
                        "source_sha256":finding["source_sha256"],"finding_source":str(args.finding),
                        "h6_observation":finding["observation_authority"]})
    if len(rows) != 376 or len({r["original_case"] for r in rows}) != 376:
        raise ValueError("expected exactly 376 distinct original statuses")
    out = runtime.output_path(args.out)
    out.mkdir(parents=True)
    runtime.write_json(out / "all-376-statuses.json",rows)
    summary = {
        "scope":"partial candidate measurement; broad verification halted, not complete",
        "original_case_count":376,
        "record_count":"not-yet-produced",
        "distinct_household_count":"not-yet-produced",
        "h4_3_a":dict(Counter(r["h4_3_a"] for r in rows)),
        "h4_3_b":dict(Counter(r["h4_3_b"] for r in rows)),
        "both_pass_cases":[r["original_case"] for r in rows if r["h4_3_a"] == r["h4_3_b"] == "pass"],
        "source_preservation_finding":finding["original_case"],
        "raw_run_interruption":{"outer_exit":130,"signal":"SIGINT", "process_id":24983,
            "reason":"halt broad traversal pending H3 bodyless/domain review",
            "raw_summary_null_finding_is_not_a_completed_audit":True},
        "input_hashes":{str(p):runtime.sha256(p) for p in
            (args.run / "all-376-statuses.json",args.run / "summary.json",args.finding)},
    }
    runtime.write_json(out / "summary.json",summary)
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
