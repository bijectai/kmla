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
| P-SUMLIST | Schema heading `findall/sum_list`, not `sumlist` | **ACCEPTED** | Builder installing in `docs/PROTOCOL.md`; `docs/PLAN.md` §4.1 is preserved byte for byte and still reads `sumlist` |
| P-RUNTIME | Debian's `swi-prolog-nox 7.2.3+dfsg-6`; identity is the `RUNTIME.json` record; native-amd64 CI baseline; three-leg archival | **ACCEPTED** | One acceptance, two artifacts: builder installing in `docs/PROTOCOL.md` B001 **and** `docs/contracts/RUNTIME.md`. Acceptance is not evidence that vendoring, GHCR publication, archival deposit or native CI has happened |
| P-PARITY5 | The five parity policies: directory contents, non-regular entries, three-valued report, IDs, aliasing | **ACCEPTED** | Builder installing in `docs/contracts/PARITY.md`. One omission flagged in A-007 §3 blocks fully mechanical installation of policy 1 |
| P-BUNDLE | `human/` stays a directory in the parent repo; no submodule | **ACCEPTED** | `docs/PROTOCOL.md`, `docs/HANDOFF.md`, `STATE.md` |

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

## 2026-09-21 — SUPERSEDED — P-SUMLIST: schema heading names `sum_list`

**Historical.** This is the proposal as written while it was pending. It is
superseded by the acceptance entry `P-SUMLIST (accepted)` below. The body is
preserved verbatim, including its "Status: awaiting Dev", which is now stale.

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


## 2026-09-21 — SUPERSEDED — P-RUNTIME: how the pinned 7.2.3 interpreter is obtained

**Historical.** This is the proposal as written while it was pending. It is
superseded by the acceptance entry `P-RUNTIME (accepted)` below, which resolves
it as option (A) plus (D). The body is preserved verbatim, including its bolded
"the existing runtime contract remains operative as written" and its
"reproducible identity today is the triple", both of which the acceptance
replaces. Read the acceptance entry for what is in force.

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

---

## 2026-09-21 — ACCEPTED (Dev, chat) — P-BUNDLE: no submodule; `human/` stays in the parent repository

Supersedes `docs/PLAN.md` §2's "`sara/`, `parity/`, `gate/exploits/`,
`invariants/statements/`, `DECISIONS.md` are in a `human/` git submodule".

**Decision.** KMLA is to be open-sourced as a single repository. `human/` remains
an ordinary tracked directory in `bijectai/kmla`. No second repository is
created and no gitlink pin is taken. Dev's reasoning, in chat: the builder is not
expected to alter `human/` unless directed.

**What the submodule was for, and what replaces it.** It was never about
secrecy — public or private was always orthogonal. `docs/PLAN.md` §2 wanted two
things:

1. *Astra cannot merge a PR that touches `human/`.* Replaced by
   `.github/workflows/verify.yml`, which fails any pull request whose diff
   touches `human/` unless the owner labels it `owner-human-update`.
2. *`human/HASHES.txt` pins every file; CI fails on any drift.* Unchanged and
   already in force: the manifest covers all 408 protected files and
   `python3 -B scripts/human_manifest.py verify` is a CI step.

**What is genuinely given up, recorded so no one discovers it later.**

- A pull request can now carry `human/` edits in its own diff, so the protection
  is *detection* rather than *impossibility*. A `pull_request` workflow runs the
  version of itself from the PR branch, so one commit could weaken `verify.yml`
  and edit `human/` together. Branch protection with CODEOWNERS on `/human/`, or
  a repository ruleset, would close this; Dev declined both as unnecessary.
- There is no single gitlink commit id to quote as "the reviewed bundle". The
  substitute identifier is the parent commit plus the manifest, i.e.
  `bijectai/kmla@<sha>:human/` together with the 408 digests in
  `human/HASHES.txt`, which is sufficient for reproduction and for the paper.

**Consequence for Checkpoint 0.** Deliverable 5 no longer requires a repository
URL or a submodule pin. What remains of it is the manifest, which must be
regenerated once `human/parity/check.py` exists so that it covers the meter:

```sh
python3 -B scripts/human_manifest.py generate > human/HASHES.txt
python3 -B scripts/human_manifest.py verify
```

`scripts/make_human_submodule.sh` is retained, tested and unused. If this
decision is ever reversed it performs the migration; it is not part of the
current path.

---

The three entries below record Dev's owner decision of 2026-09-21, staged
verbatim at `docs/contracts/OWNER_DECISIONS_2026-09-21.txt`. That text is the
governing wording; these entries index it and record consequences. It supersedes
conflicting earlier statements, including in `docs/consult/FABLE_PROMPT.md`.
None of the three is reopened here.

## 2026-09-21 — ACCEPTED (Dev, owner decision text) — P-SUMLIST (accepted): schema heading names `sum_list`

Supersedes the PENDING P-SUMLIST proposal above. Dev: "accepted. The source has
twelve `sum_list/2` sites and no `sumlist`. Correct the schema heading. No
semantic effect."

Owning artifacts: the DECISIONS.md schema line in `docs/PROTOCOL.md`.
`docs/PLAN.md` §4.1 is preserved byte for byte and still reads
"every `findall/sumlist`"; PROTOCOL supersedes it, as it does for P-MONEY.
No change to `human/DECISIONS.md` content follows from this, only to the schema
wording that names the heading.

## 2026-09-21 — ACCEPTED (Dev, owner decision text) — P-RUNTIME (accepted): Debian `swi-prolog-nox 7.2.3+dfsg-6`

Supersedes the PENDING P-RUNTIME proposal above, resolving it as option (A) with
(D). **One acceptance, two owning artifacts:** `docs/PROTOCOL.md` B001 and
`docs/contracts/RUNTIME.md` carry parallel text and are amended in this single
entry. The status index no longer says RUNTIME.md "remains operative as written";
it is not.

**The pin.** Debian's `swi-prolog-nox 7.2.3+dfsg-6`, built on the already-pinned
`debian:stretch`.

**Why B001's "exactly that interpreter" is replaced, in Dev's own terms.** It was
never satisfiable: no published image carries 7.2.3, `+dfsg` is a deletion of
upstream files for licensing, `-nox` is a further narrowing, and a self-built
tarball would carry Dev's own patches. Every available option deviates. B001 is
being made achievable, not lowered to meet this build.

**Why not build upstream.** Not a toolchain argument — a 2015 tree would build
inside the same contemporaneous `debian:stretch` (gcc 6.3, glibc 2.24). Rejected
on path dependence: it invalidates every interpreter claim in the already-accepted
`human/DECISIONS.md`. And on patch provenance: Debian's patches are third-party,
contemporaneous, reviewed, and citable by one version string, whereas patches
written here would be novel, unreviewed, and authored by the party whose results
depend on them. Both are recorded; that is not the distinction.

**The empirical claim, with its control.** The pinned interpreter reproduces all
376 directive outcomes, of which 2 execute no test and pass vacuously. The same
corpus on swipl 9.2.9 gives 312 clean and 64 errors, every one an `rdiv/2` type
error. The pin is therefore load-bearing — the corpus discriminates interpreter
version in 64 cases, against the 2 that distinguish time zone — and this
independently confirms the `rdiv` coercion behaviour recorded as O-7. Record it
as `CONTROL_swipl9.json`.

**Identity is the record, not a triple.** The runtime identity is the whole
`RUNTIME.json` record except `local_image_id`: base image digest, Dockerfile
SHA-256, the full installed package closure, and `TZ`. `TZ` is a build argument
with no default, so two images with identical Dockerfile hashes can differ on 2
of 376 cases, and P-TZ already makes `TZ` part of the artifact. Defining identity
by the record means future additions do not re-amend the contract.

**Emulation.** No native-only rule is adopted: every number obtained so far was
produced under emulation, and asserting the rule while relying on that evidence
would retroactively demote the whole base. Instead, run `run_corpus.sh` in CI on
`ubuntu-latest`, which is native amd64, and treat that as the recorded baseline.
The residual emulation risks are named so the rule is not ritual: timeouts (two
cases already needed a longer limit) and x87 long-double paths. Integer and GMP
arithmetic are exact and SSE2 doubles are faithfully translated, so `format_time`
and `%W` cannot differ. Record the translator in `RUNTIME.json`, not a boolean.

**Archival, three legs, because they fail differently.** (1) GHCR pins the output
and gives B001 its immutable digest, but only permits re-download. (2) Vendor the
`.deb` **and its dependency closure** — vendoring `swi-prolog-nox` alone still
needs `debian:stretch` from Docker Hub and the single point of failure survives.
(3) `docker save` the image, record its SHA-256, and deposit it with the paper
somewhere that outlives both registries. Vendoring changes the Dockerfile hash
and therefore forces a re-record and a re-sweep; retain both `RUNTIME.json`
values so existing claims stay traceable. Add the Debian redistribution
obligation to `NOTICE.md`.

**What this acceptance is not evidence of.** Vendoring, GHCR publication,
archival deposit and native-amd64 CI are accepted as obligations, not reported as
done. None has happened. `CONTROL_swipl9.json` is likewise required, not
recorded.

**One correction Dev will make to `human/DECISIONS.md`.** Its preamble says the
image "ignores command-line arguments under emulation". That was a misdiagnosis
of `ENTRYPOINT ["swipl"]`: the command expanded to `swipl swipl …` and SWI took
the first as a script file. argv has since been verified to work normally under
the same emulation and the image switched to `CMD`. Nothing downstream changes —
stdin remains fine — but the stated reason is wrong. Dev makes this edit; the
one-time authorization recorded in the INSTALLED entry above does not extend to
it.

## 2026-09-21 — ACCEPTED (Dev, owner decision text) — P-PARITY5: the five parity policies

Owning artifact: `docs/contracts/PARITY.md`. Dev's framing: where these restate
PARITY.md, that is said so, so nobody later reads drift between policy and
contract as an amendment. These close items 8, 9, 10, 13 and 14 of the fourteen
`--list-gaps` questions classified in A-005/A-006.

1. **Directory contents.** Ignore a dot-prefixed entry **only** when its name does
   not end in `.json`. Every `*.json` entry, dotted or not, joins the population
   and is judged by the ID grammar: `.s151_a` fails
   `[A-Za-z0-9][A-Za-z0-9_-]*` and is exit 2. This closes the hole where
   `.s151_a.json` fell through both rules and silently shrank the population,
   which PARITY.md forbids. **Dot-prefixed directories are covered by this
   policy, not by policy 2.** Astra keeps engine logs and sidecars outside the
   three directories.
2. **Non-regular entries.** Any entry in the three directories that is not a
   regular file is exit 2 — directories (including one named `s151_a.json`),
   symlinks, FIFOs, device nodes. Wrap the whole run so an unexpected exception
   re-exits 2; an uncaught Python exception exits 1, the code reserved for
   "mismatches found".
3. **The report is three-valued, matching the three exit codes.** Exit 0: write a
   zero-byte `mismatches.jsonl` **after** the comparison completes. Exit 1: write
   the records after it completes. Exit 2: create and modify nothing. So absent =
   infrastructure failure, present-and-empty = success, present-and-non-empty =
   mismatches. Never truncate before doing work — that forges the success
   artifact on any crash, and PARITY.md says exit 2 is never zero mismatches.
   UTF-8, LF, one object per line, trailing newline after the final record,
   `ensure_ascii` off, fixed key order `input_id`, `prolog`, `lean`.
4. **IDs.** Case-sensitive comparison, the ID grammar, and duplicate IDs/keys
   restate PARITY.md. Two additions and one correction:
   - Exit 2 when a record's filename stem and `input_id` differ, by byte
     equality, applied to every record in all three directories. This is
     PARITY.md's existing rule, which Dev's earlier draft dropped.
   - "The same ID appears more than once" was vacuous: byte-identical stems
     cannot coexist in one directory. What PARITY.md requires is duplicate keys
     *inside* a record — parse with `object_pairs_hook` and reject; the stdlib
     default silently keeps the last.
   - Case-sensitivity, corrected. The same-directory case rule is **not** a
     defence against case-insensitive storage and must not be read as one. Where
     the filesystem folds case the two files never coexist: the later write
     replaces the earlier, the population silently shrinks by one, and a
     same-directory scan has nothing to reject. Filesystem case-sensitivity is not
     implied by the OS or the platform pin, and no mount of the eventual runner
     has been tested, so assume nothing either way (A-006). The meter's only catch
     is the residue — a collapsed pair leaves one file whose stem and `input_id`
     differ in case, which the stem check rejects. A partial catch, not a
     guarantee. Preventing the collapse is the producer's obligation.

   Because this narrows the published ID space behind a hash freeze, land it in
   PARITY.md's grammar **before Checkpoint 1**: IDs within a section are unique
   under ASCII case folding, and `gen/` mints lowercase-only stems so the rule is
   never exercised.
5. **Aliasing — compare identity, not strings.** Exit 2 if any two of
   `--inputs`, `--prolog-out`, `--lean-out` share an `(st_dev, st_ino)` pair.
   `realpath` does not canonicalise case, so on a case-insensitive filesystem
   `OUT` and `out` are one directory with unequal realpaths, every comparison is
   an engine agreeing with itself, and Checkpoint 1 passes vacuously — verified
   on Dev's machine. Same for bind mounts of one source. Add the file-level rule
   the directory rule misses: for each selected ID, exit 2 if the two engine
   outputs share `(st_dev, st_ino)`. Extend to the working directory, so the
   meter's own report cannot land inside an argument directory and poison the next
   run under policy 1. (`--inputs` versus an engine directory is already derivable
   — input records have `payload` and no `result` — so only
   `prolog-out == lean-out` is genuinely new.)

**Sequence, as Dev set it.** Dev implements `human/parity/check.py` to PARITY.md
and these policies and installs it. Astra does not implement it, does not read
it, does not propose an implementation, and invokes it only through its CLI. Then
`scripts/parity_conformance.py --meter human/parity/check.py`, reported verbatim
including any WRONG-REASON or informational divergence, with neither the meter
nor the suite adjusted to reconcile them: a conformance failure is a finding for
Dev. Policy 4 settles the `invalid-input-id` fixture, so it is promoted from
informational to enforced; `absent-key-is-not-null` and `no-number-coercion` stay
informational until the envelope-defect classification is settled. After it
passes: regenerate `human/HASHES.txt` so it covers the meter, verify, commit,
re-run `scripts/verify_phase0.sh` and report. **Checkpoint 0 clears when that
shows zero failures and zero outstanding and Dev signs it off — not when the
tooling stops complaining.**

One omission in policy 1 is flagged in A-007 §3: an entry that is a regular file,
not dot-prefixed, and does not end in `.json` is assigned no outcome by any of
the five policies, and policy 5's own stated rationale about `mismatches.jsonl`
depends on the answer. Flagged, not resolved.

## 2026-09-21 — Verification addendum: installed contracts and recorded control

The builder installed the accepted schema wording in PROTOCOL and the staged
DECISIONS template, P-RUNTIME in both PROTOCOL B001 and RUNTIME.md, and the
parity text in PARITY.md with the policy-1 omission explicitly marked open.
The case-fold-unique grammar is installed before the meter exists. These are
installation actions, not new semantic decisions or checkpoint clearance.

**Correction to A-007 and the P-RUNTIME acceptance entry's completion note:**
`docs/contracts/CONTROL_swipl9.json` was already committed in `fb8ce24`, not
merely required. Its SHA-256 is
`ef1043cdf30c4bfb362511c185ac360706f7285c5224139b6a4787cfd33c840d`.
Read-only verification found 376 cases, 312 clean outcomes, 64 distinct error
IDs and `rdiv/2` type-error diagnostics in all 64. Neither the raw control nor
the immutable A-007 answer was edited. The log's historical bodies remain
preserved. GHCR, closure vendoring, archival deposit and native CI are still
obligations, not completed deliveries.
