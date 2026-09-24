# A-021 country-only correction: 14-case handoff

2026-09-23. **All 14 originals pass H4.3(a), H4.3(b), and the independent
supplied-country-sublist check.** The historical failing diagnostic's unchanged
comparisons now pass on the actual fix; its descriptions were refreshed only.
The final runner also passes three fixed expected-observation regressions,
independent of mutual equality. No new semantic choice was needed.
This closes only the dispatched country slice; it is not all-376 completion,
production admission, Lean parity, protected installation or Checkpoint 1.
The lane stops here for the orchestrator's independent verification and dispatch.

## Implementation and exact scope

- `harness/grounding.pl`: a by-name `country_/2` branch carries each supplied
  ground bodyless clause once, without an event-domain membership test. A source
  rule (including `country_(...) :- true`) or either unbound argument is rejected
  before assertion. This syntactic check is necessary because `clause/3` exposes
  `true` for both a fact and a rule with the body `true`.
- Placement: retain the original 1-based **source-clause index among all
  non-directive case clauses**. The existing stable provenance-index ordering
  interleaves it with the other facts at that index. No fact-value sort, grouping
  at the beginning/end, tag conversion or deduplication is introduced. Multiple
  supplied country clauses keep their respective indices and multiplicity.
  New diagnostic `fact_source_clauses` parallels the entire emitted fact list.
- `harness/grounding.py`: update measurement scope/provenance metadata only.
- New `harness/grounding_observations.py` and `.pl`: explicit H6 plumbing for
  the six approved modes exercised by the ten country-bearing paragraph cases.
  Keep all source bound arguments, strip only outer NAF, project the source
  free arguments in positional order, and retain named-variable sharing and
  anonymous-variable freshness. Fail on other modes/extra conjuncts. This is
  diagnostic plumbing, not a proposed shared payload schema or general H6 map.
- New `scripts/test_country_grounding.py`: eleven Python tests, a fixed 14-case
  verification, direct source-AST country preservation, separately labelled
  omission controls, and six composite/negative pinned-runtime guards.
- `scripts/check_grounding_findings.py`: only its docstring and report `scope`
  now describe a retained omission regression against the current grounder.
  No assertion, observation, comparator or helper change.

The ordinary event traversal, bodyless-purpose wildcard branch, tax33 candidate
domain/checks, per-unary provenance, and stipulated-clause-body extraction are
unchanged. The candidate/ordinary-event tail and the unary/candidate/stipulation
procedures were also compared byte-for-byte against the prior version. No broad
bodyless bypass, outer deduplication, source repair, population filtering,
statute replacement, or comparison weakening was applied.

## Runtime, evidence and commands

Fresh evidence root: `docs/phase1/country-fix-evidence-2026-09-23/`.
Every pinned run verifies the full accepted runtime record, excluding only its
specified `image.local_image_id` field from the record identity comparison;
the dispatched immutable local image identity is checked separately:

```text
image: sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7
runtime identity: 744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92
SWI-Prolog 7.2.3, swi-prolog-nox=7.2.3+dfsg-6, linux/amd64, America/New_York
```

`identity.json`, `runtime-measured.json`, `candidate-code.json`, `slice-code.json`,
per-case source digests, requests and their identities, exact command argv,
stdout, stderr, exit/timeout and elapsed metadata are retained. The existing
`runtime.container` boundary mounts `/human` read-only on every container and
`/corpus` read-only for every case/fixture Prolog invocation; no host case
execution or tag substitution. Runtime-only identity probing is not case
execution. No protected writes, installs or dependency changes were performed.

Exact commands below ran from the repository root with
`PYTHONDONTWRITEBYTECODE=1`. Their driver argv/streams/exit/cost are retained
under the named evidence subdirectory, with no overwrite of older evidence.

```sh
python3 scripts/test_country_grounding.py --evidence docs/phase1/country-fix-evidence-2026-09-23/slice-final --timeout 60
python3 scripts/check_grounding_findings.py --evidence docs/phase1/country-fix-evidence-2026-09-23/legacy-final
python3 -m unittest scripts.test_grounding scripts.test_country_grounding scripts.test_facts scripts.test_runtime scripts.test_runner_boundary
git diff --check -- harness/grounding.py harness/grounding.pl scripts/check_grounding_findings.py docs/phase1/COUNTRY_FIX_REPORT_2026-09-23.md
```

Results:

- `final-driver/001.*`: exit 0, 25.440766 s including runtime preflight and
  Python tests; **11 tests OK**, all 14 checks in each category pass, 3 fixed
  observation anchors pass, and 6 guard groups pass. Measurement-loop elapsed
  time is 22.982118 s. No interrupted run.
- `final-driver/002.*`: exit 0, 3.643503 s. The diagnostic's refreshed-description
  script SHA-256 is `db9d4f2dc153137944a2ea858b2373be548039cf1f7fd8ea6e98c5f2671de852`;
  its unchanged helper is `2e7c25dcbf62a0494d228aa10fcaaedbccbdb6e9e43a56fbb8976e77faf52c22`.
  Country retained, ordered lists equal, original/serialized canonical result
  both `[[{"a":"alice"},{"a":"bob"}]]`. All comparisons are unchanged.
- `final-driver/003.*`: exit 0, **70 tests OK**, 4.638 s test time,
  4.892928 s driver elapsed. This is a scoped harness regression, not a claim
  that every repository test was run.
- Scoped `git diff --check`: exit 0. No Git mutations, commits or pushes.

Earlier successful `legacy-driver/001.*`, `slice-driver/001.*` and
`unit-regression/001.*` remain intact, together with their `legacy-diagnostic/`
and `slice-1/` evidence. Those executions preceded the two new fixed-observation
unit tests and the description-only cleanup; they reported 9 and 68 tests
respectively. The final evidence above records the final implementation/tests.

## Both checks on each original

Full tagged observations and independently recorded source/query/request
identities are in `slice-final/all-14-statuses.json` and each `*.pl.status.json`.
The table's observation is identical on the original and serialized programs.
No ground expected-answer truth was substituted. All ten paragraph observations
exhaust `findall`; all four tax observations use `once(tax(Person,Year,Amount))`
with **Amount unbound**, ignoring the expected amount in the source directive.

| Original | Mode | Facts | H4.3(a) | H4.3(b) | Direct country | Canonical observation / first tax amount |
| --- | --- | ---: | --- | --- | --- | --- |
| s3306_c_A_pos | bff | 13 | pass | pass | pass | `[[{"a":"alice"},{"a":"bob"}]]` |
| s3306_c_A_neg | bff | 13 | pass | pass | pass | `[]` |
| s3306_c_B_pos | bfff | 18 | pass | pass | pass | `[[{"a":"alice"},{"a":"bob"},{"s":"caracas, venezuela"}]]` |
| s3306_c_B_neg | fbbf | 19 | pass | pass | pass | `[]` |
| s3306_c_1_pos | bb | 19 | pass | pass | pass | `[[]]` |
| s3306_c_1_neg | bb | 19 | pass | pass | pass | `[]` |
| s3306_c_1_A_i_pos | bfbfb | 19 | pass | pass | pass | `[[23200,[{"a":"alice_employer"}]]]` |
| s3306_c_1_A_i_neg | bfbfb | 20 | pass | pass | pass | `[]` |
| s3306_c_1_B_pos | bf | 19 | pass | pass | pass | `[[null]]` |
| s3306_c_1_B_neg | bf | 24 | pass | pass | pass | `[]` |
| tax_case_4 | scalar bbf | 25 | pass | pass | pass | `192` |
| tax_case_51 | scalar bbf | 41 | pass | pass | pass | `55528` |
| tax_case_81 | scalar bbf | 20 | pass | pass | pass | `10922` |
| tax_case_82 | scalar bbf | 22 | pass | pass | pass | `986` |

Notable retained inputs: `s3306_c_1_A_i_pos` binds argument 3 to `[bob]`, while
the negative case binds it to atom `bob`; neither is released as a free output
or “corrected”. The all-bound `s3306_c_1` mode observes the empty output tuple,
so success is `[[]]`, not a fabricated scalar answer. `null` in the positive
`s3306_c_1_B` result is an actual unbound Prolog output, not an omitted field.
No free Day positions occur in these six paragraph modes, so this helper makes
no new Day-role inference. H6.2 encoded tuple sorting/deduplication happens only
at the observation boundary; H4.3(a) compares exact ordered Household values.
The permanent runner separately asserts both A-pos observations equal the fixed
`[[{"a":"alice"},{"a":"bob"}]]`; two equal empty/wrong results cannot pass
this anchor. Unit tests explicitly reject wrong original, wrong serialized,
and equally wrong pairs.

## Measured opposite-sign qualification (not an assumed result)

The separate omission controls remove country only from a diagnostic copy of
the emitted Household to reproduce the old loss. They are **not originals,
production inputs, H4 pass inputs, or a remedy**. Neither the original source
nor the actual serialized programs used for H4 comparisons is altered.

- `s3306_c_B_pos`: original/fixed observations have one proof with the tagged
  location above (`commands/015.stdout`, `016.stdout`). The loss control has
  one proof `[[{"a":"alice"},{"a":"bob"},null]]` (`017.stdout`). Thus one
  encoded tuple is added and one lost, **not** a net increase in proof count.
- `s3306_c_B_neg`: original, fixed and loss-control observations all are `[]`
  (`020.stdout`, `021.stdout`, `022.stdout`); no addition was measured here.

This refines A-021's unmeasured prediction. The original `s3306_c_B/4` clause
at `section3306.pl:475–498` does not bind its `Location` from `location_/2`.
With no country facts the NAF branch succeeds with Location still free and
`Location\=="usa"` succeeds; no string location is manufactured. The negative
case also has no American-employer marker. These are source/measurement
explanations, not authority to repair the statute or adjust the comparison.
No new semantic ambiguity or consult question is needed for this fix.
The final runner asserts these exact B-pos/B-neg normal and omission-control
observations, proof counts 1/0 respectively, and set differences (1 added,
1 lost)/(0 added,0 lost). Unit tests reject changed outputs or proof counts.

## Direct preservation and guards

Each original's country clause is independently extracted from the source AST
and compared, with tags/order/multiplicity, to the emitted country sublist; its
source index must also match the grounder's provenance. All 14 pass. H4.3(a)
then covers its re-grounded list too. This does not mistake a fixed point or an
unobservable query for evidence that every supplied fact was retained.

`slice-final/guards.json` contains the separately labelled fixtures:

- Exact mixed fact sequence includes repeated identical country strings, a
  distinct atom-valued country place, intervening event facts, inert `patient`
  versus `patient_`, `medical_institution_`, `retirement_`, and the retained
  `purpose_` wildcard. Country source indices `[1,4,6]` become fact positions
  `[1,5,7]` because the preceding ordinary event clause produces duplicates.
- Duplicate `service_(e)` declarations still multiply ordinary event facts:
  two `agent_`/`patient`/`patient_` copies become four when re-grounded. Country
  remains three copies and the purpose wildcard one. This fixture deliberately
  has unequal H4.3(a) lists; it is a guard against unauthorized outer dedup or
  broad bodyless bypass, **not** an original-case preservation pass.
- Two identical country clauses with zero unary events both survive.
- Four negative requests reject country `:- true`, country `:- fail`, free
  place and free country, each exit 2/no timeout. Verbatim errors retained:
  `ERROR: Unknown error term: country_rule_not_covered` (058/059 stderr) and
  `ERROR: Unknown error term: nonground_country_not_covered` (060/061 stderr).
  These expected rejections are not empty observations or failed originals.

## Accounting and cost

- Original cases in this slice: **14/14**. The other 362 are not remeasured by
  this dispatch; earlier all-376 status evidence remains historical/unmodified.
- Diagnostic Household instances: **14**, of which **13 distinct ordered,
  tagged complete values**. `s3306_c_1_pos` and `s3306_c_1_B_pos` share the same
  Household but have different queries. Distinctness uses exact encoded values,
  not a semantic equivalence or normalized fact set.
- Production record count and production distinct-Household count:
  **not yet produced**; full shared payload/query packaging is not released.
  This measurement is not a set of parity producer records.
- Each pass emits **291 fact instances**, including 14 country facts, and
  **0 stipulations** across the originals. Both grounding passes together emit
  582 fact instances. The original pass has 59 unary event proofs, 15 service
  proofs, and 218 ordinary binary-event fact results. No tax33 candidate is in
  this slice; its domain/traversal remains unchanged, not re-certified here.
- 28 original/serialized groundings, 20 paragraph observations, 8 first-tax
  observations (inside the groundings), 2 diagnostic omission observations,
  and 7 fixture/negative groundings. There are 57 Prolog invocations and four
  identity/preflight commands: 61 logged commands total, elapsed sum 24.897986 s.
  Zero timeouts; the only nonzero exits are the four expected country rejections.
- Original grounding CPU/wall sums: 0.003834749 / 0.003818035 s. Re-grounding:
  0.003536999 / 0.003529072 s. Original+serialized query wall sum: 0.036879539 s.
  These are in-Prolog scoped timers, excluding loading/container overhead;
  driver and command costs above include their broader stated scopes.

## Preserved history, boundaries, and next dependency

The old country-finding, independent country recheck, tax33 probe, run-1 loader
failure, interrupted run-2, and qualified all-376 reports were not overwritten.
The unchanged diagnostic's pass here does not retroactively change those runs.
The earlier static-loader error was an operational implementation defect with
one corrective edit; no new clause loader change is part of this slice.

No Oracle implementation/tests/reports, owner meter source or gate exploits were
inspected. No edits under human/, Interface/, gen/, gate/, consult/, root status,
contracts/logs or git; no commits/pushes. Pre-existing pycache is left untouched;
Python child processes inherited `PYTHONDONTWRITEBYTECODE=1`.

Changed paths: the six implementation/test paths listed above, this report,
and the fresh `docs/phase1/country-fix-evidence-2026-09-23/` tree. Parent owns
status integration, consult serialization and shared artifacts. Next dependency:
parent independent review/verification and an explicit continued-Phase-1
dispatch. General H6 implementation and all-376 preservation remain unfinished
builder work; missing generic plumbing is not relabelled an owner-choice gap.

## Self-review and circuit breaker

Prolog assumptions: `assertz` appends the supplied clauses after the unchanged
statutes; the existing dynamic declarations occur before loading statute
definitions. Clause-reference body execution extracts only supplied clauses,
while resolving their body calls in the full original program. `findall` keeps
proof order/duplicates and freshens variables between solutions; stable index
ordering retains per-clause proof order. Ground atom/string identity is preserved,
and an unbound external observation maps to H6 `null`. `once(tax(...))` has an
unbound amount and is not equivalent to testing the expected ground amount.
This slice exercises zero original stipulations, so it does not newly prove
statute/stipulation behavior. The inert/order/duplicate and unbound/list output
guards check the particular mechanisms used here, not global completeness.

Country implementation: one authorized grounding edit, legacy diagnostic and all
new unit/integration tests pass on first execution; **zero failed country-fix
edit cycles**. The later fixed-anchor additions and description-only cleanup
also pass their first fresh final execution. Four expected fail-closed fixture
exits are test successes. One
ad-hoc evidence-accounting assertion failed by demanding a corpus mount on a
runtime-only identity probe; its transcript is retained in
`handoff-check-attempt-1.txt`. One corrected accounting attempt passed, requiring
RO human on every container and RO corpus on every case/fixture Prolog run;
no runtime/code/semantic comparison changed. Prior loader/candidate failures
remain in their historical reports and were not reset or erased.

**Circuit breaker: three failed edit cycles on one test means stop and report.**
No test reached that threshold. No background work remains after handoff.
