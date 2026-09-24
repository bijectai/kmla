import Interface.QueryTime

/-!
Shared representation regressions for A-022. No lane implementation is imported.
Original s151 shapes below are transcribed from Q-022, not inferred from fixture
outputs. Test-only OracleGuards isolate wiring; none is a production certificate.
-/

open KMLA

namespace StipListInterfaceTests

-- The old scalar pattern embeds without reassigning wildcard ids.
theorem scalarDayCheckUnchanged (p : Pat) :
    (StipArg.ofPat p).dayWellFormed = p.dayWellFormed := by
  cases p <;> rfl

theorem scalarInclusionInjective (p q : Pat) :
    StipArg.ofPat p = StipArg.ofPat q ↔ p = q := by
  cases p <;> cases q <;> simp [StipArg.ofPat]

-- Neither the new list nor any StipArg can leak back into a Fact position.
example : True := by
  fail_if_success have _ : Term := StipArg.list []
  fail_if_success have _ : Pat := StipArg.list []
  fail_if_success have _ : Fact := Fact.purpose_ (StipArg.list []) (.str "purpose")
  fail_if_success have _ : Fact := Fact.agent_ (.atom "event") (StipArg.list [])
  trivial

theorem nestedTagsDistinct :
    StipArg.list [.list [.val (.atom "usa")]] ≠
      StipArg.list [.list [.val (.str "usa")]] := by decide

theorem listOrderMatters :
    StipArg.list [.val (.int 1), .val (.int 2)] ≠
      StipArg.list [.val (.int 2), .val (.int 1)] := by decide

theorem listMultiplicityMatters :
    StipArg.list [.val (.atom "a"), .val (.atom "a")] ≠
      StipArg.list [.val (.atom "a")] := by decide

theorem nestingMatters :
    StipArg.list [.list []] ≠ StipArg.list [] := by decide

theorem emptyListIsNotScalarOrWildcard :
    StipArg.list [] ≠ .val (.atom "[]") ∧
    StipArg.list [] ≠ .val (.str "[]") ∧
    StipArg.list [] ≠ .wild 0 := by decide

theorem largeSignedScalarsDistinct :
    StipArg.list [.val (.int 123456789012345678901234567890),
      .val (.int (-123456789012345678901234567890))] ≠
    StipArg.list [.val (.int 123456789012345678901234567891),
      .val (.int (-123456789012345678901234567890))] := by decide

-- The same ids survive outside and inside the recursive container. This is
-- structural identity, not a unification engine or an allocation algorithm.
def sharedVariables : List StipArg :=
  [.wild 0, .list [.wild 0, .wild 1, .list [.wild 1]], .wild 1]

theorem sharedIdsPreserved :
    sharedVariables[0]? = some (.wild 0) ∧
    sharedVariables[1]? = some (.list [.wild 0, .wild 1, .list [.wild 1]]) ∧
    sharedVariables[2]? = some (.wild 1) := by decide

theorem changingOnlyNestedIdIsDetected :
    sharedVariables ≠
      [.wild 0, .list [.wild 0, .wild 1, .list [.wild 2]], .wild 1] := by decide

theorem recursiveEqualityAcceptsIdenticalValues :
    decide (sharedVariables = sharedVariables) = true := by decide

-- Main's pinned findall/numbervars witness retains aliases within each copy,
-- with fresh ids in the next copy. The container stores both rows unchanged;
-- it does not perform the freshening.
def copiedVariables : List StipArg :=
  [.wild 2, .list [.wild 2, .wild 3, .list [.wild 3]], .wild 3]

theorem copiedRowsRemainDistinct : sharedVariables ≠ copiedVariables := by decide

-- Q-022: s2_a_1_B_pos.pl:40 enumerates these four heads in this order.
def bobHead (id : Nat) (year : Int) : Stip :=
  ⟨.s151_5, [.val (.atom "bob"), .wild id,
    .list [.val (.atom "charlie")], .list [.val (.int 0)], .val (.int year)]⟩

def originalBobHeads : List Stip :=
  [bobHead 0 2014, bobHead 1 2015, bobHead 2 2016, bobHead 3 2017]

-- Q-022: s63_d_2_pos.pl supplies s151(alice,2000,[alice],_,2017).
def aliceHead : Stip :=
  ⟨.s151_5, [.val (.atom "alice"), .val (.int 2000),
    .list [.val (.atom "alice")], .wild 4, .val (.int 2017)]⟩

theorem originalHeadsHaveFiveArguments :
    (originalBobHeads ++ [aliceHead]).all Stip.wellFormed = true := by decide

theorem originalHeadsKeepOrderAndWildcards :
    originalBobHeads.map (fun s => (s.args[1]?, s.args[4]?)) =
      [(some (.wild 0), some (.val (.int 2014))),
       (some (.wild 1), some (.val (.int 2015))),
       (some (.wild 2), some (.val (.int 2016))),
       (some (.wild 3), some (.val (.int 2017)))] := by decide

theorem originalListValuesAreRetained :
    (bobHead 0 2014).args[2]? = some (.list [.val (.atom "charlie")]) ∧
    (bobHead 0 2014).args[3]? = some (.list [.val (.int 0)]) ∧
    aliceHead.args[2]? = some (.list [.val (.atom "alice")]) ∧
    aliceHead.args[3]? = some (.wild 4) := by decide

theorem shapeStillChecksOnlyOuterArity (s : Stip) :
    s.wellFormed = (s.args.length == s.pred.arity) := rfl

#guard !(Stip.mk .s151_5 [.list sharedVariables]).wellFormed
#guard (Stip.mk .s151_5 [.list [], .list sharedVariables, .wild 1,
  .val (.str ""), .val (.int (-123456789012345678901234567890))]).wellFormed

-- Day checking is still a scalar check. A list is never flattened or treated
-- as a wildcard; date-like values in non-Day positions are not reclassified.
theorem listsAreNotScalarDays :
    (StipArg.list []).dayWellFormed = false ∧
    (StipArg.list [.val (.str "2015-01-01")]).dayWellFormed = false ∧
    (StipArg.list [.wild 0]).dayWellFormed = false := by decide

#guard (Stip.mk .s151_5 [.list [.val (.str "2101-01-01")], .wild 0,
  .list [.list [.val (.int (-1))]], .list [], .list [.val (.int 250000)]]).daysWellFormed
#guard !(Stip.mk .s3306_c_5 [.wild 0, .wild 1, .wild 2,
  .list [.val (.str "2015-01-01")], .val (.int 2015)]).daysWellFormed

def listHousehold : Household := ⟨[], originalBobHeads ++ [aliceHead]⟩

-- No instance assumption can let a generated household carry stipulations.
theorem generatedStillRequiresNoStipulations [OracleGuards]
    (h : Household) (y : Year) (ok : Valid h y) : h.stipulations = [] := by
  cases h with
  | mk facts stips =>
    cases stips with
    | nil => rfl
    | cons s ss => simp [Valid, Household.v1] at ok

-- Deliberate test mocks. Toggling each semantic dependency remains observable.
abbrev allTrueForWiringOnly : OracleGuards where
  domesticAcyclic := fun _ => true
  noHohCycle := fun _ _ => true
  r5AllEligibleDecrease := fun _ _ => true

def originalCheck (g : OracleGuards) (h : Household) (y : Year := 2015) : Bool :=
  letI := g
  decide (ValidStip h y)

#guard originalCheck allTrueForWiringOnly listHousehold
#guard !originalCheck { allTrueForWiringOnly with domesticAcyclic := fun _ => false } listHousehold
#guard !originalCheck { allTrueForWiringOnly with noHohCycle := fun _ _ => false } listHousehold
#guard !originalCheck { allTrueForWiringOnly with
  r5AllEligibleDecrease := fun _ y => y != 2100 } listHousehold
#guard !originalCheck allTrueForWiringOnly listHousehold 2101
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with facts := [.amount_ (.atom "e") 1000000001] }
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with facts := [.start_ (.atom "e") (dayHi + 1)] }
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with facts := [.birth_ (.atom "b"), .start_ (.atom "b") 0,
    .start_ (.atom "b") 1] }
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with facts := [.plan_ (.atom "p"),
    .beneficiary_ (.atom "p") (.atom "a"), .beneficiary_ (.atom "p") (.atom "b")] }
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with facts := [.son_ (.atom "ab"), .agent_ (.atom "ab") (.atom "a"),
    .patient_ (.atom "ab") (.atom "b"), .son_ (.atom "ba"),
    .agent_ (.atom "ba") (.atom "b"), .patient_ (.atom "ba") (.atom "a")] }
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with facts := [.service_ (.atom "s"),
    .agent_ (.atom "s") (.atom "child"), .patient_ (.atom "s") (.atom "parent"),
    .son_ (.atom "kin"), .agent_ (.atom "kin") (.atom "child"),
    .patient_ (.atom "kin") (.atom "parent"), .birth_ (.atom "birth"),
    .agent_ (.atom "birth") (.atom "child"), .start_ (.atom "birth") 0] }
#guard !originalCheck allTrueForWiringOnly
  { listHousehold with stipulations := [⟨.s151_5, [.list []]⟩] }

-- The public query representation, its existing flat list-of-days boundary
-- and the exact operational year checks are unchanged by StipArg.
def badR8 : QueryCall := ⟨"s3306_c_10_A_ii",
  [.single (.val (.atom "p")), .single (.val (.atom "student")),
   .single (.val (.str "2101-01-01"))]⟩

theorem listStipulationsCannotAdmitBadQuery [OracleGuards] :
    ¬ Nonempty (AdmittedQuery .original listHousehold 2015 badR8) := by
  intro ⟨checked⟩
  have bad := checked.actual_v3
  have rejected : badR8.v3 = false := by decide
  simp [Household.v3ForQuery, rejected] at bad

def badStipDay : Household := { listHousehold with
  stipulations := listHousehold.stipulations ++ [⟨.s3306_c_5,
    [.wild 9, .wild 10, .wild 11, .val (.str "2101-01-01"), .val (.int 2015)]⟩] }

theorem listStipulationsCannotHideBadDay [OracleGuards] (q : QueryCall) :
    ¬ Nonempty (AdmittedQuery .original badStipDay 2015 q) := by
  intro ⟨checked⟩
  have bad := checked.actual_v3
  have rejected : badStipDay.v3 2015 = false := by decide
  simp [Household.v3ForQuery, rejected] at bad

-- Instances in these tests must not provide a production default.
example : True := by
  fail_if_success have _ : OracleGuards := inferInstance
  trivial

#print axioms KMLA.instDecidableEqStipArg
#print axioms scalarDayCheckUnchanged
#print axioms scalarInclusionInjective
#print axioms nestedTagsDistinct
#print axioms listOrderMatters
#print axioms listMultiplicityMatters
#print axioms nestingMatters
#print axioms emptyListIsNotScalarOrWildcard
#print axioms largeSignedScalarsDistinct
#print axioms sharedIdsPreserved
#print axioms changingOnlyNestedIdIsDetected
#print axioms recursiveEqualityAcceptsIdenticalValues
#print axioms copiedRowsRemainDistinct
#print axioms originalHeadsHaveFiveArguments
#print axioms originalHeadsKeepOrderAndWildcards
#print axioms originalListValuesAreRetained
#print axioms shapeStillChecksOnlyOuterArity
#print axioms listsAreNotScalarDays
#print axioms generatedStillRequiresNoStipulations
#print axioms listStipulationsCannotAdmitBadQuery
#print axioms listStipulationsCannotHideBadDay

end StipListInterfaceTests
