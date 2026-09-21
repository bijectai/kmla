# KMLA state

## Current phase

2026-09-20: Phase 0.1 drafts prepared after the user's B001–B004 clarifications.
Semantic/interface finalization is paused on the source findings below.
No gate has passed. Translation and evaluation remain gated on Checkpoint 0.

## Completed

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

## Blockers

### B005: Case-program semantics and two missing clause terminators

The original `s3306_c_2_neg.pl` and `s3306_c_2_pos.pl` each lack a full stop at
line 26, before `% Test` at line 28. The `:-` at line 29 thus continues the
preceding clause under ordinary Prolog syntax. The lexical inventory finds 376
case files but only 374 standalone test directives. No source was repaired or
case excluded; runtime behavior has not been established with pinned Prolog.

In addition, the cases contain 108 variable-bearing bodyless clauses and 434
local rules. A facts-only ingestion contract cannot silently erase or ground
these. The owner must specify clause/test interpretation, rule and variable
handling, and the intended meaning of round-trip identity in DECISIONS.
See `docs/contracts/HOUSEHOLD.md` for source citations and exact inventory scope.

Affected semantic/interface work is halted under the approved design-flaw
stop-and-report standard. The existing syntax draft explicitly marks rules and
directives unsupported rather than pretending they are validated household data.

### Checkpoint 0: Independent decisions and meter

The owner must complete and install the semantic decisions, approve the shared
interface and section observation schemas, and independently implement parity.
Unresolved source semantics remain TODO, not inferred defaults.

### Checkpoint 0: Protected-artifact enforcement

`human/` is not a configured submodule or enforced read-only mount. Its full
hash manifest is not pinned. The owner must promote approved artifacts, finish
the manifest, and supply a reviewed submodule commit; runner/CI enforcement is
required before the development lanes start.

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

Phase 0.1 drafts are ready for review in `docs/HANDOFF.md`. The owner must
resolve B005 alongside the remaining semantic decisions. Subsequent
implementation begins only after Checkpoint 0 passes.
