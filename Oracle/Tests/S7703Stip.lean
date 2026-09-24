import Oracle.S7703

/-! Self-contained kernel tests, not Prolog parity or production admission.
All assembly tests quantify over the actual missing provider; none supplies
a dummy implementation or OracleGuards instance. Existing 62 tests are separate
and unchanged. Every shape proof below checks only stipulated arity.
-/

namespace KMLA.Oracle.S7703.StipTests

def alice : Term := .atom "alice"
def bob : Term := .atom "bob"
def marriage : Term := .atom "marriage"

def one : Stip := ⟨.s7703_4, [.val alice, .val bob, .wild 7, .val (.int 2015)]⟩
def shared : Stip := ⟨.s7703_4, [.val alice, .wild 7, .wild 7, .val (.int 2015)]⟩
def distinct : Stip := ⟨.s7703_4, [.val alice, .wild 7, .wild 8, .val (.int 2015)]⟩

theorem one_fresh_at_any_supply (next : Nat) :
    Stipulation.solutions alice none 2015 next [one] (by decide) =
      (next + 1, [(.val bob, .wild next)]) := by rfl

theorem duplicate_clauses_kept_and_freshened :
    Stipulation.solutions alice none 2015 100 [one, one] (by decide) =
      (102, [(.val bob, .wild 100), (.val bob, .wild 101)]) := by rfl

theorem within_clause_shared_output_variable :
    Stipulation.solutions alice none 2015 100 [shared] (by decide) =
      (101, [(.wild 100, .wild 100)]) := by rfl

theorem distinct_output_variables_not_aliased :
    Stipulation.solutions alice none 2015 100 [distinct] (by decide) =
      (102, [(.wild 100, .wild 101)]) := by rfl

theorem repeated_clauses_do_not_share_stored_variable_names :
    Stipulation.solutions alice none 2015 100 [shared, shared] (by decide) =
      (102, [(.wild 100, .wild 100), (.wild 101, .wild 101)]) := by rfl

theorem repeated_calls_thread_the_supply :
    (let first := Stipulation.solutions alice none 2015 100 [shared] (by decide)
     let second := Stipulation.solutions alice none 2015 first.1 [shared] (by decide)
     (first.2, second.2, second.1)) =
      ([ (.wild 100, .wild 100) ], [ (.wild 101, .wild 101) ], 102) := by rfl

theorem year_binding_propagates_to_both_outputs :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice, .wild 7, .wild 7, .wild 7]⟩] (by decide) =
      (101, [(.val (.int 2015), .val (.int 2015))]) := by rfl

theorem taxpayer_binding_propagates_to_free_spouse :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.wild 7, .wild 7, .wild 8, .val (.int 2015)]⟩] (by decide) =
      (102, [(.val alice, .wild 101)]) := by rfl

theorem shared_wildcard_rejects_inconsistent_bound_inputs :
    Stipulation.solutions alice (some bob) 2015 100
      [⟨.s7703_4, [.wild 7, .wild 7, .wild 8, .val (.int 2015)]⟩] (by decide) =
      (102, []) := by rfl

theorem shared_wildcard_accepts_consistent_bound_inputs :
    Stipulation.solutions alice (some alice) 2015 100
      [⟨.s7703_4, [.wild 7, .wild 7, .wild 8, .val (.int 2015)]⟩] (by decide) =
      (102, [(.val alice, .wild 101)]) := by rfl

theorem shared_variable_constraint_is_tag_sensitive :
    Stipulation.solutions alice (some (.str "alice")) 2015 100
      [⟨.s7703_4, [.wild 7, .wild 7, .wild 8, .val (.int 2015)]⟩] (by decide) =
      (102, []) := by rfl

theorem literal_constraint_is_tag_sensitive :
    Stipulation.solutions alice (some (.str "bob")) 2015 100 [one] (by decide) =
      (101, []) := by rfl

theorem textual_year_does_not_match_integer :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice, .val bob, .wild 7, .val (.str "2015")]⟩]
      (by decide) = (101, []) := by rfl

theorem failed_head_does_not_bind_the_next_clause :
    Stipulation.solutions alice (some bob) 2015 100
      [⟨.s7703_4, [.wild 7, .wild 7, .wild 8, .val (.int 2015)]⟩, one]
      (by decide) = (103, [(.val bob, .wild 102)]) := by rfl

theorem other_signatures_do_not_reorder_matching_clauses :
    Stipulation.solutions alice none 2015 100
      [one, ⟨.s63_3, [.wild 7, .wild 8, .wild 9]⟩, shared] (by decide) =
      (102, [(.val bob, .wild 100), (.wild 101, .wild 101)]) := by rfl

theorem later_spouse_binding_preserves_alias :
    (Stipulation.solutions alice none 2015 100 [shared] (by decide)).2.head?.bind
      (fun row => Stipulation.bindSpouse row bob) =
      some (.val bob, .val bob) := by rfl

theorem later_spouse_binding_preserves_independent_marriage :
    (Stipulation.solutions alice none 2015 100 [distinct] (by decide)).2.head?.bind
      (fun row => Stipulation.bindSpouse row bob) =
      some (.val bob, .wild 101) := by rfl

theorem later_tag_mismatch_fails :
    Stipulation.bindSpouse (.val bob, .wild 100) (.str "bob") = none := by rfl

theorem unbound_is_null_only_at_observation :
    observe (rootBffbSolutions [(.wild 100, .wild 100)]) = ["[null,null]"] := by
  simp only [rootBffbSolutions, stipArgObs, observe, List.map_cons, List.map_nil,
    Solution.encode, Obs.encode, List.mergeSort]
  decide

theorem copied_variables_deduplicate_only_at_observation :
    observe (rootBffbSolutions [(.wild 100, .wild 100), (.wild 101, .wild 101)]) =
      ["[null,null]"] := by
  simp only [rootBffbSolutions, stipArgObs, observe, List.map_cons, List.map_nil,
    Solution.encode, Obs.encode]
  rw [List.mergeSort_of_pairwise (by simp)]
  decide

def household : Household :=
  ⟨[.marriage_ marriage, .agent_ marriage alice, .agent_ marriage bob], [one, one]⟩

section Assembly
variable (checked : CoveredR5Time (.year 2015))
variable (dependency : (d t : Term) → (year : Year) → CoveredR5Time (.year year) → List Unit)

theorem statute_precedes_duplicate_stipulated_clauses :
    s7703_bffb household alice 2015 checked dependency 100 (by decide) =
      (102, [(.val bob, .val marriage), (.val bob, .wild 100), (.val bob, .wild 101)]) := by rfl

theorem bbfb_doubles_statute_but_not_stipulated_clauses :
    s7703_bbfb household alice bob 2015 checked dependency 100 (by decide) =
      (102, [.val marriage, .val marriage, .wild 100, .wild 101]) := by rfl

theorem stipulated_clause_bypasses_statute_identity_guard :
    s7703_bbfb ⟨household.facts,
      [⟨.s7703_4, [.val alice, .val alice, .wild 7, .val (.int 2015)]⟩]⟩
      alice alice 2015 checked dependency 100 (by decide) = (101, [.wild 100]) := by rfl

theorem no_marriage_facts_required_for_stipulated_clause :
    s7703_bffb ⟨[], [shared]⟩ alice 2015 checked dependency 100 (by decide) =
      (101, [(.wild 100, .wild 100)]) := by rfl

theorem bbfb_bound_spouse_binds_shared_marriage :
    s7703_bbfb ⟨[], [shared]⟩ alice bob 2015 checked dependency 100 (by decide) =
      (101, [.val bob]) := by rfl

end Assembly

#print axioms Stipulation.solutions
#print axioms Stipulation.bindSpouse
#print axioms Stipulation.admitted_shape
#print axioms s7703_bffb
#print axioms s7703_bbfb
#print axioms s7703_bffb_entry
#print axioms s7703_bbfb_entry
#print axioms one_fresh_at_any_supply
#print axioms duplicate_clauses_kept_and_freshened
#print axioms within_clause_shared_output_variable
#print axioms distinct_output_variables_not_aliased
#print axioms repeated_clauses_do_not_share_stored_variable_names
#print axioms repeated_calls_thread_the_supply
#print axioms year_binding_propagates_to_both_outputs
#print axioms taxpayer_binding_propagates_to_free_spouse
#print axioms shared_wildcard_rejects_inconsistent_bound_inputs
#print axioms shared_wildcard_accepts_consistent_bound_inputs
#print axioms shared_variable_constraint_is_tag_sensitive
#print axioms literal_constraint_is_tag_sensitive
#print axioms textual_year_does_not_match_integer
#print axioms failed_head_does_not_bind_the_next_clause
#print axioms other_signatures_do_not_reorder_matching_clauses
#print axioms later_spouse_binding_preserves_alias
#print axioms later_spouse_binding_preserves_independent_marriage
#print axioms later_tag_mismatch_fails
#print axioms unbound_is_null_only_at_observation
#print axioms copied_variables_deduplicate_only_at_observation
#print axioms statute_precedes_duplicate_stipulated_clauses
#print axioms bbfb_doubles_statute_but_not_stipulated_clauses
#print axioms stipulated_clause_bypasses_statute_identity_guard
#print axioms no_marriage_facts_required_for_stipulated_clause
#print axioms bbfb_bound_spouse_binds_shared_marriage

end KMLA.Oracle.S7703.StipTests
