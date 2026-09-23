import Interface.Household
import Interface.QuerySchema

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

/--
The actual supplied argument, retaining G4 tags and A3 wildcard identity.
List-valued dates occur at s3306_a_2_B's Workday output; do not coerce them to
one Day because of that variable's name. This is a time-boundary representation,
not a replacement for the full lossless codec or the approved target modes.
-/
inductive SuppliedArg where
  | single (pattern : Pat)
  | list (patterns : List Pat)
  deriving DecidableEq, Repr

private def suppliedYearOK : Pat → Bool
  | .wild _ => true
  | .val (.int y) => 1900 ≤ y && y ≤ 2100
  | _ => false

/-- D5's lexical years stay textual; this check never changes a G4 tag. -/
private def suppliedYearTextOK : Pat → Bool
  | .wild _ => true
  | .val (.atom s) | .val (.str s) =>
      match s.toInt? with
      | some y => 1900 ≤ y && y ≤ 2100 && toString y == s
      | none => false
  | _ => false

/-- Roles come from the fixed signature schema, never from a producer tag. -/
def SuppliedArg.timeOK (role : TimeRole) (arg : SuppliedArg) : Bool :=
  match role, arg with
  | .term, _ => true -- other kind/mode constraints belong to H2/G4/target schema
  | .day, .single p => p.dayWellFormed
  | .year, .single p => suppliedYearOK p
  | .yearText, .single p => suppliedYearTextOK p
  | .days, .single (.wild _) => true
  | .days, .list ps => ps.all Pat.dayWellFormed
  | _, _ => false

/-- No second, caller-supplied list of alleged dates can omit actual arguments. -/
structure QueryCall where
  predicate : String
  args : List SuppliedArg
  deriving DecidableEq, Repr

/--
V3 for the exact query tuple. Unknown signature/arity is unsupported, not a
successful check with an empty role list. A free time introduces no date/year;
every subsequently bound operational value still needs its own check. H6/G2
mode admissibility and call-site completeness must be proved by the lanes.
-/
def QueryCall.v3 (q : QueryCall) : Bool :=
  match queryTimeSchema? q.predicate q.args.length with
  | none => false
  | some roles => (roles.zip q.args).all fun (role, arg) => arg.timeOK role

/-- V3's household and actual-query halves, sharing the same date rules. -/
def Household.v3ForQuery (h : Household) (y : Year) (q : QueryCall) : Bool :=
  h.v3 y && q.v3

inductive AdmissionLane where
  | generated | original
  deriving DecidableEq, Repr

/--
Entry admission includes both the approved household premise and the query
tuple's time check. The generator must use `generated`; `original` is Week 1
ValidStip only. A lane may not choose it to admit a generated stipulation.
This does not assert mode completeness, guard correctness or R5 adequacy.
-/
def QueryAdmissible [OracleGuards] (lane : AdmissionLane)
    (h : Household) (y : Year) (q : QueryCall) : Prop :=
  (match lane with
   | .generated => Valid h y
   | .original => ValidStip h y) ∧ h.v3ForQuery y q = true

instance [OracleGuards] (lane : AdmissionLane) (h : Household) (y : Year)
    (q : QueryCall) : Decidable (QueryAdmissible lane h y q) := by
  unfold QueryAdmissible
  cases lane <;> infer_instance

/--
Required entry-wrapper argument, indexed by the complete actual tuple. There
is no default instance and no unchecked fallback. Decoding/admission failure
must halt/report, never become [], false, null, or a filtered original.
R8 additionally consumes CoveredR5Time for its actual Workday, after binding.
-/
structure AdmittedQuery [OracleGuards] (lane : AdmissionLane)
    (h : Household) (y : Year) (q : QueryCall) : Type where
  admissible : QueryAdmissible lane h y q

def AdmittedQuery.check? [OracleGuards] (lane : AdmissionLane)
    (h : Household) (y : Year) (q : QueryCall) : Option (AdmittedQuery lane h y q) :=
  if ok : QueryAdmissible lane h y q then some ⟨ok⟩ else none

theorem AdmittedQuery.actual_v3 [OracleGuards] {lane : AdmissionLane}
    {h : Household} {y : Year} {q : QueryCall}
    (checked : AdmittedQuery lane h y q) : h.v3ForQuery y q = true :=
  checked.admissible.2

end KMLA
