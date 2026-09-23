import Interface.Household

/-!
Shared query-time boundary for the approved Option A (2026-09-22).

V10 checks all `r5Years`, not merely the outer taxable year. Every R5/R8 entry
must carry `CoveredR5Time actualSource`, where `actualSource` is its actual
ground year or Workday (including values obtained from stipulations). In
particular, R8 cannot substitute the enclosing taxable year for Workday's year.

This file supplies a checked boundary, not a termination proof or a claim that
not-yet-written Oracle wrappers use it. Before such a claim the oracle lane must
prove call-site/mode coverage, exclusion of the source's unbound-year E2 path,
exactness of `r5AllEligibleDecrease`, universe coverage and counter adequacy.
Rejection is a domain/coverage failure, never an ordinary reference result.
-/

namespace KMLA

/-- A year in exactly the finite population checked by V10. -/
structure R5Year where
  value : Year
  covered : value ∈ r5Years
  deriving DecidableEq

def R5Year.check? (y : Year) : Option R5Year :=
  if covered : y ∈ r5Years then some ⟨y, covered⟩ else none

/--
The year component of the approved D1 civil date encoding. This reuses the
shared conversion rather than introducing another epoch/calendar algorithm.
Callers must also check the V3 day bounds; an arbitrary ISO-looking string is
not a checked Workday. The date is already a typed `Day`, never a raw string.
-/
def Day.isoYear? (d : Day) : Option Year :=
  match (Day.toISO d).splitOn "-" with
  | [y, _, _] => y.toInt?
  | _ => none

/-- The actual time argument, not a caller-supplied list of alleged years. -/
inductive R5TimeSource where
  | year (value : Year)
  | workday (value : Day)
  deriving DecidableEq, Repr

/-- Fail closed on uncovered years and query/stipulation Workdays. -/
def R5TimeSource.check? : R5TimeSource → Option R5Year
  | .year y => R5Year.check? y
  | .workday d =>
      if dayLo ≤ d ∧ d ≤ dayHi then
        (Day.isoYear? d).bind R5Year.check?
      else none

/--
A dependent entry contract: the checked year is tied to the *actual* argument.
A wrapper receiving Workday `d` requires `CoveredR5Time (.workday d)`, not a
certificate for some other time. Recursive calls preserve this checked year;
fresh independent R8 invocations construct their own Workday certificate.
Do not add a total unchecked constructor, `mk!` or default-on-failure helper.
`none` is a reported coverage/domain failure, never a normal reference answer.
-/
structure CoveredR5Time (actual : R5TimeSource) where
  year : R5Year
  agrees : actual.check? = some year

def CoveredR5Time.check? (actual : R5TimeSource) : Option (CoveredR5Time actual) :=
  match agrees : actual.check? with
  | none => none
  | some y => some ⟨y, agrees⟩

/-- Coverage is kernel-checked membership, not an assertion in a sidecar. -/
theorem CoveredR5Time.year_covered {actual : R5TimeSource}
    (checked : CoveredR5Time actual) : checked.year.value ∈ r5Years :=
  checked.year.covered

-- This certificate adds only R5 year coverage. The wrapper must retain its
-- approved Valid/ValidStip premise; it must not silently reapply unrelated
-- year-indexed predicates such as V8 at the derived Workday year.

end KMLA
