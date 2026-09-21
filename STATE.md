# KMLA state

## Current phase

2026-09-21 (clarifications approved): Dev explicitly closed both Q-007 issues.
Policy 1 now states the exhaustive filename procedure, with exit 2 for every
other non-JSON entry. Checkpoint 2/3a artifacts remain reported under their own
headings, outside Checkpoint 0's counters; runtime checks and explicit owner
sign-off are unchanged. The grep count defect is corrected as directed.
Before any of these edits, the accumulated integration work and evidence were
committed and pushed as `44d2a96` on `claude/checkpoint-0-integration`, using
only the owner's attribution. Checkpoint 0 is not signed off; Phase 1 remains
unstarted and the independent meter remains absent.

Verification after the fixes: **Checkpoint 0: 17 passed, 0 failed, 1
outstanding** (the meter); **later checkpoints: 2 outstanding**, both still
reported under their own headings. Default mode exits 0 without the prior
integer-expression diagnostic; `--strict` exits 1 for the missing meter.
The full new output is in
`docs/contracts/PHASE0_ACCEPTANCE_2026-09-21.after-clarifications.txt`; the old
report is retained unchanged. Eight verifier regressions, four invocation
regressions and eighteen runtime unit tests pass; the 20-fixture self-test and
the existing 408-record protected manifest also verify. No checkpoint sign-off
is inferred from those results.

The preservation push triggered verify run `35649101727` (success) and native
workflow run `35649100277` (failed with no jobs). The native workflow contained
`${{ runner.temp }}` in job-level `env`, where GitHub does not make `runner`
available. Moved that value into the three consuming steps' `env`, without
changing runtime checks. GitHub's context-availability table supports the fix:
https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability
No native baseline is claimed from the failed run; a subsequent successful run
and retained evidence are still needed.

The following acceptance-follow-up entry is historical; the two clarification
holds it describes are resolved by the owner approval above.

2026-09-21 (owner acceptance follow-up): P-SUMLIST and P-RUNTIME are explicitly
accepted. Their schema/pin changes and the five parity policies are installed
in the staged contracts, with one narrow directory-policy case marked open.
`docs/contracts/OWNER_DECISIONS_2026-09-21.txt` preserves the supplied text;
Q-007/A-007 records the design-authority review. The independent meter remains
absent. No Phase 1 work, protected-file edit, commit, push or merge is authorized
by a passing tool alone. Development pauses for the two clarifications below;
native-runtime CI preparation is uncommitted, not a completed native run.

The following dated entries are historical snapshots, superseded where the
accepted P-BUNDLE/P-RUNTIME and current state above say otherwise.

2026-09-21 (later): The consolidation B006 called for is done, under the owner's
explicit authorization to access `human/` for it. The completed
`human/DECISIONS.md` is committed byte for byte; the authoritative
`docs/DECISION_LOG.md` and `docs/consult/evidence/` are installed at their
documented paths; `Interface/Household.lean` now implements the decided
semantics and type-checks with 29 behavioural guards; the worktree that was
nested inside `human/sara/sara/` has been relocated out of the protected bundle
and the corpus tree restored exactly; `human/HASHES.txt` carries a verifying
408-record manifest. What remains of B006 is the part only the owner can do:
the independent parity meter and the submodule pin that must cover it.
Phase 1 implementation has not started.

2026-09-21: The owner reports Phase 0 deliverables cleared and PR #1 merged.
The merge is verified. The expanded semantic decisions are present locally,
including a resolution of B005, but the installed/pinned artifact bundle cannot
yet be verified: see B006 below. Phase 1 implementation has not started.
Do not treat this installation finding as a request to re-author the supplied
semantic decisions or as permission to change anything under `human/`.

## Completed

- Consolidated the Checkpoint 0 record (2026-09-21). `human/DECISIONS.md`
  committed unmodified (sha256 `58dad769…`, matching the digest B006 recorded).
  `docs/DECISION_LOG.md` installed from the semantics lane with every entry body
  verbatim, five stale `PROPOSED` headings corrected to `ACCEPTED` to match their
  own bodies, the builder lane's DL-002 withdrawn as superseded by P-TZ and its
  DL-001 carried forward as the still-pending P-RUNTIME. `docs/consult/evidence/`
  (26 files), A-004, Q-004 and `DECISIONS_RECOMMENDED.md` installed.
- Replaced `Interface/Household.lean` with the decided semantics: G4 terms, D1
  days, H1 shape, H2 kinds, H3's 57 supplied predicates, H4 stipulations over 31
  signatures, H5 year-indexed decidable `Valid`, H6.2 canonical observation. The
  fact and stipulation constructors are generated from the specification's own
  tables. Type-checks on pinned Lean 4.33.1 with 29 behavioural guards passing
  (`scripts/check_interface.sh`).
- Relocated the git worktree that was nested inside `human/sara/sara/.claude/`
  to `.claude/worktrees/`, after confirming every file it produced was installed
  elsewhere, and removed the two empty directories it left in the corpus. The
  archive contains no `.claude` entry, so the corpus tree is again exactly as
  shipped. All 408 other digests under `human/` are unchanged from the start of
  the session; only `DECISIONS.md` differs, because the owner rewrote it.
- Generated a verifying 408-record `human/HASHES.txt`. It is explicitly marked
  incomplete: it cannot cover the parity meter, the exploits or the invariant
  statements, none of which exist.
- Built the pinned runtime and answered the three questions that were blocking
  translation; see `docs/contracts/RUNTIME_OBSERVATIONS.md` and B011.
- The Fable consult channel was published as PR #1 and merged by the owner.
  GitHub reports merge commit `00e1b45ef8a8b7f373cf168f11aed6d73586e763`,
  merged at `2026-09-21T04:59:00Z`. The builder did not merge it.
- Preserved `docs/PLAN.md` and created the repository layout.
- Recorded approved amendments in `docs/PROTOCOL.md`; added the design-flaw
  stop-and-report standard to `AGENTS.md`.
- Verified the supplied archive against a fresh official JHU download:
  `e4f1b845016fc38b95b702bbbb27a5c9af3eadfa856ba585662b8b2cd71c187c`.
- Verified all 400 installed payload files, 376 cases, and 256/120 split coverage.
  Recorded metadata separately in `docs/contracts/SOURCE_AUDIT.json`.
- Staged source, hash, runtime, parity, exploit, and invariant contracts under
  `docs/contracts/`; the tarball pin is explicitly partial.
- Delegated hazard inventory and household drafting to separate Phase 0 agents.
  The source-syntax household draft and its evidence are available; it compiles
  with the pre-existing Lean 4.33.1 toolchain. It is not an approved semantic
  interface. No oracle or serializer work has begun.
- Prepared the staged decision template with 1,243 distinct lexical observation
  sites across all 12 Prolog source files. Core counts: 150 NAF, 2 cuts,
  43 `findall`, 12 `sum_list` (0 `sumlist`), 101 `is`, and 315 conservative
  comparison sites. The scanner's semantic and lexical limits are documented.

## Resolved design blockers

- B001: JHU is the designated primary source. The supplied archive is verified;
  the extracted corpus root is `human/sara/sara/`.
- B002: stage drafts in `docs/contracts/`; the human installs and pins them.
  Never write under `human/`. Preserve earlier scaffold placeholders.
- B003: independent admission witness search and frozen-corpus grading;
  unresolved mutants excluded, v1/v2 rates on the same admitted set.
- B004: parameterized `def ... : Prop`; separate oracle proofs and checked
  refutations. Failed proof search is `PARTIAL`; refutation takes precedence.
- B005: the supplied `human/DECISIONS.md` H4.1–H4.4 now specifies stipulations,
  rule grounding, semantic round-trip identity, and the reader-only treatment
  of the two missing clause terminators. The original source findings remain
  documented in `docs/contracts/HOUSEHOLD.md`. No source repair or serializer
  implementation has been performed by this builder. The current decision
  file still needs to be part of the installed/pinned bundle (B006).

## Blockers

### Acceptance preflight finding (2026-09-21, Q-007)

**Follow-up resolution:** Dev approved the complete directory decision procedure
and phase-specific accounting. These are no longer open owner choices. The
integer-expression defect is fixed; eight focused shell/counting regressions
pass, and the runtime verification block is byte-identical to `44d2a96`.
The historical account below, including the untrusted 17/0/3 output, is retained
for provenance rather than treated as current acceptance or an active hold.

Dev has accepted P-SUMLIST, P-RUNTIME and the five parity policies; their
supplied text is staged in `docs/contracts/OWNER_DECISIONS_2026-09-21.txt`.
The owner meter is still absent. Before running it, a builder-side CLI defect
was reproduced: `parity_conformance.py` passes a relative meter path after
changing cwd to a temporary run directory. Python's file-not-found exit 2 is
then reported as a passing rejection test. A traced `empty-input-population`
fixture using only the staged stub returned `(True, '')` with `[Errno 2] No
such file or directory` for the meter path. This is not a finding against the
owner meter, whose source has not been inspected or implemented.

Q-007/A-007 classifies the relative-path bug as restoration of the existing
published CLI, not a meter divergence. It is fixed by resolving the path before
launch and reporting invocation failures as harness errors; four invocation
regressions pass. Exactly one fixture expectation was changed as Dev directed:
`invalid-input-id` is enforced. Both envelope-defect cases remain informational;
there are still 20 fixtures. No owner meter was run or inspected.

Parity acceptance remains paused for the policy clarification below. Q-007 also asks about
the phase-0 verifier counting Checkpoint 2 exploits and Checkpoint 3a statements
as current outstanding items despite Dev's phase-specific schedule. No gate has
been waived and `verify_phase0.sh` is unchanged.

**Decisions needed from Dev (A-007 escalation):**

1. For a regular non-dot-prefixed, non-JSON file such as `notes.txt` in one of
   the three argument directories, confirm exit 2 or specify the intended
   outcome. The rest of the accepted directory policy is unchanged.
2. Approve or reject reporting Checkpoint 2 exploits and Checkpoint 3a statements
   separately from Checkpoint 0's outstanding count. Do not waive them at their
   owning checkpoints, and do not exempt mandatory runtime/infrastructure
   verification. The existing script is retained and its output reported until
   this is settled. Dev's signoff remains independently required.

A-007 also raised the timing of the case-fold grammar restriction. It has
already been installed before the meter exists, satisfying the requested
before-Checkpoint-1 deadline without a between-checkpoint meter change.

**Evidence correction to A-007 and its appended log entry:** their claim that
`CONTROL_swipl9.json` is not recorded is incorrect. It was committed in
`fb8ce24`; the existing JSON was checked: 376 cases, 312 clean, 64 distinct error
IDs, all 64 with `rdiv/2` type-error diagnostics. The file was preserved. The
answer itself is immutable; this is the correction, not an edit to A-007.

**Evidence still outstanding:** native CI and the fresh full sweep have not run, and
GHCR publication, offline rebuild closure and the independent paper archive
deposit are not complete. The existing runtime record is preserved under
`docs/contracts/runtime-history/`; future builds must not overwrite its history.
The new current RUNTIME.json records a completed local build, 102 installed
packages and Rosetta for Linux identified from the running Prolog process.
Its file SHA-256 is `c1ca3a433d329ca28818cdd177190f14930a8025e310c0c9f1310d862c1aa12d`.
Eighteen runtime unit tests pass; native and QEMU paths have not been exercised
on real hosts. The new CI workflow is prepared, not dispatched. YAML syntax was
parsed with Ruby Psych; this is not GitHub Actions execution validation.

The unchanged phase-0 script was run with Docker access after the acceptances:
**17 passed, 0 failed, 3 outstanding** (meter, Checkpoint 2 exploits,
Checkpoint 3a statements). It also emitted this diagnostic verbatim:

```text
scripts/verify_phase0.sh: line 206: [: 0
0: integer expression expected
```

Cause: when grep finds zero pending headings, `grep -c ... || echo 0` captures
two zero lines instead of one integer. This is a separate reporting defect,
not a reason to waive the gate. The script is deliberately unchanged while the
requested accounting clarification is pending. No checkpoint was signed off.

### Review hold: builder acceptance tools violate their existing contracts

Historical hold below: the two manifest holes and malformed input fixture were
fixed in `626e404`; the manifest's 24 regressions and fixture self-test passed.
The current holds are the separate Q-007 issues above, not these resolved bugs.

Read-only integration review on 2026-09-21 independently confirmed the committed
decision digest `58dad769…`, a verifying current manifest, and a successful
Lean 4.33.1 interface check with 29 guards. It also reproduced these defects in
isolated temporary fixtures, without implementing or reading the owner meter:

- `scripts/parity_conformance.py:78` constructs its all-agree input using the
  engine-output helper `record()`. It writes `result: null` and omits the
  `payload` required by `docs/contracts/PARITY.md`. A conforming meter that
  checks input envelopes could correctly reject this fixture. A failed suite
  is therefore not currently reliable evidence of a defective owner meter.
- `scripts/human_manifest.py` silently omits symlinked directories from its
  inventory. Generation followed by verification accepts such a tree, despite
  HASHES.md's symlink prohibition.
- The same helper excludes every basename `HASHES.txt`, including
  `nested/HASHES.txt`, rather than only the protected root's self-manifest.
  Generation/verification accepted an unlisted nested file in a reproduction.

These are builder-side acceptance-tool findings, not new semantic decisions
or additional human artifacts. Pause reliance on the parity conformance verdict
and migration/integrity acceptance until the helpers conform to the existing
contracts and negative regression tests pass. The current manifest's success
does not demonstrate that its verifier rejects all prohibited trees.

Q-005 requests Fable's classification of the fourteen purported parity gaps
against the written contract, without adding requirements or choosing new
contract rules. No code fix or contract change has been applied in this review.
The production V7/V8 OracleGuards remain outstanding as documented; the passing
interface guards use an always-true test instance, not actual oracle semantics.

A-005 now records `Escalate to Dev: Yes` for items 8, 9, 10, 13, and 14:
non-JSON files, nested input directories, report encoding/line endings, the
definition of ambiguous IDs, and aliased engine-output directories. Preserve
the meter/affected acceptance hold; do not implement owner policy by guessing.
Most of the fourteen listed items are already covered by the current contract
or are integration responsibilities, not fourteen new human prerequisites.
Fable identifies the reproduced helper defects as violations of existing
contracts, not semantic decisions or contract amendments.

Q-006/A-006 reconcile A-005's inconsistent four/five count: the enumerated five
questions govern. A-006 also withdraws the unsupported claim that a
`linux/amd64` pin alone guarantees case-sensitive input/output storage. No
filesystem property of the future runner mounts has been established by this
review. The same narrow owner escalation remains; prior answers are unchanged.

An independent enumeration and SHA-256 comparison, not using the manifest
helper, also verified all 408 currently listed files and found no symlink paths
in the actual protected tree. Thus the reproduced verifier holes are not a
claim of current artifact drift. All 26 evidence files are installed. No
protected file, runtime acceptance, contract, or implementation was changed.

### B006 (mostly cleared): Phase 0 artifacts not fully installed or pinned

Cleared on 2026-09-21: the decisions are committed, the decision log and
evidence are installed at their documented paths, the interface is synchronized,
the nested worktree is out of the protected bundle and `human/HASHES.txt`
verifies. **Two parts remain, and both are the owner's:**

1. `human/parity/check.py` still does not exist. The builder must not write it
   (`docs/PLAN.md` section 1: if Astra writes the meter, zero mismatches means
   self-agreement) and has not. `scripts/parity_conformance.py` will check an
   owner meter against `docs/contracts/PARITY.md` through its CLI alone.
2. Regenerating `human/HASHES.txt` after the meter is installed, so the manifest
   covers it. **No submodule pin is required**: P-BUNDLE keeps `human/` in the
   parent repository, with CI carrying the enforcement the submodule was for.
   `scripts/make_human_submodule.sh` is retained and tested but unused.

The original preflight record follows.

Read-only preflight on 2026-09-21 found:

- `human/parity/check.py` does not exist. Its source was not inspected; there
  is no installed owner meter to invoke through the parity contract.
- `human/HASHES.txt` contains only its two original placeholder comments and
  zero hash records. Its SHA-256 is
  `e5a45c72e50a3843c8a123af194e945723f5fefa06fe0f40d8b3ff55ac48e85a`.
- There is no `.gitmodules` or `human/.git`; `git ls-tree HEAD human` reports
  mode `040000` (an ordinary tracked directory), not a pinned submodule gitlink.
  The existing protected-artifact enforcement prerequisite is not established.
- The expanded `human/DECISIONS.md` is an uncommitted owner change. Its observed
  SHA-256 is `58dad769c0a318e018275dc106b1389e0ac7d89586e0c66bb33f6d8f3e19b30c`.
  It references `docs/DECISION_LOG.md` and `docs/consult/evidence/`, neither of
  which is installed at this checkout's root. Related logs/evidence exist in
  the other registered worktrees; no version was selected or copied by the
  builder. The current `Interface/Household.lean` is still the syntax draft.
- This checkout is `infra/fable-consult` at local commit `608c227` ("human
  deliverables"). That commit is not on merged `main` at `00e1b45`. The dirty
  decision file and the owner's nested worktrees were left untouched; no
  checkout, merge, commit, push, or protected-file mutation was attempted.

The two other registered worktrees were checked for artifact locations, without
reading parity source. Neither contains the meter at its contracted path;
filename searches also found no alternative `*check.py` implementation or
completed human manifest there. The decision log/evidence locations found are:

- `.claude/worktrees/human-deliverables-474e7d/docs/DECISION_LOG.md`.
- `human/sara/sara/.claude/worktrees/sara-semantics-interpretation-9ecfee/docs/DECISION_LOG.md`
  and its `docs/consult/evidence/` directory.

Needed from the owner: identify/install the authoritative cleared artifact
bundle and its reviewed commit, including the independent meter and complete
hash manifest/submodule pin. Preserve the supplied decisions. Re-run entry
verification and establish the read-only runner boundary before starting the
isolated implementation lanes. No checkpoint requirement has been waived.

### Checkpoint 0: Independent decisions and meter

The owner has supplied expanded semantic decisions. The remaining installation
and provenance gap is recorded in B006; the builder must not substitute its
own meter or treat an unpinned bundle as verified. Synchronize the shared
interface with the authoritative cleared decisions before lane dispatch.

### Checkpoint 0: Protected-artifact enforcement

Revised by P-BUNDLE. `human/` stays a tracked directory in the parent repository;
no submodule and no reviewed submodule commit are required. In force:
`human/HASHES.txt` pins all 408 protected files and `.github/workflows/verify.yml`
verifies it and fails any pull request that touches `human/` without an owner
label. Still to do: regenerate the manifest once the meter exists, and establish
the read-only mount in the Phase 1 runner.

Accepted limitation, recorded under P-BUNDLE: enforcement is now detection
rather than impossibility. A pull request can carry `human/` edits in its own
diff, and a `pull_request` workflow runs the version of itself from the PR
branch. CODEOWNERS on `/human/` with required review, or a repository ruleset,
would close this; the owner declined both as unnecessary on 2026-09-21.

## Findings

- JHU links lowercase `sara.tar.gz`; the supplied uppercase URL returned HTTP
  403. The lowercase download matches the installed archive.
- The archive contains 405 AppleDouble metadata entries alongside 400 payload
  files, including 376 companions for 376 case programs. No case was filtered.
- The user calls the artifact SARA v2; JHU's linked page does not state a v2
  label. The exact archive hash is the recorded source identity.

## Validation

Source hash, payload equality, and split inventory checked. No Prolog execution,
oracle compilation, parity comparison, coverage, mutation scoring, or model
evaluation has run. Pinned Docker execution is a Phase 1 requirement.
The staged parity stub exits 2 with `unimplemented`. The household syntax draft
type-checks with installed Lean 4.33.1; no permanent project toolchain was chosen.
A main-agent `lean --version` call auto-downloaded the configured 4.34.0 default;
that newly installed toolchain was removed, restoring the prior installed set
(4.28.0 and 4.33.1); it can be downloaded again if needed.
The lexical scanner self-test passed, and regeneration matched `HAZARDS.json`
byte for byte. All required decision headings and the B005 cross-reference exist.
The original build plan remains byte-identical to the supplied attachment.
All 409 files under `human/` retain the pre-run content snapshot digest:
`612aedfea63b88c5e2d5eb11a4fa1ff6368cd36c91ace68a8b9077bb95daf225`.
No commits, pushes, or PRs were created in this session.

## Resume condition

The owner has reported Phase 0 clearance, and B005's decision is now supplied.
Resume when the authoritative cleared bundle is installed and its meter,
manifest, reviewed submodule pin, and protected runner boundary can be verified
in the implementation checkout. The remaining blocker is B006, not a request
to repeat B005's semantic decision. Subsequent implementation starts only after
that entry verification succeeds.
