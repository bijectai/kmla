import Interface.QueryTime

/-!
§7703 slice against human/DECISIONS.md, G1–G9, H1–H6, D1–D9, N1–N5,
M3/M8 and A1/A2/A6. Source: statutes/prolog/section7703.pl.

Six nonrecursive clauses are executable below in their approved modes.
The seventh, (b)(1), is a clause BODY parameterized by the unavailable
s152_a_1/3 continuation. No provider, recursive knot, R5 bound, production
OracleGuards or full s7703 target is supplied. In particular s7703/4 (2–9)
and s7703_b/3 (103–106) remain untranslated, not false-valued stubs.

Definitions named *_clause1 and *_mode are internal, ordered solution lists.
Only *_entry wrappers are query entries; each consumes AdmittedQuery for the
exact typed tuple it evaluates. None constructs a validity or time default.
There are no explicit ! sites in this source; its three -> sites use head?.
No output is sorted/deduplicated before Interface.observe at the boundary.
-/

namespace KMLA.Oracle.S7703

/-! Section-local implementation helpers, not additional shared input types. -/

-- Core Lean does not install List's nondeterminism instances. These local
-- elaboration instances expand G1's do-notation to singleton/ordered flatMap.
local instance : Pure List where
  pure x := [x]

local instance : Bind List where
  bind xs f := xs.flatMap f

/-- One success or ordinary logical failure, never a fuel-exhaustion result. -/
def succeed (condition : Bool) : List Unit := if condition then [()] else []

/-- H1/G1: select exactly the marker facts, preserving their order and duplicates. -/
def markers (h : Household) (get : Fact → Option Term) : List Term :=
  h.facts.filterMap get

def agents (h : Household) (event : Term) : List Term :=
  h.facts.filterMap fun f => match f with
    | .agent_ e p => if e == event then some p else none
    | _ => none

def patients (h : Household) (event : Term) : List Term :=
  h.facts.filterMap fun f => match f with
    | .patient_ e p => if e == event then some p else none
    | _ => none

def ends (h : Household) (event : Term) : List Day :=
  h.facts.filterMap fun f => match f with
    | .end_ e d => if e == event then some d else none
    | _ => none

def amounts (h : Household) (event : Term) : List Int :=
  h.facts.filterMap fun f => match f with
    | .amount_ e n => if e == event then some n else none
    | _ => none

/-- H2: purpose_ position 1 is bound at these call sites; a wildcard matches it. -/
def purposes (h : Household) (event : Term) : List Term :=
  h.facts.filterMap fun f => match f with
    | .purpose_ (.val e) p => if e == event then some p else none
    | .purpose_ (.wild _) p => some p
    | _ => none

/--
D1/D5 arithmetic for January 1 (days-from-civil with month=1/day=1).
Unlike the input decoder this also computes the source's derived Jan 1, 2101.
It does not admit that derived constant as a root query or supplied Workday.
-/
def firstDay (year : Year) : Day :=
  let prior := year - 1
  let era := prior.fdiv 400
  let yoe := prior - era * 400
  era * 146097 + yoe * 365 + yoe.fdiv 4 - yoe.fdiv 100 + 306 - 719468

def lastDay (year : Year) : Day := firstDay (year + 1) - 1

/-- D8: the 184 actual formatted days are July 1 through December 31. -/
def julyFirst (year : Year) : Day := lastDay year - 183

/--
section7703.pl:17–82, sole s7703_a_1/5 clause, mode bfffb.
Result: (Spouse, Marriage, S13); S13 is unbound on the end-of-year branch.
No stipulated clauses exist for this signature in H4.1.
-/
def s7703_a_1_clause1 (h : Household) (taxpayer : Term) (year : Year) :
    List (Term × Term × Option Day) := do
  let first := firstDay year
  let last := lastDay year
  let next := firstDay (year + 1)
  let marriage ← markers h (fun f => match f with | .marriage_ e => some e | _ => none)
  let _ ← (agents h marriage).filter (· == taxpayer)
  let spouse ← agents h marriage
  let _ ← succeed (taxpayer != spouse)
  -- NAF section7703.pl:30:13 — N-ABS-DATE, N2; explicit Jan 1 default.
  let starts := h.startDays marriage
  let start ← if starts.isEmpty then [first] else starts
  let _ ← succeed (start ≤ last)
  let deathsInYear : List Day := do
    let death ← markers h (fun f => match f with | .death_ e => some e | _ => none)
    let _ ← (agents h death).filter (· == spouse)
    let day ← h.startDays death
    let _ ← succeed (first ≤ day && day ≤ last)
    pure day
  -- G1 commitment, section7703.pl:40–45: first SUCCESSFUL whole condition.
  -- Failure of its consequent does not try a later death or the else branch.
  match deathsInYear.head? with
  | some deathDay =>
    let _ ← succeed (start ≤ deathDay)
    -- NAF section7703.pl:50:6 — N-ABS-DATE, N2; disjunction retains ends.
    let witnesses := if (ends h marriage).isEmpty then [()] else do
      let endDay ← ends h marriage
      succeed (deathDay ≤ endDay)
    let _ ← witnesses
    pure (spouse, marriage, some deathDay)
  | none =>
    -- NAF section7703.pl:61:6 — N-ABS-DATE in ->, N2/G1.
    -- G1 commitment at 61–62: absence is a single deterministic success.
    if (ends h marriage).isEmpty then
      let deathEvents : List Term := do
        let death ← markers h (fun f => match f with | .death_ e => some e | _ => none)
        let _ ← (agents h death).filter (· == spouse)
        pure death
      -- G1 commitment, section7703.pl:65–67: choose the EVENT before its dates.
      match deathEvents.head? with
      | none => pure (spouse, marriage, none)
      | some death =>
        let endDay ← h.startDays death
        let _ ← succeed (next ≤ endDay)
        pure (spouse, marriage, none)
    else
      let endDay ← ends h marriage
      let _ ← succeed (next ≤ endDay)
      pure (spouse, marriage, none)

def s7703_a_1_bfffb := s7703_a_1_clause1

/-- section7703.pl:85–98, sole s7703_a_2/5 clause, mode bfffb.
Result: (Spouse, Marriage, S19). G4 decree strings are not atoms. -/
def s7703_a_2_clause1 (h : Household) (taxpayer : Term) (year : Year) :
    List (Term × Term × Term) := do
  let marriage ← markers h (fun f => match f with | .marriage_ e => some e | _ => none)
  let _ ← (agents h marriage).filter (· == taxpayer)
  let spouse ← agents h marriage
  let _ ← succeed (taxpayer != spouse)
  let separation ← markers h (fun f => match f with | .legal_separation_ e => some e | _ => none)
  let _ ← (patients h separation).filter (· == marriage)
  let _ ← ((agents h separation).filter (· == .str "decree of divorce")) ++
    ((agents h separation).filter (· == .str "decree of separate maintenance"))
  let divorceDay ← h.startDays separation
  let _ ← succeed (divorceDay ≤ lastDay year)
  pure (spouse, marriage, separation)

def s7703_a_2_bfffb := s7703_a_2_clause1

/-- section7703.pl:12–14, sole s7703_a/4 clause, mode bffb.
Result: (Spouse, Marriage). The bound a_2 positions are filtered per G2. -/
def s7703_a_clause1 (h : Household) (taxpayer : Term) (year : Year) :
    List (Term × Term) := do
  let (spouse, marriage, _) ← s7703_a_1_bfffb h taxpayer year
  -- NAF section7703.pl:14:2 — N-CALL, N1/N4; S19 stays existential.
  let _ ← succeed ((s7703_a_2_bfffb h taxpayer year).filter
    (fun (s, m, _) => s == spouse && m == marriage)).isEmpty
  pure (spouse, marriage)

def s7703_a_bffb := s7703_a_clause1

/--
section7703.pl:110–139, sole s7703_b_1/4 clause BODY, mode bffb.
Result: (Household, Dependent). s152_a_1 is called with both people bound.
The required continuation must eventually be the original ordered s152_a_1
solutions, including its downstream stipulations and the R5 recursive context.
No instance or default implements it here. The caller must pass the actual-year
certificate through to that continuation without resetting a descendant budget.
This parameterized composition is not a completed reference target.
-/
def s7703_b_1_clause1 (h : Household) (taxpayer : Term) (year : Year)
    (checked : CoveredR5Time (.year year))
    (s152_a_1_bbb : (dependent taxpayer : Term) → (year : Year) →
      CoveredR5Time (.year year) → List Unit) : List (Term × Term) := do
  let first := firstDay year
  let last := lastDay year
  -- NAF section7703.pl:113:2 — N-CONJ, N5; exact dates, any co-agent.
  let jointReturns : List Unit := do
    let joint ← markers h (fun f => match f with | .joint_return_ e => some e | _ => none)
    let _ ← (agents h joint).filter (· == taxpayer)
    let _ ← (h.startDays joint).filter (· == first)
    let _ ← (ends h joint).filter (· == last)
    pure ()
  let _ ← succeed jointReturns.isEmpty
  let residence ← markers h (fun f => match f with | .residence_ e => some e | _ => none)
  let _ ← (agents h residence).filter (· == taxpayer)
  let home ← patients h residence
  let childResidence ← markers h (fun f => match f with | .residence_ e => some e | _ => none)
  let dependent ← agents h childResidence
  let _ ← (patients h childResidence).filter (· == home)
  let startTime ← h.startDays childResidence
  let start := max startTime first -- D7: latest([Start_time, First_day_year]).
  -- NAF section7703.pl:129:13 — N-ABS-DATE, N2; D7 clamps absent end to Dec 31.
  let endTimes := ends h childResidence
  let endTime ← if endTimes.isEmpty then [none] else endTimes.map some
  let stop := match endTime with | none => last | some d => min d last
  -- D4, section7703.pl:135–138: endpoint difference; equality passes.
  let _ ← succeed (2 * (stop - start) ≥ last - first)
  let _ ← s152_a_1_bbb dependent taxpayer year checked
  pure (home, dependent)

def s7703_b_1_bffb := s7703_b_1_clause1

/-- section7703.pl:142–184, sole s7703_b_2/4 clause, mode bbfb.
Result: Cost. The two findall goals retain each literal's original ordering. -/
def s7703_b_2_clause1 (h : Household) (taxpayer home : Term) (year : Year) :
    List Int := do
  -- AGG section7703.pl:143:5 — A-EV/A1: all payment/residence/agent/etc. proofs.
  let individual : List Int := do
    let payment ← markers h (fun f => match f with | .payment_ e => some e | _ => none)
    let residence ← markers h (fun f => match f with | .residence_ e => some e | _ => none)
    let _ ← (agents h payment).filter (· == taxpayer)
    let _ ← (patients h residence).filter (· == home)
    let _ ← ((purposes h payment).filter (· == residence)) ++
      ((purposes h payment).filter (· == home))
    let amount ← amounts h payment
    let day ← h.startDays payment
    -- D5: on admitted canonical Days, year(start) = Taxy.
    let _ ← succeed (firstDay year ≤ day && day ≤ lastDay year)
    pure amount
  -- AGG section7703.pl:162:2 — A-EV/A1: same goal WITHOUT agent restriction.
  let allPayments : List Int := do
    let payment ← markers h (fun f => match f with | .payment_ e => some e | _ => none)
    let residence ← markers h (fun f => match f with | .residence_ e => some e | _ => none)
    let _ ← (patients h residence).filter (· == home)
    let _ ← ((purposes h payment).filter (· == residence)) ++
      ((purposes h payment).filter (· == home))
    let amount ← amounts h payment
    let day ← h.startDays payment
    let _ ← succeed (firstDay year ≤ day && day ≤ lastDay year)
    pure amount
  -- AGG section7703.pl:180:2 — A2/M8: Int sum, duplicates counted, [] sums to 0.
  let paid := individual.sum
  -- AGG section7703.pl:181:2 — A2/M8: all-payer Int sum.
  let cost := allPayments.sum
  let _ ← succeed (cost > 0)
  -- M3, section7703.pl:183–184: rdiv comparison, including exact one-half.
  let _ ← succeed (2 * paid ≥ cost)
  pure cost

def s7703_b_2_bbfb := s7703_b_2_clause1

/-- section7703.pl:187–201, sole membership clause, internal mode bbb.
One Unit per proof, including repeated agent/patient/start/end facts. -/
def s7703_b_3_is_member_of_household_clause1
    (h : Household) (spouse home : Term) (day : Day) : List Unit := do
  let residence ← markers h (fun f => match f with | .residence_ e => some e | _ => none)
  let _ ← (agents h residence).filter (· == spouse)
  let _ ← (patients h residence).filter (· == home)
  let start ← h.startDays residence
  let _ ← succeed (start ≤ day)
  -- NAF section7703.pl:195:4 — N-ABS-DATE, N2; end absence OR each end witness.
  if (ends h residence).isEmpty then pure () else do
    let stop ← ends h residence
    succeed (day ≤ stop)

def s7703_b_3_is_member_of_household_bbb := s7703_b_3_is_member_of_household_clause1

/-- section7703.pl:203–216, sole s7703_b_3/4 clause, mode bfbb.
Result: Spouse. Its s7703_a prefix does NOT call the recursive s7703 target. -/
def s7703_b_3_clause1 (h : Household) (taxpayer home : Term) (year : Year) :
    List Term := do
  let (spouse, _) ← s7703_a_bffb h taxpayer year
  -- AGG section7703.pl:205:5 — A-DAYS/A1/D8: offsets 2..185, with multiplicity.
  let membershipOffsets : List Nat := do
    let i ← List.range 184
    let day := julyFirst year + Int.ofNat i
    let _ ← s7703_b_3_is_member_of_household_bbb h spouse home day
    pure (i + 2)
  let _ ← succeed (membershipOffsets.length == 0) -- A6, source line 216.
  pure spouse

def s7703_b_3_bfbb := s7703_b_3_clause1

/-! Entry tuples use only the shared QueryCall, SuppliedArg, Pat and Term types.
The free positions below are exactly H6.5, not ground-only substitute modes.
No runtime dispatcher, decoder or additional payload shape is invented here. -/

def a1Query (taxpayer : Term) (year : Year) : QueryCall :=
  ⟨"s7703_a_1", [.single (.val taxpayer), .single (.wild 0),
    .single (.wild 1), .single (.wild 2), .single (.val (.int year))]⟩

def a2Query (taxpayer : Term) (year : Year) : QueryCall :=
  ⟨"s7703_a_2", [.single (.val taxpayer), .single (.wild 0),
    .single (.wild 1), .single (.wild 2), .single (.val (.int year))]⟩

def b1Query (taxpayer : Term) (year : Year) : QueryCall :=
  ⟨"s7703_b_1", [.single (.val taxpayer), .single (.wild 0),
    .single (.wild 1), .single (.val (.int year))]⟩

def b2Query (taxpayer home : Term) (year : Year) : QueryCall :=
  ⟨"s7703_b_2", [.single (.val taxpayer), .single (.val home),
    .single (.wild 0), .single (.val (.int year))]⟩

def b3Query (taxpayer home : Term) (year : Year) : QueryCall :=
  ⟨"s7703_b_3", [.single (.val taxpayer), .single (.wild 0),
    .single (.val home), .single (.val (.int year))]⟩

def s7703_a_1_entry [OracleGuards] (lane : AdmissionLane)
    (h : Household) (taxpayer : Term) (year : Year)
    (_admitted : AdmittedQuery lane h year (a1Query taxpayer year)) :=
  s7703_a_1_bfffb h taxpayer year

def s7703_a_2_entry [OracleGuards] (lane : AdmissionLane)
    (h : Household) (taxpayer : Term) (year : Year)
    (_admitted : AdmittedQuery lane h year (a2Query taxpayer year)) :=
  s7703_a_2_bfffb h taxpayer year

/-- Parameterized entry only: the production continuation/adequacy remain owed. -/
def s7703_b_1_entry [OracleGuards] (lane : AdmissionLane)
    (h : Household) (taxpayer : Term) (year : Year)
    (_admitted : AdmittedQuery lane h year (b1Query taxpayer year))
    (checked : CoveredR5Time (.year year))
    (s152_a_1_bbb : (dependent taxpayer : Term) → (year : Year) →
      CoveredR5Time (.year year) → List Unit) :=
  s7703_b_1_bffb h taxpayer year checked s152_a_1_bbb

def s7703_b_2_entry [OracleGuards] (lane : AdmissionLane)
    (h : Household) (taxpayer home : Term) (year : Year)
    (_admitted : AdmittedQuery lane h year (b2Query taxpayer home year)) :=
  s7703_b_2_bbfb h taxpayer home year

def s7703_b_3_entry [OracleGuards] (lane : AdmissionLane)
    (h : Household) (taxpayer home : Term) (year : Year)
    (_admitted : AdmittedQuery lane h year (b3Query taxpayer home year)) :=
  s7703_b_3_bfbb h taxpayer home year

/-- G4/H6.2 mapping only; the shared observer performs the eventual set operation. -/
def termObs : Term → Obs
  | .atom s => .atom s
  | .str s => .str s
  | .int n => .num n

def a1Solutions (rows : List (Term × Term × Option Day)) : List Solution :=
  rows.map fun (s, m, d) => [termObs s, termObs m, match d with
    | none => .null | some day => .day day]

def a2Solutions (rows : List (Term × Term × Term)) : List Solution :=
  rows.map fun (s, m, e) => [termObs s, termObs m, termObs e]

def b1Solutions (rows : List (Term × Term)) : List Solution :=
  rows.map fun (home, d) => [termObs home, termObs d]

def b2Solutions (rows : List Int) : List Solution := rows.map (fun cost => [.num cost])
def b3Solutions (rows : List Term) : List Solution := rows.map (fun s => [termObs s])

end KMLA.Oracle.S7703
