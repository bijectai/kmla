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
  ∀ h y, Valid h y → 0 ≤ impl h y
```

The `Valid h y` form is B008 (P-VALID-YEAR); this example previously read
`Valid h`.

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

## Amendments accepted 2026-09-21

Accepted by the user in chat and recorded in `docs/DECISION_LOG.md`, which holds
each one's full reasoning. `docs/PLAN.md` is preserved byte for byte, so where
these conflict with it, these supersede it.

These keep the `P-` identifiers the decision log gives them rather than
continuing the `B00N` series, because `STATE.md` already uses `B005` onward for
blockers and reusing those numbers here would make one identifier mean two
different things. `P-STIP` is what resolves `STATE.md`'s blocker B005.

### P-MONEY: money is `Int` whole dollars

Supersedes the plan's Checkpoint 0 instruction "Money as Int cents". Every
source amount is an integer dollar literal and every output is rounded to whole
dollars, so cents would make `Valid` demand multiples of 100 and give models a
unit the reference never uses. The cents-preserving variant is written out in
`human/DECISIONS.md` M1 should this be revisited.

### P-STIP: stipulations, rule grounding and the reader exception

Resolves the case-program blocker. `Household` gains a `stipulations` list; case
rules are grounded by enumeration in the pinned interpreter; round-trip identity
is defined on the grounded lists and on solution sets rather than on bytes; and
the two unterminated `s3306_c_2` files are read with the terminator restored, as
a documented reader exception. 156 of 376 cases stipulate statute predicates and
59 define facts by rules, so a facts-only contract cannot represent them.

### P-TARGETS: per-signature targets and set observation

Supersedes the plan's Phase 2.3 "one target signature per section" and refines
Phase 3.5 and 4.3. `Interface/S{N}.lean` declares one target per queried
predicate signature plus one entry point per section; the observation of a
target is the sorted, deduplicated solution set; scalar entry points are first
solutions; per-case accuracy for models is computed on the
stipulation-independent subset of the originals.

### P-VALID-YEAR: `Valid` is year-indexed

Refines B004's statement form (above) from `∀ h y, Valid h → …` to
`∀ h y, Valid h y → …`. One reference-undefined region — the head-of-household
recursion through a supported parent — depends on the taxable year, and a
year-free exclusion would remove every section 2(b)(1)(B) input. `Valid` may
import `Oracle/` for the two conjuncts that need it.

### P-INTENT: fidelity rule

Where the runtime, reader or observation is under our control, choose the option
that reproduces the authors' own results. Where the statute code itself diverges
from its evident intent, translate the code **as written** and report the
divergence as a finding: the parity meter compares against the pinned program on
the unmodified `human/sara`, so an oracle that "corrects" the source cannot
reach zero mismatches. Grading the intended readings instead would require a
corrected Prolog copy as the parity reference and is a separate contract change,
to be proposed rather than applied silently.

## Design-flaw stop-and-report standard

When a design flaw is discovered, halt the affected development and record the
evidence, consequence, and needed decision under `STATE.md` → `Blockers`.
Report it to the user before implementing a revised design. Do not silently
change the experiment, comparison, input population, or semantic interpretation.
The mutation-admission review that led to B003 is the standard to follow.
