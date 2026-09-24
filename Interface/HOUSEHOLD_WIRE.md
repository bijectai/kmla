# Household JSON spelling

This declaration fixes the lossless transport spelling of the approved
`Household` data under [WIRE.md](WIRE.md). It is shared specification, with no
serializer, decoder, grounding implementation or shared encoder. Each isolated
lane implements against this declaration independently.

This is only the Household component. The containing `payload`, target/mode,
bound-argument tuple, year, output positions, observations and original-case
mapping are outside this declaration. It does not complete or release the
end-to-end input codec, resume either implementation lane, certify the main
task's preflight, or claim round trips, parity, termination or a checkpoint pass.

## Authority

Line references identify the declarations inspected for this spelling; the
named declarations and owner decision sections remain authoritative. If they
disagree, `human/DECISIONS.md` governs and the affected work stops for a reported
decision. Fixtures cannot supply missing semantics.

| Transport content | Owner authority in `human/DECISIONS.md` | Shared type authority in `Interface/Household.lean` |
| --- | --- | --- |
| `facts`, `stipulations`, list order and multiplicity | H1, lines 598–609; H4.2–H4.3, lines 740–757; G1, lines 23–31 | `Household` |
| Fact constructor and positional arguments | H2–H3, lines 611–691 | `Fact` |
| Atom/string tags and integer values | G4, lines 48–56; H2; M1, lines 90–99 | `Term`; typed Fact arguments |
| Whole-dollar `amount_` argument | M1; H2 | `Fact.amount_` |
| Typed Day values and ISO spelling | D1, lines 309–316; V9, lines 806–807 | `Day`; `Fact.start_`/`Fact.end_`; `Day.toISO` |
| Stipulation signature, arity and positional argument list | H4.1, lines 696–738 | `StipPred`; `StipPred.arity`; `Stip.args : List StipArg` |
| Explicit value/wildcard distinction and identity | H2; H4.1; A3, lines 1291–1295 | Event `Pat`; stipulation `StipArg` |
| Proper lists inside supplied stipulation arguments | H4.1–H4.3; A1/A3; representation-gap classification in `docs/consult/A-022.md` | `StipArg.list : List StipArg → StipArg` |
| Preservation of opaque extra stipulated arities | H4.1 (`s151_d/4`, `s2_a/5`, `s63_c_3/4`) | `StipPred.timeRoles` and its following scope comment; `Interface/TIME_SCHEMA.json`, last three signature entries |
| Exact emitted bytes | Accepted P-WIRE | `Interface/WIRE.md`, Bytes, lines 8–33 |

The field names and wrappers below are builder-owned spelling of these data,
as authorized by WIRE. They add no modes, defaults, projections, normalization
or domain restrictions. Transport preservation is separate from H5 admission:
an encodable value or well-shaped fixture need not satisfy `Valid` or
`ValidStip`. Existing admission checks must neither be inferred from examples
nor used to silently delete or repair transported data.

The 2026-09-23 correction supplies the proper-list container required by signed
H4, as classified in A-022. G4 scalar `Term` and event `Pat` are unchanged.
The new distinct `StipArg` retains the old scalar/wildcard wire bytes and adds
one recursive container. This is not an owner amendment or a full query codec.

## JSON shapes and emission order

Objects have exactly the fields shown, emitted in the listed order. Array
positions are significant. The tables describe the emitted form and its
inverse; they do not change the meter's object-key-order comparison policy.
There is no implicit field, alternate null form or default for an omitted
field. Empty outer `facts`, `stipulations` or `args` arrays are `[]`; an empty
list-valued stipulation argument is `{"list":[]}`, never a bare array.

| Value | JSON shape | Object key order / array order |
| --- | --- | --- |
| `Household` | `{"facts":[Fact,...],"stipulations":[Stip,...]}` | `facts`, `stipulations`; each list in its supplied order |
| `Fact` | `{"ctor":"constructor_name","args":[arg1,...]}` | `ctor`, `args`; arguments in the constructor's declaration order |
| `Stip` | `{"pred":"StipPred_constructor","args":[StipArg,...]}` | `pred`, `args`; arguments in source position order |
| `Term.atom s` | `{"a":s}` | single key `a`; `s` is a JSON string |
| `Term.str s` | `{"s":s}` | single key `s`; `s` is a JSON string |
| `Term.int n` | `n` | exact JSON integer number |
| `Pat.val t` | `{"val":Term}` | single key `val`; the nested Term retains its tag |
| `Pat.wild id` | `{"wild":id}` | single key `wild`; exact JSON nonnegative integer (`Nat`) |
| `StipArg.val t` | `{"val":Term}` | byte-identical to the old scalar stipulation spelling |
| `StipArg.wild id` | `{"wild":id}` | byte-identical to the old wildcard stipulation spelling |
| `StipArg.list items` | `{"list":[StipArg,...]}` | single key `list`; recursive elements in supplied order |
| `Int` in an `Int`-typed argument | `n` | exact JSON integer number |
| `Day` in a `Day`-typed argument | `"YYYY-MM-DD"` | D1 civil date, zero-padded ISO spelling |

`Fact`, `Stip`, `Pat`, `StipArg`, `Term`, `arg1`, `s`, `n` and `id` in the shape table
are metavariables, not literal JSON. Constructor and key strings are literal,
case-sensitive spellings. `ctor` is the exact `Fact` constructor name without
a namespace. `pred` is the exact `StipPred` constructor name without a
namespace, including its arity suffix. The predicate/arity columns below are
the mapping to source signatures; they are not additional JSON fields.

Keep each list as supplied, including repeated entries, interleaved predicate
names and inert facts. Do not group facts by event or predicate, sort either
list, deduplicate, or add missing facts. H4 grounding has already occurred
before a grounded Household reaches this boundary; no Prolog rule text is a
Household field. This spelling also preserves the declared helper constructors
when supplied, even though H4.2 does not emit them and V1 rejects them for
generated inputs (the `Fact` declaration's documentation).

### Primitive values and patterns

Apply all WIRE byte rules: UTF-8 without BOM; compact JSON without optional
whitespace or a trailing newline; exact decimal integers; prescribed control
escapes; raw other Unicode and `/`; no Unicode normalization. Neither string
tags nor text are inferred from the contents. `{"a":"42"}`, `{"s":"42"}`
and `42` encode three different Terms. Empty strings are representable data;
V1's nonempty-string condition remains an admission condition.

Integers and wildcard IDs have the precision of `Int` and `Nat`, not a host
machine integer or IEEE-754 number. Encode and decode them without any float
conversion. Use `0` for zero and no redundant sign, zeros, decimal point or
exponent. Do not quote a large integer to work around a parser's precision
limit. `amount_` is an `Int` in whole dollars; no scaling, rounding, clipping
or V2 filtering occurs during transport. A negative or large amount can be
preserved without asserting that it is admitted.

A typed Day is D1's proleptic-Gregorian day count represented by its civil
date, not a timestamp: `-1` corresponds to `"1969-12-31"`, `0` to
`"1970-01-01"`, and `11016` to `"2000-02-29"`. Approved dates use four-digit
zero-padded years. D1/V9 and the existing V3 domain govern dates; this document
adds no out-of-domain date convention or new range condition. Do not apply
the interpreter's timestamp shift, a time zone, a default date or overflow
normalization to this spelling.

Only `Fact.start_` and `Fact.end_` have a `Day`-typed argument. All `Stip.args`
entries are `StipArg`, including those with a declared time role. For example,
`{"val":{"s":"2015-01-01"}}` and `{"val":{"a":"2015-01-01"}}` retain
different tags, and `{"val":2015}` retains an integer. A time-role check does
not erase a tag or convert a date-looking Term to the bare Day spelling.
Preserve every literal in place, including inert out-of-range year literals.
Operational time admission remains the shared query boundary's responsibility;
this declaration supplies no query mode or operational year.

`Pat.val` is explicit in `purpose_` position 1; `StipArg.val` is explicit in
stipulations. `{"val":{"a":"_"}}` is an atom-valued pattern, not a wildcard.
`{"wild":17}` transports exactly the corresponding `Pat.wild 17` or
`StipArg.wild 17` selected by its enclosing type. Another occurrence of that
stored value retains 17, while id 18 remains distinct. Do not replace IDs with `null`, drop them,
renumber them by position, deduplicate them or allocate fresh IDs during this
transport. This preserves the stored wildcard identity under A3; it does not
specify Prolog variable allocation, clause invocation or solution-copy
freshening. H6.2's observed-unbound `null` is outside this Household format.

### Proper-list stipulation arguments

The outer `Stip.args` array enumerates argument positions. A proper list
*within* one argument uses the disjoint tag `{"list":[...]}`, recursively:
`{"list":[]}` is an empty list, and
`{"list":[{"val":{"a":"charlie"}}]}` is the singleton list `[charlie]`.
An inner list is never a bare array, a `val` containing an array, an atom/string
spelling of Prolog syntax, a wildcard or `null`. `{"val":{"a":"[]"}}` remains
a scalar atom; it is not the empty-list container.

Keep all nesting, tags, exact integers, order and duplicates. A wildcard id
inside a list is the same stored id wherever it reappears elsewhere in that
stipulated head, including other argument positions and deeper lists. Do not
renumber each occurrence or erase it during transport.
Transport performs no unification or execution-time freshening.

This type contains finite proper lists only. Improper/open-tail lists and
non-list compounds have no spelling here; encountering one remains a reported
unsupported-value finding. Do not flatten, stringify, truncate, coerce, exclude
the original or invent another tag to continue.

Event `Pat` still has only `val` and `wild`; neither `Term` nor `Fact.purpose_`
gains a list value. Lean's `StipArg.ofPat` (also the one-way coercion) preserves
the old scalar/id exactly, with no reverse coercion into event positions.
`Stip.wellFormed` still checks only the number of outer argument positions.
Existing stipulated Day slots still require a scalar date or wildcard; a list
in such a slot is not a scalar Day. Other slots are not recursively scanned
for dates, numeric ranges or inferred roles. V1 still requires no stipulations
for generated inputs; the V2–V10 requirements and actual query-time boundary
remain in force. This declaration changes no query representation or mode.

## Fact registry: 57 constructors

Each row gives the exact `ctor`, source signature and ordered `args` types.
Argument labels reproduce the Lean binders and are not JSON object keys.
The registry's declaration order does not prescribe the order of a Household's
facts. No argument is omitted even when the constructor is inert.

| `ctor` | Source signature | Ordered `args` |
| --- | --- | --- |
| `agent_` | `agent_/2` | `event: Term, value: Term` |
| `agricultural_service` | `agricultural_service/3` | `a1: Term, a2: Term, a3: Term` |
| `alice_employer` | `alice_employer/3` | `a1: Term, a2: Term, a3: Term` |
| `alice_household_maintenance` | `alice_household_maintenance/4` | `a1: Term, a2: Term, a3: Term, a4: Term` |
| `american_employer_` | `american_employer_/1` | `event: Term` |
| `amount_` | `amount_/2` | `event: Term, dollars: Int` |
| `attending_classes_` | `attending_classes_/1` | `event: Term` |
| `beneficiary_` | `beneficiary_/2` | `event: Term, value: Term` |
| `birth_` | `birth_/1` | `event: Term` |
| `blindness_` | `blindness_/1` | `event: Term` |
| `brother_` | `brother_/1` | `event: Term` |
| `business_` | `business_/1` | `event: Term` |
| `business_trust_` | `business_trust_/1` | `event: Term` |
| `citizenship_` | `citizenship_/1` | `event: Term` |
| `country_` | `country_/2` | `event: Term, value: Term` |
| `daughter_` | `daughter_/1` | `event: Term` |
| `death_` | `death_/1` | `event: Term` |
| `deduction_` | `deduction_/1` | `event: Term` |
| `destination_` | `destination_/2` | `event: Term, value: Term` |
| `disability_` | `disability_/1` | `event: Term` |
| `educational_institution_` | `educational_institution_/1` | `event: Term` |
| `end_` | `end_/2` | `event: Term, day: Day` |
| `enrollment_` | `enrollment_/1` | `event: Term` |
| `father_` | `father_/1` | `event: Term` |
| `hospital_` | `hospital_/1` | `event: Term` |
| `incarceration_` | `incarceration_/1` | `event: Term` |
| `income_` | `income_/1` | `event: Term` |
| `international_organization_` | `international_organization_/1` | `event: Term` |
| `itemize_deductions_` | `itemize_deductions_/1` | `event: Term` |
| `joint_return_` | `joint_return_/1` | `event: Term` |
| `legal_separation_` | `legal_separation_/1` | `event: Term` |
| `location_` | `location_/2` | `event: Term, value: Term` |
| `marriage_` | `marriage_/1` | `event: Term` |
| `means_` | `means_/2` | `event: Term, value: Term` |
| `medical_institution_` | `medical_institution_/1` | `event: Term` |
| `medical_patient_` | `medical_patient_/1` | `event: Term` |
| `migration_` | `migration_/1` | `event: Term` |
| `mother_` | `mother_/1` | `event: Term` |
| `nonresident_alien_` | `nonresident_alien_/1` | `event: Term` |
| `nurses_training_school_` | `nurses_training_school_/1` | `event: Term` |
| `patient` | `patient/2` | `event: Term, value: Term` |
| `patient_` | `patient_/2` | `event: Term, value: Term` |
| `payment_` | `payment_/1` | `event: Term` |
| `penal_institution_` | `penal_institution_/1` | `event: Term` |
| `plan_` | `plan_/1` | `event: Term` |
| `purpose_` | `purpose_/2` | `event: Pat, purpose: Term` |
| `reason_` | `reason_/2` | `event: Term, value: Term` |
| `residence_` | `residence_/1` | `event: Term` |
| `retirement_` | `retirement_/1` | `event: Term` |
| `service_` | `service_/1` | `event: Term` |
| `sibling_` | `sibling_/1` | `event: Term` |
| `sister_` | `sister_/1` | `event: Term` |
| `son_` | `son_/1` | `event: Term` |
| `start_` | `start_/2` | `event: Term, day: Day` |
| `termination_` | `termination_/1` | `event: Term` |
| `type_` | `type_/2` | `event: Term, value: Term` |
| `unemployment_compensation_agreement_` | `unemployment_compensation_agreement_/1` | `event: Term` |

`patient` and `patient_` remain different constructors. The three helper
constructors with three/four arguments retain all their `Term` arguments.
`first_day_year/2`, `gross_income/3`, `is_before/2` and `last_day_year/2`
are not Fact constructors (the `Fact` declaration's documentation).

## Stipulation registry: 31 signatures

For a well-shaped stipulation, `args` contains exactly the listed number of
`StipArg` values, in positions 1 through arity. Each position uses the same recursive
spelling; the table makes no assertion about a query mode, input/output
projection, argument role or successful evaluation. The extra signatures stay
distinct from any shorter signature with the same source predicate name.

| `pred` | Source signature | Arity (`StipArg` positions 1…arity) |
| --- | --- | --- |
| `s63_3` | `s63/3` | 3 |
| `s7703_4` | `s7703/4` | 4 |
| `s3306_b_8` | `s3306_b/8` | 8 |
| `s2_b_3` | `s2_b/3` | 3 |
| `s2_a_3` | `s2_a/3` | 3 |
| `s151_c_applies_3` | `s151_c_applies/3` | 3 |
| `s152_c_1_3` | `s152_c_1/3` | 3 |
| `s3306_c_5` | `s3306_c/5` | 5 |
| `s151_5` | `s151/5` | 5 |
| `s151_d_4` | `s151_d/4` | 4 |
| `s151_b_applies_3` | `s151_b_applies/3` | 3 |
| `s151_c_4` | `s151_c/4` | 4 |
| `s151_b_applies_2` | `s151_b_applies/2` | 2 |
| `total_wages_employer_6` | `total_wages_employer/6` | 6 |
| `s68_b_3` | `s68_b/3` | 3 |
| `s152_c_2_4` | `s152_c_2/4` | 4 |
| `s152_c_3` | `s152_c/3` | 3 |
| `s152_b_2_4` | `s152_b_2/4` | 4 |
| `s3306_a_2` | `s3306_a/2` | 2 |
| `s63_c_1_3` | `s63_c_1/3` | 3 |
| `s63_c_2_3` | `s63_c_2/3` | 3 |
| `s63_c_3_3` | `s63_c_3/3` | 3 |
| `s63_f_1_A_2` | `s63_f_1_A/2` | 2 |
| `s63_f_1_B_3` | `s63_f_1_B/3` | 3 |
| `s63_d_4` | `s63_d/4` | 4 |
| `s152_c_3_3` | `s152_c_3/3` | 3 |
| `s2_a_5` | `s2_a/5` | 5 |
| `s152_d_2_H_6` | `s152_d_2_H/6` | 6 |
| `s63_c_3` | `s63_c/3` | 3 |
| `s63_c_3_4` | `s63_c_3/4` | 4 |
| `s151_b_3` | `s151_b/3` | 3 |

In particular, `s151_d_4`, `s2_a_5` and `s63_c_3_4` have opaque pattern
arguments under the shared time schema. Do not infer time roles from their
values, reinterpret their arities, swap their positions, or discard them.
The `Stip` type stores `List StipArg`; arity well-formedness is the separate
`Stip.wellFormed` check. Transport copies that list exactly and does not
truncate or pad a malformed list to make the check pass.

## Declarative fixtures and checks

[fixtures/household_wire.json](fixtures/household_wire.json) contains a fixture
container with `scope`, `validity_claim` and `cases`. Each case has `name`,
`household` and `wire`. These container keys are test metadata, not Household
fields, payload fields or a new schema version. `household` is the readable
JSON value of the declaration above. After parsing the fixture container once,
`wire` is the exact expected UTF-8 text for that value, without BOM or trailing
newline. Thus the escapes inside the enclosing JSON string have one extra
escaping layer. The fixture file itself is formatted and ends with LF; that
LF is not part of any `wire` value.

| Case | Preservation covered | Admission qualification |
| --- | --- | --- |
| `empty` | Both explicitly empty lists | No validity claim |
| `tags_order_integers` | `atom`/`str` distinction, repeated ordered facts, `Int` zero and positive/negative values beyond 2^53 | Large/negative amounts fail V2 |
| `controls_unicode` | Every U+0000–U+001F control, quote, backslash, raw slash, raw BMP/astral text, distinct composed/decomposed text, empty strings | Empty Term strings fail V1 |
| `dates_and_tagged_patterns` | Pre-epoch/epoch/leap/boundary Day spelling and preserved date-like atom/string patterns | Stipulations prevent generated-input V1; no `ValidStip` claim |
| `wildcard_identity` | `val` versus `wild`, large Nat ID, distinct stored IDs, repeated ordered stipulations | Wildcards/stipulations prevent generated-input V1; no execution-freshness claim |
| `opaque_helpers_extra_arities` | All three helper constructors, `patient` versus `patient_`, inert marker, all three extra stipulated arities, inert year literal in its supplied position | Helpers/stipulations prevent generated-input V1; no `ValidStip` claim |
| `supplied_s151_lists` | The four `[charlie]`/`[0]` heads for 2014–2017 and the `[alice]` head recorded in Q-022 | Supplied shapes only; no H4.3 or `ValidStip` claim |
| `recursive_lists_shared_ids` | Empty/nonempty/nested proper lists, empty list versus scalar atom/string `"[]"`, scalar tags, signed integers beyond 64 bits, ordered duplicate elements, ids shared inside/outside nested lists | Transport example; no validity or domain claim |

The six pre-list fixtures and all their scalar/wildcard `wire` values remain
byte-identical. The two appended fixtures specify the new container only.

All numbers in the fixture container also require exact integer parsing.
Checks for implementers are preservation of the declared value, exact `wire`
bytes and registry/arity agreement with Interface. A successful JSON parse or
fixture comparison is not an H4 semantic round trip, query-admission proof,
production `Valid`/`ValidStip` check or parity result. No fixture is evidence
for a missing Prolog semantic decision. A missing choice stops the affected
scope and is reported to the coordinating task; no fallback spelling with
new semantics is authorized here.
