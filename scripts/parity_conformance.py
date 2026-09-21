#!/usr/bin/env python3
"""Black-box conformance harness for the owner's independent parity meter.

The meter at `human/parity/check.py` is an owner-owned artifact: if the assistant
wrote it, "zero mismatches" would mean the oracle agreeing with itself
(`docs/PLAN.md` section 1). This harness therefore contains NO comparison logic
and never reads, imports, or inspects the meter. It only builds fixture
directories, invokes the meter through the CLI in `docs/contracts/PARITY.md`, and
checks the observable contract: exit status, stderr, and `mismatches.jsonl`.

What this does and does not establish
-------------------------------------
It establishes that a meter obeys the published envelope contract. It establishes
nothing about statutory interpretation, and it cannot: every fixture here uses
opaque placeholder results, never a tax answer. A meter that passes every check
here may still be the wrong meter; a meter that fails one is provably out of
contract and would have produced a meaningless Checkpoint 1 gate.

Independence note for the owner
-------------------------------
These fixtures mechanise requirements already fixed in PARITY.md; they do not add
new ones. Requirements PARITY.md leaves open are reported as GAPS and are never
enforced, because enforcing an invented rule would be the assistant deciding the
contract. Write the meter from PARITY.md first and run this afterwards; treating
the harness as the specification is the failure mode to avoid.

Usage:
    python3 -B scripts/parity_conformance.py --meter human/parity/check.py
    python3 -B scripts/parity_conformance.py --meter docs/contracts/parity/check.py

Exit codes: 0 all required checks passed, 1 at least one failed, 2 the harness
itself could not run. Fixtures are built in a temporary directory and never
inside the repository or under `human/`.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


SECTION = 151
TIMEOUT = 120


def record(input_id, result, section=SECTION, version=1, omit_result=False):
    payload = {"schema_version": version, "input_id": input_id, "section": section}
    if not omit_result:
        payload["result"] = result
    return payload


def write_json(path, payload, raw=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(raw if raw is not None else json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class Case:
    """One fixture: a layout builder plus the outcome PARITY.md requires."""

    def __init__(self, name, requirement, citation, build, expect_exit,
                 expect_mismatch_ids=None, expect_stderr=False, informational=False):
        self.name = name
        self.requirement = requirement
        self.citation = citation
        self.build = build
        self.expect_exit = expect_exit
        self.expect_mismatch_ids = expect_mismatch_ids
        self.expect_stderr = expect_stderr
        self.informational = informational


def agreeing(root, ids=("s151_a_pos", "s151_b_pos")):
    for index, name in enumerate(ids):
        write_json(root / "inputs" / f"{name}.json", record(name, None))
        for engine in ("prolog-out", "lean-out"):
            write_json(root / engine / f"{name}.json", record(name, index))


def build_cases():
    cases = []

    def case(*args, **kwargs):
        cases.append(Case(*args, **kwargs))

    def agree(root):
        agreeing(root)

    case("all-agree", "Exit 0 when every requested input has both outputs and they agree",
         "PARITY.md 'Exit 0'", agree, 0, expect_mismatch_ids=[])

    def differ(root):
        agreeing(root)
        write_json(root / "lean-out" / "s151_b_pos.json", record("s151_b_pos", 999))
    case("value-mismatch", "Exit 1 and one mismatch record when a result differs",
         "PARITY.md 'Exit 1'", differ, 1, expect_mismatch_ids=["s151_b_pos"])

    def missing_lean(root):
        agreeing(root)
        (root / "lean-out" / "s151_b_pos.json").unlink()
    case("missing-lean-output", "A missing Lean output is a mismatch, not a skipped input",
         "PARITY.md 'Missing outputs are mismatches'", missing_lean, 1,
         expect_mismatch_ids=["s151_b_pos"])

    def missing_prolog(root):
        agreeing(root)
        (root / "prolog-out" / "s151_a_pos.json").unlink()
    case("missing-prolog-output", "A missing Prolog output is a mismatch",
         "PARITY.md 'Missing outputs are mismatches'", missing_prolog, 1,
         expect_mismatch_ids=["s151_a_pos"])

    def both_missing(root):
        agreeing(root)
        (root / "prolog-out" / "s151_a_pos.json").unlink()
        (root / "lean-out" / "s151_a_pos.json").unlink()
        write_json(root / "lean-out" / "s151_b_pos.json", record("s151_b_pos", 1))
    case("input-population-is-authoritative",
         "An input with NO engine output is still compared, not silently dropped",
         "PARITY.md 'Use --inputs as the authority'; 'Do not compare only the intersection'",
         both_missing, 1, expect_mismatch_ids=["s151_a_pos"])

    def empty_inputs(root):
        (root / "inputs").mkdir(parents=True)
        (root / "prolog-out").mkdir(parents=True)
        (root / "lean-out").mkdir(parents=True)
    case("empty-input-population", "An empty input population fails; it does not validate a section",
         "PARITY.md 'Empty selected input populations fail with exit 2'",
         empty_inputs, 2, expect_stderr=True)

    def extra_output(root):
        agreeing(root)
        write_json(root / "lean-out" / "s151_zzz.json", record("s151_zzz", 0))
    case("unexpected-output-id", "An output ID absent from --inputs is an infrastructure failure",
         "PARITY.md 'Unexpected output IDs ... fail with exit 2'", extra_output, 2, expect_stderr=True)

    def wrong_section(root):
        agreeing(root)
        write_json(root / "lean-out" / "s151_b_pos.json", record("s151_b_pos", 1, section=63))
    case("wrong-section", "An output carrying the wrong section is an infrastructure failure",
         "PARITY.md 'wrong sections ... fail with exit 2'", wrong_section, 2, expect_stderr=True)

    def malformed(root):
        agreeing(root)
        write_json(root / "lean-out" / "s151_b_pos.json", None, raw="{not json\n")
    case("malformed-json", "Malformed JSON is exit 2, never a mismatch and never zero mismatches",
         "PARITY.md 'Exit 2: ... malformed JSON'", malformed, 2, expect_stderr=True)

    def duplicate_keys(root):
        agreeing(root)
        write_json(root / "lean-out" / "s151_b_pos.json", None, raw=
                   '{"schema_version": 1, "input_id": "s151_b_pos", "section": 151,'
                   ' "result": 1, "result": 2}\n')
    case("duplicate-object-keys", "Duplicate JSON object keys are an infrastructure failure",
         "PARITY.md 'duplicate IDs/keys ... fail with exit 2'", duplicate_keys, 2, expect_stderr=True)

    def stem_disagrees(root):
        agreeing(root)
        write_json(root / "lean-out" / "s151_b_pos.json", record("s151_OTHER", 1))
    case("stem-id-disagreement", "The filename stem and the object's input_id must agree",
         "PARITY.md 'the filename stem and the object ID must agree'",
         stem_disagrees, 2, expect_stderr=True)

    def bad_id(root):
        agreeing(root)
        write_json(root / "inputs" / "_leading.json", record("_leading", None))
        write_json(root / "prolog-out" / "_leading.json", record("_leading", 0))
        write_json(root / "lean-out" / "_leading.json", record("_leading", 0))
    case("invalid-input-id", "IDs must match [A-Za-z0-9][A-Za-z0-9_-]*",
         "PARITY.md 'IDs match [A-Za-z0-9][A-Za-z0-9_-]*'", bad_id, 2, expect_stderr=True,
         informational=True)

    def bool_vs_int(root):
        agreeing(root)
        write_json(root / "prolog-out" / "s151_a_pos.json", record("s151_a_pos", True))
        write_json(root / "lean-out" / "s151_a_pos.json", record("s151_a_pos", 1))
    case("boolean-is-not-integer", "true and 1 are different values under strict typing",
         "PARITY.md 'booleans are not integers'", bool_vs_int, 1,
         expect_mismatch_ids=["s151_a_pos"])

    def absent_vs_null(root):
        agreeing(root)
        write_json(root / "prolog-out" / "s151_a_pos.json", record("s151_a_pos", None, omit_result=True))
        write_json(root / "lean-out" / "s151_a_pos.json", record("s151_a_pos", None))
    case("absent-key-is-not-null", "An absent key is not a null value",
         "PARITY.md 'absent keys are not null values'", absent_vs_null, 1,
         expect_mismatch_ids=["s151_a_pos"], informational=True)

    def array_order(root):
        agreeing(root)
        write_json(root / "prolog-out" / "s151_a_pos.json", record("s151_a_pos", [1, 2]))
        write_json(root / "lean-out" / "s151_a_pos.json", record("s151_a_pos", [2, 1]))
    case("array-order-matters", "Arrays retain order",
         "PARITY.md 'arrays retain order and multiplicity'", array_order, 1,
         expect_mismatch_ids=["s151_a_pos"])

    def array_multiplicity(root):
        agreeing(root)
        write_json(root / "prolog-out" / "s151_a_pos.json", record("s151_a_pos", [1, 1]))
        write_json(root / "lean-out" / "s151_a_pos.json", record("s151_a_pos", [1]))
    case("array-multiplicity-matters", "Duplicates are not collapsed",
         "PARITY.md 'Do not ... deduplicate answers'", array_multiplicity, 1,
         expect_mismatch_ids=["s151_a_pos"])

    def number_coercion(root):
        agreeing(root)
        write_json(root / "prolog-out" / "s151_a_pos.json", record("s151_a_pos", 1))
        write_json(root / "lean-out" / "s151_a_pos.json", None, raw=
                   '{"schema_version": 1, "input_id": "s151_a_pos", "section": 151, "result": 1.0}\n')
    case("no-number-coercion", "1 and 1.0 are not interchangeable",
         "PARITY.md 'Do not coerce numbers'", number_coercion, 1,
         expect_mismatch_ids=["s151_a_pos"], informational=True)

    def key_order_only(root):
        agreeing(root)
        write_json(root / "prolog-out" / "s151_a_pos.json", None, raw=
                   '{"result": {"b": 1, "a": 2}, "section": 151,'
                   ' "input_id": "s151_a_pos", "schema_version": 1}\n')
        write_json(root / "lean-out" / "s151_a_pos.json", None, raw=
                   '{"schema_version":1,"input_id":"s151_a_pos","section":151,'
                   '"result":{"a":2,"b":1}}\n')
    case("key-order-and-formatting-ignored", "Only object-key order and formatting are ignored",
         "PARITY.md 'Ignore only object-key order and JSON formatting'",
         key_order_only, 0, expect_mismatch_ids=[])

    def ordered_records(root):
        ids = ["s151_c_pos", "s151_a_pos", "s151_b_pos"]
        agreeing(root, ids=ids)
        for index, name in enumerate(ids):
            write_json(root / "lean-out" / f"{name}.json", record(name, 1000 + index))
    case("mismatch-record-order", "Mismatch records are written in input-ID order",
         "PARITY.md 'Write mismatch records in input-ID order'", ordered_records, 1,
         expect_mismatch_ids=["s151_a_pos", "s151_b_pos", "s151_c_pos"])

    def stale_report(root):
        agreeing(root)
        (root / "run").mkdir(parents=True, exist_ok=True)
        (root / "run" / "mismatches.jsonl").write_text(
            '{"input_id": "stale", "prolog": 1, "lean": 2}\n', encoding="utf-8")
    case("stale-report-is-cleared", "A successful run leaves an EMPTY mismatches.jsonl",
         "PARITY.md 'write an empty mismatches.jsonl so an old report cannot be mistaken'",
         stale_report, 0, expect_mismatch_ids=[])

    return cases


def read_mismatches(run_directory):
    path = run_directory / "mismatches.jsonl"
    if not path.exists():
        return None, "mismatches.jsonl was not written"
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [], None
    records = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            return None, f"line {number} of mismatches.jsonl is not JSON: {error}"
    return records, None


def run_case(meter, case, workspace):
    root = workspace / case.name
    run_directory = root / "run"
    root.mkdir(parents=True)
    case.build(root)
    run_directory.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable, "-B", str(meter),
        "--section", str(SECTION),
        "--inputs", str(root / "inputs"),
        "--prolog-out", str(root / "prolog-out"),
        "--lean-out", str(root / "lean-out"),
    ]
    try:
        completed = subprocess.run(command, cwd=run_directory, capture_output=True,
                                   text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, f"the meter did not finish within {TIMEOUT}s"
    except OSError as error:
        return False, f"could not invoke the meter: {error}"

    problems = []
    if completed.returncode != case.expect_exit:
        problems.append(f"exit {completed.returncode}, expected {case.expect_exit}")
    if case.expect_stderr and not completed.stderr.strip():
        problems.append("exit 2 must print a reason to stderr; stderr was empty")

    if case.expect_mismatch_ids is not None and completed.returncode in (0, 1):
        records, error = read_mismatches(run_directory)
        if error:
            problems.append(error)
        else:
            ids = [item.get("input_id") for item in records]
            if ids != case.expect_mismatch_ids:
                problems.append(f"mismatch IDs {ids}, expected {case.expect_mismatch_ids}")
            for item in records:
                missing = {"input_id", "prolog", "lean"} - set(item)
                if missing:
                    problems.append(f"record for {item.get('input_id')!r} lacks {sorted(missing)}")

    return not problems, "; ".join(problems)


GAPS = [
    ("mismatches.jsonl location", "PARITY.md says 'the invocation's working directory', so "
     "this harness runs the meter with cwd set to a dedicated run directory and reads the "
     "report from there. That is the contract's literal reading, but the real harness must "
     "be held to it too; consider pinning an explicit output path instead."),
    ("a crashed meter is indistinguishable from a completed one", "An uncaught Python "
     "exception exits 1, which is PARITY.md's 'mismatches' code. PARITY.md requires the "
     "report to be truncated only on SUCCESS, so a crash in a reused directory can present "
     "a previous run's mismatches.jsonl as this run's result. Decide whether the meter must "
     "trap unexpected exceptions and re-exit 2, and whether it must truncate the report "
     "before doing any work."),
    ("input record section vs --section", "PARITY.md fixes engine OUTPUT sections but never "
     "says whether an INPUT record whose 'section' disagrees with --section is simply not "
     "selected, or is exit 2."),
    ("what prolog and lean hold in a mismatch record", "PARITY.md says a missing side is null "
     "and an existing side is 'its full output object'. It does not say whether an ordinary "
     "value mismatch records the full objects or only the 'result' values."),
    ("definition of input-ID order", "PARITY.md requires records 'in input-ID order' without "
     "saying byte order, codepoint order, or a locale collation."),
    ("classification of envelope defects", "A missing 'result' key, a raw JSON float where "
     "DECISIONS.md requires a tagged representation, and an ID violating the published "
     "grammar are each either a mismatch (exit 1) or a malformed record (exit 2). PARITY.md "
     "does not say which. The three checks above marked INFORMATIONAL depend on this."),
    ("schema_version validation", "PARITY.md fixes schema_version to 1 but does not say "
     "whether the meter must reject another value, and with which exit code."),
    ("non-.json files in a directory", "Undefined: ignore them, or exit 2?"),
    ("nested subdirectories under --inputs", "Undefined: recurse, ignore, or exit 2?"),
    ("encoding and line endings of mismatches.jsonl", "UTF-8 is fixed for envelopes; the "
     "report's encoding, newline, and trailing-newline convention are not stated."),
    ("exit codes above 2", "Undefined. Decide whether any status other than 0, 1 and 2 is "
     "ever legal, and what the harness does when it sees one."),
    ("unreadable or absent directory", "Undefined; presumably exit 2, but it is not written down."),
    ("ID case sensitivity and 'ambiguous IDs'", "PARITY.md lists 'ambiguous IDs' as an exit-2 "
     "condition without defining the term. On a case-insensitive filesystem 's151_A' and "
     "'s151_a' are one file; on a case-sensitive one they are two. Decide whether IDs are "
     "compared case-sensitively and what makes two of them ambiguous."),
    ("shared or identical output directories", "Nothing forbids --prolog-out and --lean-out "
     "naming the same directory, or either of them naming --inputs. Decide whether that is "
     "exit 2 or is silently treated as both engines agreeing with themselves."),
]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--meter", help="path to the meter to test; never read, only invoked")
    parser.add_argument("--list-gaps", action="store_true", help="print the unresolved contract questions and exit")
    arguments = parser.parse_args(argv)

    if arguments.list_gaps:
        print("Unresolved questions in docs/contracts/PARITY.md. Each one lets two")
        print("correct-looking meters disagree. Pin them before writing the meter.\n")
        for title, detail in GAPS:
            print(f"- {title}: {detail}")
        return 0

    if not arguments.meter:
        parser.error("--meter is required unless --list-gaps is given")
    meter = Path(arguments.meter)
    if not meter.is_file():
        print(f"error: no meter at {meter}", file=sys.stderr)
        return 2

    cases = build_cases()
    passed, failed, noted = [], [], []
    with tempfile.TemporaryDirectory() as directory:
        workspace = Path(directory)
        for case in cases:
            ok, detail = run_case(meter, case, workspace)
            if ok:
                status, bucket = "ok  ", passed
            elif case.informational:
                status, bucket = "note", noted
            else:
                status, bucket = "FAIL", failed
            print(f"{status}  {case.name}")
            print(f"        {case.requirement}  [{case.citation}]")
            if not ok:
                print(f"        -> {detail}")
                if case.informational:
                    print("        -> INFORMATIONAL: PARITY.md does not fix this outcome, so this")
                    print("           result is reported, not enforced. Pin it, then re-run.")
            bucket.append(case.name)

    print(f"\n{len(passed)}/{len(cases)} contract checks passed against {meter}")
    if noted:
        print(f"{len(noted)} informational check(s) diverged: " + ", ".join(noted))
    if failed:
        print("failed: " + ", ".join(failed))
        print("\nA meter that fails any check above is out of contract; a Checkpoint 1")
        print("'zero mismatches' result from it would not mean what the gate claims.")
    print(f"\n{len(GAPS)} contract questions remain unresolved; run with --list-gaps.")
    print("Answer them in DECISIONS.md before writing the meter: docs/PLAN.md makes")
    print("'parity/check.py hash unchanged' part of the Checkpoint 1 gate, so a later")
    print("correction breaks the gate it exists to protect.")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
