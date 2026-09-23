# Phase 1.1 isolated harness slice — 2026-09-23

Implemented and verified the settled Household transport slice. **H4 grounding
is halted on a reproduced failure of the prescribed binding mode**, described
below. No replacement grounding procedure has been implemented. Full payload/
query records are also unprovided by Interface/WIRE.md, so no producer records
or reference answers are emitted.

Only this lane's new files and evidence were written. Existing changes,
including the coordinating task's STATE.md/HANDOFF.md/Interface edits, were
preserved. The coordinating task independently reviewed the raw evidence,
recorded the grounding halt in STATE.md, and submitted **Q-017** to Fable.
This lane made no concurrent STATE.md edit, allocated no Q number and authored
no Fable answer. It finishes this report without waiting for Q-017 and remains
halted on alternative grounding, as directed.

## Implemented scope

- `harness/facts.py`: immutable Term/Pat/Fact/Stip/Household data; the exact 57
  Fact and 31 StipPred registries; strict shape checking; JSON value conversion
  and canonical UTF-8 encoding/decoding per HOUSEHOLD_WIRE; exact Int/Nat
  handling without float conversion or Python's decimal digit cap; civil Day
  conversion; ordered Prolog clause and closed Lean Household term emission.
- The codec preserves both lists, duplicates, inert constructors, atom/string
  tags, all control characters, Unicode without normalization, stored wildcard
  IDs, opaque helper arguments and extra stipulated arities. No monetary scaling,
  sorting, deduplication, missing-field defaults, V3 admission or Valid filtering
  occurs. Negative/large money and malformed-arity Stip lists remain transportable
  data; malformed Stip arity is rejected specifically by Prolog clause emission,
  where emitting it would change the source predicate signature.
- Prolog output is a sequence of bodyless clauses, with stipulations following
  facts. A later execution consumer must append stipulated clauses after the
  original statutes. `_KMLA_W<id>` retains the stored ID in variable spelling
  for syntax checks. This does not assert identity across Prolog clause scopes
  or prove invocation/solution-copy freshening. Typed Day arguments become
  double-quoted ISO strings; date-looking Term/Pat values retain their tags.
- Lean emission constructs a closed `KMLA.Household` value. Unicode scalar
  construction avoids escape-dialect ambiguity; no Oracle import, guard
  instance, query year, mode, proof or admission certificate is invented.
- `harness/swipl.py`: diagnostic `PinnedSession`, using runtime.container and
  the exact dispatched immutable image. It measures and compares the entire
  approved runtime identity before running helpers, retains command argv,
  raw streams, timeout/exit status, requests and hashes, and raises on process
  or JSON failures. It supplies no production result schema or query wrapper.
- `harness/transport_reader.pl`: pinned SWI syntax inspection of bodyless
  emitted clauses, preserving argument tags and named variables. Rejects
  directives, rules and unsupported compound values. It never executes those
  clauses. `harness/grounding_probe.pl` is the exact diagnostic below, not a
  grounding implementation or fallback.
- `scripts/test_facts.py` and `scripts/test_swipl.py`: independent field/value
  checks against the shared declarative fixtures and registry, Lean execution
  of emitted data, pinned Prolog re-reading, and retained failure tests.

## Exact validation commands and results

Commands were run from `/Users/devrashie/Documents/csProjects/kmla` with
`python3 -B`; no bytecode/cache writes under human were made.

```text
python3 -B scripts/test_facts.py --evidence docs/phase1/harness-evidence-2026-09-23/facts-final
```

Exit 0: **12 tests pass**. This includes byte-for-byte agreement on all six
shared wire fixtures; inverse equality; all 57/31 registry entries; preservation
of a 5,001-digit integer/wildcard; all 73,414 admitted days checked against the
standard Gregorian calendar; malformed JSON/date rejection; preservation of
nonadmitted data; and Lean 4.33.1 evaluation of all emitted fixture/registry
fields against expected tags, code points and exact numbers. Lean stdout/stderr,
the generated Lean diagnostic, toolchain and source identities are retained in
`harness-evidence-2026-09-23/facts-final/`. This is data evaluation, not a kernel
theorem about grounding, Valid or reference equivalence.

```text
python3 -B scripts/test_swipl.py --evidence docs/phase1/harness-evidence-2026-09-23/transport-final
```

Exit 0: **11 checks pass**. Seven complete tagged clause-sequence comparisons
(six shared fixtures and all registered constructors), with clause counts
0, 7, 3, 7, 5, 10 and 88. Four negative checks report parser failure, directive,
rule and compound-value rejection as failures rather than empty results. Full
process diagnostics, runtime measurement and summary are retained in
`harness-evidence-2026-09-23/transport-final/`. The previous successful fixture
run remains in `transport-1/`; it has not been overwritten.

```text
python3 -B scripts/test_case_reader.py
python3 -B scripts/human_manifest.py verify
git diff --check
```

All exit 0: **26 reader tests pass**; every protected manifest entry matches
and the manifest covers the complete protected population; no diff whitespace
errors. `git diff --check` covers tracked edits and is not a test of new code.

Docker required sandbox escalation to access the daemon socket. The first
restricted attempt failed before any case execution and is retained under
`h4-probe/`. The authorized Docker runs then verified the full runtime identity.
No runtime was installed/rebuilt and no mutable tag was used for execution.

## Grounding blocker: H4.2(ii) on tax_case_33

`human/DECISIONS.md` H4.2(ii) prescribes enumerating binary event predicates with
their event position bound. Original `tax_case_33.pl:29–31` is:

```prolog
purpose_(Payment_event,Service_event) :- split_string(Payment_event,"_","",[Xp,Yp,Zp]),
    split_string(Service_event,"_","",[Xs,Ys,Zs]),
    Xp=="payment",Xs=="workforalice",Yp==Ys,Zp==Zs.
```

The pinned diagnostic consults the original init/statutes from the read-only
corpus, asserts the reader's original case clauses in source order, enumerates
`payment_/1`, selects its first event, and runs exactly:

```prolog
findall(Purpose, purpose_(payment_2015_1, Purpose), Purposes)
```

It does not execute `% Test` directives, rewrite a rule, bind the second
position, filter inputs or catch the exception as an empty answer. The enclosing
diagnostic catches only to print the exception and exit 2.

Verbatim stdout:

```text
{"payment_solutions":157}
payment_2015_1
```

Verbatim stderr:

```text
ERROR: split_string/4: Arguments are not sufficiently instantiated
```

Process exit **2**, `timed_out: false`, elapsed 0.543074 seconds. The failure is
at the unbound `Service_event` passed to line 30's `split_string/4`. This is a
failure of the prescribed grounding call, not a claim that the original tax
query fails, that the original is invalid, or that it may be excluded.

Evidence paths relative to this report:

- `harness-evidence-2026-09-23/h4-probe-docker/commands/005.command.json`:
  exact Docker/Prolog argv, RO mounts, exit and timing.
- Corresponding `005.stdout` and `005.stderr`: unchanged raw streams.
- `h4-probe-docker/requests/001.pl`: exact reader clause material supplied to SWI.
- `h4-probe-docker/requests/001.json`: original and generated-source hashes.
- `h4-probe-docker/runtime-measured.json` and `identity.json`: complete measured
  runtime, source/statute, semantic-specification and harness identities.

Identity values:

```text
image: sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7
runtime identity SHA-256: 744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92
original tax_case_33 SHA-256: 5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0
reader clause request SHA-256: f0f17038e17a3387d456012116ab2ec04aa1d47096ad7f1be0b13cffce270fd1
```

The exact Python diagnostic invocation was:

```python
from harness.swipl import PinnedSession, PrologFailure
s = PinnedSession('docs/phase1/harness-evidence-2026-09-23/h4-probe-docker')
try:
    print(s.probe_h4_tax_case_33().decode())
except PrologFailure as e:
    print(e)
    raise SystemExit(1)
```

It was run through `python3 -B` on stdin; the outer command exits 1 for the
retained Prolog exit-2 finding. A reproduction must choose a NEW evidence
directory; existing evidence is intentionally non-overwritable.

Exact proposed consult question, delivered to the coordinating task:

> H4.2(ii) prescribes enumerating each binary event predicate with only its
> event position bound. On the pinned runtime, `tax_case_33.pl:29–31` raises
> `instantiation_error` for `purpose_(payment_2015_1, Purpose)` because line 30
> calls `split_string/4` on unbound `Service_event`. Does an existing approved
> decision specify a grounding mode covering this rule? If not, please escalate
> the required H4 grounding decision to Dev, specifying how to preserve source
> clause order, solution multiplicity, wildcard behavior, and H4.3 query identity
> across all 376 originals. No alternate binding mode, finite value universe,
> rule rewrite, or case exclusion has been implemented.

## Counts, limits and next dependencies

`transport-final/original-inventory.json` accounts for all **376 originals**
with per-file original SHA-256, rule counts, reader exception counts, and explicit
not-produced grounding/query-identity statuses. It contains **317 bodyless** and
**59 rule-bearing** originals; both H4.4 reader exceptions remain accounted for.
This is a lexical inventory, not 317 or 376 successful grounding results.

| Count | Result |
| --- | --- |
| Producer record count | Not yet produced: full payload/query contract absent |
| Distinct households among producer records | Not yet produced |
| Original-case inventory count | 376, none filtered |
| Original H4 semantic round trips completed | 0 |
| Original Lean/Prolog parity comparisons completed | 0 |

Next dependencies: orchestrator/Fable classification and any required approved
H4 grounding decision; shared full payload/query/mode/projection packaging;
then an authorized continuation implementing the covered grounding procedure
and both H4.3 comparisons. Transport fixtures supply neither semantics nor
admission. Production V7/V8/V10, operational tuple admission, R5/R8 adequacy and
all Checkpoint 1 requirements remain open. Phase 2 was not entered.

## Self-review

- Semantic assumptions: G4 distinguishes atoms, strings and integers; H1/G1
  preserve source-list order and multiplicity; D1 uses civil day counts rather
  than interpreter timestamps; M1 uses whole dollars; A3 preserves stored
  wildcard identity. Transport does not settle variable allocation/freshening,
  grounding universes, modes, output projections or query years.
- Prolog assumptions exercised by tests: pinned SWI 7.2.3 reads emitted
  double-quoted values as strings, quoted atoms distinctly, exact integers,
  named variables and hex control escapes. Those checks are syntax/data
  checks. The H4 probe uses source-order assertion only to expose the original
  rule's prescribed call mode; it is not a general case loader.
- No Oracle implementation/tests/reports, meter source or gate exploit source
  was inspected. No protected write/perms/move/removal, commit, push, PR, merge,
  attribution footer or external message was made.
- Circuit breaker: **three failed edit cycles on one test means stop and
  report**. No transport test required a failing edit cycle. The initial Docker
  socket denial was retained as infrastructure failure. The first actual H4
  probe failed and affected grounding development stopped immediately under the
  design-flaw rule; no semantic repair cycle was attempted.
