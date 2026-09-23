# §7703 isolated oracle progress — 2026-09-23

Current status: this bounded §7703 handoff is complete and main has independently
reviewed and verified the final 62-theorem state. All three protected assertions
are closed unchanged; nine clause bodies comprise six independent clauses and
three parameterized bodies, not a complete reference. Downstream providers,
root stipulation/mode completion and R5/R8 proofs remain open; parity and CP1
remain unpassed. UNPROVED.md preserves the attempt ledger. No further code edits
or test runs are needed for this handoff; main owns the commit. Historical text
below is preserved.

## Final authorized continuation — current handoff

**Pinned fresh build and the complete 62-theorem main test file PASS.** All
three protected assertions are closed without changing their types, fixtures,
or expected literals. Nine source clause bodies are now represented: **six
independent executable clauses and three explicitly parameterized bodies**.
This is NOT a completed §7703 reference. No recursive provider, full root,
reference parity, hygiene-gate pass or CP1 pass is claimed.

This current section supersedes the historical stopped report retained below.
Dev authorized exactly one resumed proof-only round on snapshot
`6e3cdc920fa1c1433aad0b29f4348f7dad55c86a`, then a bounded §7703 continuation.
The round is finished: b1 and a1 passed R1; b3 failed R1 and R2, then passed
R3. There was **no repeated breaker and no fourth attempt**. The new composition
and its nine additional tests passed on their first compile/test attempt.
No further proof/implementation edits followed the final verification.

### Scope and changed paths

Re-read root/lane rules and the required PLAN/PROTOCOL/HANDOFF/STATE documents,
A-018 completely, the original §7703 source and relevant signed decisions.
Only this section was implemented. No later-section implementation was begun.
Original later-section call-site context was read only to establish §7703 modes.
No harness/gen implementation, tests, implementation reports, meter source,
gate exploits or the H4 investigation were inspected. No human/ write,
Interface edit, STATE/HANDOFF edit, consult invocation, git commit/push/PR/merge,
or owner-attribution change was made. The orchestrator's runner was not edited.

Changed in this resumed turn:

- `Oracle/S7703.lean`: add b composition and root statute clause body/mode
  specializations; preserve the existing seven bodies and five entry wrappers.
- `Oracle/Tests/S7703.lean`: proof-only changes to the three protected tests,
  nine new universally parameterized continuation tests and axiom printouts.
- `Oracle/UNPROVED.md`: complete pre-round references, attempt ledger, latest
  goals/status, corrected A-018 hypotheses, and open implementation/proof debts.
- `Oracle/Tests/S7703ProofDiagnostics.lean`: retained diagnostic ladder, not
  imported into the main test suite and intentionally still non-compiling.
- `Oracle/Tests/check_s7703_assertions.rb`: read-only byte-identity check against
  the pinned snapshot; no git writes.
- Retained raw evidence under `Oracle/Tests/`: `S7703_PROOF_DIAGNOSTICS_R0.txt`,
  `S7703_PROOF_ROUND_R1.txt`, `S7703_PROOF_ROUND_R2.txt`,
  `S7703_PROOF_ROUND_R3.txt`, `S7703_CONTINUATION_C1.txt`,
  `S7703_ASSERTION_IDENTITY.txt`, `S7703_FINAL_VERIFICATION.txt`.
- This dated oracle report. `S7703Reduction.lean` was rerun, not edited.

Final implementation SHA-256:
`0e0f11c6fe72c42e9b936c85039a129783710ae8ce8d540f3b1e0cf1b403df54`.
Final main test SHA-256:
`096ac907f363dd7d780787662a75544f271c4dd698b3598f582cd59283e3fa67`.
The five shared/source hashes in the historical identity table below were
rechecked and are unchanged. Other concurrently modified/untracked paths belong
to the orchestrator and were neither edited nor treated as this lane's work.

### Proof round, unchanged assertions and last goals

The full original three goal states remain at
`docs/phase1/S7703_PREROUND_GOALS_2026-09-23.txt`, referenced in UNPROVED.
No historical failure or recovery term has been recast as a successful proof.

| Original assertion | Successful proof change | Resumed failed edit cycles | Latest goals |
| --- | --- | --- | --- |
| b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity | Prove the exact concrete Int-min guard, then existing simplification | 0; closed R1 | None |
| a1_null_only_at_observation | Existing fold equation and singleton sort equation; local maxRecDepth 10000 | 0; closed R1 | None |
| b3_deduplication_only_at_observation | Existing fold equation, then List.mergeSort_of_pairwise, then decide | 2; closed R3 | None |

R1 b3's residual involved splitInTwo projections inside mergeSort; R2's involved
`List.splitAt.go` projections inside mergeSort/foldr. Their **full**, untruncated
goals and recovery-axiom printouts are retained in the R1/R2 files above. R3 and
the final build contain no error or recovery axiom for the original assertions.
All three printed axiom sets are within X1: propext, Classical.choice, Quot.sound.

The diagnostic ladder evaluates both actual observations to the unchanged
expected literals and proves the concrete guard. Its ten direct rfl/decide
encoding/observation examples fail at the limits tested (maxRecDepth 10000,
maxHeartbeats 1000000). That is not a mismatch or a proof of failure at all
higher limits. The diagnostic file is a reproducible failure record, not a
passing test artifact; it emits no accepted olean and its recovered proofs are
never imported. No skip/xfail or altered expected result was introduced.

A-018's b1 arithmetic suggestion was verified. Its year-only admission examples
**do not exercise date parsing**: they check the supplied year, not Day.fromISO?.
No broad string/date reduction claim follows. Existing proved string/sort lemmas
closed the actual observation goals; no shared implementation change was needed.

`ruby Oracle/Tests/check_s7703_assertions.rb` exits 0. It checks all 24 original
fixture definitions and these exact declarations through `:= by` byte-for-byte;
their verbatim text is retained in `S7703_ASSERTION_IDENTITY.txt`:

| Assertion | SHA-256 of exact declaration through `:= by` |
| --- | --- |
| b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity | `94ad637a8ef8ccb7a421a873d2e4fb91a01b08115e68a41bc083ca3ce8b23b2a` |
| a1_null_only_at_observation | `38fe92b93a06de672777e086244871f9c7719e97ba970756ff6b3a7854bd864c` |
| b3_deduplication_only_at_observation | `5aea04698b8ae18b730f7edeb3db9c8af9eb9b155cc0d68999ab6f9a57f26300` |

The orchestrator additionally reports its independent comparison of all 53 old
theorem statements as byte-identical and its fresh runner exit 0, with raw output
at `docs/phase1/s7703-continuation-final-2026-09-23/001.*`. That report is recorded
as orchestrator verification, not a run performed by this lane. Its earlier
intermediate b3 failure is compatible with this ledger and was not an edit cycle.

### Current clause/mode and hazard coverage

One definition per original clause; each predicate has one source statute
clause. Definition layout follows Lean dependency order, not a changed Prolog
clause order. Within each body, ordered flatMap/disjunction retains duplicates.

| Source lines | Clause | Current boundary |
| --- | --- | --- |
| 2–9 | s7703/4 | Parameterized STATUTE BODY only: bffb, bbfb; no full root/stipulation append |
| 12–14 | s7703_a/4 | Independent bffb, bound a2 outputs filtered inside NAF |
| 17–82 | s7703_a_1/5 | Independent bfffb, Option Day preserves unbound S13 |
| 85–98 | s7703_a_2/5 | Independent bfffb, exact decree string tags |
| 103–106 | s7703_b/3 | Parameterized bfb composition, bbb equality-filter specialization |
| 110–139 | s7703_b_1/4 | Parameterized bffb, required actual-year s152_a_1 continuation |
| 142–184 | s7703_b_2/4 | Independent bbfb, two ordered findall lists and sums |
| 187–201 | membership/3 | Independent bbb, one Unit per proof |
| 203–216 | s7703_b_3/4 | Independent bfbb, ordered 184-day membership proofs |

The new root body requires bound Taxp/Year and free Marriage. A free Spouse gives
one nonvar-disjunction success; a bound Spouse gives two, except that bound
identity fails at the next source literal. Ground results of a are filtered
according to the requested Spouse binding before NAF. Tests distinguish those
modes, the repeated guard × fact multiplicity, wrong spouse, same person, and
atom/string identity. These modes do not silently stand in for free-Taxp or
bound-Marriage modes. No new reference entry wrapper is exposed for the partial
root. The existing five wrappers still consume exact-tuple AdmittedQuery, and
b1's wrapper also requires the actual-year certificate and dependency.

**NAF 8/8** annotated exactly once: section7703.pl sites
9:2 (new parameterized N-CALL), 14:2 (N-CALL), 30:13, 50:6, 61:6,
129:13, 195:4 (N-ABS-DATE), 113:2 (N-CONJ). Rules N1/N4, N2 and N5
are cited at the respective definitions. **AGG 5/5** annotated exactly once:
143:5, 162:2, 205:5 (A1 findall, including D8 at 205); 180:2, 181:2
(A2/M8 sums). **CUT 0/0** explicit ! sites. The three -> sites (45, 62,
67) retain separately annotated G1 first-condition commitment semantics.
This is annotation/body coverage, not a formal source-equivalence proof.

### Exact pinned final commands and results

Working directory: `/Users/devrashie/Documents/csProjects/kmla`.
`mktemp -d /private/tmp/kmla-oracle7703-resumed.XXXXXX` created the retained
fresh directory `/private/tmp/kmla-oracle7703-resumed.BbKIpl`. No prior oleans
were used in the final build. Full commands and outputs are retained in
`Oracle/Tests/S7703_FINAL_VERIFICATION.txt`.

```sh
lean +leanprover/lean4:v4.33.1 --version
mkdir -p /private/tmp/kmla-oracle7703-resumed.BbKIpl/Interface /private/tmp/kmla-oracle7703-resumed.BbKIpl/Oracle
LEAN_PATH=/private/tmp/kmla-oracle7703-resumed.BbKIpl lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703-resumed.BbKIpl/Interface/Household.olean Interface/Household.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-resumed.BbKIpl lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703-resumed.BbKIpl/Interface/QuerySchema.olean Interface/QuerySchema.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-resumed.BbKIpl lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703-resumed.BbKIpl/Interface/QueryTime.olean Interface/QueryTime.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-resumed.BbKIpl lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703-resumed.BbKIpl/Oracle/S7703.olean Oracle/S7703.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-resumed.BbKIpl lean +leanprover/lean4:v4.33.1 Oracle/Tests/S7703.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-resumed.BbKIpl lean +leanprover/lean4:v4.33.1 Oracle/Tests/S7703Reduction.lean
ruby Oracle/Tests/check_s7703_assertions.rb
```

Every command exits 0. Lean identity: 4.33.1, arm64-apple-darwin24.6.0,
commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, Release. Main suite:
**62/62** theorem declarations (53 old + 9 new), with one harmless unused
`List.merge` simp-argument warning, retained without suppressing the linter.
All nine clause bodies, five existing entries, new mode specializations,
three protected proofs and nine new proofs have printed dependencies within
X1; no full hygiene/axiom-gate execution is claimed. Diagnostic failure logs
remain failures, separately identified above.

### Remaining obligations and next integration need

1. Implement and prove the actual ordered s152_a_1 provider in its future fresh
   section context, including downstream stipulations. The universally quantified
   continuation here is not that implementation or its termination proof.
2. Complete the root's H4 ordered stipulated append, relational unification and
   variable freshening, retaining unbound spouse/marriage for later bindings.
   A ground statute list is not the full predicate. Do not apply statute guards
   to appended facts, invent a finite universe of wildcard pairs, or identify
   wildcard ids across independent clause invocations. Further root modes and
   the H6 Bool target remain absent, not false-valued stubs.
3. Prove source-prefix/eligible-decider equivalence, operational modes and E2
   exclusion, complete participant universe, V10 born/birthless phase decrease,
   branch counter and phase/entry offsets. No fuel or exhaustion result is added.
   No production OracleGuards instance exists.
4. Cover every actual R5/R8 time path. All three parameterized bodies pass the
   same CoveredR5Time (.year year) unchanged; this proves no Workday/R8 coverage
   and does not reset or manufacture a descendant budget.
5. Prove general calendar/year-extraction and source correspondence; these
   self-contained tests are not reference comparisons or coverage of all admitted
   inputs. The separate H4 grounding issue remains outside this lane.
6. Orchestrator: next request is **opaque harness CLI integration**, with exact
   tuples/outputs/diagnostics only, for the four independent queried modes
   a1/bfffb, a2/bfffb, b2/bbfb, b3/bfbb after real admission/payload wiring.
   Parameterized b1/root must remain unsupported until their actual providers
   and proofs exist. Do not output []/false/null for missing work. Main owns
   STATE/HANDOFF, coordination, and any authorized checkpoint commit.

No Prolog reference invocation or opaque parity run occurred here: 0/376 original
cases compared, zero parity records. **All 376-case parity and CP1 remain
unpassed.** No Fable call was attempted after the reported permission denial.
There is no new failed obligation requiring an escalation from this round.

---

## Historical pre-resumption report — superseded, retained as failure evidence

Everything below through the historical self-review describes the earlier
stopped snapshot, not the current compilation/authorization status. Its original
attempts and exact failure evidence are preserved; the current outcome is above.

**Status: substantive implementation compiles; test proof circuit breaker
triggered. No completed §7703 target, reference parity or CP1 pass.**

The lane stopped after three failed proof attempts on the same three test
statements. No fourth attempt, assertion change, test deletion, Interface edit,
or alternate implementation was made. The failed tests remain visible in the
non-compiling test file. Lean's error-recovery `sorryAx` terms are NOT accepted
proofs and must not be imported or used as evidence. No test `.olean` was emitted.

The orchestrator must record this stop under `STATE.md` → `Blockers` and route
the question below through its next available Fable consult number. This lane
was explicitly restricted to Oracle §7703 files, Oracle tests, and this report;
it did not edit STATE/HANDOFF or allocate a Q number.

Subsequent orchestrator direction separately holds integration for a newly
reproduced H4 grounding contract issue while Fable review runs. This lane did
not inspect that investigation and makes no inference about its resolution.
Shared semantics remain unchanged. The opaque integration request below is
deferred pending that hold as well as the local proof stop; no additional
implementation or later-section work is authorized by this report.

## Scope and identity

Read root AGENTS, PLAN, PROTOCOL, HANDOFF, STATE, then Oracle/AGENTS; read the
whole original `section7703.pl`, its applicable signed semantic decisions and
the shared Household/QueryTime/QuerySchema types. Only §7703 was translated.
No harness/gen source, tests or implementation reports, meter source, or gate
exploits were inspected. Original source and `human/` were read-only. Existing
shared-file changes were preserved. No commits, pushes, PRs or merges occurred.

Entry HEAD: `b80a807fea2e1ff66a361766049579e931a55fc5`.

| Input | SHA-256 at verification |
| --- | --- |
| human/DECISIONS.md | `12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a` |
| human/sara/sara/statutes/prolog/section7703.pl | `37f5ad90cbfea12e47b6c91068f93edd02980cd88f3a1caacfdf79b4263e81e3` |
| Interface/Household.lean | `a78d9fd26639f2f6e1f771fbabbaf988d519a2dc0234ba546aa4d5e7d4f78007` |
| Interface/QueryTime.lean | `a80d422cf771a1a385a8155ae7fcd1236b850ca8e9158ad24d49664c6fa74991` |
| Interface/QuerySchema.lean | `6011b30293c3cdb83f51ece3587daa6d0e02990495825580bdc143681bbe1c66` |

These identify the actual uncommitted shared Interface used, not merely HEAD.
The owner's A/WIRE installation and preflight authorization were accepted as
given; neither was reopened as a semantic choice.

Files added:

- `Oracle/S7703.lean` — seven clause definitions, six executable and one with
  an explicit later-section dependency; five typed admission wrappers.
- `Oracle/Tests/S7703.lean` — 53 theorem declarations; 50 elaborated without
  errors, three proofs remain failed. The whole command exits 1, not a pass.
- `Oracle/Tests/S7703Reduction.lean` — core Lean declaration diagnostics;
  final diagnostic command exits 0, without proving any failing test.
- This report.

Implementation SHA-256:
`0261827399bac447d71c76e915bc1519a798a4f6e60222cfbfd22fe46dc19995`.
Test SHA-256:
`930758520c4bf963c7d1c592064715df6511e3075e17e1699f6e657fb2815b2f`.
Diagnostic SHA-256:
`86ba9ea74ad711a9df1dfb05257d73cac6f93f6a797014d5b9b105100f238f99`.

## Clause and mode coverage

Every translated clause has its own `*_clause1` definition. All nine source
predicates have one source clause each; mode aliases therefore require no
multi-clause concatenation. Definition order follows dependency elaboration;
each clause body preserves source literal/disjunction/solution order.

| Source clause | Mode / outputs | Status |
| --- | --- | --- |
| 2–9, s7703/4 | full recursive/root modes and stipulated outputs | Absent, explicitly unfinished |
| 12–14, s7703_a/4 | bffb → (Spouse, Marriage) | Executable; filters matching a2 spouse/marriage under NAF |
| 17–82, s7703_a_1/5 | bfffb → (Spouse, Marriage, Option Day) | Executable; first complete death condition and first fallback death event distinguished |
| 85–98, s7703_a_2/5 | bfffb → (Spouse, Marriage, S19) | Executable; exact G4 decree strings |
| 103–106, s7703_b/3 | recursive composition | Absent, explicitly unfinished |
| 110–139, s7703_b_1/4 | bffb → (Household, Dependent) | Parameterized clause body only; required s152_a_1_bbb continuation |
| 142–184, s7703_b_2/4 | bbfb → Cost | Executable; both original findall loops and sums |
| 187–201, membership/3 | internal bbb → Unit per proof | Executable; multiplicity preserved |
| 203–216, s7703_b_3/4 | bfbb → Spouse | Executable; a-prefix, 184-day ordered findall, zero-length test |

Six of nine clauses are executable without later-section implementations; one
of nine is explicitly parameterized; two are absent. The five case-query modes
are preserved, including their free outputs. No ground-only slice substitutes
for them. Broader modes needed by the eventual recursive root are not claimed.
No arbitrary finite ground-person universe is used.

The independent six clauses do not call signatures with H4.1 stipulated clauses.
Stipulations are not deleted from Household; they have no call site in this
slice. The b1 continuation must supply actual downstream stipulated solutions.
Root s7703 stipulation append/freshening, including free spouse/marriage patterns,
remains unimplemented with the root. No wildcard list is misrepresented as all
ground solution pairs.

## Hazard coverage

The following source ids each appear exactly once as an implementation
annotation in `Oracle/S7703.lean`:

| Kind | Source site | Signed rule / treatment |
| --- | --- | --- |
| NAF | section7703.pl:14:2 | N-CALL, N1/N4; a2 emptiness after spouse/marriage binding |
| NAF | section7703.pl:30:13 | N-ABS-DATE, N2; missing start defaults to Jan 1 |
| NAF | section7703.pl:50:6 | N-ABS-DATE, N2; absent end or every qualifying end |
| NAF | section7703.pl:61:6 | N-ABS-DATE, N2/G1; deterministic absence in condition |
| NAF | section7703.pl:113:2 | N-CONJ, N5; exact Jan 1/Dec 31 joint-return facts |
| NAF | section7703.pl:129:13 | N-ABS-DATE, N2/D7; absent child end clamps to Dec 31 |
| NAF | section7703.pl:195:4 | N-ABS-DATE, N2; each membership end witness |
| AGG | section7703.pl:143:5 | A-EV/A1; payment/residence/agent/purpose/amount/start solutions |
| AGG | section7703.pl:162:2 | A-EV/A1; same loop without agent restriction |
| AGG | section7703.pl:180:2 | A2/M8; individual Int sum |
| AGG | section7703.pl:181:2 | A2/M8; all-payer Int sum |
| AGG | section7703.pl:205:5 | A-DAYS/A1/D8; every offset × membership proof |

**NAF: 7/8 annotated, with 113 and 129 in the parameterized body.** The missing
site is `section7703.pl:9:2` in the absent root. **AGG: 5/5 annotated**, covering
three findall and two sum_list sites. **CUT: 0/0 explicit `!` sites** in §7703;
the two signed C1/C2 sites belong to §151 and were not translated here.
The three `->` commitments at source 45, 62 and 67 are separately documented
as G1 commitments; they are not mislabeled as those §151 cut sites.

Other covered decisions: D1/D5 derived year arithmetic, D3 inclusive date
comparisons, D4 doubled duration inequality, D7 endpoint clamping, D8 July 1
through Dec 31, M3 doubled payment inequality with prior positive cost, G4
atom/string identity, and H1/G1 fact order and duplicates. For the payment
year test the admitted canonical Day is compared to Jan 1/Dec 31 boundaries.
General calendar/year-extraction equivalence is not proved by the finite tests.

## Pinned commands and results

Working directory for every command:
`/Users/devrashie/Documents/csProjects/kmla`.

```sh
lean +leanprover/lean4:v4.33.1 --version
```

Exit 0:

```text
Lean (version 4.33.1, arm64-apple-darwin24.6.0, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
```

Build directory was produced with
`mktemp -d /private/tmp/kmla-oracle7703.XXXXXX`:
`/private/tmp/kmla-oracle7703.IqVF77`. Compiled outputs are confined there.

```sh
mkdir -p /private/tmp/kmla-oracle7703.IqVF77/Interface /private/tmp/kmla-oracle7703.IqVF77/Oracle
LEAN_PATH=/private/tmp/kmla-oracle7703.IqVF77 lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703.IqVF77/Interface/Household.olean Interface/Household.lean
LEAN_PATH=/private/tmp/kmla-oracle7703.IqVF77 lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703.IqVF77/Interface/QuerySchema.olean Interface/QuerySchema.lean
LEAN_PATH=/private/tmp/kmla-oracle7703.IqVF77 lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703.IqVF77/Interface/QueryTime.olean Interface/QueryTime.lean
LEAN_PATH=/private/tmp/kmla-oracle7703.IqVF77 lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703.IqVF77/Oracle/S7703.olean Oracle/S7703.lean
```

All three Interface commands exited 0. The first S7703 compile failed because
core Lean supplies no `Bind List`/`Pure List` instances for this do-notation.
One implementation edit added section-local singleton/ordered-flatMap instances;
the final S7703 compile exited 0 with no diagnostics. No semantic test failed
in that implementation edit.

```sh
LEAN_PATH=/private/tmp/kmla-oracle7703.IqVF77 lean +leanprover/lean4:v4.33.1 Oracle/Tests/S7703.lean
```

**Exit 1 on all three proof attempts.** Of the 53 theorem declarations, 50
elaborated without errors each time; this is not a passing test-suite command.
They cover date constants/leap boundaries; missing and repeated facts; G4 tags;
death commitment/order; decree branches; both payment aggregates, one-half
equality, zero costs and purpose overlaps; inclusive residence boundaries;
the first and last D8 days; negative b1 premises under arbitrary continuations;
and actual query-year rejection. No mock production guards or s152 provider
were used, including in tests.

The axiom printouts for all seven clause definitions and all five entry wrappers
are subsets of X1. Six clauses report `[propext]`; the parameterized b1 clause
and all five entry wrappers report `[propext, Classical.choice, Quot.sound]`.
The failed proof declarations printed recovery `sorryAx`, so the test artifact
does NOT pass the axiom requirement. This is not a full hygiene-gate result.

```sh
LEAN_PATH=/private/tmp/kmla-oracle7703.IqVF77 lean +leanprover/lean4:v4.33.1 Oracle/Tests/S7703Reduction.lean
```

Final exit 0. It prints the available core `String.foldl_eq_foldl_toList`
theorem and actual derived `instBEqTerm.beq` definition. Earlier diagnostic
queries for nonexistent guessed names failed; an earlier `#reduce escapeJson
"b"` reached the default recursion limit. No reduction-limit option was changed.
These declaration diagnostics did not assert or establish the three test goals.

## Circuit-breaker evidence and orchestrator consultation request

The SAME three statements were retained throughout:

1. `b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity`
   (test lines 227–235): the exact-half residence prefix forwards the original
   `checked` certificate and preserves every solution of an arbitrary required
   continuation. Initial `simp` did not unfold list notation; second attempt
   added `Bind.bind`/`Pure.pure`; third also unfolded tag-sensitive BEq.
2. `a1_null_only_at_observation` (lines 251–257): the shared observer emits the
   exact one-row JSON tuple with null S13.
3. `b3_deduplication_only_at_observation` (lines 259–266): duplicated internal
   spouse solutions become the exact singleton shared observation.

For both observation goals: first `decide` failed reduction; second
`decide +kernel` also failed; third rewrote the known raw results and used the
existing core `String.foldl_eq_foldl_toList` theorem before `decide`, which
still failed. All assertions, inputs and implementation bodies stayed unchanged.

Final exact b1 goal from the compiler:

```text
Oracle/Tests/S7703.lean:231:75: error: unsolved goals
checked : CoveredR5Time (R5TimeSource.year y)
dependency : Term → Term → (year : Year) → CoveredR5Time (R5TimeSource.year year) → List Unit
⊢ List.flatMap
      (fun __x =>
        List.flatMap (fun __x => [(Term.atom "home", Term.atom "bob")])
          (dependency (Term.atom "bob") (Term.atom "alice") 2015 checked))
      (if 364 ≤ 2 * (min 16618 16800 - 16436) then [()] else []) =
    List.flatMap (fun __x => [(Term.atom "home", Term.atom "bob")])
      (dependency (Term.atom "bob") (Term.atom "alice") 2015 checked)
```

Observation error locations and exact common diagnostic:

```text
Oracle/Tests/S7703.lean:257:2: error: Tactic `decide` failed for proposition
Oracle/Tests/S7703.lean:266:2: error: Tactic `decide` failed for proposition
did not reduce to `isTrue` or `isFalse`.
```

The expanded goals contain the shared `List.foldr` deduplicator and
`List.mergeSort`, `String.intercalate`, and the rewritten `List.foldl` escaping
of `"bob".toList` / `"marriage".toList`. The exact final statements and tactic
scripts are retained in the test file; the pinned command reproduces the full
diagnostics. Tool output also records the unreduced goals from earlier attempts.

The printed failed-proof evidence includes:

```text
'KMLA.Oracle.S7703.Tests.b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity' depends on axioms: [propext,
 sorryAx,
 Classical.choice,
 Quot.sound]
'KMLA.Oracle.S7703.Tests.b3_deduplication_only_at_observation' depends on axioms: [propext,
 sorryAx,
 Classical.choice,
 Quot.sound]
```

**Question for orchestrator/Fable:** On the pinned Lean 4.33.1 and these exact
unchanged statements, what kernel-checked normalization/proof steps close the
concrete Int-min/list-bind goal and the shared observation/string-fold goals?
Please classify whether any shared implementation defect is actually shown;
the current evidence shows failed proof reduction, not a semantic mismatch.
Obtain the required resumption direction after this circuit-breaker stop before
another proof edit. Do not weaken statements, remove tests, install replacement
guards, change modes/populations, use native_decide/axioms, or alter Interface
without orchestrator authorization. No new A/WIRE semantic choice is requested.

## Open obligations and next integration need

- Resolve the stopped test proofs. This report must not be read as test success.
- Supply the faithful `s152_a_1/3` recursive continuation, its downstream
  stipulations and every needed mode; parameterization is not that implementation.
- Complete s7703/4 and s7703_b/3 with original instantiation guards, source
  multiplicity, NAF site 9, ordered stipulated append, fresh variables and
  correct later bindings. No scalar §7703 entry is available yet.
- Supply real V7/V8 and the exact all-ground-pairs V10 decider, and prove its
  iff including wildcard stipulations. No OracleGuards instance was added.
- Prove the R5 structural correspondence, universe completeness, birth/phase
  decrease, cycle cut and counter adequacy. There is no fuel in this slice and
  no exhaustion-as-answer branch. The continuation has no certified recursive
  budget yet; its type alone cannot establish these obligations.
- Prove every operational actual-year/Workday certificate and mode path,
  including R8 and the existing E2 exclusion. The b1 clause passes
  `CoveredR5Time (.year year)` unchanged to its continuation. Other clauses
  here do not enter R5/R8. The five entry wrappers require exact-tuple
  `AdmittedQuery`; raw clause helpers are not admitted reference entry points.
- Establish general calendar/interval correspondence and source equivalence;
  the selected kernel examples do not prove all admitted inputs.
- Through the orchestrator, request an **opaque harness CLI contract** for the
  four independent queried signatures/modes `a1/bfffb`, `a2/bfffb`, `b2/bbfb`,
  `b3/bfbb`, preserving all outputs and failures. Provide retained tuples,
  pinned runtime identity, results and verbatim meter mismatches only; do not
  expose harness implementation. Shared payload/query packaging and production
  admission providers must be established before reference use. Integrate b1
  only after its real continuation/adequacy are supplied. No output is to be
  manufactured for an unsupported predicate or mode.

No Prolog execution, harness CLI integration or owner-meter invocation occurred
in this lane. Parity records emitted: 0; distinct households compared: 0;
original cases compared: 0 of 376. Synthetic Lean fixtures are not original-case
coverage. **All 376-case parity and CP1 remain unpassed.** No next section began.

## Self-review

Assumptions about Prolog semantics are exactly the signed specification: G1
left-to-right SLD order and duplicates; first complete `->` guard success with
no fallback after its consequent fails; G4 tag-sensitive identities; H2 bound
purpose wildcards; NAF as existential failure without bindings; N2 absent-date
candidates; D3 closed comparisons; D4 differences rather than inclusive counts;
D8 the pinned New York formatted window; M3 exact half comparisons; A1/A2
solution multiplicity; and H6 external set observation only. No dependent-child
tax intuition, selected ground-person universe, or birthday-function assumption
was substituted. Source/runtime equivalence beyond the signed decisions remains
to be checked with the independent reference.

The implementation compiles; the test file does not. The seven clause and five
entry-wrapper axiom printouts are within X1, while failed proof recovery terms are explicitly
unacceptable. No production validity instance, R5/R8 proof, complete §7703
oracle, parity pass, or checkpoint pass is claimed.

**Circuit breaker: three failed edit cycles on one test means stop and report.**
Three failed proof attempts occurred on each of the three retained statements;
the lane stopped, reported them promptly, and made no subsequent proof or
implementation edits. Only read-only accounting and this handoff followed.

---

## Current final self-review

Prolog assumptions are the signed G1/G2/G3/G4 semantics: ordered SLD solutions
and duplicates; source-mode-sensitive instantiation; two independent nonvar
disjunction successes when both terms are bound; structural tag-sensitive
identity; first complete -> condition commits even if its consequent fails;
NAF checks existential failure without exporting bindings. N2 absent-date
candidates, D3/D4/D8 date rules, A1/A2 multiplicity and H6 boundary-only set
observation are retained. H4 wildcard freshness and later unification are owed,
not replaced by ground enumeration. Parameterization is not reference completion.

All three original proofs are now closed, with exact assertions/fixtures
preserved. The new compositions and 62-theorem main suite compile under pinned
Lean; no later-section provider, R5 adequacy, production guard, parity or CP1
completion is inferred. Consultation denial was respected. No implementation
or proof edits are planned after this bounded handoff.

**Circuit breaker: three failed edit cycles on one test means stop and report.**
The authorized resumed round incurred two b3 failures before success; no repeated
breaker fired. If a future breaker fires, halt edits to that obligation and send
precise evidence to the orchestrator for Fable DESIGN-FLAW REVIEW OF THE
OBLIGATION pending explicit approval, not a fourth tactic attempt.
