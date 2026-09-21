# Historical runtime records

`RUNTIME.989b4923760cb050.json` preserves the pre-acceptance record from commit
`fb8ce24`. Its SHA-256 is
`989b4923760cb050cb610594a3de94e64f681a03e47570af83bfebd887d24e4d`.
Its contradictory triple-identity caveat and boolean-only emulation metadata
are historical provenance, not the current contract. Do not rewrite them to
make old measurements appear to have stronger provenance than they did.

The record's Dockerfile hash is `a264fb89c957b862fdcb635c1f9abe6d2817167dba056d8549dbb9e4c2df6070`.
It must not be retroactively associated with a later Dockerfile. The existing
legacy corpus summaries identify only a tag and TZ, not a hash of this record;
that linkage limitation remains visible. New runs must retain the precise
runtime record they used and fresh per-case evidence.

P-RUNTIME requires retaining both pre-vendoring and post-vendoring records and
re-sweeping after any Dockerfile change. This snapshot does not claim that
vendoring or native CI has completed.

The current `../RUNTIME.json` is the new measured local record, SHA-256
`c1ca3a433d329ca28818cdd177190f14930a8025e310c0c9f1310d862c1aa12d`.
It identifies Rosetta for Linux by the active Prolog process's translator binary
and hash, and records 102 installed packages. It was produced by a fresh local
build with Dockerfile SHA-256
`fc26076b088477b1e3c56af553ecbc6f916a69b297114cbd1a76ec734493d448`.
The fresh sweep is still outstanding: no old corpus result is attributed to this
new runtime record. Vendoring has not yet occurred, so these are pre-vendoring
history and current measurement, not the promised post-vendoring pair.
