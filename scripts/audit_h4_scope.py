#!/usr/bin/env python3
"""Read-only syntactic census; not dataflow analysis or an H4.3 check."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from harness.case_reader import read_case


def census():
    paths = sorted((ROOT / "human/sara/sara/cases").glob("*.pl"))
    split_count = 0
    findings = []
    for path in paths:
        program = read_case(path)
        for clause in program.clauses:
            if clause.kind != "rule":
                continue
            head = clause.head
            for call in clause.body.walk():
                if call.value != "split_string" or len(call.args) != 4:
                    continue
                split_count += 1
                argument = call.args[0]
                if (argument.tag == "var" and head.args
                        and (head.args[0].tag != "var"
                             or argument.value != head.args[0].value)):
                    # Variable identity is statement-local; Node equality would
                    # incorrectly compare source spans of distinct occurrences.
                    relative = str(path.relative_to(ROOT))
                    head_location = program.source.location(head.span.start)
                    split_location = program.source.location(call.span.start)
                    findings.append({
                        "case": path.name,
                        "clause_location": relative + head_location[len(str(path)):],
                        "split_location": relative + split_location[len(str(path)):],
                        "clause": program.source.text(clause.span),
                        "source_sha256": program.source.sha256,
                    })
    return {
        "scope": "Parsed original case rules; input-variable identity, not dataflow or completeness analysis",
        "original_cases": len(paths),
        "split_string_calls": split_count,
        "non_first_argument_variable_splits": findings,
    }


if __name__ == "__main__":
    print(json.dumps(census(), indent=2))
