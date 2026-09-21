# Phase 0 handoff

## Current state after Dev's 2026-09-21 decisions

Work continues from `claude/checkpoint-0-integration` at base commit `fb8ce24`.
Current integration edits are uncommitted. No Phase 1 implementation has begun.

- P-SUMLIST and P-RUNTIME are accepted, not pending. One runtime acceptance
  amends both PROTOCOL B001 and RUNTIME.md. The five parity policies are in
  PARITY.md; one narrow omission is marked open after Q-007/A-007.
- The source and `human/DECISIONS.md` remain untouched. The existing manifest
  covers 408 records; it cannot yet cover the absent owner meter.
- `Interface/Household.lean` passed 29 behavioural guards. The production
  OracleGuards for V7/V8 remain Phase 1 work; test-only guards do not prove them.
- The existing SWI 9.2.9 control is installed at
  `docs/contracts/CONTROL_swipl9.json`: 312 clean outcomes and 64 `rdiv/2`
  errors across 376 cases. The pinned legacy baseline has 376 clean outcomes,
  including two vacuous cases, not 376 exercised assertions.
- Native-runtime CI is being prepared. A workflow definition is not a native
  run. Runtime publication, closure vendoring and independent archival deposit
  remain incomplete; see RUNTIME.md. Preserve historical records when rebuilding.

## Immediate decisions needed from Dev

Development is paused for these clarifications, not for renewed approval of
P-SUMLIST or P-RUNTIME:

1. Should a regular file such as `notes.txt` (not dot-prefixed, not `.json`)
   in an input/output argument directory cause exit 2? Policy 1 explicitly
   covers dotted non-JSON entries and JSON entries; policy 2 covers non-regular
   entries. The remaining regular-file case is not explicitly assigned.
2. May the verifier report Checkpoint 2 exploits and Checkpoint 3a statements
   separately from Checkpoint 0's outstanding counter? They remain mandatory
   at their checkpoints. Runtime/infrastructure requirements must not be
   waived. Until Dev decides, `verify_phase0.sh` is unchanged and its complete
   output must be reported. Dev's signoff is required regardless of counters.

The case-fold uniqueness grammar is already installed in PARITY.md before the
meter exists, satisfying the requested timing without a between-checkpoint
meter change. No additional sequencing decision is needed for that action.

## Independent meter and completion sequence

Dev implements and installs `human/parity/check.py` to PARITY.md and the
accepted policies, including the remaining directory clarification when settled.
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
3. Re-run `scripts/verify_phase0.sh`; report all results and any unresolved
   accounting issue. Checkpoint 0 clears only with the agreed checks and
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
