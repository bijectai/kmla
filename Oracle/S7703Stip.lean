import Interface.QueryTime

/-!
§7703-only H4.1 head unification and invocation freshening. Shared Pat is the
only variable/value representation. Nat is an explicit next-unused-id supply,
not a new payload field, reference result, finite Term universe, or fuel.
Callers compose invocations by passing the returned supply; never reset it
while retaining live outputs. Stored Household ids are clause-local names:
transport leaves them unchanged; each invocation renames them consistently.
No general cross-section relational engine or recursive provider is supplied.
-/

namespace KMLA.Oracle.S7703.Stipulation

private def freshPat (next : Nat) (names : List (Nat × Nat)) (p : Pat) :
    Nat × List (Nat × Nat) × Pat :=
  match p with
  | .val t => (next, names, .val t)
  | .wild id =>
    match names.find? (fun pair => pair.1 == id) with
    | some (_, renamed) => (next, names, .wild renamed)
    | none => (next + 1, (id, next) :: names, .wild next)

/-- Freshen all four positions before trying head constraints, left to right.
Repeated source ids share a renamed id; each clause invocation starts names=[]. -/
private def freshHead (next : Nat) (a b c d : Pat) :
    Nat × Pat × Pat × Pat × Pat :=
  let (n1, names1, a') := freshPat next [] a
  let (n2, names2, b') := freshPat n1 names1 b
  let (n3, names3, c') := freshPat n2 names2 c
  let (n4, _, d') := freshPat n3 names3 d
  (n4, a', b', c', d')

/-- The two selected modes unify head variables only against ground inputs.
There are no compound terms/occurs-check cases in the shared Term domain. -/
private def bindGround (bindings : List (Nat × Term)) (p : Pat) (t : Term) :
    Option (List (Nat × Term)) :=
  match p with
  | .val v => if v == t then some bindings else none
  | .wild id =>
    match bindings.find? (fun pair => pair.1 == id) with
    | some (_, v) => if v == t then some bindings else none
    | none => some ((id, t) :: bindings)

private def resolve (bindings : List (Nat × Term)) (p : Pat) : Pat :=
  match p with
  | .val t => .val t
  | .wild id =>
    match bindings.find? (fun pair => pair.1 == id) with
    | some (_, t) => .val t
    | none => .wild id

/-- Head unification for bffb/bbfb. Free output positions do not constrain the
head, but bindings from ANY input position propagate to every shared variable.
In particular the last (Year) position may bind an earlier output. -/
private def matchHead (taxpayer : Term) (spouse : Option Term) (year : Year)
    (a b c d : Pat) : Option (Pat × Pat) := do
  let bindings ← bindGround [] a taxpayer
  let bindings ← match spouse with
    | none => some bindings
    | some t => bindGround bindings b t
  let bindings ← bindGround bindings d (.int year)
  pure (resolve bindings b, resolve bindings c)

/-- H4.1: one appended s7703/4 fact clause, with NO statute-only guard or NAF.
Other signatures are not clauses of this predicate. A well-formedness proof
prevents a malformed s7703 head from being silently dropped as logical failure.
No clause-local binding is carried into the next clause. -/
private def clause (taxpayer : Term) (spouse : Option Term) (year : Year)
    (next : Nat) (s : Stip) (shaped : s.wellFormed = true) :
    Nat × List (Pat × Pat) :=
  match hp : s.pred with
  | .s7703_4 =>
    have arity : s.args.length = 4 := by
      simpa [Stip.wellFormed, hp, StipPred.arity] using shaped
    let a := s.args[0]'(by omega)
    let b := s.args[1]'(by omega)
    let c := s.args[2]'(by omega)
    let d := s.args[3]'(by omega)
    let (next', a', b', c', d') := freshHead next a b c d
    (next', (matchHead taxpayer spouse year a' b' c' d').toList)
  | _ => (next, [])

/-- H4.1/G1: ordered stipulated clauses, including duplicates and inert heads.
Failed matching clauses still consume their allocated ids; failure is only a
head-unification failure, never a substitute for a missing provider or budget.
The first component is the next supply; the second is the ordered solution list.
Freshening here is evaluation, not a mutation of transported Household ids. -/
def solutions (taxpayer : Term) (spouse : Option Term) (year : Year)
    (next : Nat) (clauses : List Stip)
    (shaped : clauses.all Stip.wellFormed = true) : Nat × List (Pat × Pat) :=
  match clauses with
  | [] => (next, [])
  | s :: ss =>
    have good : s.wellFormed = true ∧ ss.all Stip.wellFormed = true := by
      simpa only [List.all_cons, Bool.and_eq_true] using shaped
    let (next', rows) := clause taxpayer spouse year next s good.1
    let (next'', remaining) := solutions taxpayer spouse year next' ss good.2
    (next'', rows ++ remaining)

/-- A subsequent ground constraint on Spouse updates BOTH output positions.
This is not a new query mode: it demonstrates/usefully preserves a shared
output variable through a later conjunct rather than observing it prematurely.
An inconsistent constraint is ordinary unification failure. -/
def bindSpouse (row : Pat × Pat) (spouse : Term) : Option (Pat × Pat) := do
  let bindings ← bindGround [] row.1 spouse
  pure (resolve bindings row.1, resolve bindings row.2)

/-- Existing admission implies head arity; no new validity rule or default. -/
theorem admitted_shape [OracleGuards] {lane : AdmissionLane} {h : Household}
    {year : Year} {q : QueryCall} (admitted : AdmittedQuery lane h year q) :
    h.stipulations.all Stip.wellFormed = true := by
  have valid := admitted.admissible.1
  cases lane <;> simp_all [Valid, ValidStip, Household.v1]

end KMLA.Oracle.S7703.Stipulation
