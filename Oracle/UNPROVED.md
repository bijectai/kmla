# Oracle proof obligations

## §7703 stipulated-root slice — 2026-09-23 current continuation

The explicitly authorized bffb/bbfb H4 append/head-unification/freshening slice
is implemented and checked. This section updates the historical root-stipulation
absence recorded below; it does not close the remaining modes, actual provider,
general source equivalence or R5/R8 obligations. The previous ledger is preserved.

- Implementation uses existing shared Pat results and a threaded next-unused
  Nat id. No new shared type/payload, Interface edit or private parallel public
  schema was introduced. Main confirmed that this internal supply does not by
  itself require a new shared payload field. Callers must thread the returned
  supply and not reset it while earlier outputs remain live.
- H4.1: statute rows precede ordered stipulated rows. A fresh renaming table and
  binding environment are used per clause invocation; duplicate clauses remain
  separate, repeated ids within a head retain identity, and bound constraints
  from taxpayer/spouse/year propagate to shared outputs with G4 tags intact.
  Stipulated heads are not subjected to statute-only guards/NAF. No ground
  universe substitutes for an unbound variable. Observation alone emits null.
- Two new entry wrappers require exact QueryCall admission and actual-year
  CoveredR5Time plus the real provider parameter. `admitted_shape` proves head
  well-formedness from existing admission; malformed arity is not filtered into
  ordinary failure. No OracleGuards instance or provider implementation exists.

### Bounded attempt ledger and latest goals

1. Helper build R1 failed at lines 95–96: `Unknown constant
   Bool.and_eq_true.mp`. Complete raw diagnostics and all preceding dependency
   commands: [S7703_STIP_BUILD_R1.txt](Tests/S7703_STIP_BUILD_R1.txt). This was an
   elaboration error, not an observation mismatch or a weakened assertion.
2. Helper build R2 uses the existing equality lemma via simplification of the
   same arity premise. Exit 0; [S7703_STIP_BUILD_R2.txt](Tests/S7703_STIP_BUILD_R2.txt).
   Latest helper goals: none. One failed helper edit cycle, no breaker.
3. Root assembly/entry compile: exit 0 on first attempt;
   [S7703_STIP_ROOT_BUILD.txt](Tests/S7703_STIP_ROOT_BUILD.txt).
4. Initial 24 focused theorems: all pass on first attempt;
   [S7703_STIP_TEST_R1.txt](Tests/S7703_STIP_TEST_R1.txt). Added one bbfb shared
   marriage binding assertion and full new-theorem axiom printouts; no original
   or focused assertion was changed. Final focused suite: 25/25, exit 0.
5. Final fresh build `/private/tmp/kmla-oracle7703-stip-final.y3qRdj`: all shared
   dependencies, helper, S7703, original 62 theorems, and new 25 theorems exit 0.
   Full exact commands/output/hashes:
   [S7703_STIP_FINAL_VERIFICATION.txt](Tests/S7703_STIP_FINAL_VERIFICATION.txt).
   All printed new declaration/proof axiom sets are subsets of X1; no recovery
   axiom. Latest test goals: none. Failed test edit cycles in this slice: zero.
6. Main independently reports its fresh runner unconditionally builds the helper
   and both test modules, passes 62+25 theorems, and preserves implementation/test
   hashes during verification. Evidence:
   `docs/phase1/q021-oracle-stip-independent-2026-09-23/`. This is main's check,
   not a run performed or inspected by this lane. No further implementation or
   next-section work follows this bounded handoff.

The entire original `Tests/S7703.lean` is byte-unchanged, SHA-256
`096ac907f363dd7d780787662a75544f271c4dd698b3598f582cd59283e3fa67` before/after.
Its existing unused-simp warning is retained. Historical diagnostic failure
files remain historical failures; they were not edited or used as proofs.

### Still owed after this slice

- Actual ordered s152_a_1 provider and downstream recursive implementation;
  the new assemblies remain parameterized, not a complete reference.
- Other root modes, non-ground caller inputs/general relational continuations,
  operational mode census, E2 exclusion and H6 Bool entry/integration. The two
  implemented modes have ground Taxp/Year, ground-or-free Spouse, free Marriage;
  the bffb query has two distinct free output variables.
- General source/unification/freshness correspondence and every caller's supply
  threading. The quantified one-clause supply theorem and finite focused tests
  do not prove the full cross-section operational invariant.
- Production OracleGuards, exact V10 decider iff, complete participant universe,
  phase/decrease/counter adequacy and R5/R8 actual-time coverage. Nat id allocation
  is not recursion fuel; there is no fuel-exhaustion answer or default provider.
- Opaque integration through main only; no original comparison or parity record
  was produced. All 376-case parity and CP1 remain unpassed.

No consult or git action occurred. Main owns consultations/status and runner
integration. The NEW report is
`docs/phase1/ORACLE_7703_STIP_PROGRESS_2026-09-23.md`; the old report is untouched.

Self-review: signed ordered SLD/multiplicity, structural tagged ground equality,
same-variable identity inside a head, fresh clause variables across invocations,
ground-input head unification, failure-local bindings, H4 statute-before-fact
append, and H6 boundary-only null/deduplication are the assumptions. Existing
NAF/commit/date/aggregate semantics are unchanged. Complete R5/reference behavior
is not assumed. Three failed edit cycles on one test means stop and report;
no fourth attempt or assertion weakening.

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
