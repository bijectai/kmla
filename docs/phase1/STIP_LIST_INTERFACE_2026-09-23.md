# Shared stipulation-list Interface handoff — 2026-09-23

## Scope and status

Complete within the shared Interface boundary under signed H4, the A-022
representation-gap classification and Dev's bounded instruction. No missing
semantic choice was identified. This is not an owner amendment, an encoder,
payload/query schema release, lane adaptation, parity result or phase gate.
No implementation-lane source was inspected or edited; `human/`, consultations,
status metadata and git metadata were not edited. Main owns subsequent dispatch
and commits.

## Public changes and authority

| File | Change / authority |
| --- | --- |
| `Interface/Household.lean` | New distinct `StipArg = val Term \| wild Nat \| list (List StipArg)`; `Stip.args : List StipArg`. Signed H4.1–H4.3, A1/A3 and A-022 classify proper lists as already-required supplied data. G4 `Term`, event `Pat` and all 57 `Fact` constructors remain unchanged. |
| `Interface/Household.lean` | Structural `DecidableEq StipArg`, lossless `StipArg.ofPat` and one-way `Coe Pat StipArg`; no reverse coercion. `StipArg.dayWellFormed` delegates scalar/wild cases to the existing Day check and rejects a list at a scalar Day slot. `Stip.wellFormed` remains exactly the original outer-arity comparison. |
| `Interface/HOUSEHOLD_WIRE.md`, `Interface/WIRE.md` | Disjoint recursive `{"list":[...]}` spelling, with unchanged `{"val":...}` / `{"wild":...}` bytes. Event `Pat` remains distinct. The declaration's Authority table cites signed H1–H4/G4/D1/V9/M1/A3 and the shared field/constructor declarations; both registries retain 57 Fact and 31 Stip signatures. |
| `Interface/fixtures/household_wire.json` | Two appended transport cases; the six existing cases and their wire bytes are unchanged. No fixture claims `Valid`, `ValidStip`, corpus coverage or execution behavior. |
| `scripts/stip_list_guards.lean` | New shared-only 20 named proofs, 16 behavioral guards and two negative-elaboration blocks. Covers scalar inclusion, structural identity, original s151 heads, no fact widening, arity-only shape, V1/V2–V10 wiring and exact query-time rejection. |
| `scripts/check_query_time.sh` | Unconditionally compiles the new shared guards after the unchanged old guards, using fresh temporary Interface artifacts. No existing command/assertion was removed, weakened or conditionally skipped. |
| `tests/test_stip_list_wire.py` | Five standard-library declarative-fixture tests, including exact byte checks, old-byte hashes, Interface-derived arities and new list shapes. No lane imports, Household codec or Prolog execution. |

`StipPred`, `StipPred.arity`, time-role tables, `Household.v1` through the
existing validity plumbing, `Valid`/`ValidStip` bodies and the query-time modules
are unchanged. Generated households still require `stipulations=[]`. Scalar
Day admission is unchanged; other stipulated slots are not recursively scanned
for dates, numeric ranges or inferred modes. Lists in scalar Day positions are
not a new accepted date form. No default `OracleGuards` instance was installed;
test mocks are local and explicitly not semantic certificates.

## Fixture and signature details

`supplied_s151_lists` carries the Q-022 source shapes:

- `s151(bob,_,[charlie],[0],Year)` for 2014, 2015, 2016, 2017, in that order,
  with stored wildcard ids 0–3.
- `s151(alice,2000,[alice],_,2017)`, with distinct stored wildcard id 4 in this
  combined transport example. Combining these heads is not a new corpus case.

`recursive_lists_shared_ids` includes empty/nonempty/nested lists, the separate
scalar atom and string `"[]"`, atom/string `"usa"`, signed integers beyond 64
bits, ordered duplicate elements, and the same ids inside/outside nested lists.
It preserves the shape of main's pinned `sample(X,[X,Y,[Y]],Y)` witness without
declaring a new predicate signature. A shared proof also distinguishes its
ids 0/1 row from a copied ids 2/3 row. These are stored identities, not an
implementation of `findall`, `numbervars`, unification or variable allocation.
The 31 signatures/arities are taken only from `StipPred.arity`; no mode or role
is inferred from these fixture values.

## Verified commands and results

All final commands below exited 0 on 2026-09-23 from the repository root.

| Command | Result |
| --- | --- |
| `lean --version` | Lean 4.33.1, arm64-apple-darwin24.6.0, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6` (Release); repository pin `leanprover/lean4:v4.33.1`. |
| `bash scripts/check_interface.sh` | Fresh temporary compilation; Interface type-checks and all 115 existing behavioral guards pass. |
| `bash scripts/check_query_time.sh` | Fresh temporary `Household`, `QuerySchema`, `QueryTime` artifacts; 175 shared signatures / 135 queried / 31 stipulated schema entries match; old guards and both original rejection theorems pass; all new guards and 20 named proofs pass. |
| `python3 -B -m unittest discover -s tests -p test_stip_list_wire.py -v` | Five tests pass; all eight readable values match their exact wire strings and the six legacy wire SHA-256 values match. |
| `git diff --check` | Clean. |

Final axiom output: `KMLA.instDecidableEqStipArg` uses no axioms. All old and new
printed theorem dependencies are subsets of signed X1 (`propext`,
`Classical.choice`, `Quot.sound`); no final `sorryAx`, new axiom, weakened goal
or production default is involved. The first new-test failure and every failed
goal remain verbatim below. Replacing size-based well-founded recursion with
structural recursion fixed proof reduction; none of the failing assertion
statements was changed.

The following SHA-256 values equal the pre-edit baseline, confirming both old
guard files and the shared query/time schema sources are byte-for-byte intact:

```text
82b637ce8bdfff30f5629ed0576b49a6202e03200e4701662c870911a8cdf6ba  scripts/interface_guards.lean.inc
8336e159cbfab439dacc807ed41d3983b75a44e3d048c358fdfa15f7e7a9e115  scripts/query_time_guards.lean
a80d422cf771a1a385a8155ae7fcd1236b850ca8e9158ad24d49664c6fa74991  Interface/QueryTime.lean
6011b30293c3cdb83f51ece3587daa6d0e02990495825580bdc143681bbe1c66  Interface/QuerySchema.lean
481ac1423006e18234b06aaa9c8fa2e8f246708fcd6f60bd6af1bf59e62b4f59  Interface/TIME_SCHEMA.json
```

## Main handoff / limitations

The public source-level change is `List Pat` to `List StipArg` in `Stip.args`.
Independent lane consumers must handle the recursive `.list` constructor.
Existing explicitly scalar `Pat` elements have a one-way inclusion; an entire
`List Pat` can be mapped with `StipArg.ofPat` when necessary. No reverse
conversion can put a list in a Fact position. No lane compatibility or codec
round-trip claim is made here, and neither lane was built or modified.

Only finite proper lists are represented. Unsupported non-list compounds,
improper/open-tail lists and any encountered mismatch remain findings to main,
never stringifications, truncations, coerced values or filtered originals.
Full payload/query/target/observation packaging, allocation/freshening,
execution and production semantic guard proofs remain outside this slice.

## Self-review: Prolog assumptions and circuit breaker

- Semantic authority is signed DECISIONS and Interface; Q-022 provides the
  original supplied s151 shapes, and A-022 classifies their representation gap.
  Fixtures are not semantic authority or domain/validity evidence.
- Main reports pinned SWI 7.2.3 witnesses for nested `numbervars` aliasing,
  separate ids in `findall` copies, and `[]` distinct from scalar atom `'[]'`.
  This slice stores those distinctions, without rerunning Prolog, inspecting
  a lane, generalizing an allocation algorithm or assuming a new unification
  mode. `Pat` and all fact argument kinds are deliberately not widened.
- No assumption is made that arbitrary list-bearing stipulations execute,
  satisfy production guards or constitute a valid original case. Existing
  query-time checks still apply to actual calls.
- Circuit breaker: three failed edit cycles on one test means stop and report;
  no fourth attempt or weakened assertion. This slice had one failed new-test
  edit cycle (repeated unchanged only to capture diagnostics), then a passing
  structural-recursion correction. No old assertion changed, and no failed
  goal was discarded.

## Retained failed goals: first new-test edit cycle

The first run of `bash scripts/check_query_time.sh` compiled the new Interface
and passed all existing shared query guards and two rejection theorems. Eleven
new identity proofs failed because `decide` could not unfold the size-based
well-founded equality decision. The assertions remain in
`scripts/stip_list_guards.lean`, unchanged. The exact same command was repeated
without any code/proof edit solely to retain the complete diagnostics below;
that is one failed edit cycle, not two. Recovery `sorryAx` entries in this
failed elaboration are not accepted proofs.

```text
ok: 175 shared signatures; 135 queried; 31 stipulated; generated tables match
'QueryAdmissionTests.outOfRangeQueryRejected' depends on axioms: [propext, Classical.choice, Quot.sound]
'QueryAdmissionTests.outOfRangeStipRejected' depends on axioms: [propext, Classical.choice, Quot.sound]
ok    query-time guards and kernel-checked boundary proofs passed
scripts/stip_list_guards.lean:32:53: error: Tactic `decide` failed for proposition
  StipArg.list [StipArg.list [StipArg.val (Term.atom "usa")]] ≠
    StipArg.list [StipArg.list [StipArg.val (Term.str "usa")]]
because its `Decidable` instance
  instDecidableNot
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableNot` and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.list [StipArg.list [StipArg.val (Term.atom "usa")]])
    (StipArg.list [StipArg.list [StipArg.val (Term.str "usa")]])
scripts/stip_list_guards.lean:36:56: error: Tactic `decide` failed for proposition
  StipArg.list [StipArg.val (Term.int 1), StipArg.val (Term.int 2)] ≠
    StipArg.list [StipArg.val (Term.int 2), StipArg.val (Term.int 1)]
because its `Decidable` instance
  instDecidableNot
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableNot` and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.list [StipArg.val (Term.int 1), StipArg.val (Term.int 2)])
    (StipArg.list [StipArg.val (Term.int 2), StipArg.val (Term.int 1)])
scripts/stip_list_guards.lean:40:44: error: Tactic `decide` failed for proposition
  StipArg.list [StipArg.val (Term.atom "a"), StipArg.val (Term.atom "a")] ≠ StipArg.list [StipArg.val (Term.atom "a")]
because its `Decidable` instance
  instDecidableNot
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableNot` and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.list [StipArg.val (Term.atom "a"), StipArg.val (Term.atom "a")])
    (StipArg.list [StipArg.val (Term.atom "a")])
scripts/stip_list_guards.lean:43:52: error: Tactic `decide` failed for proposition
  StipArg.list [StipArg.list []] ≠ StipArg.list []
because its `Decidable` instance
  instDecidableNot
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableNot` and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.list [StipArg.list []]) (StipArg.list [])
scripts/stip_list_guards.lean:48:36: error: Tactic `decide` failed for proposition
  StipArg.list [] ≠ StipArg.val (Term.atom "[]") ∧
    StipArg.list [] ≠ StipArg.val (Term.str "[]") ∧ StipArg.list [] ≠ StipArg.wild 0
because its `Decidable` instance
  instDecidableAnd
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableAnd`, `instDecidableNot`, and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.list []) (StipArg.val (Term.atom "[]"))
scripts/stip_list_guards.lean:54:59: error: Tactic `decide` failed for proposition
  StipArg.list
      [StipArg.val (Term.int 123456789012345678901234567890),
        StipArg.val (Term.int (-123456789012345678901234567890))] ≠
    StipArg.list
      [StipArg.val (Term.int 123456789012345678901234567891), StipArg.val (Term.int (-123456789012345678901234567890))]
because its `Decidable` instance
  instDecidableNot
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableNot` and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝
    (StipArg.list
      [StipArg.val (Term.int 123456789012345678901234567890), StipArg.val (Term.int (-123456789012345678901234567890))])
    (StipArg.list
      [StipArg.val (Term.int 123456789012345678901234567891), StipArg.val (Term.int (-123456789012345678901234567890))])
scripts/stip_list_guards.lean:64:47: error: Tactic `decide` failed for proposition
  sharedVariables[0]? = some (StipArg.wild 0) ∧
    sharedVariables[1]? = some (StipArg.list [StipArg.wild 0, StipArg.wild 1, StipArg.list [StipArg.wild 1]]) ∧
      sharedVariables[2]? = some (StipArg.wild 1)
because its `Decidable` instance
  instDecidableAnd
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableAnd`, `instDecidableEqStipArg`, and `Option.instDecidableEq`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.wild 0) (StipArg.wild 0)
scripts/stip_list_guards.lean:68:74: error: Tactic `decide` failed for proposition
  sharedVariables ≠
    [StipArg.wild 0, StipArg.list [StipArg.wild 0, StipArg.wild 1, StipArg.list [StipArg.wild 2]], StipArg.wild 1]
because its `Decidable` instance
  instDecidableNot
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `decEq`, `instDecidableEqList`, `instDecidableNot`, and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.wild 0) (StipArg.wild 0)
scripts/stip_list_guards.lean:71:60: error: Tactic `decide` failed for proposition
  decide (sharedVariables = sharedVariables) = true
because its `Decidable` instance
  instDecidableEqBool (decide (sharedVariables = sharedVariables)) true
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `decEq`, `instDecidableEqBool`, `instDecidableEqList`, `Bool.decEq`, and `instDecidableEqStipArg`, reduction got stuck at the `Decidable` instance
  match decide (sharedVariables = sharedVariables), true with
  | false, false => isTrue ⋯
  | false, true => isFalse ⋯
  | true, false => isFalse ⋯
  | true, true => isTrue ⋯
scripts/stip_list_guards.lean:94:56: error: Tactic `decide` failed for proposition
  List.map (fun s => (s.args[1]?, s.args[4]?)) originalBobHeads =
    [(some (StipArg.wild 0), some (StipArg.val (Term.int 2014))),
      (some (StipArg.wild 1), some (StipArg.val (Term.int 2015))),
      (some (StipArg.wild 2), some (StipArg.val (Term.int 2016))),
      (some (StipArg.wild 3), some (StipArg.val (Term.int 2017)))]
because its `Decidable` instance
  instDecidableEqList (List.map (fun s => (s.args[1]?, s.args[4]?)) originalBobHeads)
    [(some (StipArg.wild 0), some (StipArg.val (Term.int 2014))),
      (some (StipArg.wild 1), some (StipArg.val (Term.int 2015))),
      (some (StipArg.wild 2), some (StipArg.val (Term.int 2016))),
      (some (StipArg.wild 3), some (StipArg.val (Term.int 2017)))]
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `decEq`, `instDecidableEqList`, `instDecidableEqProd`, `instDecidableEqStipArg`, and `Option.instDecidableEq`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.wild 0) (StipArg.wild 0)
scripts/stip_list_guards.lean:100:46: error: Tactic `decide` failed for proposition
  (bobHead 0 2014).args[2]? = some (StipArg.list [StipArg.val (Term.atom "charlie")]) ∧
    (bobHead 0 2014).args[3]? = some (StipArg.list [StipArg.val (Term.int 0)]) ∧
      aliceHead.args[2]? = some (StipArg.list [StipArg.val (Term.atom "alice")]) ∧
        aliceHead.args[3]? = some (StipArg.wild 4)
because its `Decidable` instance
  instDecidableAnd
did not reduce to `isTrue` or `isFalse`.

After unfolding the instances `instDecidableAnd`, `instDecidableEqStipArg`, and `Option.instDecidableEq`, reduction got stuck at the `Decidable` instance
  KMLA.stipArgDecEq✝ (StipArg.list [StipArg.val (Term.atom "charlie")])
    (StipArg.list [StipArg.val (Term.atom "charlie")])
scripts/stip_list_guards.lean:133:0: warning: Definition `StipListInterfaceTests.allTrueForWiringOnly` of class type is semireducible. Most type class instances should be instance-reducible, so consider marking this
definition with `@[instance_reducible]`. If it is intentionally semireducible, this warning can be disabled with `set_option warn.classDefReducibility false`.
'KMLA.instDecidableEqStipArg' depends on axioms: [propext, Quot.sound]
'StipListInterfaceTests.scalarDayCheckUnchanged' depends on axioms: [propext, Classical.choice, Quot.sound]
'StipListInterfaceTests.scalarInclusionInjective' depends on axioms: [propext]
'StipListInterfaceTests.nestedTagsDistinct' depends on axioms: [sorryAx]
'StipListInterfaceTests.listOrderMatters' depends on axioms: [sorryAx]
'StipListInterfaceTests.listMultiplicityMatters' depends on axioms: [sorryAx]
'StipListInterfaceTests.nestingMatters' depends on axioms: [sorryAx]
'StipListInterfaceTests.emptyListIsNotScalarOrWildcard' depends on axioms: [sorryAx]
'StipListInterfaceTests.largeSignedScalarsDistinct' depends on axioms: [sorryAx]
'StipListInterfaceTests.sharedIdsPreserved' depends on axioms: [propext, sorryAx]
'StipListInterfaceTests.changingOnlyNestedIdIsDetected' depends on axioms: [sorryAx]
'StipListInterfaceTests.recursiveEqualityAcceptsIdenticalValues' depends on axioms: [propext, sorryAx, Quot.sound]
'StipListInterfaceTests.originalHeadsHaveFiveArguments' does not depend on any axioms
'StipListInterfaceTests.originalHeadsKeepOrderAndWildcards' depends on axioms: [propext, sorryAx]
'StipListInterfaceTests.originalListValuesAreRetained' depends on axioms: [propext, sorryAx]
'StipListInterfaceTests.shapeStillChecksOnlyOuterArity' does not depend on any axioms
'StipListInterfaceTests.listsAreNotScalarDays' depends on axioms: [propext, Classical.choice, Quot.sound]
'StipListInterfaceTests.generatedStillRequiresNoStipulations' depends on axioms: [propext, Classical.choice, Quot.sound]
'StipListInterfaceTests.listStipulationsCannotAdmitBadQuery' depends on axioms: [propext, Classical.choice, Quot.sound]
'StipListInterfaceTests.listStipulationsCannotHideBadDay' depends on axioms: [propext, Classical.choice, Quot.sound]
```
