# Approved amendments to the build plan

Accepted by the user on 2026-09-20. These amendments supersede conflicting text
in the original, preserved `docs/PLAN.md`.

## B001: Source and runtime

Use the canonical JHU SARA artifact, designated SARA v2 by the user. The verified
source identity and installed paths are in `docs/contracts/SOURCE.md`.
The primary source is not DeonticBench's copy; an audited downstream program may
be used later only as a second oracle for cross-checking.

Pin SWI-Prolog 7.2.3 in Docker on `linux/amd64`. Record an immutable image digest
and verify the runtime version and architecture before harness evaluation.
Count the original cases without silently dropping any; a discrepancy must be
reported for a human decision, not repaired by filtering or changing semantics.

## B002: Bootstrap boundary

All Phase 0.1 drafts destined for protected artifacts go under `docs/contracts/`.
The human owner copies approved drafts into `human/` and pins their hashes.
The assistant must never write under `human/`, including during bootstrap.
Existing files there are preserved. Read-only mount and submodule/hash
enforcement are prerequisites for the later development lanes.

## B003: Independent mutation admission and grading

`mutate/admit.py` admits a whole-section mutant only when it compiles, passes the
hygiene gate, and a targeted white-box witness search establishes an input on
which it differs from the oracle. The search may inspect the mutation site,
perturb the fields read by the mutated clause, sweep around mutated literals,
and perform large-budget random fuzzing with a seed disjoint from `gen/`.
Record search budgets and seeds.

Admission witnesses live in `mutate/witnesses/`. They are never merged into
`gen/out/`. No witness within budget means `UNRESOLVED`; report these mutants
separately and exclude them from the kill-rate denominator. Do not label them
equivalent.

Freeze `gen/out/` at Checkpoint 2 and record its hash. A kill means the
differential grader refutes an admitted mutant on that frozen black-box corpus.
Admission evidence does not itself count as a kill. Report per-section counts
of admitted, killed, surviving, and unresolved mutants.

A survivor has an established witness but was not refuted by the frozen corpus:
it exposes a corpus blind spot. At Checkpoint 3a, the human names missing input
modes. Adding these modes produces a new, separately frozen corpus version v2.
Re-run on the same admitted mutant set and report both v1 and v2 kill rates.
Preserve the original corpus and admitted-set identities so results remain
reproducible. Never insert the admission witness files into the grading corpus.

## B004: Claims and checked refutations

A signed invariant defines a proposition parameterized by the implementation:

```lean
import Interface.S151
def S151_nonneg (impl : Household → Year → Int) : Prop :=
  ∀ h y, Valid h → 0 ≤ impl h y
```

The human owns the statement in `human/invariants/statements/S151_nonneg.lean`.
The assistant's oracle proof is a separate theorem in
`invariants/proofs/S151_nonneg.lean`:

```lean
theorem S151_nonneg_oracle : S151_nonneg Oracle.s151_exemption := by
  -- Supply a kernel-checked proof of the exact signed claim.
```

These examples define the contract; they are not populated claims or proofs.

Invariant `REFUTED` requires a kernel-checked theorem such as
`¬ S151_nonneg model_impl`, proved by exhibiting concrete `h` and `y` and
discharging the violation by `decide` or kernel-checked evaluation. Candidate
counterexamples may come from the frozen corpus and witness search over the
claim's quantified variables. They do not mutate the frozen corpus.

Failed proof search is `PARTIAL`, never `REFUTED`. A checked violation takes
precedence over unproved goals. Signed statements are never weakened. All
proofs remain subject to the gate and approved axiom whitelist; evaluation
must not bypass kernel checking.

## Design-flaw stop-and-report standard

When a design flaw is discovered, halt the affected development and record the
evidence, consequence, and needed decision under `STATE.md` → `Blockers`.
Report it to the user before implementing a revised design. Do not silently
change the experiment, comparison, input population, or semantic interpretation.
The mutation-admission review that led to B003 is the standard to follow.
