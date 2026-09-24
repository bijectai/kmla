# Q-021 integration verification — 2026-09-23

## Consultation and authority

Dev authorized Q-021 and standing consultations with per-call scope audits.
A-021 confirms the country_/2 omission is an implementation defect under H1/H3,
not an H4 amendment. No new semantic choice or protected installation follows.
The review and authorization are committed at `9d741c1` on
`claude/checkpoint-0-integration`.

The all-path before/after audit includes ignored files, git metadata, modes and
opaque content digests. No other repository writer ran during the consult.
Only A-021 and an append to DECISION_LOG changed; all prior answers were
unchanged. The retained audit is
`docs/consult/evidence/q021-path-audit-2026-09-23.json`. The manifest verified
afterward. The independent meter's source was never inspected.

## Independent integration baseline

Raw commands, exits and complete streams are retained under
`q021-integration-checks-2026-09-23/`. These ran before integrating the country
regressions; they do not establish any new H4 comparison or reference parity.

| Command | Result |
| --- | --- |
| `python3 -B scripts/test_runner_boundary.py -v` | 12 tests pass |
| `python3 -B scripts/test_runtime.py -v` | 29 tests pass |
| `bash scripts/check_interface.sh` | 115 behavioural guards pass |
| `bash scripts/check_query_time.sh` | 175 signatures match; admission/coverage tests and proofs pass |
| `bash scripts/check_oracle7703.sh` | Existing partial implementation and 62 theorem tests compile |
| `ruby Oracle/Tests/check_s7703_assertions.rb` | Three protected assertions and 24 fixtures byte-identical |
| `python3 -B scripts/human_manifest.py verify` | Every protected file listed and digest-matching |

The oracle check retains its required dependency parameters and open obligations.
It is not a complete §7703 reference, proof of source equivalence, production
guard implementation or Checkpoint 1 result.

## Completed country integration

The final independent run is retained under
`q021-independent-country-final-2026-09-23/`: all **14/14** originals pass
H4.3(a), H4.3(b), and direct supplied-country preservation. The 11 unit tests,
three fixed expected-output regressions, and six runtime guard groups pass.
The implementation/test hashes are identical before and after that run.
Source-index placement preserves tags/order/multiplicity; ordinary event
traversal is unchanged; country rules and non-ground clauses fail closed.

The original and serialized A-positive observation are both exactly
`[[{"a":"alice"},{"a":"bob"}]]`. The B-positive omission control replaces
the tagged location with `null`: one tuple added and one lost, **not** a net
increase in proof count. B-negative remains empty. The permanent regressions
assert these measured results without changing the H4 comparison.

`q021-independent-runtime-2026-09-23/` retains an independent pass of the old
country diagnostic (comparisons unchanged) and both tax_case_33 comparisons:
1,736 facts, first result 27181. Its scoped candidate still performs 49,612
two-input calls and yields 157 proofs; this is not protected installation.
The old diagnostic's static scope description was subsequently corrected;
its independent historical run is kept as-is, and the harness's final rerun
records the description-only update.

The broader unit command passes **103 tests** with `PYTHONPATH=scripts`, covering
reader, facts, grounding, country regression, observations, meter invocation,
runtime and runner boundary. Raw output is in
`q021-unit-regressions-2026-09-23-corrected-invocation/`. The first invocation
omitted that import path and failed importing `parity_conformance`; its full
trace remains in `q021-unit-regressions-2026-09-23/`. No test or implementation
was changed to fix the invocation. This is not a claim that every repo test ran.

These are 14 diagnostic Household instances, **13 distinct ordered/tagged
Households**. Production `record_count` and `distinct_household_count` remain
not produced; reference parity remains 0/376. The full corpus audit and missing
H6 observation plumbing remain builder work, not a new missing owner choice.
The isolated oracle context continues the bounded root stipulation append and
freshening work, with the actual §152 provider and R5 proofs still explicit/open.

## Subsequent §7703 integration check

The new root bffb/bbfb assemblies retain the statute's ordered solutions before
the stipulated clauses. The latter use shared `Pat` values, ground-input
unification and a threaded fresh-id supply; they do not inherit statute-only
guards. This is a section-local implementation, not a new wire schema or a
general relational engine. The §152 dependency, other operational modes,
production guards, and R5 termination/adequacy remain open.

`q021-oracle-stip-independent-2026-09-23/` retains a fresh Lean 4.33.1 build:
**62 existing + 25 new theorems compile**. The main test file is byte-unchanged
from the entry snapshot. Implementation, both test files and runner hashes are
unchanged across the independent execution. The runner unconditionally compiles
the new `Oracle/S7703Stip.lean` dependency and both required assertion files;
any compilation/proof failure remains nonzero. No skipped or weakened test,
dummy production provider, default guards, parity or complete-reference claim.

The staged whitespace check reports one extra final blank line in the raw
`Oracle/Tests/S7703_STIP_ROOT_BUILD.txt` transcript. It is retained verbatim;
no proof/source/test comparison is affected, and no clean whole-diff whitespace
result is claimed for that raw log.

## Self-review

G4 tags, H1 source order and proof multiplicity, G5 closed-world negation, H6.2
observation-only sorting/deduplication, and the pinned interpreter remain the
semantics. A-021 distinguishes the positive read that removes the A solution
from the B branch where omission can add a solution. Neither a fixed point nor
an unaffected query alone proves preservation of inert facts.

No proof assertion was changed in these checks. Three failed edit cycles on one
test require a stop and report; a runtime error is never an ordinary answer.
Any new semantic choice or consult scope violation halts the affected lane.
Checkpoint 1 remains unpassed, and no work under human/ is authorized.
