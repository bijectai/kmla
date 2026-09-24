# Post-country H4 audit — stopped at list-valued stipulation

2026-09-23. **Not a completed round-trip audit.** The fresh run accounts for
all 376 originals and stops on its first new process failure, original
`s2_a_1_B_pos.pl`, execution position 121. It does not continue past that input,
retry with another encoding, or infer an empty Household/answer. The unaffected
dispatch work is complete; the lane ends this bounded handoff pending main's
classification of the representation finding.

## Verbatim first failure and reproducible input

Source: `human/sara/sara/cases/s2_a_1_B_pos.pl`, SHA-256
`7a5d0387154778ecdb3755377b97e86b64f66558bb5c5d9557b064b439c307f3`.
Original line 40:

```prolog
s151(bob,_,[charlie],[0],Year) :- between(2014,2017,Year).
```

The original statutory head at `section151.pl:2` is
`s151(Taxp,S2,Person_list,Exemptions_list,Taxy)`; its helper constructs the
two lists and computes `sum_list(Exemptions_list,S2)` at lines 48–58. Exact
argument mapping for the supplied clause:

| Position | Original role/name | Supplied value |
| --- | --- | --- |
| 1 | `Taxp`, taxpayer | atom `bob` |
| 2 | `S2`, total exemptions amount | anonymous unbound `_`, retained as wildcard |
| 3 | `Person_list`, ordered persons | list containing atom `charlie`, `[charlie]` |
| 4 | `Exemptions_list`, ordered exemption amounts | list containing integer zero, `[0]` |
| 5 | `Taxy`, taxable year | `Year`, bound by the original `between(2014,2017,Year)` |

The measured error is at position 3's list. Position 4 is also a list in the
source, but the encoder stops at the first error; no separate position-4
execution or inferred successful result is claimed. These are role labels
from the original statute, not a new representation decision or argument
projection. The supplied stipulated clause is not replaced by the statute's
computed values (in particular `_` is not filled with zero).

Original query (not executed as an H6 observation here):

```prolog
s2_a_1_B(bob,_,_,2016)
```

The original-grounding process exits **2**, no timeout, in 0.388587 seconds.
Its stdout is exactly **zero bytes**. Its complete stderr is:

```text
ERROR: Unknown error term: unsupported_household_term([charlie])
```

Fresh evidence root:
`docs/phase1/h4-post-country-evidence-2026-09-23/`.
Exact raw streams and Docker argv are in
`audit-1/commands/245.stdout`, `245.stderr`, `245.command.json`.
The full reader-produced input (all source clauses, original order, no case
directives) is `audit-1/requests/ground-0241.pl`, SHA-256
`e2beafa94e575317c6eebfa148fc045034b77aa1ffc853b66afb1618d9298e6f`.
Its request metadata and registry are retained alongside it. The in-container
command was:

```sh
swipl -q -f none -s /harness/grounding.pl -g main -t halt -- /requests/ground-0241.pl /requests/registry.pl regular none
```

The full original input, not a reduced or modified substitute, is retained for
main's reproduction. No separate post-failure execution was performed. This
is a reported process/representation failure, **not** a measured H4(a) inequality,
H4(b) mismatch, unsupported-query result, or success of the original directive.
No Household was emitted for the failing original and no re-grounding followed.

## Narrow implementation delivered

Changed implementation/test paths only:

- `scripts/test_grounding.py` dispatches to the existing country paragraph
  query builder/observer or existing scalar tax path; imports the existing
  direct country-preservation check. It records exact source queries, plans,
  observations, separate status counts, diagnostic Household counts, source/code
  identities, and a non-pass summary on incomplete coverage or a finding.
- New `scripts/test_grounding_dispatch.py` supplies ten focused dispatch tests.

No edits to the grounding implementation, observation helpers, existing country
test/diagnostic, transport, signatures, source, or shared representations.
The six reused paragraph modes remain exactly:

| Predicate | Mode |
| --- | --- |
| `s3306_c_A/3` | `bff` |
| `s3306_c_B/4` | `bfff`, `fbbf` |
| `s3306_c_1/2` | `bb` |
| `s3306_c_1_A_i/5` | `bfbfb` |
| `s3306_c_1_B/2` | `bf` |

Source bound inputs remain bound, including `[bob]` versus atom `bob`; only
outer NAF is stripped by the existing helper. The same positional free outputs,
named-variable sharing and anonymous-variable freshness are retained. Tax keeps
`once/1` with amount unbound, never `findall` or an expected-ground-answer test.
Unknown/mismatched paragraph modes, extra constraints and multiple source
queries yield an explicit unimplemented plan with no observation execution.
Invalid scalar input modes and invalid dispatch variants raise; there is no
fallback to another mode or to an empty answer. Missing generic H6 plumbing is
builder work, not an asserted missing owner choice.

For every attempted original with supplied country clauses, the runner calls
the existing independent source-AST versus emitted-country-sublist check with
provenance indices, tags/order/duplicates intact. It stops on a failed check.
No country-bearing source was reached before this run's first failure; those
originals remain blocked here. The prior independently verified 14-case result
is not imported as success into this fresh audit.

An H4(a) failure now stops before an H6 comparison; an H6 process failure would
preserve an already measured H4(a) result. Unvisited rows retain both blocked
statuses. Process/decode errors never become empty results; interrupted runs
are explicitly findings rather than a null-finding pass.

## Exact commands and results

Executed from the repository root with `PYTHONDONTWRITEBYTECODE=1`:

```sh
python3 -m unittest scripts.test_grounding scripts.test_grounding_dispatch scripts.test_country_grounding
python3 scripts/test_grounding.py --evidence docs/phase1/h4-post-country-evidence-2026-09-23/audit-1 --timeout 60
git diff --check -- scripts/test_grounding.py scripts/test_grounding_dispatch.py
```

- Focused tests: **27 tests OK**, exit 0; 0.027 s test time / 0.240090 s
  retained driver elapsed. Logs: `unit-regression/001.*`. Includes the six
  candidate/scalar tests, ten new dispatch tests, and eleven country tests.
  Test doubles are unit-test-only; no production or corpus execution is mocked.
- Audit: **exit 1**, no driver timeout; 103.742951 s driver elapsed,
  103.534812 s audit elapsed. Logs: `audit-driver/001.*`. The six existing
  candidate/scalar unit tests also pass inside this invocation. The failure is
  intentionally retained; the audit result is not relabelled a pass.
- Scoped whitespace/diff check: exit 0.

Implementation/test hashes recorded at audit start still match at handoff.
No helper behavior changed, so no repeat of the separate 14-case integration
slice was required. The new broad audit stopped before those cases, as required.

## All-376 accounting, not all-376 verification

`audit-1/all-376-statuses.json` contains exactly 376 unique original names,
with no omitted or duplicate row. `audit-1/audit-code.json` preserves the
376-name execution order and source identities. Order is unchanged: tax33
first, then the other original filenames sorted. All 376 original source
digests match at handoff. The 255 unvisited originals are explicitly blocked.

| Check | Pass | Unimplemented | Error | Blocked |
| --- | ---: | ---: | ---: | ---: |
| H4.3(a), ordered facts + stipulations | 120 | 0 | 1 | 255 |
| H4.3(b), approved observation | 1 | 119 | 0 | 256 |

H4(b)'s blocked entries are the failing case, whose grounding did not complete,
plus the 255 unvisited originals. Only `tax_case_33.pl` has both checks passed
in this run. The failed case's planned H6 mode is separately recorded as
unimplemented (`s2_a_1_B/4 bffb`), but its actual H4(b) status is blocked by the
earlier grounding error. It is not double-counted among the 119 measured-list
cases with unimplemented observations.

Direct country accounting: 120 not-applicable (no supplied country clauses),
one blocked at original grounding, 255 blocked after the finding. **Zero fresh
substantive country checks/paragraph observations** are claimed for this audit.
Their dispatch is wired and unit-tested; previous slice evidence is preserved
separately, not reused to fill these statuses.

Counts, with units kept separate:

- Originals retained/accounted: **376**; attempted: **121**; completed ordered
  comparisons: **120**; remaining unvisited: **255**.
- Diagnostic Household instances successfully emitted: **120**, with **70
  distinct exact ordered/tagged complete values**. No Household for the error.
- Production records and production distinct-Household count:
  **not-yet-produced**. These diagnostics do not supply full payload packaging,
  production `Valid`/`ValidStip`, Lean parity or a checkpoint.
- Per successful grounding pass: **2,238 facts and 141 stipulations**; the
  re-grounding pass has the same counts. Thus 4,476 fact instances and 282
  stipulation instances across both passes. These are not record counts.

## Cost, identities and unchanged candidate

The immutable runtime image is
`sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7`.
Full runtime identity matched
`744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`.
SWI 7.2.3 / Debian package `7.2.3+dfsg-6`, linux/amd64,
`America/New_York`; no tag substitution or host Prolog execution.
Every case invocation retained exact-pin and read-only `/human` + `/corpus`
mounts through unchanged `runtime.container`. Runtime/source/helper identities
and full raw diagnostics are retained even on the failing process.

245 logged commands: four identity/preflight commands and 241 Prolog grounding
invocations (240 completed, one error). Their elapsed-time sum is 102.363930 s;
zero timeouts. Only command 245 exits nonzero. Original successful grounding
CPU/wall sums are 0.081938285 / 0.081840754 s; re-grounding sums are
0.057946035 / 0.057877302 s. These scoped timers exclude loading, encoding,
query and container overhead; failed grounding has no completed stats record.

The fresh tax33 measurement preserves 1,736 ordered facts and scalar 27181 on
both programs. Its unchanged traversal records 316 outer event proofs × 157
distinct inner services = 49,612 two-input calls, retaining 157 successful
proofs. Original grounding wall time 0.057701826 s; re-grounding 0.034706354 s;
first-tax wall times 0.855784893 / 0.042927504 s. This is case-local evidence,
not global completeness or an installed amendment.

`accounting.json` retains the checked totals, identities, unchanged-source/code
checks and the exact failure string. No old evidence, including earlier
interrupted audits or country failures, was overwritten.

## Finding for main: classification and exact question

The source supplies actual list arguments in an approved H4.1 `s151/5`
stipulation. The unchanged encoder reaches `pat_json`/`term_json` and rejects
`[charlie]`. This is independent of the newly wired H6 dispatch and is not
ordinary event-domain loss or the old static-loader error.

Shared `Interface/Household.lean` currently has `Stip.args : List Pat`, with
`Pat.val : Term → Pat` / `Pat.wild`, and `Term` only atom/string/integer.
`Interface/HOUSEHOLD_WIRE.md` likewise spells only those Term cases inside a
stipulation pattern. H6.2's list **observations** do not supply an input-pattern
representation for this clause. No stringification, flattening, omission,
new constructor or schema extension has been chosen here.

Question for main's classification/serialized consult (main plans Q-022;
this lane does not call Fable):

> How must the supplied `s151/5` positions 3 `[charlie]` and 4 `[0]` at
> `s2_a_1_B_pos.pl:40` be represented losslessly through the shared Household
> stipulation pattern and wire contract under H4.1? Does existing signed list
> semantics already determine a missing shared builder representation, or is
> an owner-approved clarification/amendment required? Please identify the
> authoritative representation, including preservation of any permitted
> nested values and variable identity, before either isolated lane adds it.
> The existing atom/string/integer `Term`/`Pat` contract cannot encode this
> observed input; do not repair the source, stringify/flatten/drop the lists,
> widen traversal, or weaken H4 comparison.

No claim is made here that a new owner choice is necessarily required. Main
owns classification, shared Interface/contract coordination and consultation.
The immediate dependency is that representation finding. Independently, the
119 missing H6 observations remain builder mapping work: the first pending
signature is `s151_a/3`, whose amount output must follow H6.1/H6.5 rather than
be inferred from the source's all-bound test. No additional mappings were
implemented or run in this bounded slice.

## Self-review and circuit breaker

Assumptions about Prolog semantics: retain original statute/case append order;
case-clause-reference extraction does not enumerate extra statutory proofs;
`findall` preserves internal proof order and multiplicity and freshens solution
variables; atom/string/integer tags and wildcard identity remain unchanged;
H6 paragraph observations canonicalize only output tuples; scalar tax uses its
first solution with amount unbound. The new dispatch performs no Prolog source
evaluation and does not decide unimplemented modes. A Prolog list in a supplied
stipulation is not assumed to be a scalar Term or an observation-only artifact.

One implementation/test edit batch, all 27 focused tests passing first run.
One fresh corpus audit failure on the list representation, **zero remedy edit
cycles or retries** for that failure. No comparisons or assertions were weakened.
Previous lane failures/cycle accounting remain in their original reports.
**Three failed edit cycles on one test means stop and report; no fourth attempt
or weakened assertion.** No test reached that threshold in this slice.

No Oracle code/tests/reports, owner meter source or gate exploits were read.
No human/Interface/gen/consult/root-status/git mutations, source repairs,
commits, pushes, direct consultations or later-phase work. Pre-existing pycache
is preserved; all Python commands used `PYTHONDONTWRITEBYTECODE=1`.
Changed paths are the two scripts above, this new report and the fresh evidence
subtree only. No background measurement remains after this handoff.
