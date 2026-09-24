# Stipulation-list harness handoff — 2026-09-23

The bounded adapter work is complete on `claude/checkpoint-0-integration`.
Recursive stipulation transport, both named original H4 regressions, and the
14-country regression slice pass. The fresh all-376 audit **stopped at its first
actual mismatch**, `s2_b_3_B_pos.pl`: H4.3(a) expands 114 facts to 204. No remedy,
revised traversal, deduplication, comparison change or post-finding corpus
execution was attempted. This is not full H4 completion or Checkpoint 1.

Main requested quiescence for Q-023. This lane has completed its report and
accounting and has no background process. Main owns the root status/consult
updates; neither was edited here. No new human artifact is required for the
released StipArg correction. Existing protected installation/re-pin obligations
remain with Dev; this handoff supplies no installation or checkpoint approval.

## Delivered adapter changes

`harness/facts.py` now has a distinct recursive `StipArg`: scalar `val(Term)`,
`wild(Nat)`, or an ordered tuple of nested StipArgs under `list`. Stipulation
JSON, Prolog clauses and closed Lean expressions use that type. Event Term/Pat
remain scalar. Strict decoding rejects bare arrays, missing/extra/duplicate
keys, invalid nested tags, nulls, bool/float wildcard IDs, noninteger values,
invalid UTF-8 text, and lists in event positions. Transport preserves stored
IDs without renumbering, all scalar tags, exact integers, order and duplicates.

`harness/grounding.pl` encodes finite proper-list stipulation arguments with
`{"list":[...]}`. It validates them **before** the existing single `numbervars`
traversal so a supplied `'$VAR'/1` compound cannot impersonate a wildcard.
Improper/open-tail lists and unsupported compounds raise the existing
`unsupported_household_term(V)` refusal, with `validate_stip_arg/1` as context.
The source traversal and country-by-name handling are unchanged.
`harness/transport_reader.pl` can inspect emitted recursive list syntax.

The bounded paragraph observer adds only `s2_a_1_B/4 bffb` and `s63_d_2/3 bbb`
under H6.5 and their source Questions. It does not release every bound argument:

| Original | Diagnostic goal | Output tuple | Measured canonical result, both programs |
| --- | --- | --- | --- |
| `s2_a_1_B_pos.pl` | `s2_a_1_B(bob,Q0,Q1,2016)` | `[Q0,Q1]` | `[[{"a":"bob_s_house"},{"a":"charlie"}]]` |
| `s63_d_2_pos.pl` | `s63_d_2(alice,[2000],2017)` | `[]` | `[[]]` |

The first original has three raw proofs on each program, with one canonical
tuple. The second retains the bound **list** `[2000]`; its Question asks whether
that deduction falls under the provision, not for an amount output.
The four Bob s151 heads retain `[charlie]`/`[0]`, years 2014–2017 in order and
four distinct wildcard copies. Alice's head retains `[alice]` and its unbound
fourth argument. Exact head checks are independent of re-grounding equality.

Changed implementation/test files: `harness/facts.py`, `harness/grounding.pl`,
`harness/transport_reader.pl`, `harness/grounding_observations.py`,
`harness/grounding_observations.pl`, `scripts/test_facts.py`,
`scripts/test_swipl.py`, `scripts/test_grounding.py`,
`scripts/test_grounding_dispatch.py`, and new `scripts/test_stip_lists.py`.
Other lane edits observed in the working tree were left untouched.

## Test results and retained failure history

All evidence below is under
[`stip-list-harness-evidence-2026-09-23/`](stip-list-harness-evidence-2026-09-23/).
Every directory is fresh; prior evidence was preserved.

- `units-1/001.*`: **112 tests pass**, including transport, new recursive-list
  regressions, dispatch, country, source reader, runtime and runner boundaries.
  No failed implementation-test cycle preceded this result.
- `lean-transport-final/`: **12 transport tests pass**, with generated Lean
  source and complete stdout/stderr retained. Installed Lean 4.33.1 evaluates
  all eight fixtures and every Fact/Stip constructor; no toolchain installation.
- `fixture-check.json`: the six legacy fixture objects and wire bytes are
  identical to `eeea5f9^:Interface/fixtures/household_wire.json`. All eight
  current fixtures match the encoder byte for byte, including recursive aliases,
  empty lists versus atom `'[]'`/string `"[]"`, duplicates and signed large ints.
- `lists-final/`: **both named originals pass both H4 checks and exact supplied
  heads**. Seven synthetic guard groups pass: nested aliases/tags/large integers/
  empty lists and fresh variables across two proof copies; plus six expected
  refusals (compound, improper tail, open tail, nested improper tail, nested
  open tail, and supplied `'$VAR'(7)`). Re-grounding preserves the nested heads.
- `syntax-final/`: **13 checks pass**: eight shared fixtures, all constructors,
  and four expected parser/directive/rule/compound failures, with raw streams.
- `country-final/`: **14/14 originals pass H4(a), H4(b), and direct supplied
  country preservation**, with three fixed observation anchors and six runtime
  guard groups. This separate slice has 14 Household instances, 13 distinct.
- `final-readonly-checks/001.*`: protected manifest verification passes.
- `full-audit-driver/001.*`: **exit 1**, preserving the actual ordered-list
  mismatch below. All subprocesses completed; the driver did not time out.
  Audit wall time 122.476098 seconds (driver 122.605787 seconds).

Initial `list-driver-1/` / `list-runtime-1/` stopped at Docker image inspection:
`permission denied while trying to connect to the docker API at
unix:///Users/devrashie/.docker/run/docker.sock`. No Prolog process ran in that
attempt. Approved sandbox escalation enabled the existing runtime; no alternate
runtime or installation was used. `list-driver-2/` / `list-runtime-2/` passed
before main's error-name correction. Those historical streams retain the first
spelling; `targeted-drivers-final/001.*` and `lists-final/` verify the required
`unsupported_household_term` spelling after correction. No assertion was weakened.

Main separately reports independent verification of lists, country and 144
unit tests with stable code. Those are main's results, not an additional run
by this lane. No implementation or test execution followed main's final
report/accounting-only direction.

## Exact first mismatch

Original: `human/sara/sara/cases/s2_b_3_B_pos.pl`, SHA-256
`cdf109a726f44e6b5aced16ad84354a71ef51bd8b1bc3e8899b4fb81f9ac7f8a`.
Actual query: `s2_b_3_B(bob,charlie,2018)` (line 49), not evaluated as an H6
observation here. H4(a) failed first; this signature's H6 mapping was also
explicitly unimplemented in the plan.

At **zero-based fact index 20 (21st fact)**:

```json
{"original_grounding":{"ctor":"agent_","args":[{"a":"bob_maintains_household_2016"},{"a":"bob"}]},"regrounding":{"ctor":"agent_","args":[{"a":"bob_maintains_household_2015"},{"a":"bob"}]},"original_length":114,"regrounded_length":204}
```

Both lists have 13 unary proofs; the five stipulations are exactly equal.
The changed predicate counts are `agent_` 25→45, `start_` 23→43,
`end_` 22→42, `amount_` 20→40, and `purpose_` 10→20. Other counts are unchanged.
This is a measured H4(a) inequality, not a process/decode error or an H4(b)
mismatch. No list-valued stipulation failure is claimed for this witness.

The full source-reader request and emitted program are retained:

- `full-audit/requests/ground-0297.pl`, SHA-256
  `bcf7d5b0fcb9e9a078a2dbeb1175cd3b9ef470acf2bc2e2a036b711c216f7257`.
- `full-audit/requests/ground-0298.pl`, SHA-256
  `48818279d1027d0c14f5a955e38ef376a9b4f204a11f2ea6237d485feb1ffd7a`.
- Corresponding complete measurements are `ground-0297.measurement.json` and
  `ground-0298.measurement.json`. Raw commands/streams are `commands/305.*`
  and `commands/306.*`: both exit 0, no timeout, respectively 0.408175 and
  0.464697 seconds. Command metadata records exact argv and read-only mounts.
- [`first-witness.json`](stip-list-harness-evidence-2026-09-23/first-witness.json)
  retains the first difference, adjacent facts, complete unary evidence,
  predicate counts, commands, source/runtime/code identities and the inference.

**Possible mechanism — inference only:** source lines 29 and 42 both enumerate
`bob_household_maintenance` event IDs under `payment_/1` and `income_/1`.
The retained unary evidence contains each maintenance ID twice. The unchanged
grounder preserves that proof multiplicity in its `Events` traversal. Applying
that traversal again to already materialized binary facts appears to multiply
the repeated-event facts and change their ordering. No alternative traversal,
deduplication, source correction or counterfactual execution was tested.
In particular, the source's separate `bob_income` helper is not permission to
replace the actual call at line 42.

Q-023 must classify this preservation failure and establish the authorized next
step under H4.2/H4.3. No remedy or amendment is selected by this report. Affected
grounding development stays halted; the complete witness is ready for main's
serialized consultation and path audit.

## All-376 accounting

[`full-audit/all-376-statuses.json`](stip-list-harness-evidence-2026-09-23/full-audit/all-376-statuses.json)
has exactly all 376 unique corpus names. Execution order remains tax33 first,
then sorted original filenames. The first mismatch was attempt 149; the
remaining 227 originals were not visited. No case was omitted or excluded.

| Check | Pass | Unimplemented | Fail | Blocked |
| --- | ---: | ---: | ---: | ---: |
| H4.3(a) | 148 | 0 | 1 | 227 |
| H4.3(b) | 3 | 145 | 0 | 228 |

H4(b)'s blocked count is one ordered-comparison failure plus 227 unvisited
cases. Its three fresh passes are tax_case_33 and both s2_a_1_B originals.
The separate passing s63_d_2 and 14-country measurements were **not** inserted
as successes in the stopped broad run. Direct country statuses in that broad
run are 149 not-applicable (no supplied country) and 227 blocked.

The broad run emitted **149 diagnostic Household instances, 93 distinct exact
ordered/tagged values**. Original-grounding totals are 4,564 facts and 208
stipulations; re-grounding totals are 4,654 facts and 208 stipulations. These
are diagnostic instances, not producer records. Production `record_count` and
production `distinct_household_count` remain `not-yet-produced`.
Original cases accounted for: **376**. Separate named-case slice: two instances,
two distinct. Counts from overlapping runs are not added together.

[`accounting.json`](stip-list-harness-evidence-2026-09-23/accounting.json), produced
by the retained `verify_evidence.py`, independently rechecks the exact population,
all source hashes, status counts, actual retained H4 equalities, list totals,
Household counts and unchanged lane code. It verifies 16/13/57/302 pinned
Prolog invocations with read-only human/corpus mounts in the final list/syntax/
country/full-audit directories respectively. This is evidence accounting, not
another corpus execution or a replacement for the failed comparison.

## Identities and boundaries

- Immutable image:
  `sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7`.
- Full measured runtime identity:
  `744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`.
- Runtime record SHA-256:
  `c1ca3a433d329ca28818cdd177190f14930a8025e310c0c9f1310d862c1aa12d`.
- SWI 7.2.3, Debian `7.2.3+dfsg-6`, linux/amd64, America/New_York;
  execution provenance and full package closure retained in each measured record.
- Decisions SHA-256:
  `12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a`.
- Protected manifest SHA-256:
  `5ff23beb28eacdf18d4428395e1d96e4fc8123a8f51ae29abc7943bf0f6062b9`.
- Shared Household wire SHA-256:
  `67ffb4bf85e72dc0eee25d94c9500c9fcfa6ef22b20b506ec5b96444d60a2d36`.
- Final `harness/grounding.pl` SHA-256:
  `f92f547d8fdd1a3bf3319842687d5a4d9f8dc2c7280561e6081761aea1956d65`.
- Final `harness/facts.py` SHA-256:
  `98d2ff42d80d36f9e234d78e749a8e58d112941628058952057cd2a83d51404a`.

`full-audit/audit-code.json` records all adapter/check hashes, source hashes and
execution order; `identity.json` also covers the reader, transport inspector
and runtime helpers. The accounting check confirms those hashes still match.
No host Prolog, installs, protected writes, shared Interface/status/consult edits,
git mutations, commits, pushes or PRs were performed. Oracle implementations,
tests and reports, parity meter source and gate exploits were not inspected.
The pre-existing pycache was preserved; Python invocations disabled bytecode.

## Self-review and circuit breaker

Prolog assumptions: G1 clause/proof order and multiplicity remain significant;
findall copies fresh variables between proofs while preserving aliases within
a nested head; numbervars traverses the complete fact/stipulation result once.
Transport itself preserves stored IDs and does not freshen; emitted Prolog
variables retain clause scope and freshen when called. Proper-list containers
remain distinct from scalar atom/string tags, including `[]` versus `'[]'`.
H6 canonicalization occurs only at observation; s63_d_2 keeps its bound list,
s2_a_1_B exposes its two free positions, and tax keeps first-solution behavior.
Unsupported terms remain findings. The multiplicity mechanism above is an
inference, not a validated revised design or claim about source intent.

One implementation batch passed the local and pinned checks; main's requested
error-name correction passed the final runtime checks. Zero failed code-edit
cycles on these tests. The initial Docker permission failure is retained as a
preflight failure. The broad audit encountered one actual H4(a) mismatch and
stopped with **zero remedy edits or retries**. No comparison or assertion was
weakened. The lane is quiescent for Q-023.

**Three failed edit cycles on one test means stop and report: no fourth edit
and no weakened assertion.**
