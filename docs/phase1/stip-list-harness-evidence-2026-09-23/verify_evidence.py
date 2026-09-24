"""Read-only cross-check of this lane's retained measurements and counts."""
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


def read(path):
    return json.loads(path.read_text())


def main():
    directory = HERE / "full-audit"
    rows = read(directory / "all-376-statuses.json")
    summary = read(directory / "summary.json")
    code = read(directory / "audit-code.json")
    paths = sorted((ROOT / "human/sara/sara/cases").glob("*.pl"))
    assert len(rows) == len(paths) == 376
    assert [r["original_case"] for r in rows] == [p.name for p in paths]
    assert len(set(code["execution_order"])) == 376
    assert set(code["execution_order"]) == {p.name for p in paths}
    assert all(runtime.sha256(p) == code["source_files_sha256"][p.name] for p in paths)
    assert all(runtime.sha256(ROOT / name) == sha for name, sha in code["hashes"].items())
    for field in ("h4_3_a", "h4_3_b"):
        assert dict(Counter(r[field] for r in rows)) == summary[field + "_counts"]
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
                assert data["stats"]["fact_count"] == len(data["household"]["facts"])
                assert data["stats"]["stipulation_count"] == len(data["household"]["stipulations"])
                if label == "original":
                    households.append(facts.encode(facts.from_value(data["household"])))
        if row["h4_3_a"] == "pass":
            assert measurements["original"]["household"] == measurements["reground"]["household"]
        if row["h4_3_b"] == "pass":
            observed = row["observation_comparison"]
            a, b = observed["original"], observed["serialized"]
            if row["h6_observation"]["kind"] == "tax_first_solution":
                assert a["status"] == b["status"] == "first_solution" and a["value"] == b["value"]
            else:
                assert a["canonical"] == b["canonical"]
    assert len(households) == summary["diagnostic_household_instances"]
    assert len(set(households)) == summary["diagnostic_distinct_ordered_households"]
    assert Counter(hashlib.sha256(h).hexdigest() for h in households) == Counter(summary["diagnostic_household_sha256"])

    mount_counts, identity = {}, set()
    for name in ("lists-final", "syntax-final", "country-final", "full-audit"):
        base = HERE / name
        record = read(base / "identity.json")
        identity.add(record["runtime_identity_sha256"])
        assert record["image"] == IMAGE
        assert record["manifest_sha256"] == runtime.sha256(ROOT / "human/HASHES.txt")
        assert record["decisions_sha256"] == runtime.sha256(ROOT / "human/DECISIONS.md")
        assert record["household_wire_sha256"] == runtime.sha256(ROOT / "Interface/HOUSEHOLD_WIRE.md")
        assert all(runtime.sha256(ROOT / "harness" / file) == sha for file, sha in record["harness_sha256"].items())
        count = 0
        for command in sorted((base / "commands").glob("*.command.json")):
            meta = read(command)
            argv = meta["argv"]
            if argv[:2] != ["docker", "run"]:
                continue
            assert IMAGE in argv and "--read-only" in argv
            assert argv[argv.index("--network") + 1] == "none"
            mounts = [argv[i + 1] for i, arg in enumerate(argv) if arg == "--mount"]
            assert f"type=bind,src={ROOT}/human,dst=/human,readonly" in mounts
            if argv[argv.index("--entrypoint") + 1] == "swipl":
                assert f"type=bind,src={ROOT}/human/sara/sara,dst=/corpus,readonly" in mounts
                count += 1
        mount_counts[name] = count
    assert len(identity) == 1
    result = {
        "original_population_exact_and_unchanged": 376,
        "h4_3_a_counts": summary["h4_3_a_counts"], "h4_3_b_counts": summary["h4_3_b_counts"],
        "direct_country_counts": summary["direct_country_counts"],
        "diagnostic_household_instances": len(households),
        "diagnostic_distinct_ordered_households": len(set(households)),
        "record_count": summary["record_count"], "distinct_household_count": summary["distinct_household_count"],
        "list_totals": dict(totals), "source_and_lane_code_hashes_unchanged": True,
        "pinned_prolog_readonly_mount_checks": mount_counts,
        "runtime_identity_sha256": next(iter(identity)), "finding": summary["finding"],
    }
    runtime.write_json(HERE / "accounting.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
