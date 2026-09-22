# Draft corpus-impact evidence: A, C, and witness-only B

Date: 2026-09-22. Diagnostic evidence only; no restriction, producer, schema,
grounding implementation, or production observation encoding is installed.
The two diagnostic witnesses are not included in the 376-original counts.

## Results for all 376 originals

The authoritative run is `full-20260922-01/`: **376/376 originals completed,
zero unresolved runs**, plus **2/2 witnesses** separately. Every run exited 0,
without timeout or stderr. Case-source clauses were evaluated by pinned SWI,
not approximated by lexical matching.

| Audit item | Original result |
| --- | --- |
| Distinct birth events per person greater than one | 0 cases; exact case list `[]` |
| Distinct `start_` dates per birth event greater than one | 0 cases; exact case list `[]` |
| Equal known birth-date pairs of distinct people | 0 pairs in 0 cases |
| Equal-date sibling / stepsibling / neither pairs | 0 / 0 / 0 |
| Equal-date K-related pairs | 0 |
| K self edges | 0 |
| Refined A failures, all years 1900–2100 | 0 cases; exact failing case/year list `[]` |
| C failures: directed K cycles, including self | 16 cases, listed below |
| Cycles in the evaluated child-to-parent graph used for the V4 check | 0 cases |

Accounting: 5,776 supplied case clauses; 29 birth solution rows in 16 cases;
29 nonempty person/birth groups and 29 birth-event/date groups. Every such
original group has distinct cardinality one. The per-case U sizes sum to
5,229 (not a global count of distinct persons). All 113,341 ordered U×U pairs,
including self pairs, were tested for K. There are 183 K edges and therefore
36,783 K-edge/year c3 membership tests; 11,287 succeeded. These are membership
counts, not counts of Prolog solutions.

The complete per-case/per-domain-element counts, including measured zeros,
are in `all_results.json`, fields `birth_events_per_person` and
`start_dates_per_birth_event`. No case is omitted for lacking births.

### Exact C exclusion list

K is oriented **taxpayer → dependent**, with both bound when calling the
original `s152_c_2(Dependent,Taxpayer,_,_)`. Each listed component contains
both directed edges between its two displayed members. Additional edges
remain in the raw data; they have not been pruned.

| Original case ID | Cyclic component |
| --- | --- |
| `s152_c_2_A_neg` | `alice ↔ bob` |
| `s152_c_2_B_pos` | `alice ↔ bob` |
| `s152_d_2_A_neg` | `alice ↔ bob` |
| `s152_d_2_B_pos` | `alice ↔ bob` |
| `s152_d_2_D_neg` | `bob ↔ charlie` |
| `s152_d_2_E_neg` | `alice ↔ charlie` |
| `s152_d_2_E_pos` | `bob ↔ charlie` |
| `s152_d_2_F_pos` | `alice ↔ charlie` |
| `s2_b_1_A_ii_pos` | `bob ↔ charlie` |
| `tax_case_11` | `alice ↔ charlie` |
| `tax_case_18` | `bob ↔ charlie` |
| `tax_case_53` | `alice ↔ bob` |
| `tax_case_64` | `alice ↔ bob` |
| `tax_case_70` | `alice ↔ bob` |
| `tax_case_75` | `alice ↔ charlie` |
| `tax_case_85` | `alice ↔ charlie` |

### Refined A actually checked

The global uniqueness checks are at most one distinct birth event per
person and at most one distinct start date per birth event. In addition,
for every K(T,D) and each integer Y from 1900 through 2100 for which the
original `s152_c_3(D,T,Y)` succeeds, the diagnostic checks:

1. If D has a birth event, D and T each have one birth event and one known
   date, and T's date is strictly earlier than D's date.
2. If D has no birth event, the original `is_descendent_of(D,T,_,_)` succeeds.

The explicit one-event tests in branch 1 agree with the global uniqueness
requirement. The strict diagnostic comparison is
`is_before(TDate,DDate), \+ is_before(DDate,TDate)` with both dates ground.
The original non-strict `is_before/2` and original c3 are not changed.
Earlier-draft equal-date/no-self components are retained as separate fields,
not silently substituted for the refined A definition.

Stipulations were included. For example, the original
`human/sara/sara/cases/s152_c_1_pos.pl:24–25` supplies both c2 and
`s152_c_3(bob,alice,Year) :- between(2015,2020,Year)`.
The measured loaded counts for each predicate are one original clause plus
one case clause, giving two. This case has no birth event for Bob, c3
succeeds in exactly 2015–2020, and the original descendant predicate succeeds
from the supplied son event. The refined birthless branch therefore passes;
no birthday was fabricated to cover the stipulation.

## Two diagnostic witnesses, separate population

The sources are `docs/consult/evidence/r5_sibling_cycle.pl` and
`docs/consult/evidence/r5_multibirth_cycle.pl`. Both have K edges
`a → b` and `b → a`, no K self edge, and an empty child-to-parent graph.
Both fail C. Both fail refined A at 2018, with the exact all-year details below.

| Witness / K edge | Refined A edge failure | Exact failing c3-success years |
| --- | --- | --- |
| sibling: `a → b` | Taxpayer date is not strictly earlier | 1900–2024 inclusive (125) |
| sibling: `b → a` | Taxpayer date is not strictly earlier | 1900–2024 inclusive (125) |
| multibirth: `a → b` | Taxpayer has two birth events and two known dates | 1900–2025 inclusive (126) |
| multibirth: `b → a` | Dependent has two birth events and two known dates | 1900–2026 inclusive (127) |

There are no gaps inside these year ranges. All other tested years have no
c3 success for the corresponding edge. Independently, the multibirth witness
violates global birth-event uniqueness for `a` at every tested year; the
global failure is not restricted to the edge-specific c3-success years.

The sibling witness has exactly one equal-date pair, `(a,b,"2000-01-01")`:
original sibling succeeds, stepsibling fails, and K succeeds in both
directions. Both people have one birth event with one date. The multibirth
witness has no equal-date pair: `a` has dates 2000-01-01 and 2002-01-01,
and `b` has 2001-01-01. Each individual birth event has one start date.
Neither witness supplies an equal-date unrelated pair.

The early years are deliberate observations, not a lower-bound correction:
the original c3 source (`section152.pl:217–230`) bounds age from above and
does not require a nonnegative age. No pre-birth year was filtered out.

### Direct observed B-prefix evidence at 2018

For each witness, the full finite prefix solution enumeration used:

```prolog
member(T,U), member(D,U),
s152_c_1_A(D,T,S,E),
s152_c_1_B(D,_,T,S,E,2018),
s152_c_1_C(D,T,2018).
```

The very same S/E variables are passed between A and B within each solution.
No c1E call occurs in this prefix enumeration. For **each** witness the
complete collected list is exactly:

```prolog
[prefix(a,b,A,B), prefix(b,a,A,B)]
```

Here `prefix(T,D,S,E)` is a diagnostic display. `A` and `B` represent two
distinct unbound variables in that solution; numbering restarts separately
for each displayed solution. They are not atom values or a cross-solution
identity. Thus the observed E graph contains exactly `a → b` and `b → a`
for both witnesses. This is direct c1A/B/C evidence, not an inference from K
and c3 tested independently. No 376-original B-prefix sweep was performed.

Separately, both witnesses pass `s7703_a(a,_,_,2018)` and both directional
c3 checks at 2018. The diagnostic `s7703(a,_,_,2018)` reaches both the
100,000 and 1,000,000 inference limits. These bounded results are not, by
themselves, a proof of nontermination. Original file test directives were
not run; these explicit probes are the only recursion probes in this audit.

## Potential K self edge versus V4

No self edge was observed in the 376 originals or the two witnesses.
This is not a theorem that V4 excludes K self edges. Source inspection shows
that `section152.pl:178–187` admits a dependent that is a descendant of a
taxpayer's sibling/stepsibling. The predicate has no overall dependent ≠
taxpayer guard. In particular, instantiate taxpayer and dependent as `p`,
the sibling as `q`, with a sibling event between p and q and one child edge
`p → q`. The parent graph is acyclic, but the descendant-of-sibling branch
has `is_descendent_of(p,q,_,_)`. Direct sibling and child irreflexivity in
`utils.pl:98–159` does not exclude that composite path. Case-supplied c2
clauses are also included directly by the audit.

This paragraph is a source-path observation, not a newly executed third
witness, a full Valid certificate, or an installed restriction.

## Runtime, loading, and provenance

The complete measured runtime identity matches `docs/contracts/RUNTIME.json`
except the explicitly excluded local image ID. It is Debian SWI-Prolog
**7.2.3+dfsg-6**, amd64, with the pinned runtime's timezone and settings.
Identity SHA-256:
`744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`.
Executed image:
`sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7`.

`/proc/self/mountinfo` confirmed `/human`, `/corpus`, `/audit`, and `/evidence`
all mounted `ro` before case execution. Runs also use a read-only container
root, no network, dropped capabilities, and no-new-privileges. No protected
write attempt was used to establish read-only status. Host Python used `-B`;
there are no human-tree caches or permission changes from this audit.

Each input runs in a fresh container. `read_term/3` parses the source without
executing it. Only case clauses and discontiguous declarations are retained;
original consult/load/test/halt directives are recorded and skipped. The
canonical `/corpus/statutes/prolog/init.pl` is consulted once. Case head
signatures are predeclared dynamic before that consult, then every supplied
clause is appended with `assertz` in source order, including duplicates,
helpers, rules, and stipulations. Per-signature before/added/after clause
counts verify that original definitions were not replaced.

H4.4 is the only source repair. One full stop is inserted in the in-memory
code list after line 26, with exact source-hash checks:

| File | Insertion offset (zero-based, before newline) | Original SHA-256 |
| --- | --- | --- |
| `s3306_c_2_neg.pl` | 891 | `20ac10863992b937b3aff70b79ac1c27fa101a555a45feeb21f01c4f0374097e` |
| `s3306_c_2_pos.pl` | 873 | `1b912b348ef4481643a509a920bd6653522571dd9c1f29673d2ad2280c478d88` |

The original bytes are unchanged. All 378 source hashes, all loaded statute
hashes, and the two diagnostic script hashes were rechecked after the full
run and still match its metadata.

The run used four workers, a 120-second outer bound and 500,000,000-inference
audit bound per input. Summed original per-input container elapsed times were
434.189782 seconds; maximum was 2.378306 seconds. Summed concurrent durations
are not wall-clock duration.

## Raw artifacts and scope limits

- `birth_audit.pl`: diagnostic SWI queries, source loading, and explicit probes.
- `run_birth_audit.py`: standard-library driver using unchanged neutral
  `harness/runtime.py`, plus audit-only set counts and graph SCC reduction.
- `full-20260922-01/all_results.json`: all 376 originals and two separate
  witness records. Contains U, birth rows, per-person and per-event distinct
  counts, K edges, child-parent edges, c3 success year lists, refined A reasons,
  equal-date classifications, retained stipulations, skipped directives,
  witness prefix solutions, execution status, and source hashes.
- `full-20260922-01/summary.json`: exact case lists by failure component and
  population; no unresolved inputs are counted as passing.
- `full-20260922-01/metadata.json`, `runtime_measured.json`, `runtime/`,
  `mounts/`, and one directory per input: source/runtime identity and raw
  commands, stdout, stderr, and annotated per-input results.
- `smoke-20260922-01/` and `smoke-20260922-02/`: preserved initial/corrected
  smoke evidence, not the authoritative all-corpus result.

U is explicitly a **finite superset**, not an asserted semantic-person list:
all ground atom/string subterms of parsed case terms, including skipped
query/load/declaration literals, plus evaluated ground agent/patient/
beneficiary values of every unary event solution. Event IDs, places, dates,
and query strings can therefore appear. Rules are evaluated to collect event
solutions and their participant values; parsed event facts alone are not
assumed complete. Unexpected nonground or non-atom/string participant values
raise an error rather than being silently dropped. No claim is made about
arbitrary terms outside recorded U or about producers for arbitrary new cases.

K, c3, descendant, sibling, and stepsibling checks are selected **existential
memberships** using `once`, with the stated bindings. Their complete ordered
solution multisets are not captured. Source clauses remain ordered and
duplicate-preserving during execution; raw birth rows retain duplicate
birth/agent/start answers, and witness prefix collection uses full `findall`.
Distinct counts and graph edges are audit-only sets. Equal-date pairs are
unordered distinct-person pairs per identical known source date term; the
recorded corpus dates require no alias normalization. “Neither sibling nor
stepsibling” is not a proof of unrelatedness in every possible relation.

Term display uses SWI quoted term rendering to distinguish atoms from double-
quoted strings. This is a diagnostic representation, not a production codec
or output projection. Measured empty birth sets mean no solution to the
tested original goal, not invented defaults or a claim that every U member
is a person. The raw data suffice to re-evaluate the stated A/C predicates
on these populations without Prolog re-execution; they are not a replacement
for arbitrary future semantic queries. No parity, semantic round-trip,
full-Valid, universal termination, or formal producer-release claim is made.

## Self-review: Prolog assumptions and supporting evidence

1. **Source execution model:** ordered, duplicate-preserving clauses and
   original goal order are material (signed G1/H1/H4 and the actual statute
   bodies). Original clauses are consulted; case clauses are appended in
   source order without deduplication. Dynamic declarations enable this
   loading arrangement; measured clause-count checks passed for every input.
2. **Parsing and isolation:** `read_term` is used only to read terms; directives
   are not automatically executed. This is enforced by explicit directive
   filtering in the loader and recorded skipped goals. The canonical init
   and signed H4.5 permit one load; the two exact H4.4 repairs are recorded.
3. **Term identity:** atoms and strings are not conflated (signed G/H term
   distinctions, pinned runtime, and quoted raw output). SWI `sort` and ground
   equality provide distinct audit values only; they do not redefine clauses.
4. **Domain coverage is bounded:** U is the documented literal-and-evaluated-
   participant superset, not a semantic-person classifier or absent-person
   default. The script evaluates unary events and bound-event attributes,
   checks groundness, and records the entire domain for each case.
5. **Birth association:** a person's birth events are the original join
   `birth_(E), agent_(E,P)`; known dates add `start_(E,D)`. This is the same
   association used by original c3. Duplicate proofs are retained in the raw
   rows and collapsed only for the requested distinct cardinalities.
6. **Mode and existential scope:** K binds both people before original c2;
   this matters because `s152_c_2_B` uses `==` rather than unification in its
   direct-relative branch. c3 also binds both people and each year. Membership
   results do not claim complete multisets or termination of every later
   alternative after a first success.
7. **Dates and age:** signed D3 and `utils.pl:10–14` make `is_before` non-strict.
   Strictness is a separate two-direction diagnostic check on known dates,
   never a source change. Original c3 and pinned date arithmetic determine
   the reported year sets, including successful pre-birth years.
8. **Descendant strictness:** `utils.pl:158–165` traverses one or more child
   edges, not reflexive closure. V4 excludes nontrivial child cycles; the
   evaluated parent graphs here have no cycle. This does not imply K itself
   is acyclic or self-free, as the inspected c2B path shows.
9. **Stipulations are real clauses:** H4 and the original c1-positive case
   require appended c2/c3 clauses to participate. Before/after counts and the
   birthless 2015–2020 c3 results confirm they were not omitted or replaced
   with a birthday-function assumption.
10. **Prefix sharing and multiplicity:** original c1 calls A, B, C with shared
    S/E. The witness diagnostic uses that exact conjunction, retains its
    complete `findall` list, and only then derives an edge set. Variable
    display numbering is local to a solution, not a semantic substitution.
11. **Bounds are observations, not proofs:** inference-limit outcomes record
    only the bounded SWI run. Cycles in recorded finite graphs are computed
    from observed edges, without asserting a termination theorem or revised
    domain rule.

Circuit breaker: the first smoke run exposed one loader issue: trying to
change the attributes of an already static `s3306_b/8` in the two H4.4 cases.
One correction moved case-head dynamic declarations before canonical init;
the corrected four-input smoke passed and the subsequent full 378-input run
passed. There were not three failed edit cycles on any test. A later one-off
`jq` summary command had a syntax typo, corrected without editing diagnostic
code or rerunning cases. The three-failed-edit-cycles stop rule remains in
force; it was not triggered.

All changes made by this lane for this side task are the two named scripts,
this report, and the three named run directories under
`docs/contracts/phase1-decision-audit/`. Other agents' artifacts in the shared
directory are not claimed as this lane's work. Existing reader edits were
preserved. No `human/`, shared Interface, STATE, HANDOFF, or installed contract
was modified. No oracle code/reports, parity source, or owner meter source
was inspected. No commits or pushes were made. No choice between the draft
options is made.
