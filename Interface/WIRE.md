# Shared wire contract — P-WIRE accepted 2026-09-22

This is a shared byte/packaging specification, not either lane's implementation.
The semantic authority remains `human/DECISIONS.md` H1–H4, G4, D1/V9, M1,
H6.1/H6.2/H6.5, G1 and A3, plus Dev's recorded amendments. No new mode,
projection, canonicalization, missing-value convention or coercion is selected.

## Bytes

- UTF-8, no BOM, no Unicode normalization, compact JSON without optional
  whitespace. Emit no trailing newline in encoded record/observation values.
  The independent meter's JSONL report has its separate approved LF contract.
- Strings escape quotation mark as `\"`, backslash as `\\`, and backspace,
  form feed, LF, CR and tab as `\b`, `\f`, `\n`, `\r`, `\t` respectively.
  Other U+0000–U+001F controls use lowercase `\u00xx`. Other Unicode stays
  raw, including astral code points, never surrogate-pair escapes. `/` stays raw.
- Integers use exact decimal notation (zero `0`, no leading `+` or redundant
  zeros, no fractional or exponent notation). Never convert through a float.
- H6.2 observations use the existing `Obs`/`Solution`/`observe` contract in
  `Household.lean`: tagged atoms/strings, ISO days, positional solution tuples,
  sorted/deduplicated encoded tuples at the observation boundary only. Scalar
  entry points retain H6.1 first-solution behavior. Do not sort or deduplicate
  the input lists or internal oracle lists.
- The envelopes are exactly those in `docs/contracts/PARITY.md`. When emitting
  them use key order `schema_version,input_id,section,payload` for inputs and
  `schema_version,input_id,section,result` for outputs. Meter comparison still
  ignores object-key order and JSON formatting; it does not choose semantics.

These are lossless spelling choices under the owner-approved byte proposal.
The observation encoder already exists. [HOUSEHOLD_WIRE.md](HOUSEHOLD_WIRE.md)
fixes the Household component, with declarative cross-language fixtures under
`fixtures/household_wire.json`. Its distinct recursive `StipArg` uses the
disjoint `{"list":[...]}` tag for proper-list stipulation arguments, retaining
the existing scalar/wildcard bytes; event `Pat` and `Term` remain scalar.
The full input codec does **not** yet exist:
before emitting full records, fix the remaining payload/query packaging and
fixtures here (or in a referenced Interface specification).
Do not let either lane independently invent the payload wire shape.

## Field authority and record identity

| Content | Governing authority |
| --- | --- |
| Household fact/stipulation lists and their order/multiplicity | H1–H4 and G1 |
| Term tags, equality and integer values | G4, H2 and M1 |
| Days and their ISO representation | D1/V9 |
| Stipulation argument/wildcard identity | H4, A3 |
| Target, mode, bound arguments and output positions | H6.1 and H6.5 |
| Observation and scalar entry behavior | H6.1/H6.2 |
| Envelope IDs, section and schema version | PARITY.md |
| One record per household/target/bound tuple | P-WIRE owner approval |

A future field without an authority stays blocked pending an owner decision.
There is no permission to supply a semantic default merely to finish the codec.

One logical record is `(Household, target, bound-argument tuple)` with the
approved mode and applicable year retained. IDs follow PARITY's grammar and
section-local ASCII-case-fold uniqueness; generated stems are lowercase.
Retain record-to-target/mode/arguments and original-case-to-record(s) mappings.
Originals may share records or use more than one. This never redefines H6.3
case success, the 376-original population or the two extra-conjunct cases.

## Counts required in summaries, manifests and coverage reports

- `record_count`: number of records. The generated ≥10k threshold uses this unit.
- `distinct_household_count`: distinct complete H1 values among those records,
  with exact tag-sensitive terms and ordered, multiplicity-preserving facts and
  stipulations. Changing only target, mode or bound arguments is not a new
  household. No semantic household equivalence or fact normalization is used.
- `original_case_count`: originals accounted for by the case mapping, separately
  from either count above; report absent originals as failures, not exclusions.

Records and households must never be presented interchangeably. No new ≥10k
distinct-household requirement is implied. Kill rate still divides killed
admitted whole-section mutants by admitted whole-section mutants, not records.
The independent ≥20-hits-per-arm requirement and B003 corpus separation remain.
