# Pinned SWI-Prolog runtime for the KMLA harness.
#
# docs/contracts/RUNTIME.md requires SWI-Prolog 7.2.3 on linux/amd64 with a
# recorded immutable image digest. No published swipl image satisfies that: the
# official library/swipl repository has 123 tags whose oldest is 7.5.11, and
# there is no 7.0.x-7.4.x tag at all. Debian stretch, however, ships
# swi-prolog 7.2.3+dfsg-6, so this image installs it from the Debian archive.
#
# THIS IS NOT UPSTREAM'S 7.2.3 BUILD. `+dfsg-6` is Debian's repackaging with six
# Debian revisions of patches applied. Whether that satisfies B001's pin is an
# owner decision recorded in docs/DECISION_LOG.md (DL-001); this file implements
# one option and does not settle it.
#
# The base image is pinned by digest, not by the mutable `stretch` tag.
FROM --platform=linux/amd64 debian:stretch@sha256:c5c5200ff1e9c73ffbf188b4a67eb1c91531b644856b4aefe86a58d2f0cb05be

# Debian stretch is end-of-life, so its Release files are expired and its
# packages live on archive.debian.org rather than deb.debian.org.
RUN set -eux; \
    printf '%s\n' \
      'deb http://archive.debian.org/debian stretch main' \
      'deb http://archive.debian.org/debian-security stretch/updates main' \
      > /etc/apt/sources.list; \
    printf 'Acquire::Check-Valid-Until "false";\n' \
      > /etc/apt/apt.conf.d/10no-check-valid-until; \
    apt-get update; \
    apt-get install -y --no-install-recommends swi-prolog-nox=7.2.3+dfsg-6; \
    rm -rf /var/lib/apt/lists/*; \
    swipl --version

# ---------------------------------------------------------------------------
# TZ IS A SEMANTIC DECISION, NOT A DEFAULT. THE BUILD REFUSES TO GUESS IT.
#
# utils.pl:7 adds one day (`DI1 is DI+1`) before building a timestamp at a ZERO
# UTC offset (utils.pl:8), and section3306.pl:76,192 and section7703.pl:210 read
# those timestamps back with format_time/3, which renders in LOCAL time. In a
# negative-offset zone the local rendering moves the date back a day, cancelling
# the +1. The two bugs are only equivalent to no bug in a negative-offset zone.
#
# Measured on the shipped corpus with this image (docs/contracts/RUNTIME_OBSERVATIONS.md):
#   TZ=America/New_York : 376 of 376 cases agree with their own labels
#   TZ=UTC              : 374 of 376; s3306_a_1_B_neg and s3306_a_2_B_neg fail
#   TZ=Asia/Tokyo       : 374 of 376; the same two fail
#
# So the "obviously reproducible" choice, UTC, does not reproduce the reference.
# Pick deliberately and record it in human/DECISIONS.md. See DL-002.
# ---------------------------------------------------------------------------
ARG KMLA_TZ
RUN test -n "${KMLA_TZ:-}" || { \
      echo "ERROR: build argument KMLA_TZ is required and has no default." >&2; \
      echo "       The corpus's answers depend on it. See harness/Dockerfile." >&2; \
      echo "       e.g. docker build --build-arg KMLA_TZ=America/New_York ..." >&2; \
      exit 1; }
ENV TZ=${KMLA_TZ} \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# The corpus is mounted read-only at /corpus; outputs go to a separate writable
# mount. docs/contracts/RUNTIME.md forbids writing into the source mount. Cases
# consult `statutes/prolog/init` by a RELATIVE path, so the working directory
# must be the corpus root or nothing loads (verified: from cases/ the consult
# fails and the run still exits 0).
WORKDIR /corpus

# CMD, not ENTRYPOINT. With `ENTRYPOINT ["swipl"]` the natural invocation
# `docker run IMAGE swipl --version` expands to `swipl swipl --version`, and SWI
# takes the first non-option argument as a script file, so every later flag
# becomes an application argument and the run prints the banner instead. That
# symptom was once diagnosed as "the image ignores command-line arguments under
# emulation"; it is not, argv works normally under emulation. CMD removes the
# trap: `docker run IMAGE swipl -q -f cases/x.pl` and `docker run IMAGE sh -c …`
# both behave as written, with no --entrypoint override needed.
CMD ["swipl"]
