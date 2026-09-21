# Prolog execution contract

## Accepted pin (P-RUNTIME and B001, 2026-09-21)

Use Debian **`swi-prolog-nox=7.2.3+dfsg-6`**, Docker **`linux/amd64`**, and
**`TZ=America/New_York`**. This is the same accepted amendment as PROTOCOL B001,
not an exception to an otherwise-operative upstream-build requirement.
Before evaluation, verify the interpreter's reported `7.2.3`, `PLARCH=amd64`,
the exact Debian package version and TZ from inside the container. Fail on a
mismatch or an unavailable pin; do not fall back to the host or a newer image.

### Why the wording changes

Dev's decision replaces the earlier "exactly that interpreter" requirement as
unachievable, not as a standard lowered to match this build. The recorded image
search found no published 7.2.3 image. Debian's `+dfsg` source omits upstream
files for licensing; the `-nox` package further narrows the distribution, and
the contemplated self-built alternative would carry owner-authored patches.
Every considered option deviates from an unspecified original upstream binary.

Rejecting an upstream build is **not** an argument that old source needs a
modern toolchain: it could use the same pinned Debian stretch, gcc 6.3 and
glibc 2.24. The reasons are path dependence (the accepted interpreter claims in
`human/DECISIONS.md` were measured on Debian's build) and patch provenance.
Debian patches are third-party, contemporaneous, reviewed and citable by a
package version; owner-authored patches would be novel and unreviewed, authored
by the party whose results depend on them. Both could be recorded; "recorded
versus unrecorded" is not the distinction. Full owner text:
`OWNER_DECISIONS_2026-09-21.txt`; acceptance: `docs/DECISION_LOG.md` P-RUNTIME.

## Identity and historical evidence

Identity is the **entire `RUNTIME.json` record except `image.local_image_id`**.
This includes the base image digest, Dockerfile SHA-256, complete installed
package closure, environment (especially TZ) and execution provenance. Future
record fields participate without another contract amendment. A local config
digest is not a registry manifest digest; retain it as diagnostic metadata,
not as a substitute for the immutable GHCR reference.

TZ is a required build argument with no default. Equal Dockerfile hashes can
produce different results if TZ differs. Record and verify it inside the image.
Do not overwrite old records when rebuilding or vendoring: retain the old
record and associate every sweep with the record used to produce it. A changed
Dockerfile requires a new identity record and a new full-corpus sweep.

The existing `CORPUS_BASELINE_america_new_york.json` records **376 clean
directive outcomes, including two vacuous cases that execute no test**
(`s3306_c_2_neg`, `s3306_c_2_pos`). It is not evidence of 376 exercised
assertions, reader-repaired parity, or a Lean oracle. The unmodified source
control `CONTROL_swipl9.json` records SWI-Prolog 9.2.9: **312 clean, 64 errors**;
all 64 recorded errors are `rdiv/2` type errors, corroborating O-7's coercion
observation. The corpus discriminates these interpreter versions in 64 cases.
Two cases discriminate the measured time-zone choices. Keep both controls and
all failures; never filter cases to improve a baseline.

## Time zone and execution provenance

P-TZ requires `America/New_York`. `utils.pl:7` adds a day before constructing
UTC stamps; `format_time/3` renders locally. The recorded UTC sweep has 374
clean outcomes and two failed directives, whereas New York has 376 clean
outcomes (with the same two vacuous files in both populations).

Emulation is allowed; the existing arm64-host measurements are not discarded.
Record the translator's identity and supporting evidence, not a boolean or an
architecture-based guess. If it cannot be established, report that provenance
gap rather than claiming QEMU or Rosetta. Run `harness/run_corpus.sh` in native
amd64 CI on `ubuntu-latest` and retain that as the recorded baseline, alongside
its runtime record, source identity, commit, command, per-case diagnostics and
CI run identity. A workflow definition alone is not a completed native run.

The owner identifies timeout sensitivity (two cases previously needed a longer
limit) and x87 long-double paths as residual emulation risks, as distinct from
integer/GMP arithmetic and SSE2 doubles. Do not turn that risk assessment into
an unmeasured blanket guarantee that time formatting cannot differ. The native
sweep checks the corpus; it is not proof of equivalence on every possible input.

The earlier claim that emulation ignored command-line arguments was a
misdiagnosis of `ENTRYPOINT ["swipl"]`: passing `swipl` again produced
`swipl swipl ...`. The Dockerfile now uses CMD. Dev owns correction of the
protected decisions preamble; the builder does not edit it. Stdin remains valid.

## Three archival legs

1. **GHCR output pin.** Publish the image and record its immutable manifest
   digest. A tag or local image ID is not enough. This preserves re-download,
   not independent rebuilding.
2. **Offline rebuild materials.** Vendor the dependency closure, not only
   `swi-prolog-nox`: include exact-version binary packages, hashes, redistribution
   notices/corresponding sources as required, and the base-image/root-filesystem
   materials needed without Docker Hub. A build that still fetches its base or
   a dependency from a registry/archive has not met this requirement. Validate
   rebuilding with network access disabled. Retain pre-vendoring and
   post-vendoring runtime records and re-sweep after the Dockerfile changes.
3. **Independent image archive.** Save the complete image with `docker save`,
   record its SHA-256, verify restoration, and deposit it with the paper in an
   archive independent of Docker Hub and GHCR. Record the deposit identifier.
   A local tarball is preparation, not a completed deposit.

These obligations fail differently and are all required. Do not mark any as
complete without the artifact and verification evidence. NOTICE.md records the
Debian redistribution obligations; a version list alone is not a vendored bundle.

## Harness boundary

Mount the original corpus read-only at `human/sara/sara/` (in the container,
`/corpus`); `statutes/prolog/init.pl` and case consults require its layout and
working directory. Put all writable outputs elsewhere. Record source hash,
input IDs, commands, environment, exit codes, stderr and timeout diagnostics.
An interpreter exiting 0 is not successful query evaluation or parity.
Reader exceptions and result serialization remain governed by the approved
semantic decisions. This contract does not waive Checkpoint 0 or authorize
oracle/serializer development before Dev signs it off.
