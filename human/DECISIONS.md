# Semantic decisions

Recorded 2026-09-21. This file is the specification the oracle translator and
the serializer read. Every interpreter claim in it was checked on the pinned
image `kmla-swipl:7.2.3` (SWI-Prolog 7.2.3, `linux/amd64`, driven through
stdin because the image ignores command-line arguments under emulation, with
`TZ` set explicitly, D8); the probe programs, their outputs and the case
sweeps are in `docs/consult/evidence/`; contract changes are logged in
`docs/DECISION_LOG.md`. Any translation decision not covered here is a
blocker, not a guess.

Fidelity rule: reproduce the SARA authors' results where the choice is ours
(time zone, case reader, observation); translate the statute code as written
where it diverges from its evident intent, and report the divergence (G9).

---

## Conventions

These rules are assumed by every table below. They are decisions, not
observations: they fix what "the oracle" means.

**G1 (predicates are ordered solution lists).** Every Prolog predicate `p/n`
becomes a Lean function from its input positions to `List` of tuples of its
output positions, listing the solutions in SLD order: clauses in file order;
body literals left to right; fact predicates in Household order; disjunction
left branch first; `(C -> T ; E)` commits to the *first* solution of `C`;
`\+ G` is `(solutionsOf G).isEmpty`; `!` per Cut. Multiplicity is kept
(F12). A predicate used only for its truth value is `!(sols).isEmpty`; a
predicate whose first solution is consumed (`->` guards, the cut sites) uses
`head?`.

**G2 (modes are fixed by call sites).** Input positions are those bound at
every call site in the statutes and case queries; output positions are the
rest. When a call site binds an output position, the solution list is filtered
by equality on that position. Predicates called in more than one mode get one
Lean function per mode, named `p_mode`, with the mode string recorded in the
section table (H6). Instantiation guards (`nonvar/1`, `var/1`) are resolved at
translation time by the mode; the both-unbound `s152` call is the empty list
(R3).

**G3 (`=`, `==`, `\==`).** `=` with one side unbound is a binding; with both
bound it is structural equality on `Term`. `==`/`\==` on bound terms is
structural identity. `\==` with one side unbound is *true* (site
`section151.pl:135`, `Taxp \== Otaxp` before `Otaxp` is bound) and is
translated as `true`.

**G4 (term domain).** `Term := atom String | str String | int Int`. Equality is
tag-sensitive: `atom "usa" ≠ str "usa"` (probed). Statute string literals
(`"usa"`, `"cash"`, `"private home"`, `"domestic service"`,
`"agricultural labor"`, `"united states government"`,
`"decree of divorce"`, `"decree of separate maintenance"`, the plan-purpose
phrases) only match `str`. `atom_prefix/2` and `sub_atom/5` work on both tags
(probed), so `s3306_c_7` and `s3306_c_11` test the text regardless of tag.
Standard-order comparison `@>` on two 4-digit year strings is lexicographic
and coincides with numeric order inside Valid's year range (D5).

**G5 (closed world).** A fact is true iff it occurs in the Household list.
Declared-but-absent predicates fail (probed: `itemize_deductions_/1`,
`unemployment_compensation_agreement_/1`).

**G6 (reference-undefined inputs).** An input on which the pinned interpreter
raises an exception or does not terminate has no reference value. Such inputs
are excluded by `Valid` (V-rules, the V-rules under Household). The harness must treat an
exception or timeout on a Valid input as a halt-and-report finding, never as a
mismatch to be reconciled by editing either side.

**G7 (order inside the oracle, sets outside).** The oracle's internal lists
must be correctly ordered because cuts and `->` consume first solutions
(C1, D8). The external observation of a target is canonicalised per H6.

**G9 (fidelity rule).** Reproduce the authors' results
where the choice is ours (time zone, reader, observation), and translate the
statute code as written where it diverges from its evident intent (F4, F10,
F11, F16, F17, F18), reporting the divergence. Grading the intended reading
would require a corrected Prolog copy as the parity reference and is a
separate contract change. See P-INTENT in the decision log.

**G8 (one Lean definition per clause).** Clause `p :- body` becomes
`def p_k … : List _ := do-notation/bind over the body`, and `p := p_1 ++ p_2 ++ …`
in clause order. The annotation `-- NAF`, `-- CUT`, `-- AGG` cites the site id
used in the tables below (`file:line:col`).

---

---

## Money

**M1 (representation) [CONTRACT].** Money is `Int` whole dollars, not cents.
Every input amount in the corpus is an integer dollar literal (348 `amount_/2`
facts, no decimal points); every output is produced by `round/1` or by integer
arithmetic on such values; no sub-dollar value is ever observable. Cents would
force the serializer to divide by 100 on the way to Prolog, force `Valid` to
require multiples of 100, and give models a unit that the reference program
never uses. Had I kept the plan's cents, the equivalent entry would be: all money
values are multiples of 100, the oracle divides by 100 before every formula
below and multiplies the rounded dollar result by 100, and `Interface/` states
that. Logged as P-MONEY.

**M2 (rounding).** SWI 7.2.3 `round/1` rounds half away from zero for both
floats and rationals (probed: `round(2.5)=3`, `round(-2.5)=-3`,
`round(3 rdiv 2)=2`, `round(-3 rdiv 2)=-2`, `round(0.5)=1`,
`round(1 rdiv 2)=1`). Define in Lean

```lean
/-- SWI-Prolog round/1: nearest integer, ties away from zero. -/
def roundHalfAway (q : Rat) : Int :=
  if q ≥ 0 then Int.floor (q + 1/2) else -Int.floor (-q + 1/2)
```

and evaluate every `round(...)` site on the exact rational value of its
argument. The 21 sites of the form `round(C + (X − K) · R)` (§1
brackets and `s3301`) are computed by SWI in binary floating point. They agree
with the exact rational result on the whole Valid range for these reasons:
(i) the exact value has denominator dividing 1000 (rates 0.15, 0.28, 0.31,
0.36, 0.396, 0.06; constants with at most two decimals), so it is either an
exact half-integer tie or at least 1/1000 away from one; (ii) the double
rounding error of the product and sum is below `|value| · 2^-50`, which is
below 1/1000 for values under 10^11, so non-ties round the same way; (iii) at
exact ties (which occur for 0.15, 0.31, 0.396 and 0.06 as half-integer
products, and for the half-dollar constants 35,928.50, 75,528.50, 2,767.50 and
10,082.50 as integer products; the quarter-dollar constants and 0.36 admit no
tie) the computed double lands on the tie or on its far side: for 0.15, 0.31,
0.36, 0.396 and 0.06 the relative error of the nearest double is below 2^-54,
so the product is exactly the tie value; for 0.28 the nearest double exceeds
the decimal, so with a non-negative excess `X − K` the computed sum is on or
above the tie and `round` moves it up, exactly as half-away-from-zero does;
(iv) a negative excess never reaches a formula, because every bracket clause
tests its range (`Taxinc =< …`, `… < Taxinc`) before the `is`. Empirical
check on the pinned interpreter (`evidence/probe6_*`): all 18 distinct
formulas (21 sites) for every integer 0 ≤ X ≤ 400,000, 200,000 exact-tie
inputs per tie-admitting rate, and 20,000 random inputs per formula up to
10^9, with zero in-bracket mismatches against `rdiv`-exact evaluation. The
same run shows why (iv) matters: `s1_d_ii`'s formula evaluated *below* its
bracket (X from 8,575 to 14,175 in steps of 25, 176 inputs) rounds one dollar
lower in floating point than exactly, because the negative product's error
pushes the sum just under the tie. Those evaluations are unreachable. The
Valid bound on money (V2) is what makes (ii) a theorem rather than a hope.

**M3 (`rdiv` sites).** `round(X rdiv 100)` (`section68.pl:33,39`),
`round((E·Ap) rdiv 100)` (`section151.pl:156`) and
`round(Amount_A rdiv 2)` (`section68.pl:60`) are exact rational divisions
followed by M2. `Ratio is P rdiv Cost, Ratio >= rational(0.5)`
(`section7703.pl:183-184`) is `2·P ≥ Cost` on integers (`Cost > 0` is checked
one line earlier; `rational(0.5)` is exactly `1 rdiv 2`, probed). `rdiv`
accepts integral floats by exact conversion (probed: `31536000.0 rdiv 2 =
15768000`), which is why the duration sites work at all; they are rewritten in
integer days by D4.

**M4 (`ceil` sites).** `ceil(Difference/1250)` and `ceil(Difference/2500)`
(`section151.pl:180,183`): `/` on integers returns an integer when exact and a
float otherwise (probed: `2500/1250 = 2`, `2501/1250 = 2.0008`), and `ceil`
of that float is the true ceiling for every `Difference` below 2^53/2500.
Translate as `(Difference + 1249) / 1250` and `(Difference + 2499) / 2500`
with integer floor division; `Difference ≥ 0` by the preceding `max`.
Verified against the interpreter for 0 ≤ D ≤ 3,000,000 and 20,000 random D
up to 10^9 (`evidence/probe6_*`).

**M5 (integer sites).** `+`, `-`, `*` by an integer literal, `min`, `max`,
and constants are `Int` operations; `max(·,0)` clamps at zero
(`section63.pl:10,22,33`, `section151.pl:157,165`). No implicit rounding.

**M6 (`s3301`).** `round(0.06*Wages)` is `roundHalfAway (3·Wages/50)`; ties
occur (Wages ≡ 25 mod 50) and are handled by M2 (probed: 1250 → 75, 2250 →
135, 33200 → 1992, 7000 → 420).

**M7 (worked examples, all probed on the pinned interpreter).**

| Site | Input | Exact value | Result |
| --- | --- | --- | --- |
| `s1_a_i` | Taxinc 36900 | 5535.0 | 5535 |
| `s1_a_i` | Taxinc 10 | 1.5 (tie) | 2 |
| `s1_a_iii` | Taxinc 89200 | 20165 + 15.5 (tie) | 20181 (`round(50*0.31)=16`) |
| `s1_a_iv` | Taxinc 140050 | 35928.50 + 18 = 35946.5 (tie) | 35947 |
| `s1_a_v` | Taxinc 250125 | 75528.50 + 49.5 = 75578.0 | 75578 |
| `s151_d_3_A` | E 2000, Ap 33 | 660 | 660 |
| `s151_d_3_B` | Difference 2501, separate | 2·⌈2.0008⌉ | 6 → Ap 6 |
| `amount("D")` | 300000/2 | 150000 | 150000 |
| `s68_a_1` | Agi−Aa 33334 | 1000.02 | 1000 |
| `s7703_b_2` | P 1, Cost 2 | 1/2 ≥ 1/2 | true; P 1, Cost 3 → false |
| `s3301` | Wages 33200 | 1992.0 | 1992 |

**M8 (sums).** `sum_list/2` over an `Int` list is `List.sum`; the empty list
sums to 0 (probed). Lists never contain floats inside Valid (V2).

**M9 (`gross_income`).** `gross_income(Person,Year,G)` is the sum of every
`income_` amount of `Person` and every `payment_` amount received by `Person`
dated inside the year (A-EV sites), plus the spouse's same sum when a
year-long joint return exists (first `s7703` spouse, N-CONJ at
`utils.pl:289`). A call with `G` bound (`gross_income(Spouse,Taxy,0)`,
`section151.pl:82`) is an equality test on the computed value; `Gross_income
== 0` (`section152.pl:269`) is identity on `Int`, which is why V2 forbids
floats (`5.0 == 5` is false in SWI, probed).

**M10 (`is` inventory).** All 101 `is/2` sites with the rule that governs
each:

| Site | Predicate | Expression | Decision |
| --- | --- | --- | --- |
| `section1.pl:70:9` | `s1_a_i/2` | `Tax is round(Taxinc*0.15)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:75:9` | `s1_a_ii/2` | `Tax is round(5535+(Taxinc-36900)*0.28)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:80:9` | `s1_a_iii/2` | `Tax is round(20165+(Taxinc-89150)*0.31)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:85:9` | `s1_a_iv/2` | `Tax is round(35928.50+(Taxinc-140000)*0.36)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:89:9` | `s1_a_v/2` | `Tax is round(75528.50+(Taxinc-250000)*0.396)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:108:9` | `s1_b_i/2` | `Tax is round(Taxinc*0.15)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:113:9` | `s1_b_ii/2` | `Tax is round(4440+(Taxinc-29600)*0.28)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:118:9` | `s1_b_iii/2` | `Tax is round(17544+(Taxinc-76400)*0.31)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:123:9` | `s1_b_iv/2` | `Tax is round(33385+(Taxinc-127500)*0.36)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:127:9` | `s1_b_v/2` | `Tax is round(77485+(Taxinc-250000)*0.396)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:148:9` | `s1_c_i/2` | `Tax is round(Taxinc*0.15)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:153:9` | `s1_c_ii/2` | `Tax is round(3315+(Taxinc-22100)*0.28)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:158:9` | `s1_c_iii/2` | `Tax is round(12107+(Taxinc-53500)*0.31)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:163:9` | `s1_c_iv/2` | `Tax is round(31172+(Taxinc-115000)*0.36)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:167:9` | `s1_c_v/2` | `Tax is round(79772+(Taxinc-250000)*0.396)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:195:9` | `s1_d_i/2` | `Tax is round(Taxinc*0.15)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:200:9` | `s1_d_ii/2` | `Tax is round(2767.50+(Taxinc-18450)*0.28)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:205:9` | `s1_d_iii/2` | `Tax is round(10082.50+(Taxinc-44575)*0.31)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:210:9` | `s1_d_iv/2` | `Tax is round(17964.25+(Taxinc-70000)*0.36)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section1.pl:214:9` | `s1_d_v/2` | `Tax is round(37764.25+(Taxinc-125000)*0.396)` | M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7. |
| `section151.pl:15:16` | `s151/5` | `S2 is Total_ex_taxpayer+Total_ex_spouse` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section151.pl:129:8` | `s151_d_1/1` | `Ea is 2000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section151.pl:140:8` | `s151_d_2/4` | `Ea is 0` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section151.pl:156:22` | `s151_d_3_A/7` | `Reduction_amount is round( (Exemption_amount_in*Ap) rdiv 100)` | M3. `roundHalfAway (X / 100)` with exact rational division; X is an Int computed in the preceding `is`. |
| `section151.pl:157:8` | `s151_d_3_A/7` | `Ea is max(Exemption_amount_in-Reduction_amount,0)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section151.pl:165:16` | `s151_d_3_B/5` | `Difference is max(Agi-Aa,0)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section151.pl:180:20` | `s151_d_3_B/5` | `Number is 2*ceil(Difference/1250)` | M4. `2 * ((Difference + 1249) / 1250)` with Nat/Int floor division (Difference ≥ 0 by the preceding max). |
| `section151.pl:183:20` | `s151_d_3_B/5` | `Number is 2*ceil(Difference/2500)` | M4. `2 * ((Difference + 2499) / 2500)` with Nat/Int floor division (Difference ≥ 0 by the preceding max). |
| `section151.pl:186:8` | `s151_d_3_B/5` | `Ap is min(Number,100)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section151.pl:193:8` | `s151_d_5/2` | `Ea is 0` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section152.pl:134:24` | `s152_c_1_B/6` | `Half_year_duration is Taxy_duration rdiv 2` | D4. Half-year threshold: never materialised; the comparison site is rewritten as `2·(End − Start) ≥ (Dec31 − Jan1)` in whole days. |
| `section152.pl:227:10` | `s152_c_3/3` | `Taxy_25 is Taxy+25` | D5. Int year arithmetic. |
| `section2.pl:37:11` | `s2_a_1_A/5` | `Taxy2 is Taxy-2` | D5. Int year arithmetic. |
| `section2.pl:40:11` | `s2_a_1_A/5` | `Taxy1 is Taxy-1` | D5. Int year arithmetic. |
| `section2.pl:183:31` | `s2_b_1/4` | `Taxy1 is Taxy+1` | D5. Int year arithmetic. |
| `section2.pl:249:24` | `s2_b_1_A/4` | `Half_year_duration is Taxy_duration rdiv 2` | D4. Half-year threshold: never materialised; the comparison site is rewritten as `2·(End − Start) ≥ (Dec31 − Jan1)` in whole days. |
| `section3301.pl:9:9` | `s3301/6` | `Tax is round(0.06*Wages)` | M2/M6. `roundHalfAway (6 * Wages / 100)` exact rational; no ties possible; Int result. |
| `section3306.pl:33:11` | `s3306_a_1_A/3` | `Pyear is Caly-1` | D5. Int year arithmetic. |
| `section3306.pl:52:11` | `s3306_a_1_B/4` | `Year1 is Caly-1` | D5. Int year arithmetic. |
| `section3306.pl:119:11` | `s3306_a_2_A/4` | `Pyear is Caly-1` | D5. Int year arithmetic. |
| `section3306.pl:167:11` | `s3306_a_2_B/6` | `Year1 is Caly-1` | D5. Int year arithmetic. |
| `section3306.pl:242:11` | `s3306_a_3/4` | `Pyear is Caly-1` | D5. Int year arithmetic. |
| `section3306.pl:306:19` | `s3306_b_1/2` | `Remuneration2 is min(7000,Remuneration)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section3306.pl:522:11` | `s3306_c_1_A_i/5` | `Year1 is Caly-1` | D5. Int year arithmetic. |
| `section3306.pl:650:20` | `s3306_c_5_B/4` | `Day_offset is Dob_d+7671` | E1. Unreachable without a type error: `Dob_d` is a two-character string, so `is/2` raises `type_error`. Valid excludes the trigger (V-STR); no Lean arithmetic is defined for this site. |
| `section63.pl:10:9` | `s63/3` | `Taxinc is max(Taxable_income_tmp,0)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:20:8` | `s63_a/5` | `Ded63 is Total_deduction_reduced + Exemption_151` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:21:24` | `s63_a/5` | `Taxable_income_tmp is Grossinc - Ded63` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:22:9` | `s63_a/5` | `Taxinc is max(Taxable_income_tmp,0)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:32:24` | `s63_b/4` | `Taxable_income_tmp is Grossinc - Amount1 - Amount2` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:33:9` | `s63_b/4` | `Taxinc is max(Taxable_income_tmp,0)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:59:21` | `s63_c_1/3` | `Standed is Bassd+Addsd` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:69:19` | `s63_c_1_A/3` | `Bassd is min(Basic_amount,Max_amount)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:73:19` | `s63_c_1_A/3` | `Bassd is Basic_amount` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:89:15` | `s63_c_2/3` | `Bassd is Multiplier*Default_amount` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:107:16` | `s63_c_2_A/3` | `Multiplier is 2` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:131:19` | `s63_c_2_B/3` | `Bassd is 4400` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:140:15` | `s63_c_2_C/2` | `Bassd is 3000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:161:13` | `s63_c_5/5` | `Amount1 is 500` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:163:13` | `s63_c_5/5` | `Amount2 is 250+Grossinc` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:164:11` | `s63_c_5/5` | `Bassd is max(Amount1,Amount2)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:173:13` | `s63_c_6/3` | `Standed is 0` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:260:12` | `s63_c_7_i/2` | `Amount is 18000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:266:12` | `s63_c_7_ii/2` | `Amount is 12000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:314:20` | `s63_f/3` | `Amount is 600` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:317:24` | `s63_f/3` | `Additional_amounts is (Counts_blind+Counts_aged)*Amount` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section63.pl:323:37` | `s63_f_1/3` | `Count1 is 1` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:323:50` | `s63_f_1/3` | `Count1 is 0` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:324:39` | `s63_f_1/3` | `Count2 is 1` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:324:52` | `s63_f_1/3` | `Count2 is 0` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:325:12` | `s63_f_1/3` | `Counts is Count1+Count2` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:334:12` | `s63_f_1_A/2` | `Taxy65 is Taxy+65` | D5. Int year arithmetic. |
| `section63.pl:347:12` | `s63_f_1_B/3` | `Taxy65 is Taxy+65` | D5. Int year arithmetic. |
| `section63.pl:357:37` | `s63_f_2/3` | `Count1 is 1` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:357:50` | `s63_f_2/3` | `Count1 is 0` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:358:39` | `s63_f_2/3` | `Count2 is 600` | M5. As written: a blind spouse contributes 600 to the *count*, which is then multiplied by the amount (F17). Translate literally. |
| `section63.pl:358:54` | `s63_f_2/3` | `Count2 is 0` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:359:12` | `s63_f_2/3` | `Counts is Count1+Count2` | M5. Int counter arithmetic (0/1 from the `->` guards). |
| `section63.pl:387:12` | `s63_f_3/3` | `Amount is 750` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:5:31` | `s68/4` | `Amount_deductions_out is Amount_deductions_in` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:11:35` | `s68/4` | `Amount_deductions_out is Amount_deductions_in-Reduction` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:15:35` | `s68/4` | `Amount_deductions_out is Amount_deductions_in` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:28:8` | `s68_a/6` | `S7 is min(Reduction1,Reduction2)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:32:7` | `s68_a_1/3` | `X is 3*(Agi-Aa)` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:33:8` | `s68_a_1/3` | `S9 is round(X rdiv 100)` | M3. `roundHalfAway (X / 100)` with exact rational division; X is an Int computed in the preceding `is`. |
| `section68.pl:38:7` | `s68_a_2/4` | `X is 80*Itemded` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:39:9` | `s68_a_2/4` | `S14 is round(X rdiv 100)` | M3. `roundHalfAway (X / 100)` with exact rational division; X is an Int computed in the preceding `is`. |
| `section68.pl:53:12` | `amount/2` | `Amount is 300000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:55:12` | `amount/2` | `Amount is 275000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:57:12` | `amount/2` | `Amount is 250000` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `section68.pl:60:12` | `amount/2` | `Amount is round(Amount_A rdiv 2)` | M3. `roundHalfAway (300000 / 2) = 150000` (constant). |
| `section7703.pl:21:8` | `s7703_a_1/5` | `Taxy1 is Taxy+1` | D5. Int year arithmetic. |
| `section7703.pl:137:24` | `s7703_b_1/4` | `Half_year_duration is Taxy_duration rdiv 2` | D4. Half-year threshold: never materialised; the comparison site is rewritten as `2·(End − Start) ≥ (Dec31 − Jan1)` in whole days. |
| `section7703.pl:183:8` | `s7703_b_2/4` | `Ratio is Payment_by_individual rdiv Cost` | M3. Ratio never materialised; `Ratio ≥ 1/2` is rewritten as `2·Payment_by_individual ≥ Cost` (Cost > 0 already checked). |
| `utils.pl:7:6` | `day_to_stamp/2` | `DI1 is DI+1` | D2. The +1 day shift inside `day_to_stamp`; cancels in every comparison and duration; matters only for `format_time` (D8). |
| `utils.pl:95:11` | `duration/3` | `Duration is Stamp2-Stamp1` | D4. Duration in seconds = 86400·(day2 − day1); all consumers are rewritten in whole days. |
| `utils.pl:286:26` | `gross_income/3` | `Gross_income is Income_individual+Income_spouse` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `utils.pl:330:18` | `gross_income_individual/3` | `Gross_income is Income+Payment` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `utils.pl:338:24` | `tax/3` | `Income_tax is 0` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `utils.pl:345:28` | `tax/3` | `Employment_tax is 0` | M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding. |
| `utils.pl:348:9` | `tax/3` | `Tax is Income_tax+Employment_tax` | D5. Int year arithmetic. |

---

---

## Dates

**D1 (representation).** `Day : Int` = days since 1970-01-01 in the
proleptic Gregorian calendar (`Day 0 = 1970-01-01`). Conversion to and from
`YYYY-MM-DD` uses the standard civil-date algorithm (days-from-civil /
civil-from-days); the serializer always emits four-digit zero-padded years.
`Year : Int`. Valid restricts dates to years 1900–2100 and `Year` to
1900–2100 (V3), which keeps every `Taxy+65` and `Taxy+25` inside the range the
interpreter's `date_time_stamp/2` was probed on and keeps 4-digit year strings
in numeric order (G4).

**D2 (the interpreter's stamp).** `day_to_stamp(D)` is
`86400 × (Day(D) + 1)` seconds (UTC midnight of the *following* day): probed
`2015-01-01 → 1420070400.0` which is 2015-01-02T00:00Z. The shift cancels in
every comparison and duration and is undone by the time zone pin for every
`format_time` observation (D8). Day-of-month overflow is normalised forward
(`"2017-02-30"` behaves as 2017-03-02, probed); Valid forbids invalid dates
(V3), so the oracle never normalises. Malformed strings (`"2017-1-1"` is
accepted by `atom_number`; `"x"` makes `day_to_stamp` fail silently) are
likewise excluded by V3.

**D3 (`is_before`).** `is_before(A,B)` is `A ≤ B` on `Day` (probed: equal
dates succeed). With either argument unbound it fails (the `nonvar` guards,
probed). Every date that can be unbound is `Option Day` in Lean, and the
comparison `le? : Option Day → Option Day → Bool` is `false` when either side
is `none`. Sites where an `Option` can reach `is_before` are all guarded by
`var/1` disjunctions or by `latest/earliest` (D7); the guard patterns
`(var(X) ; is_before(X,Y))` and `(is_before(X,Y) ; var(X))` both mean
"`X = none ∨ X ≤ Y`".

**D4 (durations in whole days).** `duration(A,B)` is `86400·(B − A)`
seconds (probed: 2017-01-01 → 2017-12-31 = 31449600 = 364 days; 2016 = 365
days). Every consumer compares two durations, so all are rewritten in whole
days with no rationals:

| Site | Source | Whole-day form |
| --- | --- | --- |
| `section152.pl:133-136` | `Duration >= Taxy_duration rdiv 2` | `2·(End_day − Start_day) ≥ (Dec31 − Jan1)` i.e. ≥ 364 (365 in leap years) |
| `section2.pl:247-250` | same | `2·(End_res − Start_res) ≥ (Dec31 − Jan1)` |
| `section7703.pl:135-138` | same | `2·(End − Start) ≥ (Dec31 − Jan1)` |
| `section152.pl:226-230` | `Age_individual =< Duration_25_years` | `(Dec31_Y − dob) ≤ (Dec31_{Y+25} − Dec31_Y)` |
| `section63.pl:333-337` | `Time_since_birth >= Sixtyfive_years` | `(Dec31_Y − dob) ≥ (Dec31_{Y+65} − Dec31_Y)` |
| `section63.pl:346-350` | same for spouse | same |

Note the half-year test is `≥`, measures the *difference* of the end points
(a residence from Jan 1 to Jul 1 is 181 days and fails in a common year; Jan 1
to Jul 2 passes), and the difference is between the clamped window ends, not a
count of days inclusive.

**D5 (years).** `first_day_year(Y)` = Jan 1 of `Y`, `last_day_year(Y)` =
Dec 31 of `Y`; `Taxy ± k` is `Int` arithmetic; `split_string/atom_number`
year extraction is the year component of the `Day`; `Taxy == Taxy_payment_int`
is `Int` equality; `Year_remuneration @> Caly` (`section3306.pl:418`) compares
two year *strings* and equals numeric `>` inside V3.

**D6 (interval semantics per predicate).** All intervals are closed at both
ends. `Jan1`/`Dec31` are of the taxable year unless stated.

| Predicate | Sites | Semantics |
| --- | --- | --- |
| `gross_income_individual/3` | `utils.pl:311-312, 323-324` | event counts iff `Jan1 ≤ start ≤ Dec31` (start required; end ignored) |
| `s63_d/4` | `section63.pl:281-282` | deduction counts iff `Jan1 ≤ start ≤ Dec31` |
| `s63_c_6_A/4` | `section63.pl:195-196` | itemising deduction of either spouse iff `Jan1 ≤ start ≤ Dec31` |
| `s63_c_6_B/2`, `s63_c_6_D/2`, `s2_a_2_B/3`, `s2_b_2_B/3` | `section63.pl:206-220, 231-245`, `section2.pl:125-141, 345-359` | status overlaps the year iff `(start absent ∨ start ≤ Dec31) ∧ (end absent ∨ Jan1 ≤ end)` |
| `s1_a_1/6` | `section1.pl:33-48` | same overlap with explicit defaults `start ← Jan1`, `end ← Dec31` |
| `s2_b_3_A/3` | `section2.pl:401-420` | `(start absent → S119 = Jan1) ∨ (start ≤ Dec31 → S119 = Dec31)`; then `(end absent) ∨ (Jan1 ≤ end ∧ end ≥ S119)` — with both a start and an end the event must end on/after Dec 31 (F11) |
| `s63_f_2_A/2`, `s63_f_2_B/3` | `section63.pl:367, 376` | blind iff `start ≤ Dec31` (end ignored) |
| `s63_f_1_A/2`, `s63_f_1_B/3` | D4 | age 65 by Dec 31 |
| `s7703_a_1/5` | `section7703.pl:37-82` | marriage start (default Jan1) `≤ Dec31`; if the spouse's first death event is inside `[Jan1, Dec31]`: `start ≤ death ∧ (end absent ∨ death ≤ end)`; else: `end absent → (spouse has any death event → its date ≥ Jan 1 of Taxy+1 ; else true)`; `end present → end ≥ Jan 1 of Taxy+1` |
| `s7703_a_2/5`, `s2_b_2_A/5` | `section7703.pl:98`, `section2.pl:332` | decree start `≤ Dec31` |
| `s7703_b_1/4` | `section7703.pl:125-138` | child residence window `[max(start, Jan1), min(end, Dec31)]` (end absent → Dec31); half-year rule D4 |
| `s7703_b_2/4` | `section7703.pl:155-158` | payment counts iff `year(start) = Taxy` |
| `s7703_b_3/4` | `section7703.pl:205-216` | spouse is a member on day `d` iff `start ≤ d ∧ (end absent ∨ d ≤ end)`; `d` ranges over the D8 window; the paragraph holds iff no such `d` |
| `s7703_b_3_is_member_of_household/3` | `section7703.pl:192-200` | as above for one `d` |
| `s2_a_1_A/5` | `section2.pl:27-42` | `start_marriage ≤ death ∧ (end absent ∨ death ≤ end) ∧ Jan 1 of Taxy−2 ≤ death ≤ Dec 31 of Taxy−1` |
| `s2_a_1_B/4` | `section2.pl:55-92` | taxpayer residence `start ≤ Jan1 ∧ (end absent ∨ end ≥ Dec31)`; dependent residence same; kinship `(start none ∨ start ≤ Jan1) ∧ (end none ∨ end ≥ Dec31)` |
| `s2_a_2_A/5` | `section2.pl:111-113` | `start_prev < … ` is `start_prev ≤ remarriage_start ≤ Dec31` |
| `s2_b_1/4` | `section2.pl:160-190` | marriage `start ≤ Dec31`; dead spouse: `s2_b_2_C` or `death > Dec31` (strictly, via `is_before(Dec31, death)` which is `≤`: `Dec31 ≤ death`); living spouse: `end ≥ Jan 1 of Taxy+1 ∨ end absent` |
| `s2_b_1_A/4` | `section2.pl:210-250` | taxpayer residence `(start present → start ≤ Jan1) ∧ (end present → end ≥ Dec31)`; dependent residence window `[start∨Jan1, end∨Dec31]` half-year rule D4 (unclamped: a start before Jan 1 lengthens the window) |
| `s2_b_1_B/5` | `section2.pl:288-308` | parent residence `start ≤ Jan1 ∧ (end absent ∨ end ≥ Dec31)`; kinship `(start ≤ Jan1 ∨ start none) ∧ (end ≥ Dec31 ∨ end none)` |
| `s2_b_2_C/4` | `section2.pl:373-383` | `(end absent ∨ death ≤ end) ∧ Jan1 ≤ death ≤ Dec31` |
| `s2_b_3_B/3` | `section2.pl:441-458` | relationships A–G excluded iff `(start none ∨ start ≤ Jan1) ∧ (end none ∨ end ≤ Dec31)`; H required with `(StartH none ∨ StartH ≤ Jan1) ∧ (EndH none ∨ EndH ≥ Dec31)` |
| `s152_c_1_A/4`, `s152_d_1_A/5` | `section152.pl:72-86, 249-263` | relationship end = earliest of {taxpayer's first death date, dependent's first death date, kinship end}, `none` if all absent |
| `s152_c_1_B/6` | `section152.pl:94-136` | residence windows default to `[Jan1, Dec31]`; overlap start = latest of {both starts, Jan1, relationship start}, end = earliest of {both ends, Dec31, relationship end}; half-year rule D4 on `end − start` |
| `s152_c_3/3` | `section152.pl:204, 226-230` | taxpayer dob `≤` dependent dob; age < 25 rule per D4 (`≤`) |
| `s152_d_2_H/6` | `section152.pl:352-386` | no marriage with `start ≤ Dec31 ∧ (end present → end ≥ Jan1)`; both residences `start ≤ Jan1 ∧ (end present → end ≥ Dec31)` |
| `s3306_a_1_is_wages/4`, `s3306_a_2_is_wages/5`, `s3306_a_3_is_wages/5` | `section3306.pl:19-23, 106-110, 221-225` | payment counts iff `Jan1 ≤ start ≤ Dec31` of the year argument |
| `s3306_a_1_B/4`, `s3306_a_2_B/6` | `section3306.pl:58-59, 174-175` | day counts iff `Jan 1 of Caly−1 ≤ day ≤ Dec 31 of Caly` |
| `s3306_c_1_A_i/5` | `section3306.pl:540-541` | payment counts iff `Jan 1 of Caly−1 ≤ start ≤ Dec 31 of Caly` |
| `s3306_c_5_A/4`, `s3306_c_10_A_i/3`, `s3306_c_10_A_ii/3`, `s3306_c_10_B/4`, `s3306_c_13/4`, `s3306_c_21/4` | listed in the site table | status holds on `Workday` iff `start ≤ Workday ∧ (end absent ∨ Workday ≤ end)`; `s3306_c_10_A_ii` marriage start may be absent (then no lower bound) |
| `s3306_b_10_A/6` | `section3306.pl:376-377` | termination (its start, or the service end) `≤` remuneration start |
| `s3306_b_15/5` | `section3306.pl:415-418` | marriage `end absent ∨ end = death date`; `year(remuneration) > year(death)` |
| `is_child_of/4` and the kinship helpers | `utils.pl:118-270` | relationship window = `[start?, end?]` as `Option` pairs; in-law and step relations take latest of starts and earliest of ends (D7) |

**D7 (`latest/2`, `earliest/2`).** Over a list of `Option Day`: the maximum
(minimum) of the `some` entries; `none` when there is no `some` entry (probed:
`latest([_,_],L)` leaves `L` unbound; `latest(["2017-01-01",_,"2016-05-05"])`
is 2017-01-01). Equal entries are fine. Three special uses: (D7.1)
`earliest([S119,Stop_nra],S119)` (`section2.pl:419`) unifies the result with
an already-bound `S119` and therefore *tests* `Stop_nra ≥ S119` (F11); (D7.2)
in `s152_c_1_B` the lists always contain `Jan1`/`Dec31`, so the result is
never `none`; (D7.3) elsewhere a `none` result flows into a `var/1`-guarded
comparison (D3) or into another `latest/earliest`.

**D8 (time zone and `format_time`) [CONTRACT].** The harness must run the
pinned interpreter with `TZ=America/New_York` (P-TZ). Justification: it is the
only setting under which the reference program agrees with all 376 SARA labels
(F1). Under that setting `format_time/3` renders `86400·(d+1)` (UTC midnight of
`d+1`) as 19:00 or 20:00 local time on day `d`, so every formatted observation
refers to `d` itself and the `+1` of D2 is invisible. Consequences:

* `s7703_b_3` (`section7703.pl:208-210`): `date(Taxy,7,Off)` for `Off ∈
  2..185` are UTC midnights of Jul 2 … Jan 1; formatted in New York they are
  the 184 days **Jul 1 … Dec 31 of Taxy** (probed). Under UTC they would be
  Jul 2 … Jan 1 of Taxy+1 (probed), which is why the pin is a semantic
  decision and not a deployment detail.
* `%W` (`section3306.pl:76,192`): the label of day `d` is C's `strftime("%W")`
  of `d`: `W(d) = (yday0(d) + 7 − wdayMon(d)) / 7` with `yday0` the 0-based
  day of year and `wdayMon` the weekday with Monday = 0 … Sunday = 6; days
  before the first Monday of the year are week `00`. Verified equal to the
  interpreter for 1500 consecutive dates (`evidence/probe3_*`, shifted form)
  and directly for nine dates under the pin (`evidence/probe4_*`: 2017-01-01 →
  `00`, 2017-01-02 → `01`, 2017-12-31 → `52`, 2018-01-01 → `01`). The label is
  two characters without a year, so `list_to_set` over labels from `Caly−1`
  and `Caly` merges equal week numbers of different years (A-DAYS).
* No other site formats time. `is_before`, `duration`, `split_string` and
  `date_time_stamp` are TZ-independent.

Daylight-saving transitions do not move the local day (UTC 00:00 is 19:00 or
20:00 the previous evening in New York in every year of V3), so the rule is
uniform.

**D9 (dates in observations).** Output date values are serialized as
`"YYYY-MM-DD"` strings and unbound dates as JSON `null` (H6).

**D10 (date-comparison inventory).** Every `is_before`, `latest`, `earliest`,
duration comparison and year-string comparison site, for cross-checking
against the D6 table:

| Site | Predicate | Symbol | Construct |
| --- | --- | --- | --- |
| `section1.pl:47:9` | `s1_a_1/6` | `is_before` | `is_before(Start_time,Last_day)` |
| `section1.pl:48:9` | `s1_a_1/6` | `is_before` | `is_before(First_day,End_time)` |
| `section152.pl:86:2` | `s152_c_1_A/4` | `earliest` | `earliest([End_t,End_i,End_day],End_relationship)` |
| `section152.pl:130:5` | `s152_c_1_B/6` | `earliest` | `earliest([End_individual,End_taxpayer,Last_day_of_year,End_relationshi` |
| `section152.pl:132:5` | `s152_c_1_B/6` | `latest` | `latest([Start_individual,Start_taxpayer,First_day_of_year,Start_relati` |
| `section152.pl:136:11` | `s152_c_1_B/6` | `>=` | `Duration >= Half_year_duration` |
| `section152.pl:204:13` | `s152_c_3/3` | `is_before` | `is_before(Taxpayer_dob,Individual_dob)` |
| `section152.pl:230:17` | `s152_c_3/3` | `=<` | `Age_individual =< Duration_25_years` |
| `section152.pl:263:2` | `s152_d_1_A/5` | `earliest` | `earliest([End_t,End_i,End_day],End_relationship)` |
| `section152.pl:324:5` | `s152_d_2_E/5` | `latest` | `latest([Start_day_sibling,Start_day_child],Start_day)` |
| `section152.pl:325:5` | `s152_d_2_E/5` | `earliest` | `earliest([End_day_sibling,End_day_child],End_day)` |
| `section152.pl:331:5` | `s152_d_2_F/5` | `latest` | `latest([Start_day_sibling,Start_day_child],Start_day)` |
| `section152.pl:332:5` | `s152_d_2_F/5` | `earliest` | `earliest([End_day_sibling,End_day_child],End_day)` |
| `section152.pl:352:9` | `s152_d_2_H/6` | `is_before` | `is_before(Start,Last_day_year)` |
| `section152.pl:356:4` | `s152_d_2_H/6` | `is_before` | `is_before(First_day_year,End)` |
| `section152.pl:365:5` | `s152_d_2_H/6` | `is_before` | `is_before(Start_taxpayer_residence,First_day_year)` |
| `section152.pl:369:3` | `s152_d_2_H/6` | `is_before` | `is_before(Last_day_year,End_taxpayer_residence)` |
| `section152.pl:377:5` | `s152_d_2_H/6` | `is_before` | `is_before(Start_individual_residence,First_day_year)` |
| `section152.pl:381:3` | `s152_d_2_H/6` | `is_before` | `is_before(Last_day_year,End_individual_residence)` |
| `section152.pl:385:5` | `s152_d_2_H/6` | `latest` | `latest([Start_taxpayer_residence,Start_individual_residence],Start_day` |
| `section152.pl:386:5` | `s152_d_2_H/6` | `earliest` | `earliest([End_taxpayer_residence,End_individual_residence],End_day)` |
| `section2.pl:27:5` | `s2_a_1_A/5` | `is_before` | `is_before(Start_marriage,Time_death)` |
| `section2.pl:34:13` | `s2_a_1_A/5` | `is_before` | `is_before(Time_death,End_marriage)` |
| `section2.pl:39:5` | `s2_a_1_A/5` | `is_before` | `is_before(First_day_year,Time_death)` |
| `section2.pl:42:5` | `s2_a_1_A/5` | `is_before` | `is_before(Time_death,Last_day_year)` |
| `section2.pl:55:5` | `s2_a_1_B/4` | `is_before` | `is_before(Start_taxpayer_residence,First_day_year)` |
| `section2.pl:62:13` | `s2_a_1_B/4` | `is_before` | `is_before(Last_day_year,End_taxpayer_residence)` |
| `section2.pl:70:5` | `s2_a_1_B/4` | `is_before` | `is_before(Start_dependent_residence,First_day_year)` |
| `section2.pl:77:13` | `s2_a_1_B/4` | `is_before` | `is_before(Last_day_year,End_dependent_residence)` |
| `section2.pl:87:9` | `s2_a_1_B/4` | `is_before` | `is_before(Start_dependent,First_day_year)` |
| `section2.pl:91:9` | `s2_a_1_B/4` | `is_before` | `is_before(Last_day_year,End_dependent)` |
| `section2.pl:111:5` | `s2_a_2_A/5` | `is_before` | `is_before(Start_previous_marriage,S31)` |
| `section2.pl:113:5` | `s2_a_2_A/5` | `is_before` | `is_before(S31,Last_day_year)` |
| `section2.pl:130:17` | `s2_a_2_B/3` | `is_before` | `is_before(Start_nra,Last_day_year)` |
| `section2.pl:140:17` | `s2_a_2_B/3` | `is_before` | `is_before(First_day_year,End_nra)` |
| `section2.pl:162:9` | `s2_b_1/4` | `is_before` | `is_before(Start_marriage,Last_day_year)` |
| `section2.pl:171:25` | `s2_b_1/4` | `is_before` | `is_before(Last_day_year,Death_time)` |
| `section2.pl:185:25` | `s2_b_1/4` | `is_before` | `is_before(First_day_year1,End_marriage)` |
| `section2.pl:213:9` | `s2_b_1_A/4` | `is_before` | `is_before(Start_taxpayer_residence,First_day_year)` |
| `section2.pl:220:9` | `s2_b_1_A/4` | `is_before` | `is_before(Last_day_year,End_taxpayer_residence)` |
| `section2.pl:250:35` | `s2_b_1_A/4` | `>=` | `Duration_individual_residence >= Half_year_duration` |
| `section2.pl:289:5` | `s2_b_1_B/5` | `is_before` | `is_before(Start_dependent_residence,First_day_year)` |
| `section2.pl:297:13` | `s2_b_1_B/5` | `is_before` | `is_before(Last_day_year,End_dependent_residence)` |
| `section2.pl:302:9` | `s2_b_1_B/5` | `is_before` | `is_before(Start_child,First_day_year)` |
| `section2.pl:306:9` | `s2_b_1_B/5` | `is_before` | `is_before(Last_day_year,End_child)` |
| `section2.pl:332:5` | `s2_b_2_A/5` | `is_before` | `is_before(Divorce_time,Last_day_year)` |
| `section2.pl:349:13` | `s2_b_2_B/3` | `is_before` | `is_before(Start_nra,Last_day_year)` |
| `section2.pl:358:13` | `s2_b_2_B/3` | `is_before` | `is_before(First_day_year,Stop_nra)` |
| `section2.pl:379:13` | `s2_b_2_C/4` | `is_before` | `is_before(Time_death,End_marriage)` |
| `section2.pl:382:5` | `s2_b_2_C/4` | `is_before` | `is_before(First_day_year,Time_death)` |
| `section2.pl:383:5` | `s2_b_2_C/4` | `is_before` | `is_before(Time_death,Last_day_year)` |
| `section2.pl:408:13` | `s2_b_3_A/3` | `is_before` | `is_before(Start_nra,Last_day_year)` |
| `section2.pl:418:13` | `s2_b_3_A/3` | `is_before` | `is_before(First_day_year,Stop_nra)` |
| `section2.pl:419:13` | `s2_b_3_A/3` | `earliest` | `earliest([S119,Stop_nra],S119)` |
| `section2.pl:443:13` | `s2_b_3_B/3` | `is_before` | `is_before(Start_relationship,First_day)` |
| `section2.pl:447:13` | `s2_b_3_B/3` | `is_before` | `is_before(End_relationship,Last_day)` |
| `section2.pl:453:9` | `s2_b_3_B/3` | `is_before` | `is_before(StartH,First_day)` |
| `section2.pl:457:9` | `s2_b_3_B/3` | `is_before` | `is_before(Last_day,EndH)` |
| `section3301.pl:18:13` | `total_wages_employer/6` | `is_before` | `is_before(Start_day,Remuneration_time)` |
| `section3301.pl:19:13` | `total_wages_employer/6` | `is_before` | `is_before(Remuneration_time,End_day)` |
| `section3306.pl:21:5` | `s3306_a_1_is_wages/4` | `is_before` | `is_before(Time,Last_day_year)` |
| `section3306.pl:23:5` | `s3306_a_1_is_wages/4` | `is_before` | `is_before(First_day_year,Time)` |
| `section3306.pl:58:13` | `s3306_a_1_B/4` | `is_before` | `is_before(First_day_year1,Day)` |
| `section3306.pl:59:13` | `s3306_a_1_B/4` | `is_before` | `is_before(Day,Last_day_year)` |
| `section3306.pl:108:5` | `s3306_a_2_is_wages/5` | `is_before` | `is_before(Time,Last_day_year)` |
| `section3306.pl:110:5` | `s3306_a_2_is_wages/5` | `is_before` | `is_before(First_day_year,Time)` |
| `section3306.pl:174:13` | `s3306_a_2_B/6` | `is_before` | `is_before(First_day_year1,Day)` |
| `section3306.pl:175:13` | `s3306_a_2_B/6` | `is_before` | `is_before(Day,Last_day_year)` |
| `section3306.pl:223:5` | `s3306_a_3_is_wages/5` | `is_before` | `is_before(Time,Last_day_year)` |
| `section3306.pl:225:5` | `s3306_a_3_is_wages/5` | `is_before` | `is_before(First_day_year,Time)` |
| `section3306.pl:377:5` | `s3306_b_10_A/6` | `is_before` | `is_before(Start_termination,Start_remuneration)` |
| `section3306.pl:418:19` | `s3306_b_15/5` | `@>` | `Year_remuneration@>Caly` |
| `section3306.pl:540:13` | `s3306_c_1_A_i/5` | `is_before` | `is_before(First_day_year,Payment_time)` |
| `section3306.pl:541:13` | `s3306_c_1_A_i/5` | `is_before` | `is_before(Payment_time,Last_day_year)` |
| `section3306.pl:626:13` | `s3306_c_5_A/4` | `is_before` | `is_before(Time_start,Workday)` |
| `section3306.pl:633:21` | `s3306_c_5_A/4` | `is_before` | `is_before(Workday,Time_end)` |
| `section3306.pl:694:2` | `s3306_c_10_A_i/3` | `is_before` | `is_before(Start_enrollment,Workday)` |
| `section3306.pl:695:2` | `s3306_c_10_A_i/3` | `is_before` | `is_before(Start_attendance,Workday)` |
| `section3306.pl:702:4` | `s3306_c_10_A_i/3` | `is_before` | `is_before(Workday,Stop_enrollment)` |
| `section3306.pl:711:4` | `s3306_c_10_A_i/3` | `is_before` | `is_before(Workday,Stop_attendance)` |
| `section3306.pl:726:4` | `s3306_c_10_A_ii/3` | `is_before` | `is_before(Start_marriage,Workday)` |
| `section3306.pl:735:4` | `s3306_c_10_A_ii/3` | `is_before` | `is_before(Workday,End_marriage)` |
| `section3306.pl:751:2` | `s3306_c_10_B/4` | `is_before` | `is_before(Start_patient,Workday)` |
| `section3306.pl:758:4` | `s3306_c_10_B/4` | `is_before` | `is_before(Workday,End_patient)` |
| `section3306.pl:789:2` | `s3306_c_13/4` | `is_before` | `is_before(Start_enrollment,Workday)` |
| `section3306.pl:790:2` | `s3306_c_13/4` | `is_before` | `is_before(Start_attendance,Workday)` |
| `section3306.pl:797:4` | `s3306_c_13/4` | `is_before` | `is_before(Workday,Stop_enrollment)` |
| `section3306.pl:806:4` | `s3306_c_13/4` | `is_before` | `is_before(Workday,Stop_attendance)` |
| `section3306.pl:826:2` | `s3306_c_21/4` | `is_before` | `is_before(Start_incarceration,Workday)` |
| `section3306.pl:833:4` | `s3306_c_21/4` | `is_before` | `is_before(Workday,End_incarceration)` |
| `section63.pl:195:4` | `s63_c_6_A/4` | `is_before` | `is_before(First_day_year,Start)` |
| `section63.pl:196:4` | `s63_c_6_A/4` | `is_before` | `is_before(Start,Last_day_year)` |
| `section63.pl:210:13` | `s63_c_6_B/2` | `is_before` | `is_before(Start_nra,Last_day_year)` |
| `section63.pl:219:13` | `s63_c_6_B/2` | `is_before` | `is_before(First_day_year,End_nra)` |
| `section63.pl:235:13` | `s63_c_6_D/2` | `is_before` | `is_before(Start_trust,Last_day_year)` |
| `section63.pl:244:13` | `s63_c_6_D/2` | `is_before` | `is_before(First_day_year,End_trust)` |
| `section63.pl:281:4` | `s63_d/4` | `is_before` | `is_before(First,Start)` |
| `section63.pl:282:4` | `s63_d/4` | `is_before` | `is_before(Start,Last)` |
| `section63.pl:337:21` | `s63_f_1_A/2` | `>=` | `Time_since_birth>=Sixtyfive_years` |
| `section63.pl:350:21` | `s63_f_1_B/3` | `>=` | `Time_since_birth>=Sixtyfive_years` |
| `section63.pl:367:5` | `s63_f_2_A/2` | `is_before` | `is_before(Start_time,Last_day_year)` |
| `section63.pl:376:5` | `s63_f_2_B/3` | `is_before` | `is_before(Start_time,Last_day_year)` |
| `section7703.pl:37:5` | `s7703_a_1/5` | `is_before` | `is_before(Start_marriage,Last_day_year)` |
| `section7703.pl:43:4` | `s7703_a_1/5` | `is_before` | `is_before(First_day_year,S13)` |
| `section7703.pl:44:4` | `s7703_a_1/5` | `is_before` | `is_before(S13,Last_day_year)` |
| `section7703.pl:47:4` | `s7703_a_1/5` | `is_before` | `is_before(Start_marriage,S13)` |
| `section7703.pl:54:6` | `s7703_a_1/5` | `is_before` | `is_before(S13,End_time)` |
| `section7703.pl:70:7` | `s7703_a_1/5` | `is_before` | `is_before(First_day_next_year,End_time)` |
| `section7703.pl:78:6` | `s7703_a_1/5` | `is_before` | `is_before(First_day_next_year,End_time)` |
| `section7703.pl:98:2` | `s7703_a_2/5` | `is_before` | `is_before(Divorce_time,Last_day_year)` |
| `section7703.pl:126:5` | `s7703_b_1/4` | `latest` | `latest([Start_time,First_day_year],Start)` |
| `section7703.pl:133:5` | `s7703_b_1/4` | `earliest` | `earliest([End_time,Last_day_year],End)` |
| `section7703.pl:138:11` | `s7703_b_1/4` | `>=` | `Duration >= Half_year_duration` |
| `section7703.pl:192:5` | `s7703_b_3_is_member_of_household/3` | `is_before` | `is_before(Time_start,Day)` |
| `section7703.pl:199:4` | `s7703_b_3_is_member_of_household/3` | `is_before` | `is_before(Day,Time_end)` |
| `utils.pl:30:9` | `latest/2` | `latest` | `latest(Days,Day,Output)` |
| `utils.pl:34:9` | `latest/2` | `latest` | `latest(Days,Output)` |
| `utils.pl:44:17` | `latest/3` | `is_before` | `is_before(Day,Latest)` |
| `utils.pl:45:17` | `latest/3` | `latest` | `latest(Days,Latest,Output)` |
| `utils.pl:48:20` | `latest/3` | `is_before` | `is_before(Day,Latest)` |
| `utils.pl:49:17` | `latest/3` | `latest` | `latest(Days,Day,Output)` |
| `utils.pl:55:9` | `latest/3` | `latest` | `latest(Days,Latest,Output)` |
| `utils.pl:64:9` | `earliest/2` | `earliest` | `earliest(Days,Day,Output)` |
| `utils.pl:68:9` | `earliest/2` | `earliest` | `earliest(Days,Output)` |
| `utils.pl:78:17` | `earliest/3` | `is_before` | `is_before(Earliest,Day)` |
| `utils.pl:79:17` | `earliest/3` | `earliest` | `earliest(Days,Earliest,Output)` |
| `utils.pl:82:20` | `earliest/3` | `is_before` | `is_before(Earliest,Day)` |
| `utils.pl:83:17` | `earliest/3` | `earliest` | `earliest(Days,Day,Output)` |
| `utils.pl:89:9` | `earliest/3` | `earliest` | `earliest(Days,Earliest,Output)` |
| `utils.pl:180:5` | `is_stepsibling_of/4` | `latest` | `latest([Day_start_x,Day_start_y,Start_time], Day_start)` |
| `utils.pl:187:5` | `is_stepsibling_of/4` | `earliest` | `earliest([Day_end_x,Day_end_y,End_time],Day_end)` |
| `utils.pl:205:5` | `is_sibling_in_law_of_aux/4` | `latest` | `latest([Start_time,Day_start_y],Day_start)` |
| `utils.pl:212:5` | `is_sibling_in_law_of_aux/4` | `earliest` | `earliest([End_time,Day_end_y],Day_end)` |
| `utils.pl:226:5` | `is_child_in_law_of/4` | `latest` | `latest([Start_time,Day_start_y],Day_start)` |
| `utils.pl:233:5` | `is_child_in_law_of/4` | `earliest` | `earliest([End_time,Day_end_y],Day_end)` |
| `utils.pl:247:5` | `is_parent_in_law_of/4` | `latest` | `latest([Start_time,Day_start_y],Day_start)` |
| `utils.pl:254:5` | `is_parent_in_law_of/4` | `earliest` | `earliest([End_time,Day_end_y],Day_end)` |
| `utils.pl:262:5` | `is_stepparent_of/4` | `latest` | `latest([Start_time,Day_start_y],Day_start)` |
| `utils.pl:270:5` | `is_stepparent_of/4` | `earliest` | `earliest([End_time,Day_end_y],Day_end)` |
| `utils.pl:311:13` | `gross_income_individual/3` | `is_before` | `is_before(First_day_year,Start_time)` |
| `utils.pl:312:13` | `gross_income_individual/3` | `is_before` | `is_before(Start_time,Last_day_year)` |
| `utils.pl:323:13` | `gross_income_individual/3` | `is_before` | `is_before(First_day_year,Start_time)` |
| `utils.pl:324:13` | `gross_income_individual/3` | `is_before` | `is_before(Start_time,Last_day_year)` |

---

---

## Household

**H1 (shape).**

```lean
structure Household where
  facts        : List Fact      -- source order, duplicates kept (F13)
  stipulations : List Stip      -- H4; empty for every generated input
```

`Fact` has one constructor per declared event predicate (H3) with `Term`
arguments; `Term` is G4. Order is the clause order of the case file after
grounding (H4.2). Nothing is keyed, deduplicated, sorted or defaulted. An
absent fact is simply absent (G5).

**H2 (argument kinds).** `amount_` carries `int`; `start_`/`end_` carry a
`Day` (D1); every other position carries `atom` or `str` exactly as the source
lexeme (a double-quoted lexeme is `str`, an unquoted one is `atom`; the
serializer reproduces the quoting). Wildcards: the original corpus has exactly
two bodyless event facts with a wildcard, both `purpose_(_,"agricultural
labor")` (`s3306_a_2_B_neg.pl:75`, `s3306_a_2_B_pos.pl`), and 124 wildcard
positions inside stipulations. A wildcard in an event fact means "matches any
bound value in that position"; every statute call of `purpose_/2` binds the
first argument, so no unbound wildcard ever flows out of a fact. Wildcards are
permitted only in `purpose_` position 1 of event facts and in stipulation
patterns; `Valid` forbids them in generated inputs (V1).

**H3 (field list).** The 61 predicates declared in `events.pl`, with the role
each argument plays in the statutes, how many statute call sites read the
predicate, and how many case clauses supply it. Predicates with zero statute
reads are still part of `Household` (the serializer must round-trip them) but
never affect any output.

| Declared predicate | Argument roles | Statute reads | Case clauses |
| --- | --- | --- | --- |
| `agent_/2` | (event, participant): the actor of an event; marriages and joint returns list both spouses as agents; residences list residents | 154 | 1358 |
| `agricultural_service/3` | case-local helper name (rules only) | 0 | 2 |
| `alice_employer/3` | case-local helper name (rules only) | 0 | 1 |
| `alice_household_maintenance/4` | case-local helper name (rules only) | 0 | 10 |
| `american_employer_/1` | (event id): event/status type marker | 1 | 7 |
| `amount_/2` | (event, Int dollars) | 7 | 400 |
| `attending_classes_/1` | (event id): event/status type marker | 2 | 8 |
| `beneficiary_/2` | (plan event, person) | 2 | 18 |
| `birth_/1` | (event id): event/status type marker | 7 | 29 |
| `blindness_/1` | (event id): event/status type marker | 2 | 7 |
| `brother_/1` | (event id): event/status type marker | 1 | 13 |
| `business_/1` | (event id): event/status type marker | 1 | 2 |
| `business_trust_/1` | (event id): event/status type marker | 1 | 2 |
| `citizenship_/1` | (event id): event/status type marker | 2 | 14 |
| `country_/2` | (place, country string) | 4 | 14 |
| `daughter_/1` | (event id): event/status type marker | 2 | 1 |
| `death_/1` | (event id): event/status type marker | 12 | 50 |
| `deduction_/1` | (event id): event/status type marker | 2 | 20 |
| `destination_/2` | (migration event, place) | 1 | 1 |
| `disability_/1` | (event id): event/status type marker | 1 | 4 |
| `educational_institution_/1` | (event id): event/status type marker | 1 | 7 |
| `end_/2` | (event, Day) | 95 | 453 |
| `enrollment_/1` | (event id): event/status type marker | 2 | 8 |
| `father_/1` | (event id): event/status type marker | 1 | 35 |
| `first_day_year/2` | statute predicate declared discontiguous here; never defined in cases | 41 | 0 |
| `gross_income/3` | statute predicate; never defined in cases | 9 | 0 |
| `hospital_/1` | (event id): event/status type marker | 2 | 4 |
| `incarceration_/1` | (event id): event/status type marker | 1 | 3 |
| `income_/1` | (event id): event/status type marker | 1 | 122 |
| `international_organization_/1` | (event id): event/status type marker | 1 | 1 |
| `is_before/2` | statute predicate; never defined in cases | 104 | 0 |
| `itemize_deductions_/1` | (event id): event/status type marker | 0 | 0 |
| `joint_return_/1` | (event id): event/status type marker | 15 | 55 |
| `last_day_year/2` | statute predicate; never defined in cases | 51 | 0 |
| `legal_separation_/1` | (event id): event/status type marker | 2 | 6 |
| `location_/2` | (event, place or location string); several per event allowed and semantically significant (F12) | 5 | 113 |
| `marriage_/1` | (event id): event/status type marker | 17 | 156 |
| `means_/2` | (payment, medium string or plan) | 10 | 13 |
| `medical_institution_/1` | (event id): event/status type marker | 0 | 1 |
| `medical_patient_/1` | (event id): event/status type marker | 1 | 4 |
| `migration_/1` | (event id): event/status type marker | 1 | 1 |
| `mother_/1` | (event id): event/status type marker | 1 | 3 |
| `nonresident_alien_/1` | (event id): event/status type marker | 5 | 14 |
| `nurses_training_school_/1` | (event id): event/status type marker | 2 | 1 |
| `patient/2` | declared without underscore; never read by any statute; inert if present | 0 | 2 |
| `patient_/2` | (event, participant | place | plan): the undergoer; for `service_` the employer, for `payment_` the recipient (or a plan), for `residence_` the household/place, for `enrollment_` the institution | 52 | 624 |
| `payment_/1` | (event id): event/status type marker | 6 | 259 |
| `penal_institution_/1` | (event id): event/status type marker | 1 | 2 |
| `plan_/1` | (event id): event/status type marker | 4 | 17 |
| `purpose_/2` | (event, purpose string | service | place); wildcard first argument occurs in two original cases (H2) | 24 | 230 |
| `reason_/2` | (termination event, reason event) | 1 | 10 |
| `residence_/1` | (event id): event/status type marker | 14 | 141 |
| `retirement_/1` | (event id): event/status type marker | 0 | 11 |
| `service_/1` | (event id): event/status type marker | 10 | 96 |
| `sibling_/1` | (event id): event/status type marker | 0 | 2 |
| `sister_/1` | (event id): event/status type marker | 1 | 3 |
| `son_/1` | (event id): event/status type marker | 2 | 72 |
| `start_/2` | (event, Day) | 106 | 1065 |
| `termination_/1` | (event id): event/status type marker | 1 | 5 |
| `type_/2` | (event, type string) | 9 | 4 |
| `unemployment_compensation_agreement_/1` | (event id): event/status type marker | 1 | 0 |

**H4 (stipulations, rules and grounding) [CONTRACT].** This resolves
Astra's B005.

* H4.1 (what a stipulation is). A case clause whose head is a statute
  predicate (`s…`, `total_wages_employer/6`) adds a clause *after* the
  statute's clauses (the case consults `init` first). In Prolog terms the
  predicate's solution list becomes `statute solutions ++ stipulated
  solutions`, in that order. The oracle implements exactly that: every statute
  predicate `p` is `p_statute h … ++ h.stipulations.filter p …` with wildcard
  positions matching anything and producing an unbound output (a `wild` value
  that is pairwise distinct from every other value, A3). 156 of 376 cases
  contain stipulations (203 fact clauses, 28 rule clauses, 31 signatures):

| Stipulated predicate | Fact clauses | Rule clauses | Wildcard positions | Files (by section prefix) |
| --- | ---: | ---: | --- | --- |
| `s63/3` | 60 | 0 | — | 60 (s1:60) |
| `s7703/4` | 26 | 0 | pos 2×2, pos 3×26 | 26 (s1:24, s68:2) |
| `s3306_b/8` | 20 | 0 | pos 2×4, pos 8×20 | 10 (s3306:10) |
| `s2_b/3` | 19 | 0 | pos 2×19 | 19 (s1:12, s63:3, s68:4) |
| `s2_a/3` | 19 | 0 | pos 2×19 | 19 (s1:11, s63:1, s68:7) |
| `s151_c_applies/3` | 1 | 14 | — | 15 (s151:1, s2:8, s7703:6) |
| `s152_c_1/3` | 8 | 0 | — | 6 (s151:2, s152:4) |
| `s3306_c/5` | 0 | 8 | — | 8 (s3306:8) |
| `s151/5` | 5 | 1 | pos 3×4, pos 4×5 | 6 (s2:1, s63:5) |
| `s151_d/4` | 5 | 0 | pos 2×4, pos 3×1 | 5 (s151:1, s152:4) |
| `s151_b_applies/3` | 5 | 0 | — | 5 (s63:5) |
| `s151_c/4` | 4 | 0 | pos 2×4 | 4 (s151:4) |
| `s151_b_applies/2` | 4 | 0 | — | 4 (s151:4) |
| `total_wages_employer/6` | 4 | 0 | pos 3×4, pos 4×4 | 2 (s3301:2) |
| `s68_b/3` | 2 | 0 | — | 2 (s151:2) |
| `s152_c_2/4` | 2 | 0 | — | 2 (s152:2) |
| `s152_c/3` | 1 | 1 | — | 2 (s152:1, s2:1) |
| `s152_b_2/4` | 2 | 0 | pos 2×2 | 2 (s2:2) |
| `s3306_a/2` | 0 | 2 | — | 2 (s3301:2) |
| `s63_c_1/3` | 2 | 0 | — | 2 (s63:2) |
| `s63_c_2/3` | 2 | 0 | — | 2 (s63:2) |
| `s63_c_3/3` | 2 | 0 | — | 2 (s63:2) |
| `s63_f_1_A/2` | 2 | 0 | — | 2 (s63:2) |
| `s63_f_1_B/3` | 2 | 0 | — | 2 (s63:2) |
| `s63_d/4` | 2 | 0 | pos 2×2 | 2 (s68:2) |
| `s152_c_3/3` | 0 | 1 | — | 1 (s152:1) |
| `s2_a/5` | 1 | 0 | pos 2×1, pos 3×1, pos 4×1 | 1 (s1:1) |
| `s152_d_2_H/6` | 0 | 1 | — | 1 (s2:1) |
| `s63_c/3` | 1 | 0 | — | 1 (s63:1) |
| `s63_c_3/4` | 1 | 0 | pos 2×1 | 1 (s63:1) |
| `s151_b/3` | 1 | 0 | — | 1 (s63:1) |

* H4.2 (grounding). Cases also define event facts by rules (59 files, 434
  rules, e.g. `payment_(E) :- bob_household_maintenance(_,E,_,_)`). The
  harness grounds a case by running it in the pinned interpreter and
  enumerating, in this order: (i) every unary event predicate to obtain the
  event universe; (ii) every binary event predicate with the event position
  bound to each event, collecting all solutions with multiplicity; (iii) every
  stipulated statute predicate with all positions unbound, keeping unbound
  outputs as wildcards. Step (ii) is what makes rules such as
  `amount_(P,5207) :- split_string(P,"_","",[X,Y,_]), …` (`tax_case_33.pl`)
  groundable: they raise `instantiation_error` when called with the event
  unbound and behave as facts when it is bound. A grounding that raises or
  fails to terminate is a finding.
* H4.3 (round-trip identity). Identity holds for a case iff (a) grounding the
  serialized Household again yields the same ordered fact list and
  stipulation list, and (b) every queried goal of the case (H6) has the same
  canonical solution set on the original file and on the serialized file.
  Byte identity of the source is not required and is impossible for the 59
  rule-bearing files.
* H4.4 (the two unterminated files). `s3306_c_2_neg.pl` and
  `s3306_c_2_pos.pl` are read by the harness with the full stop restored
  after line 26, and the `% Test` goal taken as the queried goal, recorded as
  a documented reader exception (F2). The alternative I rejected:
  both cases reported as "no executable test" and excluded from Week 1
  parity with the exclusion counted, never silently.
* H4.5 (duplicate `init` loads). `tax_case_37.pl` and `tax_case_86.pl` load
  `init` twice; reconsulting is idempotent in SWI, and grounding is unaffected.

**H5 (`Valid`) [CONTRACT].** `Valid : Household → Year → Prop`, `Decidable`.
The year index is needed because one reference-undefined region (V8) depends
on the taxable year; this changes the invariant form in PROTOCOL B004
(P-VALID-YEAR). All of the following must hold:

* V1 (well-formed). Every fact uses a declared predicate/arity (H3) with the
  argument kinds of H2; no wildcard anywhere; `stipulations = []`; every
  `Term` string is non-empty.
* V2 (money). Every `amount_` value `v` satisfies `0 ≤ v ≤ 10^9`.
* V3 (time). Every `Day` lies in 1900-01-01 … 2100-12-31; the year index
  `y` lies in 1900 … 2100.
* V4 (kinship acyclic, E3). The directed graph on persons with an edge
  `child → parent` for every `son_`/`daughter_` event (agent → patient) and
  every `father_`/`mother_` event (patient → agent), excluding self-edges,
  has no cycle.
* V5 (E1, `s3306_c_5_B`). No `service_` event `S` with `agent_(S,E)` and
  `patient_(S,P)` such that `E` is a child of `P` (`is_child_of(E,P)`) and
  `E` has a `birth_` event with a `start_` fact.
* V6 (E2, `s3306_b_2`). Every `plan_` event has at most one distinct
  `beneficiary_` value.
* V7 (E4, domestic cycle). Let `dom(S)` hold iff `S` is a `service_` with a
  `type_` or `purpose_` equal to `str "domestic service"`, a `location_` in
  {`"private home"`, `"local college club"`, `"local chapter of a college
  fraternity"`, `"local chapter of a college sorority"`} (strings), an `end_`
  fact, and `s3306_c_A(S) ∨ s3306_c_B(S)`. The relation `P ⇒ P'` iff some
  `payment_` `R` with `agent_(R,P)` and `purpose_(R,S)` has `dom(S)` and
  `patient_(S,P')` must be acyclic (in particular no `P ⇒ P`). This
  over-approximates the divergent region (a cycle whose service end years
  never coincide would terminate); the over-approximation is deliberate.
* V8 (E5, head-of-household cycle). `¬ hohCycle h t y` for every person `t`,
  where `hohCycle` is the decidable predicate "evaluating `s2_b_1_B(t,_,_,_,y)`
  reaches `s151_c(t,d,_,y)` with `s151_c_applies(t,d,y)` true, while
  `y ∉ [2018,2025]`, `s151_d_2(t,_,_,y)` has no solution, `s68_b_1_A(t,…)` has
  no solution, the `s2_b_1` not-married conjunct holds, `s2_a(t,_,y)` has no
  solution, and every `s2_b_1_A(t,…,y)` solution is rejected by `s2_b_3`".
  All sub-predicates named terminate under V4 and are the oracle's own
  definitions with the recursive call replaced by `[]`. A cruder year-free
  over-approximation ("no parent of any person has a `residence_` fact")
  would exclude every §2(b)(1)(B) input; I rejected it.
* V9 (dates well-formed for the interpreter). Implied by D1/V3; listed so the
  serializer's obligation (zero-padded ISO strings) is explicit.
* V10 (R5/R8, Option A). Each person is associated with at most one distinct
  `birth_` event identifier via `agent_`. Each `birth_` event has at most one
  distinct `start_` day. Distinctness is G4 tag-sensitive identity; repetitions
  of identical facts do not count as distinct events/days and are not deleted.
  These uniqueness requirements apply even if no eligible relationship exists.

  For every year `y` in 1900–2100, and every ground taxpayer/dependent pair
  `(t,d)` for which the original `s152_c_2(d,t,_,_)` and `s152_c_3(d,t,y)` both
  have a solution, require either:

  1. `d` has a birth event, `t` and `d` have defined unique birth dates, and
     `DOB(t) < DOB(d)`; or
  2. `d` has no birth event and is a strict descendant of `t` in the original
     `is_descendent_of(d,t,_,_)` relation.

  A birth event with no date is still a birth; it cannot use alternative 2.
  Include every permitted fact solution and applicable c2/c3 stipulation, not
  a selected birth or relationship witness. Self-transitions fail the strict
  decrease. Relationship/age eligibility must be computed independently of
  the recursive group and before the decrease restriction, never prefiltered
  to hide violating edges. The oracle retains source ordering and multiplicity;
  this universal check is termination evidence, not an observation change.


`Valid` includes V1–V10. `ValidStip` includes V2–V10 and the existing
stipulation-shape requirement, allowing the original stipulations and two
`purpose_` wildcards. V10 is included in **both** predicates, not hidden in V1.
Its fact uniqueness checks are executable in `Interface/`; the universal
original K/c3 decrease check is a required dependency with no default.
Its result must be true **if and only if** the quantified condition holds;
incomplete search is not permission to return false and narrow the domain.
Wildcard person stipulations require an exact decision, not an assumed finite
enumeration of all ground pairs. This is a representation obligation, not a
new input restriction.
No test instance establishes that production dependency's correctness.

**Stated domain limitations.** Multibirth persons, multi-date births and
same-birthday eligible dependent pairs are excluded from the graded domain.
The approved all-years check also rejects a household with a violating eligible
pair in any admitted year even if its outer query year would not expose it.
It does not ban unrelated people sharing a birthday. The retained pinned audit
found zero exclusions from the 376 originals under these proposed checks over
all 201 years; this is not full `ValidStip` certification or a parity result.
Both preserved R5 witnesses are rejected: equal-DOB strict-decrease failure and
multiple-birth uniqueness failure respectively.

**H6 (targets, observation, per-case accuracy) [CONTRACT].** PLAN Phase 2.3
speaks of one target per section, but the 376 cases query 135 distinct
predicate signatures (134 paragraph predicates plus `tax/3`), and per-case
accuracy (Phase 3.5, 4.3) is undefined for them under a single target. Resolution:

* H6.1 (targets). `Interface/S{N}.lean` declares one Lean target per queried
  predicate signature of section N (table below), typed by G1/G2 with the
  output positions as the result tuple, plus one *entry point* per section
  used by invariants, equivalence and mutation: §1 `s1 : Household → Person →
  Year → List (Int × Int)`; §2 `s2_a`, `s2_b : Household → Person → Year →
  Bool`; §63 `s63 : … → List Int`; §68 `s68 : Household → Person → Int → Year →
  List Int`; §151 `s151_a : … → List Int`; §152 `s152 : Household → Person →
  Person → Year → Bool`; §3301 `s3301 : … → List Int` (the tax); §3306
  `s3306_a : … → Bool`, `s3306_b`, `s3306_c` as list targets; §7703 `s7703 :
  Household → Person → Year → Bool`; utils `tax : Household → Person → Year →
  Int` (first solution; `tax/3` always has one). Scalar entry points for
  invariants are the *first* solution under G1 order, e.g.
  `s151_exemption h p y := (s151_a h p y).head?.getD 0`.
* H6.2 (observation and canonical form). For a target with inputs `I` the
  Prolog side computes `findall(O, T(I,O), L)`; both sides map each solution
  to JSON (`Int` → number, `atom s` → `{"a": s}`, `str s` → `{"s": s}`,
  `Day` → ISO string, unbound → `null`, Prolog lists → arrays) and the
  observation is the **sorted, deduplicated array** of solutions (solution
  *set*). Rationale: the case directives have existential semantics (a ground
  directive succeeds if *any* solution matches, and `s1_a_1_pos` depends on
  the second solution supplied by a stipulation), while exact multiplicity of
  duplicate solutions (`s2_a` yields the same tuple twice on some inputs) is
  not a property a formalization should be graded on. Evidence: of the 376
  case goals enumerated with `findall` under the pinned TZ
  (`evidence/sweep_all_solutions_ny.tsv`), 38 have between 2 and 64
  solutions and in every one of them all solutions are the same tuple;
  exhaustive enumeration of `tax/3` on `tax_case_83` and `tax_case_91` (six
  agricultural employees, many workdays) yields one solution but takes about
  two minutes of backtracking under emulation, against seconds for the first
  solution. Scalar entry points therefore
  observe the first solution only (H6.1) and the harness never enumerates
  `tax/3`. Multiplicity still matters *inside* the oracle wherever the source
  aggregates (A1); the internal lists are ordered and multiset-valued, the
  external observation is a set.
* H6.3 (per-case accuracy). A positive case passes iff the expected tuple
  (the ground values of the case goal in output positions, or "non-empty" if
  none) is in the observed set; a negative case passes iff it is not. The two
  cases with extra conjuncts (`s152_d_2_D_pos/neg`) evaluate the conjuncts on
  each observed tuple. The `tax_case_*` files test `tax/3` with a ground
  answer.
* H6.4 (models and stipulations). Model outputs are graded on
  stipulation-free inputs only (V1). Per-case accuracy on the originals is
  defined for the **stipulation-independent** subset: a case is
  stipulation-independent iff deleting its stipulation clauses leaves the
  observed solution set unchanged (decided mechanically by the harness in the
  pinned interpreter, recorded per case). The oracle is additionally checked
  on all 376 through H4.1. Alternative A, kept in reserve so that every
  original can count for models: paragraph targets take an explicit environment record of the
  other paragraph and section functions (`env : S{N}.Env`), the harness ties
  the knot with fuel and injects stipulations into `env`; models must then
  call sub-paragraphs through `env`. It is complete but costs every model a
  calling convention the statute text never mentions. Decision:
  stipulation-independent subset now; Alternative A only if the subset proves
  too small (the harness reports its size).
* H6.5 (queried targets). The 135 signatures with the modes the cases use;
  the oracle translator adds the statute-internal modes clause by clause
  (G2). A `b` in a position that the `% Question` text presents as the answer
  (e.g. the `4000` in `s151_a(alice,4000,2015)`) is an output position.

| Section | Queried predicate | Case modes (b = bound, f = free) | Cases | Extra conjuncts |
| --- | --- | --- | ---: | --- |
| §1 | `s1_a/4` | `bbfb`×4 | 4 |  |
| §1 | `s1_a_i/2` | `bb`×4 | 4 |  |
| §1 | `s1_a_ii/2` | `bb`×4 | 4 |  |
| §1 | `s1_a_iii/2` | `bb`×4 | 4 |  |
| §1 | `s1_a_iv/2` | `bb`×4 | 4 |  |
| §1 | `s1_a_v/2` | `bb`×4 | 4 |  |
| §1 | `s1_b/4` | `bbfb`×2 | 2 |  |
| §1 | `s1_b_i/2` | `bb`×2 | 2 |  |
| §1 | `s1_b_ii/2` | `bb`×2 | 2 |  |
| §1 | `s1_b_iii/2` | `bb`×2 | 2 |  |
| §1 | `s1_b_iv/2` | `bb`×2 | 2 |  |
| §1 | `s1_b_v/2` | `bb`×2 | 2 |  |
| §1 | `s1_c/4` | `bbfb`×2 | 2 |  |
| §1 | `s1_c_i/2` | `bb`×2 | 2 |  |
| §1 | `s1_c_ii/2` | `bb`×2 | 2 |  |
| §1 | `s1_c_iii/2` | `bb`×2 | 2 |  |
| §1 | `s1_c_iv/2` | `bb`×2 | 2 |  |
| §1 | `s1_c_v/2` | `bb`×2 | 2 |  |
| §1 | `s1_d/5` | `bfbfb`×2 | 2 |  |
| §1 | `s1_d_i/2` | `bb`×2 | 2 |  |
| §1 | `s1_d_ii/2` | `bb`×2 | 2 |  |
| §1 | `s1_d_iii/2` | `bb`×2 | 2 |  |
| §1 | `s1_d_iv/2` | `bb`×2 | 2 |  |
| §1 | `s1_d_v/2` | `bb`×2 | 2 |  |
| §2 | `s2_a_1_A/5` | `bfffb`×2 | 2 |  |
| §2 | `s2_a_1_B/4` | `bffb`×2 | 2 |  |
| §2 | `s2_a_2_A/5` | `bfffb`×2 | 2 |  |
| §2 | `s2_a_2_B/3` | `bfb`×2 | 2 |  |
| §2 | `s2_b_1/4` | `bffb`×2 | 2 |  |
| §2 | `s2_b_1_A/4` | `bffb`×2 | 2 |  |
| §2 | `s2_b_1_A_i/3` | `fbb`×2 | 2 |  |
| §2 | `s2_b_1_A_i_I/2` | `bb`×2 | 2 |  |
| §2 | `s2_b_1_A_i_II/3` | `bbb`×2 | 2 |  |
| §2 | `s2_b_1_A_ii/3` | `fbb`×2 | 2 |  |
| §2 | `s2_b_1_B/5` | `bfffb`×2 | 2 |  |
| §2 | `s2_b_2_A/5` | `bbffb`×2 | 2 |  |
| §2 | `s2_b_2_B/3` | `bfb`×2 | 2 |  |
| §2 | `s2_b_2_C/4` | `bffb`×2 | 2 |  |
| §2 | `s2_b_3_A/3` | `bbf`×2 | 2 |  |
| §2 | `s2_b_3_B/3` | `bfb`×1, `bbb`×1 | 2 |  |
| §63 | `s63_a/5` | `bbbff`×2 | 2 |  |
| §63 | `s63_b/4` | `bbbf`×2 | 2 |  |
| §63 | `s63_c_1/3` | `bbb`×2 | 2 |  |
| §63 | `s63_c_2_A_i/3` | `bfb`×2 | 2 |  |
| §63 | `s63_c_2_A_ii/2` | `bb`×2 | 2 |  |
| §63 | `s63_c_2_B/3` | `bbb`×2 | 2 |  |
| §63 | `s63_c_2_C/2` | `bb`×2 | 2 |  |
| §63 | `s63_c_3/3` | `bbb`×2 | 2 |  |
| §63 | `s63_c_5/5` | `bffbb`×2 | 2 |  |
| §63 | `s63_c_6_A/4` | `bffb`×2 | 2 |  |
| §63 | `s63_c_6_B/2` | `bb`×2 | 2 |  |
| §63 | `s63_c_6_D/2` | `bb`×2 | 2 |  |
| §63 | `s63_c_7_i/2` | `bb`×2 | 2 |  |
| §63 | `s63_c_7_ii/2` | `bb`×2 | 2 |  |
| §63 | `s63_d/4` | `bfbb`×2 | 2 |  |
| §63 | `s63_d_2/3` | `bbb`×2 | 2 |  |
| §63 | `s63_f_1_A/2` | `bb`×2 | 2 |  |
| §63 | `s63_f_1_B/3` | `bfb`×2 | 2 |  |
| §63 | `s63_f_2_A/2` | `bb`×2 | 2 |  |
| §63 | `s63_f_2_B/3` | `bfb`×2 | 2 |  |
| §63 | `s63_f_3/3` | `bbb`×2 | 2 |  |
| §68 | `s68_a_2/4` | `bfbb`×2 | 2 |  |
| §68 | `s68_b/3` | `bfb`×2 | 2 | yes |
| §68 | `s68_b_1_A/5` | `bfffb`×1, `bffbb`×1 | 2 |  |
| §68 | `s68_b_1_B/3` | `bbb`×2 | 2 |  |
| §68 | `s68_b_1_C/3` | `bfb`×1, `bbb`×1 | 2 |  |
| §68 | `s68_b_1_D/3` | `bbb`×2 | 2 |  |
| §68 | `s68_f/1` | `b`×2 | 2 |  |
| §151 | `s151_a/3` | `bbb`×2 | 2 |  |
| §151 | `s151_b/3` | `bbb`×1 | 1 |  |
| §151 | `s151_b/4` | `bbfb`×1 | 1 |  |
| §151 | `s151_c/4` | `bbfb`×2 | 2 |  |
| §151 | `s151_d_1/1` | `b`×2 | 2 |  |
| §151 | `s151_d_2/4` | `bfbb`×2 | 2 |  |
| §151 | `s151_d_3_A/7` | `bfffbbb`×2 | 2 |  |
| §151 | `s151_d_3_B/5` | `bbfbf`×2 | 2 |  |
| §151 | `s151_d_5/2` | `bb`×2 | 2 |  |
| §152 | `s152_a/5` | `bbbff`×2 | 2 |  |
| §152 | `s152_b_1/3` | `bfb`×2 | 2 |  |
| §152 | `s152_b_2/4` | `bfbb`×1, `bffb`×1 | 2 |  |
| §152 | `s152_c_1/3` | `bbb`×2 | 2 |  |
| §152 | `s152_c_1_B/6` | `bfbffb`×2 | 2 |  |
| §152 | `s152_c_1_E/3` | `bfb`×2 | 2 |  |
| §152 | `s152_c_2/4` | `bbff`×2 | 2 |  |
| §152 | `s152_c_2_A/5` | `bbfff`×2 | 2 |  |
| §152 | `s152_c_2_B/5` | `bbfff`×2 | 2 |  |
| §152 | `s152_c_3/3` | `bbb`×2 | 2 |  |
| §152 | `s152_d_1_B/2` | `bb`×2 | 2 |  |
| §152 | `s152_d_1_D/2` | `bb`×2 | 2 |  |
| §152 | `s152_d_2_A/4` | `bbff`×2 | 2 |  |
| §152 | `s152_d_2_B/4` | `bbff`×2 | 2 |  |
| §152 | `s152_d_2_C/4` | `bbff`×2 | 2 |  |
| §152 | `s152_d_2_D/4` | `bbff`×2 | 2 | yes |
| §152 | `s152_d_2_E/5` | `bbfff`×2 | 2 |  |
| §152 | `s152_d_2_F/5` | `bbfff`×2 | 2 |  |
| §152 | `s152_d_2_G/4` | `bbff`×2 | 2 | yes |
| §152 | `s152_d_2_H/6` | `bbbfff`×2 | 2 |  |
| §3301 | `s3301/6` | `bbfffb`×2 | 2 |  |
| §3306 | `s3306_a_1/2` | `bb`×2 | 2 |  |
| §3306 | `s3306_a_1_A/3` | `bbf`×2 | 2 |  |
| §3306 | `s3306_a_1_B/4` | `bffb`×2 | 2 |  |
| §3306 | `s3306_a_2_A/4` | `bbff`×2 | 2 |  |
| §3306 | `s3306_a_2_B/6` | `bffffb`×2 | 2 |  |
| §3306 | `s3306_a_3/4` | `bffb`×2 | 2 |  |
| §3306 | `s3306_b/8` | `fbbbbbbf`×1, `fbffffff`×1 | 2 |  |
| §3306 | `s3306_b_10_A/6` | `bbbbff`×1, `bfffff`×1 | 2 |  |
| §3306 | `s3306_b_10_B/3` | `bbf`×1, `fbf`×1 | 2 |  |
| §3306 | `s3306_b_11/3` | `bbf`×1, `bff`×1 | 2 |  |
| §3306 | `s3306_b_15/5` | `bbbbf`×1, `bffff`×1 | 2 |  |
| §3306 | `s3306_b_2_A/1` | `b`×2 | 2 |  |
| §3306 | `s3306_b_2_C/1` | `b`×2 | 2 |  |
| §3306 | `s3306_b_7/6` | `bbbbff`×1, `bfffff`×1 | 2 |  |
| §3306 | `s3306_c_1/2` | `bb`×2 | 2 |  |
| §3306 | `s3306_c_10_A/4` | `bbbb`×1 | 1 | yes |
| §3306 | `s3306_c_10_A_i/3` | `bbb`×1 | 1 |  |
| §3306 | `s3306_c_10_A_ii/3` | `bbb`×2 | 2 |  |
| §3306 | `s3306_c_10_B/4` | `bfbb`×2 | 2 |  |
| §3306 | `s3306_c_11/2` | `bf`×2 | 2 |  |
| §3306 | `s3306_c_13/4` | `bffb`×2 | 2 |  |
| §3306 | `s3306_c_16/2` | `bf`×2 | 2 |  |
| §3306 | `s3306_c_1_A_i/5` | `bfbfb`×2 | 2 |  |
| §3306 | `s3306_c_1_B/2` | `bf`×2 | 2 |  |
| §3306 | `s3306_c_2/3` | `bfb`×2 | 2 |  |
| §3306 | `s3306_c_21/4` | `bbfb`×2 | 2 |  |
| §3306 | `s3306_c_5/4` | `fbbb`×2 | 2 |  |
| §3306 | `s3306_c_6/1` | `b`×2 | 2 |  |
| §3306 | `s3306_c_7/2` | `bf`×2 | 2 |  |
| §3306 | `s3306_c_A/3` | `bff`×2 | 2 |  |
| §3306 | `s3306_c_B/4` | `fbbf`×1, `bfff`×1 | 2 |  |
| §7703 | `s7703_a_1/5` | `bfffb`×2 | 2 |  |
| §7703 | `s7703_a_2/5` | `bfffb`×2 | 2 |  |
| §7703 | `s7703_b_1/4` | `bffb`×2 | 2 |  |
| §7703 | `s7703_b_2/4` | `bbfb`×2 | 2 |  |
| §7703 | `s7703_b_3/4` | `bfbb`×2 | 2 |  |
| §utils | `tax/3` | `bbb`×100 | 100 |  |

---

---

## NAF

**N1 (semantics).** `\+ G` is `(solutionsOf G).isEmpty` evaluated after the
bindings established to its left (G1). Free variables inside `G` are
existential and never bound by the negation. Instantiation guards inside `G`
are resolved by mode (G2).

**N2 (optional-date pattern).** The 57 `N-ABS-DATE` sites all sit in a
disjunction `( \+ start_(E,_) ; start_(E,D) )` (or `end_`), sometimes with an
explicit default in the first branch. Translation: `startCandidates h E :
List (Option Day)` = `if (starts h E).isEmpty then [none] else (starts h
E).map some`, iterated in fact order; a site with an explicit default replaces
`none` by that value. The if-then-else variant `( \+ start_(E,_) -> default ;
start_(E,D) )` (`section152.pl:94-127`, `section2.pl:210-223`,
`section152.pl:353-359, 366-372, 378-384`) is the same list, except that
`( end_(E,X) -> test ; \+ end_(E,_) )` commits to the *first* `end_` fact.
Multiple `start_` facts for one event produce multiple candidates and hence
multiple solutions (a real corpus phenomenon: `tax_case_10.pl:38` gives one
event 101 start dates).

**N3 (attribute absence).** `N-ABS-ATTR`/`N-ABS-TAG` sites test that no fact
with the given first argument (and, for tags, the given *string* second
argument) exists; a tag written as an `atom` never satisfies the test (G4,
F3).

**N4 (negated calls).** `N-CALL` sites negate a statute predicate with some
positions free: compute the solution list in the mode with the bound
arguments and test emptiness. Never enumerate; never bind.

**N5 (negated conjunctions).** The 20 `N-CONJ` sites are spelled out
individually in the table because each encodes an interval or membership
condition; the year-long joint-return pattern (exact `start_ = Jan 1` and
`end_ = Dec 31` facts, 8 sites) is the most common.

**N6 (inventory).** All 150 sites:

| Site | Predicate | Construct | Intended translation |
| --- | --- | --- | --- |
| `section1.pl:27:5` | `s1_a_1/6` | `\+ ( % nonresident aliens can't file jointly nonresident_alien_(someone_is_nra), ( agent_(…` | N-CONJ. No nonresident-alien event whose agent is Taxp or Spouse and whose effective period [start (default Jan 1), end (default Dec 31)] overlaps the tax year (start ≤ Dec 31 ∧ Jan 1 ≤ end). Both defaults come from the inner N-ABS-DATE disjunctions; overlap test is closed on both ends. |
| `section1.pl:35:17` | `s1_a_1/6` | `\+ start_(someone_is_nra,_)` | N-ABS-DATE. `someone_is_nra` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section1.pl:42:17` | `s1_a_1/6` | `\+ end_(someone_is_nra,_)` | N-ABS-DATE. `someone_is_nra` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section1.pl:133:5` | `s1_c/4` | `\+ s2_a(Taxp,_,Taxy)` | N-CALL. `(s2_a …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section1.pl:134:5` | `s1_c/4` | `\+ s2_b(Taxp,_,Taxy)` | N-CALL. `(s2_b …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section1.pl:135:5` | `s1_c/4` | `\+ s7703(Taxp,_,_,Taxy)` | N-CALL. `(s7703 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section1.pl:174:5` | `s1_d/5` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), …` | N-CONJ. No joint-return event J with agent_(J,Taxp), agent_(J,Spouse), start_(J, Jan 1 Taxy) and end_(J, Dec 31 Taxy). Exact string match on the two dates (equality on Day values), not an interval test. |
| `section151.pl:20:13` | `s151/5` | `\+ ( s7703(Taxp,Spouse,_,Taxy), joint_return_(Joint_return), agent_(Joint_return,Taxp), ag…` | N-CONJ. Negation of the whole joint branch: ¬∃ Spouse (s7703 Taxp Spouse Taxy) with a year-long joint return (same exact-date pattern as section1.pl:174). Spouse ranges over the s7703 solution list. |
| `section151.pl:72:5` | `s151_b_applies/3` | `\+ ( % if a joint return is not made by the taxpayer and his spouse joint_return_(Joint_re…` | N-CONJ. Same exact joint-return pattern with Taxp and the already-bound Spouse. |
| `section151.pl:81:5` | `s151_b_applies/3` | `\+ s152(Spouse,_,Taxy)` | N-CALL. `(s152 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section151.pl:112:13` | `s151_d/3` | `\+ s151_d_2(Taxp,_,_,Taxy)` | N-CALL. `(s151_d_2 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section151.pl:113:13` | `s151_d/3` | `\+ s151_d_5(_,Taxy)` | N-CALL. `(s151_d_5 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section151.pl:118:21` | `s151_d/3` | `\+ s151_d_3(Taxp,Exemption_in,Ea,Taxy)` | N-CALL. `(s151_d_3 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section151.pl:169:13` | `s151_d_3_B/5` | `\+ ( % if a joint return is not made by the taxpayer and his spouse joint_return_(Joint_re…` | N-CONJ. Same exact joint-return pattern; the whole (s7703 ∧ ¬joint) condition is the `->` guard for the $1,250 step, committing to the first s7703 spouse. |
| `section152.pl:3:2` | `s152/3` | `\+ ( var(Dependent), var(Taxp) )` | N-MODE. Instantiation guard: succeeds iff at least one of Dependent, Taxp is bound. In Lean this is a mode split: the function is only ever called with Dependent bound or Taxp bound; the both-unbound call made by s152_b_1 inside s152 is translated as the constant empty solution list (see R-152). |
| `section152.pl:5:2` | `s152/3` | `\+ s152_b_1(Taxp,_,Taxy)` | N-CALL. `(s152_b_1 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section152.pl:7:2` | `s152/3` | `\+ s152_b_2(Dependent,_,_,Taxy)` | N-CALL. `(s152_b_2 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section152.pl:95:3` | `s152_c_1_B/6` | `\+ start_(Residence_individual,_)` | N-ABS-DATE. `Residence_individual` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section152.pl:103:3` | `s152_c_1_B/6` | `\+ end_(Residence_individual,_)` | N-ABS-DATE. `Residence_individual` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section152.pl:114:3` | `s152_c_1_B/6` | `\+ start_(Residence_taxpayer,_)` | N-ABS-DATE. `Residence_taxpayer` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section152.pl:122:3` | `s152_c_1_B/6` | `\+ end_(Residence_taxpayer,_)` | N-ABS-DATE. `Residence_taxpayer` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section152.pl:144:5` | `s152_c_1_E/3` | `\+ ( s7703(Dependent,Spouse,_,Taxy), joint_return_(Joint_return), agent_(Joint_return,Depe…` | N-CONJ. Dependent has no spouse (in the s7703 sense) with whom a year-long joint return (exact dates) exists. |
| `section152.pl:207:13` | `s152_c_3/3` | `\+ ( birth_(Someone_is_born), ( agent_(Someone_is_born,Dependent); agent_(Someone_is_born,…` | N-CONJ. No birth_ event whose agent is Dependent. The disjunction repeats `agent_(Someone_is_born,Dependent)` twice (source as written; Taxp is not tested). |
| `section152.pl:273:5` | `s152_d_1_D/2` | `\+ s152_c(Dependent,_,Taxy)` | N-CALL. `(s152_c …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section152.pl:347:5` | `s152_d_2_H/6` | `\+ ( marriage_(Marriage), agent_(Marriage,Dependent), agent_(Marriage,Taxp), start_(Marria…` | N-CONJ. No marriage M between Dependent and Taxp with start ≤ Dec 31 Taxy and (end present → end ≥ Jan 1 Taxy ; end absent). The inner `->` commits to the first end_ fact of M. |
| `section152.pl:358:4` | `s152_d_2_H/6` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section152.pl:371:3` | `s152_d_2_H/6` | `\+ end_(Taxpayer_residence,_)` | N-ABS-DATE. `Taxpayer_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section152.pl:383:3` | `s152_d_2_H/6` | `\+ end_(Individual_residence,_)` | N-ABS-DATE. `Individual_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:6:5` | `s2_a/3` | `\+ s2_a_2(Taxp,Spouse,Previous_marriage,Taxy)` | N-CALL. `(s2_a_2 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:30:13` | `s2_a_1_A/5` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:58:13` | `s2_a_1_B/4` | `\+ end_(Taxpayer_residence,_)` | N-ABS-DATE. `Taxpayer_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:73:13` | `s2_a_1_B/4` | `\+ end_(Dependent_residence,_)` | N-ABS-DATE. `Dependent_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:100:5` | `s2_a_2/4` | `\+ s2_a_2_B(Taxp,Spouse,Taxy)` | N-CALL. `(s2_a_2_B …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:117:5` | `s2_a_2_B/3` | `\+ ( % no joint return shall be made if either the husband or wife at any time during the …` | N-CONJ. No nonresident-alien event for Taxp or Spouse whose period overlaps the year: (start absent ∨ start ≤ Dec 31) ∧ (end absent ∨ Jan 1 ≤ end). |
| `section2.pl:125:17` | `s2_a_2_B/3` | `\+ start_(Someone_is_nra,_)` | N-ABS-DATE. `Someone_is_nra` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:135:17` | `s2_a_2_B/3` | `\+ end_(Someone_is_nra,_)` | N-ABS-DATE. `Someone_is_nra` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:149:5` | `s2_b/3` | `\+ s2_b_3(Taxp,Dependent,Taxy)` | N-CALL. `(s2_b_3 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:155:5` | `s2_b_1/4` | `\+ ( % "such individual is not married" marriage_(Marriage), agent_(Marriage,Taxp), agent_…` | N-CONJ. "Not married at close of year": no marriage M of Taxp with some Spouse ≠ Taxp, start ≤ Dec 31, such that [spouse has a death event and (s2_b_2_C holds for M ∨ death date > Dec 31)] ∨ [spouse has no death event and (end ≥ Jan 1 of Taxy+1 ∨ no end)], and ¬s2_b_2_A(any,any,any,M,Taxy) and ¬s2_b_2_B(Taxp,Spouse,Taxy). Translate the inner structure literally; the two inner NAFs are N-CALL over M and (Taxp,Spouse). |
| `section2.pl:176:17` | `s2_b_1/4` | `\+ ( death_(Spouse_dies), agent_(Spouse_dies,Spouse) )` | N-CONJ. Spouse has no death_ event at all (any date). |
| `section2.pl:188:25` | `s2_b_1/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:193:9` | `s2_b_1/4` | `\+ s2_b_2_A(_,_,_,Marriage,Taxy)` | N-CALL. `(s2_b_2_A …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:194:9` | `s2_b_1/4` | `\+ s2_b_2_B(Taxp,Spouse,Taxy)` | N-CALL. `(s2_b_2_B …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:196:5` | `s2_b_1/4` | `\+ s2_a(Taxp,_,Taxy)` | N-CALL. `(s2_a …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:215:9` | `s2_b_1_A/4` | `\+ start_(Taxpayer_residence,_)` | N-ABS-DATE. `Taxpayer_residence` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:222:9` | `s2_b_1_A/4` | `\+ end_(Taxpayer_residence,_)` | N-ABS-DATE. `Taxpayer_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:231:13` | `s2_b_1_A/4` | `\+ start_(Individual_residence,_)` | N-ABS-DATE. `Individual_residence` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:240:13` | `s2_b_1_A/4` | `\+ end_(Individual_residence,_)` | N-ABS-DATE. `Individual_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:259:5` | `s2_b_1_A_i/3` | `\+ ( s2_b_1_A_i_I(Dependent,Taxy), s2_b_1_A_i_II(Dependent,Taxp,Taxy) )` | N-CONJ. Not (Dependent is married under s7703 in Taxy AND Dependent has a year-long joint return with Taxp as the spouse via s152_b_2(Dependent,_,Taxp,Taxy)). |
| `section2.pl:293:13` | `s2_b_1_B/5` | `\+ end_(Parent_residence,_)` | N-ABS-DATE. `Parent_residence` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:345:13` | `s2_b_2_B/3` | `\+ start_(Spouse_is_nra,_)` | N-ABS-DATE. `Spouse_is_nra` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:354:13` | `s2_b_2_B/3` | `\+ end_(Spouse_is_nra,_)` | N-ABS-DATE. `Spouse_is_nra` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:369:5` | `s2_b_2_C/4` | `\+ s2_b_2_B(Taxp,Spouse,Taxy)` | N-CALL. `(s2_b_2_B …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:375:13` | `s2_b_2_C/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:403:13` | `s2_b_3_A/3` | `\+ start_(Taxpayer_is_nra,_)` | N-ABS-DATE. `Taxpayer_is_nra` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:414:13` | `s2_b_3_A/3` | `\+ end_(Taxpayer_is_nra,_)` | N-ABS-DATE. `Taxpayer_is_nra` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section2.pl:427:5` | `s2_b_3_B/3` | `\+ s152_b(Dependent,Taxp,Taxy)` | N-CALL. `(s152_b …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:428:5` | `s2_b_3_B/3` | `\+ s152_a_1(Dependent,Taxp,Taxy)` | N-CALL. `(s152_a_1 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section2.pl:431:5` | `s2_b_3_B/3` | `\+ ( ( s152_d_2_A(Dependent,Taxp,Start_relationship,End_relationship); s152_d_2_B(Dependen…` | N-CONJ. No relationship under s152_d_2 (A)–(G) between Dependent and Taxp whose Start is unbound or ≤ Jan 1 and whose End is unbound or ≤ Dec 31 (note: End ≤ Dec 31, not ≥; source as written). Unbound Start/End arise from kinship events without start_/end_ facts and are Option.none in Lean (D7). |
| `section3306.pl:24:5` | `s3306_a_1_is_wages/4` | `\+ purpose_(Service, "agricultural labor")` | N-ABS-TAG. No `purpose_` fact for `Service` whose second argument is the *string* "agricultural labor" (atom values never match, G4). |
| `section3306.pl:25:2` | `s3306_a_1_is_wages/4` | `\+ purpose_(Service, "domestic service")` | N-ABS-TAG. No `purpose_` fact for `Service` whose second argument is the *string* "domestic service" (atom values never match, G4). |
| `section3306.pl:45:5` | `s3306_a_1_is_day_of_employment/3` | `\+ purpose_(Service,"agricultural labor")` | N-ABS-TAG. No `purpose_` fact for `Service` whose second argument is the *string* "agricultural labor" (atom values never match, G4). |
| `section3306.pl:46:5` | `s3306_a_1_is_day_of_employment/3` | `\+ purpose_(Service,"domestic service")` | N-ABS-TAG. No `purpose_` fact for `Service` whose second argument is the *string* "domestic service" (atom values never match, G4). |
| `section3306.pl:47:5` | `s3306_a_1_is_day_of_employment/3` | `\+ type_(Service,"agricultural labor")` | N-ABS-TAG. No `type_` fact for `Service` whose second argument is the *string* "agricultural labor" (atom values never match, G4). |
| `section3306.pl:48:5` | `s3306_a_1_is_day_of_employment/3` | `\+ type_(Service,"domestic service")` | N-ABS-TAG. No `type_` fact for `Service` whose second argument is the *string* "domestic service" (atom values never match, G4). |
| `section3306.pl:228:4` | `s3306_a_3_is_wages/5` | `\+ means_(Remuneration,_)` | N-ABS-ATTR. No `means_` fact whose first argument is `Remuneration` (closed world over the fact list). |
| `section3306.pl:273:10` | `s3306_b/8` | `\+ means_(Remuneration,_)` | N-ABS-ATTR. No `means_` fact whose first argument is `Remuneration` (closed world over the fact list). |
| `section3306.pl:280:13` | `s3306_b/8` | `\+ plan_(Payee)` | N-ABS-ATTR. `Payee` is not the argument of any `plan_` fact. |
| `section3306.pl:298:2` | `s3306_b/8` | `\+ s3306_b_2(Remuneration,Employment,Payer,Payee,_,Plan)` | N-CALL. `(s3306_b_2 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:299:5` | `s3306_b/8` | `\+ s3306_b_7(Remuneration,Employment,Payer,Payee,_,_)` | N-CALL. `(s3306_b_7 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:300:2` | `s3306_b/8` | `\+ s3306_b_10(Remuneration,Employment,Payer,Payee,_,Plan)` | N-CALL. `(s3306_b_10 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:301:2` | `s3306_b/8` | `\+ s3306_b_11(Remuneration,Employment,_)` | N-CALL. `(s3306_b_11 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:302:5` | `s3306_b/8` | `\+ s3306_b_15(Remuneration,Employer,Payee,Employee,_)` | N-CALL. `(s3306_b_15 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:415:3` | `s3306_b_15/5` | `\+ end_(Emar,_)` | N-ABS-DATE. `Emar` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:440:2` | `s3306_c/5` | `\+ s3306_c_1(Service,Caly)` | N-CALL. `(s3306_c_1 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:441:2` | `s3306_c/5` | `\+ s3306_c_2(Service,_,Caly)` | N-CALL. `(s3306_c_2 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:442:2` | `s3306_c/5` | `\+ s3306_c_5(Service,Employer,Employee,Workday)` | N-CALL. `(s3306_c_5 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:443:2` | `s3306_c/5` | `\+ s3306_c_6(Service)` | N-CALL. `(s3306_c_6 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:444:2` | `s3306_c/5` | `\+ s3306_c_7(Service,_)` | N-CALL. `(s3306_c_7 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:445:2` | `s3306_c/5` | `\+ s3306_c_10(Service,Employer,Employee,Workday)` | N-CALL. `(s3306_c_10 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:446:2` | `s3306_c/5` | `\+ s3306_c_11(Service,Employer)` | N-CALL. `(s3306_c_11 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:447:2` | `s3306_c/5` | `\+ s3306_c_13(Service,Employer,Employee,Workday)` | N-CALL. `(s3306_c_13 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:448:2` | `s3306_c/5` | `\+ s3306_c_16(Service,Employer)` | N-CALL. `(s3306_c_16 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:449:2` | `s3306_c/5` | `\+ s3306_c_21(Service,Employee,_,Workday)` | N-CALL. `(s3306_c_21 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:458:13` | `s3306_c_A/3` | `\+ location_(Service,_)` | N-ABS-ATTR. No `location_` fact whose first argument is `Service` (closed world over the fact list). |
| `section3306.pl:468:13` | `s3306_c_A/3` | `\+ country_(Geographical_location,_)` | N-ABS-ATTR. No `country_` fact whose first argument is `Geographical_location` (closed world over the fact list). |
| `section3306.pl:483:13` | `s3306_c_B/4` | `\+ country_(Location,_)` | N-ABS-ATTR. No `country_` fact whose first argument is `Location` (closed world over the fact list). |
| `section3306.pl:487:2` | `s3306_c_B/4` | `\+ ( unemployment_compensation_agreement_(Agreement), agent_(Agreement,"usa"), agent_(Agre…` | N-CONJ. No unemployment_compensation_agreement_ event with agent_ "usa" (string) and agent_ Location. Location is whatever the preceding disjunction bound (possibly unbound → then any agreement with a "usa" agent and any second agent satisfies the conjunction). |
| `section3306.pl:504:2` | `s3306_c_1/2` | `\+ ( s3306_c_1_A(Service,_,Caly), s3306_c_1_B(Service,_) )` | N-CONJ. Not (s3306_c_1_A(Service,_,Caly) ∧ s3306_c_1_B(Service,_)); c_1_A requires Caly bound (nonvar guard) and c_1_B is itself a NAF. |
| `section3306.pl:544:21` | `s3306_c_1_A_i/5` | `\+ means_(Payment,_)` | N-ABS-ATTR. No `means_` fact whose first argument is `Payment` (closed world over the fact list). |
| `section3306.pl:575:2` | `s3306_c_1_B/2` | `\+ ( ( type_(Service,"agricultural labor"); purpose_(Service,"agricultural labor") ), citi…` | N-CONJ. Not (service is agricultural by type_ or purpose_ ∧ some employee-citizenship event with patient ≠ "usa" ∧ a migration_ event for that Employee with destination_ "usa" and purpose_ "agricultural labor"). Employee is unbound at the call site (s3306_c_1_B(Service,_)), so it ranges over all citizenship agents. |
| `section3306.pl:604:2` | `s3306_c_2/3` | `\+ s3306_a_3(Person,_,_,Caly)` | N-CALL. `(s3306_a_3 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section3306.pl:629:21` | `s3306_c_5_A/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:698:4` | `s3306_c_10_A_i/3` | `\+ end_(Student_is_enrolled,_)` | N-ABS-DATE. `Student_is_enrolled` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:707:4` | `s3306_c_10_A_i/3` | `\+ end_(Student_attends_classes,_)` | N-ABS-DATE. `Student_attends_classes` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:722:4` | `s3306_c_10_A_ii/3` | `\+ start_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:731:4` | `s3306_c_10_A_ii/3` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:754:4` | `s3306_c_10_B/4` | `\+ end_(Employee_is_medical_patient,_)` | N-ABS-DATE. `Employee_is_medical_patient` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:793:4` | `s3306_c_13/4` | `\+ end_(Student_is_enrolled,_)` | N-ABS-DATE. `Student_is_enrolled` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:802:4` | `s3306_c_13/4` | `\+ end_(Student_attends_classes,_)` | N-ABS-DATE. `Student_attends_classes` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section3306.pl:829:4` | `s3306_c_21/4` | `\+ end_(Person_goes_to_jail,_)` | N-ABS-DATE. `Person_goes_to_jail` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section63.pl:6:4` | `s63/3` | `\+ s63_b(Taxp,Taxy,_,_)` | N-CALL. `(s63_b …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:28:5` | `s63_b/4` | `\+ s63_d(Taxp,_,_,Taxy)` | N-CALL. `(s63_d …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:56:12` | `s63_c_1/3` | `\+ s63_c_6(Taxp,Taxy,_)` | N-CALL. `(s63_c_6 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:72:13` | `s63_c_1_A/3` | `\+ s63_c_5(Taxp,_,_,Taxy,_)` | N-CALL. `(s63_c_5 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:87:9` | `s63_c_2/3` | `\+ s63_c_2_B(Taxp,Taxy,_)` | N-CALL. `(s63_c_2_B …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:92:9` | `s63_c_2/3` | `\+ s63_c_2_A(Taxp,Taxy,_)` | N-CALL. `(s63_c_2_A …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:96:9` | `s63_c_2/3` | `\+ s63_c_2_A(Taxp,Taxy,_)` | N-CALL. `(s63_c_2_A …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:97:9` | `s63_c_2/3` | `\+ s63_c_2_B(Taxp,Taxy,_)` | N-CALL. `(s63_c_2_B …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:130:13` | `s63_c_2_B/3` | `\+ s63_c_7_i(Taxy,_)` | N-CALL. `(s63_c_7_i …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:139:9` | `s63_c_2_C/2` | `\+ s63_c_7_ii(Taxy,_)` | N-CALL. `(s63_c_7_ii …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:182:4` | `s63_c_6_A/4` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), …` | N-CONJ. Same exact year-long joint-return pattern for Taxp and Spouse. |
| `section63.pl:206:13` | `s63_c_6_B/2` | `\+ start_(Taxp_is_nra,_)` | N-ABS-DATE. `Taxp_is_nra` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section63.pl:215:13` | `s63_c_6_B/2` | `\+ end_(Taxp_is_nra,_)` | N-ABS-DATE. `Taxp_is_nra` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section63.pl:231:13` | `s63_c_6_D/2` | `\+ start_(Taxp_is_trust,_)` | N-ABS-DATE. `Taxp_is_trust` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section63.pl:240:13` | `s63_c_6_D/2` | `\+ end_(Taxp_is_trust,_)` | N-ABS-DATE. `Taxp_is_trust` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section63.pl:313:13` | `s63_f/3` | `\+ s63_f_3(Taxp,Taxy,_)` | N-CALL. `(s63_f_3 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:385:5` | `s63_f_3/3` | `\+ s7703(Taxp,_,_,Taxy)` | N-CALL. `(s7703 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section63.pl:386:5` | `s63_f_3/3` | `\+ s2_a(Taxp,_,Taxy)` | N-CALL. `(s2_a …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section68.pl:8:9` | `s68/4` | `\+ s68_f(Taxy)` | N-CALL. `(s68_f …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section68.pl:14:13` | `s68/4` | `\+ s68_a(Taxp,_,_,Amount_deductions_in,_,Taxy)` | N-CALL. `(s68_a …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section68.pl:86:5` | `s68_b_1_C/3` | `\+ s7703(Taxp,_,_,Taxy)` | N-CALL. `(s7703 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section68.pl:87:5` | `s68_b_1_C/3` | `\+ s2_a(Taxp,_,Taxy)` | N-CALL. `(s2_a …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section68.pl:88:5` | `s68_b_1_C/3` | `\+ s2_b(Taxp,_,Taxy)` | N-CALL. `(s2_b …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section68.pl:94:5` | `s68_b_1_D/3` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), …` | N-CONJ. Same exact year-long joint-return pattern for Taxp and Spouse. |
| `section7703.pl:9:2` | `s7703/4` | `\+ s7703_b(Taxp,Spouse,Taxy)` | N-CALL. `(s7703_b …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section7703.pl:14:2` | `s7703_a/4` | `\+ s7703_a_2(Taxp,Spouse,Marriage,_,Taxy)` | N-CALL. `(s7703_a_2 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `section7703.pl:30:13` | `s7703_a_1/5` | `\+ start_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section7703.pl:50:6` | `s7703_a_1/5` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section7703.pl:61:6` | `s7703_a_1/5` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section7703.pl:113:2` | `s7703_b_1/4` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), start_(Joint_return,First_day…` | N-CONJ. No joint-return event of Taxp (any co-agent) with start_ = Jan 1 and end_ = Dec 31 of Taxy (exact dates). |
| `section7703.pl:129:13` | `s7703_b_1/4` | `\+ end_(Child_lives_at_home,_)` | N-ABS-DATE. `Child_lives_at_home` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `section7703.pl:195:4` | `s7703_b_3_is_member_of_household/3` | `\+ end_(Spouse_lives_in_household,_)` | N-ABS-DATE. `Spouse_lives_in_household` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:48:17` | `latest/3` | `\+ is_before(Day,Latest)` | N-CMP. Both operands bound here: ¬(Day ≤ Latest) ⇔ Day > Latest. Together with the first branch this is max over bound entries. |
| `utils.pl:82:17` | `earliest/3` | `\+ is_before(Earliest,Day)` | N-CMP. ¬(Earliest ≤ Day) ⇔ Day < Earliest. Together with the first branch this is min over bound entries. |
| `utils.pl:120:13` | `is_child_of/4` | `\+ start_(Relationship,_)` | N-ABS-DATE. `Relationship` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:126:4` | `is_child_of/4` | `\+ end_(Relationship,_)` | N-ABS-DATE. `Relationship` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:147:13` | `is_sibling_of/4` | `\+ start_(Relationship,_)` | N-ABS-DATE. `Relationship` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:153:4` | `is_sibling_of/4` | `\+ end_(Relationship,_)` | N-ABS-DATE. `Relationship` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:176:13` | `is_stepsibling_of/4` | `\+ start_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:183:4` | `is_stepsibling_of/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:201:13` | `is_sibling_in_law_of_aux/4` | `\+ start_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:208:4` | `is_sibling_in_law_of_aux/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:222:13` | `is_child_in_law_of/4` | `\+ start_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:229:4` | `is_child_in_law_of/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:243:13` | `is_parent_in_law_of/4` | `\+ start_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `start_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:250:4` | `is_parent_in_law_of/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:266:4` | `is_stepparent_of/4` | `\+ end_(Marriage,_)` | N-ABS-DATE. `Marriage` has no `end_` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2). |
| `utils.pl:289:13` | `gross_income/3` | `\+ ( s7703(Person,Spouse,_,Year), joint_return_(Joint_return), agent_(Joint_return,Person)…` | N-CONJ. Negation of the joint-income branch: ¬∃ Spouse from s7703 with a year-long joint return (exact dates). |
| `utils.pl:337:13` | `tax/3` | `\+ s1(Taxp,Taxy,_,_)` | N-CALL. `(s1 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |
| `utils.pl:344:13` | `tax/3` | `\+ s3301(Taxp,Taxy,_,_,_,_)` | N-CALL. `(s3301 …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further). |

---

---

## Cut

Both cuts are in `s151_d_3_A/7` (`section151.pl:149-157`).

**C1 (`section151.pl:151:5`).** After `gross_income(Taxp,Taxy,Agi)`. The
call is deterministic on Valid inputs except for the choice of spouse in the
joint branch (`utils.pl:278`, first `s7703` solution with a year-long joint
return). Translation: take `head?` of the `gross_income` solution list; no
backtracking into it.

**C2 (`section151.pl:153:5`).** After `s68_b(Taxp,Aa,Taxy)`. Commits to the
*first* `s68_b` solution in clause order `s68_b_1_A` (joint return, then any
surviving spouse in the household — F10), `s68_b_1_B`, `s68_b_1_C`,
`s68_b_1_D`. Translation: `match (s68_b h taxp y).head? with | none => [] |
some aa => if agi > aa then … else []`. Because of the cuts, when `Agi > Aa`
fails the whole `s151_d_3_A` clause fails and no other `s68_b` alternative is
tried; `s151_d` then takes the `\+ s151_d_3` branch and returns the
unreduced amount. The cut is local to `s151_d_3_A`; callers (`s151_d_3`,
both the positive and the negated call in `s151_d`) see an ordinary
predicate.

---

---

## Aggregates

**A1 (`findall`).** The list of solutions of the goal in G1 order, one entry
per *solution* (not per distinct tuple), including duplicate solutions that
arise from several proofs of the same tuple (F12) and from duplicate facts
(F13). Free variables in the template that stay unbound (wildcards from
stipulations, `Workday` in `s3306_c`) become `wild` values, pairwise distinct
(SWI copies each solution with fresh variables; probed:
`list_to_set([(A,2000),(B,2000)])` keeps both).

**A2 (`sum_list`).** `List.sum` over `Int`; empty list is 0. (The schema's
`sumlist` does not occur; all 12 sites are `sum_list/2`, F14.)

**A3 (`list_to_set`).** Deduplicate by structural identity (`==`) keeping
the first occurrence and the order of first occurrences (probed:
`[(1,2),(1,2),(2,1)] → [(1,2),(2,1)]`; `[1.0,1]` stays two elements; a
wildcard is identical only to itself). Nine sites: `section151.pl:40,46`,
`section3301.pl:28`, `section3306.pl:69,80,161,185,196,214`.

**A4 (`append`).** Concatenation preserving order (`section151.pl:16,17,39,47`).

**A5 (`member` projections, `A-PROJ`).** `findall(X, member(pattern,L), Out)`
is `L.filterMap` in order with multiplicity; when the pattern has a bound
position (`member((Individual,Wage,_),…)`) it is the ordered sublist of
matching entries.

**A6 (`length`).** `length(L,N)` is `L.length`; `L>0` at `section63.pl:292`
requires a non-empty itemised list; `Num_days==0` at `section7703.pl:216`
requires an empty membership list.

**A7 (inventory).** All 43 `findall` sites and 12 `sum_list` sites:

| Site | Predicate | Construct | Duplicate and order decision |
| --- | --- | --- | --- |
| `section151.pl:34:5` | `s151_individual/5` | `findall( (Person,Exemption), s151_b(Taxp,Person,Exemption,Taxy), List_b )…` | A-SOL. Solution list of `s151_b/4` (spouse exemption): pairs (Spouse, Ea) in SLD order; stipulated s151_b/4 tuples follow the statute solutions (H4). |
| `section151.pl:41:5` | `s151_individual/5` | `findall( (Person,Exemption), s151_c(Taxp,Person,Exemption,Taxy), List_c )…` | A-SOL. Solution list of `s151_c/4` (dependent exemptions) in SLD order; stipulated tuples (possibly with wildcard Person) follow; wildcard outputs are pairwise distinct for the later `list_to_set` (A3). |
| `section151.pl:48:5` | `s151_individual/5` | `findall( Person, member((Person,_),List_all_exemptions), Person_list )…` | A-PROJ. First components of List_all_exemptions in order, multiplicity kept. |
| `section151.pl:53:5` | `s151_individual/5` | `findall( Exemption, member((_,Exemption),List_all_exemptions), Exemptions_list )…` | A-PROJ. Second components in order, multiplicity kept; summed by sum_list. |
| `section3301.pl:13:5` | `total_wages_employer/6` | `findall( (Individual,Wages,Service), ( s3306_b(Wages,Remuneration,Service,Employ…` | A-SOL. Every solution of `s3306_b` for payer = employer = Employer whose remuneration start lies in [Start_day, End_day]; one entry per *solution*, so a payment provable through k locations/countries or k `means_`/`patient_` alternatives appears k times (F12). |
| `section3301.pl:23:5` | `total_wages_employer/6` | `findall( Individual, member((Individual,_,_),Individuals_x_wages), Individual_li…` | A-PROJ. Individuals in order with multiplicity; deduplicated next by list_to_set (A3). |
| `section3301.pl:29:5` | `total_wages_employer/6` | `findall( (Individual,Total_wage), ( member(Individual, Individual_set), findall(…` | A-NEST. For each distinct individual (in first-occurrence order), the capped sum of all of that individual's wage entries (inner findall below). |
| `section3301.pl:33:13` | `total_wages_employer/6` | `findall( Wage, member((Individual,Wage,_),Individuals_x_wages), Individual_wages…` | A-PROJ. All wage entries of Individual, in order, multiplicity kept (so duplicates are summed). |
| `section3301.pl:43:5` | `total_wages_employer/6` | `findall( Wage, ( member(Individual,Individual_set), member((Individual,Wage),Ind…` | A-PROJ. Capped wage per individual in Individual_set order; `member((Individual,Wage),…)` yields exactly one entry per individual because Individuals_x_capped_wages was built from the set. |
| `section3301.pl:52:5` | `total_wages_employer/6` | `findall( Service, member((_,_,Service),Individuals_x_wages), Service_list )…` | A-PROJ. Service of every entry (multiplicity kept, so repeated services appear repeatedly); output only. |
| `section3306.pl:28:2` | `s3306_a_1_A/3` | `findall( Amount, ( s3306_a_1_is_wages(Employee, Caly, Remuneration, Amount); ( P…` | A-SOL. Amounts of non-agricultural, non-domestic wage solutions for Caly followed by those for Caly−1 (disjunction order); multiplicity per solution. |
| `section3306.pl:54:2` | `s3306_a_1_B/4` | `findall( (Stamp,Day,Individual), ( s3306_a_1_is_day_of_employment(Employer,Indiv…` | A-SOL. Triples (Stamp, Day, Individual) for every day-of-employment solution with Jan 1 of Caly−1 ≤ Day ≤ Dec 31 of Caly. From base facts this list is always empty (F4): the statute never binds Workday; only stipulated `s3306_c/5` tuples supply days. |
| `section3306.pl:64:5` | `s3306_a_1_B/4` | `findall( Stamp, member((Stamp,_,_),Stamp_day_individual), Emp_days )…` | A-PROJ. Stamps in order; deduplicated next by list_to_set (distinct days). |
| `section3306.pl:72:5` | `s3306_a_1_B/4` | `findall( Week, ( member(Stamp,Emp_days), format_time(atom(Week), "%W", Stamp) ),…` | A-DAYS. `%W` week label (D8) of every stamp in Emp_days (with multiplicity, deduplicated next). The label carries no year, so equal week numbers of Caly−1 and Caly collapse. |
| `section3306.pl:83:5` | `s3306_a_1_B/4` | `findall( Day, member((_,Day,_),Stamp_day_individual), Workday )…` | A-PROJ. Days in order (output only). |
| `section3306.pl:88:5` | `s3306_a_1_B/4` | `findall( Individual, member((_,_,Individual),Stamp_day_individual), Employee )…` | A-PROJ. Individuals in order (output only). |
| `section3306.pl:114:2` | `s3306_a_2_A/4` | `findall( (Amount,Service_), ( s3306_a_2_is_wages(Employer, Caly, Epay, Amount, S…` | A-SOL. (Amount, Service) of agricultural wage solutions for Caly then Caly−1; multiplicity per solution. |
| `section3306.pl:125:5` | `s3306_a_2_A/4` | `findall( Amount, member((Amount,_),Amount_service), Wageslist )…` | A-PROJ. Amounts in order, multiplicity kept, summed. |
| `section3306.pl:130:5` | `s3306_a_2_A/4` | `findall( Service_, member((_,Service_),Amount_service), Service )…` | A-PROJ. Services in order (output only). |
| `section3306.pl:140:2` | `s3306_a_2_is_day_of_employment/4` | `findall( (Employee,Service), ( s3306_c(Service,Person,Employee,Day,_), ( purpose…` | A-SOL. (Employee, Service) for every agricultural `s3306_c` solution on Day; from base facts this requires a bound Day and is empty when reached with Day unbound (F4). |
| `section3306.pl:151:5` | `s3306_a_2_is_day_of_employment/4` | `findall( Employee, member((Employee,_),Employee_x_service), Employees )…` | A-PROJ. Employees in order; deduplicated next by list_to_set. |
| `section3306.pl:156:5` | `s3306_a_2_is_day_of_employment/4` | `findall( Labor, member((_,Labor),Employee_x_service), Agricultural_labor )…` | A-PROJ. Services in order (output only). |
| `section3306.pl:169:2` | `s3306_a_2_B/6` | `findall( (Stamp,Day,Employees,Labor), ( s3306_c(_,Employer,_,Day,_), % narrow do…` | A-SOL. Day-level tuples; the leading `s3306_c(_,Employer,_,Day,_)` yields Day only from stipulated tuples (F4); the following `is_before` calls fail on an unbound Day, so base facts contribute nothing. |
| `section3306.pl:180:5` | `s3306_a_2_B/6` | `findall( Stamp, member((Stamp,_,_,_),Stamp_day_employees_labor), Stamp_list )…` | A-PROJ. Stamps; deduplicated next. |
| `section3306.pl:188:5` | `s3306_a_2_B/6` | `findall( Week, ( member(Stamp,Stamp_list), format_time(atom(Week), "%W", Stamp) …` | A-DAYS. `%W` labels (D8) with multiplicity; deduplicated next. |
| `section3306.pl:199:5` | `s3306_a_2_B/6` | `findall( Employees, member((_,_,Employees,_),Stamp_day_employees_labor), Employe…` | A-PROJ. Output only. |
| `section3306.pl:204:5` | `s3306_a_2_B/6` | `findall( Labor, member((_,_,_,Labor),Stamp_day_employees_labor), Service )…` | A-PROJ. Output only. |
| `section3306.pl:209:5` | `s3306_a_2_B/6` | `findall( Day, member((_,Day,_,_),Stamp_day_employees_labor), Days_list )…` | A-PROJ. Days; deduplicated next by list_to_set. |
| `section3306.pl:237:2` | `s3306_a_3/4` | `findall( (Amount,Service_), ( s3306_a_3_is_wages(Employer, Caly, Epay, Service_,…` | A-SOL. (Amount, Service) of domestic-service cash wage solutions for Caly then Caly−1; multiplicity per solution; reaching `s3306_b` here is where the E4 cycle starts when the service is a USA private-home domestic service. |
| `section3306.pl:248:5` | `s3306_a_3/4` | `findall( Amount, member((Amount,_),Amount_service), Wages_list )…` | A-PROJ. Amounts in order, summed. |
| `section3306.pl:253:5` | `s3306_a_3/4` | `findall( Service_, member((_,Service_),Amount_service), Service )…` | A-PROJ. Services (output only). |
| `section3306.pl:524:5` | `s3306_c_1_A_i/5` | `findall( (Amount,Employee_,Service_), ( payment_(Payment), agent_(Payment,Employ…` | A-EV. (Amount, Employee, Service) for every payment by Employer to an employee for an agricultural service, dated in [Jan 1 Caly−1, Dec 31 Caly], paid in cash or with no means_ fact; one entry per fact-combination (a payment with two `purpose_` links or two `amount_` facts appears twice). |
| `section3306.pl:551:5` | `s3306_c_1_A_i/5` | `findall( Amount, member((Amount,_,_),Amounts_employee_service), Amounts )…` | A-PROJ. Amounts in order, summed. |
| `section3306.pl:558:5` | `s3306_c_1_A_i/5` | `findall( Individual, member((_,Individual,_),Amounts_employee_service), Employee…` | A-PROJ. Output only. |
| `section3306.pl:563:5` | `s3306_c_1_A_i/5` | `findall( Service_, member((_,_,Service_),Amounts_employee_service), Service )…` | A-PROJ. Output only. |
| `section63.pl:274:2` | `s63_d/4` | `findall( (Amount,Deduction), ( deduction_(Deduction), agent_(Deduction,Taxp), am…` | A-EV. (Amount, Deduction) for every deduction_ event with agent Taxp, an amount_ fact and a start_ in [Jan 1, Dec 31] of Taxy; one entry per (amount_ fact × start_ fact) combination. |
| `section63.pl:286:2` | `s63_d/4` | `findall( Amount, member((Amount,_),Amount_deduction), Amounts )…` | A-PROJ. Amounts in order, summed; `length > 0` requires at least one entry (an empty itemised list makes s63_d fail, so s63_b applies). |
| `section63.pl:294:2` | `s63_d/4` | `findall( Deduction, member((_,Deduction),Amount_deduction), Itemded )…` | A-PROJ. Deduction ids in order (output; observed as a list, order and multiplicity kept). |
| `section7703.pl:143:5` | `s7703_b_2/4` | `findall( Payment_amount, ( payment_(Payment), residence_(Residence), agent_(Paym…` | A-EV. Amounts of payments by Taxp whose purpose is a residence event at Household or the Household itself, and whose start_ date has year == Taxy; one entry per (residence_ × purpose_ × amount_ × start_) combination, so a household with r residence events at the same place multiplies each payment r times in *both* sums (ratio unaffected, Cost > 0 unaffected). |
| `section7703.pl:162:2` | `s7703_b_2/4` | `findall( Payment_amount, ( payment_(Payment), residence_(Residence), patient_(Re…` | A-EV. Same as the previous site without the agent restriction (all payers). |
| `section7703.pl:205:5` | `s7703_b_3/4` | `findall( Day_offset, ( between(2,185,Day_offset), date_time_stamp(date(Taxy,7,Da…` | A-DAYS. The 184 window days (D8: Jul 1 … Dec 31 under the pinned TZ) on which the spouse's residence at Household is ongoing (start ≤ day ∧ (end absent ∨ day ≤ end)); one entry per (day × residence event) solution; only the emptiness of the list is used. |
| `utils.pl:304:5` | `gross_income_individual/3` | `findall( Amount, ( income_(Income), agent_(Income,Person), amount_(Income,Amount…` | A-EV. Amounts of income_ events of Person with start_ in [Jan 1, Dec 31]; one entry per (amount_ × start_) fact combination (duplicate facts double-count, F13). |
| `utils.pl:316:5` | `gross_income_individual/3` | `findall( Amount, ( payment_(Payment), patient_(Payment,Person), amount_(Payment,…` | A-EV. Amounts of payment_ events with patient Person and start_ in the year; same multiplicity rule. |

| Site | Predicate | Construct | Decision |
| --- | --- | --- | --- |
| `section151.pl:58:5` | `s151_individual/5` | `sum_list(Exemptions_list,S2)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section3301.pl:38:13` | `total_wages_employer/6` | `sum_list(Individual_wages,Wage_sum)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section3301.pl:51:5` | `total_wages_employer/6` | `sum_list(Capped_wages,Total_wages)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section3306.pl:39:2` | `s3306_a_1_A/3` | `sum_list(Wages_list,Wages)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section3306.pl:135:2` | `s3306_a_2_A/4` | `sum_list(Wageslist,Wages)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section3306.pl:258:2` | `s3306_a_3/4` | `sum_list(Wages_list,Wages)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section3306.pl:556:5` | `s3306_c_1_A_i/5` | `sum_list(Amounts,Remuneration)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section63.pl:293:2` | `s63_d/4` | `sum_list(Amounts,Total_amount)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section7703.pl:180:2` | `s7703_b_2/4` | `sum_list(Payments_by_individual,Payment_by_individual)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `section7703.pl:181:2` | `s7703_b_2/4` | `sum_list(Payments_all,Cost)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `utils.pl:328:5` | `gross_income_individual/3` | `sum_list(Income_amounts,Income)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |
| `utils.pl:329:5` | `gross_income_individual/3` | `sum_list(Payment_amounts,Payment)` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |

---

---

## Recursion

The lexical dependency analysis finds six direct and four mutual recursion
groups. Termination strategy per group; the gate forbids `partial`, so every
recursive definition takes an explicit measure or fuel.

**R1 `is_descendent_of/4` (`utils.pl:158-165`).** Recursion descends through
`is_child_of(Z,Y)` from the ancestor. Structural bound: the number of persons
in the Household. Translate with `fuel := persons.length + 1` decremented per
call; on Valid inputs (V4) fuel is never exhausted. Solution order: the direct
child first, then recursively for each child in fact order.

**R2 `latest/2,3`, `earliest/2,3` (`utils.pl:25-90`).** Structural on the
list; total.

**R3 `amount/2` (`section68.pl:52-60`).** `amount("D")` calls `amount("A")`;
not a true recursion. Translate as four constants (300000, 275000, 250000,
150000).

**R4 `s152/3 ↔ s152_b_1/3` (`section152.pl:2-7, 38-39`).** Bounded by the
instantiation guard: `s152(D,T,Y)` calls `s152_b_1(T,_,Y)`, which calls
`s152(T,O,Y)` with `O` unbound, whose own `\+ s152_b_1(O,_,Y)` calls
`s152(O,_,Y)` with both unbound and fails at the guard. Translate as two
functions: `s152_full h d t y` (both bound; performs the (b)(1) check) and
`s152_b1 h t y := !(s152_a_solutions h t y).isEmpty && !(s152_b_2 h t y)` which
performs no (b)(1) check on the found taxpayer (the `Dependent \== Taxp` test
is vacuous there because `Otaxp` is unbound, G3). No fuel needed.

**R5 `s152_a_1 → s152_c → s152_c_1 → s152_c_1_E → s7703 → s7703_b →
s7703_b_1 → s152_a_1`.** The original child-descent argument is false:
`s152_c_2` admits symmetric sibling/stepsibling relations not constrained by V4.
Use Option A's V10 and prove each actual contracted transition is among its
eligible pairs. In the born phase the unique DOB strictly increases; a
transition into a birthless person cannot return to a born person. The birthless
phase follows strict descendant paths in the V4 DAG. An undated birth can start
only a birthless suffix. Thus the proposed measure has no repeated person on a
branch. The finite universe must contain every possible participant from facts,
stipulations and bound query arguments; its completeness must be proved.

For universe size `N`, derive the proposed `N+1` branch-depth counter from the
at-most-`N−1` contracted transitions, with an explicit finite phase ordering
between transitions. Decrement once on crossing the successful c1 A/B/C prefix
into c1E and its recursive continuation. This is not a mutable global budget:
sequential calls and backtracking alternatives do not spend one shared counter.
Fresh independent invocations use the full bound; descendants never reset it.
Check entry/wrapper offsets and every approved mode before certifying the
constant. No `2·persons+2` bound or birthday-function assumption is reinstated.

**Query-year coverage is a prerequisite, not a claim.** V10 checks the single
shared `r5Years` population, 1900–2100. All root years and actual Workdays,
including query- and stipulation-supplied arguments, must be checked at the
shared Interface boundary. R8 uses Workday's actual civil year, not an enclosing
taxable year. Wrappers must consume a certificate tied to that actual argument;
no total default/cast may manufacture coverage. A failed check is a reported
coverage/domain error, never a reference answer. Prove that every admitted
operational call is covered, including the existing E2 unbound-year exclusion,
before claiming R5-group termination. A standalone checked type does not prove
that all call sites use it.

The nonrecursive K/c3 definitions, stipulated solutions, structural descendant
correspondence, all call modes, absence of exceptions, universe coverage, cycle
cut and fuel adequacy still require kernel-checked proofs. This amendment
authorizes that work; it does not declare it complete.

**R6 `s151_c → s151_d → s151_d_3 → s151_d_3_A → s68_b → s68_b_1_B → s2_b →
s2_b_1 → s2_b_1_B → s151_c`.** Re-enters `s151_d` with identical arguments;
terminates only when the path is not taken (F6). Valid excludes the divergent
region (V8). Translate with a group fuel of `persons.length + 2`; exhaustion
returns `[]`, which on Valid inputs is unreachable. (`s2_b_1_A` never
re-enters: it calls `s151_b_applies`/`s151_c_applies`, which go to `s152` and
not to `s151_d`.)

**R7 `s3306_b → s3306_c → s3306_c_2 → s3306_a_3 → s3306_a_3_is_wages →
s3306_b`, plus `s3306_b → s3306_b_{2,7,10,15} → s3306_c` and `s3306_c_1 →
s3306_c_1_A → s3306_c_1_A_ii → s3306_a_2_B → s3306_c`.** The `s3306_c_1`
branch is bounded by the `nonvar(Caly)` guard (`section3306.pl:513`): the
inner `s3306_c(_,Employer,_,Day,_)` call leaves `Caly` unbound, so
`s3306_c_1_A` fails and no further recursion occurs (this is also why F4
holds). The `s3306_c_2` branch is the E4 cycle, excluded by V7. Fuel for the
group: `services.length + payments.length + 2`.

**R8 `s3306_c_10_A_ii → s7703 → s7703_b_1 → s152_a_1 → … → s7703`.** Use the
re-derived R5 discipline with the year extracted from the actual Workday's D1
ISO prefix. Check query/stipulation Workdays as well as fact-derived ones.
A fresh independent group invocation receives its full depth counter, and a
recursive descendant does not reset it. Coverage and adequacy proofs are
required; referring to R5's old fuel assertion does not discharge them.

**R9 (what fuel exhaustion means).** Fuel exhaustion is never a reference value
on an admitted input. It is a design/adequacy failure and must halt and be
reported, not be graded as `[]`, `false`, `null`, a mismatch or a successful
answer. A total Lean definition may have an outside-premise branch; that does
not give reference-undefined inputs a reference answer. G6 excludes them through
the approved validity premise, not by assigning an oracle value. For every
group, an unreachable-exhaustion assertion on admitted inputs requires the
adequacy proof; a bounded runtime probe or unproved invariant is not that proof.

---

---

## Axioms

**X1.** The whitelist is `propext`, `Quot.sound`, `Classical.choice`.
Confirmed: it is what `#print axioms` reports for proofs by `decide`, `simp`,
`omega` and `grind` over `Int`/`List` definitions written without
`Classical` opens; `Decidable` instances derived by `deriving DecidableEq` or
`inferInstance` on structures of `Int`, `String`, `Option` and `List` do not
add axioms. Anything else (`sorry`-free or not) is INVALID at the gate.

---

---

## Source hazard inventory

The tables in Money, Dates, NAF, Cut and Aggregates are the inventory. Counts by file
(from `docs/contracts/HAZARDS.json`, unchanged): 150 `\+`, 2 `!`, 43
`findall`, 12 `sum_list`, 0 `sumlist`, 101 `is`, 103 `is_before`, 18
`earliest`, 15 `latest`, 2 duration comparisons, 1 `@>`. Each site id
(`file:line:col`) is the key Astra's `-- NAF`, `-- CUT`, `-- AGG` annotations
must cite; Checkpoint 1 checks that every id in these tables appears exactly
once in `Oracle/`.

Sites without a hazard tag that nevertheless carry a decision:
`section3306.pl:292` (`end_` required, F18); `section3306.pl:428` (`Workday`
never bound, F4); `section68.pl:75` (unbound surviving spouse, F10);
`section2.pl:419` (self-unifying `earliest`, F11); `section151.pl:69`
(`s151_b_applies/2` is unconditionally true, so every taxpayer receives the
personal exemption); `section3306.pl:265` (`s3306_a_4()` with zero
arguments is a syntactically odd but harmless fact); `section63.pl:358`
(F17).

---

### Source findings

Findings established during the inventory; F1, F2 and F14 changed contracts (see `docs/DECISION_LOG.md`).

| Id | Finding | Where | Consequence |
| --- | --- | --- | --- |
| F1 | The reference program's answers depend on the process time zone. Under `TZ=America/New_York` all 376 case directives succeed. Under UTC, Europe/Amsterdam and Asia/Tokyo two fail (`s3306_a_1_B_neg`, `s3306_a_2_B_neg`), because `format_time/3` renders UTC-midnight stamps in local time. | `utils.pl:2-8`, `section7703.pl:209-210`, `section3306.pl:76,192` | **[CONTRACT]** RUNTIME must pin `TZ=America/New_York` (D8). Under that pin the "+1 day" in `day_to_stamp` is undone for every `format_time` observation. See P-TZ in the decision log. |
| F2 | `s3306_c_2_neg.pl:26` and `s3306_c_2_pos.pl:26` lack a full stop, so the intended `s3306_b/8` fact becomes a rule whose body is the intended test, and the files have no test directive. Grounding that rule diverges (E4-shaped recursion through `\+ s3306_c_2 → s3306_a_3 → s3306_b`). | cases | H4.4: read the two files with the terminator restored inside the harness reader (documented, never in `human/`), the rejected alternative was to exclude them as a finding. |
| F3 | Atom versus string. `location_(alice_employer,usa)` (atom) never matches `Geographical_location=="usa"` (string), so `s3306_c_A` fails for the 3306 cases written with atom locations; those cases only pass through their stipulated `s3306_b/8` facts. | `section3306.pl:459-470`, e.g. `s3306_c_2_pos.pl:17` | Household must keep the atom/string distinction (G4, H2). |
| F4 | The statute never binds `Workday` in `s3306_c/5` (line 428 leaves it unbound). Therefore `s3306_a_1_B`, `s3306_a_2_B`, `s3306_a_2_is_day_of_employment` and `s3306_c_1_A_ii` have no solutions from base facts; they succeed only through stipulated `s3306_c/5` tuples. Probed: `s3306_a_1_B(boss,_,_,2017)` yields 0 solutions with a full-year service and payment. | `section3306.pl:424-449, 50-92, 165-214, 570-571` | The "10 days in 10 weeks" arms are unreachable in the generated corpus. Coverage ≥ 20 hits per arm (Week 2 gate) is impossible for them; report, do not manufacture inputs. |
| F5 | Non-termination E4: a domestic service in a private home (or the other three locations) whose service passes `s3306_c_A`/`s3306_c_B` and that the employer paid for makes `s3306_c_2 → \+ s3306_a_3 → s3306_b → s3306_c → \+ s3306_c_2 …` recurse until `resource_error(stack)`. Probed with `location_(S,"private home"), location_(S,"usa")`. | `section3306.pl:441, 604, 220, 295` | Valid must exclude the cycle (V-DOM). §3306(c)(2) and (a)(3) are only evaluable through stipulation. |
| F6 | Non-termination E5: an unmarried taxpayer with no own `residence_` at the household but a parent living there and a qualifying deduction recurses `s2_b_1_B → s151_c → s151_d → s151_d_3_A → s68_b → s68_b_1_B → s2_b → s2_b_1 → s2_b_1_B …` (stack overflow; probed). Years 2018–2025 escape via `s151_d_5`. | `section2.pl:309`, `section151.pl:100,116,152`, `section68.pl:81` | Valid must exclude the cycle (V-HOH). |
| F7 | Non-termination E3: any cycle in the child relation (`son_`/`daughter_`/`father_`/`mother_` events) makes `is_descendent_of` overflow the stack whenever the cycle is reachable from the queried ancestor. | `utils.pl:158-165` | Valid requires an acyclic child graph (V-KIN). |
| F8 | Type error E1: `s3306_c_5_B` computes `Dob_d+7671` on a two-character string and raises `type_error` whenever it is reached (employee is a child of the employer, has a `birth_` event with a `start_`, and `s3306_c_5_A` fails). The exception propagates out of `s3306_c` and every caller. | `section3306.pl:649-654` | §3306(c)(5)(B) is never evaluable; Valid excludes the trigger (V-STR). |
| F9 | Instantiation error E2: `s3306_b_2` calls `s152(Payee,Employee,_)` with the year unbound; whenever `Payee ≠ Employee` this reaches `first_day_year(_,_)` and raises. Reached for plan payments whose beneficiary is not the employee. | `section3306.pl:317`, `section152.pl:97,129,345` | Valid excludes the trigger (V-PLAN). |
| F10 | `s68_b_1_A` is called as `s68_b_1_A(Taxp,_,_,Aa,Taxy)`, so its `s2_a(Surviving_spouse,_,Taxy)` branch has the taxpayer unbound: any surviving spouse in the household gives every taxpayer the $300,000 applicable amount as the *first* `s68_b` solution. Probed: unrelated `zed` gets `[300000,300000,250000]`. Because of the cut at `section151.pl:153`, the phase-out uses that first value. | `section68.pl:75`, `section151.pl:152-153` | Translate literally; note it for the paper. |
| F11 | `s2_b_3_A` with `earliest([S119,Stop_nra],S119)`: a nonresident-alien event with both a start and an end inside the year *fails* (probed), one with only a start succeeds with Dec 31, one with only an end succeeds with Jan 1. | `section2.pl:396-421` | Translate literally (D7.3). |
| F12 | Solution multiplicity is observable. A service with three matching `location_`/`country_` facts yields three `s3306_c` solutions, three `s3306_b` solutions, and `total_wages_employer` sums the payment three times (probed: 5000 → 15000 → capped 7000). | `section3306.pl:455-471`, `section3301.pl:13-22` | Aggregates must count solutions, not tuples (A1, A-SOL). |
| F13 | Duplicate facts count twice: two identical `amount_(inc1,100)` facts give gross income 200 (probed). `tax_case_16` and `tax_case_41` contain duplicated fact blocks. | `utils.pl:304-330` | Household is a list, not a set (H1). |
| F14 | The schema says `sumlist`; the source has 12 `sum_list/2` and no `sumlist`. | all aggregate sites | Rename the schema heading target; no semantic change. |
| F15 | The 376-directive sweep succeeds 376/376 only with F1's TZ. The two `s3306_c_2` files count as "success" because they execute no test at all. | cases | Week 1 parity must evaluate the intended queries (H6), not the files' directives. |
| F16 | `s152_c_3` line 207-212 negates `birth_` of `Dependent` twice (the second disjunct repeats `Dependent`; `Taxp` is never tested). | `section152.pl:207-213` | Translate as written. |
| F17 | `s63_f_2` sets `Count2 is 600` for a blind spouse; the count is then multiplied by the amount, adding 600 × 600 (or 600 × 750) dollars to the standard deduction. | `section63.pl:358` | Translate as written; report. |
| F18 | Only `s3306_b` requires the service to have an `end_` fact (line 292); a service without one yields no wages anywhere. | `section3306.pl:292-295` | Translate as written; generators should include end-less services deliberately. |

---

---

## Verification record

Items I still intend to re-confirm; none blocks the decisions above:

1. That the probes in `docs/consult/evidence/` reproduce on the runner with
   the same image id (`de470fb4c535`) and that `TZ=America/New_York` yields
   376/376 (`evidence/sweep_directives_ny.tsv`); the TZ pin is the single
   most consequential decision here, and it rests on the assumption that the
   SARA authors' machine ran in US Eastern time.
2. That the observation is the solution *set* (H6.2) and not the ordered
   multiset; the oracle reproduces order either way, the meter compares sets.
3. The size of the stipulation-independent subset (H6.4) once the harness
   computes it.
4. That F4 (unreachable "10 days" arms) stays a reported coverage gap rather
   than a reason to redesign the generator.
5. The assumption running through every table: the pinned interpreter's
   behaviour on Valid inputs is what the probes show for the specific inputs
   probed; the bulk rounding check (M2, M4) covers the money range only up to
   the sampled bounds, and the analytic argument covers the rest.
