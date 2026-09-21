#!/usr/bin/env python3
"""Retain and enforce the 376-case reference baseline, not a parity verdict."""

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import sys

from runtime import (Commands, HERE, RuntimeFailure, TZ, container, identity,
                     identity_sha256, measure, output_path, positive_seconds,
                     sha256, write_json)

VACUOUS = ("s3306_c_2_neg", "s3306_c_2_pos")
COUNT = 376


def inventory(corpus):
    cases = sorted((corpus / "cases").glob("*.pl"))
    if len(cases) != COUNT:
        raise RuntimeFailure(f"case population is {len(cases)}, expected {COUNT}; no filtering permitted")
    for path in cases:
        if path.is_symlink() or not path.is_file() or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", path.stem):
            raise RuntimeFailure(f"invalid case path: {path}")
    ids = [path.stem for path in cases]
    if not set(VACUOUS).issubset(ids):
        raise RuntimeFailure("known vacuous cases absent; source population differs")
    statutes = sorted((corpus / "statutes" / "prolog").glob("*.pl"))
    if len(statutes) != 12 or not (corpus / "statutes/prolog/init.pl").is_file():
        raise RuntimeFailure("expected the 12 original Prolog statute files including init.pl")
    for path in statutes:
        if path.is_symlink() or not path.is_file() or not re.fullmatch(r"[A-Za-z0-9_]+", path.stem):
            raise RuntimeFailure(f"invalid statute path: {path}")
    hashes = {str(p.relative_to(corpus)): sha256(p) for p in cases + statutes}
    return ids, hashes


def classify(code, stdout, stderr):
    if code in (124, 137):
        return "timeout_or_killed"
    if code != 0:
        return "process_failure"
    if stderr:
        if b"does not exist" in stderr:
            return "load_failure"
        if re.search(rb"(?m)^ERROR", stderr):
            return "error"
        if b"Goal (directive) failed" in stderr:
            return "directive_failed"
        return "other_stderr"
    if stdout:
        return "unexpected_stdout"
    return "clean"


def collect_rows(directory, ids):
    rows, problems = [], []
    unexpected = sorted(p.stem for p in directory.glob("*.status") if p.stem not in ids)
    if unexpected:
        problems.append(f"unexpected case status files: {unexpected}")
    for case_id in ids:
        row = {"id": case_id, "known_vacuous": case_id in VACUOUS,
               "exit": None, "class": "not_run", "started": (directory / f"{case_id}.started").exists()}
        raw = {}
        for stream in ("stdout", "stderr"):
            path = directory / f"{case_id}.{stream}"
            raw[stream] = path.read_bytes() if path.is_file() else b""
            row[stream] = raw[stream].decode("utf-8", errors="replace")
            row[f"{stream}_file"] = str(Path("cases") / path.name) if path.is_file() else None
            row[f"{stream}_sha256"] = sha256(path) if path.is_file() else None
        status = directory / f"{case_id}.status"
        if status.exists():
            try:
                text = status.read_text(encoding="ascii")
                if not re.fullmatch(r"[0-9]+\t[0-9]+\t[0-9]+\n", text):
                    raise ValueError("expected exit, start and end, with final newline")
                code, start, end = map(int, text.split())
                if code > 255 or end < start or not row["started"] or any(
                        row[f"{stream}_file"] is None for stream in ("stdout", "stderr")):
                    raise ValueError("inconsistent status or missing diagnostics")
                row.update(exit=code, elapsed_seconds=end - start,
                           **{"class": classify(code, raw["stdout"], raw["stderr"])})
            except (ValueError, UnicodeError) as error:
                row["class"] = "invalid_status"
                problems.append(f"{case_id}: {error}")
        elif row["started"]:
            row["class"] = "incomplete"
        rows.append(row)
    return rows, problems


def report(rows, problems, execution):
    classes = dict(sorted(Counter(row["class"] for row in rows).items()))
    observed_ids = [row["id"] for row in rows]
    if len(observed_ids) != COUNT or len(set(observed_ids)) != COUNT:
        problems.append("case results must contain 376 unique IDs")
    if sorted(row["id"] for row in rows if row["known_vacuous"]) != list(VACUOUS):
        problems.append("vacuous annotations differ from the two known cases")
    if execution.get("timed_out") or execution.get("exit") != 0:
        problems.append("container sweep failed or exceeded the total run budget")
    if classes != {"clean": COUNT}:
        problems.append(f"unexpected case outcomes: {classes}")
    return {"passed": not problems, "cases": len(rows), "classification": classes,
            "clean_outcomes": classes.get("clean", 0), "known_vacuous_cases": list(VACUOUS),
            "nonvacuous_cases": COUNT - len(VACUOUS),
            "claim": "376/376 clean directive outcomes includes 2 cases that execute no test; not 376 tested assertions.",
            "problems": problems, "execution": execution, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=HERE.parent)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--require-native", action="store_true")
    parser.add_argument("--case-timeout", type=positive_seconds, default=120)
    parser.add_argument("--run-timeout", type=positive_seconds, default=1200)
    args = parser.parse_args()
    log = None
    ids, rows = [], []
    case_dir = None
    summary = None
    try:
        out = output_path(args.out)
        log = Commands(str(out) + ".diagnostics")
        corpus = args.root.resolve() / "human/sara/sara"
        # Only source inventory is read here; no owner meter or exploits are accessed.
        ids, hashes = inventory(corpus)
        source = {"files_sha256": hashes, "input_ids": ids}
        archive = args.root.resolve() / "human/sara/SARA.tar.gz"
        source["archive_sha256"] = sha256(archive)
        write_json(log.directory / "source.json", source)
        _, commit, _ = log.run(["git", "-C", str(args.root.resolve()), "rev-parse", "HEAD"])
        run_context = {"git_commit": commit.decode("ascii").strip(),
                       "ci": {key: os.environ.get(key) for key in (
                           "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_SHA",
                           "GITHUB_REPOSITORY", "GITHUB_SERVER_URL", "RUNNER_OS", "RUNNER_ARCH")}}
        write_json(log.directory / "run_context.json", run_context)
        expected = json.loads(args.runtime.read_text(encoding="utf-8"))
        if os.environ.get("KMLA_TZ", TZ) != TZ:
            raise RuntimeFailure(f"KMLA_TZ must equal approved {TZ}; runtime TZ is never overridden")
        # Resolve a recorded local ID, then use that ID throughout (no mutable-tag race).
        current = measure(log, expected["image"]["local_image_id"], expected["image"]["tag"], args.require_native)
        write_json(log.directory / "RUNTIME.measured.json", current)
        if identity(current) != identity(expected):
            raise RuntimeFailure("runtime identity differs from the supplied record; retain a new record and sweep")
        case_dir = log.directory / "cases"
        case_dir.mkdir()
        with (case_dir / "input_ids.txt").open("x", encoding="ascii") as stream:
            stream.write("\n".join(ids) + "\n")
        image = current["image"]["local_image_id"]
        mounts = [(corpus, "/corpus", True), (HERE, "/harness", True), (case_dir, "/out", False)]
        # A separate positive loading check does not execute or alter case tests.
        files = ",".join("'" + p + "'" for p in hashes if p.startswith("statutes/"))
        goal = ("consult('statutes/prolog/init'),"
                f"(forall(member(F,[{files}]),(absolute_file_name(F,P),source_file(P)))"
                "->writeln(kmla_statutes_loaded),halt(0);halt(2))")
        smoke, stdout, stderr = container(log, image, ["swipl", "-q", "-f", "none", "-g", goal], mounts=mounts)
        if smoke["timed_out"] or smoke["exit"] != 0 or stderr or stdout != b"kmla_statutes_loaded\n":
            raise RuntimeFailure("positive statute-loading check failed; no case outcome accepted")
        execution, stdout, stderr = container(
            log, image, ["sh", "/harness/corpus_sweep.sh", str(args.case_timeout)],
            mounts=mounts, timeout=args.run_timeout)
        rows, problems = collect_rows(case_dir, ids)
        if stdout or stderr:
            problems.append("unexpected output from the sweep driver; see command diagnostics")
        _, after = inventory(corpus)
        if after != hashes:
            problems.append("source hashes changed during the run")
        summary = report(rows, problems, execution)
        summary.update(runtime=current, runtime_identity_sha256=identity_sha256(current), source=source,
                       run_context=run_context,
                       case_timeout_seconds=args.case_timeout, run_timeout_seconds=args.run_timeout,
                       diagnostics_directory=str(log.directory),
                       harness_files_sha256={p.name: sha256(p) for p in (
                           HERE / "runtime.py", HERE / "runtime_probe.sh", HERE / "run_corpus.py",
                           HERE / "corpus_sweep.sh", HERE / "run_corpus.sh")})
        write_json(out, summary)
        print(f"{summary['clean_outcomes']}/{COUNT} clean directive outcomes; "
              f"2 known vacuous cases, 374 nonvacuous cases. {'PASS' if summary['passed'] else 'FAIL'}")
        return 0 if summary["passed"] else 1
    except (RuntimeFailure, OSError, ValueError, KeyError, IndexError) as error:
        if log is not None:
            if case_dir is not None:
                rows, _ = collect_rows(case_dir, ids)
            else:
                rows = [{"id": case_id, "class": "not_run", "exit": None} for case_id in ids]
            failure = {"passed": False, "error": str(error), "cases": len(ids), "rows": rows,
                       "diagnostics_directory": str(log.directory)}
            write_json(log.directory / "failure.json", failure)
            if not args.out.exists():
                write_json(args.out, failure)
        print(f"FAIL: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
