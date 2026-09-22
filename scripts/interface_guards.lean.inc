-- Behavioural checks for Interface/Household.lean, appended to it by
-- scripts/check_interface.sh and run through the pinned toolchain.
--
-- Not a standalone Lean file and not part of Interface/: it is concatenated, so
-- no import is needed and the hygiene gate's import whitelist is untouched.
-- Behavioural assertions and the missing-instance elaboration checks make
-- `lean` exit non-zero on failure. All oracle substitutes here are test-only;
-- none computes eligibility or supplies a production Valid certificate.

open KMLA
-- D1 round trip against known day numbers
#guard Day.toISO 0 == "1970-01-01"
#guard Day.toISO (-25567) == "1900-01-01"
#guard Day.toISO 47846 == "2100-12-31"
#guard Day.toISO 17190 == "2017-01-24"
#guard Day.toISO 16800 == "2015-12-31"
#guard Day.toISO (-1) == "1969-12-31"
#guard Day.toISO 11016 == "2000-02-29"

-- acyclicity
#guard acyclic [(Term.atom "a", Term.atom "b"), (Term.atom "b", Term.atom "c")] == true
#guard acyclic [(Term.atom "a", Term.atom "b"), (Term.atom "b", Term.atom "a")] == false
#guard acyclic [] == true

-- G4 tag sensitivity
#guard (Term.atom "usa" == Term.str "usa") == false
#guard (Term.str "usa" == Term.str "usa") == true

-- H6.2 observation is a sorted, deduplicated set
#guard observe [[Obs.num 2], [Obs.num 1], [Obs.num 2]] == ["[1]", "[2]"]
#guard observe [] == []
#guard Obs.encode (Obs.atom "alice") == "{\"a\":\"alice\"}"
#guard Obs.encode (Obs.str "usa") == "{\"s\":\"usa\"}"
#guard Obs.encode (Obs.day 0) == "\"1970-01-01\""

-- kinship edges: son_(e), agent_(e,bob), patient_(e,charlie) means bob -> charlie
#guard (Household.mk [Fact.son_ (Term.atom "e"), Fact.agent_ (Term.atom "e") (Term.atom "bob"),
                      Fact.patient_ (Term.atom "e") (Term.atom "charlie")] []).parentEdges
        == [(Term.atom "bob", Term.atom "charlie")]

-- An Interface-only context must supply the oracle dependency explicitly.
example : True := by
  fail_if_success have _ : OracleGuards := inferInstance
  fail_if_success have _ := Valid (Household.mk [] []) 2018
  fail_if_success have _ := ValidStip (Household.mk [] []) 2018
  trivial

section LegacyInterfaceGuards
-- H5: a local test-only mock preserves the existing structural regressions.
local instance : OracleGuards where
  domesticAcyclic := fun _ => true
  noHohCycle      := fun _ _ => true
  r5AllEligibleDecrease := fun _ _ => true

def goodHh : Household :=
  { facts := [Fact.income_ (Term.atom "e"), Fact.agent_ (Term.atom "e") (Term.atom "alice"),
              Fact.amount_ (Term.atom "e") 100000, Fact.start_ (Term.atom "e") 16800],
    stipulations := [] }

#guard decide (Valid goodHh 2015) == true
-- V2: an amount above 10^9 is rejected
#guard decide (Valid { goodHh with facts := goodHh.facts ++ [Fact.amount_ (Term.atom "f") 2000000000] } 2015) == false
-- V3: a day outside 1900..2100 is rejected
#guard decide (Valid { goodHh with facts := goodHh.facts ++ [Fact.start_ (Term.atom "f") 99999] } 2015) == false
-- V3: a year outside 1900..2100 is rejected
#guard decide (Valid goodHh 1800) == false
-- V1: a stipulation is rejected by Valid but allowed by ValidStip
#guard decide (Valid { goodHh with stipulations := [⟨StipPred.s63_3, [Pat.val (Term.atom "alice"), Pat.wild 0, Pat.val (Term.int 2015)]⟩] } 2015) == false
#guard decide (ValidStip { goodHh with stipulations := [⟨StipPred.s63_3, [Pat.val (Term.atom "alice"), Pat.wild 0, Pat.val (Term.int 2015)]⟩] } 2015) == true
-- V1: a wildcard in a purpose_ fact is rejected by Valid, allowed by ValidStip
#guard decide (Valid { goodHh with facts := goodHh.facts ++ [Fact.purpose_ (Pat.wild 1) (Term.str "agricultural labor")] } 2015) == false
#guard decide (ValidStip { goodHh with facts := goodHh.facts ++ [Fact.purpose_ (Pat.wild 1) (Term.str "agricultural labor")] } 2015) == true
-- V4: a kinship cycle is rejected
#guard decide (Valid { goodHh with facts := goodHh.facts ++
    [Fact.son_ (Term.atom "k1"), Fact.agent_ (Term.atom "k1") (Term.atom "a"), Fact.patient_ (Term.atom "k1") (Term.atom "b"),
     Fact.son_ (Term.atom "k2"), Fact.agent_ (Term.atom "k2") (Term.atom "b"), Fact.patient_ (Term.atom "k2") (Term.atom "a")] } 2015) == false
-- V6: two distinct beneficiaries on one plan is rejected
#guard decide (Valid { goodHh with facts := goodHh.facts ++
    [Fact.plan_ (Term.atom "p"), Fact.beneficiary_ (Term.atom "p") (Term.atom "x"),
     Fact.beneficiary_ (Term.atom "p") (Term.atom "y")] } 2015) == false
end LegacyInterfaceGuards

namespace R5InterfaceTests

-- These supplied edges are deliberately mock data, not solutions computed
-- from K/original_c3. In particular, rejected fixtures are not generator output.
abbrev mockOracle (pairs : Year → List (Term × Term)) : OracleGuards where
  domesticAcyclic := fun _ => true
  noHohCycle := fun _ _ => true
  r5AllEligibleDecrease := fun h y =>
    (pairs y).all fun pair => h.r5Decreases pair.1 pair.2

def t : Term := .atom "taxpayer"
def d : Term := .atom "dependent"
def mid : Term := .atom "middle"
def bt : Term := .atom "birth-t"
def bd : Term := .atom "birth-d"

abbrev noEdges : OracleGuards := mockOracle (fun _ => [])
abbrev tdEdge : OracleGuards := mockOracle (fun _ => [(t, d)])
abbrev edgesAt (year : Year) (pairs : List (Term × Term)) : OracleGuards :=
  mockOracle (fun y => if y == year then pairs else [])

-- Each assertion checks BOTH predicates separately against the expected
-- result. ValidStip also carries an actual stipulation and a purpose wildcard.
def bothReturn (mock : OracleGuards) (h : Household) (expected : Bool) : Bool :=
  letI := mock
  let stipulated := { h with
    facts := h.facts ++ [.purpose_ (.wild 7) (.str "test-only")]
    stipulations := [⟨.s63_3, [.val t, .wild 8, .val (.int 2018)]⟩] }
  (decide (Valid h 2018) == expected)
  && (decide (ValidStip stipulated 2018) == expected)

def birthFacts (event person : Term) (day : Day) : List Fact :=
  [.birth_ event, .agent_ event person, .start_ event day]

def datedPair : Household := ⟨birthFacts bt t 0 ++ birthFacts bd d 1, []⟩
def sameBirthday : Household := ⟨birthFacts bt t 0 ++ birthFacts bd d 0, []⟩
def reversedBirthdays : Household := ⟨birthFacts bt t 1 ++ birthFacts bd d 0, []⟩
def duplicated : Household := { datedPair with facts := datedPair.facts ++ datedPair.facts }
def twoEvents : Household := ⟨birthFacts bt t 0 ++ birthFacts bd t 0, []⟩
def twoUndatedEvents : Household :=
  ⟨[.birth_ bt, .agent_ bt t, .birth_ bd, .agent_ bd t], []⟩
def twoStarts : Household := ⟨birthFacts bd d 0 ++ [.start_ bd 1], []⟩

-- The approved years are exactly the full interval, including both endpoints.
#guard r5Years.length == 201
#guard r5Years.head? == some 1900
#guard r5Years.getLast? == some 2100
#guard r5Years.all (fun y => 1900 ≤ y && y ≤ 2100)
#guard !(r5Years.contains 1899) && !(r5Years.contains 2101)

-- Repetition is allowed and preserved in the projections (two markers times
-- two agents gives four matching birth-event solutions for each person).
#guard duplicated.birthEvents == [bt, bd, bt, bd]
#guard duplicated.birthEventsOf t == [bt, bt, bt, bt]
#guard duplicated.startDays bt == [0, 0]
#guard duplicated.facts.length == 12
#guard duplicated.birthUnique
#guard duplicated.uniqueDOB t == some 0 && duplicated.uniqueDOB d == some 1
#guard bothReturn tdEdge duplicated true
#guard bothReturn (mockOracle (fun _ => [(t, d), (t, d)])) duplicated true

-- Uniqueness applies even with no eligible edges, and is not hidden in V1.
#guard twoEvents.v1 && twoStarts.v1 && twoUndatedEvents.v1
#guard !twoEvents.birthUnique && !twoStarts.birthUnique && !twoUndatedEvents.birthUnique
#guard twoEvents.uniqueDOB t == none && twoStarts.uniqueDOB d == none
#guard bothReturn noEdges twoEvents false
#guard bothReturn noEdges twoUndatedEvents false
#guard bothReturn noEdges twoStarts false
#guard bothReturn tdEdge { datedPair with facts := datedPair.facts ++ [.start_ bd 2] } false
-- Start uniqueness also applies to a birth event with no agent at all.
#guard bothReturn noEdges ⟨[.birth_ bd, .start_ bd 0, .start_ bd 1], []⟩ false
#guard bothReturn noEdges ⟨[.birth_ bd, .birth_ bd, .start_ bd 0, .start_ bd 0], []⟩ true
-- Other event kinds retain their multiple start dates.
#guard bothReturn noEdges ⟨[.income_ bd, .start_ bd 0, .start_ bd 1], []⟩ true

-- Person and event equality must both distinguish atom from string.
def taggedPersons : Household :=
  ⟨birthFacts bt (.atom "p") 0 ++ birthFacts bd (.str "p") 1, []⟩
def taggedEvents : Household :=
  ⟨birthFacts (.atom "b") t 0 ++ birthFacts (.str "b") t 0, []⟩
def taggedSeparate : Household :=
  ⟨birthFacts (.atom "b") (.atom "p") 0 ++ birthFacts (.str "b") (.str "p") 1, []⟩
#guard bothReturn noEdges taggedPersons true
#guard taggedPersons.uniqueDOB (.atom "p") == some 0
#guard taggedPersons.uniqueDOB (.str "p") == some 1
#guard bothReturn noEdges taggedEvents false
#guard bothReturn (mockOracle (fun _ => [(.atom "p", .str "p")])) taggedSeparate true
#guard taggedSeparate.startDays (.atom "b") == [0]
#guard taggedSeparate.startDays (.str "b") == [1]

-- Strict DOB increase, including rejection of every edge, not just the first.
#guard bothReturn tdEdge datedPair true
#guard bothReturn tdEdge reversedBirthdays false
#guard bothReturn tdEdge sameBirthday false
#guard bothReturn noEdges sameBirthday true
#guard bothReturn (mockOracle (fun _ => [(t, d), (d, t)])) datedPair false
#guard bothReturn (mockOracle (fun _ => [(d, t), (t, d)])) datedPair false
#guard bothReturn (mockOracle (fun _ => [(t, t)])) datedPair false
#guard bothReturn (mockOracle (fun _ => [(t, t)])) ⟨[], []⟩ false

-- A bad edge in 2100 must still reject outer year 2018. Check 1900 too, and
-- inject a bad edge separately at EVERY approved year to detect interior gaps.
#guard bothReturn (edgesAt 2100 [(t, d)]) sameBirthday false
#guard bothReturn (edgesAt 1900 [(t, d)]) sameBirthday false
#guard r5Years.all (fun y => bothReturn (edgesAt y [(t, d)]) sameBirthday false)
#guard bothReturn (edgesAt 2100 [(t, d)]) datedPair true
#guard bothReturn (edgesAt 1899 [(t, d)]) sameBirthday true
#guard bothReturn (edgesAt 2101 [(t, d)]) sameBirthday true

-- Birthless descent: two links, with both parent-first and child-first facts.
def birthlessChain : Household :=
  ⟨[.son_ (.atom "k1"), .agent_ (.atom "k1") d, .patient_ (.atom "k1") mid,
    .mother_ (.atom "k2"), .agent_ (.atom "k2") t, .patient_ (.atom "k2") mid], []⟩
def otherKinshipChain : Household :=
  ⟨[.daughter_ (.atom "k1"), .agent_ (.atom "k1") d, .patient_ (.atom "k1") mid,
    .father_ (.atom "k2"), .agent_ (.atom "k2") t, .patient_ (.atom "k2") mid], []⟩
def undatedDependent : Household :=
  { birthlessChain with facts := birthlessChain.facts ++ [.birth_ bd, .agent_ bd d] }
def datedDependentOnly : Household :=
  { birthlessChain with facts := birthlessChain.facts ++ birthFacts bd d 1 }
def equalDatedDescendant : Household :=
  { birthlessChain with facts := birthlessChain.facts ++ sameBirthday.facts }

#guard birthlessChain.v4 && !birthlessChain.hasBirth d
#guard birthlessChain.isStrictDescendantOf d t
#guard birthlessChain.isStrictDescendantOf d mid
#guard !(birthlessChain.isStrictDescendantOf t d)
#guard !(birthlessChain.isStrictDescendantOf t t)
#guard bothReturn tdEdge birthlessChain true
#guard bothReturn tdEdge otherKinshipChain true
#guard bothReturn tdEdge { birthlessChain with facts := birthlessChain.facts ++ birthlessChain.facts } true
-- The taxpayer's own DOB need not be known when the dependent has no birth.
#guard bothReturn tdEdge { birthlessChain with facts := birthlessChain.facts ++ [.birth_ bt, .agent_ bt t] } true
#guard bothReturn tdEdge ⟨[], []⟩ false
#guard bothReturn (mockOracle (fun _ => [(d, t)])) birthlessChain false
-- Birth presence requires the birth marker AND a matching agent, not a date,
-- a patient link, or a same-spelled event ID with the wrong tag.
#guard bothReturn tdEdge { birthlessChain with facts := birthlessChain.facts ++ [.agent_ bd d, .start_ bd 1] } true
#guard bothReturn tdEdge { birthlessChain with facts := birthlessChain.facts ++ [.birth_ bd, .patient_ bd d, .start_ bd 1] } true
#guard bothReturn tdEdge { birthlessChain with facts := birthlessChain.facts ++ [.birth_ (.atom "b"), .agent_ (.str "b") d] } true
#guard undatedDependent.hasBirth d && undatedDependent.uniqueDOB d == none
#guard bothReturn noEdges undatedDependent true
#guard bothReturn tdEdge undatedDependent false
#guard bothReturn tdEdge datedDependentOnly false
#guard bothReturn tdEdge { datedDependentOnly with facts := datedDependentOnly.facts ++ [.birth_ bt, .agent_ bt t] } false
#guard bothReturn tdEdge equalDatedDescendant false
#guard bothReturn tdEdge { birthlessChain with facts := birthlessChain.facts ++ datedPair.facts } true

-- The structural path bound does not waive V4, V7 or V8.
def cyclicKinship : Household :=
  { birthlessChain with facts := birthlessChain.facts ++
      [.son_ (.atom "k3"), .agent_ (.atom "k3") t, .patient_ (.atom "k3") d] }
#guard !cyclicKinship.v4 && !(cyclicKinship.isStrictDescendantOf t t)
#guard bothReturn tdEdge cyclicKinship false
#guard bothReturn { tdEdge with domesticAcyclic := fun _ => false } datedPair false
#guard bothReturn { tdEdge with noHohCycle := fun _ _ => false } datedPair false

end R5InterfaceTests

-- Neither the legacy local instance nor the explicit R5 mocks may leak into
-- an Oracle-free context and silently discharge its dependency.
example : True := by
  fail_if_success have _ : OracleGuards := inferInstance
  fail_if_success have _ := Valid (Household.mk [] []) 2018
  fail_if_success have _ := ValidStip (Household.mk [] []) 2018
  trivial
