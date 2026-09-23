# Oracle proof obligations

## §7703 authorized resumed proof round, 2026-09-23

Dev authorized one bounded proof-only round on the three existing assertions,
followed by continued §7703 translation. This supersedes the earlier stop for
this round only. No change to any assertion type, input fixture, expected
literal, shared Interface, or semantic decision is authorized.

The pre-round snapshot is `6e3cdc920fa1c1433aad0b29f4348f7dad55c86a`.
All THREE pre-round goal states and complete compiler diagnostics are preserved
by reference in [S7703_PREROUND_GOALS_2026-09-23.txt](../docs/phase1/S7703_PREROUND_GOALS_2026-09-23.txt).
The old failed attempts remain in the historical oracle progress report and
committed tests; no prior failure is erased by restarting this ledger.

| Obligation | Pre-round location | Latest status | Resumed failed edit cycles |
| --- | --- | --- | --- |
| b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity | diagnostic line 6; original test 227–235 | CLOSED R1; latest goals: none | 0 |
| a1_null_only_at_observation | diagnostic error at original test 257 | CLOSED R1; latest goals: none | 0 |
| b3_deduplication_only_at_observation | diagnostic error at original test 266 | CLOSED R3; latest goals: none | 2 |

### Attempt ledger

- R0: read A-018 completely and full pre-round diagnostics. No proof edit.
  Its year-only admission/date-parser claim is incorrect: these queries have
  no supplied concrete Day. Those two tests establish only actual query-year
  rejection. No broad string/date reduction claim follows from them.
- D1: prepare a bounded diagnostic ladder in `Tests/S7703ProofDiagnostics.lean`
  with `maxRecDepth 10000`, `maxHeartbeats 1000000`, ordinary evaluation of both
  exact observations, a kernel concrete guard proof, and paired rfl/decide
  checks for escaping, encoding, sorting and deduplication. Both actual
  observations equal the unchanged expected literals under `#eval`; the
  concrete Int guard proves by `decide`. All ten direct rfl/decide observation
  ladder proofs fail at those tested resource limits. Full results:
  [S7703_PROOF_DIAGNOSTICS_R0.txt](Tests/S7703_PROOF_DIAGNOSTICS_R0.txt).
  This diagnostic source intentionally remains non-compiling and is not
  imported into the main suite or accepted as a proof artifact. It has no
  emitted olean. Its recovered proof terms are not evidence. Reproduction of
  an unchanged command to capture full diagnostics is not an edit cycle.
- R1: only proof bodies/resource limits changed on the three original tests.
  b1 adds `have hguard : (364 : Int) ≤ 2 * (min 16618 16800 - 16436) := by decide`
  to the existing simplification: PASS. a1 uses the existing string-fold
  equality plus the singleton mergeSort equation under local maxRecDepth
  10000: PASS. b3 analogously attempts unfolding mergeSort/merge: FAIL,
  residual foldr/mergeSort over splitInTwo projections. Full latest-at-R1
  goals: [S7703_PROOF_ROUND_R1.txt](Tests/S7703_PROOF_ROUND_R1.txt).
- R2: b3 only, adds splitInTwo/splitAt/merge/ite_self simplification: FAIL,
  residual foldr over mergeSort of `List.splitAt.go` projections. Full
  latest-at-R2 goals: [S7703_PROOF_ROUND_R2.txt](Tests/S7703_PROOF_ROUND_R2.txt).
  b1/a1 unchanged and still pass. b3 now has two failed edit cycles, not three.
- R3: b3 only, replaces mergeSort implementation unfolding with
  `rw [List.mergeSort_of_pairwise (by simp)]` after the existing encoder/fold
  equations; final `decide`: PASS. All 53 original theorems pass; no remaining
  original goal. [S7703_PROOF_ROUND_R3.txt](Tests/S7703_PROOF_ROUND_R3.txt).
  All three printed proof axiom sets are exactly a subset of X1, with no
  recovery axiom. The unused `List.merge` warning in a1 is harmless and retained;
  no extra edit cycle was spent on cosmetic cleanup.
- C1, after the bounded proof round: add only the two missing §7703 clause
  compositions and nine tests. Source compile and complete 62-theorem main
  suite PASS on the first attempt. All providers remain universally quantified
  in tests. [S7703_CONTINUATION_C1.txt](Tests/S7703_CONTINUATION_C1.txt).
- Final: rebuild every current shared dependency and S7703 in fresh retained
  `/private/tmp/kmla-oracle7703-resumed.BbKIpl`, then compile the complete main
  test file: all commands exit 0. Exact commands/output:
  [S7703_FINAL_VERIFICATION.txt](Tests/S7703_FINAL_VERIFICATION.txt).
  `ruby Oracle/Tests/check_s7703_assertions.rb` exits 0 and verifies byte identity
  of the three assertion declarations through `:= by`, including fixtures at
  the use sites and expected literals, plus all 24 original fixture definitions.
  [S7703_ASSERTION_IDENTITY.txt](Tests/S7703_ASSERTION_IDENTITY.txt) preserves
  their exact text and SHA-256 values. None of those assertions was weakened.
- Orchestrator final coordination: its independent fresh runner also exits 0
  for this nine-clause-body/62-theorem snapshot, with raw output retained at
  `docs/phase1/s7703-continuation-final-2026-09-23/001.*`; its independent check
  reports all 53 old theorem statements byte-identical. No proof/implementation
  edit follows that confirmation. Main owns STATE/HANDOFF and any commit.

### A-018 hypotheses checked, not adopted as authority

The concrete Int guard suggestion was sufficient for b1. At the diagnostic
limits actually tested (10000/1000000), rfl and decide both failed on direct
string/observation examples, including opaqueFix/WellFounded reduction. This
does not prove failure at every larger limit or establish a shared semantic
defect. Existing proved fold and sort lemmas suffice for both unchanged actual
assertions; no Interface replacement is needed. The year-only admission tests
do not exercise `Day.fromISO?` or establish date-parser reduction.

### Still open: implementation and general proof obligations

- Required ordered `s152_a_1/3` provider, downstream stipulations and full
  recursive evaluation. Parameterized b1, b and root statute bodies are not a
  completed reference, even though their finite compositions compile.
- Root H4 append/unification/freshening, with unbound spouse/marriage retained
  as actual variables for subsequent calls. No arbitrary finite ground universe
  can stand in for all wildcard solution pairs. No root Bool entry is supplied.
- All remaining source modes, including free taxpayer/bound spouse; full
  operational mode census and E2 unbound-year exclusion. New root bodies only
  handle bound Taxp/Year, free Marriage, free-or-bound Spouse.
- Real OracleGuards and exact V10 eligible-pair decider; correspondence to
  source prefixes, universe coverage (facts/stipulations/bound queries), strict
  phase/decrease and branch-depth/counter adequacy. No recursive fuel is added.
- Every R5/R8 actual-year/Workday path and admission proof. The new compositions
  pass the same CoveredR5Time (.year year) into b1; they do not implement R8 or
  certify that every operational call path has been covered.
- General calendar/year-test/source equivalence and reference parity. All
  376 original cases and CP1 remain unpassed. The independent H4 investigation
  is neither inspected nor resolved here.

No new breaker or obligation-review escalation is required by this successful
proof round. If another breaker occurs, send evidence to the orchestrator for
Fable DESIGN-FLAW REVIEW OF THE OBLIGATION pending explicit consultation
approval; do not invoke Fable or bypass the denied Q-020 invocation.

No production OracleGuards or downstream provider is supplied. All source
equivalence, full operational coverage and R5/R8 adequacy obligations remain
open. A passing local proof is neither reference parity nor CP1.

Circuit breaker: three failed edit cycles on one test means stop and report.
If any original obligation reaches three failures in this resumed round, stop
edits to that obligation and request Fable DESIGN-FLAW REVIEW OF THE OBLIGATION;
there is no fourth cycle. Other authorized §7703 translation may continue.

Final self-review: assume signed ordered SLD/duplicate semantics, mode-sensitive
nonvar and identity, committed first -> condition, binding-free existential NAF,
exact atom/string tags, signed date/aggregate rules and boundary-only observation
deduplication. H4 freshening, all remaining modes and general R5/R8 adequacy are
still obligations, not assumptions of completion. No dependency was mocked and
no fuel-exhaustion value was introduced. The bounded handoff is finished.

Circuit breaker: three failed edit cycles on one test means stop and report.
