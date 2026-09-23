#!/usr/bin/env python3
"""Pinned Prolog transport integration tests. Writes fresh retained evidence.

Usage: python3 -B scripts/test_swipl.py --evidence NEW_DIRECTORY
This is deliberately opt-in Docker testing, never host Prolog or a skipped pass.
"""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness import facts as f, runtime
from harness.swipl import PinnedSession, PrologFailure
from harness.case_reader import read_case
from scripts.test_facts import fixtures, registry_household


def expected_clauses(h):
    def term(t):
        return t.value if t.tag == "int" else {"a" if t.tag == "atom" else "s": t.value}
    def pat(p):
        return {"variable": f"_KMLA_W{p.value}"} if p.tag == "wild" else term(p.value)
    result = []
    for fact in h.facts:
        args = [term(a) if k == "Term" else pat(a) if k == "Pat" else
                {"s": f.day_to_iso(a)} if k == "Day" else a
                for k, a in zip(f.FACT_TYPES[fact.ctor], fact.args)]
        result.append({"pred": fact.ctor, "args": args})
    for stip in h.stipulations:
        result.append({"pred": f.STIP_SIGNATURES[stip.pred][0], "args": list(map(pat, stip.args))})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    session = PinnedSession(args.evidence)
    originals = []
    for path in sorted((ROOT / "human/sara/sara/cases").glob("*.pl")):
        case = read_case(path)
        originals.append({"case": path.name, "source_sha256": case.source.sha256,
                          "rule_count": sum(s.kind == "rule" for s in case.clauses),
                          "reader_exceptions": len(case.source.edits),
                          "grounding_status": "not-produced: H4 grounding halted",
                          "query_identity_status": "not-produced"})
    runtime.write_json(session.directory / "original-inventory.json", originals)
    if len(originals) != 376:
        raise AssertionError(f"expected 376 originals, found {len(originals)}; retained inventory")
    results = []
    cases = [(c["name"], f.from_value(c["household"])) for c in fixtures()]
    cases.append(("all_registered_constructors", registry_household()))
    for name, h in cases:
        actual = session.inspect(f.emit_prolog(h))
        expected = expected_clauses(h)
        if actual != expected:
            runtime.write_json(session.directory / "mismatch.json", {
                "fixture": name, "expected": expected, "actual": actual})
            raise AssertionError(f"{name}: complete tagged clause sequence differs")
        results.append({"fixture": name, "passed": True, "clauses": len(actual)})
        print(f"PASS {name}: {len(actual)} ordered tagged clauses")
    for name, source in (("parser_failure", "birth_('unterminated).\n"),
                         ("reject_directive", ":- halt.\n"),
                         ("reject_rule", "birth_(x) :- true.\n"),
                         ("reject_compound_value", "birth_(f(x)).\n")):
        try:
            session.inspect(source)
        except PrologFailure:
            results.append({"fixture": name, "passed": True, "expected_failure": True})
            print(f"PASS {name}: reported failure with raw diagnostics")
        else:
            raise AssertionError(f"{name}: unexpected successful read")
    runtime.write_json(session.directory / "summary.json", {
        "scope": "Prolog syntax re-emission only; not H4 re-grounding/query identity/parity/Valid",
        "checks": results, "record_count": "not-yet-produced",
        "distinct_household_count": "not-yet-produced (no producer records)",
        "original_case_count": len(originals),
        "original_count_scope": "lexical inventory only; no original H4 round trips or query comparisons",
        "rule_bearing_original_count": sum(r["rule_count"] > 0 for r in originals),
        "bodyless_original_count": sum(r["rule_count"] == 0 for r in originals),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
