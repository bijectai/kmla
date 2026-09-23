# Query-admission proof resumption — 2026-09-23

Dev authorized continuation after the reported circuit breaker. Entry HEAD:
`b80a807`. The previous three-failure record remains unchanged in
`QUERY_ADMISSION_CIRCUIT_BREAKER_2026-09-22.txt`. Q-016/A-016 supplied a
proof-engineering review, not a semantic amendment. No protected file changed.

## Diagnosis

On the unchanged committed code, `bash scripts/check_query_time.sh` reproduced
the same `decide` reduction failure. Scratch probes against pinned Lean 4.33.1
isolated these outcomes (no edits to the guarded proposition):

| `by decide` proposition | Outcome |
| --- | --- |
| `"abc".toList = ['a','b','c']` | Pass |
| `("2101-01-01".splitOn "-").length = 3` | Reduction failure |
| `"2101".toInt? = some 2101` | Reduction failure |
| `(queryTimeSchema? "s3306_c_10_A_ii" 3).isSome = true` | Pass |
| `Day.toISO 0 = "1970-01-01"` | Pass |
| `(Household.mk [] []).v3 2015 = true` | Pass |

In particular, A-016's predicted renderer failure did **not** reproduce. The
renderer remains unchanged. The evidence does not justify the broader claim
that every well-founded definition is irreducible: raw `#reduce` probes also
hit recursion/heartbeat limits. The actionable finding is the pinned parser
calls' failure under the ordinary concrete proof, not a universal Lean claim.

## Fix and exact claim

Only `Day.fromISO?`'s split/digit plumbing changes: structurally recursive
character-list splitting and ASCII digit scanning replace the core String
calls. Bounds, inverse civil arithmetic and the final exact `toISO` equality
remain unchanged. Canonical in-range dates contain unsigned ASCII digits;
noncanonical widths, signs, invalid dates and overflow are still rejected.

The guarded proposition is unchanged (now named for an axiom audit):

```lean
theorem outOfRangeQueryRejected :
    ¬ Nonempty (AdmittedQuery .original emptyH 2015
      (r8 (day "2101-01-01"))) := by
  intro ⟨checked⟩
  have bad := checked.actual_v3
  have rejected : emptyH.v3ForQuery 2015
      (r8 (day "2101-01-01")) = false := by decide
  rw [rejected] at bad
  contradiction
```

There was one resumed production-code/proof edit cycle; it passed. A patch
context mismatch before applying any change was not a Lean test/edit cycle.
No `sorry`, native decision axiom, relaxed assertion or reference value was
introduced. The test-local guard instance remains test-only.

## Verification

`bash scripts/check_query_time.sh` exits 0, with these output lines:

```text
ok: 175 shared signatures; 135 queried; 31 stipulated; generated tables match
'QueryAdmissionTests.outOfRangeQueryRejected' depends on axioms: [propext, Classical.choice, Quot.sound]
'QueryAdmissionTests.outOfRangeStipRejected' depends on axioms: [propext, Classical.choice, Quot.sound]
ok    query-time guards and kernel-checked boundary proofs passed
```

The suite checks all 73,414 admitted days for round-trip and Workday-year
coverage. New literal-string kernel proofs cover malformed leap/overflow,
widths, plus sign, missing/extra components, non-ASCII digits and a valid date.
An additional kernel theorem rejects an out-of-range stipulated Workday for
every possible root query; it too uses only X1 and passed on its first run.
The pre-edit parser is retained as a test-only regression function: results
match on all 93,786 combinations of years 1899..2101, months 00..13, days
00..32, plus 19 adversarial text strings. This is finite regression evidence,
not a general parser-equivalence theorem over all Strings.

Other commands in this resumed turn:

- `python3 -B -m unittest discover -s scripts -p 'test_*.py'`: 99 tests, OK.
- `bash scripts/check_interface.sh`: 115 behavioural guards, pass.
- `python3 -B scripts/human_manifest.py verify`: every protected record matches.

Production operational call-site coverage, R5 eligibility-decider exactness,
finite-universe/decrease/fuel proofs, full semantic round trips and Lean/Prolog
parity remain open. This resolves the pre-dispatch proof obstruction; it does
not sign off Checkpoint 1 or claim a general date-characterization theorem.

## Self-review

No Prolog behavior is inferred from this Lean reduction result. D1/V3/V9,
tag preservation and the approved canonical-date boundary are unchanged;
unsigned scanning is justified only inside the existing canonical round-trip
check. The previous circuit breaker was honored until Dev resumed work.
Three failed edit cycles on one test still require stop-and-report; this
resumption used one successful cycle on that test.
