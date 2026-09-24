"""Reviewed tax_case_33 H4 candidate and fail-closed measurement orchestration.

Not an installed amendment, admission check, parity producer or H6 mode guesser.
Generic non-tax H6 observation coverage is an unfinished implementation task.
A-021's by-name ground/bodyless country_/2 correction is measured separately;
this is not a production grounder or a corpus-wide preservation certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

from harness import facts, runtime
from harness.case_reader import CaseProgram
from harness.swipl import CORPUS, IMAGE, ROOT, PinnedSession, PrologFailure

CANDIDATE_NAME = "tax_case_33.pl"
CANDIDATE_SHA256 = "5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0"
PURPOSE_CLAUSE = '''purpose_(Payment_event,Service_event) :- split_string(Payment_event,"_","",[Xp,Yp,Zp]),
    split_string(Service_event,"_","",[Xs,Ys,Zs]),
    Xp=="payment",Xs=="workforalice",Yp==Ys,Zp==Zs.'''


class GroundingFailure(PrologFailure):
    pass


def candidate_mode(case: CaseProgram):
    name = Path(case.source.name).name
    if name != CANDIDATE_NAME:
        if case.source.sha256 == CANDIDATE_SHA256:
            raise GroundingFailure("candidate digest supplied with a different original filename")
        return "regular"
    if case.source.sha256 != CANDIDATE_SHA256:
        raise GroundingFailure("tax_case_33 candidate digest mismatch; no ordinary-call fallback")
    purposes = [s for s in case.clauses if s.head.value == "purpose_" and len(s.head.args) == 2]
    if len(purposes) != 1 or purposes[0].kind != "rule" or case.reader_text(purposes[0]) != PURPOSE_CLAUSE:
        raise GroundingFailure("candidate must match exactly one original purpose_/2 rule")
    return "tax_case_33"


def tax_inputs(case: CaseProgram):
    """Only H6's explicit tax/3 scalar mode; never use the expected amount."""
    if len(case.queries) != 1:
        return "none"
    goal = case.queries[0].goal
    if goal.tag != "compound" or goal.value != "tax" or len(goal.args) != 3:
        return "none"
    person, year, _expected = goal.args
    if person.tag not in ("atom", "str", "int") or year.tag != "int":
        raise GroundingFailure("unsupported tax input shape; no inferred scalar mode")
    person_text = facts._prolog_term(facts.Term(person.tag, person.value))
    return f"tax_inputs({person_text},{year.value})"


def _registry():
    kind = {"Term": "term", "Pat": "pat", "Int": "int", "Day": "day"}
    lines = [f"fact_kind({p},[{','.join(kind[k] for k in ks)}])."
             for p, ks in facts.FACT_TYPES.items()]
    lines += [f"stip_kind({p},{arity},{ctor})." for ctor, (p, arity) in facts.STIP_SIGNATURES.items()]
    return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class Measurement:
    household: facts.Household
    raw: dict
    request: str


class GroundingSession:
    def __init__(self, directory):
        self.pinned = PinnedSession(directory)
        self.directory = self.pinned.directory
        self.number = 0
        with (self.pinned.requests / "registry.pl").open("x", encoding="utf-8") as stream:
            stream.write(_registry())
        runtime.write_json(self.directory / "candidate-code.json", {
            "scope": "A-020 candidate / A-021 country correction measurement; not installation or parity",
            "hashes": {name: runtime.sha256(ROOT / name) for name in
                ("harness/grounding.py", "harness/grounding.pl", "scripts/test_grounding.py")},
            "fact_emission_order": "stable source-clause provenance order (H1); phase execution stays unary, binary, stipulation",
            "wildcards": "findall copies numbered in final facts/stipulations traversal; no wildcard expansion",
            "country": "country_/2 only: supplied ground bodyless clause emitted once at original source-clause index; rule/non-ground fails closed",
        })

    def measure(self, source, *, candidate, query, name, timeout=60):
        if candidate not in ("regular", "tax_case_33"):
            raise GroundingFailure("unknown candidate marker")
        self.number += 1
        stem = f"ground-{self.number:04d}"
        request = self.pinned.requests / (stem + ".pl")
        with request.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(source)
        runtime.write_json(self.pinned.requests / (stem + ".json"), {
            "case": name, "candidate": candidate, "query": query,
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        })
        result, out, err = runtime.container(
            self.pinned.log, IMAGE,
            ["swipl", "-q", "-f", "none", "-s", "/harness/grounding.pl", "-g", "main", "-t", "halt",
             "--", f"/requests/{request.name}", "/requests/registry.pl", candidate, query],
            mounts=[(CORPUS, "/corpus", True), (ROOT / "harness", "/harness", True),
                    (self.pinned.requests, "/requests", True)],
            timeout=runtime.positive_seconds(timeout))
        if result["timed_out"] or result["exit"] != 0 or re.search(rb"(?m)^ERROR:", err):
            raise GroundingFailure(f"{name}: process failure {result}; retained raw diagnostics")
        try:
            data = json.loads(out)
            household = facts.from_value(data["household"])
        except (ValueError, TypeError, KeyError) as error:
            raise GroundingFailure(f"{name}: decode failure {error}; retained raw diagnostics") from error
        runtime.write_json(self.directory / (stem + ".measurement.json"), data)
        return Measurement(household, data, request.name)

    def original(self, case, *, timeout=60):
        return self.measure("\n".join(case.clause_texts()) + "\n", candidate=candidate_mode(case),
                            query=tax_inputs(case), name=Path(case.source.name).name, timeout=timeout)

    def reground(self, case, household, *, timeout=60):
        # The re-emitted program contains no candidate rule; never apply its
        # two-input exception to ground facts in place of the ordinary procedure.
        return self.measure(facts.emit_prolog(household), candidate="regular", query=tax_inputs(case),
                            name=Path(case.source.name).name + " (re-emitted)", timeout=timeout)
