# §7703 isolated oracle progress — 2026-09-23

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
