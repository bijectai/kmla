# A-023 event-domain correction — harness lane, 2026-09-23

The bounded correction and accounting are complete. The fresh audit visited
all **376 originals**, with **376 H4(a) passes**, **114 H4(b) passes**, and
**262 explicitly unimplemented H4(b) statuses**. No new actual error, mismatch
or timeout occurred. There are **376 diagnostic Households, 297 distinct**.
The audit deliberately exits **1 for incomplete H6 coverage**, not a comparison
failure. This lane is quiescent; no H6 expansion or further work is undertaken.

## Authority and bounded change

Authority is Dev's standing Phase 1 authorization, A-023's existing-contract
classification, and main's bounded dispatch after the clean full scope audit.
No fresh user approval or accepted amendment occurred after A-023. The immutable
`docs/consult/A-023.md` classifies distinct-event traversal as an existing-contract
correction, with no blocking owner amendment, and explicitly withdraws A-020
§3.3's defensible-multiset interpretation. No H4 draft or human artifact was
changed or installed. This report is diagnostic evidence, not Valid, parity,
production-record or Checkpoint 1 approval.

`harness/grounding.pl` now derives `Events` from all `EventProofs` using the
existing stable `distinct_terms/2` helper, whose equality is Prolog `==`.
Only that traversal domain is distinct. `Unary`, `UnaryFacts`, all binary
proofs, source-clause provenance, stable source-clause emission order and the
ordinary step-(ii) path for bodyless event facts remain intact. The country
exception and wildcard handling are unchanged. There is no source repair,
validity/exclusion filtering, deduplication of stored or compared lists, or
comparison weakening.

The old `stats.unary_proofs` meaning is preserved: it counts every unary proof.
New `stats.distinct_event_domain` and top-level `event_domain` diagnose the
distinct count and exact tagged order. `service_proofs` and
`distinct_service_domain` retain their meanings; candidate loop counts still
count the actual traversal calls. `harness/grounding.py` changes only evidence
metadata. No observer, adapter, Interface or H6 mapping was changed here.

Other changed code is limited to `scripts/test_event_domain.py`, the narrowly
corrected synthetic expectation in `scripts/test_country_grounding.py`, and
audit code-identity metadata in `scripts/test_grounding.py`. Evidence and its
read-only accounting checker are under
[`event-domain-harness-evidence-2026-09-23/`](event-domain-harness-evidence-2026-09-23/).

## Fresh witness: N = 69, not a mixed-version round trip

The exact original is `human/sara/sara/cases/s2_b_3_B_pos.pl`, SHA-256
`cdf109a726f44e6b5aced16ad84354a71ef51bd8b1bc3e8899b4fb81f9ac7f8a`.
Its actual query remains `s2_b_3_B(bob,charlie,2018)`.

| Procedure | Source grounding | First re-grounding | Second re-grounding |
| --- | ---: | ---: | ---: |
| Retained legacy procedure | 114 | 204 | 384 |
| Fresh corrected procedure | 69 | 69 | 69 |

These are separate measured procedures. The corrected run starts again from
the original source; it does not feed the legacy 114-fact output into a changed
grounder and call that a same-procedure fixed point. A-023's `114 → N → N`
phrase is only before/after shorthand. All three corrected passes have exactly
**13 unary proofs, 8 distinct event-domain entries, 69 ordered facts and 5
stipulations**. The complete Household is asserted against an independent
literal expectation on each pass, not only compared against the prior output.
Source-clause indices are asserted exactly as well.

The domain, in first-occurrence order, is the atoms `alice_and_bob`,
`alice_dies`, `charlie_and_bob_residence`, then
`bob_maintains_household_2015` through `bob_maintains_household_2019`.
Both `payment_` and `income_` facts for each maintenance event survive.
Both actual `agent_` rule definitions survive: two Bob-agent facts for each
maintenance event. The separate `bob_income` helper is not used to repair the
source's actual call.

[`domain-regressions/witness.json`](event-domain-harness-evidence-2026-09-23/domain-regressions/witness.json)
retains all three measurements (`ground-0001` through `ground-0003`), counts,
query plan and identical complete-Household SHA-256:
`4a84d820e61ee908c46da09cbfff25ca97a4b08b5e9a1d59db0914045a0d2f7f`.
H4.3(a) passes across the three corrected passes. H4.3(b) is explicitly
`unimplemented:approved-H6-projection-not-implemented` for `s2_b_3_B/3 bbb`;
it is not a pass, an invented projection or a new owner-choice blocker.

The legacy first difference remains in the untouched earlier report/evidence:
zero-based fact index 20, original `agent_(bob_maintains_household_2016,bob)`
versus re-grounded `agent_(bob_maintains_household_2015,bob)`, lengths 114/204.
The old 114/204/384 measurements are not rerun, overwritten or transferred into
the corrected audit. A-023's multiplicative-domain explanation is its reviewed
mechanism; the fresh 69 counts and fixed-point equality are direct measurements.

## Exact multiplicity, order and adapter regressions

`scripts/test_event_domain.py` checks two additional exact ordered fixed points:

- Genuine duplicate unary clauses, duplicate binary clauses and multiproof
  rules: **15 facts, 5 unary proofs, 2 domain entries `[z,a]`** on both passes.
  Two `service_(z)` clauses, two unary proofs of `service_(a)`, two
  `agent_(z,p)` clauses, each event's ordered `patient_` proofs `[q,p,q]`, and
  two `amount_(a,7)` proofs all remain. Exact first-pass provenance is checked.
- Tag-sensitive first occurrence: **11 facts, 6 unary proofs, 5 domain
  entries** on both passes, in order string `"z"`, atom `z`, integer `7`,
  atom `'7'`, string `"7"`. The repeated string-event unary fact is retained.
  The order is deliberately not a sorted term order.

One old country synthetic fixture explicitly enshrined the withdrawn
multiset-domain model. Its source is unchanged. Its old exact expectation and
source are preserved in
[`baseline.json`](event-domain-harness-evidence-2026-09-23/baseline.json),
including the old comment and expected first provenance. Historically each
single `agent_`, `patient` and `patient_` clause emitted 2 copies, then 4 on
re-grounding. Under A-023 each emits exactly 1 on each pass. The corrected test
asserts the entire exact **11-fact** Household and source indices `1..11` on
both passes, plus exact predicate counts. Both genuine `service_(e)` clauses,
all three country clauses, inert/unary facts, tags and the wildcard purpose
remain. This is the specific withdrawn expectation's correction, not a relaxed
comparison; separate duplicate/multiproof tests mandate real multiplicity.
The historical `country-final/` evidence is untouched.

Raw provenance for that withdrawn expectation is
`stip-list-harness-evidence-2026-09-23/country-final/requests/ground-0029.pl`
(source SHA-256 `1ed9482c4e94c23a861e6e44724b92ab116461d82626fe7fe4fe91165da2a228`)
and its old re-emission `ground-0030.pl`
(`e1f7721af8515155dcdaf1ec7af56752f0de261c824ac4c51df69b432c20ba62`).
The corresponding `ground-0029.measurement.json` and
`ground-0030.measurement.json` retain **14 → 20** total facts; raw commands and
streams are `commands/055.*` and `commands/056.*`, both exit 0. Both original
and re-emitted requests, measurements, old assertions and bytes remain available,
rather than replacing the history with the new **11 → 11** expectation.

The fresh 14-country slice passes **14/14 H4(a), 14/14 H4(b), and direct
supplied-country preservation**, plus three fixed observation anchors and six
runtime guard groups. It measures 14 diagnostic Households, 13 distinct.
The two list originals freshly pass both H4 checks and exact supplied heads:
`s2_a_1_B_pos.pl` and `s63_d_2_pos.pl`. The latter still uses
`s63_d_2(alice,[2000],2017)`, H6.5 `bbb`, with a bound list, not an integer or
automatically released argument. Recursive aliases/tags/large integers/empty
lists/copy freshness pass. Six unsupported-input guards still refuse with
`unsupported_household_term(V)`, including a supplied `'$VAR'/1` compound;
pre-numbervars validation remains in place. No adapter implementation changed.

## Fresh tax33 measurement and single-kind byte control

Exact original `tax_case_33.pl` SHA-256:
`5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0`.
Both H4 checks pass freshly: **1,736 ordered facts**, no stipulations, and
first-solution tax **27,181** on original and re-grounded programs. All 316
unary proofs identify distinct event terms, so this also supplies the requested
single-kind control. The entire ordered fact wire is byte-identical to retained
pre-fix `stip-list-harness-evidence-2026-09-23/full-audit/ground-0001.measurement.json`.
Fact-wire SHA-256:
`dd4252617bd66e90024693b1ff513d919095f8d35c771e3e13ad1fdd09e9643f`.

The unchanged A-020 candidate makes **316 × 157 = 49,612** two-input calls and
retains **157 successful proofs**. Fresh original grounding CPU/wall seconds
are 0.060605667/0.060625792; first tax observation CPU/wall seconds are
0.807501247/0.808592558. Re-grounding CPU/wall seconds are
0.037796625/0.037807941, and re-grounded tax CPU/wall seconds are
0.042596375/0.042596340. These are measurements, not performance bounds.
Full stats, raw requests/streams and the byte comparison are in
[`domain-regressions/tax33-single-kind.json`](event-domain-harness-evidence-2026-09-23/domain-regressions/tax33-single-kind.json).

## Fresh all-376 accounting

[`full-audit/all-376-statuses.json`](event-domain-harness-evidence-2026-09-23/full-audit/all-376-statuses.json)
contains exactly the 376 unique corpus filenames, with both statuses per case.
This run restarted from the beginning: tax33 first, then every other original
in sorted filename order. No legacy result or separate regression result was
substituted into the broad run. `finding` is null and all originals were visited.

| Check | Pass | Unimplemented | Fail/error | Blocked |
| --- | ---: | ---: | ---: | ---: |
| H4.3(a) | 376 | 0 | 0 | 0 |
| H4.3(b) | 114 | 262 | 0 | 0 |

H4(b)'s exact unavailable status is
`unimplemented:approved-H6-projection-not-implemented`. The 114 passes are
100 tax first-solution comparisons and 14 existing paragraph comparisons;
the latter comprise two cases each for `s2_a_1_B`, `s3306_c_1_A_i`,
`s3306_c_1_B`, `s3306_c_1`, `s3306_c_A`, `s3306_c_B` and `s63_d_2`.
No missing mapping was invented and none of the 262 gaps is counted as a pass.
`audit_pass` is false and driver **exit 1 is solely the unavailable H6 coverage**.
The stop-first-actual-finding policy was retained; no such finding occurred.

Direct country preservation has **14 passes and 362 not-applicable statuses**
(no supplied country). The broad run produced **376 diagnostic Household
instances and 297 distinct exact ordered/tagged Households**. It measured
**17,943 facts and 440 stipulations** on both original grounding and re-grounding.
These are not producer records: production `record_count` and production
`distinct_household_count` remain `not-yet-produced`. Overlapping targeted
measurements are not added to the broad population.

Audit wall time was **442.501002 seconds**; driver wall time **442.640493 seconds**.
The unchanged per-process limit was 60 seconds, with no timeout. The driver,
exact argv and complete streams are in `full-audit-driver/001.*`; each of the
752 groundings and 28 paragraph-observation processes has its own retained
command/stream evidence. The broad witness independently records 69/69 facts
at `ground-0297`/`ground-0298` and still reports its H4(b) mapping unavailable.

[`accounting.json`](event-domain-harness-evidence-2026-09-23/accounting.json)
is an independent read-only cross-check, not another corpus run. Its retained
`verify_evidence.py` checks exact population, all source hashes, actual retained
H4 equalities, status counts, fact/stipulation totals, Household counts, runtime
identities, mounts and unchanged tested lane-code hashes. It independently
checks every successful measurement's first-occurrence tagged domain, all stored
unary proofs, their old stats meaning and source-clause ordering: **798
measurements** across the four fresh groups (9 domain, 6 lists, 31 country,
752 broad). It verifies **9/16/57/780** pinned Prolog read-only human/corpus
invocations in those groups. All **2,725 historical evidence files** and the
three retained old code snapshots pass their SHA-256 checks unchanged.

## Test and failure history

The correction passed its first implementation-test cycle. There were **zero
failed edit cycles** and no recovery edit to make a failing assertion pass.
The A-023-authorized old synthetic expectation correction is explained above;
all new expectations remain exact.

- `units-1/001.*`: **115 tests pass**, exit 0, including facts/recursive-list
  adapters, dispatch, country, source reader, runtime and runner boundaries.
  Test-run time 2.504 seconds; driver 2.736561 seconds. Existing fixture-byte,
  strict decode and closed Lean-emission checks remain included.
- `targeted-drivers-1/001.*`: corrected three-pass witness, genuine duplicates,
  tag order, fresh tax33 and single-kind byte control pass; exit 0, 6.819911 seconds.
- `targeted-drivers-1/002.*`: two list originals and seven list guard groups
  pass; exit 0, 7.497013 seconds. Six child exits 2 are the asserted refusals,
  not unexpected failures or fallback results.
- `targeted-drivers-1/003.*`: all 14 country originals, three anchors and six
  guard groups pass; exit 0, 22.396936 seconds. Four child exits 2 are the
  unchanged asserted refusals of country rules/non-ground country clauses.
- `full-audit-driver/001.*`: all 376 attempted, no actual finding, exit 1 only
  because 262 approved-H6 projections are unimplemented. Six recognition tests
  also pass. No process exceeded its limit.
- `manifest-driver/001.*`: protected manifest verification passes, exit 0.
  It hashes protected bytes without exposing their contents.
- `accounting-driver/001.*`: independent evidence accounting passes, exit 0,
  1.148644 seconds.

All measured execution used the existing pinned runtime via approved Docker
access. No install, alternate Prolog, source repair, fallback or threshold
increase occurred. Earlier legacy failures, including the 114/204/384 defect
and the withdrawn synthetic behavior, remain intact in old evidence rather
than being rewritten as successes.

Main separately reports independent passing corrected 69×3, tax33, synthetics,
country14, list2 and **147 unit tests**, with stable engine hashes, and the
unchanged source snapshot for the independently verified **122 oracle assertions**.
Main's identity record checks seven source/runner files; 87 prior assertion
statements remain unchanged and 122 assertions are proved in total. Main also
reports independent full accounting: 376 exact names/source hashes, ordered
equalities and domain orders; 114 equal observations, 262 unimplemented modes,
and 297 distinct Households. Main identifies the repeated-event originals as
`s2_b_3_B_pos.pl`, `tax_case_16.pl` and `tax_case_41.pl`.
Those are main's reported checks, not additional executions or Oracle inspections
by this lane. No Oracle implementation, test or report was inspected here.

## Identities, preservation and scope boundaries

The pre-correction snapshot records branch `claude/checkpoint-0-integration`
at baseline commit `9fee7c06062cb265a5d7561f7fde2f9a7b2575f5`. Main advanced
shared history during this work; this lane made no Git edits. Tested code is
identified by file hashes, checked stable across targeted and broad execution,
not by assuming the shared HEAD stayed fixed.

- Immutable SWI image:
  `sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7`.
- Full measured runtime identity:
  `744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`.
- Runtime-record SHA-256:
  `c1ca3a433d329ca28818cdd177190f14930a8025e310c0c9f1310d862c1aa12d`.
  SWI 7.2.3, Debian `7.2.3+dfsg-6`, linux/amd64, America/New_York; full runtime
  and execution provenance remain in each group's `runtime-measured.json`.
- Decisions SHA-256:
  `12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a`.
- Protected manifest SHA-256:
  `5ff23beb28eacdf18d4428395e1d96e4fc8123a8f51ae29abc7943bf0f6062b9`.
- Household wire SHA-256:
  `67ffb4bf85e72dc0eee25d94c9500c9fcfa6ef22b20b506ec5b96444d60a2d36`.
- Immutable A-023 SHA-256:
  `5eec13f43f04d0a9c7d85498549f223b4f3e62cbc86af12be9066e00bd44b742`.
- Corrected `harness/grounding.pl` SHA-256:
  `b79f8dff6110ee226d795fc81eec07b392b4222561701dfd9ce8eea929e15c0d`.
- Corrected `harness/grounding.py` SHA-256:
  `42b9f7967746bcd7a39a3a3eda5cf2d906f6120370a145d972cdb0aaa04fead5`.
- `scripts/test_event_domain.py` SHA-256:
  `f5c80c3212c86787ada8e96af50f93c2ce1f76f6a7d26b7d955ba6f4d931127b`.
- Baseline snapshot SHA-256:
  `dc267cc6a0f282e7082db735551ff15113d0d6b5d0a2050255c00f1d7f45cecd`.
  It retains complete old source and hashes for grounding.pl
  (`f92f547d8fdd1a3bf3319842687d5a4d9f8dc2c7280561e6081761aea1956d65`),
  grounding.py and the old country test, plus the historical-file hash manifest.
- All-376 statuses SHA-256:
  `b4350833bea6eed9a0c84f87931b581db53f8fc8e30a8a7fdd40fb3ba0bfdec0`.

Full lane-code and all-376 original-source hash maps are retained in
`full-audit/audit-code.json`; all statute-file hashes and harness/runtime
dependencies are retained in each group's `identity.json`. No mutation to
human, corpus, shared Interface, Oracle, consult, shared status, shared guard
scripts or Git was performed. `human/parity/check.py` and gate exploits were
not inspected. Other writers' changes were left untouched. This report and its
fresh evidence directory are the only new documentation artifacts from this
turn; the earlier stipulation-list handoff remains unchanged.

## Self-review and quiescence

Bounded work is complete and there is no background audit or additional
implementation underway. The 262 unavailable H6 projections remain explicitly
outstanding; this lane will not expand them or claim a complete H4/CP1 gate.

Prolog assumptions: event-domain entries are ground before distinctness;
`==` preserves atom/string/integer identity without binding; first occurrence
preserves the existing unary enumeration order. A matching ground fact supplies
one proof per actual clause, while `findall` preserves every solution and
freshens variable copies between proofs. Stable source-key ordering preserves
within-clause proof order; bodyless facts still traverse ordinary step (ii).
No assumption permits dropping unary/binary duplicates, altering the source,
releasing unspecified H6 inputs or changing tax's first-solution semantics.
The exact witness, duplicate/multiproof, tag, country, list and tax checks
exercise these assumptions on the measured pinned SWI runtime.

Circuit breaker: **three failed edit cycles on one test means stop and report;
no fourth edit and no weakened assertion**. This correction had zero failed
edit cycles. Legacy failures remain evidence, and exit 1 for missing H6 coverage
is not suppressed. The lane is now quiescent.
