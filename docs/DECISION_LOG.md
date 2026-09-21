# Decision log

Entries are appended by Fable (design authority). PROPOSED entries are not in
force until Dev accepts them and installs the corresponding text in the owning
artifact. Contract sources: `docs/PLAN.md` §4, `docs/PROTOCOL.md` B001–B004,
`docs/contracts/RUNTIME.md`.

## Consolidation note (2026-09-21)

This is the authoritative log, installed at the documented path. It was
assembled from two divergent copies:

- `human/sara/sara/.claude/worktrees/sara-semantics-interpretation-9ecfee/docs/DECISION_LOG.md`
  — the semantics lane's log, which carries the owner's acceptances. **Every
  entry body below is reproduced from it verbatim.**
- `.claude/worktrees/human-deliverables-474e7d/docs/DECISION_LOG.md` — the
  builder lane's log, carrying two runtime proposals. Its DL-002 (time zone)
  duplicated P-TZ and has been withdrawn as superseded; its DL-001 is carried
  forward below as P-RUNTIME, still pending.

One thing was corrected, and only this: five entries carried the heading status
`PROPOSED` while their own body recorded `accepted by Dev in chat, 2026-09-21
("good to go"); installed in human/DECISIONS.md the same day`. The headings now
read `ACCEPTED`, matching the bodies. **No entry's meaning was altered**, and
nothing was newly accepted by the builder. P-SUMLIST's body says "awaiting Dev"
and its heading still reads PENDING.

## Status index

| Entry | Subject | Status | Installed in the owning artifact? |
| --- | --- | --- | --- |
| P-TZ | `TZ=America/New_York` in the pinned container | **ACCEPTED** | `human/DECISIONS.md`; `docs/contracts/RUNTIME.md` |
| P-MONEY | Money is `Int` whole dollars, not cents | **ACCEPTED** | `human/DECISIONS.md` M1; `docs/PROTOCOL.md`. `docs/PLAN.md` is preserved byte for byte and still says cents; PROTOCOL supersedes it |
| P-STIP | Stipulations, rule grounding, B005 reader exception | **ACCEPTED** | `human/DECISIONS.md` H4; `docs/PROTOCOL.md`. The reader exception still needs a harness contract when the harness exists |
| P-TARGETS | Per-signature targets, solution-set observation | **ACCEPTED** | `human/DECISIONS.md` H6; `docs/PROTOCOL.md`. `Interface/S{N}.lean` not written |
| P-VALID-YEAR | `Valid : Household → Year → Prop` | **ACCEPTED** | `human/DECISIONS.md` H5; `docs/PROTOCOL.md`, including the corrected B004 example; `Interface/Household.lean` |
| P-INTENT | Fidelity rule | **ACCEPTED** | `human/DECISIONS.md` G9; `docs/PROTOCOL.md` |
| P-SUMLIST | Schema heading `findall/sum_list`, not `sumlist` | **PENDING** | — |
| P-RUNTIME | Debian's `7.2.3+dfsg-6` build, emulation, image distribution | **PENDING** | —; `docs/contracts/RUNTIME.md` remains operative as written |

`INSTALLED` entries record an action taken, not a proposal.

## 2026-09-21 — ACCEPTED (Dev, chat) — P-TZ: pin the interpreter time zone

Origin: A-004 / `DECISIONS_RECOMMENDED.md` D8, F1.
Change: add to `docs/contracts/RUNTIME.md` (and the Phase 1 harness) the
requirement `TZ=America/New_York` inside the pinned container, recorded with
the image digest. Reason: `format_time/3` renders UTC stamps in local time;
the reference program reproduces all 376 SARA labels only under that zone
(two cases fail under UTC, Europe/Amsterdam, Asia/Tokyo). The setting changes
the meaning of §7703(b)(3) and of the week counts in §3306(a)(1)(B),
(a)(2)(B). Status: accepted by Dev in chat, 2026-09-21 ("good to go"); installed in `human/DECISIONS.md` the same day (see INSTALLED entry).

## 2026-09-21 — ACCEPTED (Dev, chat) — P-MONEY: money as Int dollars

Origin: A-004 / M1. Conflicts with PLAN Checkpoint 0 ("Money as Int cents").
Change: `Interface/` money type is `Int` whole dollars. Reason: every source
amount is an integer dollar; every output is rounded to whole dollars; cents
would require `Valid` to demand multiples of 100 and give models a unit the
reference never uses. The cents-preserving variant is written out in M1 if
Dev keeps the plan. Status: accepted by Dev in chat, 2026-09-21 ("good to go"); installed in `human/DECISIONS.md` the same day (see INSTALLED entry).

## 2026-09-21 — ACCEPTED (Dev, chat) — P-STIP: stipulations and grounding (resolves B005)

Origin: A-004 / H4. Change: `Household` gains a `stipulations` list; case
rules are grounded by enumeration in the pinned interpreter; round-trip
identity is defined on the grounded lists and on solution sets; the two
unterminated `s3306_c_2` files are read with the terminator restored as a
documented reader exception. Reason: 156 of 376 cases stipulate statute
predicates, 59 define facts by rules; a facts-only contract cannot represent
them and the plan's "round-trip identity on all 376 cases" is otherwise
undefined. Status: accepted by Dev in chat, 2026-09-21 ("good to go"); installed in `human/DECISIONS.md` the same day (see INSTALLED entry).

## 2026-09-21 — ACCEPTED (Dev, chat) — P-TARGETS: paragraph targets and set observation

Origin: A-004 / H6. Conflicts with PLAN Phase 2.3 (one target signature per
section) and refines Phase 3.5/4.3 (per-case accuracy). Change:
`Interface/S{N}.lean` declares one target per queried predicate signature
plus one entry point per section; the observation of a target is the sorted,
deduplicated solution set; scalar entry points are first solutions; per-case
accuracy for models is computed on the stipulation-independent subset of the
originals; Alternative A (environment-passing targets) is recorded for the
case where that subset is too small. Reason: 135 signatures are queried by
the cases; existential directive semantics; stipulations must not leak into
graded inputs. Status: accepted by Dev in chat, 2026-09-21 ("good to go"); installed in `human/DECISIONS.md` the same day (see INSTALLED entry).

## 2026-09-21 — ACCEPTED (Dev, chat) — P-VALID-YEAR: `Valid` is year-indexed

Origin: A-004 / H5 V8. Refines PROTOCOL B004's statement form
`∀ h y, Valid h → …` to `∀ h y, Valid h y → …`. Reason: one
reference-undefined region (the head-of-household recursion through a
supported parent) depends on the taxable year (2018–2025 escape it); a
year-free exclusion would remove every §2(b)(1)(B) input. `Valid` may import
`Oracle/` for V7/V8. Status: accepted by Dev in chat, 2026-09-21 ("good to go"); installed in `human/DECISIONS.md` the same day (see INSTALLED entry).

## 2026-09-21 — PENDING — P-SUMLIST: schema heading names `sum_list`

Origin: A-004 / F14. Change: the DECISIONS.md schema line "every
findall/sumlist" reads "every findall/sum_list". Reason: the source contains
12 `sum_list/2` sites and no `sumlist`. No semantic effect. Status: awaiting
Dev.

## 2026-09-21 — ACCEPTED (Dev, chat) — P-INTENT: fidelity rule

Dev's directive: "stay faithful to what SARA authors intended." Operational
form, recorded so Astra applies it uniformly:

1. Where the *runtime, reader or observation* is under our control, choose
   the option that reproduces the authors' own results: `TZ=America/New_York`
   (P-TZ), the restored terminator in the two `s3306_c_2` files (P-STIP,
   H4.4), the existential (solution-set) observation that the case directives
   assume (P-TARGETS), the stipulation-independent subset for per-case
   accuracy.
2. Where the *statute code* itself diverges from its evident intent (F10
   unbound surviving spouse in `s68_b_1_A`, F11 `s2_b_3_A` start+end, F16
   duplicated disjunct in `s152_c_3`, F17 `Count2 is 600` in `s63_f_2`, F18
   `end_` required in `s3306_b`, F4 unbound `Workday`), the oracle translates
   the code as written. Reason: the parity meter compares against the pinned
   program on the unmodified `human/sara`, and an oracle that "corrects" the
   source cannot reach zero mismatches; the divergences are reported as
   findings in the paper. If Dev wants the intended readings graded instead,
   that is a separate contract change (a corrected Prolog copy as the parity
   reference, as Phase 4.1 already does for counterfactuals) and must be
   proposed, not applied silently.
3. Interpretive latitude that neither the code nor the labels settle is
   resolved toward the reading the 376 labels support, and the choice is
   written down at the site.

## 2026-09-21 — INSTALLED — `human/DECISIONS.md` written by Fable

Dev's explicit one-time authorization in chat ("just this once I let you
update DECISIONS.md") overrides the standing rule that Fable never writes
under `human/`. The file now carries the accepted decisions under the schema
headings (Conventions, Money, Dates, Household, NAF, Cut, Aggregates,
Recursion, Axioms, Source hazard inventory, Verification record), generated
from `docs/consult/DECISIONS_RECOMMENDED.md` without semantic change. The
one-time exception does not extend to any other file under `human/` or to
later edits of this one. Consequences for Dev: re-pin `human/HASHES.txt`
after review; the RUNTIME time-zone requirement (P-TZ) and the reader
exception for the two `s3306_c_2` files (P-STIP) still need their own
installation in the owning contracts; the change is uncommitted in the main
checkout.


## 2026-09-21 — PENDING — P-RUNTIME: how the pinned 7.2.3 interpreter is obtained

Origin: the builder lane's DL-001, carried forward unresolved. Contract
affected: `docs/PROTOCOL.md` B001 ("Pin SWI-Prolog 7.2.3 in Docker on
`linux/amd64`. Record an immutable image digest") and
`docs/contracts/RUNTIME.md` ("a Docker image for `linux/amd64` containing
exactly that interpreter"; "Do not fall back to a host interpreter or a newer
image when the pin is unavailable").

**No acceptance of a deviation is recorded anywhere, so the existing runtime
contract remains operative as written.** This entry states the problem and the
options; it does not resolve them.

Evidence.

- The official Docker `library/swipl` repository has 123 tags and the oldest is
  7.5.11 (2017-08-10); there is no 7.0.x–7.4.x tag. Verified against the Docker
  Hub tag API.
- Debian stretch ships `swi-prolog 7.2.3+dfsg-6`, still served by
  `archive.debian.org`. An image built from it reports, from inside the
  container, `SWI-Prolog version 7.2.3 for amd64`, `PLARCH=amd64`. See
  `harness/Dockerfile`, `harness/pin_runtime.sh`, `docs/contracts/RUNTIME.json`.
- The upstream 7.2.3 source tarball also remains available; a from-source build
  has not been attempted.

Why it is a contract change: `+dfsg-6` is Debian's repackaging with six
revisions of Debian patches. It reports itself as 7.2.3 and is the build Debian
shipped, but it is not byte-for-byte upstream's 7.2.3, and B001 says "exactly
that interpreter".

**A point the owner should see before deciding.** `human/DECISIONS.md` opens by
recording that *every interpreter claim in it* was checked on
`kmla-swipl:7.2.3` — that is, on the Debian build this entry is about. The
accepted decisions therefore already rest on this interpreter. Either the
deviation is accepted, or the interpreter-dependent claims in the accepted
decisions need re-deriving on whatever build is chosen instead. This is a
provenance question about the evidence base, not a defect in the decisions.

Options: (A) accept Debian `7.2.3+dfsg-6` and amend B001 to name it;
(B) build 7.2.3 from the upstream tarball and pin that; (C) amend B001 to a
newer interpreter; (D) vendor the `.deb` so the build does not depend on
`archive.debian.org` remaining reachable.

Two further points settle either way: whether amd64 under emulation on an
arm64 host satisfies the reproducibility claim (`debian:stretch` also publishes
an arm64 manifest), and where the image is published so a digest can pin it —
a locally built image's ID is not reproducible across builds, so the
reproducible identity today is the triple (base image digest, Debian package
version, Dockerfile SHA-256), all recorded in `docs/contracts/RUNTIME.json`.

## 2026-09-21 — WITHDRAWN — DL-002: pin the interpreter time zone

Superseded by P-TZ, which covers the same change and is accepted. The builder
lane raised it independently, measured the same effect (376/376 cases agree
with their labels under `America/New_York`; 374/376 under `UTC` or
`Asia/Tokyo`, the two failures being `s3306_a_1_B_neg` and `s3306_a_2_B_neg`),
and reached the same conclusion. Recorded here so the corroboration is not
lost and so no one looks for a second, still-open time-zone decision. The
measurement is in `docs/contracts/RUNTIME_OBSERVATIONS.md` O-5 and O-6 and the
per-case baselines in `docs/contracts/CORPUS_BASELINE_*.json`.
