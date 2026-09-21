# Phase 0 contract staging

All files here are drafts for review. The assistant never copies them into
`human/`; the human owner promotes approved artifacts and pins their hashes.
The original plan and its approved amendments are in `docs/PLAN.md` and
`docs/PROTOCOL.md`.

| Draft | Purpose or owner promotion target |
| --- | --- |
| `SOURCE.md`, `SOURCE_AUDIT.json` | Verified source provenance and case inventory |
| `HASHES.txt` | Source-only starting pin for `human/HASHES.txt`; incomplete |
| `HASHES.md` | Full protected-file manifest contract |
| `DECISIONS.md` | TODO template and hazard inventory for `human/DECISIONS.md` |
| `HAZARDS.json` | Machine-readable source hazard inventory |
| `HOUSEHOLD.md` | Evidence and questions for the shared input draft |
| `PARITY.md` | Independent comparator CLI and file contract |
| `parity/check.py` | Exit-2 placeholder for the owner-authored meter |
| `gate/exploits/README.md` | Convention for the owner-authored exploit suite |
| `invariants/statements/README.md` | Approved proposition and evidence form |
| `RUNTIME.md` | Required Prolog runtime and reproducibility boundary |

The household draft lives in `Interface/Household.lean`; approval must be recorded
in the owner's decisions before it becomes a shared implementation contract.
Placeholders are not semantic approvals, independent validation, or passed gates.
