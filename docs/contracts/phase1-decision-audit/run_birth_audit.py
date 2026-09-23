#!/usr/bin/env python3
"""DRAFT diagnostic. Run with python3 -B; all writes stay beside this script.

No producers, installed domain rules, oracle imports or original test execution.
An output directory must be new; successful measurements and raw streams persist.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "harness"))
import runtime

FIXES = {
    "s3306_c_2_neg.pl": "20ac10863992b937b3aff70b79ac1c27fa101a555a45feeb21f01c4f0374097e",
    "s3306_c_2_pos.pl": "1b912b348ef4481643a509a920bd6653522571dd9c1f29673d2ad2280c478d88",
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def cycle_components(edges):
    """Tarjan SCCs on audit-only edges; returns nontrivial SCCs and self loops."""
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set())
    index, low, stack, active, components = {}, {}, [], set(), []

    def visit(v):
        index[v] = low[v] = len(index)
        stack.append(v)
        active.add(v)
        for w in sorted(graph[v]):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            component = []
            while True:
                w = stack.pop()
                active.remove(w)
                component.append(w)
                if w == v:
                    break
            if len(component) > 1 or v in graph[v]:
                components.append(sorted(component))

    for v in sorted(graph):
        if v not in index:
            visit(v)
    return sorted(components)


def annotate(data):
    if data.get("status") != "ok":
        return data
    by_person = {}
    by_event = {}
    for birth in data["births"]:
        event = birth["event"]
        by_event.setdefault(event, set()).update(birth["starts"])
        for person in birth["agents"]:
            by_person.setdefault(person, set()).add(event)
    # Zero is a measured count for the recorded domain, never a fabricated fact.
    data["birth_events_per_person"] = [
        {"person": p, "events": sorted(by_person.get(p, ())), "count": len(by_person.get(p, ()))}
        for p in data["domain"]]
    data["start_dates_per_birth_event"] = [
        {"event": e, "dates": sorted(ds), "count": len(ds)} for e, ds in sorted(by_event.items())]
    data["multiple_birth_events"] = [r for r in data["birth_events_per_person"] if r["count"] > 1]
    data["multiple_birth_start_dates"] = [r for r in data["start_dates_per_birth_event"] if r["count"] > 1]
    data["k_self_edges"] = [a for a, b in data["k_edges"] if a == b]
    data["k_cycle_components"] = cycle_components(data["k_edges"])
    data["v4_cycle_components"] = cycle_components(data["child_parent_edges"])
    data["equal_birth_k_related"] = [r for r in data["equal_birth_pairs"]
                                     if r["k_left_to_right"] or r["k_right_to_left"]]
    data["earlier_a_components_hit"] = [key for key in ("multiple_birth_events", "multiple_birth_start_dates",
                                                "equal_birth_k_related", "k_self_edges") if data[key]]
    data["refined_a_edge_failures"] = [r for r in data["k_age_checks"]
                                      if r["c3_success_years"] and not r["proposed_condition"]]
    data["refined_a_components_hit"] = [key for key in (
        "multiple_birth_events", "multiple_birth_start_dates", "refined_a_edge_failures") if data[key]]
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="new directory basename under this draft directory")
    parser.add_argument("--smoke", action="store_true", help="two witnesses and two H4.4 cases only")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if Path(args.out).name != args.out or args.out in (".", ".."):
        parser.error("--out must be a new basename")
    out = runtime.output_path(HERE / args.out)
    out.mkdir()
    approved = json.loads((ROOT / "docs/contracts/RUNTIME.json").read_text())
    live = runtime.measure(runtime.Commands(out / "runtime"), approved["image"]["tag"],
                           approved["image"]["tag"])
    runtime.write_json(out / "runtime_measured.json", live)
    if runtime.identity(live) != runtime.identity(approved):
        raise RuntimeError("whole measured runtime identity differs from approved record")
    image = live["image"]["local_image_id"]
    mounts = [(ROOT / "human", "/human", True),
              (ROOT / "human/sara/sara", "/corpus", True),
              (HERE, "/audit", True),
              (ROOT / "docs/consult/evidence", "/evidence", True)]
    check, raw, err = runtime.container(runtime.Commands(out / "mounts"), image,
                                        ["sh", "-c", "cat /proc/self/mountinfo"], mounts=mounts)
    if check["exit"] != 0 or err:
        raise RuntimeError("mount inspection failed")
    inspected = {}
    for line in raw.decode().splitlines():
        fields = line.split()
        if fields[4] in ("/human", "/corpus", "/audit", "/evidence"):
            inspected[fields[4]] = fields[5]
    if set(inspected) != {"/human", "/corpus", "/audit", "/evidence"} or any(
            "ro" not in options.split(",") for options in inspected.values()):
        raise RuntimeError(f"readonly mounts not established: {inspected}")
    paths = sorted((ROOT / "human/sara/sara/cases").glob("*.pl"))
    if len(paths) != 376:
        raise RuntimeError(f"case population is {len(paths)}, expected 376")
    if args.smoke:
        paths = [p for p in paths if p.name in FIXES]
    jobs = [(p, "/corpus/cases/" + p.name, "original") for p in paths]
    for name in ("r5_sibling_cycle", "r5_multibirth_cycle"):
        jobs.append((ROOT / "docs/consult/evidence" / (name + ".pl"),
                     "/evidence/" + name + ".pl", "witness"))
    hashes = {str(p.relative_to(ROOT)): sha(p) for p, _, _ in jobs}
    runtime.write_json(out / "metadata.json", {
        "draft_only": True, "runtime_identity_sha256": runtime.identity_sha256(live),
        "mounts": inspected, "sources": hashes,
        "statutes": {p.name: sha(p) for p in sorted((ROOT / 'human/sara/sara/statutes/prolog').glob('*.pl'))},
        "diagnostics": {p.name: sha(p) for p in (Path(__file__), HERE / 'birth_audit.pl')},
        "original_test_directives_executed": False,
        "per_input_outer_timeout_seconds": 120, "per_input_inference_limit": 500000000,
        "smoke_only": args.smoke})

    def run(job):
        path, mounted, kind = job
        data = path.read_bytes()
        offset = -1
        if path.name in FIXES:
            if sha256(data).hexdigest() != FIXES[path.name]:
                raise RuntimeError(f"H4.4 source identity changed: {path}")
            offset = len(b"".join(data.splitlines(keepends=True)[:26]).rstrip(b"\r\n"))
        log = runtime.Commands(out / path.stem)
        status, stdout, stderr = runtime.container(log, image,
            ["swipl", "-q", "-f", "none", "-s", "/audit/birth_audit.pl", "-g", "birth_audit:main",
             "--", mounted, str(offset), kind], mounts=mounts, timeout=120)
        if status["exit"] == 0 and not status["timed_out"]:
            try:
                result = json.loads(stdout)
            except ValueError:
                result = {"status": "invalid_json"}
        else:
            result = {"status": "execution_failed"}
        result.update(id=path.stem, population=kind, source_sha256=sha256(data).hexdigest(),
                      h44_offset=offset, stderr=stderr.decode("utf-8", errors="replace"), execution=status)
        if path.read_bytes() != data:
            raise RuntimeError(f"source changed during diagnostic: {path}")
        annotate(result)
        runtime.write_json(out / path.stem / "audit.json", result)
        return result

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, job) for job in jobs]
        for f in as_completed(futures):
            result = f.result()
            results.append(result)
            if len(results) % 25 == 0 or result["status"] != "ok":
                print(f"completed {len(results)}/{len(jobs)}; {result['id']}: {result['status']}", flush=True)
    results.sort(key=lambda r: (r["population"], r["id"]))
    runtime.write_json(out / "all_results.json", results)
    summary = {}
    for population in ("original", "witness"):
        rs = [r for r in results if r["population"] == population]
        ok = [r for r in rs if r["status"] == "ok"]
        summary[population] = {"attempted": len(rs), "ok": len(ok),
            "unresolved": [{"id": r["id"], "status": r["status"]} for r in rs if r["status"] != "ok"],
            **{key: [r["id"] for r in ok if r[key]] for key in (
                "multiple_birth_events", "multiple_birth_start_dates", "equal_birth_pairs",
                "equal_birth_k_related", "k_self_edges", "k_cycle_components", "v4_cycle_components",
                "earlier_a_components_hit", "refined_a_edge_failures", "refined_a_components_hit")}}
    runtime.write_json(out / "summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
