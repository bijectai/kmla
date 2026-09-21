-- Behavioural checks for Interface/Household.lean, appended to it by
-- scripts/check_interface.sh and run through the pinned toolchain.
--
-- Not a standalone Lean file and not part of Interface/: it is concatenated, so
-- no import is needed and the hygiene gate's import whitelist is untouched.
-- Every check is a #guard, so `lean` exits non-zero if one fails.

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

-- H5: Valid is decidable once the two oracle-dependent conjuncts are supplied.
instance : OracleGuards where
  domesticAcyclic := fun _ => true
  noHohCycle      := fun _ _ => true

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
