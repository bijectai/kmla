import Oracle.S7703

/-!
Kernel checks of the bounded §7703 bffb/bbfb StipArg adaptation.
H4/G1/A1/A3 preserve aliases within recursive proper lists and across positions;
each clause/call receives fresh variables. H6.2 observes lists recursively.
These are explicit head-shape checks, not ValidStip, source parity or R5 proofs.
Assembly checks quantify over the actual missing provider and time certificate.
-/

namespace KMLA.Oracle.S7703.StipListTests

def alice : Term := .atom "alice"
def bob : Term := .atom "bob"
def marriage : Term := .atom "marriage"

def nested : Stip :=
  ⟨.s7703_4, [.val alice, .wild 7,
    .list [.wild 7, .list [.wild 8, .wild 7], .wild 8, .list []], .val (.int 2015)]⟩

def nestedRow (first second : Nat) : StipArg × StipArg :=
  (.wild first, .list [.wild first, .list [.wild second, .wild first],
    .wild second, .list []])

theorem nested_aliases_share_one_renaming_table :
    Stipulation.solutions alice none 2015 100 [nested] (by decide) =
      (102, [nestedRow 100 101]) := by rfl

theorem distinct_ids_allocate_in_depth_first_head_order :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice,
        .list [.wild 9, .list [.wild 7, .wild 9], .wild 8],
        .list [.wild 8, .wild 7, .wild 9], .val (.int 2015)]⟩] (by decide) =
      (103, [(.list [.wild 100, .list [.wild 101, .wild 100], .wild 102],
        .list [.wild 102, .wild 101, .wild 100])]) := by rfl

theorem nested_first_occurrence_aliases_later_scalar_position :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice, .list [.list [.wild 7, .wild 7]],
        .wild 7, .val (.int 2015)]⟩] (by decide) =
      (101, [(.list [.list [.wild 100, .wild 100]], .wild 100)]) := by rfl

theorem taxpayer_and_late_year_bind_every_nested_alias :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.wild 7,
        .list [.wild 8, .list [.wild 7, .wild 9, .wild 8]],
        .list [.wild 9, .wild 8, .wild 7, .list [.wild 9]], .wild 9]⟩]
      (by decide) =
      (103, [(.list [.wild 101, .list [.val alice, .val (.int 2015), .wild 101]],
        .list [.val (.int 2015), .wild 101, .val alice, .list [.val (.int 2015)]])]) := by rfl

theorem bound_spouse_resolves_nested_marriage_aliases :
    Stipulation.solutions alice (some bob) 2015 100 [nested] (by decide) =
      (102, [(.val bob, .list [.val bob, .list [.wild 101, .val bob],
        .wild 101, .list []])]) := by rfl

theorem later_spouse_binding_reaches_nested_aliases :
    Stipulation.bindSpouse (nestedRow 100 101) bob =
      some (.val bob, .list [.val bob, .list [.wild 101, .val bob],
        .wild 101, .list []]) := by rfl

theorem nested_binding_preserves_scalar_string_tag :
    Stipulation.bindSpouse (nestedRow 100 101) (.str "bob") =
      some (.val (.str "bob"), .list [.val (.str "bob"),
        .list [.wild 101, .val (.str "bob")], .wild 101, .list []]) := by rfl

theorem inconsistent_bound_alias_with_nested_occurrences_fails :
    Stipulation.solutions alice (some bob) 2015 100
      [⟨.s7703_4, [.wild 7, .wild 7, .list [.list [.wild 7]], .val (.int 2015)]⟩]
      (by decide) = (101, []) := by rfl

theorem list_taxpayer_cannot_match_scalar_input :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.list [.val alice], .val bob, .list [], .val (.int 2015)]⟩]
      (by decide) = (100, []) := by rfl

theorem list_spouse_cannot_match_scalar_input :
    Stipulation.solutions alice (some bob) 2015 100
      [⟨.s7703_4, [.val alice, .list [.val bob], .wild 7, .val (.int 2015)]⟩]
      (by decide) = (101, []) := by rfl

theorem list_year_cannot_match_scalar_input :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice, .wild 7, .list [.wild 7], .list [.val (.int 2015)]]⟩]
      (by decide) = (101, []) := by rfl

theorem empty_list_taxpayer_is_not_scalar_empty_list_atom :
    Stipulation.solutions (.atom "[]") none 2015 100
      [⟨.s7703_4, [.list [], .val bob, .list [], .val (.int 2015)]⟩]
      (by decide) = (100, []) := by rfl

theorem empty_list_spouse_is_not_scalar_empty_list_atom :
    Stipulation.solutions alice (some (.atom "[]")) 2015 100
      [⟨.s7703_4, [.val alice, .list [], .list [], .val (.int 2015)]⟩]
      (by decide) = (100, []) := by rfl

theorem later_list_spouse_constraint_fails :
    Stipulation.bindSpouse (.list [], .list [.wild 100]) (.atom "[]") = none := by rfl

theorem scalar_empty_list_atom_still_matches_itself :
    Stipulation.solutions (.atom "[]") (some (.atom "[]")) 2015 100
      [⟨.s7703_4, [.val (.atom "[]"), .val (.atom "[]"), .list [], .val (.int 2015)]⟩]
      (by decide) = (100, [(.val (.atom "[]"), .list [])]) := by rfl

theorem empty_output_lists_remain_two_output_positions :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice, .list [], .list [], .val (.int 2015)]⟩]
      (by decide) = (100, [(.list [], .list [])]) := by rfl

def tagged : StipArg :=
  .list [.val (.atom "7"), .val (.str "7"), .val (.int 7),
    .val (.int 18446744073709551617), .val (.int (-18446744073709551617)),
    .list [], .val (.atom "[]"), .val (.str "[]"), .val (.int 7)]

theorem list_tags_large_integers_order_and_duplicates_survive :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.val alice, tagged, .list [tagged], .val (.int 2015)]⟩]
      (by decide) = (100, [(tagged, .list [tagged])]) := by rfl

theorem duplicate_nested_clauses_keep_distinct_fresh_copies :
    Stipulation.solutions alice none 2015 100 [nested, nested] (by decide) =
      (104, [nestedRow 100 101, nestedRow 102 103]) := by rfl

theorem repeated_nested_calls_thread_the_supply :
    (let first := Stipulation.solutions alice none 2015 100 [nested] (by decide)
     let second := Stipulation.solutions alice none 2015 first.1 [nested] (by decide)
     (first.2, second.2, second.1)) =
      ([nestedRow 100 101], [nestedRow 102 103], 104) := by rfl

theorem binding_one_copy_preserves_another_copy :
    (([nestedRow 100 101, nestedRow 102 103]).head?.bind
      (fun row => Stipulation.bindSpouse row bob),
     ([nestedRow 100 101, nestedRow 102 103]).tail) =
      (some (.val bob, .list [.val bob, .list [.wild 101, .val bob],
        .wild 101, .list []]), [nestedRow 102 103]) := by rfl

theorem failed_list_head_consumes_ids_but_not_bindings :
    Stipulation.solutions alice none 2015 100
      [⟨.s7703_4, [.list [.wild 7, .list [.wild 7, .wild 8]],
        .wild 8, .list [.wild 9], .val (.int 2015)]⟩, nested]
      (by decide) = (105, [nestedRow 103 104]) := by rfl

theorem unrelated_signature_keeps_nested_clause_order_and_supply :
    Stipulation.solutions alice none 2015 100
      [nested, ⟨.s151_5, [.wild 7, .list [.wild 8], .list [],
        .list [.wild 9], .val (.int 2015)]⟩, nested] (by decide) =
      (104, [nestedRow 100 101, nestedRow 102 103]) := by rfl

theorem arbitrary_supply_keeps_nested_aliases (next : Nat) :
    Stipulation.solutions alice none 2015 next [nested] (by decide) =
      (next + 1 + 1, [nestedRow next (next + 1)]) := by rfl

theorem nested_observer_preserves_tags_and_exact_integers :
    stipArgObs tagged =
      .arr [.atom "7", .str "7", .num 7,
        .num 18446744073709551617, .num (-18446744073709551617),
        .arr [], .atom "[]", .str "[]", .num 7] := by rfl

theorem nested_observer_preserves_structure_and_duplicate_elements :
    rootBffbSolutions [nestedRow 100 101, nestedRow 102 103] =
      [[.null, .arr [.null, .arr [.null, .null], .null, .arr []]],
       [.null, .arr [.null, .arr [.null, .null], .null, .arr []]]] := by rfl

theorem empty_list_atom_string_and_unbound_observe_differently :
    rootBbfbSolutions [.list [], .val (.atom "[]"), .val (.str "[]"), .wild 0] =
      [[.arr []], [.atom "[]"], [.str "[]"], [.null]] := by rfl

theorem empty_and_nested_empty_lists_encode_as_arrays :
    observe (rootBffbSolutions [(.list [], .list [.list [], .list []])]) =
      ["[[],[[],[]]]"] := by
  change observe [[.arr [], .arr [.arr [], .arr []]]] = ["[[],[[],[]]]"]
  simp only [observe, List.map_cons, List.map_nil, Solution.encode, Obs.encode,
    List.mergeSort]
  decide

theorem nested_duplicate_solutions_deduplicate_only_at_observation :
    observe (rootBffbSolutions [nestedRow 100 101, nestedRow 102 103]) =
      ["[null,[null,[null,null],null,[]]]"] := by
  rw [nested_observer_preserves_structure_and_duplicate_elements]
  simp only [observe, List.map_cons, List.map_nil, Solution.encode, Obs.encode]
  rw [List.mergeSort_of_pairwise (by simp)]
  decide

theorem list_element_duplicates_survive_canonical_observation :
    observe (rootBbfbSolutions [.list [.val (.int 7), .val (.int 7), .list []]]) =
      ["[[7,7,[]]]"] := by
  change observe [[.arr [.num 7, .num 7, .arr []]]] = ["[[7,7,[]]]"]
  simp only [observe, List.map_cons, List.map_nil, Solution.encode, Obs.encode,
    List.mergeSort]
  decide

section Assembly
variable (checked : CoveredR5Time (.year 2015))
variable (dependency : (d t : Term) → (year : Year) → CoveredR5Time (.year year) → List Unit)

def household : Household :=
  ⟨[.marriage_ marriage, .agent_ marriage alice, .agent_ marriage bob], [nested, nested]⟩

theorem statute_precedes_nested_stipulations :
    s7703_bffb household alice 2015 checked dependency 100 (by decide) =
      (104, [(.val bob, .val marriage), nestedRow 100 101, nestedRow 102 103]) := by rfl

theorem bbfb_keeps_doubled_statute_and_bound_nested_outputs :
    s7703_bbfb household alice bob 2015 checked dependency 100 (by decide) =
      (104, [.val marriage, .val marriage,
        .list [.val bob, .list [.wild 101, .val bob], .wild 101, .list []],
        .list [.val bob, .list [.wild 103, .val bob], .wild 103, .list []]]) := by rfl

theorem free_spouse_can_be_a_nested_list :
    s7703_bffb ⟨[], [⟨.s7703_4, [.val alice, .list [.list [.wild 7]],
      .wild 7, .val (.int 2015)]⟩]⟩ alice 2015 checked dependency 100 (by decide) =
      (101, [(.list [.list [.wild 100]], .wild 100)]) := by rfl

theorem bbfb_rejects_list_spouse_without_discarding_other_clauses :
    s7703_bbfb ⟨[], [⟨.s7703_4, [.val alice, .list [.val bob],
      .wild 7, .val (.int 2015)]⟩, nested]⟩
      alice bob 2015 checked dependency 100 (by decide) =
      (103, [.list [.val bob, .list [.wild 102, .val bob], .wild 102, .list []]]) := by rfl

theorem stipulated_nested_output_bypasses_statute_identity_guard :
    s7703_bbfb ⟨[], [nested]⟩ alice alice 2015 checked dependency 100 (by decide) =
      (102, [.list [.val alice, .list [.wild 101, .val alice], .wild 101, .list []]]) := by rfl

theorem bbfb_observation_retains_resolved_nested_output :
    rootBbfbSolutions
      (s7703_bbfb ⟨[], [nested]⟩ alice bob 2015 checked dependency 100 (by decide)).2 =
      [[.arr [.atom "bob", .arr [.null, .atom "bob"], .null, .arr []]]] := by rfl

end Assembly

#print axioms Stipulation.solutions
#print axioms Stipulation.bindSpouse
#print axioms Stipulation.admitted_shape
#print axioms s7703_bffb
#print axioms s7703_bbfb
#print axioms s7703_bffb_entry
#print axioms s7703_bbfb_entry
#print axioms stipArgObs
#print axioms rootBffbSolutions
#print axioms rootBbfbSolutions
#print axioms nested_aliases_share_one_renaming_table
#print axioms distinct_ids_allocate_in_depth_first_head_order
#print axioms nested_first_occurrence_aliases_later_scalar_position
#print axioms taxpayer_and_late_year_bind_every_nested_alias
#print axioms bound_spouse_resolves_nested_marriage_aliases
#print axioms later_spouse_binding_reaches_nested_aliases
#print axioms nested_binding_preserves_scalar_string_tag
#print axioms inconsistent_bound_alias_with_nested_occurrences_fails
#print axioms list_taxpayer_cannot_match_scalar_input
#print axioms list_spouse_cannot_match_scalar_input
#print axioms list_year_cannot_match_scalar_input
#print axioms empty_list_taxpayer_is_not_scalar_empty_list_atom
#print axioms empty_list_spouse_is_not_scalar_empty_list_atom
#print axioms later_list_spouse_constraint_fails
#print axioms scalar_empty_list_atom_still_matches_itself
#print axioms empty_output_lists_remain_two_output_positions
#print axioms list_tags_large_integers_order_and_duplicates_survive
#print axioms duplicate_nested_clauses_keep_distinct_fresh_copies
#print axioms repeated_nested_calls_thread_the_supply
#print axioms binding_one_copy_preserves_another_copy
#print axioms failed_list_head_consumes_ids_but_not_bindings
#print axioms unrelated_signature_keeps_nested_clause_order_and_supply
#print axioms arbitrary_supply_keeps_nested_aliases
#print axioms nested_observer_preserves_tags_and_exact_integers
#print axioms nested_observer_preserves_structure_and_duplicate_elements
#print axioms empty_list_atom_string_and_unbound_observe_differently
#print axioms empty_and_nested_empty_lists_encode_as_arrays
#print axioms nested_duplicate_solutions_deduplicate_only_at_observation
#print axioms list_element_duplicates_survive_canonical_observation
#print axioms statute_precedes_nested_stipulations
#print axioms bbfb_keeps_doubled_statute_and_bound_nested_outputs
#print axioms free_spouse_can_be_a_nested_list
#print axioms bbfb_rejects_list_spouse_without_discarding_other_clauses
#print axioms stipulated_nested_output_bypasses_statute_identity_guard
#print axioms bbfb_observation_retains_resolved_nested_output

end KMLA.Oracle.S7703.StipListTests
