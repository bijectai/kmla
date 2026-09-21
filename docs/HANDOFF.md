# Phase 0 handoff

The approved B001–B004 amendments are in `docs/PROTOCOL.md`. The source is
installed and verified. Phase 0.1 drafts are staged under `docs/contracts/`;
the human promotes and pins them. The assistant never writes under `human/`.

## Verified source

The existing `human/sara/SARA.tar.gz` matches a fresh download from the lowercase
archive link on the JHU SARA page. SHA-256:

```text
e4f1b845016fc38b95b702bbbb27a5c9af3eadfa856ba585662b8b2cd71c187c
```

The actual corpus root is `human/sara/sara/`, with `statutes/source/`,
`statutes/prolog/`, and `cases/`. All 400 payload files match the archive.
The 376 case programs comprise 276 section cases and 100 numerical tax cases;
train/test splits contain 256/120 disjoint IDs covering all cases.
See `docs/contracts/SOURCE.md` and `SOURCE_AUDIT.json` for archive metadata.

The tarball hash is staged in `docs/contracts/HASHES.txt`. This does not update
`human/HASHES.txt` or establish a complete pin; the human performs that step.

## Human deliverables for Checkpoint 0

Source review found a new blocker: `s3306_c_2_neg.pl` and `s3306_c_2_pos.pl`
lack the period at line 26 before their `% Test` comment. Under ordinary clause
syntax the apparent test continues a rule, leaving only 374 standalone test
directives across 376 files. Cases also contain 108 non-ground bodyless clauses
and 434 rules. Resolve their treatment and the meaning of round-trip identity
explicitly in the decisions; no repairs or facts-only filtering are assumed.
`docs/contracts/HOUSEHOLD.md` contains the evidence. Semantic finalization is
paused under the design-flaw stop-and-report standard.

1. Complete `docs/contracts/DECISIONS.md`, including every source-located hazard.
   Resolve Money, Dates, Household, NAF, Cut, Aggregates, Recursion, Axioms,
   arithmetic, and builtin behavior. Install the decisions in `human/DECISIONS.md`.
2. Review `Interface/Household.lean` and `docs/contracts/HOUSEHOLD.md`. Approve
   or correct the semantic interface in your decisions. A source-syntax draft
   does not settle defaults, groundness, rule handling, units, or query/result
   projections. Finalize section input and output payloads before implementation.
3. Independently implement `human/parity/check.py` to `docs/contracts/PARITY.md`.
   Its CLI retains `--section`, `--inputs`, `--prolog-out`, and `--lean-out`.
   Exit 0 means complete agreement; exit 1 writes `mismatches.jsonl` records
   containing `input_id`, `prolog`, and `lean`. Exit 2 reports an invalid or
   unimplemented comparison. The staged stub always exits 2. The assistant
   must not read the real meter's source.
4. Review the staged `gate/exploits/README.md` and
   `invariants/statements/README.md` conventions for later human-authored
   artifacts. Invariants use `def ... : Prop`, with separate proofs.
5. Configure the human-owned submodule, preserving the source and your work.
   Supply its repository and pinned commit. Complete `human/HASHES.txt` using
   `docs/contracts/HASHES.md`, including the tarball pin. The source-only draft
   is incomplete. The reviewed submodule commit pins the manifest itself.

Earlier layout placeholders under `human/` remain untouched. The human decides
which ones to replace when promoting reviewed drafts from `docs/contracts/`.

## Conditions before Phase 1

Do not translate clauses or implement serializers before Checkpoint 0 passes.
Establish the actual read-only mount, hash verification, and protected submodule
policy before separate development lanes start.

Oracle translation and generator/serializer development use separate contexts,
sharing only `DECISIONS.md` and `Interface/` as their semantic contract and
accessing the designated source as required. Neither may see the other's code.

Pin SWI-Prolog 7.2.3 on `linux/amd64` in Docker and record its verified immutable
image digest before harness evaluation. See `docs/contracts/RUNTIME.md`.
The runtime has not yet been built or executed.

## Confirmed later-phase rules

Admission witnesses stay in `mutate/witnesses/`, separate from the frozen and
hashed `gen/out/`. No witness means `UNRESOLVED`, excluded from kill rates.
New input modes produce a separately frozen v2, evaluated on the same admitted
mutants; report both rates. Never merge admission witnesses into the corpus.

Invariant `REFUTED` requires a kernel-checked negation with a concrete witness.
Failed proof search is `PARTIAL`; checked refutations take precedence.

On a design flaw, halt affected work, record evidence and the needed decision in
`STATE.md`, and report it before changing the design. Later human checkpoints
remain mandatory. No PR may be merged by the assistant.
