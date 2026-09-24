# Stipulation-list integration — 2026-09-23

## Authority and boundary

A-022 classifies the failure as a shared representation gap under signed H4,
not a new owner amendment or reference-undefined original. Its scope audit
finds only the new answer and an append to DECISION_LOG. The audit record is
`docs/consult/evidence/q022-path-audit-2026-09-23.json`; prior answers and the
protected manifest are unchanged. No protected installation is made.

The correction is a distinct recursive stipulation argument, not a list
constructor on event `Term` or `Pat`. Event fact kinds, generated-input V1,
original arity checks, time admission, source order and observation rules must
remain unchanged. Proper lists retain tags/order/duplicates and wildcard ids.
Non-list compounds and improper/open-tail lists remain reported unsupported
values, never coerced data or an excluded original.

## Independent pinned semantic checks

All three diagnostics run on immutable SWI 7.2.3 image
`sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7`,
with read-only mounts and no network. They are synthetic semantic checks, not
admitted inputs, corpus parity or a grounding-completeness claim.

1. `q022-variable-identity/001.*`: `sample(X,[X,Y,[Y]],Y)` numbers X as id 0
   everywhere and Y as id 1 everywhere, with next id 2. Exit 0.
2. `q022-solution-copy/001.*`: two `findall` copies preserve those aliases within
   each row, with ids 0/1 in the first row and 2/3 in the second. Next id 4;
   exit 0. This checks solution-copy freshening separately from numbering.
3. `q022-empty-list/001.*`: exact stdout, exit 0:

   ```text
   atom_empty_list=false
   atom_quoted_brackets=true
   identical=false
   bare=[]
   quoted='[]'
   ```

The paths above are under `docs/consult/evidence/`, with their separate probe
sources retained adjacent. The empty list is not the scalar atom spelled `[]`;
the transport must preserve both. This does not test improper-list support.

## Integration status

The shared context is implementing and verifying the declaration, wire and
fixtures. The two isolated implementation contexts remain paused until that
checked handoff. Neither lane may inspect the other's implementation or invent
a different list spelling. The required next evidence is preservation through
each adapter, both H4 comparisons for the two affected originals, the existing
country regressions and a fresh full-population report.

All earlier failing audit evidence stays unchanged. No all-376 round trip,
production records, `ValidStip` certification, reference parity or Checkpoint 1
pass is claimed.

## Self-review

List containers are distinct from scalar tags and from the outer argument
tuple. Wildcard identity is per variable, not per occurrence; solution copies
freshen, while the wire does not. These assumptions were tested above on the
pinned runtime. Three failed edit cycles on one test require a stop and report;
unsupported values never become ordinary answers. No remedy is implemented in
these diagnostic probes.
