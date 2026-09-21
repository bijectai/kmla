# Household input contract — DRAFT ONLY

Status: Phase 0.1 source-syntax draft, pending the owner's `human/DECISIONS.md`
and Checkpoint 0 approval. The Lean declarations are in
[Interface/Household.lean](../../Interface/Household.lean), under
`HouseholdDraft`. They are not the approved semantic interface.

The approved amendments in [PROTOCOL.md](../PROTOCOL.md) supersede the original
plan. They designate SWI-Prolog 7.2.3 on Docker `linux/amd64` for later execution;
this lexical inventory does not execute or validate that runtime. The main lane
owns the verified archive provenance and generic parity envelope. The supplied
archive SHA-256 is
`e4f1b845016fc38b95b702bbbb27a5c9af3eadfa856ba585662b8b2cd71c187c`;
it is recorded here as supplied, not independently re-verified in this lane.

## Scope and inspection basis

This inventory reads only the designated
[events.pl](../../human/sara/sara/statutes/prolog/events.pl) and all **376**
`human/sara/sara/cases/*.pl` files. Source citations below are local relative
paths with one-based line anchors. `E<n>` links to line `n` of `events.pl`.
No source statute body or imported initialization file was used to infer a
predicate's meaning. Corpus identity, provenance, hashes, other contracts and
the statute hazard inventory belong to the other work lanes.

The inspection is lexical: comments and quoted text were separated from clause
syntax, full-stop-terminated terms were inspected across line boundaries, and
head names, argument counts and per-position token shapes were counted. The
source was not consulted or executed in Prolog. The inventory does not certify
runtime behavior under any Prolog dialect or initialization settings.

| Observed surface category | Occurrences | Distinct head signatures / files |
| --- | ---: | --- |
| Ground bodyless clauses | 5,234 | Included in the 79 bodyless signatures below |
| Bodyless clauses containing variables | 108 | 94 files; only anonymous `_` occurs in these clauses |
| All bodyless clauses | 5,342 | 79 name/arity pairs |
| Clauses with a `:-` body | 434 | 27 head signatures in 61 files |
| Top-level directives | 1,346 | Includes declarations, loads, tests and `halt` |
| `events.pl` discontiguous declarations | 61 | 61 distinct name/arity pairs |

There are **92 distinct case clause-head signatures**: 79 have bodyless
occurrences, 27 have rule occurrences, and 14 have both. A total of 149 cases
contain a variable-bearing bodyless clause, a rule, or both. These counts follow
literal term boundaries, including the two cross-`% Test` clauses described
below. All 376 cases contain directives; none is a file of facts alone.

The tables below cover all **227 distinct identifier-style name/arity pairs**
found in the event declarations and case heads, calls, and predicate indicators.
The separate surface-syntax table includes prefix `discontiguous/1`,
`halt/0`, operators, and load notation that are not captured as ordinary
parenthesized calls. Query-only predicates are not household facts.

## Draft representation and preservation

`HouseholdDraft.Household` contains one `List Item`. Its order is the source
order across predicates and item kinds; it is not a map, a set, a sorted list
or a collection grouped by event. Each occurrence gets its own list position.
For example, repeated `marriage_` and `agent_` clauses at
[tax_case_16.pl:13](../../human/sara/sara/cases/tax_case_16.pl#L13) and
[tax_case_16.pl:17](../../human/sara/sara/cases/tax_case_16.pl#L17), and at
[tax_case_41.pl:9](../../human/sara/sara/cases/tax_case_41.pl#L9) and
[tax_case_41.pl:16](../../human/sara/sara/cases/tax_case_41.pl#L16), remain
separate occurrences. Six later duplicate bodyless occurrences were observed
across these two files. Different dates attached to the same event also remain
separate clauses.

An absent fact has no entry. An empty list records no entries, with no inserted
zero, false, unknown-person, missing-date, default-year, or other replacement.
This structural absence does not assert Prolog falsity or any closed-world
meaning. No field has a default, no identifier has an inferred domain, and no
`Valid` predicate is supplied.

`FactPredicate : Nat → Type` has exactly one constructor for each of the 79
observed bodyless name/arity pairs. `Fact` pairs it with a `Vector Argument`
of that arity. This enforces argument count, not semantic types, per-position
token classes, lexical correctness, or groundness. The positional summaries in
the inventory are observations, not allowed-domain declarations.

The supported bodyless argument forms are:

| Constructor | Captured syntax | Evidence and boundary |
| --- | --- | --- |
| `unquotedAtom` | Original unquoted atom lexeme | `alice_makes_money` and `alice` at [s151_a_neg.pl:11](../../human/sara/sara/cases/s151_a_neg.pl#L11). No person/event distinction is inferred. |
| `doubleQuoted` | Complete lexeme, including quotes and any escapes | `"2015-01-01"` at [s151_a_neg.pl:12](../../human/sara/sara/cases/s151_a_neg.pl#L12); names also use this syntax, e.g. [s63_c_6_D_neg.pl:10](../../human/sara/sara/cases/s63_c_6_D_neg.pl#L10). No runtime string/atom/list interpretation is selected. |
| `unsignedDecimal` | Original digit lexeme | `100000` at [s151_a_neg.pl:14](../../human/sara/sara/cases/s151_a_neg.pl#L14); `2015` at [s151_a_neg.pl:15](../../human/sara/sara/cases/s151_a_neg.pl#L15). No unit or numerical conversion is supplied. |
| `anonymousVariable` | One occurrence of `_` | [s151_a_neg.pl:15](../../human/sara/sara/cases/s151_a_neg.pl#L15). The 108 non-ground bodyless clauses contain 124 such occurrences. There is no name, default value, or shared-variable identity attached to this constructor. |
| `atomList` | Closed list of unquoted atom lexemes in order, with multiplicity | The only observed bodyless list is `[alice]` at [s63_d_2_pos.pl:14](../../human/sara/sara/cases/s63_d_2_pos.pl#L14). Other lengths are structurally possible, not an approved domain. |

Only the arity index is checked by Lean. String payloads can be malformed if
constructed incorrectly; no lexical validator or ingestion implementation exists.
The argument type admits combinations not observed in any case. This does not
authorize generating such inputs or treating them as valid.

`Item.fact` means a bodyless clause; it does not mean a ground assertion.
Non-ground bodyless clauses are captured as syntax only. In particular,
`purpose_(_,"agricultural labor").` at
[s3306_a_2_B_neg.pl:75](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L75)
must not be converted to a fact about a missing event or materialized over guessed
events. Rules and directives are explicit `unsupportedRule` and
`unsupportedDirective` source payloads at their positions in the same list.
A raw payload retains its entire terminated clause/directive, including its
body. These are unsupported records, not executable data and not evidence that
semantic ingestion is complete. Any future semantic consumer must stop on them
and report the source; silently dropping or executing them is not an option.

This draft preserves clause/argument order, multiplicity, predicate spelling,
arity, token classes and supported token lexemes. It does **not** preserve
comments or whitespace around typed bodyless clauses, and is not a byte-for-byte
source-file representation. Comments/whitespace inside an unsupported raw
clause can be retained as part of that payload. There is no parser, serializer,
round-trip checker, oracle, generator, statement or theorem implementation here.
In particular, no claim of round-trip identity on all 376 cases has passed.

## Unsupported forms and blocking findings

The following are observed and explicitly outside executable support:

| Form | Source evidence | Required treatment in this draft |
| --- | --- | --- |
| Variable-bearing bodyless clauses | [s151_a_neg.pl:15](../../human/sara/sara/cases/s151_a_neg.pl#L15), [s63_a_neg.pl:16](../../human/sara/sara/cases/s63_a_neg.pl#L16), [s3306_a_2_B_neg.pl:75](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L75) | Capture anonymous variable occurrences; no unification, instantiation, quantification or truth interpretation is implemented. |
| Named variables and dependent rule bodies | [s2_a_1_B_neg.pl:26](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L26) and the projection clauses at [s2_a_1_B_neg.pl:31](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L31) | Preserve the complete rule as unsupported. Do not expand `between`, build event names or query helper predicates. |
| Rules whose heads overlap fact predicates | [s2_b_3_B_pos.pl:42](../../human/sara/sara/cases/s2_b_3_B_pos.pl#L42) | Keep their positions; no replacement of a rule with its head or derived facts. |
| Named variables, quoted atoms and list arguments inside rules | [tax_case_10.pl:43](../../human/sara/sara/cases/tax_case_10.pl#L43), [s2_a_1_B_pos.pl:40](../../human/sara/sara/cases/s2_a_1_B_pos.pl#L40), [tax_case_33.pl:15](../../human/sara/sara/cases/tax_case_33.pl#L15) | These are outside the typed bodyless argument subset and remain in the raw rule. |
| Conjunction, disjunction, identity tests and conditionals/unification | [s3306_a_2_B_neg.pl:22](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L22), [s7703_b_1_neg.pl:30](../../human/sara/sara/cases/s7703_b_1_neg.pl#L30) | No branch selection, equality interpretation or evaluation. |
| Instantiation-sensitive `var`/`nonvar` and date helpers | [s3306_b_15_neg.pl:10](../../human/sara/sara/cases/s3306_b_15_neg.pl#L10) | No finite fact expansion or guessed date range. |
| String/atom construction and decomposition | [tax_case_33.pl:13](../../human/sara/sara/cases/tax_case_33.pl#L13), [tax_case_33.pl:34](../../human/sara/sara/cases/tax_case_33.pl#L34) | No conversion or assumption about these predicates' execution modes. |
| Directives: discontiguous declarations, loading, positive/negative and compound tests, termination | [s151_a_neg.pl:8](../../human/sara/sara/cases/s151_a_neg.pl#L8), [s151_a_neg.pl:18](../../human/sara/sara/cases/s151_a_neg.pl#L18), [s152_d_2_D_neg.pl:19](../../human/sara/sara/cases/s152_d_2_D_neg.pl#L19) | Retain explicitly as unsupported directives; they are not household facts. |

No floating-point, signed-number, compound-function, named-variable, quoted-atom,
open-list or nested-list argument occurs in the bodyless clause subset inspected
here. Those forms have no typed bodyless constructor in this draft. Named
variables, quoted atoms and other list element kinds do occur in rules and/or
directives; their raw preservation is not typed or executable support. Any new
predicate or unsupported bodyless syntax is a review blocker, not an invitation
to add a guessed predicate or coerce its arguments.

**Clause-boundary finding; affected interpretation is stopped.**
In both
[s3306_c_2_neg.pl:26](../../human/sara/sara/cases/s3306_c_2_neg.pl#L26) and
[s3306_c_2_pos.pl:26](../../human/sara/sara/cases/s3306_c_2_pos.pl#L26),
the `s3306_b(...)` head lacks a period before the `% Test` comment.
The following `:-` at line 29 therefore belongs to the same terminated surface
term. Literal syntax yields a rule with `s3306_c_2/3` in its body (under
`\+` in the negative file), not a separate bodyless fact and test directive.
The counts record two such rules, and only 374 standalone test directives.
No period was inserted, no comment was treated as a clause separator, and neither
case was excluded. Any intended test/fact interpretation or repair requires an
owner decision before the affected ingestion/round-trip contract can proceed.

The plan's facts-to-household round-trip requirement also needs an explicit
decision for all local rules and non-ground clauses. The source includes
instantiation-sensitive rules; finite enumeration of some `between` examples
does not justify treating all cases as ground data. This draft does not implement
that workaround. A raw unsupported payload is solely a visible record of missing
support. Approval of this document alone must not be recorded as completion of
the all-case round-trip requirement.

Spelling and arity differences are observations requiring preservation, not
repairs: `patient/2` and `patient_/2`, `s151_b_applies/2` and `/3`,
`s2_a/3` and `/5`, `s63_c_3/3` and `/4`, and the rule heads
`bob_income/3` and `/4`. No typo correction or predicate alias is supplied.

## Complete observed inventory

Notation: `G` = ground bodyless occurrence; `N` = variable-bearing bodyless
occurrence. `A` = unquoted atom; `D` = double-quoted lexeme; `I` = unsigned
decimal lexeme; `V` = variable token (only `_` for bodyless clauses);
`L[A]` / `L[I]` = closed list containing atoms / integer lexemes.
A slash inside a positional shape means multiple observed token classes at that
position. Summaries are component-wise; they do not assert that every Cartesian
combination appeared or is admissible. The witnesses cover every displayed
per-position class. No semantic argument names are inferred.

### All 79 bodyless predicate/arity pairs

These are exactly the `FactPredicate` constructors. Some also have rules;
those rule occurrences are counted separately below. A dash in the declaration
column means no declaration in the designated `events.pl`, not nonexistence
in other files.

| Predicate/arity | G / N count | Argument shapes (G; N where present) | Event declaration | Source witnesses for all displayed shapes |
| --- | ---: | --- | --- | --- |
| `agent_/2` | 1298 / 0 | G: `(A, A/D)` | [E1](../../human/sara/sara/statutes/prolog/events.pl#L1) | [s151_a_neg.pl:11](../../human/sara/sara/cases/s151_a_neg.pl#L11); [s2_b_2_A_neg.pl:14](../../human/sara/sara/cases/s2_b_2_A_neg.pl#L14) |
| `american_employer_/1` | 7 / 0 | G: `(A)` | [E5](../../human/sara/sara/statutes/prolog/events.pl#L5) | [s3306_c_1_A_i_pos.pl:23](../../human/sara/sara/cases/s3306_c_1_A_i_pos.pl#L23) |
| `amount_/2` | 348 / 0 | G: `(A, I)` | [E6](../../human/sara/sara/statutes/prolog/events.pl#L6) | [s151_a_neg.pl:14](../../human/sara/sara/cases/s151_a_neg.pl#L14) |
| `attending_classes_/1` | 8 / 0 | G: `(A)` | [E7](../../human/sara/sara/statutes/prolog/events.pl#L7) | [s3306_c_10_A_i_neg.pl:30](../../human/sara/sara/cases/s3306_c_10_A_i_neg.pl#L30) |
| `beneficiary_/2` | 18 / 0 | G: `(A, A)` | [E8](../../human/sara/sara/statutes/prolog/events.pl#L8) | [s3306_b_2_A_neg.pl:26](../../human/sara/sara/cases/s3306_b_2_A_neg.pl#L26) |
| `birth_/1` | 29 / 0 | G: `(A)` | [E9](../../human/sara/sara/statutes/prolog/events.pl#L9) | [s152_c_3_neg.pl:9](../../human/sara/sara/cases/s152_c_3_neg.pl#L9) |
| `blindness_/1` | 7 / 0 | G: `(A)` | [E10](../../human/sara/sara/statutes/prolog/events.pl#L10) | [s63_f_2_A_neg.pl:17](../../human/sara/sara/cases/s63_f_2_A_neg.pl#L17) |
| `brother_/1` | 13 / 0 | G: `(A)` | [E11](../../human/sara/sara/statutes/prolog/events.pl#L11) | [s152_c_2_A_neg.pl:9](../../human/sara/sara/cases/s152_c_2_A_neg.pl#L9) |
| `business_/1` | 2 / 0 | G: `(A)` | [E12](../../human/sara/sara/statutes/prolog/events.pl#L12) | [s3306_b_7_neg.pl:10](../../human/sara/sara/cases/s3306_b_7_neg.pl#L10) |
| `business_trust_/1` | 2 / 0 | G: `(A)` | [E13](../../human/sara/sara/statutes/prolog/events.pl#L13) | [s63_c_6_D_neg.pl:9](../../human/sara/sara/cases/s63_c_6_D_neg.pl#L9) |
| `citizenship_/1` | 14 / 0 | G: `(A)` | [E14](../../human/sara/sara/statutes/prolog/events.pl#L14) | [s3306_c_1_A_i_neg.pl:23](../../human/sara/sara/cases/s3306_c_1_A_i_neg.pl#L23) |
| `country_/2` | 14 / 0 | G: `(D, D)` | [E15](../../human/sara/sara/statutes/prolog/events.pl#L15) | [s3306_c_1_A_i_neg.pl:15](../../human/sara/sara/cases/s3306_c_1_A_i_neg.pl#L15) |
| `daughter_/1` | 1 / 0 | G: `(A)` | [E16](../../human/sara/sara/statutes/prolog/events.pl#L16) | [tax_case_20.pl:23](../../human/sara/sara/cases/tax_case_20.pl#L23) |
| `death_/1` | 50 / 0 | G: `(A)` | [E17](../../human/sara/sara/statutes/prolog/events.pl#L17) | [s2_a_1_A_neg.pl:13](../../human/sara/sara/cases/s2_a_1_A_neg.pl#L13) |
| `deduction_/1` | 20 / 0 | G: `(A)` | [E18](../../human/sara/sara/statutes/prolog/events.pl#L18) | [s63_a_pos.pl:15](../../human/sara/sara/cases/s63_a_pos.pl#L15) |
| `destination_/2` | 1 / 0 | G: `(A, D)` | [E19](../../human/sara/sara/statutes/prolog/events.pl#L19) | [s3306_c_1_B_neg.pl:30](../../human/sara/sara/cases/s3306_c_1_B_neg.pl#L30) |
| `disability_/1` | 4 / 0 | G: `(A)` | [E20](../../human/sara/sara/statutes/prolog/events.pl#L20) | [s3306_b_10_A_pos.pl:14](../../human/sara/sara/cases/s3306_b_10_A_pos.pl#L14) |
| `educational_institution_/1` | 7 / 0 | G: `(A)` | [E21](../../human/sara/sara/statutes/prolog/events.pl#L21) | [s3306_c_10_A_i_neg.pl:9](../../human/sara/sara/cases/s3306_c_10_A_i_neg.pl#L9) |
| `end_/2` | 400 / 0 | G: `(A, D)` | [E22](../../human/sara/sara/statutes/prolog/events.pl#L22) | [s151_a_neg.pl:13](../../human/sara/sara/cases/s151_a_neg.pl#L13) |
| `enrollment_/1` | 8 / 0 | G: `(A)` | [E23](../../human/sara/sara/statutes/prolog/events.pl#L23) | [s3306_c_10_A_i_neg.pl:25](../../human/sara/sara/cases/s3306_c_10_A_i_neg.pl#L25) |
| `father_/1` | 35 / 0 | G: `(A)` | [E24](../../human/sara/sara/statutes/prolog/events.pl#L24) | [s152_d_1_D_neg.pl:16](../../human/sara/sara/cases/s152_d_1_D_neg.pl#L16) |
| `hospital_/1` | 4 / 0 | G: `(A)` | [E27](../../human/sara/sara/statutes/prolog/events.pl#L27) | [s3306_c_10_B_neg.pl:9](../../human/sara/sara/cases/s3306_c_10_B_neg.pl#L9) |
| `incarceration_/1` | 3 / 0 | G: `(A)` | [E28](../../human/sara/sara/statutes/prolog/events.pl#L28) | [s3306_c_21_neg.pl:22](../../human/sara/sara/cases/s3306_c_21_neg.pl#L22) |
| `income_/1` | 120 / 0 | G: `(A)` | [E29](../../human/sara/sara/statutes/prolog/events.pl#L29) | [s151_a_neg.pl:10](../../human/sara/sara/cases/s151_a_neg.pl#L10) |
| `international_organization_/1` | 1 / 0 | G: `(A)` | [E30](../../human/sara/sara/statutes/prolog/events.pl#L30) | [s3306_c_16_pos.pl:9](../../human/sara/sara/cases/s3306_c_16_pos.pl#L9) |
| `joint_return_/1` | 53 / 0 | G: `(A)` | [E33](../../human/sara/sara/statutes/prolog/events.pl#L33) | [s151_b_neg.pl:13](../../human/sara/sara/cases/s151_b_neg.pl#L13) |
| `legal_separation_/1` | 6 / 0 | G: `(A)` | [E35](../../human/sara/sara/statutes/prolog/events.pl#L35) | [s2_b_2_A_neg.pl:13](../../human/sara/sara/cases/s2_b_2_A_neg.pl#L13) |
| `location_/2` | 113 / 0 | G: `(A, A/D)` | [E36](../../human/sara/sara/statutes/prolog/events.pl#L36) | [s3306_a_3_neg.pl:30](../../human/sara/sara/cases/s3306_a_3_neg.pl#L30); [s3306_c_10_A_i_neg.pl:16](../../human/sara/sara/cases/s3306_c_10_A_i_neg.pl#L16) |
| `marriage_/1` | 156 / 0 | G: `(A)` | [E37](../../human/sara/sara/statutes/prolog/events.pl#L37) | [s151_b_neg.pl:9](../../human/sara/sara/cases/s151_b_neg.pl#L9) |
| `means_/2` | 13 / 0 | G: `(A, A/D)` | [E38](../../human/sara/sara/statutes/prolog/events.pl#L38) | [s3306_a_3_neg.pl:22](../../human/sara/sara/cases/s3306_a_3_neg.pl#L22); [s3306_b_10_B_pos.pl:31](../../human/sara/sara/cases/s3306_b_10_B_pos.pl#L31) |
| `medical_institution_/1` | 1 / 0 | G: `(A)` | [E39](../../human/sara/sara/statutes/prolog/events.pl#L39) | [s3306_c_21_neg.pl:20](../../human/sara/sara/cases/s3306_c_21_neg.pl#L20) |
| `medical_patient_/1` | 4 / 0 | G: `(A)` | [E40](../../human/sara/sara/statutes/prolog/events.pl#L40) | [s3306_c_10_B_neg.pl:25](../../human/sara/sara/cases/s3306_c_10_B_neg.pl#L25) |
| `migration_/1` | 1 / 0 | G: `(A)` | [E41](../../human/sara/sara/statutes/prolog/events.pl#L41) | [s3306_c_1_B_neg.pl:29](../../human/sara/sara/cases/s3306_c_1_B_neg.pl#L29) |
| `mother_/1` | 3 / 0 | G: `(A)` | [E42](../../human/sara/sara/statutes/prolog/events.pl#L42) | [s152_d_2_C_neg.pl:13](../../human/sara/sara/cases/s152_d_2_C_neg.pl#L13) |
| `nonresident_alien_/1` | 14 / 0 | G: `(A)` | [E43](../../human/sara/sara/statutes/prolog/events.pl#L43) | [s2_a_2_B_neg.pl:17](../../human/sara/sara/cases/s2_a_2_B_neg.pl#L17) |
| `nurses_training_school_/1` | 1 / 0 | G: `(A)` | [E44](../../human/sara/sara/statutes/prolog/events.pl#L44) | [s3306_c_13_pos.pl:23](../../human/sara/sara/cases/s3306_c_13_pos.pl#L23) |
| `patient/2` | 2 / 0 | G: `(A, A)` | [E45](../../human/sara/sara/statutes/prolog/events.pl#L45) | [tax_case_25.pl:11](../../human/sara/sara/cases/tax_case_25.pl#L11) |
| `patient_/2` | 615 / 0 | G: `(A, A/D)` | [E46](../../human/sara/sara/statutes/prolog/events.pl#L46) | [s152_c_1_B_neg.pl:11](../../human/sara/sara/cases/s152_c_1_B_neg.pl#L11); [s3306_c_10_A_i_neg.pl:12](../../human/sara/sara/cases/s3306_c_10_A_i_neg.pl#L12) |
| `payment_/1` | 209 / 0 | G: `(A)` | [E47](../../human/sara/sara/statutes/prolog/events.pl#L47) | [s3306_a_1_neg.pl:16](../../human/sara/sara/cases/s3306_a_1_neg.pl#L16) |
| `penal_institution_/1` | 2 / 0 | G: `(A)` | [E48](../../human/sara/sara/statutes/prolog/events.pl#L48) | [s3306_c_21_pos.pl:20](../../human/sara/sara/cases/s3306_c_21_pos.pl#L20) |
| `plan_/1` | 17 / 0 | G: `(A)` | [E49](../../human/sara/sara/statutes/prolog/events.pl#L49) | [s3306_b_10_B_pos.pl:32](../../human/sara/sara/cases/s3306_b_10_B_pos.pl#L32) |
| `purpose_/2` | 176 / 2 | G: `(A, A/D)`; N: `(V, D)` | [E50](../../human/sara/sara/statutes/prolog/events.pl#L50) | [s3306_a_1_neg.pl:15](../../human/sara/sara/cases/s3306_a_1_neg.pl#L15); [s3306_a_1_neg.pl:20](../../human/sara/sara/cases/s3306_a_1_neg.pl#L20); [s3306_a_2_B_neg.pl:75](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L75) |
| `reason_/2` | 10 / 0 | G: `(A, A/D)` | [E51](../../human/sara/sara/statutes/prolog/events.pl#L51) | [s3306_b_10_A_neg.pl:20](../../human/sara/sara/cases/s3306_b_10_A_neg.pl#L20); [s3306_b_10_A_pos.pl:20](../../human/sara/sara/cases/s3306_b_10_A_pos.pl#L20) |
| `residence_/1` | 141 / 0 | G: `(A)` | [E52](../../human/sara/sara/statutes/prolog/events.pl#L52) | [s152_c_1_B_neg.pl:12](../../human/sara/sara/cases/s152_c_1_B_neg.pl#L12) |
| `retirement_/1` | 11 / 0 | G: `(A)` | [E53](../../human/sara/sara/statutes/prolog/events.pl#L53) | [s3306_b_10_A_neg.pl:17](../../human/sara/sara/cases/s3306_b_10_A_neg.pl#L17) |
| `s151/5` | 0 / 5 | N: `(A, I, L[A]/V, V, I)` | — | [s63_a_neg.pl:16](../../human/sara/sara/cases/s63_a_neg.pl#L16); [s63_d_2_pos.pl:14](../../human/sara/sara/cases/s63_d_2_pos.pl#L14) |
| `s151_b/3` | 1 / 0 | G: `(A, I, I)` | — | [s63_d_neg.pl:14](../../human/sara/sara/cases/s63_d_neg.pl#L14) |
| `s151_b_applies/2` | 4 / 0 | G: `(A, I)` | — | [s151_d_1_neg.pl:10](../../human/sara/sara/cases/s151_d_1_neg.pl#L10) |
| `s151_b_applies/3` | 5 / 0 | G: `(A, A, I)` | — | [s63_c_5_pos.pl:18](../../human/sara/sara/cases/s63_c_5_pos.pl#L18) |
| `s151_c/4` | 0 / 4 | N: `(A, V, I, I)` | — | [s151_a_neg.pl:15](../../human/sara/sara/cases/s151_a_neg.pl#L15) |
| `s151_c_applies/3` | 1 / 0 | G: `(A, A, I)` | — | [s151_d_2_pos.pl:10](../../human/sara/sara/cases/s151_d_2_pos.pl#L10) |
| `s151_d/4` | 0 / 5 | N: `(A, A/V, I/V, I)` | — | [s151_d_2_neg.pl:10](../../human/sara/sara/cases/s151_d_2_neg.pl#L10); [s152_d_1_B_neg.pl:15](../../human/sara/sara/cases/s152_d_1_B_neg.pl#L15) |
| `s152_b_2/4` | 0 / 2 | N: `(A, V, A, I)` | — | [s2_b_1_A_i_II_pos.pl:44](../../human/sara/sara/cases/s2_b_1_A_i_II_pos.pl#L44) |
| `s152_c/3` | 1 / 0 | G: `(A, A, I)` | — | [s152_d_1_D_neg.pl:19](../../human/sara/sara/cases/s152_d_1_D_neg.pl#L19) |
| `s152_c_1/3` | 8 / 0 | G: `(A, A, I)` | — | [s151_c_neg.pl:14](../../human/sara/sara/cases/s151_c_neg.pl#L14) |
| `s152_c_2/4` | 2 / 0 | G: `(A, A, D, D)` | — | [s152_c_1_neg.pl:23](../../human/sara/sara/cases/s152_c_1_neg.pl#L23) |
| `s2_a/3` | 0 / 19 | N: `(A, V, I)` | — | [s1_a_2_i_neg.pl:11](../../human/sara/sara/cases/s1_a_2_i_neg.pl#L11) |
| `s2_a/5` | 0 / 1 | N: `(A, V, V, V, I)` | — | [s1_a_2_i_pos.pl:11](../../human/sara/sara/cases/s1_a_2_i_pos.pl#L11) |
| `s2_b/3` | 0 / 19 | N: `(A, V, I)` | — | [s1_a_1_neg.pl:11](../../human/sara/sara/cases/s1_a_1_neg.pl#L11) |
| `s3306_b/8` | 0 / 18 | N: `(I, A/V, A, A, A, A, A, V)` | — | [s3306_a_1_A_neg.pl:10](../../human/sara/sara/cases/s3306_a_1_A_neg.pl#L10); [s3306_a_1_neg.pl:22](../../human/sara/sara/cases/s3306_a_1_neg.pl#L22) |
| `s63/3` | 60 / 0 | G: `(A, I, I)` | — | [s1_a_1_i_neg.pl:17](../../human/sara/sara/cases/s1_a_1_i_neg.pl#L17) |
| `s63_c/3` | 1 / 0 | G: `(A, I, I)` | — | [s63_a_neg.pl:15](../../human/sara/sara/cases/s63_a_neg.pl#L15) |
| `s63_c_1/3` | 2 / 0 | G: `(A, I, I)` | — | [s63_b_neg.pl:15](../../human/sara/sara/cases/s63_b_neg.pl#L15) |
| `s63_c_2/3` | 2 / 0 | G: `(A, I, I)` | — | [s63_c_1_neg.pl:15](../../human/sara/sara/cases/s63_c_1_neg.pl#L15) |
| `s63_c_3/3` | 2 / 0 | G: `(A, I, I)` | — | [s63_c_1_neg.pl:16](../../human/sara/sara/cases/s63_c_1_neg.pl#L16) |
| `s63_c_3/4` | 0 / 1 | N: `(A, V, I, I)` | — | [s63_d_2_neg.pl:14](../../human/sara/sara/cases/s63_d_2_neg.pl#L14) |
| `s63_d/4` | 0 / 2 | N: `(A, V, I, I)` | — | [s68_a_2_neg.pl:15](../../human/sara/sara/cases/s68_a_2_neg.pl#L15) |
| `s63_f_1_A/2` | 2 / 0 | G: `(A, I)` | — | [s63_c_3_neg.pl:19](../../human/sara/sara/cases/s63_c_3_neg.pl#L19) |
| `s63_f_1_B/3` | 2 / 0 | G: `(A, A, I)` | — | [s63_c_3_neg.pl:20](../../human/sara/sara/cases/s63_c_3_neg.pl#L20) |
| `s68_b/3` | 2 / 0 | G: `(A, I, I)` | — | [s151_d_3_B_neg.pl:15](../../human/sara/sara/cases/s151_d_3_B_neg.pl#L15) |
| `s7703/4` | 0 / 26 | N: `(A, A/V, V, I)` | — | [s1_a_1_i_neg.pl:11](../../human/sara/sara/cases/s1_a_1_i_neg.pl#L11); [s68_b_1_A_neg.pl:14](../../human/sara/sara/cases/s68_b_1_A_neg.pl#L14) |
| `service_/1` | 91 / 0 | G: `(A)` | [E54](../../human/sara/sara/statutes/prolog/events.pl#L54) | [s3306_a_1_neg.pl:10](../../human/sara/sara/cases/s3306_a_1_neg.pl#L10) |
| `sibling_/1` | 2 / 0 | G: `(A)` | [E55](../../human/sara/sara/statutes/prolog/events.pl#L55) | [s3306_c_5_neg.pl:23](../../human/sara/sara/cases/s3306_c_5_neg.pl#L23) |
| `sister_/1` | 3 / 0 | G: `(A)` | [E56](../../human/sara/sara/statutes/prolog/events.pl#L56) | [s152_d_2_E_neg.pl:13](../../human/sara/sara/cases/s152_d_2_E_neg.pl#L13) |
| `son_/1` | 72 / 0 | G: `(A)` | [E57](../../human/sara/sara/statutes/prolog/events.pl#L57) | [s152_c_1_B_neg.pl:9](../../human/sara/sara/cases/s152_c_1_B_neg.pl#L9) |
| `start_/2` | 1000 / 0 | G: `(A, D)` | [E58](../../human/sara/sara/statutes/prolog/events.pl#L58) | [s151_a_neg.pl:12](../../human/sara/sara/cases/s151_a_neg.pl#L12) |
| `termination_/1` | 5 / 0 | G: `(A)` | [E59](../../human/sara/sara/statutes/prolog/events.pl#L59) | [s3306_b_10_A_neg.pl:14](../../human/sara/sara/cases/s3306_b_10_A_neg.pl#L14) |
| `total_wages_employer/6` | 0 / 4 | N: `(A, I, V, V, D, D)` | — | [s3301_neg.pl:12](../../human/sara/sara/cases/s3301_neg.pl#L12) |
| `type_/2` | 4 / 0 | G: `(A, D)` | [E60](../../human/sara/sara/statutes/prolog/events.pl#L60) | [s3306_b_7_neg.pl:12](../../human/sara/sara/cases/s3306_b_7_neg.pl#L12) |

### All 27 rule-head predicate/arity pairs

These 434 rules remain unsupported source records, including rules for the
14 signatures that also have bodyless occurrences. The 13 rule-only signatures
do not get a bodyless fact constructor. `V` here includes named variables.

| Predicate/arity | Rule count | Rule-head shapes | Event declaration | Source witnesses for all displayed shapes |
| --- | ---: | --- | --- | --- |
| `agent_/2` | 60 | `(V, A/V)` | [E1](../../human/sara/sara/statutes/prolog/events.pl#L1) | [s2_a_1_B_neg.pl:32](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L32); [tax_case_10.pl:48](../../human/sara/sara/cases/tax_case_10.pl#L48) |
| `agricultural_service/3` | 2 | `(V, V, V)` | [E2](../../human/sara/sara/statutes/prolog/events.pl#L2) | [tax_case_83.pl:27](../../human/sara/sara/cases/tax_case_83.pl#L27) |
| `alice_employer/3` | 1 | `(V, V, V)` | [E3](../../human/sara/sara/statutes/prolog/events.pl#L3) | [tax_case_10.pl:43](../../human/sara/sara/cases/tax_case_10.pl#L43) |
| `alice_household_maintenance/4` | 10 | `(V, V, V, V)` | [E4](../../human/sara/sara/statutes/prolog/events.pl#L4) | [s7703_b_1_neg.pl:27](../../human/sara/sara/cases/s7703_b_1_neg.pl#L27) |
| `amount_/2` | 52 | `(V, I)` | [E6](../../human/sara/sara/statutes/prolog/events.pl#L6) | [s2_a_1_B_neg.pl:33](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L33) |
| `bob_household_maintenance/4` | 32 | `(V, V, V, V)` | — | [s2_a_1_B_neg.pl:26](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L26) |
| `bob_income/3` | 1 | `(V, V, V)` | — | [tax_case_90.pl:38](../../human/sara/sara/cases/tax_case_90.pl#L38) |
| `bob_income/4` | 1 | `(V, V, V, V)` | — | [s2_b_3_B_pos.pl:37](../../human/sara/sara/cases/s2_b_3_B_pos.pl#L37) |
| `end_/2` | 53 | `(V, D/V)` | [E22](../../human/sara/sara/statutes/prolog/events.pl#L22) | [s2_a_1_B_neg.pl:36](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L36); [tax_case_10.pl:51](../../human/sara/sara/cases/tax_case_10.pl#L51) |
| `income_/1` | 2 | `(V)` | [E29](../../human/sara/sara/statutes/prolog/events.pl#L29) | [s2_b_3_B_pos.pl:42](../../human/sara/sara/cases/s2_b_3_B_pos.pl#L42) |
| `joint_return_/1` | 2 | `(V)` | [E33](../../human/sara/sara/statutes/prolog/events.pl#L33) | [s7703_b_2_pos.pl:41](../../human/sara/sara/cases/s7703_b_2_pos.pl#L41) |
| `joint_return_alice_and_bob/4` | 2 | `(V, V, V, V)` | — | [s7703_b_2_pos.pl:36](../../human/sara/sara/cases/s7703_b_2_pos.pl#L36) |
| `patient_/2` | 9 | `(V, A/V)` | [E46](../../human/sara/sara/statutes/prolog/events.pl#L46) | [tax_case_10.pl:49](../../human/sara/sara/cases/tax_case_10.pl#L49); [tax_case_10.pl:53](../../human/sara/sara/cases/tax_case_10.pl#L53) |
| `payment_/1` | 50 | `(V)` | [E47](../../human/sara/sara/statutes/prolog/events.pl#L47) | [s2_a_1_B_neg.pl:31](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L31) |
| `payment_for_labor/4` | 2 | `(V, V, V, V)` | — | [tax_case_83.pl:89](../../human/sara/sara/cases/tax_case_83.pl#L89) |
| `purpose_/2` | 52 | `(V, A/D/V)` | [E50](../../human/sara/sara/statutes/prolog/events.pl#L50) | [s2_a_1_B_neg.pl:34](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L34); [tax_case_10.pl:57](../../human/sara/sara/cases/tax_case_10.pl#L57); [tax_case_10.pl:58](../../human/sara/sara/cases/tax_case_10.pl#L58) |
| `s151/5` | 1 | `(A, V, L[A], L[I], V)` | — | [s2_a_1_B_pos.pl:40](../../human/sara/sara/cases/s2_a_1_B_pos.pl#L40) |
| `s151_c_applies/3` | 14 | `(A, A, V)` | — | [s2_b_1_A_ii_pos.pl:39](../../human/sara/sara/cases/s2_b_1_A_ii_pos.pl#L39) |
| `s152_c/3` | 1 | `(A, A, V)` | — | [s2_b_1_A_pos.pl:40](../../human/sara/sara/cases/s2_b_1_A_pos.pl#L40) |
| `s152_c_3/3` | 1 | `(A, A, V)` | — | [s152_c_1_pos.pl:25](../../human/sara/sara/cases/s152_c_1_pos.pl#L25) |
| `s152_d_2_H/6` | 1 | `(A, A, V, V, V, V)` | — | [s2_b_3_B_pos.pl:35](../../human/sara/sara/cases/s2_b_3_B_pos.pl#L35) |
| `s3306_a/2` | 2 | `(A, V)` | — | [s3301_neg.pl:11](../../human/sara/sara/cases/s3301_neg.pl#L11) |
| `s3306_b/8` | 2 | `(I, A, A, A, A, A, A, V)` | — | [s3306_c_2_neg.pl:26](../../human/sara/sara/cases/s3306_c_2_neg.pl#L26) |
| `s3306_c/5` | 8 | `(A/V, A, A/V, V, V)` | — | [s3306_a_1_B_neg.pl:20](../../human/sara/sara/cases/s3306_a_1_B_neg.pl#L20); [s3306_b_15_neg.pl:10](../../human/sara/sara/cases/s3306_b_15_neg.pl#L10); [s3306_a_2_B_neg.pl:22](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L22) |
| `service_/1` | 5 | `(V)` | [E54](../../human/sara/sara/statutes/prolog/events.pl#L54) | [tax_case_10.pl:47](../../human/sara/sara/cases/tax_case_10.pl#L47) |
| `someone_household_maintenance/4` | 3 | `(V, V, V, V)` | — | [s2_b_1_A_neg.pl:39](../../human/sara/sara/cases/s2_b_1_A_neg.pl#L39) |
| `start_/2` | 65 | `(A/V, D/V)` | [E58](../../human/sara/sara/statutes/prolog/events.pl#L58) | [s2_a_1_B_neg.pl:35](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L35); [tax_case_10.pl:38](../../human/sara/sara/cases/tax_case_10.pl#L38); [tax_case_10.pl:50](../../human/sara/sara/cases/tax_case_10.pl#L50) |

### Event declarations without any case clause head

The preceding tables account for 55 of the 61 event declarations (52 with
bodyless occurrences and three rule-only signatures). These six complete the
event declaration inventory. A discontiguous declaration is not a fact, a type,
a proof of existence, or permission to insert an absent predicate.

| Predicate/arity | Event declaration | Observed use in cases |
| --- | --- | --- |
| `first_day_year/2` | [E25](../../human/sara/sara/statutes/prolog/events.pl#L25) | Directive call: [s152_d_2_D_neg.pl:21](../../human/sara/sara/cases/s152_d_2_D_neg.pl#L21); Rule-body call: [s2_a_1_B_neg.pl:29](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L29) |
| `gross_income/3` | [E26](../../human/sara/sara/statutes/prolog/events.pl#L26) | Directive call: [s68_a_1_neg.pl:19](../../human/sara/sara/cases/s68_a_1_neg.pl#L19) |
| `is_before/2` | [E31](../../human/sara/sara/statutes/prolog/events.pl#L31) | Directive call: [s152_d_2_D_neg.pl:22](../../human/sara/sara/cases/s152_d_2_D_neg.pl#L22); Rule-body call: [s3306_b_15_neg.pl:13](../../human/sara/sara/cases/s3306_b_15_neg.pl#L13) |
| `itemize_deductions_/1` | [E32](../../human/sara/sara/statutes/prolog/events.pl#L32) | No occurrence in the cases |
| `last_day_year/2` | [E34](../../human/sara/sara/statutes/prolog/events.pl#L34) | Rule-body call: [s2_a_1_B_neg.pl:30](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L30) |
| `unemployment_compensation_agreement_/1` | [E61](../../human/sara/sara/statutes/prolog/events.pl#L61) | No occurrence in the cases |

### Remaining 129 named signatures: calls only

These signatures occur in case rule bodies or directives but never as case
clause heads or `events.pl` declarations. They do not get fact constructors.
Calls of signatures already listed above remain calls, regardless of whether
that same signature also occurs as a fact elsewhere. No imported definitions
were inspected or inferred.

| Predicate/arity | Observed context | Source |
| --- | --- | --- |
| `atom_concat/3` | Rule-body call | [s2_a_1_B_neg.pl:28](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L28) |
| `atom_number/2` | Rule-body call | [tax_case_33.pl:35](../../human/sara/sara/cases/tax_case_33.pl#L35) |
| `between/3` | Rule-body call | [s152_c_1_pos.pl:25](../../human/sara/sara/cases/s152_c_1_pos.pl#L25) |
| `member/2` | Rule-body call | [s3306_a_1_B_neg.pl:21](../../human/sara/sara/cases/s3306_a_1_B_neg.pl#L21) |
| `nonvar/1` | Rule-body call | [s3306_b_15_neg.pl:12](../../human/sara/sara/cases/s3306_b_15_neg.pl#L12) |
| `s151_a/3` | Directive/test call | [s151_a_neg.pl:18](../../human/sara/sara/cases/s151_a_neg.pl#L18) |
| `s151_b/4` | Directive/test call | [s151_b_pos.pl:15](../../human/sara/sara/cases/s151_b_pos.pl#L15) |
| `s151_d_1/1` | Directive/test call | [s151_d_1_neg.pl:13](../../human/sara/sara/cases/s151_d_1_neg.pl#L13) |
| `s151_d_2/4` | Directive/test call | [s151_d_2_neg.pl:13](../../human/sara/sara/cases/s151_d_2_neg.pl#L13) |
| `s151_d_3_A/7` | Directive/test call | [s151_d_3_A_neg.pl:18](../../human/sara/sara/cases/s151_d_3_A_neg.pl#L18) |
| `s151_d_3_B/5` | Directive/test call | [s151_d_3_B_neg.pl:18](../../human/sara/sara/cases/s151_d_3_B_neg.pl#L18) |
| `s151_d_5/2` | Directive/test call | [s151_d_5_neg.pl:13](../../human/sara/sara/cases/s151_d_5_neg.pl#L13) |
| `s152_a/5` | Directive/test call | [s152_a_neg.pl:13](../../human/sara/sara/cases/s152_a_neg.pl#L13) |
| `s152_b_1/3` | Directive/test call | [s152_b_1_neg.pl:14](../../human/sara/sara/cases/s152_b_1_neg.pl#L14) |
| `s152_c_1_B/6` | Directive/test call | [s152_c_1_B_neg.pl:20](../../human/sara/sara/cases/s152_c_1_B_neg.pl#L20) |
| `s152_c_1_E/3` | Directive/test call | [s152_c_1_E_neg.pl:29](../../human/sara/sara/cases/s152_c_1_E_neg.pl#L29) |
| `s152_c_2_A/5` | Directive/test call | [s152_c_2_A_neg.pl:15](../../human/sara/sara/cases/s152_c_2_A_neg.pl#L15) |
| `s152_c_2_B/5` | Directive/test call | [s152_c_2_B_neg.pl:15](../../human/sara/sara/cases/s152_c_2_B_neg.pl#L15) |
| `s152_d_1_B/2` | Directive/test call | [s152_d_1_B_neg.pl:18](../../human/sara/sara/cases/s152_d_1_B_neg.pl#L18) |
| `s152_d_1_D/2` | Directive/test call | [s152_d_1_D_neg.pl:23](../../human/sara/sara/cases/s152_d_1_D_neg.pl#L23) |
| `s152_d_2_A/4` | Directive/test call | [s152_d_2_A_neg.pl:15](../../human/sara/sara/cases/s152_d_2_A_neg.pl#L15) |
| `s152_d_2_B/4` | Directive/test call | [s152_d_2_B_neg.pl:15](../../human/sara/sara/cases/s152_d_2_B_neg.pl#L15) |
| `s152_d_2_C/4` | Directive/test call | [s152_d_2_C_neg.pl:23](../../human/sara/sara/cases/s152_d_2_C_neg.pl#L23) |
| `s152_d_2_D/4` | Directive/test call | [s152_d_2_D_neg.pl:19](../../human/sara/sara/cases/s152_d_2_D_neg.pl#L19) |
| `s152_d_2_E/5` | Directive/test call | [s152_d_2_E_neg.pl:19](../../human/sara/sara/cases/s152_d_2_E_neg.pl#L19) |
| `s152_d_2_F/5` | Directive/test call | [s152_d_2_F_neg.pl:19](../../human/sara/sara/cases/s152_d_2_F_neg.pl#L19) |
| `s152_d_2_G/4` | Directive/test call | [s152_d_2_G_neg.pl:16](../../human/sara/sara/cases/s152_d_2_G_neg.pl#L16) |
| `s1_a/4` | Directive/test call | [s1_a_1_neg.pl:15](../../human/sara/sara/cases/s1_a_1_neg.pl#L15) |
| `s1_a_i/2` | Directive/test call | [s1_a_1_i_neg.pl:20](../../human/sara/sara/cases/s1_a_1_i_neg.pl#L20) |
| `s1_a_ii/2` | Directive/test call | [s1_a_1_ii_neg.pl:20](../../human/sara/sara/cases/s1_a_1_ii_neg.pl#L20) |
| `s1_a_iii/2` | Directive/test call | [s1_a_1_iii_neg.pl:20](../../human/sara/sara/cases/s1_a_1_iii_neg.pl#L20) |
| `s1_a_iv/2` | Directive/test call | [s1_a_1_iv_neg.pl:20](../../human/sara/sara/cases/s1_a_1_iv_neg.pl#L20) |
| `s1_a_v/2` | Directive/test call | [s1_a_1_v_neg.pl:20](../../human/sara/sara/cases/s1_a_1_v_neg.pl#L20) |
| `s1_b/4` | Directive/test call | [s1_b_neg.pl:15](../../human/sara/sara/cases/s1_b_neg.pl#L15) |
| `s1_b_i/2` | Directive/test call | [s1_b_i_neg.pl:15](../../human/sara/sara/cases/s1_b_i_neg.pl#L15) |
| `s1_b_ii/2` | Directive/test call | [s1_b_ii_neg.pl:15](../../human/sara/sara/cases/s1_b_ii_neg.pl#L15) |
| `s1_b_iii/2` | Directive/test call | [s1_b_iii_neg.pl:15](../../human/sara/sara/cases/s1_b_iii_neg.pl#L15) |
| `s1_b_iv/2` | Directive/test call | [s1_b_iv_neg.pl:15](../../human/sara/sara/cases/s1_b_iv_neg.pl#L15) |
| `s1_b_v/2` | Directive/test call | [s1_b_v_neg.pl:15](../../human/sara/sara/cases/s1_b_v_neg.pl#L15) |
| `s1_c/4` | Directive/test call | [s1_c_neg.pl:20](../../human/sara/sara/cases/s1_c_neg.pl#L20) |
| `s1_c_i/2` | Directive/test call | [s1_c_i_neg.pl:13](../../human/sara/sara/cases/s1_c_i_neg.pl#L13) |
| `s1_c_ii/2` | Directive/test call | [s1_c_ii_neg.pl:13](../../human/sara/sara/cases/s1_c_ii_neg.pl#L13) |
| `s1_c_iii/2` | Directive/test call | [s1_c_iii_neg.pl:13](../../human/sara/sara/cases/s1_c_iii_neg.pl#L13) |
| `s1_c_iv/2` | Directive/test call | [s1_c_iv_neg.pl:13](../../human/sara/sara/cases/s1_c_iv_neg.pl#L13) |
| `s1_c_v/2` | Directive/test call | [s1_c_v_neg.pl:13](../../human/sara/sara/cases/s1_c_v_neg.pl#L13) |
| `s1_d/5` | Directive/test call | [s1_d_neg.pl:15](../../human/sara/sara/cases/s1_d_neg.pl#L15) |
| `s1_d_i/2` | Directive/test call | [s1_d_i_neg.pl:15](../../human/sara/sara/cases/s1_d_i_neg.pl#L15) |
| `s1_d_ii/2` | Directive/test call | [s1_d_ii_neg.pl:15](../../human/sara/sara/cases/s1_d_ii_neg.pl#L15) |
| `s1_d_iii/2` | Directive/test call | [s1_d_iii_neg.pl:15](../../human/sara/sara/cases/s1_d_iii_neg.pl#L15) |
| `s1_d_iv/2` | Directive/test call | [s1_d_iv_neg.pl:15](../../human/sara/sara/cases/s1_d_iv_neg.pl#L15) |
| `s1_d_v/2` | Directive/test call | [s1_d_v_neg.pl:15](../../human/sara/sara/cases/s1_d_v_neg.pl#L15) |
| `s2_a_1_A/5` | Directive/test call | [s2_a_1_A_neg.pl:18](../../human/sara/sara/cases/s2_a_1_A_neg.pl#L18) |
| `s2_a_1_B/4` | Directive/test call | [s2_a_1_B_neg.pl:52](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L52) |
| `s2_a_2_A/5` | Directive/test call | [s2_a_2_A_neg.pl:23](../../human/sara/sara/cases/s2_a_2_A_neg.pl#L23) |
| `s2_a_2_B/3` | Directive/test call | [s2_a_2_B_neg.pl:22](../../human/sara/sara/cases/s2_a_2_B_neg.pl#L22) |
| `s2_b_1/4` | Directive/test call | [s2_b_1_neg.pl:41](../../human/sara/sara/cases/s2_b_1_neg.pl#L41) |
| `s2_b_1_A/4` | Directive/test call | [s2_b_1_A_neg.pl:52](../../human/sara/sara/cases/s2_b_1_A_neg.pl#L52) |
| `s2_b_1_A_i/3` | Directive/test call | [s2_b_1_A_i_neg.pl:47](../../human/sara/sara/cases/s2_b_1_A_i_neg.pl#L47) |
| `s2_b_1_A_i_I/2` | Directive/test call | [s2_b_1_A_i_I_neg.pl:45](../../human/sara/sara/cases/s2_b_1_A_i_I_neg.pl#L45) |
| `s2_b_1_A_i_II/3` | Directive/test call | [s2_b_1_A_i_II_neg.pl:45](../../human/sara/sara/cases/s2_b_1_A_i_II_neg.pl#L45) |
| `s2_b_1_A_ii/3` | Directive/test call | [s2_b_1_A_ii_neg.pl:53](../../human/sara/sara/cases/s2_b_1_A_ii_neg.pl#L53) |
| `s2_b_1_B/5` | Directive/test call | [s2_b_1_B_neg.pl:43](../../human/sara/sara/cases/s2_b_1_B_neg.pl#L43) |
| `s2_b_2_A/5` | Directive/test call | [s2_b_2_A_neg.pl:19](../../human/sara/sara/cases/s2_b_2_A_neg.pl#L19) |
| `s2_b_2_B/3` | Directive/test call | [s2_b_2_B_neg.pl:18](../../human/sara/sara/cases/s2_b_2_B_neg.pl#L18) |
| `s2_b_2_C/4` | Directive/test call | [s2_b_2_C_neg.pl:21](../../human/sara/sara/cases/s2_b_2_C_neg.pl#L21) |
| `s2_b_3_A/3` | Directive/test call | [s2_b_3_A_neg.pl:44](../../human/sara/sara/cases/s2_b_3_A_neg.pl#L44) |
| `s2_b_3_B/3` | Directive/test call | [s2_b_3_B_neg.pl:41](../../human/sara/sara/cases/s2_b_3_B_neg.pl#L41) |
| `s3301/6` | Directive/test call | [s3301_neg.pl:16](../../human/sara/sara/cases/s3301_neg.pl#L16) |
| `s3306_a_1/2` | Directive/test call | [s3306_a_1_neg.pl:37](../../human/sara/sara/cases/s3306_a_1_neg.pl#L37) |
| `s3306_a_1_A/3` | Directive/test call | [s3306_a_1_A_neg.pl:18](../../human/sara/sara/cases/s3306_a_1_A_neg.pl#L18) |
| `s3306_a_1_B/4` | Directive/test call | [s3306_a_1_B_neg.pl:25](../../human/sara/sara/cases/s3306_a_1_B_neg.pl#L25) |
| `s3306_a_2_A/4` | Directive/test call | [s3306_a_2_A_neg.pl:37](../../human/sara/sara/cases/s3306_a_2_A_neg.pl#L37) |
| `s3306_a_2_B/6` | Directive/test call | [s3306_a_2_B_neg.pl:78](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L78) |
| `s3306_a_3/4` | Directive/test call | [s3306_a_3_neg.pl:41](../../human/sara/sara/cases/s3306_a_3_neg.pl#L41) |
| `s3306_b_10_A/6` | Directive/test call | [s3306_b_10_A_neg.pl:29](../../human/sara/sara/cases/s3306_b_10_A_neg.pl#L29) |
| `s3306_b_10_B/3` | Directive/test call | [s3306_b_10_B_neg.pl:33](../../human/sara/sara/cases/s3306_b_10_B_neg.pl#L33) |
| `s3306_b_11/3` | Directive/test call | [s3306_b_11_neg.pl:23](../../human/sara/sara/cases/s3306_b_11_neg.pl#L23) |
| `s3306_b_15/5` | Directive/test call | [s3306_b_15_neg.pl:34](../../human/sara/sara/cases/s3306_b_15_neg.pl#L34) |
| `s3306_b_2_A/1` | Directive/test call | [s3306_b_2_A_neg.pl:47](../../human/sara/sara/cases/s3306_b_2_A_neg.pl#L47) |
| `s3306_b_2_C/1` | Directive/test call | [s3306_b_2_C_neg.pl:45](../../human/sara/sara/cases/s3306_b_2_C_neg.pl#L45) |
| `s3306_b_7/6` | Directive/test call | [s3306_b_7_neg.pl:37](../../human/sara/sara/cases/s3306_b_7_neg.pl#L37) |
| `s3306_c_1/2` | Directive/test call | [s3306_c_1_neg.pl:30](../../human/sara/sara/cases/s3306_c_1_neg.pl#L30) |
| `s3306_c_10_A/4` | Directive/test call | [s3306_c_10_A_i_pos.pl:37](../../human/sara/sara/cases/s3306_c_10_A_i_pos.pl#L37) |
| `s3306_c_10_A_i/3` | Directive/test call | [s3306_c_10_A_i_neg.pl:37](../../human/sara/sara/cases/s3306_c_10_A_i_neg.pl#L37) |
| `s3306_c_10_A_ii/3` | Directive/test call | [s3306_c_10_A_ii_neg.pl:40](../../human/sara/sara/cases/s3306_c_10_A_ii_neg.pl#L40) |
| `s3306_c_10_B/4` | Directive/test call | [s3306_c_10_B_neg.pl:32](../../human/sara/sara/cases/s3306_c_10_B_neg.pl#L32) |
| `s3306_c_11/2` | Directive/test call | [s3306_c_11_neg.pl:25](../../human/sara/sara/cases/s3306_c_11_neg.pl#L25) |
| `s3306_c_13/4` | Directive/test call | [s3306_c_13_neg.pl:37](../../human/sara/sara/cases/s3306_c_13_neg.pl#L37) |
| `s3306_c_16/2` | Directive/test call | [s3306_c_16_neg.pl:25](../../human/sara/sara/cases/s3306_c_16_neg.pl#L25) |
| `s3306_c_1_A_i/5` | Directive/test call | [s3306_c_1_A_i_neg.pl:31](../../human/sara/sara/cases/s3306_c_1_A_i_neg.pl#L31) |
| `s3306_c_1_B/2` | Directive/test call | [s3306_c_1_B_neg.pl:35](../../human/sara/sara/cases/s3306_c_1_B_neg.pl#L35) |
| `s3306_c_2/3` | Rule-body call | [s3306_c_2_neg.pl:29](../../human/sara/sara/cases/s3306_c_2_neg.pl#L29) |
| `s3306_c_21/4` | Directive/test call | [s3306_c_21_neg.pl:29](../../human/sara/sara/cases/s3306_c_21_neg.pl#L29) |
| `s3306_c_5/4` | Directive/test call | [s3306_c_5_neg.pl:28](../../human/sara/sara/cases/s3306_c_5_neg.pl#L28) |
| `s3306_c_6/1` | Directive/test call | [s3306_c_6_neg.pl:25](../../human/sara/sara/cases/s3306_c_6_neg.pl#L25) |
| `s3306_c_7/2` | Directive/test call | [s3306_c_7_neg.pl:25](../../human/sara/sara/cases/s3306_c_7_neg.pl#L25) |
| `s3306_c_A/3` | Directive/test call | [s3306_c_A_neg.pl:24](../../human/sara/sara/cases/s3306_c_A_neg.pl#L24) |
| `s3306_c_B/4` | Directive/test call | [s3306_c_B_neg.pl:30](../../human/sara/sara/cases/s3306_c_B_neg.pl#L30) |
| `s63_a/5` | Directive/test call | [s63_a_neg.pl:19](../../human/sara/sara/cases/s63_a_neg.pl#L19) |
| `s63_b/4` | Directive/test call | [s63_b_neg.pl:19](../../human/sara/sara/cases/s63_b_neg.pl#L19) |
| `s63_c_2_A_i/3` | Directive/test call | [s63_c_2_A_i_neg.pl:19](../../human/sara/sara/cases/s63_c_2_A_i_neg.pl#L19) |
| `s63_c_2_A_ii/2` | Directive/test call | [s63_c_2_A_ii_neg.pl:24](../../human/sara/sara/cases/s63_c_2_A_ii_neg.pl#L24) |
| `s63_c_2_B/3` | Directive/test call | [s63_c_2_B_neg.pl:24](../../human/sara/sara/cases/s63_c_2_B_neg.pl#L24) |
| `s63_c_2_C/2` | Directive/test call | [s63_c_2_C_neg.pl:24](../../human/sara/sara/cases/s63_c_2_C_neg.pl#L24) |
| `s63_c_5/5` | Directive/test call | [s63_c_5_neg.pl:23](../../human/sara/sara/cases/s63_c_5_neg.pl#L23) |
| `s63_c_6_A/4` | Directive/test call | [s63_c_6_A_neg.pl:24](../../human/sara/sara/cases/s63_c_6_A_neg.pl#L24) |
| `s63_c_6_B/2` | Directive/test call | [s63_c_6_B_neg.pl:23](../../human/sara/sara/cases/s63_c_6_B_neg.pl#L23) |
| `s63_c_6_D/2` | Directive/test call | [s63_c_6_D_neg.pl:15](../../human/sara/sara/cases/s63_c_6_D_neg.pl#L15) |
| `s63_c_7_i/2` | Directive/test call | [s63_c_7_i_neg.pl:17](../../human/sara/sara/cases/s63_c_7_i_neg.pl#L17) |
| `s63_c_7_ii/2` | Directive/test call | [s63_c_7_ii_neg.pl:19](../../human/sara/sara/cases/s63_c_7_ii_neg.pl#L19) |
| `s63_d_2/3` | Directive/test call | [s63_d_2_neg.pl:17](../../human/sara/sara/cases/s63_d_2_neg.pl#L17) |
| `s63_f_2_A/2` | Directive/test call | [s63_f_2_A_neg.pl:22](../../human/sara/sara/cases/s63_f_2_A_neg.pl#L22) |
| `s63_f_2_B/3` | Directive/test call | [s63_f_2_B_neg.pl:24](../../human/sara/sara/cases/s63_f_2_B_neg.pl#L24) |
| `s63_f_3/3` | Directive/test call | [s63_f_3_neg.pl:23](../../human/sara/sara/cases/s63_f_3_neg.pl#L23) |
| `s68_a_1/3` | Directive/test call | [s68_a_1_neg.pl:20](../../human/sara/sara/cases/s68_a_1_neg.pl#L20) |
| `s68_a_2/4` | Directive/test call | [s68_a_2_neg.pl:19](../../human/sara/sara/cases/s68_a_2_neg.pl#L19) |
| `s68_b_1_A/5` | Directive/test call | [s68_b_1_A_neg.pl:17](../../human/sara/sara/cases/s68_b_1_A_neg.pl#L17) |
| `s68_b_1_B/3` | Directive/test call | [s68_b_1_B_neg.pl:17](../../human/sara/sara/cases/s68_b_1_B_neg.pl#L17) |
| `s68_b_1_C/3` | Directive/test call | [s68_b_1_C_neg.pl:17](../../human/sara/sara/cases/s68_b_1_C_neg.pl#L17) |
| `s68_b_1_D/3` | Directive/test call | [s68_b_1_D_neg.pl:17](../../human/sara/sara/cases/s68_b_1_D_neg.pl#L17) |
| `s68_f/1` | Directive/test call | [s68_f_neg.pl:17](../../human/sara/sara/cases/s68_f_neg.pl#L17) |
| `s7703_a_1/5` | Directive/test call | [s7703_a_1_neg.pl:18](../../human/sara/sara/cases/s7703_a_1_neg.pl#L18) |
| `s7703_a_2/5` | Directive/test call | [s7703_a_2_neg.pl:19](../../human/sara/sara/cases/s7703_a_2_neg.pl#L19) |
| `s7703_b_1/4` | Directive/test call | [s7703_b_1_neg.pl:56](../../human/sara/sara/cases/s7703_b_1_neg.pl#L56) |
| `s7703_b_2/4` | Directive/test call | [s7703_b_2_neg.pl:49](../../human/sara/sara/cases/s7703_b_2_neg.pl#L49) |
| `s7703_b_3/4` | Directive/test call | [s7703_b_3_neg.pl:43](../../human/sara/sara/cases/s7703_b_3_neg.pl#L43) |
| `split_string/4` | Rule-body call | [tax_case_33.pl:15](../../human/sara/sara/cases/tax_case_33.pl#L15) |
| `tax/3` | Directive/test call | [tax_case_1.pl:33](../../human/sara/sara/cases/tax_case_1.pl#L33) |
| `var/1` | Directive/test call; Rule-body call | [s152_d_2_D_neg.pl:20](../../human/sara/sara/cases/s152_d_2_D_neg.pl#L20); [s3306_b_15_neg.pl:16](../../human/sara/sara/cases/s3306_b_15_neg.pl#L16) |

### Additional directive/control syntax

| Surface form | Syntactic arity / role | Source |
| --- | --- | --- |
| `discontiguous` | Prefix declaration `discontiguous/1`; its argument is a predicate indicator, not a fact | [s151_a_neg.pl:8](../../human/sara/sara/cases/s151_a_neg.pl#L8), [E1](../../human/sara/sara/statutes/prolog/events.pl#L1) |
| `halt` | `halt/0`; 376 directive occurrences | [s151_a_neg.pl:19](../../human/sara/sara/cases/s151_a_neg.pl#L19) |
| `:-` | Unary directive marker and binary clause separator | [s151_a_neg.pl:8](../../human/sara/sara/cases/s151_a_neg.pl#L8), [s2_a_1_B_neg.pl:26](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L26) |
| `\+` | Unary goal operator; interpretation deferred | [s151_a_neg.pl:18](../../human/sara/sara/cases/s151_a_neg.pl#L18) |
| `,` | Binary goal conjunction as well as argument/list punctuation | [s2_a_1_B_neg.pl:27](../../human/sara/sara/cases/s2_a_1_B_neg.pl#L27) |
| `;` | Binary goal operator | [s3306_a_2_B_neg.pl:28](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L28) |
| `==` | Binary goal operator | [s3306_a_2_B_neg.pl:26](../../human/sara/sara/cases/s3306_a_2_B_neg.pl#L26) |
| `->` and `=` | Binary goal operators | [s7703_b_1_neg.pl:30](../../human/sara/sara/cases/s7703_b_1_neg.pl#L30) |
| `[statutes/prolog/init]` | Load-directive notation; 378 occurrences; no call to an inferred `consult` predicate was inventoried | [s151_a_neg.pl:9](../../human/sara/sara/cases/s151_a_neg.pl#L9) |
| `/`, lists and parentheses | Binary `/` occurs in predicate indicators and unquoted load paths; list and grouping syntax are not additional household predicates | [s151_a_neg.pl:8](../../human/sara/sara/cases/s151_a_neg.pl#L8), [s151_a_neg.pl:9](../../human/sara/sara/cases/s151_a_neg.pl#L9), [s63_d_2_pos.pl:14](../../human/sara/sara/cases/s63_d_2_pos.pl#L14) |

## Difference from the eventual approved interface

The intended eventual interface uses **Int cents** for money and **day counts**
for dates. This draft instead stores unsigned decimal and double-quoted source
lexemes without decoding or conversion. A source numeral's position does not
automatically make it money; a date-shaped quoted token is not yet a day count.
There is no epoch, rounding rule, currency scaling, interval convention, date
validity, default, arithmetic or tax interpretation in the Lean file.

`HouseholdDraft.Household` is a temporary syntax container. Publishing the
approved `Household` and `Year` types, choosing their fields, and mapping
each source argument into those types are still pending. `Year` is deliberately
not declared here; the year-looking numerals in clauses remain source lexemes.
No adapter from this draft to a semantic interface is implemented.

The accepted invariant declaration form remains
`def invariant (impl : Household → Year → Int) : Prop`, with the signed
proposition supplied by its owner and a proof of an instantiation in a separate
module. The draft neither implements a signed statement nor invents a
`Valid` premise, theorem body, invariant or proof.

The invariant's `Int` result does not establish a universal case-result type.
For example, the source contains a list argument in the test at
[s63_d_2_neg.pl:17](../../human/sara/sara/cases/s63_d_2_neg.pl#L17), a compound
test at [s152_d_2_D_neg.pl:19](../../human/sara/sara/cases/s152_d_2_D_neg.pl#L19),
and `tax/3` calls such as
[tax_case_100.pl:28](../../human/sara/sara/cases/tax_case_100.pl#L28).
No input/output argument modes, scalar projection, answer multiplicity, or
per-section payload/result semantics are inferred from these syntactic forms.
Those mappings remain pending the owner's decisions; a generic parity envelope
does not settle them.

## Unresolved owner decisions

1. Approve the shared semantic field list and the role of case-local statutory
   assumptions, relations, event identifiers, names and multiple predicate arities.
   Decide how the draft maps to the approved `Household` and `Year`.
2. Specify source-money units, exact conversion to Int cents, rounding and
   worked examples. Numeral storage here does not settle any of these.
3. Specify the day-count representation, epoch, date interpretation and
   predicate-specific interval semantics. Determine which quoted positions
   denote dates and how other quoted values behave.
4. Specify variable scope, anonymous-variable handling, unification and the
   treatment of the 108 non-ground bodyless clauses and all 434 local rules.
   Resolve their relation to the oracle and to case-supplied statutory predicates.
   Decide the instantiation-sensitive and control behavior through DECISIONS.
5. Resolve the two cross-`% Test` terms without silent source repairs, and
   define what counts as a test directive and as a successful case.
6. Define round-trip identity: bytes, source syntax or some explicitly approved
   semantic equivalence. Decide how full case files, directives and unsupported
   forms enter that contract. No facts-only subset may silently replace the
   designated 376 cases.
7. State any semantic absence, duplicate, ordering and aggregation policies.
   The syntax container preserves these distinctions until such decisions exist.
   Do not infer closed-world defaults from an empty list.
8. Approve lexical/domain validation and the handling of future predicates or
   syntax changes; raw constructors and an arity index are not a validity check.
   Select the permanent Lean toolchain through the owning contract.
9. Approve each section's payload and result semantics, including how its case
   queries relate to the shared input and approved implementation signatures.
   Do not assume that every case query has one scalar section result.

## Local validation and limits

The draft type-checks with the already installed **Lean 4.33.1**
(`arm64-apple-darwin24.6.0`, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`). The installed binary was invoked
directly on `Interface/Household.lean`; no `lean-toolchain` was created,
no default/override was changed, and no tool was installed or downloaded.
One reserved binder name was corrected after the first compiler check; the
following check passed. The three-failed-edit-cycle circuit breaker was not
reached.

No Prolog execution, semantic parity, source round-trip, normalized input
validity, theorem proof or phase-gate pass is claimed. Only the household draft
and this contract were written in this work lane. The protected input tree was
read-only throughout; prohibited independent artifacts were not read.
The clause-boundary and full-case ingestion findings are handed to the main
lane for `STATE.md` → `Blockers` under the protocol's stop-and-report rule;
`STATE.md` is outside this lane's exclusive write scope. The affected semantic
interpretation and ingestion work remains stopped, without a workaround.

## Self-review: assumptions about Prolog semantics

- Predicate identity is inventoried by literal name plus arity. Spelling
  differences and arity variants are preserved without claiming equivalence,
  typographical error or statute meaning.
- The lexical audit treats `%` text as comments and a terminating full stop
  outside quotes as a term boundary. It does not treat `% Facts` or `% Test`
  as executable separators. Its interpretation of the two cross-comment terms
  assumes ordinary clause syntax and is not a runtime Prolog validation.
- `_` is retained per source occurrence, with no shared identity or default.
  No named-variable binding, unification, substitution or quantified Lean
  proposition is implemented. All execution behavior remains undecided here.
- Double-quoted lexemes are not assumed to be strings, atoms, character lists or
  code lists at runtime. Quoted date-like lexemes are not parsed; unquoted and
  quoted source forms are not conflated.
- Numeric lexemes carry no assumption about money units, year domains, signs
  permitted by an eventual domain, overflow, arithmetic or rounding. Identifier
  names carry no inferred person/event/domain validity.
- Rule bodies, declaration effects, module loading, negation, instantiation
  tests, control order, date helpers and arithmetic/conversion helpers are not
  evaluated. No finite grounding or missing-fact default is assumed.
- List order and duplicate occurrences are preserved as syntax. This makes no
  claim that all consumers are order-insensitive, set-based, duplicate-free or
  closed-world.
- The invariant implementation signature does not determine all case-query
  result types. No argument modes, scalar answer projection or per-section
  output semantics are assumed.
