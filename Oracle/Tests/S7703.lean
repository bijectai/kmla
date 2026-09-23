import Oracle.S7703

/-!
Self-contained kernel tests of the §7703 slice, not reference parity.
No OracleGuards instance or substitute s152 implementation is installed.
Parameterized b1 checks quantify over an arbitrary continuation; they do not
claim that any continuation implements the later section or terminates R5.
-/

namespace KMLA.Oracle.S7703.Tests

def alice : Term := .atom "alice"
def bob : Term := .atom "bob"
def carol : Term := .atom "carol"
def marriage : Term := .atom "marriage"
def home : Term := .atom "home"
def death1 : Term := .atom "death1"
def death2 : Term := .atom "death2"
def residence : Term := .atom "residence"
def separation : Term := .atom "separation"
def payment1 : Term := .atom "payment1"
def payment2 : Term := .atom "payment2"

def y : Year := 2015
def jan1 : Day := firstDay y
def dec31 : Day := lastDay y
def jul1 : Day := julyFirst y
def janNext : Day := firstDay (y + 1)

def married : List Fact :=
  [.marriage_ marriage, .agent_ marriage alice, .agent_ marriage bob]

def hh (facts : List Fact) : Household := ⟨facts, []⟩

theorem calendar_epoch : firstDay 1970 = 0 := by decide
theorem calendar_low : firstDay 1900 = dayLo := by decide
theorem calendar_high : lastDay 2100 = dayHi := by decide
theorem calendar_next : firstDay 2101 = 47847 := by decide
theorem calendar_common_half : lastDay 2015 - firstDay 2015 = 364 := by decide
theorem calendar_leap_half : lastDay 2016 - firstDay 2016 = 365 := by decide
theorem calendar_july : Day.toISO (julyFirst 2015) = "2015-07-01" := by decide
theorem calendar_leap_july : Day.toISO (julyFirst 2000) = "2000-07-01" := by decide
theorem calendar_184 : julyFirst 2015 + 183 = lastDay 2015 := by decide

theorem a1_absent_start_and_end :
    s7703_a_1_bfffb (hh married) alice y = [(bob, marriage, none)] := by decide

theorem a1_duplicate_agents :
    s7703_a_1_bfffb (hh (married ++ [.agent_ marriage bob])) alice y =
      [(bob, marriage, none), (bob, marriage, none)] := by decide

theorem a1_duplicate_starts :
    s7703_a_1_bfffb (hh (married ++
      [.start_ marriage jan1, .start_ marriage jan1])) alice y =
      [(bob, marriage, none), (bob, marriage, none)] := by decide

theorem a1_string_is_not_atom :
    s7703_a_1_bfffb (hh married) (.str "alice") y = [] := by decide

theorem a1_living_end_dec31_fails :
    s7703_a_1_bfffb (hh (married ++ [.end_ marriage dec31])) alice y = [] := by decide

theorem a1_living_end_next_jan1_passes :
    s7703_a_1_bfffb (hh (married ++ [.end_ marriage janNext])) alice y =
      [(bob, marriage, none)] := by decide

def deadOnLast : List Fact :=
  [.death_ death1, .agent_ death1 bob, .start_ death1 dec31]

theorem a1_death_closed_end :
    s7703_a_1_bfffb (hh (married ++ deadOnLast ++ [.end_ marriage dec31])) alice y =
      [(bob, marriage, some dec31)] := by decide

def earlyThenLate : List Fact :=
  [.death_ death1, .death_ death2, .agent_ death1 bob, .agent_ death2 bob,
   .start_ death1 jan1, .start_ death2 dec31]

theorem a1_committed_then_failure :
    s7703_a_1_bfffb (hh (married ++ [.start_ marriage jul1] ++ earlyThenLate)) alice y =
      [] := by decide

theorem a1_order_changes_committed_witness :
    s7703_a_1_bfffb (hh (married ++ [.start_ marriage jul1,
      .death_ death2, .death_ death1, .agent_ death1 bob, .agent_ death2 bob,
      .start_ death1 jan1, .start_ death2 dec31])) alice y =
      [(bob, marriage, some dec31)] := by decide

theorem a1_first_successful_whole_condition :
    s7703_a_1_bfffb (hh (married ++
      [.death_ death1, .death_ death2, .agent_ death1 bob, .agent_ death2 bob,
       .start_ death1 (jan1 - 1), .start_ death2 dec31])) alice y =
      [(bob, marriage, some dec31)] := by decide

theorem a1_first_event_undated_blocks_later_death :
    s7703_a_1_bfffb (hh (married ++
      [.death_ death1, .death_ death2, .agent_ death1 bob, .agent_ death2 bob,
       .start_ death2 janNext])) alice y = [] := by decide

theorem a1_first_event_dates_all_retained :
    s7703_a_1_bfffb (hh (married ++
      [.death_ death1, .agent_ death1 bob,
       .start_ death1 janNext, .start_ death1 (janNext + 1)])) alice y =
      [(bob, marriage, none), (bob, marriage, none)] := by decide

theorem a1_in_year_condition_commits_before_repeated_dates :
    s7703_a_1_bfffb (hh (married ++
      [.death_ death1, .agent_ death1 bob,
       .start_ death1 jul1, .start_ death1 dec31])) alice y =
      [(bob, marriage, some jul1)] := by decide

def decree (tag : Term) : List Fact :=
  [.legal_separation_ separation, .patient_ separation marriage,
   .agent_ separation tag, .start_ separation dec31]

theorem a2_decree_string :
    s7703_a_2_bfffb (hh (married ++ decree (.str "decree of divorce"))) alice y =
      [(bob, marriage, separation)] := by decide

theorem a2_decree_atom_fails :
    s7703_a_2_bfffb (hh (married ++ decree (.atom "decree of divorce"))) alice y =
      [] := by decide

theorem a2_both_decree_branches_count :
    s7703_a_2_bfffb (hh (married ++ decree (.str "decree of divorce") ++
      [.agent_ separation (.str "decree of separate maintenance")])) alice y =
      [(bob, marriage, separation), (bob, marriage, separation)] := by decide

theorem a_legal_separation_negates_matching_marriage :
    s7703_a_bffb (hh (married ++ decree (.str "decree of divorce"))) alice y =
      [] := by decide

theorem a_other_marriage_survives :
    s7703_a_bffb (hh (married ++ decree (.str "decree of divorce") ++
      [.marriage_ (.atom "other"), .agent_ (.atom "other") alice,
       .agent_ (.atom "other") carol])) alice y =
      [(carol, .atom "other")] := by decide

def maintenance (others : Int) : List Fact :=
  [.residence_ residence, .residence_ (.atom "residence2"),
   .patient_ residence home, .patient_ (.atom "residence2") home,
   .payment_ payment1, .payment_ payment2,
   .agent_ payment1 alice, .agent_ payment2 bob,
   .purpose_ (.val payment1) home, .purpose_ (.val payment2) home,
   .amount_ payment1 1, .amount_ payment2 others,
   .start_ payment1 jan1, .start_ payment2 dec31]

theorem b2_residence_multiplicity_and_exact_half :
    s7703_b_2_bbfb (hh (maintenance 1)) alice home y = [4] := by decide

theorem b2_less_than_half :
    s7703_b_2_bbfb (hh (maintenance 2)) alice home y = [] := by decide

theorem b2_agent_duplicates_only_multiply_individual :
    s7703_b_2_bbfb (hh (maintenance 2 ++ [.agent_ payment1 alice])) alice home y =
      [6] := by decide

theorem b2_duplicate_amounts :
    s7703_b_2_bbfb (hh (maintenance 1 ++ [.amount_ payment1 1])) alice home y =
      [6] := by decide

theorem b2_duplicate_starts :
    s7703_b_2_bbfb (hh (maintenance 1 ++ [.start_ payment1 jan1])) alice home y =
      [6] := by decide

theorem b2_other_year_ignored :
    s7703_b_2_bbfb (hh (maintenance 1 ++ [.start_ payment1 janNext])) alice home y =
      [4] := by decide

theorem b2_zero_cost_fails :
    s7703_b_2_bbfb (hh []) alice home y = [] := by decide

theorem b2_overlapping_purpose_branches_count_twice :
    s7703_b_2_bbfb (hh
      [.residence_ home, .patient_ home home, .payment_ payment1,
       .agent_ payment1 alice, .purpose_ (.val payment1) home,
       .amount_ payment1 7, .start_ payment1 jan1]) alice home y = [14] := by decide

theorem b2_purpose_wildcard_matches_bound_payment :
    purposes (hh [.purpose_ (.wild 17) (.str "agricultural labor")]) payment1 =
      [.str "agricultural labor"] := by decide

def living (start : Day) (stops : List Day) : List Fact :=
  [.residence_ residence, .agent_ residence bob, .patient_ residence home,
   .start_ residence start] ++ stops.map (.end_ residence)

theorem member_inclusive_endpoints :
    s7703_b_3_is_member_of_household_bbb (hh (living jul1 [jul1])) bob home jul1 =
      [()] := by decide

theorem member_end_absent :
    s7703_b_3_is_member_of_household_bbb (hh (living jul1 [])) bob home dec31 =
      [()] := by decide

theorem member_duplicate_ends :
    s7703_b_3_is_member_of_household_bbb (hh (living jul1 [dec31, dec31])) bob home jul1 =
      [(), ()] := by decide

theorem b3_no_residence :
    s7703_b_3_bfbb (hh married) alice home y = [bob] := by decide

theorem b3_july1_excluded :
    s7703_b_3_bfbb (hh (married ++ living jul1 [jul1])) alice home y = [] := by decide

theorem b3_june30_outside_window :
    s7703_b_3_bfbb (hh (married ++ living (jul1 - 1) [jul1 - 1])) alice home y =
      [bob] := by decide

theorem b3_dec31_excluded :
    s7703_b_3_bfbb (hh (married ++ living dec31 [dec31])) alice home y = [] := by decide

theorem b3_next_jan1_outside_window :
    s7703_b_3_bfbb (hh (married ++ living janNext [])) alice home y = [bob] := by decide

theorem b3_marriage_multiplicity :
    s7703_b_3_bfbb (hh (married ++ [.agent_ marriage bob])) alice home y =
      [bob, bob] := by decide

def childHome (stop : Day) : List Fact :=
  [.residence_ (.atom "taxpayer_residence"), .agent_ (.atom "taxpayer_residence") alice,
   .patient_ (.atom "taxpayer_residence") home] ++ living jan1 [stop]

theorem b1_insufficient_duration_without_any_dependency_assumption
    (checked : CoveredR5Time (.year y))
    (dependency : (d t : Term) → (year : Year) → CoveredR5Time (.year year) → List Unit) :
    s7703_b_1_bffb (hh (childHome jul1)) alice y checked dependency = [] := by rfl

theorem b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity
    (checked : CoveredR5Time (.year y))
    (dependency : (d t : Term) → (year : Year) → CoveredR5Time (.year year) → List Unit) :
    s7703_b_1_bffb (hh (childHome (jul1 + 1))) alice y checked dependency =
      (dependency bob alice y checked).flatMap (fun _ => [(home, bob)]) := by
  simp [Bind.bind, Pure.pure, BEq.beq, instBEqTerm, instBEqTerm.beq,
    s7703_b_1_bffb, s7703_b_1_clause1, childHome, living, hh, markers,
    agents, patients, ends, Household.startDays, succeed, firstDay, lastDay,
    y, jan1, jul1, julyFirst, home, residence, alice, bob]

theorem b1_exact_joint_return_blocks_without_any_dependency_assumption
    (checked : CoveredR5Time (.year y))
    (dependency : (d t : Term) → (year : Year) → CoveredR5Time (.year year) → List Unit) :
    s7703_b_1_bffb (hh (childHome dec31 ++
      [.joint_return_ (.atom "joint"), .agent_ (.atom "joint") alice,
       .start_ (.atom "joint") jan1, .end_ (.atom "joint") dec31]))
      alice y checked dependency = [] := by rfl

theorem a1_admission_checks_actual_year : (a1Query alice 2101).v3 = false := by decide
theorem b3_admission_checks_actual_year : (b3Query alice home 2101).v3 = false := by decide

theorem b1_certificate_is_for_the_actual_year (checked : CoveredR5Time (.year y)) :
    checked.year.value ∈ r5Years := checked.year_covered

theorem a1_null_only_at_observation :
    observe (a1Solutions (s7703_a_1_bfffb (hh married) alice y)) =
      ["[{\"a\":\"bob\"},{\"a\":\"marriage\"},null]"] := by
  rw [a1_absent_start_and_end]
  simp only [a1Solutions, termObs, bob, marriage, observe, List.map_cons, List.map_nil,
    Solution.encode, Obs.encode, escapeJson, String.foldl_eq_foldl_toList]
  decide

theorem b3_deduplication_only_at_observation :
    observe (b3Solutions (s7703_b_3_bfbb
      (hh (married ++ [.agent_ marriage bob])) alice home y)) =
      ["[{\"a\":\"bob\"}]"] := by
  rw [b3_marriage_multiplicity]
  simp only [b3Solutions, termObs, bob, observe, List.map_cons, List.map_nil,
    Solution.encode, Obs.encode, escapeJson, String.foldl_eq_foldl_toList]
  decide

-- Axiom checks for every clause, entry wrapper, and the parameterized proof.
#print axioms s7703_a_1_clause1
#print axioms s7703_a_2_clause1
#print axioms s7703_a_clause1
#print axioms s7703_b_1_clause1
#print axioms s7703_b_2_clause1
#print axioms s7703_b_3_is_member_of_household_clause1
#print axioms s7703_b_3_clause1
#print axioms s7703_a_1_entry
#print axioms s7703_a_2_entry
#print axioms s7703_b_1_entry
#print axioms s7703_b_2_entry
#print axioms s7703_b_3_entry
#print axioms b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity
#print axioms b3_deduplication_only_at_observation

end KMLA.Oracle.S7703.Tests
