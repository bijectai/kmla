# Q-025 evidence: G2 output-position derivation

A-024 asked for the output positions of the 135 queried signatures to be derived
from G2 statute call sites as well as H6.5's case modes and its bound-answer
table, with each row keeping its basis, and for underdetermined rows to come
back for review. This directory is that derivation. It is **builder analysis for
review, not a declaration**: nothing here is in `Interface/`.

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

Bindings inside `\+` and `findall/3` do not escape. Modes propagate from the
case modes through every statute caller. G2's `nonvar`/`var` guards are
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

## Critic corrections, not applied to the table

- `s7703_a_1/5` position 5 under L: the adjudicated row marks it
  underdetermined, conditioned on a "Q1" that is defined nowhere. The critic
  shows that under the table's own L reading it is an input: outputs_L
  `[1,2,3,4]`, consistent with the other s7703 L rows. See the critic's
  evidence in `derivation.json`.
- `s3306_c_10_A_ii/3` under L: the result `[]` is right, but the row's stated
  basis is wrong. The correct basis is that `:681` is reached only after `:678`
  succeeds, and `:678` has no solution with Workday unbound: `:694` fails at the
  `nonvar` guard in `utils.pl:11`.
- **Missing basis text, with no change to outputs:**
  - `tax/3` and `s151_a/3` should cite `DECISIONS.md:913-916` and A-024's
    table. `tax/3` also stays the H6.1/H6.2 first-solution exception and is
    never enumerated.
  - The L-only exclusions in `s152_b_2`, `s152_c_1_E`, `s152_c_3` and
    `s152_d_1_D` should cite `section152.pl:65 -> :129`,
    `:243 -> :268 -> utils.pl:274` and `:285 -> :345`.
  - Several rows omit why their excluded positions are always bound.

## Limits

- **Not executed.** A reviewer should sample rows against the source.
- **Beyond the corpus:** some input classifications rely on corpus stipulations
  being ground in a position, for example every `s63/3` stipulation in position
  3 for the 20 `s1_*_{i..v}/2` rows. They would change for Households carrying
  wildcard stipulations there. Whether that matters beyond the corpus is one of
  Q-025's questions.
- **Statute-internal modes:** these are recorded in `reached_modes` but not
  proposed for the declaration, following A-024 §1 and H6.5.
