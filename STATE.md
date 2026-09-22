# KMLA state

## Current phase

2026-09-22 (A and WIRE accepted; Checkpoint 1 unsigned): Dev selected refined
Option A, explicitly requiring query-year coverage before an R5 proof claim and
prohibiting generator-created multibirth persons, multi-date births and
same-birthday eligible pairs. WIRE's two release spans and both handling
proposals are installed in PARITY and Interface/WIRE.md. The record unit is
distinct from household and original-case counts; all three must be reported.
No mode, projection or observation canonicalization changed.

Interface now includes V10 in both Valid and ValidStip, with real fact-based
uniqueness/decrease checks and a required, still-unimplemented original K/c3
universal-decrease decider. Its all-years scope is the accepted proposal, not a new
strengthening. QueryTime supplies a dependent checked-year/Workday boundary,
not a call-site coverage or R5 termination proof. The generator's future-domain
contract is installed; no Phase 2 generator exists. The same-birthday and
conservative all-years exclusions are stated limitations. Dev's protected
H5/R5/R8/R9 installation text is staged in
`docs/contracts/DECISIONS_R5_A_AMENDMENT.md`; human and its manifest are untouched.
Owner installation/re-pin remains due, as do production eligibility, operational
query/stipulation coverage and kernel adequacy. No Checkpoint 1 pass is inferred.

Verification: 97 shared-interface guards, 19 query-time guards (including all
73,414 admitted days), 3 observation tests and 10 verifier regressions pass.
The protected manifest still verifies. The extra pinned stipulated-time audit
completed all 376 cases with no unresolved execution but deliberately exits 1
for two literal out-of-range year slots; see the finding below and
`docs/contracts/A_WIRE_INSTALLATION_2026-09-22.md`. No clean coverage pass is
claimed from that audit.

The dated entries below are historical snapshots, superseded by this acceptance
and the current obligations under Blockers. Checkpoint 0 remains signed off.

2026-09-21 (Greptile remedies installed): Dev authorized sensible patches for
two reproduced enforcement defects. `Interface/Household.lean` now escapes all
JSON control characters; all three black-box observation tests pass. A missing
or empty `human/HASHES.txt` is now a mechanical verifier failure, and
`.github/workflows/verify.yml` invokes manifest verification unconditionally.
Ten verifier regressions, YAML parsing, the 29 Interface guards, manifest
verification and strict Phase 0 all pass. Neither remedy changes statute
semantics or protected artifacts.

2026-09-21 (Checkpoint 0 signed off): Dev explicitly stated, "I sign off
checkpoint 0 and authorize phase 1". Checkpoint 0 is cleared; Phase 1 entry
preparation is active. Entry commit `ba1e9206f4bb4cc7067e7bd70a951191b64fa51b`;
the immediately preceding strict run had 17 passed, 0 failed, 0 outstanding,
with the 412-record manifest verifying. The meter hash frozen at entry is
`c5cc94a60437d393b302a87f6c6fd40d1a1758e610c121f65662c014ff3c92e5`.
The phase handoff now specifies separate fresh contexts, read-only execution,
and the owner's exact Checkpoint 1 review and sign-off deliverables. Sign-off
does not waive the later checkpoints or unfinished runtime archival work.

Phase 1 work is now paused for the A-008 producer-release escalation and the
R5 sibling-cycle finding and remedy review in Q-009/Q-010, following Dev's
stop-and-ask rule.
Two fresh contexts were used without sharing implementations. The serializer
reader passes 26 tests across all 376 original cases; per-case source hashes
and lexical counts are retained under `docs/phase1/`. It does not ground or
serialize Households yet. The §7703 context audited dependencies/modes and
stopped before implementing any Lean definitions. No oracle parity is claimed.
The shared JSON diagnostic now has 3 passing tests after the authorized
control-character escaping restoration. Its before-fix output is retained in
`docs/consult/evidence/observation_before_fix_2026-09-21.txt`. Ten verifier
regressions, four invocation regressions, eighteen runtime regressions and all
29 existing Interface guards pass. The entry meter and manifest hashes are
unchanged; all 412 protected records still verify.

Actual Docker mount inspection verified both `/human` and `/corpus` read-only
without attempting a protected write. The live runtime record matched the
approved local identity. Evidence: `docs/phase1/ENTRY_2026-09-21.json`.

The entries below are historical; their pending Checkpoint 0 sign-off statements
are superseded by this explicit authorization.

2026-09-21 (owner audit and acceptance): Dev states that the installed parity
meter was independently audited and accepted. It is now the owner-accepted
protected meter for Checkpoint 0. No Phase 1 lane is authorized by this
acceptance; Checkpoint 0 still requires Dev's explicit sign-off.

Implementation and mechanical acceptance are complete.
The meter is executable and standard-library-only. The published 20-fixture
suite reports 19 enforced passes, no failures, and the directed informational
`absent-key-is-not-null` exit-2 divergence. Additional black-box checks report
11 passed and 0 failed, with the ASCII-case-fold collision noted as
unmaterializable on this case-insensitive host. `human/HASHES.txt` now covers
412 records and verifies. Both normal and strict Phase 0 verification with
Docker access report **17 passed, 0 failed, 0 outstanding for Checkpoint 0**;
the later Checkpoint 2/3a artifacts remain separately reported. The remaining
hold is Dev's explicit Checkpoint 0 sign-off; Phase 1 has not begun.

2026-09-21 (continuation preflight): `human/parity/check.py` is still absent;
the existing 408-record protected manifest verifies and no protected file was
changed. Phase 1 remains unstarted: a general request to continue does not
substitute for the independent meter or explicit Checkpoint 0 sign-off.
The unchanged verifier was re-run with `--strict`: **17 passed, 0 failed,
1 outstanding** for Checkpoint 0, exit 1 as intended. Both later-checkpoint
artifact groups are still reported separately. No integer-expression diagnostic
occurred, and no acceptance expectation or runtime check was changed.

Native runtime run `35649969714` on `b265977` has now succeeded. Its downloaded
evidence was independently checked: 376 clean directive outcomes, including
two known vacuous cases, matching source/harness hashes, matching full runtime
identity, 376 valid raw case statuses and 752 matching raw stream hashes. All
1546 downloaded files are retained byte-for-byte in the archive documented by
`docs/contracts/runtime-history/NATIVE_35649969714.md`. This closes the native
baseline evidence item, not Lean parity, the local Rosetta sweep, GHCR publication,
offline rebuild closure or independent image deposition. The verify workflow
for the same commit also passed (`35649969482`).

The dated entries below are preserved history; their statements that native CI
is not yet run are superseded by this evidence. The active blocker remains the
independently authored meter and its completion sequence, described below.

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

### Q-014 representation hold — resolved by A-014, equivalence proof still owed

The initial required `r5EligiblePairs` field promises a finite ground-pair list
without carrying the approved universe/query arguments. Well-formed wildcard
c2/c3 stipulations can make infinitely many ground Term pairs eligible, although
A can still reject them by a finite violating witness. Thus an all-ground-pairs
enumeration contract is not a sound implementation requirement. A-014 classifies
this as a builder representation defect, not a new owner decision. It is now
replaced by required `r5AllEligibleDecrease : Household → Year → Bool`, with
no default and an explicit iff with the universal original K/c3 decrease rule.
Both directions are required: false-on-unknown may not silently narrow A.
The semantic equivalence still needs a production proof.
Do not fix this by restricting persons to household literals, omitting wildcard
solutions, or treating a finite test list as production completeness evidence.
No A domain change or R5 proof has been implemented or claimed.

### A-012 review hold — resolved by A-013; coverage implementation still owed

Dev accepted A and WIRE on 2026-09-22, expressly without Checkpoint 1 sign-off.
The shared-interface installation review A-012 temporarily paused R5 edits.
A-013 withdraws its two false premises: the accepted A draft already requires
all 201 years, and the retained audit already enumerated them
(`birth_audit.pl:103`, 75,576 original K-and-c3 graphs). Stipulation coverage and
constructor-error handling are existing implementation obligations, not new
owner choices. No stronger domain or new audit claim is inferred. Actual
wrapper/mode coverage remains unimplemented; no R5/R8 theorem is claimed.
Uncovered time is reported, never a reference answer. A-012 stays immutable.
A-013 requests measurement of original stipulated time arguments; escalate only
if an actual uncovered original is found, with its ID and source-mode evidence.

Measured result: 376/376 executions complete; `s151_d_3_B_neg` and `_pos` each
contain `s68_b(alice,2015,250000)`, with 250000 in the canonical year position.
The actual case query binds Taxy to 2015 and section151:166–168 forwards it
unchanged, so this appended head cannot match that call. Preserve both cases
and the literal; do not impose a blanket stipulation-year filter. Also retain
150 wildcard time slots rather than calling them bounded. This census does not
establish an uncovered operational R5 call or discharge complete mode coverage.
Full evidence/limitations are in the installation report; a real uncovered
admitted call still halts for owner review. A-014 closes the conditional owner
escalation for these two literals specifically; P-INTENT requires preserving
their apparent argument transposition as a source finding.

### Current R5/producer prerequisites — implementation and protected installation

Dev's A/WIRE choices are settled. Before reference use: install/re-pin the
protected amendment, implement/prove the exact original K/c3 universal decider and real
V7/V8, integrate checked operational time at every wrapper/mode, prove universe
coverage and R5/R8 fuel adequacy, and fix the remaining lossless input codec with
shared fixtures. No always-true/empty production guard or default year is allowed.
The staged amendment and HANDOFF enumerate the obligations. Missing signatures
or proofs are unfinished work, not another request to select A/WIRE. Gen's
output-domain contract is not a claim that a generator exists. Checkpoint 1
requires all 376 round trips/parity comparisons and Dev's separate sign-off.

### Historical R5 remedy hold — resolved by refined A; A-009 remains withdrawn

Fable confirmed the original R5 flaw and proposed a V10 excluding equal birth
days among related distinct persons. Orchestrator review found that its proof
silently assumes a single birth date per person, which H1/H5 do not require.
A second read-only pinned diagnostic gives `a` dates 2000 and 2002, and `b` date
2001: no cross-person date equality, both age-order directions succeed, and
the query again exhausts 100,000 and 1,000,000 inferences. Removing only the
sibling fact in the separate control makes it finish. A-010 explicitly withdraws
V10, its global-equal-birthday variant and the proposed `2 * persons.length + 2`
bound. A-009 is preserved unchanged. Do not treat its V10 or suggested
fuel bound as a sufficient remedy or ask Dev to adopt them as proved.
All source and result evidence is retained in `r5_multibirth_cycle*`.

The required owner decision is now open, not yes/no on the withdrawn proposal:
a reference-domain/termination rule over all permitted fact solutions, a derived
fuel/decrease argument (including R8), and corrected R5/R9. A-010 lists the
proof obligations. Both preserved witnesses must be considered; no new input
filter, uniqueness assumption or semantic rule has been installed.

Source-reading qualification to A-010: in the first age disjunct,
`Individual_is_born` and `Individual_dob` are already bound when the final
under-25 conjunct is reached. That conjunct does not independently re-select
the event/date in this branch, contrary to A-010's broader phrasing. The finding
does not rely on that assertion: selections differ between recursive calls,
and all selected dates in the witness meet the under-25 check. The retained
`age_both_directions` probe establishes both directions without that assumption.

### Historical Phase 1.2 §7703 recursive closure — R5 finding (Q-009)

The fresh oracle lane found that R5's child-descent termination argument does
not cover the sibling branch in `section152.pl:178–186`. Sibling symmetry
(`utils.pl:131–144`) and equal birth dates accepted at `section152.pl:204`
permit the static cycle in `docs/phase1/ORACLE_7703.md`: two married siblings
residing together cause `s7703 → s7703_b_1 → s152_c → s152_c_1_E → s7703`
to alternate siblings. The parent graph can be empty, with no V5/V6/V7 triggers
and year 2018 outside V8's divergent region. The orchestrator then ran the
diagnostic input on the measured pinned runtime, with the source read-only:
the query exhausted both 100,000 and 1,000,000 inferences; its finite marriage
prefix succeeded, and removing only the sibling fact in a separate in-memory
control made the query finish. Exact fixture and full bounded results are
retained under `docs/consult/evidence/r5_sibling_cycle*`. This is bounded runtime
evidence plus a static repeated-call argument, not a formal divergence proof or
a kernel-checked production `Valid` certificate.

Halt the affected recursive definitions; do not implement fuel exhaustion as
a truncation heuristic, alter `Valid`, or replace dependencies with stubs.
The independent `(a)`, `(b)(2)`, membership and `(b)(3)` slice does not reach
that closure. Fable confirmed the finding in A-009; A-010 then withdrew the
proposed remedy after the second diagnostic. The owner-approved termination/
domain decision is still required. No revised design or shared Interface
edit is made by this lane. Checkpoint 0 authorization remains in force.

### Historical producer-release escalation (A-008) — WIRE now accepted

Fable classifies JSON control-character escaping as builder-owned restoration,
not a semantic change. Dev authorized the correction; complete U+0000–U+001F
escaping is installed and all three diagnostic tests pass.

A-008 also escalates P-WIRE: owner approval of wording that releases PARITY.md's
stale producer block after signed H1-H6/Interface approval. It recommends a record
per (household, target, bound-argument tuple) and asks Dev to confirm that counting
unit before corpus freeze. No new schema, record-count unit, contract release or
comparison change has been installed. Checkpoint 0 remains signed off.

### Phase 1 shared observation reproduction (Q-008; classification complete)

The shared `escapeJson` emits literal U+000A in an atom even though the
well-formedness check accepts that nonempty term. A pinned Lean 4.33.1 probe of
`Solution.encode [.atom "line\nbreak"]` produced invalid multiline JSON;
`Household.v1` returned true. Evidence and the exact probe are in Q-008.
A-008 classifies this as restoration of the existing H6.2 JSON requirement,
with byte-stable existing encodings and pinned control-character escape spellings.
The shared encoder now implements that restoration; `Valid`, protected
artifacts and comparison expectations are unchanged. Its separate
producer-release escalation and Q-009's semantic finding remain the reasons
development is paused.

### Checkpoint 0 entry hold — resolved

The meter, checks, retained results and complete protected manifest are
installed; strict verification has zero Checkpoint 0 failures and zero current
outstanding items. Dev independently audited and accepted the meter, then
explicitly signed off Checkpoint 0 and authorized Phase 1. The entry hold is
resolved. No production parity, round-trip or Checkpoint 1 result is yet claimed.

Checkpoint 2 exploits and Checkpoint 3a signed statements remain separately
reported later deliverables, not reasons to block Checkpoint 0. Native baseline
evidence is now retained; the remaining runtime archival obligations remain
visible in RUNTIME.md. No additional semantic decision is inferred or requested.

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

The following is the original scaffold validation record, not the current
validation status. Current interface/runtime results and protected-file checks
are recorded above and in the dated evidence under `docs/contracts/`.

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

Checkpoint 0 remains explicitly signed off. A/WIRE are accepted, not open
choices. Continue only within their installed shared contracts and the remaining
implementation obligations above, with separate oracle/serializer contexts and
read-only human. Protected amendment installation/re-pin is Dev's. Do not claim
R5 termination before actual query/stipulation coverage and adequacy proofs.
Checkpoint 1 still requires zero parity mismatches on all 376 cases, an unchanged
meter hash, owner hazard/mismatch review and explicit owner sign-off before Phase 2.
