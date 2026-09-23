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
