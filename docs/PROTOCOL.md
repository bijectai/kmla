# Approved amendments to the build plan

Accepted by the user on 2026-09-20. These amendments supersede conflicting text
in the original, preserved `docs/PLAN.md`.

## B001: Source and runtime

Use the canonical JHU SARA artifact, designated SARA v2 by the user. The verified
source identity and installed paths are in `docs/contracts/SOURCE.md`.
The primary source is not DeonticBench's copy; an audited downstream program may
be used later only as a second oracle for cross-checking.

P-RUNTIME (accepted by Dev, 2026-09-21) pins Debian's
`swi-prolog-nox=7.2.3+dfsg-6` in Docker on `linux/amd64`, with
`TZ=America/New_York` (P-TZ). This amendment and `docs/contracts/RUNTIME.md`
are one decision; the latter no longer requires an unspecified identical
upstream build. Verify interpreter version, architecture, package version and
time zone before harness evaluation; never silently substitute another runtime.

Artifact identity is the **whole `RUNTIME.json` record except
`image.local_image_id`**, including the pinned base digest, Dockerfile SHA-256,
full installed package closure, TZ and execution/translator provenance. It is
not a three-field tuple. Preserve prior records when an identity changes.

Record the immutable GHCR image digest, vendor the dependency closure together
with what is needed to rebuild without either registry (including the base),
and archive a `docker save` image with SHA-256 for deposit alongside the paper
outside both registries. These are three distinct obligations, not alternatives.
Vendoring changes the Dockerfile identity and requires a new record and sweep;
retain both records. Emulated runs remain evidence; native amd64 CI on
`ubuntu-latest` supplies the recorded baseline. Record the actual translator,
not merely an emulation boolean. See RUNTIME.md for provenance and evidence
limits; acceptance of the policy does not claim those deliveries have occurred.

Count the original cases without silently dropping any; a discrepancy must be
reported for a human decision, not repaired by filtering or changing semantics.

## B002: Bootstrap boundary

All Phase 0.1 drafts destined for protected artifacts go under `docs/contracts/`.
The human owner copies approved drafts into `human/` and pins their hashes.
The assistant must never write under `human/`, including during bootstrap.
Existing files there are preserved. Read-only mount and manifest/CI
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

### P-SUMLIST: schema spelling

The Aggregates schema heading reads `every findall/sum_list, duplicate + order
semantics`. The source has twelve `sum_list/2` sites and no `sumlist`. This is
a spelling correction with no semantic effect. It supersedes the preserved
PLAN's schema spelling; neither PLAN nor the protected decisions is rewritten.

### P-RUNTIME and parity policies: owner acceptance

The complete owner directive is preserved in
`docs/contracts/OWNER_DECISIONS_2026-09-21.txt`. P-RUNTIME amends B001 above and
`docs/contracts/RUNTIME.md` together. The five parity policies are installed in
`docs/contracts/PARITY.md`, including directory handling, three-valued report
artifacts, ASCII-case-fold-unique IDs and inode-based alias checks. Only the
invalid-input-id fixture is promoted to enforced; the two envelope-defect
fixtures remain informational pending the owner's classification. A conformance
failure is a finding for Dev, not permission to change the meter or test
expectations. Checkpoint 0 requires the checks and Dev's explicit signoff.

### P-PARITY5 clarification and checkpoint accounting (accepted 2026-09-21)

Directory policy 1 is complete: an entry ending in `.json` joins the population
and is judged by the ID grammar (and regular-file requirement); a dot-prefixed
entry not ending in `.json` is ignored; **any other entry is exit 2**. This
preserves rejection of other non-JSON files, including `notes.txt`; the narrowed
dotfile exemption must not be read as loosening that rejection.

`verify_phase0.sh` reports Checkpoint 2 exploits and Checkpoint 3a signed
statements under their own headings, without adding them to Checkpoint 0's
pass/failure/outstanding counts. They remain visible and mandatory at their
respective checkpoints. Runtime checks are unchanged. Checkpoint 0 clears only
on zero failures, zero outstanding **for Checkpoint 0**, and Dev's explicit
sign-off. A successful script exit is not sign-off.

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

### P-BUNDLE: no submodule; `human/` stays in the parent repository

Supersedes the plan's §2 requirement that the owner-owned artifacts live in a
`human/` git submodule. KMLA is open-sourced as a single repository and `human/`
is an ordinary tracked directory. The two properties the submodule existed for
are carried by CI instead: a pull request that touches `human/` fails unless the
owner labels it, and `human/HASHES.txt` pins every protected file with the
manifest check as a CI step.

The difference is that enforcement is now detection rather than impossibility,
and the bundle is identified by the parent commit plus the manifest rather than
by a gitlink. Both are recorded in `docs/DECISION_LOG.md` under P-BUNDLE.

### P-INTENT: fidelity rule

Where the runtime, reader or observation is under our control, choose the option
that reproduces the authors' own results. Where the statute code itself diverges
from its evident intent, translate the code **as written** and report the
divergence as a finding: the parity meter compares against the pinned program on
the unmodified `human/sara`, so an oracle that "corrects" the source cannot
reach zero mismatches. Grading the intended readings instead would require a
corrected Prolog copy as the parity reference and is a separate contract change,
to be proposed rather than applied silently.

## Amendments accepted 2026-09-22

### P-WIRE: producer release, packaging and counts

Dev approved WIRE including both handling proposals in
`docs/contracts/P_WIRE_DRAFT.md`. Installed release wording and record packaging
are in `docs/contracts/PARITY.md`; `Interface/WIRE.md` fixes the shared byte
contract. The concrete input codec remains builder work: fix its lossless field
spelling and shared fixtures once in Interface before either isolated producer
uses it. Fields not determined by H1–H4, G4, D1/V9, M1, H6.1/H6.2/H6.5 and
their referenced G1/A3 rules remain blocked for an owner decision.

One record is a household/target/bound-argument tuple in the approved mode.
Report record, distinct-household and original-case counts separately in run
summaries, freeze manifests and coverage reports. ≥10k refers to records, not
necessarily distinct households. H6.3 case scoring, all 376 originals,
≥20 hits per arm and B003's admitted-mutant denominator remain unchanged.
No mode, projection or observation canonicalization is redefined.

### P-R5CYCLE: Option A with coverage and generator conditions

Dev selected A from `docs/contracts/P_R5CYCLE_OPTIONS_DRAFT.md`, including its
all-201-years scope and zero-exclusion audit, with two explicit conditions:
close the query-year coverage gap in Interface before any R5-group termination
proof is claimed, and have gen never mint multibirth persons, multi-date births
or same-birthday eligible pairs. Same-birthday eligible dependent pairs are an
accepted, stated limitation of the graded domain. The all-years restriction
also excludes a household if a violating pair is eligible in another admitted
year; unrelated equal birthdays remain allowed.

Install the new H5 conjunct in both Valid and ValidStip, not only V1. The exact
protected amendment is staged in `docs/contracts/DECISIONS_R5_A_AMENDMENT.md`
and was installed/re-pinned by Dev at `0a2a65a`; human remains read-only to the
builder. The executable
uniqueness/decrease checks and required universal-decrease dependency are in
Interface. A required instance with no default prevents omission, not a false
implementation: prove the decider true iff the original K/c3 quantified condition
holds, including wildcard stipulations. Neither a finite ground-pair enumeration
nor conservative false-on-unknown is a substitute. This representation correction
(A-014) changes no domain; real decider correctness and production V7/V8 remain
obligations.

All root/query/stipulation years and R8 Workdays must be tied to their actual
source arguments at the shared checked-year boundary. Constructor failure is a
reported coverage/domain failure, never a normal reference answer. Every
admitted operational call must be proved covered, and unbound-year/E2 paths
accounted for. No complete wrapper coverage or R5/R8 theorem is claimed by this
installation. The re-derived N+1 branch-depth proposal needs universe, phase,
mode and adequacy proofs; the old V10 and 2·persons+2 stay withdrawn. Exhaustion
cannot stand in as a reference value. The generator contract is installed, but
the generator itself belongs to Phase 2 and does not exist yet.

**Neither A nor WIRE signs off Checkpoint 1.** All existing parity, hazard
review and explicit owner sign-off requirements remain intact.

## Design-flaw stop-and-report standard

When a design flaw is discovered, halt the affected development and record the
evidence, consequence, and needed decision under `STATE.md` → `Blockers`.
Report it to the user before implementing a revised design. Do not silently
change the experiment, comparison, input population, or semantic interpretation.
The mutation-admission review that led to B003 is the standard to follow.
