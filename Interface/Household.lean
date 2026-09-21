/-
DRAFT ONLY — pending the owner's human/DECISIONS.md and Checkpoint 0 approval.

Syntax inventory: human/sara/sara/statutes/prolog/events.pl and the 376 files
human/sara/sara/cases/*.pl. See docs/contracts/HOUSEHOLD.md for every observed
signature, argument shape, source citation, unsupported form, and open decision.

This is a source-syntax draft, not the approved Int-cent/day-count interface.
No Prolog evaluation, normalization, domain validity, defaults, or tax semantics
are supplied. In particular, raw rules/directives are unsupported source records,
not executable household facts. No full-corpus round-trip claim is made.
-/

namespace HouseholdDraft

/--
Only argument forms observed in bodyless clauses. String payloads retain source
lexemes, not decoded Prolog values: doubleQuoted includes the quote characters;
unsignedDecimal retains its digits without choosing a numeric interpretation.
Each anonymousVariable is a separate occurrence of the source token "_".
atomList retains the order and multiplicity of its unquoted atom lexemes.

These constructors do not validate their String payloads or approve a domain.
Named variables and quoted atoms occur in rules but have no typed representation
here; retain those complete rules as unsupportedRule.
-/
inductive Argument where
  | unquotedAtom (lexeme : String)
  | doubleQuoted (lexeme : String)
  | unsignedDecimal (lexeme : String)
  | anonymousVariable
  | atomList (lexemes : List String)

/--
The 79 distinct name/arity pairs actually occurring as bodyless clause heads.
The arity index records syntax only. Rule-only, declaration-only and query-only
predicates are documented, not promoted to facts. There is no other-predicate
constructor. Distinct arities and patient/2 versus patient_/2 remain distinct.
-/
inductive FactPredicate : Nat → Type where
  | agent__arity2 : FactPredicate 2
  | american_employer__arity1 : FactPredicate 1
  | amount__arity2 : FactPredicate 2
  | attending_classes__arity1 : FactPredicate 1
  | beneficiary__arity2 : FactPredicate 2
  | birth__arity1 : FactPredicate 1
  | blindness__arity1 : FactPredicate 1
  | brother__arity1 : FactPredicate 1
  | business__arity1 : FactPredicate 1
  | business_trust__arity1 : FactPredicate 1
  | citizenship__arity1 : FactPredicate 1
  | country__arity2 : FactPredicate 2
  | daughter__arity1 : FactPredicate 1
  | death__arity1 : FactPredicate 1
  | deduction__arity1 : FactPredicate 1
  | destination__arity2 : FactPredicate 2
  | disability__arity1 : FactPredicate 1
  | educational_institution__arity1 : FactPredicate 1
  | end__arity2 : FactPredicate 2
  | enrollment__arity1 : FactPredicate 1
  | father__arity1 : FactPredicate 1
  | hospital__arity1 : FactPredicate 1
  | incarceration__arity1 : FactPredicate 1
  | income__arity1 : FactPredicate 1
  | international_organization__arity1 : FactPredicate 1
  | joint_return__arity1 : FactPredicate 1
  | legal_separation__arity1 : FactPredicate 1
  | location__arity2 : FactPredicate 2
  | marriage__arity1 : FactPredicate 1
  | means__arity2 : FactPredicate 2
  | medical_institution__arity1 : FactPredicate 1
  | medical_patient__arity1 : FactPredicate 1
  | migration__arity1 : FactPredicate 1
  | mother__arity1 : FactPredicate 1
  | nonresident_alien__arity1 : FactPredicate 1
  | nurses_training_school__arity1 : FactPredicate 1
  | patient_arity2 : FactPredicate 2
  | patient__arity2 : FactPredicate 2
  | payment__arity1 : FactPredicate 1
  | penal_institution__arity1 : FactPredicate 1
  | plan__arity1 : FactPredicate 1
  | purpose__arity2 : FactPredicate 2
  | reason__arity2 : FactPredicate 2
  | residence__arity1 : FactPredicate 1
  | retirement__arity1 : FactPredicate 1
  | s151_arity5 : FactPredicate 5
  | s151_b_arity3 : FactPredicate 3
  | s151_b_applies_arity2 : FactPredicate 2
  | s151_b_applies_arity3 : FactPredicate 3
  | s151_c_arity4 : FactPredicate 4
  | s151_c_applies_arity3 : FactPredicate 3
  | s151_d_arity4 : FactPredicate 4
  | s152_b_2_arity4 : FactPredicate 4
  | s152_c_arity3 : FactPredicate 3
  | s152_c_1_arity3 : FactPredicate 3
  | s152_c_2_arity4 : FactPredicate 4
  | s2_a_arity3 : FactPredicate 3
  | s2_a_arity5 : FactPredicate 5
  | s2_b_arity3 : FactPredicate 3
  | s3306_b_arity8 : FactPredicate 8
  | s63_arity3 : FactPredicate 3
  | s63_c_arity3 : FactPredicate 3
  | s63_c_1_arity3 : FactPredicate 3
  | s63_c_2_arity3 : FactPredicate 3
  | s63_c_3_arity3 : FactPredicate 3
  | s63_c_3_arity4 : FactPredicate 4
  | s63_d_arity4 : FactPredicate 4
  | s63_f_1_A_arity2 : FactPredicate 2
  | s63_f_1_B_arity3 : FactPredicate 3
  | s68_b_arity3 : FactPredicate 3
  | s7703_arity4 : FactPredicate 4
  | service__arity1 : FactPredicate 1
  | sibling__arity1 : FactPredicate 1
  | sister__arity1 : FactPredicate 1
  | son__arity1 : FactPredicate 1
  | start__arity2 : FactPredicate 2
  | termination__arity1 : FactPredicate 1
  | total_wages_employer_arity6 : FactPredicate 6
  | type__arity2 : FactPredicate 2

/-- Argument count is structural; per-position kinds and groundness are not checked. -/
inductive Fact where
  | mk {arity : Nat}
      (predicate : FactPredicate arity)
      (arguments : Vector Argument arity)

/--
One source-order item. A fact is a bodyless clause and may contain "_"; it is not
necessarily ground. Unsupported source payloads retain the entire terminated
clause/directive, including its body, rather than a materialized fact expansion.
They must be reported as unsupported before any downstream semantic processing.
Unknown predicate signatures or new forms require review, not coercion into a
known fact constructor. There is deliberately no evaluator or fallback behavior.
-/
inductive Item where
  | fact (head : Fact)
  | unsupportedRule (source : String)
  | unsupportedDirective (source : String)

/--
DRAFT shared source-syntax container for one case. The single list preserves
cross-predicate order and duplicate occurrences, including repeated arguments.
An absent fact has no entry; no value is inserted for it. No semantic conclusion
about absence follows. No fields have defaults and no fact is keyed by event ID.

This namespace intentionally does not publish an approved global Household or
Year. The eventual semantic interface still requires the owner's decisions.
-/
structure Household where
  items : List Item

end HouseholdDraft
