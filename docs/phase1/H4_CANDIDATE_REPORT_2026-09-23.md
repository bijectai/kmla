# H4 candidate measurement — 2026-09-23

**The exact tax_case_33 candidate passes both measured H4.3 checks. General
grounding is halted on the independently reproduced country_/2 loss.** The
coordinating task drafted Q-021 to classify whether H1/H3 already determine
the repair or whether a semantic decision is missing. Its automatic approval
review rejected spawning that consultation before the CLI ran: the reported
authorization covered Q-020, not Q-021's new repository payload. Q-021 has **not
run**; main owns the exact denial and the request for explicit Dev permission.
This lane has neither retried nor bypassed it. No country traversal,
all-bodyless bypass, outer deduplication, source repair or other remedy has been
implemented. This is candidate measurement, not protected installation, complete
376-case verification, parity, Valid certification or Checkpoint 1.

## Files changed by this lane

New implementation and diagnostics:

- `harness/grounding.py`
- `harness/grounding.pl`
- `harness/grounding_findings.pl`
- `scripts/test_grounding.py`
- `scripts/check_grounding_findings.py`
- `scripts/report_grounding_candidate.py`
- this report and fresh `docs/phase1/h4-candidate-evidence-2026-09-23/`

No existing protected artifact, Interface, root status/contract/log, other-lane
file or Git state was edited. Existing raw evidence and the pre-existing
`scripts/__pycache__/inventory_cases.cpython-314.pyc` were preserved. The
coordinating task owns its independent scope/integrity and A-020 assumption
diagnostics; those were not duplicated here. Its retained assumption results are
at `docs/consult/evidence/q020-assumptions-2026-09-23/commands/005.stdout`, with
metadata alongside. This lane references that evidence without claiming to
have produced it.

## Implemented candidate and observed results

Python checks the exact original name and SHA-256
`5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0`, requires
exactly one `purpose_/2` clause, and checks its exact reader text. The Prolog
helper independently checks that unique clause against the expected clause term
up to variable names. A mismatch raises, with no single-input fallback.

The two-input traversal replaces the raising call only for that exact original.
Unary results retain predicate and source-clause provenance. Outer event proofs
are not deduplicated. The inner domain is exactly the `service_/1` projection,
deduplicated by tagged structural identity in first-occurrence order. The full
original `purpose_(Event,Service)` is executed for every pair; successful proofs
are retained in interpreter order without deduplication. Re-emitted ground facts
use the ordinary path, not the candidate exception.

The helper executes unary, binary and stipulation phases, then restores H1's
source-clause order using retained source indices. It does not sort by fact
values. Stipulation extraction uses only case-clause references and their bodies;
it does not collect the base statutory predicate's solutions into stipulations.
Original statute clauses are loaded before case clauses are asserted. Bodyless
purpose wildcards retain patterns; `findall` solution copies are numbered once
in final fact/stipulation order, retaining within-solution sharing. These are
implementation choices intended to realize H1/H2/H4, not an adequacy proof.

The **run-2 tax_case_33** result is:

| Measurement | Result |
| --- | ---: |
| Unary proofs / outer iterations | 316 |
| `service_/1` proofs | 157 |
| Distinct inner service terms | 157 |
| Full two-input calls | 49,612 = 316 × 157 |
| Successful purpose proofs, undeduplicated | 157 |
| Emitted facts / Prolog clauses | 1,736 |
| Emitted stipulations / wildcards | 0 / 0 |
| H4.3(a), exact ordered Household equality | Pass |
| H4.3(b), `tax(alice,2015,Amount)` first solution | 27,181 on both programs |

The tax measurement leaves Amount unbound and uses `once/1`, as H6.1/H6.2
require. It does not test membership of the expected ground answer and never
exhaustively enumerates tax/3. The original expected answer is not an input to
that observation.

Whole grounding-phase CPU/wall times were **0.052637 / 0.052663 seconds** on
the original and **0.034333 / 0.034333 seconds** on the serialized program.
These include all grounding phases, not an isolated purpose-only timer. Tax
first-solution CPU/wall times were **0.901283 / 0.906825 seconds** on the original
and **0.043031 / 0.043031 seconds** on the serialized program. Container/client
elapsed times, which also include loading and encoding, are separately retained
in the command metadata: **1.460759 seconds** original, **0.490272 seconds**
serialized, both exit 0 without timeout. No native-speed or global-extensional-completeness
claim follows from this pinned, translated-runtime measurement.

Complete data: `run-2/tax_case_33.status.json`,
`run-2/ground-0001.measurement.json`, `run-2/ground-0002.measurement.json`,
and the exact emitted `run-2/requests/ground-0002.pl` under the evidence root.
The first run also passed both tax_case_33 checks; both runs remain available.

## Loader defect, correction and failed-cycle accounting

Run-1 then reached `s151_a_neg.pl` and failed before grounding:

```text
ERROR: '$set_predicate_attribute'/3: No permission to modify static procedure `s151_c/4'
ERROR: Defined at /corpus/statutes/prolog/section151.pl:98
```

The failing operation was `dynamic(s151_c/4)` after the original static
definition had loaded, before its `assertz`. This was a builder loader defect,
not a new semantic choice: H4.1 already requires appending case clauses after
the statutes. One corrective edit moved dynamic declarations before statute
loading; original statute clauses still load first, followed by source-ordered
case assertions. The corrected `s151_a_neg` grounding contains its five facts
and exactly its one supplied `s151_c/4` stipulation, with its wildcard intact;
ordered re-grounding passes. No statutory solutions were copied into that list.

Run-1 raw diagnostics are unchanged, including `commands/007.stderr` and
`007.command.json` (Prolog exit 2, no timeout). This is **one failed measurement
followed by one corrective implementation edit** for that loader issue; the
next measurement passed it. It was not escalated as an owner-choice blocker.

## Concrete general-grounder defect: country_/2

Integration review identified that `binary_solution` applies the unary event
domain to country_/2, even though H3 declares its first role as **place**, not
event. No remedy was inferred from that review. A pinned minimal reproduction
ran the unchanged grounder on original `s3306_c_A_pos.pl`, whose source SHA-256
is `4f788e912133535b3433f32fa53d489a9d5933f5f674b485b141ce92d784012b`.
Its line 15 supplies:

```prolog
country_("baltimore, maryland, usa","usa").
```

That fact is absent from the emitted Household because neither unary event is
that place. The grounder's emitted list is idempotent, so **H4.3(a) passes**.
However, H6.5 explicitly fixes `s3306_c_A/3` at mode `bff` for these cases.
The diagnostic enumerates the complete Employer/Employee tuple list with the
service bound, then applies H6.2's tagged, sorted, deduplicated observation.
It does not replace the observation with ground goal truth.

```text
original canonical:    [[{"a":"alice"},{"a":"bob"}]]
serialized canonical: []
```

Thus **H4.3(b) fails**. Raw stdout is `country-finding/commands/007.stdout` and
`008.stdout`; corresponding commands both complete normally. The full finding,
supplied fact, source identity, raw solution lists, canonical observations and
comparison statuses are in `country-finding/finding.json`.

This demonstrates a defect in the **general loader's domain treatment**, not a
counterexample to the tax_case_33-only second-input domain. Whether the correct
country handling is already dictated by H1/H3, and how it relates to H4.2's
event-position traversal, is the coordinating task's Q-021 review. No blanket
bodyless bypass is authorized by this report. In particular, bypassing all
bodyless event clauses could conceal a real re-grounding failure from repeated
outer events. The implementation keeps those outer iterations unchanged; no
duplicate-event remedy or guarantee has been installed.

## Complete population accounting and run-2 interruption

Every one of the 376 original names has both H4 statuses in
`qualified-report/all-376-statuses.json`. The qualified summary combines raw
run-2 statuses with the separate country reproduction, without rewriting either.

| Status | H4.3(a) | H4.3(b) |
| --- | ---: | ---: |
| Pass for the measured comparison | 115 | 1 |
| Fail | 0 | 1 |
| Observation implementation not completed | 0 | 113 |
| Blocked by the halt of general traversal | 261 | 261 |
| Total originals accounted for | 376 | 376 |

**Only tax_case_33 has both checks passed.** The 115 ordered-equality passes do
not certify preservation of original facts or observations; the country witness
shows precisely why that distinction matters. No original was filtered from
the accounting. Producer record count and distinct households among producer
records are **not yet produced**, not 115 or 376.

Run-2 was deliberately interrupted with SIGINT after integration review exposed
the general domain problem. The outer command exited **130** after
**106.039425 seconds**. It completed 114 ordered comparisons, reached one
additional original (`s1_d_pos.pl`) without completing its result, and had 261
not-yet-run originals. Its pre-existing finally block wrote all statuses but did
not classify KeyboardInterrupt: the raw summary therefore has `finding: null`
and the interrupted row says `error:in-progress`. **Neither is evidence of a
successful or completed audit.** The new qualified report explicitly records
the interruption and classifies uncompleted work as blocked. The separate
country reproduction adds one completed ordered comparison and one failing
observation to that raw run. Future driver interruptions now receive explicit
statuses; old evidence was not edited.

The interrupted `run-2/commands/233.stdout` has no completed
`233.command.json`; its streams are not promoted to a result. The process was interrupted while
awaiting the original `s1_d_pos` invocation. Raw artifacts remain intact.

Earlier per-row wording said a shared output schema was absent. That must not
be read as a blanket owner-choice blocker. **Implementing exact H6 observations
is builder work wherever signed H6 already determines the positions**, including
the demonstrated country bff case and the explicit tax scalar mode. General
H6 coverage is simply unfinished here. Only a concrete unresolved role would
justify a semantic escalation. No non-tax success was manufactured because
machine-readable mode declarations are missing.

## Commands and retained evidence

All commands ran from `/Users/devrashie/Documents/csProjects/kmla` with `-B`.
Evidence directories are fresh and non-overwritable.

```text
python3 -B scripts/test_grounding.py
  exit 0; six fail-closed recognition/input-mode tests pass

python3 -u -B scripts/test_grounding.py --evidence docs/phase1/h4-candidate-evidence-2026-09-23/run-1 --timeout 60
  exit 1; tax_case_33 passes both checks, then loader failure retained

python3 -u -B scripts/test_grounding.py --evidence docs/phase1/h4-candidate-evidence-2026-09-23/run-2 --timeout 60
  exit 130 on deliberate SIGINT; incomplete audit, not a clean pass

python3 -u -B scripts/check_grounding_findings.py --evidence docs/phase1/h4-candidate-evidence-2026-09-23/country-finding
  exit 1; country omission and exact H6 observation mismatch retained

python3 -B scripts/report_grounding_candidate.py --run docs/phase1/h4-candidate-evidence-2026-09-23/run-2 --finding docs/phase1/h4-candidate-evidence-2026-09-23/country-finding/finding.json --out docs/phase1/h4-candidate-evidence-2026-09-23/qualified-report
  exit 0; accounting/report generation only, not verification success
```

Every interpreter execution uses `runtime.container` and immutable image
`sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7`.
Each session measures and checks the entire approved runtime identity before
execution. `/human`, `/corpus`, helpers and generated requests are read-only;
the container has no network. The full measured records, commands, raw streams,
source/request hashes and candidate-code identities remain in each evidence
directory. No mutable tag substitution or host case execution occurred.

## Handoff and self-review

Generic grounding changes stop pending authorization to run Q-021 and its
classification. Next work is
the resulting authorized correction or decision, then a fresh full audit and
exact H6 observation implementation. No broad bodyless traversal, exclusion,
deduplication, source edit, comparison weakening or other semantic workaround
has been applied. The narrow tax_case_33 measurements do not justify general
preservation, production record packaging, termination or a checkpoint claim.

Assumptions about Prolog semantics: source-clause order determines ordered
proofs; dynamic declaration before loading permits H4.1 append without changing
the original clauses; `findall` preserves multiplicity and freshens solution
variables; `numbervars` retains sharing within each copied solution; G4 tags
remain distinct; H6 tax uses the first solution while bff paragraph observations
enumerate all tuples. Those assumptions were exercised only by the documented
measurements, not proved for all operational calls. Repeated unary events stay
repeated; no idempotence theorem is inferred from the tax_case_33 result.

Circuit breaker: **three failed edit cycles on one test means stop and report**.
The static-loader issue had one failed measurement and one corrective edit,
then passed. The country observation failed once and triggered the design-flaw
halt, with **zero semantic repair attempts**. The deliberate run-2 interruption
is recorded as an interruption, not hidden as either a pass or a failed edit
cycle. No breaker threshold was reached. No Oracle source/tests/reports, meter
source or gate exploits were inspected; no protected writes, commits, pushes,
PRs or merges were made by this lane.
