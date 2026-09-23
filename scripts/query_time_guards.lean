import Interface.QueryTime

open KMLA

private def yearValue (source : R5TimeSource) : Option Year :=
  source.check?.map R5Year.value

#guard r5Years.length == 201
#guard yearValue (.year 1900) == some 1900
#guard yearValue (.year 2100) == some 2100
#guard yearValue (.year 1899) == none
#guard yearValue (.year 2101) == none
#guard yearValue (.workday dayLo) == some 1900
#guard yearValue (.workday dayHi) == some 2100
#guard yearValue (.workday (dayLo - 1)) == none
#guard yearValue (.workday (dayHi + 1)) == none
#guard yearValue (.workday 0) == some 1970
#guard yearValue (.workday (-1)) == some 1969
#guard yearValue (.workday 11016) == some 2000
#guard yearValue (.workday 17190) == some 2017
-- New-year boundary: the Workday's year, never an enclosing query year.
#guard yearValue (.workday 16800) == some 2015
#guard yearValue (.workday 16801) == some 2016
#guard (CoveredR5Time.check? (.workday dayHi)).isSome
#guard (CoveredR5Time.check? (.workday (dayHi + 1))).isNone
#guard (CoveredR5Time.check? (.year 2101)).isNone
-- Check every V3-admitted day, not just the boundary/leap fixtures. This is an
-- executable finite regression, not a source-mode or R5 termination theorem.
#guard (List.range 73414).all fun offset =>
  (CoveredR5Time.check? (.workday (dayLo + Int.ofNat offset))).isSome

-- D1/V3 decoder: every admitted day round-trips; malformed/overflow spellings
-- are not normalized into a different reference input.
#guard (List.range 73414).all fun offset =>
  let day := dayLo + Int.ofNat offset
  Day.fromISO? (Day.toISO day) == some day
#guard Day.fromISO? "1900-01-01" == some dayLo
#guard Day.fromISO? "2100-12-31" == some dayHi
#guard Day.fromISO? "2000-02-29" == some 11016
#guard Day.fromISO? "1900-02-29" == none
#guard Day.fromISO? "2100-02-29" == none
#guard Day.fromISO? "2017-02-30" == none
#guard Day.fromISO? "2017-1-1" == none
#guard Day.fromISO? "1899-12-31" == none
#guard Day.fromISO? "2101-01-01" == none
#guard Day.fromISO? "+2017-01-01" == none
#guard Day.fromISO? "2017-00-01" == none
#guard Day.fromISO? "2017-01-00" == none
#guard Day.fromISO? "x" == none

-- A certificate for a root year cannot be used for an unrelated Workday.
example (checked : CoveredR5Time (.workday 16801)) :
    checked.year.value ∈ r5Years := checked.year_covered

example : ¬ Nonempty (CoveredR5Time (.workday (dayHi + 1))) := by
  intro ⟨checked⟩
  have impossible := checked.agrees
  change none = some checked.year at impossible
  contradiction

example : ¬ Nonempty (CoveredR5Time (.year 2101)) := by
  intro ⟨checked⟩
  have impossible := checked.agrees
  change none = some checked.year at impossible
  contradiction

namespace QueryAdmissionTests

-- No production guard is installed; this instance only tests admission wiring.
local instance : OracleGuards where
  domesticAcyclic := fun _ => true
  noHohCycle := fun _ _ => true
  r5AllEligibleDecrease := fun _ _ => true

def a (s : String) : SuppliedArg := .single (.val (.atom s))
def day (s : String) : SuppliedArg := .single (.val (.str s))
def yr (y : Int) : SuppliedArg := .single (.val (.int y))
def free (n : Nat) : SuppliedArg := .single (.wild n)
def emptyH : Household := ⟨[], []⟩
def r8 (d : SuppliedArg) : QueryCall := ⟨"s3306_c_10_A_ii", [a "p", a "student", d]⟩

#guard (r8 (day "1900-01-01")).v3
#guard (r8 (day "2100-12-31")).v3
#guard !(r8 (day "1899-12-31")).v3
#guard !(r8 (day "2101-01-01")).v3
#guard !(r8 (day "2017-02-30")).v3
#guard !(r8 (yr 2015)).v3
#guard (r8 (a "2016-01-01")).v3 -- atom tag preserved, same date arithmetic
#guard (r8 (free 77)).v3 -- time-only check; NOT H6/G2 mode certification
#guard !(QueryCall.mk "s3306_c_10_A_ii" [a "p", a "student"]).v3
#guard !(QueryCall.mk "unknown" []).v3
#guard (QueryCall.mk "s7703" [a "p", free 1, free 2, yr 1900]).v3
#guard !(QueryCall.mk "s7703" [a "p", free 1, free 2, yr 2101]).v3
#guard !(QueryCall.mk "s7703" [a "p", free 1, free 2, a "2015"]).v3
#guard !(QueryCall.mk "s68_b" [a "p", free 1, yr 250000]).v3
#guard (QueryCall.mk "s3306_c" [free 0, a "p", free 1, day "2015-01-01", yr 2015]).v3
#guard !(QueryCall.mk "s3306_c" [free 0, a "p", free 1, day "2101-01-01", yr 2015]).v3
-- These Workday-named positions actually contain lists. Check every element.
#guard (QueryCall.mk "s3306_a_2_B"
  [a "p", .list [.val (.str "2015-01-01"), .val (.str "2015-01-02")],
   free 1, free 2, free 3, yr 2015]).v3
#guard !(QueryCall.mk "s3306_a_2_B"
  [a "p", .list [.val (.str "2015-01-01"), .val (.str "2101-01-01")],
   free 1, free 2, free 3, yr 2015]).v3
#guard !(QueryCall.mk "s3306_a_2_B"
  [a "p", day "2015-01-01", free 1, free 2, free 3, yr 2015]).v3
-- D5/G4: s3306_b_15 returns a textual year, never an Int-coerced observation.
#guard (QueryCall.mk "s3306_b_15" [free 0, free 1, free 2, free 3, day "2015"]).v3
#guard (QueryCall.mk "s3306_b_15" [free 0, free 1, free 2, free 3, a "2015"]).v3
#guard !(QueryCall.mk "s3306_b_15" [free 0, free 1, free 2, free 3, yr 2015]).v3
#guard !(QueryCall.mk "s3306_b_15" [free 0, free 1, free 2, free 3, day "2101"]).v3
#guard !(QueryCall.mk "s3306_b_15" [free 0, free 1, free 2, free 3, day "02015"]).v3
-- A valid household does NOT make an out-of-range query admissible.
#guard decide (Valid emptyH 2015)
#guard (AdmittedQuery.check? .generated emptyH 2015 (r8 (day "2015-01-01"))).isSome
#guard (AdmittedQuery.check? .generated emptyH 2015 (r8 (day "2101-01-01"))).isNone
#guard (AdmittedQuery.check? .original emptyH 2015 (r8 (day "2101-01-01"))).isNone

example (q : QueryCall) (checked : AdmittedQuery .generated emptyH 2015 q) :
    emptyH.v3ForQuery 2015 q = true := checked.actual_v3

example : ¬ Nonempty (AdmittedQuery .original emptyH 2015 (r8 (day "2101-01-01"))) := by
  intro ⟨checked⟩
  have bad := checked.actual_v3
  -- +kernel asks the kernel to check the decision proof directly; it is NOT
  -- +native/native_decide and adds no native-evaluation axiom. String reduction
  -- in the elaborator alone gets stuck on this concrete tuple.
  have rejected : emptyH.v3ForQuery 2015 (r8 (day "2101-01-01")) = false := by decide +kernel
  rw [rejected] at bad
  contradiction

end QueryAdmissionTests
