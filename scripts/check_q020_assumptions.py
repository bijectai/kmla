#!/usr/bin/env python3
"""Pinned read-only measurements of A-020's two source-only assumptions."""

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from harness import runtime
from harness.case_reader import read_case
from harness.swipl import CORPUS, IMAGE, PinnedSession


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Fresh evidence directory")
    args = parser.parse_args()
    case = read_case(CORPUS / "cases/tax_case_33.pl")
    expected = "5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0"
    if case.source.sha256 != expected:
        raise runtime.RuntimeFailure("tax_case_33 identity changed")
    # All unary predicates supplied by this original; no others can contribute
    # original case declarations. This provenance diagnostic has no output-order
    # or production-grounding interpretation.
    unary = list(dict.fromkeys(c.head.value for c in case.clauses if len(c.head.args) == 1))
    if any(not re.fullmatch(r"[a-z][A-Za-z0-9_]*_", name) for name in unary):
        raise runtime.RuntimeFailure("unexpected unary predicate spelling")
    session = PinnedSession(args.out)
    request = session.requests / "001.pl"
    with request.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write("\n".join(case.clause_texts()) + "\n")
        stream.write("\n".join(f"q020_unary({name})." for name in unary) + "\n")
    helper = ROOT / "docs/consult/evidence/q020_assumptions.pl"
    runtime.write_json(session.directory / "assumptions-input.json", {
        "original_sha256": case.source.sha256,
        "request_sha256": runtime.sha256(request),
        "helper_sha256": runtime.sha256(helper),
        "supplied_unary_predicates": unary,
        "scope": "A-020 assumptions only, not H4.3 or candidate traversal cost",
    })
    result, out, err = runtime.container(
        session.log, IMAGE,
        ["swipl", "-q", "-f", "none", "-s", "/diagnostic/q020_assumptions.pl",
         "-g", "main", "-t", "halt"],
        mounts=[(CORPUS, "/corpus", True),
                (helper.parent, "/diagnostic", True),
                (session.requests, "/request", True)], timeout=60)
    sys.stdout.buffer.write(out)
    sys.stderr.buffer.write(err)
    if result["timed_out"] or result["exit"] != 0 or re.search(rb"(?m)^ERROR:", err):
        raise runtime.RuntimeFailure(f"assumption diagnostic failed: {result}")


if __name__ == "__main__":
    main()
