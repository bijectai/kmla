# Independent parity meter contract

Owner implementation target: `human/parity/check.py`. The staged `parity/check.py`
contains no comparison logic; it always prints `unimplemented` and exits 2.
The builder may invoke the owner's implementation but must never inspect its
source or replace it with a different comparator.

The five policies below were accepted by Dev on 2026-09-21; the supplied
decision text is preserved in `OWNER_DECISIONS_2026-09-21.txt`. Existing
requirements are identified as restatements, not silently reclassified as new
policy. Neither these policies nor the fixture suite supplies a meter.

## Invocation and results

```text
python human/parity/check.py --section N --inputs DIR --prolog-out DIR --lean-out DIR
```

- Exit 0: every requested input has both outputs and every output agrees;
  write a zero-byte `mismatches.jsonl` only after comparison completes.
- Exit 1: mismatches; write `mismatches.jsonl` in the invocation's working
  directory. Each line has `input_id`, `prolog`, and `lean`.
- Exit 2: unimplemented or unable to perform a valid comparison (for example,
  malformed JSON, invalid schema, or ambiguous IDs). Print the reason to stderr.
  Create and modify nothing. This is an infrastructure failure, never zero
  mismatches. An unexpected exception must also exit 2, not Python's uncaught
  exception exit 1, which is reserved for completed mismatch comparisons.

This elaborates the plan's 0/1 contract without relaxing its success condition.
The harness invokes the meter in a fresh, dedicated run directory and retains its
exit status, diagnostics, input identity, and mismatch artifact.
An absent report there means infrastructure failure; present-and-empty means
success; present-and-non-empty means mismatches. Never truncate a report before
doing the comparison: that would manufacture a success artifact on failure.
If invoked with an existing report, exit 2 leaves it untouched; the report alone
cannot establish the new run's outcome. The harness must use a fresh directory
and retain the exit status, rather than reuse a stale report as evidence.

## File envelopes

Use UTF-8 JSON, one object per `<input_id>.json`. IDs match
`[A-Za-z0-9][A-Za-z0-9_-]*`, and the filename stem and object ID must agree
byte-for-byte in **every record in all three directories** (otherwise exit 2).
ID comparison is case-sensitive. As an additional population constraint, IDs
within a section must be unique under ASCII case folding. Producers must
prevent collisions before writing; `gen/` must mint lowercase-only stems.
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
- Write mismatch records in input-ID order, only after comparison completes.
  On successful comparison, write an empty `mismatches.jsonl` so an old report
  cannot be mistaken for the new run. On invalid data, leave any report untouched
  and report the error without claiming that comparisons completed.

## Accepted directory and identity policies

1. **Directory contents.** Apply this complete decision procedure, in order,
   to every entry in each of the three argument directories:

   - An entry whose name ends in `.json`, dotted or not, joins the population
     and is judged by the ID grammar. Thus `.s151_a.json` is exit 2, not ignored.
     Such entries must also satisfy rule 2's regular-file requirement.
   - A dot-prefixed entry whose name does not end in `.json` is ignored.
     Dot-prefixed directories are covered here, before rule 2.
   - **Any other entry is exit 2**, including a regular file such as `notes.txt`
     or `README`. There is no third, unspecified category.

   Dev's clarification preserves the original rejection of other non-JSON
   files; narrowing the dotfile exemption does not loosen that rule. Stray
   files may indicate interrupted runs. Producers keep engine logs and sidecars
   outside all three directories rather than silently ignoring them.
2. **Non-regular entries.** After rule 1, any entry that is not a regular file
   is exit 2: directories (including `s151_a.json`), symlinks, FIFOs and device
   nodes. Do not recurse or follow a link into additional records. Unexpected
   exceptions must exit 2 as specified above.
3. **Report format.** Exit 0 writes zero bytes after completion; exit 1 writes
   records after completion; exit 2 creates/modifies nothing. For exit 1 use
   UTF-8, LF, one object per line, a trailing newline after the final record,
   unescaped non-ASCII characters (`ensure_ascii` off), and fixed key order
   `input_id`, `prolog`, `lean`. This refines the report encoding, not the
   comparison's strict typing or canonical observations.
4. **IDs and duplicate keys.** Case-sensitive comparison, the lexical grammar,
   stem equality and rejection of duplicate IDs/JSON keys restate existing
   requirements. Reject duplicate keys inside records rather than silently
   accepting the last value. Byte-identical filename stems cannot coexist in
   one ordinary directory; that fact does not check duplicate JSON keys.
   The ASCII-case-fold uniqueness requirement above is the new restriction
   and must be in force before Checkpoint 1's freeze.
5. **Aliasing.** Compare directory identities, not path strings: exit 2 if any
   two of `--inputs`, `--prolog-out`, `--lean-out` and the working directory
   share an `(st_dev, st_ino)` pair. For each selected ID, also exit 2 if its
   two engine output files share an `(st_dev, st_ino)` pair. This covers
   directory and file aliases; `realpath` string equality is not sufficient.

The filesystem need not be case-sensitive merely because the OS is Linux or
the platform is `linux/amd64` (A-006). On case-folding storage a later write
can replace an earlier differently-cased filename before the meter sees it.
A remaining stem/ID case mismatch is detectable; its absence does not prove no
collapse occurred. The producer must prevent population loss. The meter cannot
recover an input that was overwritten before invocation.

**Clarification resolved (Dev, 2026-09-21):** rule 1 above explicitly preserves
exit 2 for every other non-JSON entry. A-007's directory-policy escalation is
closed. The accepted rules, including ASCII-case-fold uniqueness, are installed
before the meter exists. No between-checkpoint meter re-pin is planned.

## Independent implementation and acceptance sequence

Dev implements and installs `human/parity/check.py` independently. The builder
does not inspect, implement or propose its source. Invoke only through its CLI:

```sh
python3 -B scripts/parity_conformance.py --meter human/parity/check.py
```

Report the output verbatim, including any WRONG-REASON or informational
divergence. A conformance failure is a finding for Dev; do not change the meter
or suite to reconcile it. Dev explicitly promoted `invalid-input-id` from
informational to enforced. `absent-key-is-not-null` and `no-number-coercion`
remain informational until the envelope-defect classification is settled.
No informational result is silently relabelled as an enforced pass.

The current 20-fixture suite does not cover all five policies (directory entry
types, inode aliasing and the exact report bytes are not comprehensively tested).
A passing run establishes only the tested requirements, not full policy
compliance. The builder has not added conformance fixtures without approval.

After conformance passes, the protected manifest must cover the installed
meter, verify, and be committed. Re-run `scripts/verify_phase0.sh` and report
all results. Checkpoint 0 requires zero failures, zero outstanding **for
Checkpoint 0**, and Dev's explicit signoff. Checkpoint 2 exploits and
Checkpoint 3a statements remain reported under their own headings and remain
mandatory at those checkpoints; they do not enter Checkpoint 0's counters.
Runtime checks are unchanged. Changing tooling output cannot substitute for
the checks or signoff.

The human can implement this envelope comparison independently while the
section-specific payloads are being reviewed. No real comparison implementation
or result canonicalizer is provided here.
