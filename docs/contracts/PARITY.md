# Independent parity meter contract

Owner implementation target: `human/parity/check.py`. The staged `parity/check.py`
contains no comparison logic; it always prints `unimplemented` and exits 2.
The assistant may invoke the owner's implementation but must never inspect its
source or replace it with an assistant-authored comparator.

## Invocation and results

```text
python human/parity/check.py --section N --inputs DIR --prolog-out DIR --lean-out DIR
```

- Exit 0: every requested input has both outputs and every output agrees.
- Exit 1: mismatches; write `mismatches.jsonl` in the invocation's working
  directory. Each line has `input_id`, `prolog`, and `lean`.
- Exit 2: unimplemented or unable to perform a valid comparison (for example,
  malformed JSON, invalid schema, or ambiguous IDs). Print the reason to stderr.
  This is an infrastructure failure, never zero mismatches.

This elaborates the plan's 0/1 contract without relaxing its success condition.
The harness invokes the meter in a dedicated run directory and retains its
exit status, diagnostics, input identity, and mismatch artifact.

## File envelopes

Use UTF-8 JSON, one object per `<input_id>.json`. IDs match
`[A-Za-z0-9][A-Za-z0-9_-]*`, and the filename stem and object ID must agree.
Every input record contains:

```json
{
  "schema_version": 1,
  "input_id": "s151_b_pos",
  "section": 151,
  "payload": {}
}
```

The empty payload above is illustrative, not a valid household. The approved
`Interface/` and `DECISIONS.md` will define section payloads and query encodings.
That definition remains pending; the independent meter only needs the input
identity and section to determine the expected output population.

Each engine output contains exactly the following fields:

```json
{
  "schema_version": 1,
  "input_id": "s151_b_pos",
  "section": 151,
  "result": null
}
```

The example `null` is an illustrative JSON value, not an assumed statute answer.
`result` is the canonical observation specified by the approved section
interface. Its wire values may be null, booleans, strings, integers, arrays, and
objects with string keys. Floating-point observations must use the tagged/string
representation approved in `DECISIONS.md`, not an implicitly rounded JSON float.
No epoch, rounding, answer projection, result ordering, or missing-fact behavior
is selected by this contract.

## Comparison requirements

- Use `--inputs` as the authority for all input IDs in the requested section.
  Do not compare only the intersection of engine outputs. Empty selected input
  populations fail with exit 2; they do not validate a section.
- Require exactly one output from each engine per selected ID. Missing outputs
  are mismatches: the missing side is `null` in the mismatch record, and an
  existing side contains its full output object. Unexpected output IDs, wrong
  sections, duplicate IDs/keys, or malformed records fail with exit 2.
- Compare parsed JSON structurally with strict types: booleans are not integers,
  absent keys are not null values, and arrays retain order and multiplicity.
  Ignore only object-key order and JSON formatting. Do not coerce numbers,
  deduplicate answers, introduce tolerances, or interpret Prolog semantics.
- Both engines must implement only approved canonicalization before emitting
  outputs. Until the payload and result specifications are approved, producers
  are blocked rather than guessing representations.
- A compile error, interpreter failure, timeout, or serialization failure must
  not be serialized as an ordinary answer or silently removed from the input
  population. The harness reports it as an infrastructure failure; parity has
  not passed.
- Write mismatch records in input-ID order. On successful comparison, write an
  empty `mismatches.jsonl` so an old report cannot be mistaken for the new run.
  On invalid data, report the error without claiming that comparisons completed.

The human can implement this envelope comparison independently while the
section-specific payloads are being reviewed. No real comparison implementation
or result canonicalizer is provided here.
