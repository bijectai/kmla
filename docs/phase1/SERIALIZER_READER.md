# Phase 1.1 source reader — paused at the lexical slice

## Implemented and checked

`harness/case_reader.py` is a source-preserving, non-executing parser for the
syntax present in the 376 original cases. It is not a Prolog evaluator, a
grounder, a Household serializer, or a query/output projection.

The fresh serializer context read the signed decisions, shared Interface and
original source. It did not inspect any Oracle implementation, oracle audit,
or the owner meter's source. It changed only `harness/case_reader.py` and
`scripts/test_case_reader.py`, and stopped implementation when directed. This
report and retained accounting were added by the orchestrator after the pause.

- Original UTF-8 bytes and every token's source span are retained. Comments,
  whitespace, quotation spelling, parentheses, duplicates and ordering survive.
- Atoms and double-quoted strings have different AST tags. Dates stay source
  strings at this layer; no date or money semantics is applied.
- Named variables share identity within a statement; anonymous `_` occurrences
  are distinct. Rule-head/body and query-conjunct relationships are preserved.
- Supplied fact/rule text is separated from every directive without executing
  or reconstructing it. Repeated `init` loads remain recorded.
- `% Question` and `% Test` evidence is retained verbatim. The complete test
  goal, including NAF and extra conjuncts, is represented. No free/bound or
  filename heuristic chooses semantic output positions.
- Only the two exact filename/hash pairs in H4.4 receive an in-memory full stop
  after line 26, with original offsets, source hashes and decision provenance.
  A changed named file fails closed; unrelated malformed syntax is not repaired.

## Verification

```sh
python3 -B scripts/test_case_reader.py
python3 -B scripts/test_case_reader.py --accounting
```

Both the worker and the orchestrator ran the tests: **26 passed**. The reader
covers all 376 distinct original IDs and the 256/120 train/test split union.
`READER_ACCOUNTING_2026-09-21.json` retains one row and original SHA-256 per
case. The inventory identity is
`129d8e92303cc5bbdb5167d67ade6c5dafd545bc0f39f8b93554837164d49594`.

| Lexical item after H4.4 | Count |
| --- | ---: |
| Original source bytes | 370212 |
| Bodyless clauses | 5344 |
| Rules | 432 |
| Cases containing rules | 59 |
| Load directives | 378 |
| Declaration directives | 218 |
| Complete test queries | 376 |
| Halt directives | 376 |
| Other directive roles | 0 |
| In-memory H4.4 insertions | 2 |

These are lexical accounting categories, not the signed grounding inventories
or evidence that all clauses execute as intended. All protected files still
match the entry manifest after reading and testing.

## Limits and remaining work

The parser has a fixed operator table for the observed subset. It rejects
unsupported syntax rather than treating it as a value or silently skipping it.
It is not a general Prolog reader; quoted escapes, list tails, floats and other
unneeded forms are deliberately unsupported. Future generated inputs are not
to be restricted to this reader's subset merely to satisfy its tests.

The operator/variable AST checks have **not** been cross-checked against the
pinned interpreter's `read_term` output. Exact clause slices, rather than an
AST pretty-printer, are the handoff for future interpreter grounding. That
cross-check remains a builder verification task before relying on the AST for
semantic extraction. No semantic round trip or Lean/Prolog parity has run.

Still unimplemented: H4 grounding, Household construction, Prolog/Lean emission,
query-mode/output-position projection, producer schema, all 376 semantic round
trips, stipulation-independent subset measurement and parity integration.
Production is paused for the owner questions in STATE.md and Q-008/Q-009.

## Self-review

The worker assumed G4/H2's lexical tag distinctions, ordinary statement-local
variable identities, and the documented fixed precedence of the observed
operators. It preserved H1/F13 order and multiplicity, H4.5 duplicate directives,
and only H4.4's two authorized reader repairs. It made no assumption about
grounding, query answers, termination or observation encoding. One initial
diagnostic-regex test failure was corrected; no test reached the three-failed-
edit-cycle circuit breaker. No implementation changed after the pause.
