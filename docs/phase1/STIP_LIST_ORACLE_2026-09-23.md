# §7703 recursive stipulation-list Oracle handoff

The bounded adaptation is complete. The main-owned combined runner exits 0 on
pinned Lean 4.33.1 for **62 existing + 25 existing stipulation + 35 new list
assertions**. The 87 existing assertion declarations remain byte-identical to
shared-boundary commit `eeea5f9`. This is a local kernel-check result, not full
reference coverage, Prolog parity or Checkpoint 1.

## Scope and implementation

Work is on `claude/checkpoint-0-integration`, isolated to the Oracle §7703 lane.
The required root/Oracle instructions, PLAN, PROTOCOL, HANDOFF and STATE were
read. Semantic authority used here is `human/DECISIONS.md`, the checked shared
`Interface/`, and the dispatch's public pinned-runtime observations. No harness
or generator implementation, tests or reports, consultation evidence, owner
meter source or gate exploits were inspected. The mandated status/handoff
documents were read without following their links into the other lane.

`Oracle/S7703Stip.lean` now uses the shared `StipArg` throughout. Structurally
recursive freshening traverses head positions left to right and list elements
depth first, using one source-id/renamed-id table for the whole clause. A nested
occurrence aliases the same source id inside or outside another list. The next
unused id continues across clauses and caller-threaded invocations. Repeated
clauses retain separate fresh copies; failed matching clauses still consume
their allocated ids as before.

The implemented bffb/bbfb modes constrain only ground scalar taxpayer, optional
ground scalar spouse and integer year. A `.list` head at a constrained position
fails ordinary unification, including `.list []` against scalar atom `[]`.
Bindings remain scalar, and recursive resolution substitutes them at every
aliased output leaf. It preserves all list containers, tags, order and element
duplicates. It neither needs nor implements general variable/list unification.

`Oracle/S7703.lean` retains `StipArg` results through both root assemblies and
observation adapters. Statute rows precede stipulated rows, including the bbfb
statute's existing two nonvar successes. The structurally recursive
`stipArgObs` maps lists to `Obs.arr` and unbound leaves to null; it preserves
nested/empty arrays, rather than narrowing outputs to scalar `Pat`. `Term`,
event `Pat`, query tuples, admission and time requirements are unchanged.

No semantic decision, revised design, protected installation, new human
deliverable or consultation was needed for this authorized representation
correction. Main retains status/consultation/runner ownership. This lane made
no edits to Interface, human, status, consultation, scripts or git metadata,
and performed no installs, commits, pushes or PR actions.

## Assertions and verification

`Oracle/Tests/S7703StipLists.lean` contains 35 new named assertions, all with
axiom printouts. They cover recursive and cross-position aliases, late year
binding, bound/later spouse binding, each scalar-input/list rejection, empty
list versus atom/string, exact large integers, tags, traversal allocation,
fresh duplicate clauses and calls, failed-head isolation, unrelated signatures,
statute-first assembly, list-valued free spouse, and recursive observation
with duplicate elements and duplicate solution rows.

Main confirmed that `scripts/check_oracle7703.sh` unconditionally compiles the
new file alongside the old two files. This lane used that runner without
editing it. The final command was:

```sh
set -o pipefail
bash scripts/check_oracle7703.sh 2>&1 | tee Oracle/Tests/S7703_STIP_LIST_COMBINED_R3.txt
```

Final exit: 0. Fresh build location reported by the runner:
`/var/folders/nb/1nmz4lr56rz3wcmmcgglfyx00000gn/T//kmla-s7703.PM08eM`.
The installed compiler identity measured in the first fresh build is
`Lean 4.33.1, arm64-apple-darwin24.6.0,
commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release`.
No other toolchain was installed or used.

All final printed axiom sets are subsets of `propext`, `Classical.choice`,
`Quot.sound`; no recovery axiom remains. `stipArgObs`, `rootBffbSolutions`
and `rootBbfbSolutions` have no axioms. The earlier unchanged unused-simp
warning in the 62-test file remains. No partial definition, sorry,
native_decide, axiom declaration or fake production dependency was introduced.

The complete 62-test file remains byte-identical, SHA-256
`096ac907f363dd7d780787662a75544f271c4dd698b3598f582cd59283e3fa67`.
In the 25-test file, only two proof-body simplification arguments changed from
`patObs` to `stipArgObs`; every assertion, fixture and expected value is intact.
The preservation check compared both complete files to `eeea5f9`, allowing
exactly those two substitutions, and separately compared all 87 declaration
headers through their proof delimiter. Results and hashes:
[S7703_STIP_LIST_ASSERTION_IDENTITY.txt](../../Oracle/Tests/S7703_STIP_LIST_ASSERTION_IDENTITY.txt).

## Failed attempts retained

| Attempt | Result | Retained evidence |
| --- | --- | --- |
| R1 | Helper/root and 62 tests pass; 23/25 old stipulation tests pass. Two observation proofs still unfold `patObs`, leaving the new observer unreduced. | [Full goals/axioms](../../Oracle/Tests/S7703_STIP_LIST_BUILD_R1.txt) |
| R2 | Source syntax error: documentation comment before `mutual`; tests not reached. | [Full diagnostic](../../Oracle/Tests/S7703_STIP_LIST_COMBINED_R2.txt) |
| R3 | Comment moved inside mutual block; all 122 assertions pass. | [Final complete output and axiom sets](../../Oracle/Tests/S7703_STIP_LIST_COMBINED_R3.txt) |

R1's compiler recovery terms, including its printed recovery axiom, are retained
failed evidence and are not accepted proof artifacts. R3 has no failed goals.
The new 35 assertions pass on their first reached compilation. Each of the two
affected old tests has one executed failed edit cycle; conservatively including
the source-blocked R2 gives two failed build cycles before the pass, never three.
The prior worker's service-compaction interruption is not a proof failure.

A first ad-hoc assertion scanner printed
`assertion change: Oracle/Tests/S7703.lean`: it mistakenly required 62 `:= by`
proofs, overlooking the existing direct `:= checked.year_covered` proof. The
complete file hash was unchanged. The corrected scanner accounts for that
existing proof form and additionally checks whole-file equality with only the
two permitted proof-body substitutions. Its final result is 62/62 and 25/25
unchanged; no assertion was edited in response to that checker error.

## Remaining obligations and self-review

The real ordered §152 continuation, missing root/source modes, non-ground caller
inputs and general relational continuations, production OracleGuards, exact
V10 decider iff, finite-participant coverage, phase/decrease/fuel adequacy and
complete operational R5/R8 coverage remain explicit/open in
[Oracle/UNPROVED.md](../../Oracle/UNPROVED.md). Actual-tuple query admission and
actual-year certificates remain required by the entry wrappers. No default
certificate, fake provider, fuel-exhaustion answer or later section was added.
These finite structural traversals do not discharge recursive statute proofs.
No original cases or production parity records were compared in this lane.

Prolog assumptions: signed ordered SLD solutions and multiplicity; one variable
identity shared throughout a head, including nested lists; fresh identities
for separate copied solutions and invocations; tag-sensitive scalar equality;
finite proper lists preserving structure/order/duplicates and distinct from
the scalar atom `[]`; H4 statute-before-stipulation append; H6 boundary-only
null, sorting and solution deduplication. The supported input constraints are
ground scalars, so variable-to-list binding and occurs-check behavior are not
assumed implemented. Existing NAF, commitment, date and aggregate behavior was
not revised.

Circuit breaker: **three failed edit cycles on one test means stop and report;
no fourth edit or weakened assertion.** It did not fire in this adaptation.
