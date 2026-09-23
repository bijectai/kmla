# A/WIRE installation and verification — 2026-09-22

Dev's acceptance is recorded verbatim in DECISION_LOG. Checkpoint 0 remains
signed off; **Checkpoint 1 is not signed off**. No Phase 2 generator, complete
producer, production OracleGuards instance or R5/R8 theorem is claimed.

## Installed

- `Interface/Household.lean`: V10 in both Valid and ValidStip, unconditional
  distinct birth-event/day uniqueness, strict DOB/birthless descendant decrease,
  and all-years checks against the single `r5Years` list. The exact original K/c3
  universal-decrease decider is a required dependency, with no default. Test mocks live outside
  Interface, have local scope, and cannot certify a production instance.
- `Interface/QueryTime.lean`: a checked root-year/Workday entry type indexed by
  the actual argument. Workdays use the existing D1 ISO-year conversion.
  Out-of-range inputs fail explicitly. There is no default-year constructor and
  no extra Valid-at-derived-year/V8 restriction. Wrappers are still to be written;
  they must report failure, never return a statute value for it.
- PARITY, Interface/WIRE, PROTOCOL, HANDOFF and STATE: approved WIRE release
  wording, record packaging, lossless byte policy, distinct counts and the exact
  remaining implementation obligations. Full input-field codec/fixtures remain
  work, not an owner semantic choice where the approved sections determine them.
- gen/AGENTS and README: never mint prohibited births/eligible pairs, invoke
  real validity through Interface without reading Oracle source, preserve the
  original-case accounting, and put separate counts in manifests/coverage reports.
  These are requirements for the later generator, not generated-corpus evidence.
- `DECISIONS_R5_A_AMENDMENT.md`: exact protected H5/R5/R8/R9 amendment for Dev's
  installation and re-pin. No file under human was changed by the builder.

The graded-domain limitations include same-birthday eligible dependent pairs,
multibirth persons, multi-date births and a violating eligible pair in *another*
admitted year. Unrelated equal birthdays are allowed. The earlier pinned audit
found zero A exclusions among 376 originals across all 201 years (75,576
K-and-c3 graphs), and rejected both preserved witnesses. This is not full
ValidStip certification, round-trip identity or Lean/Prolog parity.

## Verification commands and observed results

| Command | Result and scope |
| --- | --- |
| `bash scripts/check_interface.sh` | Pinned Lean 4.33.1 compiles; 97 behavioral guards pass, plus two missing-instance examples. Checks all 201 possible injected violation years; original structural assertions retained. |
| `bash scripts/check_query_time.sh` | 19 guards pass, including every one of 73,414 V3-admitted days, plus kernel-checked boundary examples. This proves no operational call-site or R5 termination claim. |
| `python3 -B scripts/test_observation.py` | 3 tests pass: controls, Unicode/tags/exact integers, and encoded solution-set ordering/deduplication. |
| `python3 -B scripts/test_verify_phase0.py` | 10 verifier regressions pass; not a new checkpoint sign-off. |
| `python3 -B scripts/human_manifest.py verify` | Every protected file is listed and its digest matches. The old manifest remains valid because human is untouched. |
| `git diff --check` | Clean whitespace check. |
| `python3 -B docs/contracts/phase1-decision-audit/run_stip_time_audit.py --out stip-time-smoke-20260922-01 --smoke` | 4 original files completed on the pinned runtime; exit 0. |
| `python3 -B docs/contracts/phase1-decision-audit/run_stip_time_audit.py --out stip-time-full-20260922-01` | 376/376 completed, no unresolved case or stderr. **Exit 1** reports two out-of-range stipulated year slots, detailed below; do not relabel this a clean coverage pass. |

## Original stipulated-time measurement — a finding, not a domain change

Retained output: `phase1-decision-audit/stip-time-full-20260922-01/` contains
source/statute/diagnostic hashes, measured runtime identity, actual read-only
mount inspection, every command/stdout/stderr, all 376 per-case records and
summary. Runtime identity is
`744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`.
Human, corpus and diagnostic source mounts were all read-only.

The diagnostic parses case clauses with the pinned reader, retains canonical
statutes and appended clauses in order, and evaluates each appended clause body
with its head positions initially unbound. It does **not** call the whole statute
predicate and mistake its original solutions for appended clauses. H4.4's two
terminators are restored only in memory after hash checks. Original test/load/
halt directives are skipped. This is not a production grounder or a round trip.

Observed: 156 stipulated cases, 203 fact clauses, 28 rule clauses, all 31 H4.1
signatures and 440 appended-clause solutions. The diagnostic classifies 266
bound year slots and 162 bound date slots. There are also 150 wildcard time
slots, **not treated as bounded**: 144 `s3306_c/5` year slots, four `s3306_c/5`
Workday slots and two provisional date slots on the corpus-only `s2_a/5`.

Two explicit year-slot findings:

| Original | Preserved clause | Source signature |
| --- | --- | --- |
| `s151_d_3_B_neg` | `s68_b(alice,2015,250000)` | `s68_b(Taxp,Aa,Taxy)` — year is argument 3 |
| `s151_d_3_B_pos` | `s68_b(alice,2015,250000)` | Same |

Do not swap the arguments to match the natural-language comment or reject the
whole original merely for containing this literal. Each actual test is
`s151_d_3_B(...,alice,_,2015,_)`; `section151.pl:166–168` passes that same bound
year to `s68_b(Taxp,Aa,Taxy)`. The appended head's `250000` cannot unify with
that `2015`. This is a source/unification argument, not an instrumented whole
call-tree proof or a new parity result. It demonstrates why a blanket scan of
stipulation integers is not a valid domain filter. No uncovered **operational**
R5 call has been established by this measurement; none is assumed impossible.

The audit slot table is diagnostic, not a new Interface schema. Most positions
come directly from original predicate heads. H4.1 also includes corpus-only
extra-arity `s151_d/4`, `s2_a/5`, `s63_c_3/4`; the last arguments were audited
as year candidates and s2_a/5's wildcard positions 3/4 as date candidates.
They have no corresponding canonical head from which to prove those roles.
The raw solutions retain every argument for the required typed/mode audit;
these provisional classifications must not become producer field semantics.

Wildcard years/Workdays must be checked when actually supplied to a wrapper.
Do not infer their range from the bound-value census. Complete source-mode and
stipulation matching coverage remains an explicit prerequisite to any R5-group
termination claim. An actually uncovered admitted call must halt and be
reported with evidence, never repaired through filtering or an oracle fallback.

## Review and preserved identities

A-012 temporarily escalated two false premises (fixed-year approval and a
case-year-only audit). A-013 explicitly withdrew them after Q-013 cited the
approved all-years draft and retained audit. Both answers remain immutable.
The remaining issues are existing implementation obligations, not a request for
Dev to approve A or WIRE again. The new measurement above is retained as a
finding rather than reported as the empty census A-013 anticipated.

Final review Q-014/A-014 caught a builder representation defect: a finite
ground-pair list cannot promise completeness with arbitrary wildcard c2/c3
stipulations. The dependency is now `r5AllEligibleDecrease`, with an explicit
iff to A's universal rule, not an enumeration or conservative false-on-unknown.
The Bool-only interface prevents omission but cannot certify correctness;
production equivalence is still owed. This preserves A's domain unchanged.
A-014 also confirms that the two s68_b literal findings need reporting under
P-INTENT, not a new owner decision. No R5 completeness/termination claim follows.

Unchanged SHA-256 identities:

- DECISIONS: `58dad769c0a318e018275dc106b1389e0ac7d89586e0c66bb33f6d8f3e19b30c`.
- HASHES: `7dcf2d707a908b53530dbc2dab4f4fa0e59bf8c033434c95db47c29339128480`.
- Meter: `c5cc94a60437d393b302a87f6c6fd40d1a1758e610c121f65662c014ff3c92e5`;
  hashed only, source never inspected.
- PLAN: `6e446627961f5c93c56b2854f28d3748bee46c62126fef8da2cd000cae159928`.

## Self-review

Prolog assumptions: tag-sensitive identity; birth presence requires birth/agent
solutions even without a date; duplicates keep their source multiplicity; rule
head variables share bindings with their bodies; original clauses precede
appended clauses; a bound integer 2015 cannot unify with 250000. Structural
parent reachability with unbound date outputs must correspond to the original
descendant relation; the exact K/c3 universal decider and that correspondence still
need proof. The strict DOB comparison narrows the approved domain and does not
rewrite source `is_before`. No inferred functionality or successful bounded run
is substituted for the measure/adequacy proof.

Circuit breaker: three failed edit cycles on one test means stop and report.
None occurred. Both new Lean suites passed on their first test run. The
stipulation diagnostic's full-run exit 1 is an unrepaired source-slot finding;
no expectation, case or source was changed to make it pass.
