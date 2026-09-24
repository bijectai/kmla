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

Both adapters are complete and independently checked in
`q022-adapters-independent-2026-09-23/`: both named list-bearing originals pass
both H4 comparisons and exact supplied-head checks; the 14-country slice passes
both comparisons/direct retention/three anchors/six guard groups; 144 unit tests
pass; the fresh oracle build passes 62 + 25 + 35 assertions. All 87 prior
assertion statements remain unchanged. Hashes stay stable in each independent
run. The combined oracle checker is now wired into CI, with every assertion
file mandatory. This is not the later hygiene gate or complete Oracle parity.

The fresh broad harness audit stops at its first actual mismatch,
`s2_b_3_B_pos.pl`: H4(a) expands 114 facts to 204. Main independently reproduces
114 -> 204 -> 384 without a code change. Q-023 preserves the exact first differing
fact and asks Fable to distinguish implementation correction from missing owner
choice. No remedy has been attempted. The broad run has 149 diagnostic instances,
93 distinct; H4(a) 148 passes, one failure, 227 unvisited; H4(b) three passes,
145 unimplemented, 228 blocked. The named-case/country successes are separate
run-specific evidence, never inserted into the halted full audit.

The safety rerun in `q022-integration-safety-2026-09-23/` reports Checkpoint 0
17/0/0, ten verifier tests, twelve boundary tests and 29 runtime tests passing.
Later checkpoint inputs remain reported. The owner's meter was invoked through
its contract only; neither its source nor protected artifacts were edited.

The shared context completed the declaration, wire and fixtures. Main's fresh
independent run, retained in `q022-shared-independent-2026-09-23/`, passes all
115 old Interface guards, the unchanged query-time checks, 16 new guards,
20 new kernel-checked proofs and five fixture tests. The final equality
decision uses no axioms; theorem dependencies stay within X1, without sorryAx.
Input hashes stayed stable throughout. The protected manifest verifies.
The first failed new-test cycle and its exact goals remain in the shared
handoff; the structural-recursion correction changed no assertion.

The two isolated implementation contexts may now adapt against this checked
handoff. Neither lane may inspect the other's implementation or invent a
different list spelling. Their pre-change passing results are historical
snapshots, not a claim that the new adapters already build. The required next
evidence is preservation through each adapter, both H4 comparisons for the two
affected originals, the existing country regressions and a fresh full-population
report.

All earlier failing audit evidence stays unchanged. No all-376 round trip,
production records, `ValidStip` certification, reference parity or Checkpoint 1
pass is claimed.

The first adapter dispatch was interrupted during large-context worker setup;
the oracle context reported a service token-rate limit. Both old workers were
closed before any adapter edits landed, and fresh non-forked, lane-isolated
contexts received the bounded tasks. This was not a proof/test failure or a
semantic breaker. Completed earlier goals and source evidence remain retained.
The shared commit `eeea5f9` passed hosted `verify` run 35941841906 and
`Native runtime baseline` run 35941841971; those workflow results are not a
whole-project build, reference-parity result or checkpoint sign-off.

## Self-review

List containers are distinct from scalar tags and from the outer argument
tuple. Wildcard identity is per variable, not per occurrence; solution copies
freshen, while the wire does not. These assumptions were tested above on the
pinned runtime. Three failed edit cycles on one test require a stop and report;
unsupported values never become ordinary answers. No remedy is implemented in
these diagnostic probes.
