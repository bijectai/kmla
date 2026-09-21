# Independent parity meter

Add the human-authored `check.py` here once the input/output JSON contract is
finalized. The assistant may invoke the completed meter but must not read or
implement it.

Planned invocation:

```text
python human/parity/check.py --section N --inputs DIR --prolog-out DIR --lean-out DIR
```

The plan requires exit 0 for zero mismatches, or exit 1 with `mismatches.jsonl`
records containing `input_id`, `prolog`, and `lean` for mismatches. An
unimplemented stub must exit 2 with `unimplemented`; no executable stub is
included in this layout-only scaffold.
