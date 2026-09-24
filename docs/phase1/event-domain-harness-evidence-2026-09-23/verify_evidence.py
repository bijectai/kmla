"""Independent read-only accounting of this A-023 lane's retained evidence."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from harness import facts, runtime
from harness.swipl import IMAGE

HERE = Path(__file__).resolve().parent
GROUPS = ("domain-regressions", "list-regressions", "country-regressions", "full-audit")


def read(path):
    return json.loads(path.read_text())


def check_domain(data):
    # Canonical tagged JSON is an independent identity key, not a sort of the
    # domain. The original traversal order remains visible in this list.
    expected, seen = [], set()
    for unary in data["unary"]:
        term = unary["event"]
        key = json.dumps(term, sort_keys=True, separators=(",", ":"))
        if key not in seen:
            seen.add(key)
            expected.append(term)
    assert expected == data["event_domain"]
    assert data["stats"]["unary_proofs"] == len(data["unary"])
    assert data["stats"]["distinct_event_domain"] == len(expected)
    stored_unary = [x for x in data["household"]["facts"] if len(x["args"]) == 1]
    assert stored_unary == [{"ctor": x["predicate"], "args": [x["event"]]} for x in data["unary"]]
    assert data["fact_source_clauses"] == sorted(data["fact_source_clauses"])
    assert len(data["fact_source_clauses"]) == len(data["household"]["facts"])
    assert data["stats"]["fact_count"] == len(data["household"]["facts"])
    assert data["stats"]["stipulation_count"] == len(data["household"]["stipulations"])


def main():
    baseline = read(HERE / "baseline.json")
    for name, sha in baseline["historical_files_sha256"].items():
        assert runtime.sha256(ROOT / name) == sha, name
    for old in baseline["old_code"].values():
        assert hashlib.sha256(old["source"].encode()).hexdigest() == old["sha256"]

    directory = HERE / "full-audit"
    rows, summary, code = [read(directory / name) for name in
                           ("all-376-statuses.json", "summary.json", "audit-code.json")]
    paths = sorted((ROOT / "human/sara/sara/cases").glob("*.pl"))
    assert len(rows) == len(paths) == 376
    assert [r["original_case"] for r in rows] == [p.name for p in paths]
    assert len(set(code["execution_order"])) == 376
    assert set(code["execution_order"]) == {p.name for p in paths}
    assert code["execution_order"][0] == "tax_case_33.pl"
    assert all(runtime.sha256(p) == code["source_files_sha256"][p.name] for p in paths)
    for name in (directory / "audit-code.json", HERE / "domain-regressions/correction-code.json"):
        for path, sha in read(name)["hashes"].items():
            assert runtime.sha256(ROOT / path) == sha, path
    for field in ("h4_3_a", "h4_3_b"):
        assert dict(Counter(r[field] for r in rows)) == summary[field + "_counts"]
    assert dict(Counter(r["direct_country"]["status"] for r in rows)) == summary["direct_country_counts"]
    measured_names = {r["original_case"] for r in rows if "source_sha256" in r}
    assert measured_names == set(code["execution_order"][:summary["attempted_original_count"]])
    households, totals = [], Counter()
    for row in rows:
        measurements = {}
        for label in ("original", "reground"):
            key = label + "_measurement"
            if key in row:
                data = read(directory / (Path(row[key]).stem + ".measurement.json"))
                measurements[label] = data
                totals[label + "_facts"] += len(data["household"]["facts"])
                totals[label + "_stipulations"] += len(data["household"]["stipulations"])
                if label == "original":
                    households.append(facts.encode(facts.from_value(data["household"])))
        if row["h4_3_a"] == "pass":
            assert measurements["original"]["household"] == measurements["reground"]["household"]
        if row["h4_3_b"] == "pass":
            observed = row["observation_comparison"]
            left, right = observed["original"], observed["serialized"]
            if row["h6_observation"]["kind"] == "tax_first_solution":
                assert left["status"] == right["status"] == "first_solution"
                assert left["value"] == right["value"]
            else:
                assert left["canonical"] == right["canonical"]
        if row["h4_3_b"].startswith("unimplemented:"):
            assert row["h6_observation"]["kind"] == "unimplemented"
            assert row["observation_comparison"]["owner_choice_blocker"] is False
    assert len(households) == summary["diagnostic_household_instances"]
    assert len(set(households)) == summary["diagnostic_distinct_ordered_households"]
    assert Counter(hashlib.sha256(h).hexdigest() for h in households) == Counter(summary["diagnostic_household_sha256"])

    mount_counts, domain_counts, identity, process_exits, process_timeouts = {}, {}, set(), {}, {}
    for name in GROUPS:
        base = HERE / name
        record = read(base / "identity.json")
        identity.add(record["runtime_identity_sha256"])
        assert record["image"] == IMAGE
        assert record["runtime_record_sha256"] == runtime.sha256(ROOT / "docs/contracts/RUNTIME.json")
        assert record["manifest_sha256"] == runtime.sha256(ROOT / "human/HASHES.txt")
        assert record["decisions_sha256"] == runtime.sha256(ROOT / "human/DECISIONS.md")
        assert record["household_wire_sha256"] == runtime.sha256(ROOT / "Interface/HOUSEHOLD_WIRE.md")
        for path, sha in record["harness_sha256"].items():
            assert runtime.sha256(ROOT / "harness" / path) == sha
        for path, sha in record["source_files_sha256"].items():
            assert runtime.sha256(ROOT / "human/sara/sara" / path) == sha
        for path, sha in read(base / "candidate-code.json")["hashes"].items():
            assert runtime.sha256(ROOT / path) == sha
        count, timeouts, exits = 0, 0, Counter()
        for command in sorted((base / "commands").glob("*.command.json")):
            meta = read(command)
            argv = meta["argv"]
            exits[str(meta["exit"])] += 1
            if meta["timed_out"]:
                # A bounded audit timeout is a retained finding, never a pass.
                assert name == "full-audit" and summary["finding"] is not None
                timeouts += 1
            if argv[:2] != ["docker", "run"]:
                continue
            assert IMAGE in argv and "--read-only" in argv
            assert argv[argv.index("--network") + 1] == "none"
            mounts = [argv[i + 1] for i, arg in enumerate(argv) if arg == "--mount"]
            assert f"type=bind,src={ROOT}/human,dst=/human,readonly" in mounts
            if argv[argv.index("--entrypoint") + 1] == "swipl":
                assert f"type=bind,src={ROOT}/human/sara/sara,dst=/corpus,readonly" in mounts
                count += 1
        mount_counts[name], process_exits[name] = count, dict(exits)
        process_timeouts[name] = timeouts
        measured = sorted(base.glob("*.measurement.json"))
        for path in measured:
            check_domain(read(path))
        domain_counts[name] = len(measured)
    assert len(identity) == 1
    result = {
        "original_population_exact_and_unchanged": 376,
        "attempted_original_count": summary["attempted_original_count"],
        "h4_3_a_counts": summary["h4_3_a_counts"], "h4_3_b_counts": summary["h4_3_b_counts"],
        "direct_country_counts": summary["direct_country_counts"],
        "diagnostic_household_instances": len(households),
        "diagnostic_distinct_ordered_households": len(set(households)),
        "record_count": summary["record_count"], "distinct_household_count": summary["distinct_household_count"],
        "list_totals": dict(totals), "source_and_lane_code_hashes_unchanged": True,
        "historical_files_byte_unchanged": len(baseline["historical_files_sha256"]),
        "legacy_code_snapshots_sha256_verified": len(baseline["old_code"]),
        "all_measurements_unary_proof_and_distinct_domain_checks": domain_counts,
        "pinned_prolog_readonly_mount_checks": mount_counts,
        "retained_process_exit_counts": process_exits,
        "retained_process_timeout_counts": process_timeouts,
        "runtime_identity_sha256": next(iter(identity)), "finding": summary["finding"],
    }
    runtime.write_json(HERE / "accounting.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
