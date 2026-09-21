# Phase 1 handoff

## Authorization and entry identity

On 2026-09-21 Dev explicitly stated: "I sign off checkpoint 0 and authorize
phase 1". Checkpoint 0 is cleared. The immediately preceding strict verification
reported 17 passed, 0 failed, 0 outstanding; the installed 412-record manifest
verified. Entry commit: `ba1e9206f4bb4cc7067e7bd70a951191b64fa51b`.

- Meter SHA-256: `c5cc94a60437d393b302a87f6c6fd40d1a1758e610c121f65662c014ff3c92e5`.
- Manifest SHA-256: `7dcf2d707a908b53530dbc2dab4f4fa0e59bf8c033434c95db47c29339128480`.
- Meter conformance: 19/20 matching outcomes, no enforced failure. The approved
  informational `absent-key-is-not-null` divergence remains reported, not waived
  or relabelled. The suite does not establish every accepted policy.

## Builder lanes and boundaries

1. Phase 1.1: a fresh serializer/harness context implements case reading,
   pinned Prolog execution and semantic round trips for all 376 cases. It must
   not inspect `Oracle/`. Follow H4 grounding, stipulations and both documented
   reader exceptions; do not filter difficult cases or confuse the earlier
   directive baseline with round-trip or Lean parity.
2. Phase 1.2: a separate fresh oracle context for each section, in order
   7703, 3306, 3301, 2, 63, 68, 151, 152, 1. It must not inspect serializer or
   generator implementation. Shared semantics are only `human/DECISIONS.md`
   and `Interface/`, with original Prolog source read-only. Cite every clause
   and annotate the applicable NAF/CUT/AGG sites. No semantic defaults, `sorry`,
   `partial` or `native_decide` may stand in for missing implementations.
3. The orchestrator owns integration and retains per-section outputs, full
   mismatch evidence, runtime/source/meter identities, and the 376-case coverage
   accounting. Test the actual read-only corpus mount before executing case
   programs. Never expose one lane's implementation to the other to obtain a
   passing comparison. Missing shared decisions stop the affected lane.

The production V7/V8 `OracleGuards` must use real oracle definitions; the Phase 0
test-only instance is not an implementation. `human/` remains strictly read-only.
The meter is invoked only via its CLI in fresh output directories, never read.
Existing runtime archival obligations remain open and are not erased by sign-off.

## Exact human deliverables for Checkpoint 1

No further human artifact was required at Phase 1 entry. The first pass has
since found the specific issues below; development is paused pending review,
without retracting the Checkpoint 0 sign-off.

### Current clarification requests

- Q-008/A-008: approve P-WIRE's replacement of stale pending/blocked producer
  wording with a lossless codec of the already-approved H1-H6/Interface shape.
  Confirm the proposed record unit (one household, target and bound-argument
  tuple) before freezing a corpus. No release or counting-unit change is yet
  installed. Dev separately authorized the control-character JSON restoration;
  it is installed and its three black-box observation tests pass.
- Q-009/Q-010: review the reproduced sibling cycle in the R5 §7703/§152 recursion
  group. Current child-graph acyclicity does not justify the stated person-count
  fuel bound. Any new reference-domain/termination rule must be the owner's
  explicit decision; no rule, truncation or source correction is implemented.
  A-009's suggested equal-birthday exclusion was withdrawn in A-010: a
  second diagnostic uses multiple different birth dates per person and reaches
  the same cycle without any cross-person equal date. A justified replacement
  domain/termination rule remains open; do not adopt the suggested fuel bound
  from that incomplete argument. The owner decision is open in content; A-010
  records the proof obligations, not a replacement approved rule.

The source-reader slice has 26 passing tests covering all 376 case files, with
its full lexical accounting retained in `docs/phase1/`. Grounding, semantic
round trips and oracle parity remain unimplemented. The oracle context produced
a source/mode audit and halted before adding any Lean definitions.

### Review when implementation reaches Checkpoint 1

At Checkpoint 1, Dev must:

- Review the per-section clause/hazard audit and every NAF/CUT/AGG annotation
  against the signed decisions. Require every hazard to be accounted for.
- Triage every reported mismatch, reference exception, timeout or uncovered
  semantic decision. Any semantic clarification belongs in the owner-maintained
  decisions, with a new protected manifest; the builder does not edit them.
- Review semantic round-trip evidence for all 376 cases and zero Lean/Prolog
  parity mismatches across that same population, with the meter hash unchanged
  from the entry identity above. Placeholders and missing outputs do not pass.
- Explicitly sign off Checkpoint 1 before Phase 2 begins.

Checkpoint 2 still requires human-authored gate exploits; Checkpoint 3a still
requires human-signed invariant statements. Neither is newly due in Phase 1.

## Historical Phase 0 handoff

The record below is retained as history. Its earlier absent-meter and pending
sign-off statements are superseded by the Phase 1 authorization above.

## Current state after Dev's 2026-09-21 decisions

### Meter independently audited and accepted by the owner

Dev independently audited and accepted `human/parity/check.py` on 2026-09-21.
The meter, its black-box owner checks and their retained results are installed.
The protected manifest covers 412 records and verifies.

The 20-fixture conformance suite has no enforced failure: 19 checks pass and
`absent-key-is-not-null` retains its directed informational exit-2 divergence.
The additional black-box suite reports 11 checks passed and 0 failed; its
case-fold collision fixture is informational on this host because the
case-insensitive filesystem collapses the two names before invocation. The
strict Phase 0 verifier, with Docker access, reports **17 passed, 0 failed, 0
outstanding for Checkpoint 0**. Complete outputs are retained in
`human/parity/CONFORMANCE_2026-09-21.txt`,
`human/parity/OWNER_CHECKS_2026-09-21.txt`, and
`docs/contracts/PHASE0_ACCEPTANCE_2026-09-21.after-meter.txt`.

The independent owner audit and acceptance are complete. Before Phase 1, Dev
must still explicitly sign off Checkpoint 0. Meter acceptance alone did not
authorize Phase 1.

Work continues on `claude/checkpoint-0-integration`. The accumulated integration
work was committed and pushed as `44d2a96` before applying Dev's follow-up
clarifications. No Phase 1 implementation has begun.

- P-SUMLIST and P-RUNTIME are accepted, not pending. One runtime acceptance
  amends both PROTOCOL B001 and RUNTIME.md. The five parity policies are in
  PARITY.md; Dev's complete directory procedure closes Q-007/A-007's escalation.
- The source and `human/DECISIONS.md` remain untouched. The existing manifest
  covers 408 records; it cannot yet cover the absent owner meter.
- `Interface/Household.lean` passed 29 behavioural guards. The production
  OracleGuards for V7/V8 remain Phase 1 work; test-only guards do not prove them.
- The existing SWI 9.2.9 control is installed at
  `docs/contracts/CONTROL_swipl9.json`: 312 clean outcomes and 64 `rdiv/2`
  errors across 376 cases. The pinned legacy baseline has 376 clean outcomes,
  including two vacuous cases, not 376 exercised assertions.
- Native-runtime CI run `35649969714` on `b265977` completed successfully.
  The downloaded evidence verifies 376 clean directive outcomes, including the
  two known vacuous cases. Its native runtime record and all 1546 diagnostic
  files are retained in `docs/contracts/runtime-history/`; see
  `NATIVE_35649969714.md`. This is not Lean parity. Runtime publication, closure
  vendoring and independent archival deposit remain incomplete; see RUNTIME.md.
  Preserve historical records when rebuilding.

## Follow-up approvals installed

Dev approved both follow-up points; no renewed approval is needed:

1. An entry ending in `.json` joins the population and is judged by the ID
   grammar and regular-file rule; a dotted non-JSON entry is ignored; any
   other entry, including `notes.txt`, is exit 2. No category is left open.
2. The verifier reports exploits under Checkpoint 2 and signed statements under
   Checkpoint 3a, separately from Checkpoint 0's counters. They remain visible
   and mandatory at those checkpoints. Runtime checks are unchanged. The grep
   count bug is fixed, and the new report must replace the earlier untrusted
   17/0/3 result for acceptance purposes. Dev's sign-off is still required.

The corrected local run exits cleanly and reports **17 passed, 0 failed,
1 outstanding for Checkpoint 0** (the absent meter), with the **two later
artifacts still reported separately**. Strict mode correctly exits 1. See
`docs/contracts/PHASE0_ACCEPTANCE_2026-09-21.after-clarifications.txt` for the
complete output. The earlier acceptance report remains unchanged as history.

The case-fold uniqueness grammar is already installed in PARITY.md before the
meter exists, satisfying the requested timing without a between-checkpoint
meter change. No additional sequencing decision is needed for that action.

## Independent meter and completion sequence

The sequence below is mechanically complete: the owner-audited meter exists,
conformance and owner checks pass as reported above, the manifest covers it,
and strict Phase 0 verification has zero current outstanding items. Dev's
explicit Checkpoint 0 sign-off remains.

Dev implements and installs `human/parity/check.py` to PARITY.md and the
accepted policies, including the now-complete directory decision procedure.
The builder must not implement it, inspect its source or propose its algorithm.

A builder CLI preflight found that relative meter paths stopped resolving after
the suite changed cwd. That defect is fixed and four invocation regressions
pass (A-007 classifies this as contract restoration, not changing expectations).
Only `invalid-input-id` was promoted to enforced, exactly as Dev directed.
`absent-key-is-not-null` and `no-number-coercion` remain informational. There
are still 20 conformance fixtures, and they do not cover every new policy.

Once the meter exists:

1. Invoke `python3 -B scripts/parity_conformance.py --meter human/parity/check.py`.
   Report output verbatim, including WRONG-REASON and informational divergences.
   A failure is a finding for Dev; do not alter the meter or expected outcomes
   to reconcile it.
2. Only after conformance passes, refresh `human/HASHES.txt` to cover the
   meter, verify, and commit per Dev's sequence. The conditional manifest step
   has not occurred. No other protected-file write is authorized.
3. Re-run `scripts/verify_phase0.sh`; report all results, with later artifacts
   under their own headings. Checkpoint 0 clears only with zero failures,
   zero outstanding for Checkpoint 0, and
   **Dev's explicit signoff**, not because tooling has become quieter.

Dev will separately correct the decisions preamble's argv/emulation diagnosis.
The actual error was `ENTRYPOINT ["swipl"]` producing `swipl swipl ...`.
Stdin remains valid; the builder does not edit that protected preamble.

## Bundle and source

**No submodule, second repository or URL is required (P-BUNDLE).** `human/`
stays in the parent repository. Bundle identity is
`bijectai/kmla@<parent sha>:human/` plus its manifest. CI detects protected
changes and hash drift; the accepted limitation is detection, not impossibility.
The migration script is retained but unused; additional rulesets were declined.

The canonical JHU archive SHA-256 is
`e4f1b845016fc38b95b702bbbb27a5c9af3eadfa856ba585662b8b2cd71c187c`.
Installed root: `human/sara/sara/`; 400 original payload files and 376 case
programs, with 256/120 train/test splits. No source repair or filtering is
authorized. The accepted reader exceptions are described in the decisions.

## Later checkpoints and implementation boundaries

- Checkpoint 2: human-authored `human/gate/exploits/`, written against GATE.md.
  Do not inspect their source during gate development.
- Checkpoint 3a: human-signed invariant statements. Prove exact statements;
  failed proof search is PARTIAL, not REFUTED.
- Phase 1 requires separate oracle and serializer/generator contexts, shared
  decisions/interface only, and a read-only protected source mount. Neither
  lane may inspect the other's implementation.
- Mutation admission witnesses remain separate from frozen grading inputs.
  Survivors and unresolved mutants remain findings; versioned corpus expansion
  preserves both reported rates.
- On a design flaw, halt the affected work, record evidence in STATE.md and
  ask Dev before changing the design. Never merge a PR.
