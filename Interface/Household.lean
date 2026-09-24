/-
Interface/Household.lean — the shared source-of-truth types for KMLA.

Implements the owner's `human/DECISIONS.md` (recorded 2026-09-21): G4 (term
domain), D1 (dates), H1 (shape), H2 (argument kinds), H3 (field list), H4
(stipulations) and H5 (`Valid`). Section ids in the doc comments cite that file,
which is the specification; where this file and `human/DECISIONS.md` disagree,
`human/DECISIONS.md` wins. The owner installed Option A's H5/R5/R8/R9 amendment
at `0a2a65a`; V10 below is part of both `Valid` and `ValidStip`.

This replaces the Phase 0.1 `HouseholdDraft`, which was a source-syntax
container (lexemes plus unparsed rule strings) written before the semantics were
decided. It could round-trip bytes but nothing could be computed from it.

Import discipline: `docs/PLAN.md` section 2.4 has the hygiene gate reject
imports outside `Interface/` and `Oracle/`, so this file uses core Lean 4 only —
no Mathlib, no Batteries. Everything decidable here is decidable by `decide`.

Not yet settled here, and deliberately so:
  * V7/V8 and V10's all-eligible-pairs decider depend on oracle definitions.
    `OracleGuards` has no default instance: the oracle lane must supply the
    actual guards and prove the V10 decider equivalent to its universal rule.
    Structural checks here do not decide that rule or prove R5/R8 termination.
  * `Interface/S{N}.lean` (H6.1 targets) is a separate per-section file.
-/

namespace KMLA

/-! ## Terms (G4) -/

/--
G4. The term domain. Equality is tag-sensitive: `atom "usa" ≠ str "usa"`, which
the owner probed on the pinned interpreter. Statute string literals only match
`str`; `atom_prefix/2` and `sub_atom/5` work on both tags.
-/
inductive Term where
  | atom (s : String)
  | str  (s : String)
  | int  (n : Int)
  deriving DecidableEq, Repr, Inhabited, BEq

/--
D1. Days since 1970-01-01 in the proleptic Gregorian calendar; `0 = 1970-01-01`.
Conversion to and from `YYYY-MM-DD` is the standard civil-date algorithm and the
serializer always emits four-digit zero-padded years.
-/
abbrev Day := Int

/-- D1. A taxable year. `Valid` restricts it to 1900 … 2100 (V3). -/
abbrev Year := Int

/-- Option A: every approved R5 query year, independently of `Valid`'s year index. -/
def r5Years : List Year := (List.range 201).map (fun n => 1900 + Int.ofNat n)

/-- A person is an `atom` term in every case file; the alias is for readability. -/
abbrev Person := Term

/--
H2/A3. A scalar event-fact pattern, used by the two original
`purpose_(_, "agricultural labor")` facts and the scalar query-time boundary.
Wildcard identity is carried by its id: a wildcard is identical only to itself.
Stipulation arguments use the distinct recursive `StipArg` below; event
positions do not gain a list constructor.
-/
inductive Pat where
  | val  (t : Term)
  | wild (id : Nat)
  deriving DecidableEq, Repr, Inhabited, BEq

/-! ## Facts (H2, H3) -/

/--
H3. One constructor per event predicate declared in `events.pl` that a case can
supply: 57 of the 61 declarations. The four omitted — `first_day_year/2`,
`gross_income/3`, `is_before/2`, `last_day_year/2` — are statute predicates that
no case defines, so they are not household data.

H2 fixes the argument kinds: `amount_` carries `Int` dollars (M1), `start_` and
`end_` carry a `Day`, and every other position carries a `Term` whose tag
reproduces the source lexeme's quoting. A wildcard is permitted only in
`purpose_` position 1, which is why that is the one constructor taking a `Pat`.

H4.2 grounding enumerates unary and binary event predicates only, so a grounded
household contains no arity-3 or arity-4 fact. The three case-local helper
names are represented anyway, because H3 puts every declared predicate in
`Household` and the serializer must round-trip what it is given; `Valid` V1
rejects them in a generated input.
-/
inductive Fact where

  /-- `agent_/2` — (event, participant): the actor of an event; marriages and joint returns lis (reads 154, case clauses 1358) -/
  | agent_ (event value : Term)
  /-- `agricultural_service/3` — case-local helper name (rules only) (reads 0, case clauses 2) -/
  | agricultural_service (a1 : Term) (a2 : Term) (a3 : Term)
  /-- `alice_employer/3` — case-local helper name (rules only) (reads 0, case clauses 1) -/
  | alice_employer (a1 : Term) (a2 : Term) (a3 : Term)
  /-- `alice_household_maintenance/4` — case-local helper name (rules only) (reads 0, case clauses 10) -/
  | alice_household_maintenance (a1 : Term) (a2 : Term) (a3 : Term) (a4 : Term)
  /-- `american_employer_/1` — (event id): event/status type marker (reads 1, case clauses 7) -/
  | american_employer_ (event : Term)
  /-- `amount_/2` — (event, Int dollars) (reads 7, case clauses 400) -/
  | amount_ (event : Term) (dollars : Int)
  /-- `attending_classes_/1` — (event id): event/status type marker (reads 2, case clauses 8) -/
  | attending_classes_ (event : Term)
  /-- `beneficiary_/2` — (plan event, person) (reads 2, case clauses 18) -/
  | beneficiary_ (event value : Term)
  /-- `birth_/1` — (event id): event/status type marker (reads 7, case clauses 29) -/
  | birth_ (event : Term)
  /-- `blindness_/1` — (event id): event/status type marker (reads 2, case clauses 7) -/
  | blindness_ (event : Term)
  /-- `brother_/1` — (event id): event/status type marker (reads 1, case clauses 13) -/
  | brother_ (event : Term)
  /-- `business_/1` — (event id): event/status type marker (reads 1, case clauses 2) -/
  | business_ (event : Term)
  /-- `business_trust_/1` — (event id): event/status type marker (reads 1, case clauses 2) -/
  | business_trust_ (event : Term)
  /-- `citizenship_/1` — (event id): event/status type marker (reads 2, case clauses 14) -/
  | citizenship_ (event : Term)
  /-- `country_/2` — (place, country string) (reads 4, case clauses 14) -/
  | country_ (event value : Term)
  /-- `daughter_/1` — (event id): event/status type marker (reads 2, case clauses 1) -/
  | daughter_ (event : Term)
  /-- `death_/1` — (event id): event/status type marker (reads 12, case clauses 50) -/
  | death_ (event : Term)
  /-- `deduction_/1` — (event id): event/status type marker (reads 2, case clauses 20) -/
  | deduction_ (event : Term)
  /-- `destination_/2` — (migration event, place) (reads 1, case clauses 1) -/
  | destination_ (event value : Term)
  /-- `disability_/1` — (event id): event/status type marker (reads 1, case clauses 4) -/
  | disability_ (event : Term)
  /-- `educational_institution_/1` — (event id): event/status type marker (reads 1, case clauses 7) -/
  | educational_institution_ (event : Term)
  /-- `end_/2` — (event, Day) (reads 95, case clauses 453) -/
  | end_ (event : Term) (day : Day)
  /-- `enrollment_/1` — (event id): event/status type marker (reads 2, case clauses 8) -/
  | enrollment_ (event : Term)
  /-- `father_/1` — (event id): event/status type marker (reads 1, case clauses 35) -/
  | father_ (event : Term)
  /-- `hospital_/1` — (event id): event/status type marker (reads 2, case clauses 4) -/
  | hospital_ (event : Term)
  /-- `incarceration_/1` — (event id): event/status type marker (reads 1, case clauses 3) -/
  | incarceration_ (event : Term)
  /-- `income_/1` — (event id): event/status type marker (reads 1, case clauses 122) -/
  | income_ (event : Term)
  /-- `international_organization_/1` — (event id): event/status type marker (reads 1, case clauses 1) -/
  | international_organization_ (event : Term)
  /-- `itemize_deductions_/1` — (event id): event/status type marker (reads 0, case clauses 0) -/
  | itemize_deductions_ (event : Term)
  /-- `joint_return_/1` — (event id): event/status type marker (reads 15, case clauses 55) -/
  | joint_return_ (event : Term)
  /-- `legal_separation_/1` — (event id): event/status type marker (reads 2, case clauses 6) -/
  | legal_separation_ (event : Term)
  /-- `location_/2` — (event, place or location string); several per event allowed and semanticall (reads 5, case clauses 113) -/
  | location_ (event value : Term)
  /-- `marriage_/1` — (event id): event/status type marker (reads 17, case clauses 156) -/
  | marriage_ (event : Term)
  /-- `means_/2` — (payment, medium string or plan) (reads 10, case clauses 13) -/
  | means_ (event value : Term)
  /-- `medical_institution_/1` — (event id): event/status type marker (reads 0, case clauses 1) -/
  | medical_institution_ (event : Term)
  /-- `medical_patient_/1` — (event id): event/status type marker (reads 1, case clauses 4) -/
  | medical_patient_ (event : Term)
  /-- `migration_/1` — (event id): event/status type marker (reads 1, case clauses 1) -/
  | migration_ (event : Term)
  /-- `mother_/1` — (event id): event/status type marker (reads 1, case clauses 3) -/
  | mother_ (event : Term)
  /-- `nonresident_alien_/1` — (event id): event/status type marker (reads 5, case clauses 14) -/
  | nonresident_alien_ (event : Term)
  /-- `nurses_training_school_/1` — (event id): event/status type marker (reads 2, case clauses 1) -/
  | nurses_training_school_ (event : Term)
  /-- `patient/2` — declared without underscore; never read by any statute; inert if present (reads 0, case clauses 2) -/
  | patient (event value : Term)
  /-- `patient_/2` — (event, participant | place | plan): the undergoer; for `service_` the emplo (reads 52, case clauses 624) -/
  | patient_ (event value : Term)
  /-- `payment_/1` — (event id): event/status type marker (reads 6, case clauses 259) -/
  | payment_ (event : Term)
  /-- `penal_institution_/1` — (event id): event/status type marker (reads 1, case clauses 2) -/
  | penal_institution_ (event : Term)
  /-- `plan_/1` — (event id): event/status type marker (reads 4, case clauses 17) -/
  | plan_ (event : Term)
  /-- `purpose_/2` — (event, purpose string | service | place); wildcard first argument occurs in (reads 24, case clauses 230) -/
  | purpose_ (event : Pat) (purpose : Term)
  /-- `reason_/2` — (termination event, reason event) (reads 1, case clauses 10) -/
  | reason_ (event value : Term)
  /-- `residence_/1` — (event id): event/status type marker (reads 14, case clauses 141) -/
  | residence_ (event : Term)
  /-- `retirement_/1` — (event id): event/status type marker (reads 0, case clauses 11) -/
  | retirement_ (event : Term)
  /-- `service_/1` — (event id): event/status type marker (reads 10, case clauses 96) -/
  | service_ (event : Term)
  /-- `sibling_/1` — (event id): event/status type marker (reads 0, case clauses 2) -/
  | sibling_ (event : Term)
  /-- `sister_/1` — (event id): event/status type marker (reads 1, case clauses 3) -/
  | sister_ (event : Term)
  /-- `son_/1` — (event id): event/status type marker (reads 2, case clauses 72) -/
  | son_ (event : Term)
  /-- `start_/2` — (event, Day) (reads 106, case clauses 1065) -/
  | start_ (event : Term) (day : Day)
  /-- `termination_/1` — (event id): event/status type marker (reads 1, case clauses 5) -/
  | termination_ (event : Term)
  /-- `type_/2` — (event, type string) (reads 9, case clauses 4) -/
  | type_ (event value : Term)
  /-- `unemployment_compensation_agreement_/1` — (event id): event/status type marker (reads 1, case clauses 0) -/
  | unemployment_compensation_agreement_ (event : Term)
  deriving DecidableEq, Repr, Inhabited

/-! ## Stipulations (H4) -/

/--
H4.1/H4.2(iii). One supplied stipulation argument: a G4 scalar, an unbound
variable identified by its existing id, or a finite proper list of arguments.
Lists preserve nesting, order, duplicates and ids shared with other positions.
This repairs the representation gap classified in A-022; `Term` and event
`Pat` stay scalar. Non-list compounds and improper lists are not represented:
an encounter remains a reported finding, never a coerced value or exclusion.
-/
inductive StipArg where
  | val (t : Term)
  | wild (id : Nat)
  | list (items : List StipArg)
  deriving Repr, Inhabited

-- Mutually structural recursive decisions compare the entire structure and
-- reduce in the kernel, with no normalization of the represented values.
mutual
  private def stipArgDecEq : (a b : StipArg) → Decidable (a = b)
    | .val a, .val b =>
        match decEq a b with
        | isTrue h => isTrue (congrArg StipArg.val h)
        | isFalse h => isFalse (fun e => h (StipArg.val.inj e))
    | .wild a, .wild b =>
        match decEq a b with
        | isTrue h => isTrue (congrArg StipArg.wild h)
        | isFalse h => isFalse (fun e => h (StipArg.wild.inj e))
    | .list as, .list bs =>
        match stipArgsDecEq as bs with
        | isTrue h => isTrue (congrArg StipArg.list h)
        | isFalse h => isFalse (fun e => h (StipArg.list.inj e))
    | .val _, .wild _ | .val _, .list _
    | .wild _, .val _ | .wild _, .list _
    | .list _, .val _ | .list _, .wild _ => isFalse (by intro h; cases h)
  termination_by structural a => a

  private def stipArgsDecEq : (as bs : List StipArg) → Decidable (as = bs)
    | [], [] => isTrue rfl
    | [], _ :: _ | _ :: _, [] => isFalse (by intro h; cases h)
    | a :: as, b :: bs =>
        match stipArgDecEq a b with
        | isFalse h => isFalse (fun e => h (List.cons.inj e).1)
        | isTrue h =>
            match stipArgsDecEq as bs with
            | isFalse t => isFalse (fun e => t (List.cons.inj e).2)
            | isTrue t => isTrue (by cases h; cases t; rfl)
  termination_by structural as => as
end

instance : DecidableEq StipArg := stipArgDecEq

/-- Lossless one-way inclusion of the old scalar pattern, preserving its id. -/
def StipArg.ofPat : Pat → StipArg
  | .val t => .val t
  | .wild id => .wild id

-- Keeps explicit legacy Pat arguments usable without widening Fact.purpose_.
-- There is deliberately no reverse coercion from StipArg to Pat or Term.
instance : Coe Pat StipArg := ⟨StipArg.ofPat⟩

/--
H4.1. The 31 statute signatures that case files supply clauses for. A case
clause whose head is a statute predicate adds a clause *after* the statute's
own, so the predicate's solution list is `statute solutions ++ stipulated
solutions`. 156 of the 376 original cases carry stipulations (203 fact clauses,
28 rule clauses).
-/
inductive StipPred where

  /-- `s63/3` — 60 fact clause(s), 0 rule clause(s) -/
  | s63_3
  /-- `s7703/4` — 26 fact clause(s), 0 rule clause(s) -/
  | s7703_4
  /-- `s3306_b/8` — 20 fact clause(s), 0 rule clause(s) -/
  | s3306_b_8
  /-- `s2_b/3` — 19 fact clause(s), 0 rule clause(s) -/
  | s2_b_3
  /-- `s2_a/3` — 19 fact clause(s), 0 rule clause(s) -/
  | s2_a_3
  /-- `s151_c_applies/3` — 1 fact clause(s), 14 rule clause(s) -/
  | s151_c_applies_3
  /-- `s152_c_1/3` — 8 fact clause(s), 0 rule clause(s) -/
  | s152_c_1_3
  /-- `s3306_c/5` — 0 fact clause(s), 8 rule clause(s) -/
  | s3306_c_5
  /-- `s151/5` — 5 fact clause(s), 1 rule clause(s) -/
  | s151_5
  /-- `s151_d/4` — 5 fact clause(s), 0 rule clause(s) -/
  | s151_d_4
  /-- `s151_b_applies/3` — 5 fact clause(s), 0 rule clause(s) -/
  | s151_b_applies_3
  /-- `s151_c/4` — 4 fact clause(s), 0 rule clause(s) -/
  | s151_c_4
  /-- `s151_b_applies/2` — 4 fact clause(s), 0 rule clause(s) -/
  | s151_b_applies_2
  /-- `total_wages_employer/6` — 4 fact clause(s), 0 rule clause(s) -/
  | total_wages_employer_6
  /-- `s68_b/3` — 2 fact clause(s), 0 rule clause(s) -/
  | s68_b_3
  /-- `s152_c_2/4` — 2 fact clause(s), 0 rule clause(s) -/
  | s152_c_2_4
  /-- `s152_c/3` — 1 fact clause(s), 1 rule clause(s) -/
  | s152_c_3
  /-- `s152_b_2/4` — 2 fact clause(s), 0 rule clause(s) -/
  | s152_b_2_4
  /-- `s3306_a/2` — 0 fact clause(s), 2 rule clause(s) -/
  | s3306_a_2
  /-- `s63_c_1/3` — 2 fact clause(s), 0 rule clause(s) -/
  | s63_c_1_3
  /-- `s63_c_2/3` — 2 fact clause(s), 0 rule clause(s) -/
  | s63_c_2_3
  /-- `s63_c_3/3` — 2 fact clause(s), 0 rule clause(s) -/
  | s63_c_3_3
  /-- `s63_f_1_A/2` — 2 fact clause(s), 0 rule clause(s) -/
  | s63_f_1_A_2
  /-- `s63_f_1_B/3` — 2 fact clause(s), 0 rule clause(s) -/
  | s63_f_1_B_3
  /-- `s63_d/4` — 2 fact clause(s), 0 rule clause(s) -/
  | s63_d_4
  /-- `s152_c_3/3` — 0 fact clause(s), 1 rule clause(s) -/
  | s152_c_3_3
  /-- `s2_a/5` — 1 fact clause(s), 0 rule clause(s) -/
  | s2_a_5
  /-- `s152_d_2_H/6` — 0 fact clause(s), 1 rule clause(s) -/
  | s152_d_2_H_6
  /-- `s63_c/3` — 1 fact clause(s), 0 rule clause(s) -/
  | s63_c_3
  /-- `s63_c_3/4` — 1 fact clause(s), 0 rule clause(s) -/
  | s63_c_3_4
  /-- `s151_b/3` — 1 fact clause(s), 0 rule clause(s) -/
  | s151_b_3
  deriving DecidableEq, Repr, Inhabited

/-- H4.1. The arity of each stipulated signature. -/
def StipPred.arity : StipPred → Nat

  | .s63_3 => 3
  | .s7703_4 => 4
  | .s3306_b_8 => 8
  | .s2_b_3 => 3
  | .s2_a_3 => 3
  | .s151_c_applies_3 => 3
  | .s152_c_1_3 => 3
  | .s3306_c_5 => 5
  | .s151_5 => 5
  | .s151_d_4 => 4
  | .s151_b_applies_3 => 3
  | .s151_c_4 => 4
  | .s151_b_applies_2 => 2
  | .total_wages_employer_6 => 6
  | .s68_b_3 => 3
  | .s152_c_2_4 => 4
  | .s152_c_3 => 3
  | .s152_b_2_4 => 4
  | .s3306_a_2 => 2
  | .s63_c_1_3 => 3
  | .s63_c_2_3 => 3
  | .s63_c_3_3 => 3
  | .s63_f_1_A_2 => 2
  | .s63_f_1_B_3 => 3
  | .s63_d_4 => 4
  | .s152_c_3_3 => 3
  | .s2_a_5 => 5
  | .s152_d_2_H_6 => 6
  | .s63_c_3 => 3
  | .s63_c_3_4 => 4
  | .s151_b_3 => 3


/--
H4.1. One stipulated clause, already grounded: a statute signature and one
pattern per argument position. Wildcard positions match anything and produce an
unbound output (A3).
-/
structure Stip where
  pred : StipPred
  args : List StipArg
  deriving DecidableEq, Repr, Inhabited

/-- A stipulation is well-formed when it supplies exactly one pattern per argument. -/
def Stip.wellFormed (s : Stip) : Bool := s.args.length == s.pred.arity

/-! ## The household (H1) -/

/--
H1. The shared input. `facts` is in source order after grounding (H4.2), with
duplicates kept; nothing is keyed, deduplicated, sorted or defaulted. An absent
fact is simply absent (G5, closed world). `stipulations` is empty for every
generated input (V1) and non-empty for 156 of the 376 originals.
-/
structure Household where
  facts        : List Fact
  stipulations : List Stip
  deriving DecidableEq, Repr, Inhabited

/-! ## Structural projections -/

/-- Every `Term` occurring in a fact. -/
def Fact.terms : Fact → List Term

  | .agent_ e v => [e, v]
  | .agricultural_service a1 a2 a3 => [a1, a2, a3]
  | .alice_employer a1 a2 a3 => [a1, a2, a3]
  | .alice_household_maintenance a1 a2 a3 a4 => [a1, a2, a3, a4]
  | .american_employer_ e => [e]
  | .amount_ e _ => [e]
  | .attending_classes_ e => [e]
  | .beneficiary_ e v => [e, v]
  | .birth_ e => [e]
  | .blindness_ e => [e]
  | .brother_ e => [e]
  | .business_ e => [e]
  | .business_trust_ e => [e]
  | .citizenship_ e => [e]
  | .country_ e v => [e, v]
  | .daughter_ e => [e]
  | .death_ e => [e]
  | .deduction_ e => [e]
  | .destination_ e v => [e, v]
  | .disability_ e => [e]
  | .educational_institution_ e => [e]
  | .end_ e _ => [e]
  | .enrollment_ e => [e]
  | .father_ e => [e]
  | .hospital_ e => [e]
  | .incarceration_ e => [e]
  | .income_ e => [e]
  | .international_organization_ e => [e]
  | .itemize_deductions_ e => [e]
  | .joint_return_ e => [e]
  | .legal_separation_ e => [e]
  | .location_ e v => [e, v]
  | .marriage_ e => [e]
  | .means_ e v => [e, v]
  | .medical_institution_ e => [e]
  | .medical_patient_ e => [e]
  | .migration_ e => [e]
  | .mother_ e => [e]
  | .nonresident_alien_ e => [e]
  | .nurses_training_school_ e => [e]
  | .patient e v => [e, v]
  | .patient_ e v => [e, v]
  | .payment_ e => [e]
  | .penal_institution_ e => [e]
  | .plan_ e => [e]
  | .purpose_ (.val t) v => [t, v]
  | .purpose_ (.wild _) v => [v]
  | .reason_ e v => [e, v]
  | .residence_ e => [e]
  | .retirement_ e => [e]
  | .service_ e => [e]
  | .sibling_ e => [e]
  | .sister_ e => [e]
  | .son_ e => [e]
  | .start_ e _ => [e]
  | .termination_ e => [e]
  | .type_ e v => [e, v]
  | .unemployment_compensation_agreement_ e => [e]


/-- The dollar amounts a fact carries (`amount_` only, H2/M1). -/
def Fact.amounts : Fact → List Int

  | .amount_ _ v => [v]
  | _ => []


/-- The days a fact carries (`start_`/`end_` only, H2/D1). -/
def Fact.days : Fact → List Day

  | .end_ _ d => [d]
  | .start_ _ d => [d]
  | _ => []


/-- True when the fact carries a wildcard. Only `purpose_` position 1 can (H2). -/
def Fact.hasWildcard : Fact → Bool

  | .purpose_ (.wild _) _ => true
  | _ => false


/--
True for the three case-local helper names, which exist only as rule heads.
H4.2 grounding emits unary and binary event facts only, so a grounded household
never contains one and `Valid` V1 rejects them in a generated input.
-/
def Fact.isCaseLocalHelper : Fact → Bool

  | .agricultural_service .. => true
  | .alice_employer .. => true
  | .alice_household_maintenance .. => true
  | _ => false
/-! ## Kinship (V4, V5) -/

/--
The parent edges H5 V4 names: `child → parent` for every `son_`/`daughter_`
event (agent → patient) and every `father_`/`mother_` event (patient → agent),
self-edges excluded.
-/
def Household.parentEdges (h : Household) : List (Term × Term) :=
  let agentsOf (e : Term) : List Term :=
    h.facts.filterMap fun f => match f with
      | .agent_ ev p => if ev == e then some p else none
      | _ => none
  let patientsOf (e : Term) : List Term :=
    h.facts.filterMap fun f => match f with
      | .patient_ ev p => if ev == e then some p else none
      | _ => none
  let childFirst : List Term :=
    h.facts.filterMap fun f => match f with
      | .son_ e => some e
      | .daughter_ e => some e
      | _ => none
  let parentFirst : List Term :=
    h.facts.filterMap fun f => match f with
      | .father_ e => some e
      | .mother_ e => some e
      | _ => none
  let fromChildFirst := childFirst.flatMap fun e =>
    (agentsOf e).flatMap fun c => (patientsOf e).map fun p => (c, p)
  let fromParentFirst := parentFirst.flatMap fun e =>
    (patientsOf e).flatMap fun c => (agentsOf e).map fun p => (c, p)
  (fromChildFirst ++ fromParentFirst).filter fun pr => pr.1 != pr.2

/--
Acyclicity by repeated leaf-peeling: drop every edge whose target has no
outgoing edge, and repeat. Structural recursion on explicit fuel, because
`docs/PLAN.md` section 2.4 has the gate reject `partial`.
-/
def acyclicAux : Nat → List (Term × Term) → Bool
  | 0,        es => es.isEmpty
  | fuel + 1, es =>
      let sources := es.map Prod.fst
      let kept := es.filter fun e => sources.contains e.2
      if kept.length == es.length then es.isEmpty else acyclicAux fuel kept

/-- True when the edge list has no directed cycle. -/
def acyclic (es : List (Term × Term)) : Bool := acyclicAux es.length es

/-- `is_child_of` restricted to the direct relation, as V5 uses it. -/
def Household.isChildOf (h : Household) (child parent : Term) : Bool :=
  h.parentEdges.contains (child, parent)

/-- Nonempty directed paths of at most `fuel` edges in the structural parent graph. -/
def parentReachableWithin (es : List (Term × Term)) : Nat → Term → Term → Bool
  | 0, _, _ => false
  | fuel + 1, child, ancestor =>
      es.any fun e =>
        e.1 == child && (e.2 == ancestor || parentReachableWithin es fuel e.2 ancestor)

/--
Option A's strict structural descendant test. Under V4 every path is simple,
so `parentEdges.length` bounds its length, including when facts repeat. The
bound is for this finite reachability check, not an R5 oracle fuel claim.
Self-pairs are rejected explicitly; neither facts nor repeated edges are changed.
-/
def Household.isStrictDescendantOf (h : Household) (descendant ancestor : Term) : Bool :=
  let es := h.parentEdges
  descendant != ancestor && parentReachableWithin es es.length descendant ancestor

/-! ## Birth structure (Option A, H5 V10) -/

/-- Birth-event markers in fact order, including repeated identical markers. -/
def Household.birthEvents (h : Household) : List Term :=
  h.facts.filterMap fun f => match f with
    | .birth_ e => some e
    | _ => none

/-- Every `(person, event)` birth/agent fact combination, with multiplicity kept. -/
def Household.births (h : Household) : List (Term × Term) :=
  h.birthEvents.flatMap fun e =>
    h.facts.filterMap fun f => match f with
      | .agent_ ev p => if ev == e then some (p, e) else none
      | _ => none

/-- All birth-event IDs of a person; equality of both persons and IDs is tag-sensitive. -/
def Household.birthEventsOf (h : Household) (person : Term) : List Term :=
  h.births.filterMap fun b => if b.1 == person then some b.2 else none

/-- Start-day facts of an event, in fact order with duplicates kept. -/
def Household.startDays (h : Household) (event : Term) : List Day :=
  h.facts.filterMap fun f => match f with
    | .start_ e d => if e == event then some d else none
    | _ => none

/-- A birth is present even when it has no `start_` fact (G5, N-CONJ at 152:207). -/
def Household.hasBirth (h : Household) (person : Term) : Bool :=
  !(h.birthEventsOf person).isEmpty

/--
Option A's unconditional uniqueness restrictions: at most one distinct birth
event per person, and at most one distinct start day per birth event, even if
the event has no agent. Repeated identical facts remain allowed and untouched.
Non-birth events retain their unrestricted start-day multiplicity.
-/
def Household.birthUnique (h : Household) : Bool :=
  let births := h.births
  (births.all fun b => births.all fun b' => b.1 != b'.1 || b.2 == b'.2)
  && h.birthEvents.all fun e =>
    let days := h.startDays e
    days.all fun d => days.all fun d' => d == d'

/--
A known unique DOB, requiring both a unique birth-event ID and a unique start
day. Absence, an undated birth and conflicting facts all yield `none`; callers
must use `hasBirth` separately to distinguish absence from an undated birth.
-/
def Household.uniqueDOB (h : Household) (person : Term) : Option Day :=
  match h.birthEventsOf person with
  | [] => none
  | e :: es =>
      if es.all (fun e' => e' == e) then
        match h.startDays e with
        | [] => none
        | d :: ds => if ds.all (fun d' => d' == d) then some d else none
      else none

/--
Option A's decrease condition for an eligible `(taxpayer, dependent)` pair.
A dependent with any birth must have a known unique DOB strictly later than
the taxpayer's known unique DOB. Only a dependent with no birth may instead
use strict structural descent. Equal-DOB eligible dependent pairs are excluded
as an approved domain limitation; unrelated equal birthdays remain allowed.
-/
def Household.r5Decreases (h : Household) (taxpayer dependent : Term) : Bool :=
  if h.hasBirth dependent then
    match h.uniqueDOB taxpayer, h.uniqueDOB dependent with
    | some tDOB, some dDOB => tDOB < dDOB
    | _, _ => false
  else h.isStrictDescendantOf dependent taxpayer

/-! ## Valid (H5) -/

/--
H5 V7/V8 and Option A's V10 eligibility depend on the oracle's definitions.
The oracle lane must supply their production implementations separately.

The class is deliberately *not* given a default instance. An `Oracle/`-free
build of `Interface/` therefore cannot silently assume the guards hold.
-/
class OracleGuards where
  /-- V7. The `P ⇒ P'` relation over domestic-service payments is acyclic. -/
  domesticAcyclic : Household → Bool
  /-- V8. `¬ hohCycle h t y` for every person `t`. -/
  noHohCycle      : Household → Year → Bool
  /--
  V10. Required nonrecursive decision procedure, with this EXACT contract:

    r5AllEligibleDecrease h y = true ↔
      ∀ ground t d, (original_s152_c_2 h d t has some solution ∧
                    original_s152_c_3 h d t y has some solution) →
                   h.r5Decreases t d = true.

  Both people are bound in the original calls. Include all applicable facts and
  stipulations, including wildcard person patterns; a finite ground-pair list
  cannot represent all such cases. Do not restrict persons to household literals
  or prefilter a violating edge. Prove BOTH directions: returning false merely
  because search/proof ran out would silently narrow the approved domain.

  Required at every `r5Years` year, for Valid and ValidStip. No default instance
  exists. This Bool-only interface prevents omission, not an unfaithful provider:
  the equivalence above is a recorded production proof obligation. Test mocks
  are not its implementation or certificate. The finite universe for the later
  R5 path measure needs its separate completeness proof.
  -/
  r5AllEligibleDecrease : Household → Year → Bool

/--
H5 V10 (approved Option A). Birth uniqueness always applies, even with no
eligible pairs. Check the universal rule in all 201 approved years, not merely
the outer `Valid h y` year. The exact nonrecursive decider is still required;
this interface conjunct alone establishes no R5/R8 termination theorem.
-/
def Household.v10 [OracleGuards] (h : Household) : Bool :=
  h.birthUnique && r5Years.all (OracleGuards.r5AllEligibleDecrease h)

/-- V3. `Day` bounds: 1900-01-01 … 2100-12-31, as days since 1970-01-01. -/
def dayLo : Day := -25567
/-- V3. Upper `Day` bound. -/
def dayHi : Day := 47846

/-- V3's shared day-bound check, including supplied query/stipulation days. -/
def Day.inRange (d : Day) : Bool := dayLo ≤ d && d ≤ dayHi

/--
D1. `YYYY-MM-DD` for a day count, by the standard civil-from-days algorithm,
with the four-digit zero-padded year the serializer is required to emit. Uses
`Int.fdiv` throughout because the algorithm needs floor division and Lean's `/`
on `Int` truncates toward zero.
-/
def Day.toISO (z : Day) : String :=
  let z := z + 719468
  let era := (if z ≥ 0 then z else z - 146096).fdiv 146097
  let doe := z - era * 146097
  let yoe := (doe - doe.fdiv 1460 + doe.fdiv 36524 - doe.fdiv 146096).fdiv 365
  let y := yoe + era * 400
  let doy := doe - (365 * yoe + yoe.fdiv 4 - yoe.fdiv 100)
  let mp := (5 * doy + 2).fdiv 153
  let d := doy - (153 * mp + 2).fdiv 5 + 1
  let m := mp + (if mp < 10 then 3 else -9)
  let y := y + (if m ≤ 2 then 1 else 0)
  let pad (n : Int) (width : Nat) : String :=
    let s := toString n.natAbs
    let s := "".pushn '0' (width - s.length) ++ s
    if n < 0 then "-" ++ s else s
  pad y 4 ++ "-" ++ pad m 2 ++ "-" ++ pad d 2

-- Split on the ASCII date separator without the core String reduction path.
private def splitDateParts : List Char → List Char → List (List Char)
  | [], acc => [acc.reverse]
  | c :: cs, acc =>
      if c == '-' then acc.reverse :: splitDateParts cs []
      else splitDateParts cs (c :: acc)

-- Structural recursion keeps literal date checks kernel-reducible. Only
-- unsigned ASCII digits can occur in a canonical, in-range ISO date; the
-- unchanged final round-trip check still rejects noncanonical widths.
private def dateDigits? (cs : List Char) : Option Int := do
  if cs.isEmpty then none else
    let n ← cs.foldl (init := some 0) fun acc c => do
      let n ← acc
      if '0' ≤ c && c ≤ '9' then some (n * 10 + (c.toNat - '0'.toNat)) else none
    some (Int.ofNat n)

/--
D1/V3/V9: decode a canonical, in-range ISO day without normalizing malformed
or overflow dates. The inverse civil algorithm is checked by re-encoding;
e.g. 1900-02-29, 2017-02-30 and 2017-1-1 are rejected, not repaired. This
parser validates the spelling only; it does not change a stipulated Term tag.
-/
def Day.fromISO? (s : String) : Option Day := do
  let [ys, ms, ds] := splitDateParts s.toList [] | none
  let y ← dateDigits? ys
  let m ← dateDigits? ms
  let d ← dateDigits? ds
  if !(1900 ≤ y && y ≤ 2100 && 1 ≤ m && m ≤ 12 && 1 ≤ d && d ≤ 31) then
    none
  else
    let y := y - (if m ≤ 2 then 1 else 0)
    let era := y.fdiv 400
    let yoe := y - era * 400
    let mp := m + (if m > 2 then -3 else 9)
    let doy := (153 * mp + 2).fdiv 5 + d - 1
    let doe := yoe * 365 + yoe.fdiv 4 - yoe.fdiv 100 + doy
    let day := era * 146097 + doe - 719468
    if Day.inRange day && Day.toISO day == s then some day else none

/-- Time roles only; `term` does not replace H2/G4's other kind constraints. -/
inductive TimeRole where
  | term | day | days | year | yearText
  deriving DecidableEq, BEq, Repr

/--
Check a Day-typed supplied position without changing its tag, spelling or
wildcard identity. A wildcard introduces no date; its actual bound caller value
must still be checked. An integer here is a malformed date under D2, not a day
count to coerce, and fails V3. Missing positions fail the separate shape check.
-/
def Pat.dayWellFormed : Pat → Bool
  | .wild _ => true
  | .val (.atom s) | .val (.str s) => (Day.fromISO? s).isSome
  | .val (.int _) => false

/--
The existing scalar Day check for a stipulated position. A proper list is not
a scalar Day, even if empty or containing a date. Other positions are still
governed solely by the existing signature/time checks, not recursively scanned
for date-looking values. No list-valued Day slot occurs in the H4.1 registry.
-/
def StipArg.dayWellFormed : StipArg → Bool
  | .val t => (Pat.val t).dayWellFormed
  | .wild id => (Pat.wild id).dayWellFormed
  | .list _ => false

-- BEGIN GENERATED STIPULATION TIME ROLES
-- Generated from Interface/TIME_SCHEMA.json; scripts/check_time_schema.py
-- verifies this table without loading either implementation lane.
def StipPred.timeRoles : StipPred → List TimeRole
  | .s63_3 => [.term, .year, .term]
  | .s7703_4 => [.term, .term, .term, .year]
  | .s3306_b_8 => [.term, .term, .term, .term, .term, .term, .term, .term]
  | .s2_b_3 => [.term, .term, .year]
  | .s2_a_3 => [.term, .term, .year]
  | .s151_c_applies_3 => [.term, .term, .year]
  | .s152_c_1_3 => [.term, .term, .year]
  | .s3306_c_5 => [.term, .term, .term, .day, .year]
  | .s151_5 => [.term, .term, .term, .term, .year]
  | .s151_d_4 => [.term, .term, .term, .term]
  | .s151_b_applies_3 => [.term, .term, .year]
  | .s151_c_4 => [.term, .term, .term, .year]
  | .s151_b_applies_2 => [.term, .year]
  | .total_wages_employer_6 => [.term, .term, .term, .term, .day, .day]
  | .s68_b_3 => [.term, .term, .year]
  | .s152_c_2_4 => [.term, .term, .day, .day]
  | .s152_c_3 => [.term, .term, .year]
  | .s152_b_2_4 => [.term, .term, .term, .year]
  | .s3306_a_2 => [.term, .year]
  | .s63_c_1_3 => [.term, .year, .term]
  | .s63_c_2_3 => [.term, .year, .term]
  | .s63_c_3_3 => [.term, .term, .year]
  | .s63_f_1_A_2 => [.term, .year]
  | .s63_f_1_B_3 => [.term, .term, .year]
  | .s63_d_4 => [.term, .term, .term, .year]
  | .s152_c_3_3 => [.term, .term, .year]
  | .s2_a_5 => [.term, .term, .term, .term, .term]
  | .s152_d_2_H_6 => [.term, .term, .year, .term, .day, .day]
  | .s63_c_3 => [.term, .year, .term]
  | .s63_c_3_4 => [.term, .term, .term, .term]
  | .s151_b_3 => [.term, .term, .year]
-- END GENERATED STIPULATION TIME ROLES

/--
V3 reaches supplied Day positions through the shared signature schema. Years
in a stipulated head are *not* all operational years: a bound caller may never
unify with a literal (the preserved s68_b(...,250000) originals). Check actual
query/call years at the query boundary instead of rejecting inert head literals.
The three corpus-only extra arities have no canonical time-role declaration;
they remain opaque patterns, not invented date/year modes. See TIME_SCHEMA.json.
-/
def Stip.daysWellFormed (s : Stip) : Bool :=
  s.wellFormed && (s.pred.timeRoles.zip s.args).all (fun (role, arg) =>
    match role with
    | .day => arg.dayWellFormed
    | .days => false -- no H4.1 signature supplies a list-valued Day position
    | .term | .year | .yearText => true)

/--
H5 V1. Well-formed: the argument kinds of H2 are enforced by `Fact`'s own types,
so what remains is no wildcard, no stipulation, no case-local helper, and no
empty string.
-/
def Household.v1 (h : Household) : Bool :=
  h.stipulations.isEmpty
  && h.facts.all (fun f => !f.hasWildcard && !f.isCaseLocalHelper)
  && h.facts.all (fun f => f.terms.all fun t => match t with
       | .atom s => s != "" | .str s => s != "" | .int _ => true)

/-- H5 V2. Every `amount_` value lies in `0 … 10^9`. -/
def Household.v2 (h : Household) : Bool :=
  h.facts.all fun f => f.amounts.all fun v => 0 ≤ v && v ≤ 1000000000

/--
H5 V3. Fact and stipulated days lie in 1900-01-01 … 2100-12-31 and the year
index in 1900 … 2100. Query arguments are not part of Household: every entry
wrapper additionally requires the tuple-indexed admission in QueryTime.lean.
Valid/ValidStip alone never certify a query or an internal call's actual time.
-/
def Household.v3 (h : Household) (y : Year) : Bool :=
  (1900 ≤ y && y ≤ 2100)
  && h.facts.all (fun f => f.days.all Day.inRange)
  && h.stipulations.all Stip.daysWellFormed

/-- H5 V4. The kinship graph is acyclic. -/
def Household.v4 (h : Household) : Bool := acyclic h.parentEdges

/--
H5 V5 (E1, `s3306_c_5_B`). No `service_` event whose agent is a child of its
patient and who has a `birth_` event carrying a `start_` fact. That clause
computes `Dob_d + 7671` on a string and raises, so such inputs are
reference-undefined (G6).
-/
def Household.v5 (h : Household) : Bool :=
  let services := h.facts.filterMap fun f => match f with
    | .service_ e => some e | _ => none
  let agentsOf (e : Term) := h.facts.filterMap fun f => match f with
    | .agent_ ev p => if ev == e then some p else none | _ => none
  let patientsOf (e : Term) := h.facts.filterMap fun f => match f with
    | .patient_ ev p => if ev == e then some p else none | _ => none
  let births := h.facts.filterMap fun f => match f with
    | .birth_ e => some e | _ => none
  let hasDatedBirth (person : Term) : Bool :=
    births.any fun b =>
      (agentsOf b).contains person
      && h.facts.any fun f => match f with
           | .start_ ev _ => ev == b | _ => false
  services.all fun s =>
    (agentsOf s).all fun e =>
      (patientsOf s).all fun p =>
        !(h.isChildOf e p && hasDatedBirth e)

/-- H5 V6 (E2, `s3306_b_2`). Every `plan_` event has at most one distinct `beneficiary_`. -/
def Household.v6 (h : Household) : Bool :=
  let plans := h.facts.filterMap fun f => match f with
    | .plan_ e => some e | _ => none
  plans.all fun pl =>
    let bens := h.facts.filterMap fun f => match f with
      | .beneficiary_ ev b => if ev == pl then some b else none
      | _ => none
    bens.all fun b => bens.all fun b' => b == b'

/--
H5. `Valid : Household → Year → Prop`, decidable. The year index is required
because V8 depends on the taxable year (P-VALID-YEAR); this is the premise of
every invariant and of PROVED-EQUIV, and it refines `docs/PROTOCOL.md` B004's
statement form from `∀ h y, Valid h → …` to `∀ h y, Valid h y → …`.

V9 (dates well-formed for the interpreter) is implied by D1 and V3 and is listed
in the decisions only to make the serializer's obligation explicit.
-/
def Valid [OracleGuards] (h : Household) (y : Year) : Prop :=
  h.v1 && h.v2 && h.v3 y && h.v4 && h.v5 && h.v6 && h.v10
  && OracleGuards.domesticAcyclic h && OracleGuards.noHohCycle h y

instance [OracleGuards] (h : Household) (y : Year) : Decidable (Valid h y) := by
  unfold Valid; infer_instance

/--
H5. `ValidStip` is `Valid` without V1: stipulations and the two original
`purpose_` wildcards are allowed. The 376 original cases are compared under this
for Week 1 parity only; generated inputs must satisfy the full `Valid`.
Option A's V10, including unconditional birth uniqueness, applies to both.
-/
def ValidStip [OracleGuards] (h : Household) (y : Year) : Prop :=
  h.v2 && h.v3 y && h.v4 && h.v5 && h.v6 && h.v10
  && h.stipulations.all Stip.wellFormed
  && OracleGuards.domesticAcyclic h && OracleGuards.noHohCycle h y

instance [OracleGuards] (h : Household) (y : Year) : Decidable (ValidStip h y) := by
  unfold ValidStip; infer_instance

/-! ## Canonical observation (H6.2) -/

/--
H6.2. The wire form of one observed value. Both engines map `Int` to a number,
`atom s` to `{"a": s}`, `str s` to `{"s": s}`, a `Day` to an ISO string and an
unbound position to `null`.
-/
inductive Obs where
  | null
  | num  (n : Int)
  | atom (s : String)
  | str  (s : String)
  | day  (d : Day)
  | arr  (xs : List Obs)
  deriving Repr, Inhabited

/-- One lowercase hexadecimal digit for a JSON `\u00XX` escape. -/
private def jsonHexDigit (n : Nat) : String :=
  (Char.ofNat (if n < 10 then 48 + n else 87 + n)).toString

/-- JSON string escaping for quotes, backslashes and every U+0000–U+001F control. -/
def escapeJson (s : String) : String :=
  s.foldl (init := "") fun acc c =>
    acc ++ match c.toNat with
      | 8  => "\\b"
      | 9  => "\\t"
      | 10 => "\\n"
      | 12 => "\\f"
      | 13 => "\\r"
      | 34 => "\\\""
      | 92 => "\\\\"
      | n  =>
        if n < 32 then
          "\\u00" ++ jsonHexDigit (n / 16) ++ jsonHexDigit (n % 16)
        else
          c.toString

/--
H6.2. Canonical JSON for one observed value. `DecidableEq` cannot be derived for
`Obs` because `arr` nests `List Obs`; canonicalising to a string is both what the
decision actually specifies — "both sides map each solution to JSON" — and what
gives the sort and the deduplication below a total order for free.
-/
def Obs.encode : Obs → String
  | .null    => "null"
  | .num n   => toString n
  | .atom s  => "{\"a\":\"" ++ escapeJson s ++ "\"}"
  | .str s   => "{\"s\":\"" ++ escapeJson s ++ "\"}"
  | .day d   => "\"" ++ Day.toISO d ++ "\""
  | .arr xs  => "[" ++ String.intercalate "," (xs.map Obs.encode) ++ "]"

/-- H6.2. A solution is a tuple of observed output positions. -/
abbrev Solution := List Obs

/-- H6.2. Canonical JSON for one solution tuple. -/
def Solution.encode (s : Solution) : String :=
  "[" ++ String.intercalate "," (s.map Obs.encode) ++ "]"

/--
H6.2. The observation of a target: the **sorted, deduplicated** array of its
solutions — a solution *set*, not a multiset. The case directives have
existential semantics, and exact multiplicity of duplicate solutions is not a
property a formalization should be graded on. Multiplicity still matters inside
the oracle wherever the source aggregates (A1); it is dropped only here, at the
boundary.

Scalar entry points do **not** use this: H6.1 observes their first solution
under G1 order.
-/
def observe (sols : List Solution) : List String :=
  let encoded := sols.map Solution.encode
  let sorted := encoded.mergeSort (fun a b => a ≤ b)
  sorted.foldr (init := []) fun x acc =>
    match acc with
    | []      => [x]
    | y :: _  => if x == y then acc else x :: acc

end KMLA
