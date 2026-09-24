# KMLA handoff

## Current state

- Integration branch: `claude/checkpoint-0-integration`.
- Pushed implementation head checked for this consolidation:
  `fe25216db512aefdb205cdd0ba3e0c8769208176`. The handoff-only commit follows it;
  resolve that revision with `git log -1 --format=%H -- docs/HANDOFF.md` on
  the integration branch rather than treating the implementation hash as HEAD.
- Checkpoint 0 is signed off at owner parent
  `0a2a65ac1313c180bea39d137e6665c01b8e833a`; Phase 1 is authorized.
  **Checkpoint 1 is not passed. No Phase 2 work is authorized.**
- `human/DECISIONS.md` SHA-256:
  `12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a`.
- `human/HASHES.txt` SHA-256:
  `5ff23beb28eacdf18d4428395e1d96e4fc8123a8f51ae29abc7943bf0f6062b9`.
  Both digests checked directly at consolidation. The retained verification
  passes; no protected artifact was installed or re-pinned by this handoff.
- Frozen entry meter SHA-256:
  `c5cc94a60437d393b302a87f6c6fd40d1a1758e610c121f65662c014ff3c92e5`.
  Invoke only via its CLI; never read or implement its source.
- All implementation contexts are quiescent. The pre-existing untracked
  `scripts/__pycache__/inventory_cases.cpython-314.pyc` is not task work and
  remains untouched. No outstanding implementation changes were present.

Read `docs/PLAN.md`, accepted `docs/PROTOCOL.md` amendments, the applicable
working/lane rules and this file before work. The original PLAN is preserved;
accepted amendments override it. Historical status paragraphs in STATE and
the [verbatim handoff archive](phase1/HANDOFF_HISTORY.md) do not override this
consolidated state. Consult lane-specific reports only from their owning lane.

### Complete, with bounded evidence

| Item | Verified result | Evidence (read only in the appropriate lane) |
| --- | --- | --- |
| Shared boundary and preflight | Read-only runner/CI enforcement, query/stipulation admission, V10 in Valid and ValidStip; these are not production guard or operational coverage proofs | `Interface/`, `docs/phase1/RUNNER_BOUNDARY_2026-09-22.md`, `docs/phase1/QUERY_ADMISSION_RESUMED_2026-09-23.md` |
| Household wire | Recursive StipArg with distinct list encoding; shared fixtures, event Term/Pat and validity semantics preserved | `Interface/HOUSEHOLD_WIRE.md`, `docs/phase1/STIP_LIST_INTERFACE_2026-09-23.md` |
| H4.3(a) | Ordered re-grounding identity passes 376/376 originals | Harness: `docs/phase1/EVENT_DOMAIN_CORRECTION_2026-09-23.md`, `docs/phase1/event-domain-harness-evidence-2026-09-23/full-audit/` |
| H4.3(b) | 114 passes, 262 explicitly unimplemented; no measured mismatch/error/timeout in the restarted run | Same harness evidence; `audit_pass: false`, exit 1 for incomplete coverage |
| Narrow regressions | All 14 country originals and both list originals pass both H4 checks; tax_case_33 retains 1,736 ordered facts and result 27181 | Same harness report; earlier failing evidence is preserved |
| Partial oracle | §7703 slice has 122 kernel-checked assertions; 87 earlier statements unchanged; still parameterized by real downstream dependencies | Oracle: `Oracle/UNPROVED.md`, `docs/phase1/STIP_LIST_ORACLE_2026-09-23.md` |
| Builder regressions | 147 unit tests passed at the implementation head | `docs/phase1/q023-independent-2026-09-23/regression-driver/003.*` |

The broad diagnostic population is **376 Household instances / 297 distinct**.
These are not production records. Full reference parity has not been produced.
No new audit, compilation or evidence re-hashing was performed to consolidate
this file; the results above are checked against the retained repository record.

### Open work, findings and breakers

- **Shared output projections are not yet declared for all 135 queried
  signatures.** H6.5 explicitly says a bound argument presented as the answer
  is an output (`human/DECISIONS.md:916`); `f` positions alone are insufficient.
  `Interface/QuerySchema.lean` and `TIME_SCHEMA.json` supply time/schema roles,
  not the missing complete output declaration. No new semantic mode is authorized.
- **262 H6 observations and full producer records remain unimplemented.**
  `Interface/WIRE.md` / `HOUSEHOLD_WIRE.md` leave full payload/target packaging
  to be fixed once in the shared Interface before either producer uses it.
- **H4.2 bound-purpose exception awaits Dev's installation and re-pin.**
  `docs/contracts/H4_BOUND_PURPOSE_DRAFT.md` is a reviewed, conditionally
  implemented candidate, not signed text. A-020 reviewed it; A-023 corrects
  A-020's outer event-multiset interpretation. Read the draft with that correction
  and current measured evidence, not its historical country/permission hold.
  Full H4.3(b) evidence remains incomplete. Only Dev installs protected text.
- Q-021 country retention, Q-022 recursive stipulation representation and
  Q-023 distinct traversal domain are resolved implementation defects. Their
  immutable answers and failure evidence remain available; none requires
  another A/WIRE choice or Checkpoint 0 sign-off.
- **Oracle obligations remain open:** other root modes, the actual ordered
  §152 provider, source/unification/freshening correspondence, production V7/V8,
  exact V10 universal-decider iff, participant-universe coverage, strict
  measure/phase and fuel adequacy, and every operational R5/R8 actual-time path.
  `Oracle/UNPROVED.md` is the owning ledger. No R5 termination certificate,
  default provider or exhaustion-as-answer is available.
- The two inert `s68_b(alice,2015,250000)` stipulated year findings remain
  source findings, not exclusions or argument repairs (A-014;
  `docs/contracts/A_WIRE_INSTALLATION_2026-09-22.md`).
- No active three-failure breaker remains. The earlier admission/proof breakers
  were resumed under owner authority and resolved; failed goals stay recorded
  in `docs/phase1/QUERY_ADMISSION_CIRCUIT_BREAKER_2026-09-22.txt` and
  `Oracle/UNPROVED.md`. A new three-failed-edit-cycle check stops affected work;
  never weaken an assertion or take a fourth attempt without the required review.
- Runtime publication, offline rebuild closure and independent image deposit
  remain obligations in `docs/contracts/RUNTIME.md`; prior native directive
  baselines are not Lean parity.

### Next work, in order

1. **Before implementing the remaining 262 observations**, declare the
   output-position projections for all **135 queried signatures** once in
   shared `Interface/`, from G2 and H6.5. Include bound arguments presented
   by a case as its answer. Both isolated lanes consume this declaration;
   move the harness's hand-coded projection exceptions into it. Do not infer
   an output solely from `b/f`, choose new modes or silently guess a missing
   decision. This handoff declares the task, not the projection table itself.
2. Fix the remaining lossless record/payload field map and shared fixtures in
   Interface before emitting production records. Preserve WIRE's approved
   record unit and report records, distinct households and originals separately.
3. In the isolated harness lane, implement the remaining H6 observations
   against that declaration; complete both H4.3 checks for every original.
   Preserve all failures and the bound-purpose traversal/cost evidence. The
   H4.2 exception is waiting for **Dev to install it**, never for a builder
   write under human/. No complete round-trip claim precedes complete evidence.
4. In the separate oracle context, continue the explicit unfinished §7703
   modes/providers/guards and proof obligations. R5 work is authorized on the
   narrowed domain with obligations open; an unproved goal is recorded, not a
   reference value or permission to alter semantics. Keep failing tests failing.
   Subsequent fresh section contexts follow **7703, 3306, 3301, 2, 63, 68,
   151, 152, 1**. Do not pass lane implementation through integration.
5. Integrate through opaque engine CLIs, retain outputs and verbatim meter
   mismatches, and obtain all-376 reference parity and hazard accounting for
   Dev's Checkpoint 1 review. No filtering or semantic repair to obtain a pass.

The future generator contract prohibits multibirth persons, multi-date births
and same-birthday eligible pairs as a **validity boundary**, not an
answer-dependent filter. All-years A and the same-birthday graded-domain
limitation remain operative. No Phase 2 generator exists yet.

## Exact owner deliverables for Checkpoint 1

1. Review the H4.2 bound-purpose candidate, A-020 with A-023's correction, and
   the required all-376 H4.3 evidence/cost. Install any approved protected
   wording into `human/DECISIONS.md` and re-pin the manifest personally.
2. For each section, review every source-clause/hazard annotation (NAF, CUT,
   AGG) against the signed decisions; require every hazard to be accounted for.
3. Triage every mismatch, reference exception, timeout and uncovered semantic
   choice. Any clarification is an owner-maintained decision and re-pin;
   implementation is rerun against it, not repaired by editing the source.
4. Review both semantic round-trip checks for all 376 originals and zero
   Lean/Prolog parity mismatches on that same population, with the independent
   meter's entry hash unchanged. Missing outputs/placeholders cannot pass.
5. Explicitly sign off Checkpoint 1 before Phase 2. Tool success, A/WIRE
   acceptance and this handoff do not sign it.

Dev continues to own the four artifacts: DECISIONS, parity meter, gate exploits
and signed invariant statements; every installation under human/, every re-pin
and every checkpoint sign-off. Checkpoint 2 exploits and Checkpoint 3a statements
remain later deliverables, not newly due for Checkpoint 1.

## Existing worktrees — preserved, not cleaned up

Inventory checked with `git worktree list --porcelain` at consolidation. No
worktree was removed or updated. Paths below are relative to
`/Users/devrashie/Documents/csProjects/kmla` except the main checkout itself.

| Worktree | Branch | Head at inventory | Stale? |
| --- | --- | --- | --- |
| Main checkout | `claude/checkpoint-0-integration` | `fe25216` before handoff commit | No; current integration checkout |
| `.claude/worktrees/human-deliverables-474e7d` | `claude/human-deliverables-474e7d` | `6406e0c` | Yes; old artifact work, no local CLAUDE.md present |
| `.claude/worktrees/sara-semantics-interpretation-9ecfee` | `claude/sara-semantics-interpretation-9ecfee` | `00e1b45` | Yes; local CLAUDE.md still assigns the old design-authority role |

Do not start a new session in either stale worktree: old local instructions
or inherited main-checkout instructions can conflict. The owner's transition
requires a separately reviewed roles branch; this consolidation does not
activate any role change. Preserve these worktrees until separately authorized.
