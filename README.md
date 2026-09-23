# KMLA

**Kernel-checked, Mutation-validated Lean Autoformalization.**

KMLA is a benchmark for one question: when a model turns a natural-language
statute into Lean, is the Lean *right*? It answers without an LLM judge and
without human raters. A formalization is graded against a Lean oracle that is
itself checked, input by input, against an independent executable reference —
and the differential check at the heart of the grader is validated by mutation
testing before it grades anything. The first target is United States tax law,
using the SARA dataset.

## The problem

"It compiles" is not "it is correct." A Lean file can type-check and still
encode the wrong threshold, the wrong rounding, or the wrong reading of
"during the taxable year." The usual ways of checking are weak in specific
ways: an LLM judge grades a model with a model, and its errors correlate with
the model's; human raters do not scale to thousands of inputs per section and
do not give reproducible numbers; and a hand-written reference encodes one
reading of the statute and is only as tested as its author's own suite.

KMLA replaces judgement with computation wherever it can. Where it cannot — the
reading of the reference's own semantics — the judgement is written down once,
site by site, in an owner-signed file, and pinned.

## How a formalization is graded

This is the grading protocol as specified in `docs/PLAN.md` and
`docs/PROTOCOL.md`.

For each statute section, a model is given the statute text and a fixed Lean
interface — the shared `Household` input type, a `Valid` predicate, and the
target signatures it must implement, one per predicate the SARA cases query
plus a per-section entry point — and asked, under a fixed prompt with one
attempt and up to three compiler-feedback retries, for definitions. The result
is run through four checks, in order, and receives one verdict.

1. **Hygiene gate.** The file must compile on the pinned toolchain with no
   `sorry`, no axioms outside a short whitelist, no `native_decide`,
   `implemented_by`, `extern`, `unsafe`, `partial`, opaque bodies, or
   check-disabling options, and no imports beyond `Interface/` and `Oracle/`.
   Anything else is **INVALID**. The gate must reject every file in an
   owner-written exploit suite that its developer never sees while building it.
2. **Equivalence proof.** The grader attempts a kernel-checked proof that the
   model's definition equals the oracle's on every valid input, with a fixed
   tactic set and time budget. Success is **PROVED-EQUIV**.
3. **Differential testing.** The model and the oracle are run on a frozen,
   hash-pinned corpus of generated inputs — boundary values around every
   numeric literal and date in the statute, plus adversarial random households.
   Any disagreement is **REFUTED**, with the first witness recorded.
4. **Invariants.** Each owner-signed invariant of the section that has been
   proved of the oracle (non-negativity, monotonicity in income,
   exception-dominates-base, and so on) is instantiated with the model's
   definition. A kernel-checked counterexample is **REFUTED**; an unproved goal
   is **PARTIAL**; otherwise **CONSISTENT**. Signed statements the oracle proof
   could not close are reported, not graded.

A REFUTED verdict always carries a concrete witness — a corpus input on which
model and oracle disagree, or a kernel-checked counterexample to a signed
invariant. INVALID carries the gate's stated reason; PARTIAL names the
statement the fixed tactics could not close. Nothing is a score out of ten.

## How the grader is validated

A grader that cannot catch wrong formalizations is worthless, so KMLA measures
its own recall before reporting anything.

**Mutation testing.** The oracle is systematically broken — comparators
flipped, constants perturbed by ±1 and by one unit, match arms deleted,
adjacent arms swapped, guards negated, negation-as-failure checks replaced by
`true` — and each admitted mutant is run through the differential check on the
frozen corpus. A mutant is *admitted* only if it compiles, passes the gate, and
a white-box witness search proves it actually differs from the oracle on some
input; mutants with no found witness are reported as unresolved and excluded,
never counted as equivalent. The differential check must refute at least 95%
of admitted mutants per section. A surviving mutant is not a failure to be
tuned away: it is a blind spot in the input corpus, reported as a finding and
used to name the missing input mode.

**Counterfactuals.** To separate formalization from memorization, each section
is also evaluated on variants where one threshold, rate, or date has been
consistently edited in both the statute text and the oracle. A variant is kept
only if the edit changes the oracle's output on at least 5% of the corpus;
boundary inputs are regenerated around the new value, and the edited oracle is
itself re-checked by parity against a correspondingly edited copy of the
Prolog. A model that reproduces the original statute from memory is therefore
refuted on the variant.

**Parity.** Before any grading, the oracle is checked against the executable
reference on the original 376 SARA cases and on the generated corpus, using a
comparison meter written by the project owner before any oracle existed, whose
source the builder never reads and only invokes. Zero mismatches is the
precondition for everything above.

## Independence, and why the numbers mean something

The credibility of a benchmark like this rests on the things it checks *with*
being independent of the things it checks. KMLA makes that a mechanical check
rather than a matter of good intentions.

Four artifacts are owned by a human and are never written or edited by the
automated builder that constructs everything else. Two of them — the meter and
the exploits — are not even read by it: the builder invokes the meter only
through its command line, and runs the finished gate against the exploits only
after the gate is built.

| Artifact | Why it cannot be delegated |
| --- | --- |
| `human/DECISIONS.md` | The semantics of the reference — every negation, cut, aggregate, rounding rule, and date convention, decided site by site. The builder reads it as its specification; no test can confirm an interpretation. |
| `human/parity/check.py` | The meter the oracle is measured with. If the builder wrote it, zero mismatches would mean the oracle agreeing with itself. |
| `human/gate/exploits/` | The attacks the hygiene gate must survive. A gate validated against its own author's imagination proves nothing. |
| `human/invariants/statements/` | The claims worth proving. The builder proves them of the oracle; nothing is graded that the owner did not sign. |

Every protected file under `human/` is hash-pinned in a manifest (which cannot
list itself) that CI verifies, and a pull request that touches `human/` fails
CI unless the owner applies the `owner-human-update` label. The oracle
translator and the input generators and serializer are built in separate
contexts that share only `DECISIONS.md` and `Interface/`, so parity between
them is meaningful. When a design flaw is found, the affected work halts and
the flaw is recorded and reported; it is never resolved by weakening a
comparison, filtering an input, or reinterpreting a clause to make a check
pass.

Claims are stated as **"consistent with a verified reference"**, never
"faithful to the statute." Where the reference itself diverges from the
statute's evident intent, the oracle reproduces the reference as written and the
divergence is published as a finding.

## The reference: SARA

[SARA](https://nlp.jhu.edu/law/sara/) (Statutory Reasoning Assessment, Johns
Hopkins University) encodes nine sections of the Internal Revenue Code — §§ 1,
2, 63, 68, 151, 152, 3301, 3306 and 7703 — as Prolog programs, with 376 cases:
276 entailment questions and 100 numerical tax computations, each with its
expected answer encoded as a test directive. KMLA uses the Prolog as its
executable reference.

Two properties of the reference are load-bearing and are pinned rather than
assumed. It is executed only on SWI-Prolog 7.2.3, the version SARA specifies,
in a Docker image whose identity — base image digest, package closure,
Dockerfile hash, and timezone — is recorded; SWI-Prolog 9.2.9 fails 64 of the
376 cases on `rdiv/2` alone. And the timezone is part of that identity: all
376 case directives succeed (two of them vacuously, because those cases contain
no test) only in a negative-offset time zone, because a date offset in the
reference's utilities cancels there; under UTC two cases fail.
`America/New_York` is the pinned zone.

Defects found in the reference are documented, not repaired. The corpus is
redistributed byte for byte under its own licence.

## Repository layout

Directories are listed by the role they hold in the design. Which of them are
populated at any moment is recorded in `STATE.md`, not here.

```text
kmla/
  human/                    Owner-owned, hash-pinned, read-only to the builder
    sara/                   The SARA archive, digest sidecar, and extracted corpus
    DECISIONS.md            The semantic specification the oracle is built from
    parity/check.py         The independent comparison meter
    gate/exploits/          Where the owner's adversarial Lean files go
    invariants/statements/  Where the owner's signed invariant claims go
    HASHES.txt              Manifest covering every protected file
  Interface/                Shared types, Valid, and the query-time and wire schemas
  Oracle/                   Home of the Lean reference translations, one per section
  harness/                  Pinned Prolog runtime, corpus runner, and case reader
  gen/                      Home of the input generators; out/ holds the frozen corpus
  gate/                     Home of the hygiene checker
  mutate/                   Home of the mutation operators and admission runner
  invariants/               Mined candidates and proofs of signed statements
  eval/                     Home of the grader, model runner, counterfactuals, reports
  docs/
    PLAN.md                 The build plan, preserved as written
    PROTOCOL.md             Owner-approved amendments; supersedes PLAN where they conflict
    DECISION_LOG.md         Every proposed and accepted contract change, with reasoning
    contracts/              Parity, gate, runtime, manifest and shared-input contracts; source findings
  scripts/                  Verification tooling: manifest, inventories, conformance
  NOTICE.md                 Attribution and licence obligations
```

## Reproducing

The Python tooling is standard-library only and writes nothing into the
repository. The two harness commands need Docker and write their records to
the path given by `--out`; the Lean check needs `elan` and the pinned toolchain.

```sh
python3 -B scripts/human_manifest.py verify                 # every protected file matches its digest
python3 -B scripts/inventory_cases.py --summary             # structural inventory of the 376 cases
KMLA_TZ=America/New_York bash harness/pin_runtime.sh --out RUN/RUNTIME.json
                                                            # build and record the pinned interpreter
bash harness/run_corpus.sh --runtime RUN/RUNTIME.json --out RUN/BASELINE.json
                                                            # run all 376 cases against that record
bash scripts/check_interface.sh                             # type-check Interface/Household.lean and run its guards
bash scripts/verify_phase0.sh                               # Checkpoint 0 mechanical acceptance checks
```

The Lean toolchain is pinned by `lean-toolchain`; a bare `lean` invocation
outside this repository will download a different version.

## Documents

- [`docs/PLAN.md`](docs/PLAN.md) — the design, the build sequence, and the
  ownership model.
- [`docs/PROTOCOL.md`](docs/PROTOCOL.md) — approved amendments, including the
  mutation-admission rules, the invariant contract, and the stop-and-report
  standard.
- [`human/DECISIONS.md`](human/DECISIONS.md) — the semantic specification:
  what every construct in the reference means in Lean.
- [`docs/DECISION_LOG.md`](docs/DECISION_LOG.md) — how each decision was
  reached.
- [`docs/contracts/`](docs/contracts/) — the parity, gate, runtime, and hash
  contracts, and the source findings.

Where the build currently stands is in [`STATE.md`](STATE.md) and
[`docs/HANDOFF.md`](docs/HANDOFF.md), not here.

## Attribution

SARA is the work of its authors at Johns Hopkins University
(<https://nlp.jhu.edu/law/sara/>), © 2020 Nils Holzenberger, redistributed here
unmodified under its own licence. Its copyright and permission notice must be
included in all copies — `human/sara/sara/LICENSE` travels with the corpus and is
hash-pinned. See [NOTICE.md](NOTICE.md) for the full attribution, the archive
digest, and what this project did and did not change.
