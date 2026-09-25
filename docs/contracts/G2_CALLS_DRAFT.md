# G2 call-entry census (P-G2-CALLS): install candidate

Status: **CANDIDATE ONLY — not approved, not installed.** Staged at Dev's
direction on 2026-09-25 so that Dev can decide and, if approving, install it
without drafting. It contains:
- A-025 §2's proposed P-G2-CALLS clarification, verbatim;
- A-025 §5's editorial citation fix;
- the exact patch, re-pin and verify commands.

Only Dev approves, amends, installs into `human/DECISIONS.md` and re-pins. The
builder wrote nothing under `human/`. Staging this draft approves nothing: not
the ENTRY policy, not any projection row, not Checkpoint 1.

## Origin

G2 (`human/DECISIONS.md:33-40`) does not choose which call sites count once a
path has unavoidably failed or raised. Q-025 submitted a derivation under two
readings, S (syntactic continuation) and L (live path). A-025 did not approve
either column. It separated three policies (S, ENTRY and defined-domain-only),
selected none, and proposed the ENTRY census below as a candidate.

The governor's record is the "2026-09-25 — PROPOSED — P-G2-CALLS" entry in
`docs/DECISION_LOG.md`, with its Status index row. The evidence is in
`docs/consult/evidence/q025-g2-derivation/` and the blocker in `STATE.md` →
Blockers. P-H6-CONJ (A-024) and the G6 finding (R-Q025) are separate decisions
and are not in this draft.

## Change 1: editorial citation fix (A-025 §5)

This is `human/DECISIONS.md` line 40, file SHA-256
`12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a`. It is
the only occurrence of `(R3)` in the file.

| | Line 40 |
| --- | --- |
| Before | `(R3).` |
| After | `(R4).` |

The line ends G2's sentence "the both-unbound `s152` call is the empty list".
R3 (line 1390) is `amount/2`; the rule meant is R4, `s152/3 ↔ s152_b_1/3`
(lines 1394-1401). The substance of G2 is unchanged.

## Change 2: the P-G2-CALLS clarification (A-025 §2), verbatim

**Insertion point:** a new paragraph immediately after G2, that is after line 40
(`(R4).` once change 1 is applied) and before the blank line that precedes G3
(`**G3 (...)`, currently line 42). After both changes, the clarification
occupies lines 42-55, with blank lines at 41 and 56, and G3 starts at line 57.
The text is copied byte for byte from `docs/consult/A-025.md` §2, with the
`> ` quote markers removed, and is identical to the quote in the DECISION_LOG
entry:

```text
For the H6.5 case-mode declaration, count statute and case-test call entries
reachable by a finite prefix of the G1-ordered evaluation from the listed
root modes. The census covers stipulation-free, well-formed H1–H3 households
in those modes and each original case with its own facts and H4 stipulations;
do not pool unrelated case stipulations. Do not prune this census using
G6/V-rule exclusions. An entered goal counts even if it fails, raises, or
belongs to an evaluation that later raises or diverges. A successor requiring
a return that cannot occur does not count. Binding at a successor is derived
from the successful returns that can actually reach it, including stipulated
rule bodies, not head-variable spelling or vacuous success implications.
Keep H6.5's bound-answer rule. This census does not certify binding claims
for arbitrary additional wildcard stipulations or discharge any theorem
quantified over all `ValidStip`; those obligations remain open. No validity,
source, observation, or corpus-population change follows from this census.
```

Dev may add a label or rewrap it. Any change to the bytes changes the expected
digests below.

## Exact patch

The patch is also staged as `docs/contracts/G2_CALLS_DRAFT.patch`, with
identical bytes. `git apply --check docs/contracts/G2_CALLS_DRAFT.patch`
passed against the current `human/DECISIONS.md` on 2026-09-25. That was a
check only; nothing was written.

```diff
--- a/human/DECISIONS.md
+++ b/human/DECISIONS.md
@@ -37,7 +37,22 @@
 Lean function per mode, named `p_mode`, with the mode string recorded in the
 section table (H6). Instantiation guards (`nonvar/1`, `var/1`) are resolved at
 translation time by the mode; the both-unbound `s152` call is the empty list
-(R3).
+(R4).
+
+For the H6.5 case-mode declaration, count statute and case-test call entries
+reachable by a finite prefix of the G1-ordered evaluation from the listed
+root modes. The census covers stipulation-free, well-formed H1–H3 households
+in those modes and each original case with its own facts and H4 stipulations;
+do not pool unrelated case stipulations. Do not prune this census using
+G6/V-rule exclusions. An entered goal counts even if it fails, raises, or
+belongs to an evaluation that later raises or diverges. A successor requiring
+a return that cannot occur does not count. Binding at a successor is derived
+from the successful returns that can actually reach it, including stipulated
+rule bodies, not head-variable spelling or vacuous success implications.
+Keep H6.5's bound-answer rule. This census does not certify binding claims
+for arbitrary additional wildcard stipulations or discharge any theorem
+quantified over all `ValidStip`; those obligations remain open. No validity,
+source, observation, or corpus-population change follows from this census.
 
 **G3 (`=`, `==`, `\==`).** `=` with one side unbound is a binding; with both
 bound it is structural equality on `Term`. `==`/`\==` on bound terms is
```

## Install and re-pin (Dev only)

Run this from the repository root, in Dev's own shell rather than a builder
session: the project settings deny builder edits under `human/`, and owner
installation is never delegated. Use a branch for the owner-labelled PR.

```sh
git apply docs/contracts/G2_CALLS_DRAFT.patch
shasum -a 256 human/DECISIONS.md
#   expect bc94996b75102acb0ceaf27192f526b87860f4c573ce30fbd4f9879b93556ea5
python3 -B scripts/human_manifest.py generate > human/HASHES.txt
python3 -B scripts/human_manifest.py verify
#   expect: verified: every file under human/ is listed and matches its digest
shasum -a 256 human/HASHES.txt
#   expect bf9ee0e2c00f309f8adb87ec3e6e2e2377a98cec6596e00a26e0b7e3b3d76179
```

The re-pin and verify commands are the recorded ones from
`docs/DECISION_LOG.md:271-272` and the `docs/contracts/HASHES.txt` header.

**Where the expected digests come from.** On 2026-09-25, `generate` reproduced
the current `human/HASHES.txt` byte for byte, and `DECISIONS.md` is its only
record that changes. The expected digests were computed in memory from the
patched text. They hold only if these two changes are the only change under
`human/`. For example, installing P-H6-CONJ in the same pass changes both.

**CI.** A pull request touching `human/` needs the `owner-human-update` label
(`.github/workflows/verify.yml`, job "human/ is read-only to the assistant").
The manifest verification job runs regardless.

## What approval would and would not settle

- **Would:** fix the census that decides which call sites count for the H6.5
  case-mode output declaration. That census is ENTRY: count entered calls,
  including ones that later fail or raise; drop successors that cannot be
  reached; take bindings from the successful returns that reach a call.
- **Next for the builder:** re-derive the affected rows under ENTRY. Neither
  the S nor the L column of the Q-025 evidence is ENTRY. The re-derived
  declaration still goes for review before anything is written to
  `Interface/`.
- **Would not:** change `Valid`/`ValidStip`, the source, observations or the
  corpus population; certify binding claims for additional wildcard
  stipulations or discharge any `ValidStip` theorem; decide P-H6-CONJ or the
  G6 finding; sign Checkpoint 1.
- **Alternatives (A-025 §2):**
  - S: syntactic continuation, which also needs an explicit binding rule for
    successors of goals that cannot return;
  - defined-domain-only: this needs a proved domain analysis and changes more
    rows, including those Q-025 §2(a) lists.

  Either choice needs a different draft.
- **Builder follow-ups after an install:**
  - record the new `DECISIONS.md` and `HASHES.txt` digests in `docs/HANDOFF.md`
    and `STATE.md`;
  - change the P-G2-CALLS log status only when Dev directs it, since the
    governor maintains that log.

## Self-review

- **Provenance:** the clarification's 14 lines were extracted from
  `docs/consult/A-025.md` and checked byte-identical against the DECISION_LOG
  quote.
- **Measurements:** the line numbers, the single `(R3)` occurrence, the current
  digests and the patch check were all measured on the current tree.
- **Nothing written under `human/`:** the new digests were computed in memory,
  not by applying the patch.
- **Semantics:** no Prolog semantics are assumed beyond A-025's own text.
- **Circuit breaker:** three failed edit cycles on one check means stop and
  report. No edit cycle was needed.
