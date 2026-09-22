#!/usr/bin/env python3
"""Draft-only analysis of retained diagnostics; does not install a V-rule."""
import hashlib
import json
from pathlib import Path
from run_birth_audit import cycle_components

root = Path(__file__).resolve().parent
source = root / "full-20260922-01" / "all_results.json"
raw = source.read_bytes()
records = json.loads(raw)
assert len(records) == 378 and all(r["status"] == "ok" for r in records)
originals = [r for r in records if r["population"] == "original"]
assert len(originals) == 376
cyclic_age_graphs = []
checks = 0
for record in originals:
    for year in range(1900, 2101):
        edges = [(e["taxpayer"], e["dependent"])
                 for e in record["k_age_checks"] if year in e["c3_success_years"]]
        cycles = cycle_components(edges)
        checks += 1
        if cycles:
            cyclic_age_graphs.append({"id": record["id"], "year": year, "cycles": cycles})
print(json.dumps({
    "draft_only": True,
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "originals": len(originals),
    "a_excluded": [r["id"] for r in originals if r["refined_a_components_hit"]],
    "K_and_c3_graphs_checked": checks,
    "K_and_c3_cycles": cyclic_age_graphs,
    "B_limit": "E is a subgraph of K-and-c3; no separate full-corpus E enumeration claimed.",
    "c_excluded": [{"id": r["id"], "cycles": r["k_cycle_components"]}
                   for r in originals if r["k_cycle_components"]],
    "witnesses": [{"id": r["id"],
                   "A_failures": r["refined_a_components_hit"],
                   "B_prefix_edges_2018": r["witness_c1_prefix_edges_2018"],
                   "C_cycles": r["k_cycle_components"]}
                  for r in records if r["population"] == "witness"]
}, indent=2))
