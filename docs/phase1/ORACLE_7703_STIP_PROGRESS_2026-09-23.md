# §7703 stipulated-root progress — 2026-09-23

Bounded bffb/bbfb H4 assembly is implemented. Fresh Lean 4.33.1 verification
passes the unchanged 62-theorem suite and 25 new focused theorems. This is
**not a completed reference, original parity or CP1 pass**; the actual s152
provider remains required and unimplemented here.

## Changed paths

- `Oracle/S7703Stip.lean` (new): section-local freshening, tagged ground-input
  head unification, ordered stipulated clauses, subsequent spouse binding, and
  a proof that existing admission supplies head-arity well-formedness.
- `Oracle/S7703.lean`: imports the helper; adds bffb/bbfb assemblies, exact-tuple
  admitted entry wrappers and explicit observation adapters. All nine existing
  source clause bodies are preserved; comments now describe the implemented
  stipulation layer. Existing NAF 8/8, AGG 5/5 and CUT 0/0 annotations remain;
  H4 head matching introduces no new source NAF/CUT/AGG site.
- `Oracle/Tests/S7703Stip.lean` (new): 25 focused theorems and axiom printouts.
- `Oracle/Tests/S7703_STIP_BUILD_R1.txt`, `S7703_STIP_BUILD_R2.txt`,
  `S7703_STIP_ROOT_BUILD.txt`, `S7703_STIP_TEST_R1.txt`,
  `S7703_STIP_FINAL_VERIFICATION.txt`: new raw evidence, preserving the only
  initial failure and the final successful commands/results.
- `Oracle/UNPROVED.md`: prepended current ledger/open obligations, preserving
  all prior history. This NEW report; the previous progress report is untouched.

No shared Interface, human/, STATE/HANDOFF, scripts, prior tests/logs, or later
section was edited. No git action or direct consultation occurred. Required
root/lane instructions and current PLAN/PROTOCOL/HANDOFF/STATE were read; no
harness/gen implementation/tests/reports, meter source or exploits were read.

## Implemented boundary

Authority: human/DECISIONS.md G1–G4/G8, H1/H4.1, A1/A3 and H6.2; the original
section7703.pl:2–9; existing Interface Pat, Stip, Term, QueryCall and admission.
Each matched stipulated clause contributes one row after all statute rows.
The statute's bbfb nonvar disjunction still doubles its solutions, but not the
appended facts. Statute-only identity/NAF guards do not constrain those facts.

Ground inputs are Taxp/Year and, for bbfb, Spouse. Marriage is free; bffb has
distinct free Spouse/Marriage query positions. Repeated stored ids inside a
stipulated head name the same variable. Each head is freshly renamed before
matching; duplicates and later invocations use new ids, with no leaked binding
environment. Ground constraints in any input position—including the last Year
position—propagate to every occurrence of that variable. G4 tags are never
coerced. Unbound values remain shared Pat.wild values, not invented ground terms
or null; only explicit observation maps them to null.

The result uses existing types: `(next-unused Nat, ordered List of Pat rows)`.
Nat is a threaded administrative fresh-id supply, not a payload field or fuel.
Main explicitly confirmed this internal state does not by itself need a new
shared payload declaration. Callers must pass the returned supply into later
invocations and never reset it while retaining live outputs. The wrappers keep
AdmittedQuery for the actual tuple, CoveredR5Time for the actual year, and the
required provider; there is no production OracleGuards instance or dummy provider.

## Verification and retained failures

Working directory: `/Users/devrashie/Documents/csProjects/kmla`.
Pinned identity: Lean 4.33.1, arm64-apple-darwin24.6.0, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, Release.

Fresh directory created with
`mktemp -d /private/tmp/kmla-oracle7703-stip-final.XXXXXX`:
`/private/tmp/kmla-oracle7703-stip-final.y3qRdj`.
Full exact build commands, exit statuses, raw outputs and hashes are retained in
`Oracle/Tests/S7703_STIP_FINAL_VERIFICATION.txt`. Dependencies were built in order:
Interface/Household, Interface/QuerySchema, Interface/QueryTime,
Oracle/S7703Stip, Oracle/S7703, using the following pinned command shape for each
actual file listed in the log:

```sh
LEAN_PATH=/private/tmp/kmla-oracle7703-stip-final.y3qRdj lean +leanprover/lean4:v4.33.1 -o /private/tmp/kmla-oracle7703-stip-final.y3qRdj/Oracle/S7703Stip.olean Oracle/S7703Stip.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-stip-final.y3qRdj lean +leanprover/lean4:v4.33.1 Oracle/Tests/S7703.lean
LEAN_PATH=/private/tmp/kmla-oracle7703-stip-final.y3qRdj lean +leanprover/lean4:v4.33.1 Oracle/Tests/S7703Stip.lean
```

All final build/test commands exit 0. Results: **62/62 existing + 25/25 new**.
The original test file is byte-unchanged, SHA-256
`096ac907f363dd7d780787662a75544f271c4dd698b3598f582cd59283e3fa67` before/after;
its one pre-existing unused List.merge warning is retained. New tests cover
append order, duplicate clauses, tag/year mismatches, shared-variable consistency,
input-to-output propagation, invocation freshness, later binding, and null/set
observation only at the boundary. One fresh-allocation test quantifies over
every starting Nat; assembly tests quantify over the missing provider.
All new printed axiom sets are subsets of X1, with no recovery axiom. No full
hygiene-gate or source-equivalence proof is inferred from these checks.

Only failure: first helper compile reported `Unknown constant
Bool.and_eq_true.mp` at lines 95–96. Full R1 diagnostics are preserved; the second
helper compile used the same premise via existing simplification and passed.
There was no observation mismatch or failed assertion edit cycle. The initial
24 tests passed, then the additional bbfb shared-marriage test passed in the
fresh final run. Latest goals: none; no breaker fired. UNPROVED contains the
complete attempt ledger, including prior-round history.

## Remaining dependencies and next integration

The actual s152 provider, recursive execution, other root modes/general relational
continuations, H6 Bool entry, full source/freshness correspondence, and caller
supply-threading coverage remain open. So do production guards, V10 equivalence,
participant universe, phase/decrease/counter adequacy, E2 exclusion and R5/R8
actual-time coverage. No new semantic decision, finite wildcard universe or
exhaustion-as-answer is introduced to conceal those obligations.

Main independently reports its fresh runner now unconditionally compiles the
helper and both modules, with 62+25 theorem declarations passing and unchanged
implementation/test hashes during verification. Main's evidence is at
`docs/phase1/q021-oracle-stip-independent-2026-09-23/`; this lane did not run or
inspect that verification or edit its script. The focused test SHA-256 is
`f7f5715d1064a034d839a6fb778cb6de8b50cdd1e3df042a611f493ab3e3a548`, matching
this lane's final log. The modules are `Oracle/Tests/S7703.lean` and
`Oracle/Tests/S7703Stip.lean`; runner wiring is complete per main's confirmation.
Opaque harness/record integration remains main-owned and must preserve these
dependency/admission limits. No Prolog comparison or meter invocation occurred:
0 parity records, 0 original households/cases compared, **376-case parity and
CP1 unpassed**. No §3306 work began.

## Self-review

Assumptions: (1) G1 preserves clause/body/solution order and duplicate proofs;
(2) G2 modes here have the stated ground inputs and distinct free query outputs;
(3) G3/G4 ground unification is structural and tag-sensitive, without coercion;
(4) equal variable ids within one head retain identity, but clause invocations
freshen independently; (5) bindings from failed head attempts do not escape;
(6) H4 stipulated facts append after statute clauses and do not inherit their
guards; (7) shared flat Term/Pat values require no compound-term occurs check;
(8) callers thread a fresh supply above existing live output ids;
(9) H6 observes unbound as null and deduplicates only at the boundary.
Existing first-condition commitment, NAF, date and aggregate rules are unchanged.
No complete source/reference or R5 adequacy claim is assumed.

Circuit breaker: **three failed edit cycles on one test means stop and report;
no fourth attempt or assertion weakening.**
