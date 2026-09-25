# H6.3 extra-conjunct scope (P-H6-CONJ): install draft

Status: **APPROVED by Dev on 2026-09-25 — NOT INSTALLED.** Dev approved
P-H6-CONJ as proposed in A-024 §3. The approval is recorded in
`docs/DECISION_LOG.md` by the builder at Dev's direction, with "installed"
pending. This draft stages the exact text and patch. Only Dev installs it into
`human/DECISIONS.md` and re-pins. The builder wrote nothing under `human/`.
Approval of the text is not installation, projection acceptance or
Checkpoint 1.

## Origin

H6.3 (`human/DECISIONS.md:893-898`) names only `s152_d_2_D_pos/neg` as cases
with extra conjuncts. H6.5 also flags `s152_d_2_G/4`, `s68_b/3` and
`s3306_c_10_A/4`, and the original directives
`cases/s152_d_2_G_pos.pl:19`, `cases/s68_a_1_pos.pl:17`,
`cases/s68_a_1_neg.pl:17` and `cases/s3306_c_10_A_i_pos.pl:37` carry extra
conjuncts too (A-024 §3; paths under `human/sara/sara/`).

The governor's record is the "2026-09-24 — PROPOSED — P-H6-CONJ" entry in
`docs/DECISION_LOG.md`. Dev's acceptance is the 2026-09-25 entry after it.

## Change: replace H6.3's "The two cases…" sentence (A-024 §3), verbatim

The sentence replaced runs across lines 895-897 of `human/DECISIONS.md` (file
SHA-256 `12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a`):

```text
The two cases with extra conjuncts (`s152_d_2_D_pos/neg`) evaluate the
conjuncts on each observed tuple.
```

The replacement words are A-024 §3's text, byte for byte, with the `> ` quote
markers removed. They are identical to the quote in the DECISION_LOG entry:

```text
For every original case directive with additional conjuncts, evaluate the
additional conjuncts on each matching solution of the queried target,
preserving the original variable sharing, literal order, bindings and
negation scope. The positive test succeeds iff a solution satisfies the
entire conjunction; a negated conjunction succeeds iff none does. This
includes `s152_d_2_D_pos/neg`, `s152_d_2_G_pos`, `s68_a_1_pos/neg`, and
`s3306_c_10_A_i_pos`. Additional conjuncts do not change the target's
output-position tuple or the H6.1/H6.2 observation policy.
```

**Placement inside the H6.3 bullet** is the one formatting choice here. The
words are the approved text:
- Line 895 keeps its first sentence and ends after "passes iff it is not.".
- The eight replacement lines follow, each with H6.3's two-space continuation
  indent.
- "The `tax_case_*` files test `tax/3` with a ground" and "answer." keep their
  words and indent.

The resulting bullet, when installed alone:

```text
* H6.3 (per-case accuracy). A positive case passes iff the expected tuple
  (the ground values of the case goal in output positions, or "non-empty" if
  none) is in the observed set; a negative case passes iff it is not.
  For every original case directive with additional conjuncts, evaluate the
  additional conjuncts on each matching solution of the queried target,
  preserving the original variable sharing, literal order, bindings and
  negation scope. The positive test succeeds iff a solution satisfies the
  entire conjunction; a negated conjunction succeeds iff none does. This
  includes `s152_d_2_D_pos/neg`, `s152_d_2_G_pos`, `s68_a_1_pos/neg`, and
  `s3306_c_10_A_i_pos`. Additional conjuncts do not change the target's
  output-position tuple or the H6.1/H6.2 observation policy.
  The `tax_case_*` files test `tax/3` with a ground
  answer.
```

## Exact patches

- `docs/contracts/H6_CONJ_DRAFT.patch`: this change alone.
- `docs/contracts/G2_H6_INSTALL.patch`: this change plus P-G2-CALLS
  (`docs/contracts/G2_CALLS_DRAFT.md`), as one patch. Dev asked for a single
  install. After it, H6.3 starts at line 908.

On 2026-09-25, each patch passed `git apply --check` against the current
`human/DECISIONS.md`. Applied to a scratch copy (never under `human/`), each
gave exactly the expected digest below.

## Combined install and re-pin (Dev only; this is the requested path)

Run this from the repository root, in Dev's own shell rather than a builder
session, on a branch for a pull request labelled `owner-human-update`:

```sh
git apply docs/contracts/G2_H6_INSTALL.patch
shasum -a 256 human/DECISIONS.md
#   expect bac708d5d2b80614e4f45d92efe0031e7740965684ed0cedc83a3c6e37ecdf23
python3 -B scripts/human_manifest.py generate > human/HASHES.txt
python3 -B scripts/human_manifest.py verify
#   expect: verified: every file under human/ is listed and matches its digest
shasum -a 256 human/HASHES.txt
#   expect 9b342252312ac68cd1f34c7a8c6dd585a42b1ac14460ebcd1e7944749e01babe
```

For reference, if this change is installed alone:
- patch: `H6_CONJ_DRAFT.patch`;
- `DECISIONS.md`: `8e16231259cdcfc20d34e18a48632facda20f739dd9ae07e3cca5ad6fd5977c2`;
- `HASHES.txt`: `f67207124152b0ffa79bfffa6f53925996bbb5b3a163f92adb19e42b8e629416`.

The expected digests assume nothing else under `human/` changes. `generate`
currently reproduces `human/HASHES.txt` byte for byte, and `DECISIONS.md` is
its only record that changes. The re-pin and verify commands are the recorded
ones (`docs/DECISION_LOG.md:271-272`).

## What installation would and would not settle

- **Would:** define scoring for every original with additional conjuncts.
  That covers the six named originals, not only `s152_d_2_D_pos/neg`, while
  keeping variable sharing, literal order, bindings and negation scope.
- **Would not:** change any target's output-position tuple, the H6.1/H6.2
  observation policy, `Valid`, the source or the population. It is not
  projection acceptance, and it does not pass Checkpoint 1.
- **Builder follow-ups after Dev confirms the install:**
  - verify the manifest, and record the new digests in `docs/HANDOFF.md` and
    `STATE.md`;
  - lift the scoring halt;
  - implement conjunct evaluation in the scoring path, with tests for all six
    originals. That is lane and integration work, dispatched per HANDOFF.

## Self-review

- **Provenance:** the eight replacement lines were extracted from
  `docs/consult/A-024.md` and checked byte-identical against the DECISION_LOG
  quote.
- **Measurements:** the line numbers and digests were measured on the current
  tree.
- **Nothing written under `human/`:** the patch results were verified on
  scratch copies.
- **Semantics:** no Prolog semantics are assumed beyond A-024's text.
- **Circuit breaker:** three failed edit cycles on one check means stop and
  report. No edit cycle was needed.
