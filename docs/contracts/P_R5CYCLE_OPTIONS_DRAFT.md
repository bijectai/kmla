# P-R5CYCLE — owner-choice draft, no recommendation

**Selected by Dev, 2026-09-22: A**, with query-year coverage required before any
R5-group termination proof claim and generator prohibition of multibirth persons,
multi-date births and same-birthday eligible pairs. The same-birthday exclusion
is an accepted stated limitation. Neither this selection nor WIRE signs off
Checkpoint 1. The original proposal/evidence below is preserved as history;
`DECISIONS_R5_A_AMENDMENT.md` is the protected installation text for Dev.

**A excludes zero of the 376 originals under the proposed checks below.** All
376 completed the pinned audit; no failed or timed-out audit was counted as a
pass. C excludes 16, listed individually below. No original has been removed.

**Historical draft status at presentation.** This document selects nothing, installs nothing and closes no
decision. Approval/selection words are **A**, **B**, or **C**; each selects the
specified domain/proof route and its stated costs. C cannot release the unchanged
checkpoint gates: its scope conflicts are explicit below. Selection is not a
claim that the required Lean proofs already exist. P-WIRE needs its own approval.

## Decision table

| Choice | Exact proposed approach | Original-case impact | Cost, in one line | Halted work released after owner installation |
| --- | --- | --- | --- | --- |
| **A — narrow `Valid`** | Birth-event and birth-date functionality, plus the all-solutions `DecreaseA` condition below. | **0/376 excluded** by the proposed checks, including stipulated c2/c3 solutions; all 201 years 1900–2100 audited. | Removes multibirth/multidate and nondecreasing eligible-kinship adversaries; requires independent prefix definitions and a decrease/fuel proof, estimated **3–6 working days**. | §152, §7703, R8 and every halted caller reaching this group, on the narrowed domain; reference use awaits the proof obligations. |
| **B — formal all-solutions route** | Require the complete pre-recursion graph `E_y` below to be acyclic; no birth functionality requirement. | **0 additional exclusions inferred for these 376**: all 75,576 year-indexed `K ∧ c3` supergraphs are acyclic and `E_y` is a subgraph; not a separate full-corpus `E_y` run. | Preserves birth multiplicity but conservatively excludes cyclic-prefix households; finite call abstraction, decidability and kernel decrease/fuel proofs estimated **5–10 working days**. | The same §152/§7703/R8/caller work; selecting B starts a proof project, not permission to use an unproved reference. |
| **C — coarse structural exclusion** | Require the full relationship graph `K` to be acyclic, including self-edges. | **16/376 excluded**, leaving 360 in this proposed domain. | Excludes every realized sibling/stepsibling pair and makes some sibling-branch arms unreachable; **2–4 working days** for guard/proofs, plus owner redesign of the 376-case and full-arm gates. | The same recursive work only on the structurally restricted domain; current Checkpoints 1/2 cannot pass under this choice without separately explicit gate amendments. |

Estimates are planning ranges for the restriction, measure, decidability and
R5/R8 proof work, not measured completion times or guarantees. They exclude full
section translation, other recursion groups, parity runs and owner review. A new
counterexample stops work; it is not absorbed by extending the estimate silently.

## Shared definitions and placement

The finding is unchanged. `s152_c_2`'s sibling/stepsibling branch is not controlled
by V4's child graph. Both preserved fixtures admit a repeated R5 call. The old
V10 and `2 * persons.length + 2` remain withdrawn. No comparison in the source,
including `is_before`, is changed.

Let `U` be a finite, tag-sensitive set containing every term that can become a
person in the relevant calls; `N = |U|`. Facts, applicable stipulations and bound
query arguments must be covered. Adding isolated query terms is harmless; missing
a participant is not. The diagnostic uses an explicit conservative finite
superset, not a claim that all string literals are semantically persons.

For ground `t,d ∈ U`:

```text
Birth(p)  := some birth_(e), agent_(e,p) solution exists, even without a date
DOB(p,b)  := some birth_(e), agent_(e,p), start_(e,b) solution exists
Desc(t,d) := original is_descendent_of(d,t,_,_) succeeds (nonempty path)
K(t,d)    := original s152_c_2(d,t,_,_) has some solution, both people bound
L_y(t,d)  := K(t,d) and original s152_c_3(d,t,y) succeeds
```

Use the source's complete fact-solution union, not one selected birth, marriage,
residence or relationship witness. `K` includes both c2 branches, descendants of
siblings/stepsiblings, date behavior, and appended c2 stipulations. `c3` includes
appended c3 stipulations. Set-valued graph edges are only termination evidence;
the oracle's G1 lists keep order and multiplicity.

**Proposed placement for all options:** a new H5 conjunct, explicitly included
in **both** `Valid` and `ValidStip`, not hidden in V1 (which `ValidStip` omits).
For A this includes the uniqueness half too. Dev installs the selected amendment
to H5/R5/R8/R9 and re-pins the protected manifest. The builder does not do so.

For A/B, check every V3-admitted year 1900–2100, not only the outer query year.
R8 extracts its actual year from Workday. The implementation proof must establish
that every admitted operational year is covered, including query/stipulation
Workdays; current `Household.v3` checks fact dates, not arbitrary query arguments.
**That coverage is an explicit outstanding proof/interface obligation, not an
assumption certified by this draft.** Unbound-year paths require their existing
mode/E2-exclusion argument. Never fall back to a value for an uncovered year.
C's structural premise is year-independent.

## A — exact narrowing and measure

Proposed new conjunct:

1. Each person is associated with at most one **distinct birth-event identifier**.
2. Each birth event has at most one **distinct start day**.
3. For every `L_y(t,d)`, require:

```text
DecreaseA(t,d) :=
  (Birth(d) and t,d have defined unique DOBs and DOB(t) < DOB(d))
  or
  (not Birth(d) and Desc(t,d)).
```

Term distinctness is G4 tag-sensitive identity: an atom and string with identical
text remain different events/persons. Repeated occurrences of an identical fact
are not different events/days and are not deleted. A birth lacking a start date
is still a birth; absence of a date does not enable the birthless alternative.
Requiring one event alone would be insufficient: one event with multiple starts
recreates the existential-date problem.

The strict inequality is a **proposed domain restriction**, not a change from the
source's inclusive `is_before`. No global ban on unrelated people sharing a DOB
is proposed. This is also stronger than merely checking equal birthdays: a
self-transition must fail `DecreaseA`, and arbitrary c3 stipulations must satisfy
it too. This latter requirement deliberately rejects incompatible stipulated
edges rather than assuming they obey the statute clause.

**Measure argument.** Along dated-to-dated transitions the unique DOB strictly
increases. Once a transition enters a birthless person, it cannot return to a
dated person: that would require the taxpayer to have a defined DOB. Subsequent
transitions follow strict descendant paths in the V4 DAG. An undated birth can
start only a birthless suffix. Thus no person repeats on a branch, so it has at
most `N−1` contracted transitions. Equivalently, use a lexicographic phase rank
(born before birthless), decreasing DOB rank in the born part, and descendant
height in the birthless part. These are source-level arguments awaiting kernel
proofs, not a reinstatement of a withdrawn birthday-function assumption.

Uniqueness is fact-list decidable. The `K/c3` half requires separately total
relationship/age definitions under V4, including stipulated clauses; it is not
being sold as a facts-only validation check.

## B — complete pre-recursion relation and proof burden

For each admitted actual year, define:

```text
E_y(t,d) := there exists a complete compatible solution of
  s152_c_1_A(d,t,start,end),
  s152_c_1_B(d,_,t,start,end,y),
  s152_c_1_C(d,t,y).
```

The `start/end` bindings are shared across the first two goals exactly as in the
source; optional dates, first-solution commitments and all fact witnesses remain
intact. **Do not include c1E.** Otherwise the decidable premise would invoke the
recursion it is supposed to justify. Require `E_y` acyclic, including self-edges.
This is an intentional over-approximation: it ignores marriage and other caller
prefix conditions that might prevent the recursive call. Cyclic-prefix inputs
that happen to terminate for those other reasons can therefore be excluded.

The proof route is:

1. Prove the finite universe covers all bound/free call modes after source
   bindings; prove all actual recursive transitions are edges of `E_y`.
2. Define total prefix enumerators without the recursive group. Under V4,
   descendant search is finite; other prefix fact searches are finite. Establish
   absence of exceptions under the full admitted-input premises.
3. Decide graph acyclicity by finite enumeration. Construct graph height on
   acyclic inputs and prove each transition strictly decreases it.
4. Derive the runtime counter bound from height and prove its adequacy for every
   entry mode, `ValidStip` and R8, with actual-year coverage as above.

The graph-height function belongs in the proof; the executable definition uses
the uniform finite bound below without presupposing that the input is valid.
This route does not preserve the old `Valid` unchanged: the two cyclic witnesses
cannot acquire a termination proof. It changes admissibility, not source values.

## C — coarse exclusion and exact cost

Require `K` acyclic, including self-edges. Since `E_y ⊆ L_y ⊆ K`, K-height
decreases on every contracted recursive transition; no DOB functionality is
needed. Computing K still requires the original relationship/date/marriage
helpers and V4, not just a scan for brother/sister tokens.

Every realized sibling/stepsibling pair gives both directed edges when queried
with bound people. Thus C excludes terminating sibling households too, even if
age, residence or marriage prevents recursive execution. The following originals
all have the listed two-cycle (arrows denote taxpayer → dependent). These are the
**complete 16 exclusions** from the pinned audit:

| Case ID | K cycle causing exclusion |
| --- | --- |
| `s152_c_2_A_neg` | alice ↔ bob |
| `s152_c_2_B_pos` | alice ↔ bob |
| `s152_d_2_A_neg` | alice ↔ bob |
| `s152_d_2_B_pos` | alice ↔ bob |
| `s152_d_2_D_neg` | bob ↔ charlie |
| `s152_d_2_E_neg` | alice ↔ charlie |
| `s152_d_2_E_pos` | bob ↔ charlie |
| `s152_d_2_F_pos` | alice ↔ charlie |
| `s2_b_1_A_ii_pos` | bob ↔ charlie |
| `tax_case_11` | alice ↔ charlie |
| `tax_case_18` | bob ↔ charlie |
| `tax_case_53` | alice ↔ bob |
| `tax_case_64` | alice ↔ bob |
| `tax_case_70` | alice ↔ bob |
| `tax_case_75` | alice ↔ charlie |
| `tax_case_85` | alice ↔ charlie |

**Gate conflict, not a waiver:** 360 in-domain cases are not a pass on the
approved 376-case gate. Successful sibling-branch paths, including inner c2_B
arms, cannot meet the unchanged full-arm coverage requirement. Choosing C needs
Dev to approve explicit scope/gate amendments before it can deliver the original
plan's checkpoints. No replacement denominator or coverage exemption is silently
bundled into the word C here. C is G6-compliant as a conservative domain choice,
but is not a one-word release of the unchanged experiment.

## Counter discipline shared by the three routes

Proposed executable **depth counter `N+1`**, derived from the at-most-`N−1`
contracted transitions, with this exact discipline:

- Decrement once when a successful `s152_c_1` A/B/C prefix crosses into its c1E
  continuation (and then the recursive `s7703` call). Helpers do not decrement
  this counter; their own termination measures remain separate.
- Pass the smaller counter down that branch. It is **not** a mutable global
  budget spent across sequential calls, siblings or backtracking alternatives.
  Fresh independent group invocations start with the full bound; a descendant
  recursive invocation must not reset it. R8 follows this same discipline.
- The Lean termination construction needs a secondary finite phase ordering
  between contracted transitions. Prove no cycle in the R5 subtree avoids the
  decrement, and verify wrapper offsets before certifying the constant.
- Cover direct paragraph queries/c1E, `s152_b_2`, `gross_income`, §151's direct
  calls, other callers, every approved mode and R8's actual Workday year.

**Fuel exhaustion is never a reference answer.** Any reachable exhaustion on an
admitted input is a halt-and-report failure, not `[]`, `false`, a mismatch, or an
instruction to increase an arbitrary budget. Exclude reference-undefined inputs
through the signed `Valid` premise. A total Lean definition outside that premise
does not grant those inputs a reference value. R9's unreachable-exhaustion claim
may be asserted only after the adequacy proof, not on the strength of this audit.

## Both preserved witnesses checked before presentation

| Candidate | Equal-birthday sibling witness | Multibirth witness |
| --- | --- | --- |
| A | Rejected: both directions have births and `2000 < 2000` is false. | Rejected: `a` has two distinct birth events; the audit also flags incompatible edge conditions. |
| B | Measured compatible c1A/B/C prefix edges `a→b` and `b→a` at 2018; graph cyclic. | Measured the same prefix cycle, selecting the appropriate different birth facts. |
| C | Measured K contains `a→b→a`. | Measured K contains `a→b→a`. |

Both fresh runs reproduce finite marriage prefixes, age success in both
directions, and `s7703` exhaustion at 100,000 and 1,000,000 inferences. Budget
exhaustion is bounded evidence, not a divergence proof; the repeated-call source
argument is separate. No kernel `Valid` certificate or oracle theorem is claimed.

An extra review check changed only an in-memory copy of the sibling fixture:
`b` born in 1990 and `a` also a child of `b`. It has distinct single birthdays
and an acyclic child graph, yet K and the compatible c1 prefix have `a→a`.
Pinned execution confirms the self-edge and 100,000-inference exhaustion. A's
strict decrease and B/C's self-cycle checks reject it. This is why self-edges
must not be assumed impossible under V4.

## Evidence and limitations

Retained diagnostic directory: `docs/contracts/phase1-decision-audit/`.

- `full-20260922-01/summary.json`: 376/376 originals and 2/2 witnesses completed;
  no stderr, missing result, exception or timeout. No uniqueness violations,
  equal-DOB pairs, self-edges or proposed A-condition failures in the originals.
- `full-20260922-01/all_results.json`: individual source digests, complete case
  clause accounting, graph edges, birth facts, years and failure reasons.
- `MENU_GRAPH_CHECK.json`: 75,576 acyclic `K ∧ c3` graphs and the 16 C exclusions.
  The B zero-impact inference uses subgraph inclusion; it is not a separate
  full-corpus B execution or a machine-checked theorem.
- `self-edge-20260922/`: exact command and streams for the extra self-edge check.
- Runtime identity `744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`:
  measured Debian `7.2.3+dfsg-6`, amd64, approved TZ and full record match.
  `/human`, `/corpus`, diagnostic sources and witnesses mounted read-only.

The audit reads terms with the pinned reader, loads canonical statutes, and
appends case clauses in order. Original test/load/halt directives are not
executed; case predicates and rules are evaluated for the diagnostic queries.
Both H4.4 terminators are restored only in memory, after checking their hashes.
Clause counts verify originals plus appended clauses; diagnostic graph sets do
not rewrite the original lists. This is a rule-impact audit, not semantic
round-trip acceptance, full `ValidStip` certification or Week-1 parity.

The first smoke run hit the pinned runtime's prohibition on making an already
static predicate dynamic. The second predeclared the case-supplied heads before
canonical loading, checked clause preservation, and passed; the full run uses
that corrected diagnostic. Failed evidence is retained, not counted as passing.

Review: Q-011/A-011 and an isolated source audit. A-011 is immutable. Its claim
that V4 rules out K self-edges is refuted by the extra diagnostic above. Its
whole-section closure claim is too broad: use only the R5 recursive subtree;
§152's other branches call `gross_income`, and `(b)(3)` calls `s7703_a`.
Likewise K's helper computations do involve dates and marriages. The draft does
not adopt those overbroad claims from the review.

## Resume boundary and self-review

No oracle work resumes in this draft session. Owner selection fixes the proposed
route; owner installation and re-pinning release the corresponding domain hold.
Then the isolated oracle lane can implement §152/§7703 and reaching predicates,
including R8, with the stated proof obligations. P-WIRE must separately be
installed before producers run. No option signs off Checkpoint 1 or authorizes a
builder edit to `human/`; C additionally has the explicit gate conflict above.

**Self-review — Prolog assumptions:** left-to-right SLD order; first-success
`->`; NAF does not export bindings; inclusive source `is_before`; tag-sensitive
identity; finite fact lists with duplicates retained; H4 stipulations appended
after statute clauses. Birth bindings are shared within one c3 invocation but
fresh across calls. No attribute is assumed functional except where A explicitly
requires it. Mode coverage, finite-universe completeness, operational-year
coverage, exception-freedom and kernel fuel adequacy remain proof obligations.
**Circuit breaker:** three failed edit cycles on one test means stop and report.
The diagnostic had one failed smoke cycle followed by a passing fix; no
production implementation or semantic-repair edit cycle was undertaken.
