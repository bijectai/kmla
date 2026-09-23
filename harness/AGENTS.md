# Harness / serializer lane isolation

Read the root working rules. This context uses original Prolog, the approved
`human/DECISIONS.md` and shared `Interface/`. Never inspect `Oracle/`, oracle
tests, or oracle implementation reports. A callable Lean runner is an opaque
integration interface; the orchestrator coordinates it without sharing code.

Use `runtime.container` for pinned Prolog execution: the complete human bundle
and corpus must be mounted read-only, with independent writable output outside
it. Never inspect the independent meter's source; only invoke its contract.
No case file is executed directly on the host. Do not write protected files.

Implement H4 grounding, ordered/multiplicity-preserving round trips, tags and
wildcards exactly. Preserve all 376 originals and report exceptions/timeouts/
decode failures as failures, never empty answers or excluded records. Retain
raw diagnostics and mismatch lines verbatim. Raw directive success is not
semantic round-trip identity or Lean parity.

V3 includes supplied dates at the shared schema boundary. Every producer/entry
wrapper must consume actual-tuple admission; ValidStip alone is insufficient.
Unknown roles, fields, target modes or projection decisions are not defaults.
The shared lossless JSON field map and fixtures must be fixed in Interface
before emitting producer records; request shared changes through the
orchestrator, never copy another lane's implementation.

Report record, distinct-household and original-case counts separately. Phase 2
generation is not authorized before Checkpoint 1. No answer-dependent filter.
End each handoff with Prolog assumptions and the circuit breaker: three failed
edit cycles on one test means stop and report.
