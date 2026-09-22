#!/usr/bin/env python3
"""Diagnostic only: evaluate original appended clause bodies, inspect time values.

Does not supply a production grounding implementation, query-mode proof or Valid
certificate. Preserve streams, identities and every case; never write human/.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
import json
from pathlib import Path
import re

from run_birth_audit import HERE, ROOT, FIXES, runtime, sha

# Argument positions from the original predicate heads; this table is only an
# audit classification, not a new call mode or producer schema. Arity-only
# artifact signatures are included, even when no time field exists.
TIME = {
    "s63/3": ([2], []), "s7703/4": ([4], []), "s3306_b/8": ([], []),
    "s2_b/3": ([3], []), "s2_a/3": ([3], []), "s151_c_applies/3": ([3], []),
    "s152_c_1/3": ([3], []), "s3306_c/5": ([5], [4]), "s151/5": ([5], []),
    "s151_d/4": ([4], []), "s151_b_applies/3": ([3], []), "s151_c/4": ([4], []),
    "s151_b_applies/2": ([], []), "total_wages_employer/6": ([], [5, 6]),
    "s68_b/3": ([3], []), "s152_c_2/4": ([], [3, 4]), "s152_c/3": ([3], []),
    "s152_b_2/4": ([4], []), "s3306_a/2": ([2], []), "s63_c_1/3": ([2], []),
    "s63_c_2/3": ([2], []), "s63_c_3/3": ([3], []), "s63_f_1_A/2": ([2], []),
    "s63_f_1_B/3": ([3], []), "s63_d/4": ([4], []), "s152_c_3/3": ([3], []),
    "s2_a/5": ([5], [3, 4]), "s152_d_2_H/6": ([3], [5, 6]),
    "s63_c/3": ([2], []), "s63_c_3/4": ([4], []), "s151_b/3": ([3], []),
}


def analyze(rows):
    counts = {"cases": len(rows), "cases_with_stipulations": 0, "fact_clauses": 0,
              "rule_clauses": 0, "solutions": 0, "year_values": 0, "day_values": 0,
              "wild_time_values": 0}
    issues, wilds, unresolved, years, days, signatures = [], [], [], set(), set(), set()
    for row in rows:
        if row["status"] != "ok" or row["stderr"]:
            unresolved.append({"id": row["id"], "status": row["status"], "stderr": row["stderr"]})
            continue
        if row["clauses"]:
            counts["cases_with_stipulations"] += 1
        for clause in row["clauses"]:
            counts[clause["kind"] + "_clauses"] += 1
            for solution in clause["solutions"]:
                counts["solutions"] += 1
                sig = f"{solution['predicate']}/{solution['arity']}"
                signatures.add(sig)
                if sig not in TIME:
                    issues.append({"id": row["id"], "unknown_signature": sig})
                    continue
                for kind, positions in zip(("year", "day"), TIME[sig]):
                    for position in positions:
                        arg = solution["args"][position - 1]
                        record = {"id": row["id"], "signature": sig, "position": position,
                                  "kind": kind, "argument": arg, "source": clause["source"]}
                        if arg["kind"] == "wild":
                            counts["wild_time_values"] += 1
                            wilds.append(record)
                            continue
                        counts[kind + "_values"] += 1
                        if kind == "year":
                            valid = arg["kind"] == "int" and 1900 <= arg["value"] <= 2100
                            if arg["kind"] == "int":
                                years.add(arg["value"])
                        else:
                            valid = False
                            if arg["kind"] == "str" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", arg["value"]):
                                try:
                                    d = date.fromisoformat(arg["value"])
                                    valid = date(1900, 1, 1) <= d <= date(2100, 12, 31)
                                    days.add(arg["value"])
                                except ValueError:
                                    pass
                        if not valid:
                            issues.append(record)
    return {"counts": counts, "signatures": sorted(signatures), "unresolved": unresolved,
            "out_of_range_or_wrong_kind": issues, "wild_time_arguments": wilds,
            "distinct_years": sorted(years), "distinct_days": sorted(days),
            "scope": "Original appended clauses evaluated with all head positions unbound; wild time fields retained, not treated as bounded. Not operational call-site coverage."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if Path(args.out).name != args.out or args.out in (".", ".."):
        parser.error("--out must be a new basename")
    signed = (ROOT / "human/DECISIONS.md").read_text()
    table = signed.split("| Stipulated predicate |", 1)[1].split("* H4.2", 1)[0]
    expected = set(re.findall(r"\| `([^`]+/\d+)` \|", table))
    if expected != set(TIME) or len(TIME) != 31:
        raise RuntimeError("audit table differs from the 31 signed H4.1 signatures")
    out = runtime.output_path(HERE / args.out)
    out.mkdir()
    approved = json.loads((ROOT / "docs/contracts/RUNTIME.json").read_text())
    live = runtime.measure(runtime.Commands(out / "runtime"), approved["image"]["tag"], approved["image"]["tag"])
    runtime.write_json(out / "runtime_measured.json", live)
    if runtime.identity(live) != runtime.identity(approved):
        raise RuntimeError("measured runtime identity differs")
    image = live["image"]["local_image_id"]
    mounts = [(ROOT / "human", "/human", True), (ROOT / "human/sara/sara", "/corpus", True), (HERE, "/audit", True)]
    check, raw, err = runtime.container(runtime.Commands(out / "mounts"), image,
                                       ["sh", "-c", "cat /proc/self/mountinfo"], mounts=mounts)
    inspected = {f[4]: f[5] for f in map(str.split, raw.decode().splitlines()) if f[4] in ("/human", "/corpus", "/audit")}
    if check["exit"] != 0 or err or set(inspected) != {"/human", "/corpus", "/audit"} or any(
            "ro" not in v.split(",") for v in inspected.values()):
        raise RuntimeError("read-only mounts not established")
    cases = sorted((ROOT / "human/sara/sara/cases").glob("*.pl"))
    if len(cases) != 376:
        raise RuntimeError("population differs from 376")
    if args.smoke:
        names = {"s3306_c_2_neg", "s3306_c_2_pos", "s152_c_1_A_pos", "s2_a_1_A_neg", "s3301_pos"}
        cases = [p for p in cases if p.stem in names]
    runtime.write_json(out / "metadata.json", {
        "runtime_identity_sha256": runtime.identity_sha256(live), "mounts": inspected,
        "source_sha256": {p.name: sha(p) for p in cases}, "time_positions": TIME,
        "statutes": {p.name: sha(p) for p in sorted((ROOT / "human/sara/sara/statutes/prolog").glob("*.pl"))},
        "diagnostics": {p.name: sha(p) for p in (Path(__file__), HERE / "stip_time_audit.pl", HERE / "birth_audit.pl", HERE / "run_birth_audit.py")},
        "smoke_only": args.smoke, "original_test_directives_executed": False})

    def run(path):
        source = path.read_bytes()
        offset = -1
        if path.name in FIXES:
            if sha(path) != FIXES[path.name]:
                raise RuntimeError("H4.4 source hash changed")
            offset = len(b"".join(source.splitlines(keepends=True)[:26]).rstrip(b"\r\n"))
        status, stdout, stderr = runtime.container(runtime.Commands(out / path.stem), image,
            ["swipl", "-q", "-f", "none", "-s", "/audit/stip_time_audit.pl", "-g", "stip_time_audit:main",
             "--", "/corpus/cases/" + path.name, str(offset)], mounts=mounts, timeout=120)
        if status["exit"] == 0 and not status["timed_out"]:
            try:
                result = json.loads(stdout)
            except ValueError:
                result = {"status": "invalid_json"}
        else:
            result = {"status": "execution_failed"}
        result.update(id=path.stem, source_sha256=sha(path), execution=status, stderr=stderr.decode(errors="replace"))
        if path.read_bytes() != source:
            raise RuntimeError("source changed during diagnostic")
        runtime.write_json(out / path.stem / "audit.json", result)
        return result

    rows = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(run, p) for p in cases]):
            row = future.result()
            rows.append(row)
            if len(rows) % 50 == 0 or row["status"] != "ok":
                print(f"completed {len(rows)}/{len(cases)}; {row['id']}: {row['status']}", flush=True)
    rows.sort(key=lambda r: r["id"])
    runtime.write_json(out / "all_results.json", rows)
    summary = analyze(rows)
    runtime.write_json(out / "summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "wild_time_arguments"}, indent=2), flush=True)
    if summary["unresolved"] or summary["out_of_range_or_wrong_kind"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
