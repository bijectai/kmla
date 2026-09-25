# Q-025 evidence: G2 output-position derivation

A-024 asked for the output positions of the 135 queried signatures to be derived
from G2 statute call sites as well as H6.5's case modes and its bound-answer
table, with each row keeping its basis, and for underdetermined rows to come
back for review. This directory is that derivation. It is **builder analysis for
review, not a declaration**: nothing here is in `Interface/`. A-025 reviewed it
and did not approve it; see "Review status" below.

- `TABLE.md`: a summary table, then one section per signature listing its
  reached modes and every position's classification under both readings, with
  file:line basis.
- `derivation.json`: the same rows in machine-readable form, plus the
  analysts' open questions, the pass-two critic's findings and the pass-one
  critic's findings.

## Sources and isolation

Only `human/sara/sara/statutes/prolog/*.pl`, `human/sara/sara/cases/*.pl`,
`human/DECISIONS.md`, `Interface/TIME_SCHEMA.json`, Q-024, A-024 and
`../q024-question-bindings/` were read, all read-only. No lane directory
(`harness/`, `Oracle/`, `gen/`), lane report, review note, protected meter,
exploit or governor log was opened, and no interpreter was run. The
classifications are static readings of the source by model agents. They were
not executed.

## Definitions

A position is b at a call site when the argument is certainly ground at call
entry in that caller mode. That holds for:
- a literal;
- a head variable whose head position is b;
- a variable bound on every path by an earlier goal: builtins, Household facts,
  or an earlier statute call whose clauses always bind it and which no case
  stipulation leaves unbound.

Bindings made inside `\+` do not escape. Neither do bindings of the variables
inside a `findall/3` goal, but `findall/3`'s third argument is bound to the
collected list (A-025 §3). Modes propagate from the case modes through every
statute caller. G2's `nonvar`/`var` guards are
resolved by the mode, and the both-unbound `s152` call is empty.

- **Reading S (syntactic):** every call site reached in a reached mode counts.
- **Reading L (live path):** as S, but a call site does not count in a mode if
  every path to it first passes a goal that raises an instantiation error or has
  no success path.

Under each reading a position is an **output** if it is free at some counted
call site or case query, or if A-024's bound-answer table lists it. It is an
**input** only with evidence that it is ground at every counted site, and
otherwise **underdetermined**.

## Method

1. **Pass one** (superseded) used two independent analysts per statute file,
   adjudication and a mechanical fixpoint. Its critic found three errors: its
   record format could not express "bound by the head or by an earlier call"
   (39 wrong rows, including all 20 `s1_*_{i..v}/2`), it ignored G2's guards,
   and it mixed live and dead paths. Its critique is kept in `derivation.json`.
   Its table is not used.
2. **Pass two** used two independent analysts per section group, each deriving
   every position of every signature under both readings from the source. The
   derivations agreed on every position in 9 of 10 groups. The s7703 group was
   adjudicated.
3. **A critic** checked the merged table against A-024 and the source.

## Result

- 135 of 135 signatures, every position classified.
- **A-024 checks:** all 47 bound-answer entries are outputs under both readings.
  `s63_d/4` has outputs 2 and 3. `s3306_b/8` and `s3306_c_B/4` have every
  position as an output. `s152_d_2_D/4` and `s152_d_2_G/4` include 3 and 4.
  `s68_b/3` is `[2]`, with no invented slot.
- **Rows that differ between the readings (10):** `s152_b_2/4`, `s152_c_1_E/3`,
  `s152_c_3/3`, `s152_d_1_D/2`, `s3306_c_10_A_ii/3`, `s7703_a_1/5`,
  `s7703_a_2/5`, `s7703_b_1/4`, `s7703_b_2/4` and `s7703_b_3/4`. In each, the
  position is free only on the unbound-year or unbound-Workday paths (the
  F9/E2 call at `section3306.pl:317`, and F4), which raise or fail first.
- **Verified-empty output tuples under both readings (13):** `s2_b_1_A_i_I/2`,
  `s2_b_1_A_i_II/3`, `s63_c_2_A_ii/2`, `s63_c_6_B/2`, `s63_c_6_D/2`,
  `s63_d_2/3`, `s63_f_1_A/2`, `s63_f_2_A/2`, `s68_f/1`, `s3306_a_1/2`,
  `s3306_b_2_A/1`, `s3306_b_2_C/1` and `s3306_c_6/1`.

## Critic findings, reconciled against the delivered table

An earlier version of this section repeated the pass-two critic's findings
without checking them against `TABLE.md`. A-025 found several of them stale.
The critic's original text is kept unchanged in `derivation.json` as history;
this section describes the table as delivered.

- **`s7703_a_1/5` position 5 under L.** The row is underdetermined, and
  `TABLE.md:2406` defines the two questions it depends on (Q1, Q2). The
  critic's "undefined Q1" was wrong. A-025 finds the row's status inconsistent
  with the `s152_b_2/4` position-4 argument under L. Given L and the stated
  corpus-stipulation premises, position 5 would be an input, but that is not a
  certification over arbitrary `ValidStip`. The row is left as delivered,
  because neither column is accepted (see "Review status").
- **`s3306_c_10_A_ii/3` under L.** `TABLE.md:2260` already gives the correct
  basis: `:681` is reached only after `:678` succeeds, and with Workday unbound
  `:678` fails at the `nonvar` guard in `utils.pl:11` via `:694`. The critic's
  claim that the basis was wrong is stale. A raise at `:717`, inside the
  callee, would not establish non-entry.
- **Bound-answer basis.** `tax/3` position 3 (`TABLE.md:2497`) and
  `s151_a/3` position 2 (`TABLE.md:1276`) already cite A-024's table and
  `DECISIONS.md:913-916`, and `tax/3` keeps the H6.1/H6.2 first-solution
  exception. A-025's sampled §152 L rows contain source chains. Some other rows
  may still omit why their excluded positions are always bound. Reconcile any
  row against the delivered bytes, not the critic's checklist.
- **The critic's scoping premise.** Its unqualified "bindings inside findall do
  not escape" is corrected as in Definitions above.

## Review status (A-025, 2026-09-25)

- **Not approved.** The derivation is retained analysis. Neither the S column
  nor the L column is accepted as the declaration, and two analysts agreeing
  does not prove an input position is always ground.
- **Counting policy.** A-025 separates three counting policies: S (syntactic
  continuation), ENTRY (operational call entry) and defined-domain-only. It
  selects none, and proposes P-G2-CALLS, an ENTRY census, for Dev to approve or
  amend. Under the policy Dev chooses, the affected rows must be re-derived. S
  would also need a uniform rule for bindings after a goal that cannot return:
  "bound on every successful return" is vacuous when nothing returns.
- **Interpretation points.** Its answers to the nine points are in A-025 §3.
  Classifications that rely on corpus stipulations hold for the corpus only.
- **Representation.** Accepted as builder spelling only: one-based `outputs`
  keyed by case mode, with `[]` versus absence kept distinct. Content is not
  approved.
- **Halt.** HANDOFF item 1 is halted until Dev decides P-G2-CALLS and
  P-H6-CONJ (`STATE.md` → Blockers).

## Limits

- **Not executed.** A reviewer should sample rows against the source.
- **Beyond the corpus:** some input classifications rely on corpus stipulations
  being ground in a position, for example every `s63/3` stipulation in position
  3 for the 20 `s1_*_{i..v}/2` rows. They would change for Households carrying
  wildcard stipulations there. A-025: do not extrapolate. `ValidStip` does not
  require those positions to be ground, so the claims hold for the corpus only.
- **Statute-internal modes:** these are recorded in `reached_modes` but not
  proposed for the declaration, following A-024 §1 and H6.5.
