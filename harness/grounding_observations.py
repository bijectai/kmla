"""Explicit H6 modes for the country and list-stipulation paragraph slices.

This is diagnostic query plumbing, not shared payload packaging. The source's
bound arguments stay bound; only its outer NAF is stripped. Tax is handled by
GroundingSession's existing once/1 observation, with amount unbound.
"""
from dataclasses import dataclass
import hashlib
import json
import re

from harness import facts, runtime
from harness.grounding import CORPUS, IMAGE, ROOT, GroundingFailure


MODES = {
    ("s3306_c_A", "bff"), ("s3306_c_B", "bfff"), ("s3306_c_B", "fbbf"),
    ("s3306_c_1", "bb"), ("s3306_c_1_A_i", "bfbfb"), ("s3306_c_1_B", "bf"),
    # H6.5: s2_a_1_B exposes its two source-free outputs. s63_d_2's
    # Question asks applicability, not an amount: retain [2000] as an input.
    ("s2_a_1_B", "bffb"), ("s63_d_2", "bbb"),
}


def _ungroup(node):
    while node.tag == "group":
        node = node.args[0]
    return node


def _bound(node):
    if node.tag in ("atom", "str", "int"):
        return facts._prolog_term(facts.Term(node.tag, node.value))
    if node.tag == "list":
        return "[" + ",".join(_bound(n) for n in node.args) + "]"
    raise GroundingFailure("unsupported bound argument; no new mode or projection inferred")


@dataclass(frozen=True)
class Query:
    predicate: str
    mode: str
    goal: str
    outputs: tuple[str, ...]
    outer_naf: bool
    original_goal: str

    def request(self):
        return f"observation({self.goal},[{','.join(self.outputs)}]).\n"


def paragraph_query(case):
    if len(case.queries) != 1:
        raise GroundingFailure("bounded paragraph slice requires exactly one source query")
    original = case.queries[0].goal
    goal = _ungroup(original)
    negative = goal.tag == "op" and goal.value == "\\+"
    if negative:
        goal = _ungroup(goal.args[0])
    if goal.tag != "compound":
        raise GroundingFailure("unsupported query/conjunct; do not strip constraints")
    mode = "".join("f" if n.tag == "var" else "b" for n in goal.args)
    if (goal.value, mode) not in MODES:
        raise GroundingFailure(f"unimplemented H6 observation: {goal.value}/{len(goal.args)} {mode}")
    # Reader ordinals retain named-variable sharing; each anonymous _ is fresh.
    args = [f"Q{n.value.ordinal}" if n.tag == "var" else _bound(n) for n in goal.args]
    outputs = tuple(arg for arg, m in zip(args, mode) if m == "f")
    return Query(goal.value, mode, f"'{goal.value}'({','.join(args)})", outputs,
                 negative, case.original_text(original))


def canonical(rows):
    """H6.2/WIRE encoded positional tuple sorting/dedup; no input alteration."""
    if type(rows) is not list or any(type(row) is not list for row in rows):
        raise GroundingFailure("observation must be an array of positional tuples")
    encoded = {json.dumps(row, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
               for row in rows}
    return [json.loads(s) for s in sorted(encoded)]


def observe(session, measurement, query, *, label, timeout=60):
    request = session.pinned.requests / f"{label}.observation.pl"
    with request.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(query.request())
    runtime.write_json(request.with_suffix(".json"), {
        "query": query.__dict__, "program_request": measurement.request,
        "program_sha256": runtime.sha256(session.pinned.requests / measurement.request),
        "request_sha256": hashlib.sha256(query.request().encode()).hexdigest(),
    })
    result, out, err = runtime.container(
        session.pinned.log, IMAGE,
        ["swipl", "-q", "-f", "none", "-s", "/harness/grounding_observations.pl",
         "-g", "observe_main", "-t", "halt", "--", f"/requests/{measurement.request}",
         f"/requests/{request.name}"],
        mounts=[(CORPUS, "/corpus", True), (ROOT / "harness", "/harness", True),
                (session.pinned.requests, "/requests", True)], timeout=timeout)
    if result["timed_out"] or result["exit"] != 0 or re.search(rb"(?m)^ERROR:", err):
        raise GroundingFailure(f"{label}: observation failure {result}; raw streams retained")
    try:
        data = json.loads(out)
        data["canonical"] = canonical(data["raw_solutions"])
        data["command"] = result
    except (ValueError, TypeError, KeyError) as error:
        raise GroundingFailure(f"{label}: observation decode failure: {error}") from error
    runtime.write_json(session.directory / f"{label}.observation.json", data)
    return data
