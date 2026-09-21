# Prolog execution contract

The [JHU SARA instructions](https://nlp.jhu.edu/law/sara/) specify SWI-Prolog
7.2.3 for amd64. The future harness must use a Docker image for `linux/amd64`
containing exactly that interpreter and record the immutable image digest.
Version tags alone are insufficient for the recorded experiment.

## Time zone (P-TZ, accepted 2026-09-21)

The container must run with `TZ=America/New_York`, and the setting is recorded
alongside the image digest as part of the artifact's identity, not as an
environment detail.

`utils.pl:7` adds a day before `date_time_stamp/2` builds a stamp at a zero UTC
offset, and `section3306.pl:76`, `section3306.pl:192` and `section7703.pl:210`
read those stamps back with `format_time/3`, which renders in local time. In a
negative-offset zone the render cancels the `+1`. The reference reproduces all
376 SARA labels only under that zone: `UTC` and `Asia/Tokyo` each leave
`s3306_a_1_B_neg` and `s3306_a_2_B_neg` disagreeing with their own labels. The
setting changes the meaning of section 7703(b)(3) and of the week counts in
section 3306(a)(1)(B) and (a)(2)(B).

A harness that does not pin `TZ` has not pinned the experiment. Verify it from
inside the container along with the version and architecture, and fail if it
does not match.

Before evaluations, verify and retain the interpreter's reported version and
architecture from inside the container. Fail if they do not match. Do not fall
back to a host interpreter or a newer image when the pin is unavailable.

The original source is mounted read-only. The installed corpus root is
`human/sara/sara/`; `statutes/prolog/init.pl` consults the complete statute set
relative to that corpus. Per-case directives likewise depend on the original
layout. Writable outputs must be separate from the source mount.

Record image digest, interpreter version, architecture, execution command,
environment, source hash, input IDs, and exit/timeout diagnostics for each run.
The decisions must resolve numeric and date behavior before output serialization.
An interpreter process exiting does not by itself establish successful query
evaluation or parity.

Selecting/building and testing the pinned image belongs to Phase 1. This contract
does not claim that the image exists locally or that the corpus has executed.
