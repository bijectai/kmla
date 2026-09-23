# Approved Option A — protected-contract installation text

Dev selected A on 2026-09-22, with query-year coverage required before any R5
termination claim and generator prohibition of multibirth persons, multi-date
births and same-birthday eligible pairs. Dev accepted the same-birthday exclusion
as a stated limitation. Neither A nor WIRE signs off Checkpoint 1.

This is exact text for the owner to install in `human/DECISIONS.md` and then
re-pin. The builder has not modified `human/` or the manifest. The existing R5
argument and A-009's withdrawn V10/`2·persons+2` must not remain operative.
The approved option is preserved in `P_R5CYCLE_OPTIONS_DRAFT.md`, including its
complete evidence and qualifications. This amendment does not certify a proof.

## H5 — append after V9; replace the Valid/ValidStip summary

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

## Replace R5

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

## Replace R8

**R8 `s3306_c_10_A_ii → s7703 → s7703_b_1 → s152_a_1 → … → s7703`.** Use the
re-derived R5 discipline with the year extracted from the actual Workday's D1
ISO prefix. Check query/stipulation Workdays as well as fact-derived ones.
A fresh independent group invocation receives its full depth counter, and a
recursive descendant does not reset it. Coverage and adequacy proofs are
required; referring to R5's old fuel assertion does not discharge them.

## Replace R9

**R9 (what fuel exhaustion means).** Fuel exhaustion is never a reference value
on an admitted input. It is a design/adequacy failure and must halt and be
reported, not be graded as `[]`, `false`, `null`, a mismatch or a successful
answer. A total Lean definition may have an outside-premise branch; that does
not give reference-undefined inputs a reference answer. G6 excludes them through
the approved validity premise, not by assigning an oracle value. For every
group, an unreachable-exhaustion assertion on admitted inputs requires the
adequacy proof; a bounded runtime probe or unproved invariant is not that proof.
