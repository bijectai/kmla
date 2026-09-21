# Prolog execution contract

The [JHU SARA instructions](https://nlp.jhu.edu/law/sara/) specify SWI-Prolog
7.2.3 for amd64. The future harness must use a Docker image for `linux/amd64`
containing exactly that interpreter and record the immutable image digest.
Version tags alone are insufficient for the recorded experiment.

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
