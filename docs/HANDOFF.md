# Phase 0 handoff

## Current state after Dev's 2026-09-21 decisions

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
