KMLA build plan
KMLA: Kernel-checked, Mutation-validated Lean Autoformalization. Evaluated first on SARA statutory tax law. Grades NL statute → Lean formalizations with no LLM judge and no human raters, against a borrowed oracle, with the grader itself validated by mutation.
Tags used throughout: [YOU] means you build or validate it, and Astra may not touch it. [ASTRA] means Astra owns it end to end. [CONTRACT] means Astra designs the interface so your piece drops in.
1. Ownership model
The benchmark's credibility rests on four artifacts being independent of the code they check. Everything else is delegable.
Artifact	Owner	Why it can't be delegated
DECISIONS.md	[YOU]	Interpretation of SARA semantics. No test can confirm it.
parity/check.py	[YOU]	The meter for the oracle. If Astra writes it, zero mismatches means self-agreement.
gate/exploits/	[YOU]	Adversarial imagination against the hygiene gate.
invariants/statements/	[YOU]	The claims Lean is for. Proofs are Astra's; statements are yours.
Plus four checkpoints, one per week, where you read the meters and diffs. Everything else is Astra's, roughly 70% of the calendar.
2. Enforcement mechanics
Prompts don't hold for a month. Files do.
* Filesystem. sara/, parity/, gate/exploits/, invariants/statements/, DECISIONS.md are in a human/ git submodule Astra's runner mounts read-only.
* CI. human/HASHES.txt pins every file. CI fails on any drift. Astra cannot merge a PR that touches human/.
* Isolation. The oracle translator and the generator/serializer subagents run in separate contexts. The orchestrator passes them only DECISIONS.md and Interface/, never each other's code. Parity is meaningful only if both sides are written blind.
* Stop conditions. Any subagent that cannot pass a check without editing human/ writes the blocker to STATE.md and halts. Astra never resolves a blocker by weakening a comparison, filtering inputs, or reinterpreting a Prolog clause.
* Stop-before-push. Astra opens PRs. You merge.
3. Repo layout
kmla/
  human/                    [YOU]  read-only submodule, hash-pinned
    sara/                   original Prolog statutes + 376 cases
    DECISIONS.md            semantics decisions (schema in §4.1)
    parity/check.py         parity meter (contract in §4.2)
    gate/exploits/          adversarial Lean files (contract in §4.3)
    invariants/statements/  invariant .lean statements (contract in §4.4)
    HASHES.txt
  Oracle/                   [ASTRA] one file per section
  Interface/                [ASTRA] shared types + target signatures
  harness/                  [ASTRA] swipl runner, serializer, lean runner
  gen/                      [ASTRA] boundary/random generators, coverage
  gate/check.py             [ASTRA] hygiene gate
  mutate/                   [ASTRA] operators, validity filter, runner
  invariants/proofs/        [ASTRA] proofs of human-written statements
  eval/                     [ASTRA] grader, model runner, counterfactuals, reports
  docs/HANDOFF.md           [ASTRA] what it needs from you, per phase
  STATE.md                  [ASTRA] session chain
4. Contracts [CONTRACT]
Astra's first job is to write these contracts as stubs plus a docs/HANDOFF.md so your pieces drop in without renegotiation. You implement to the contract. Astra builds against the stub.
4.1 DECISIONS.md schema
Astra generates a template with these sections filled with TODO and the grep results pre-populated. You fill the decisions.
## Money        representation, rounding rule, worked examples
## Dates        epoch, interval semantics per predicate
## Household    single shared type, field list
## NAF          every `\+` in sara/, file:line, intended translation
## Cut          every `!` in sara/, file:line, intended ordering
## Aggregates   every findall/sumlist, duplicate + order semantics
## Recursion    termination strategy per recursive predicate
## Axioms       whitelist: propext, Quot.sound, Classical.choice
Astra reads this file as spec. Any translation decision not covered here is a blocker, not a guess.
4.2 parity/check.py CLI contract
parity/check.py --section N --inputs DIR --prolog-out DIR --lean-out DIR
exit 0  → zero mismatches
exit 1  → mismatches; writes mismatches.jsonl {input_id, prolog, lean}
Astra's harness produces --prolog-out and --lean-out as one JSON per input id, same schema. Astra never reads check.py source. It only calls it.
4.3 gate/exploits/ convention
One .lean file per bypass, name describes the attack. Optional EXPECTED.txt per file with the rejection reason. Astra's gate/check.py must reject every file and print a reason. Astra never reads the directory contents during gate development, only runs the gate against it after.
4.4 invariants/statements/ format
-- S151_nonneg.lean
import Interface.S151
theorem S151_nonneg (impl : Household → Year → Int) : Prop :=
  ∀ h y, Valid h → 0 ≤ impl h y
Statements are parameterized over impl so the same file is instantiated with the oracle (Astra proves it) and with each model output (grader attempts it). Astra's miner proposes candidates to invariants/candidates/. You promote the ones you endorse into statements/, edited as needed. Nothing gets graded that you didn't sign.
5. Astra orchestrator prompt
Give this once, at the start.
You are building KMLA per docs/PLAN.md. Rules that override everything else: (1) human/ is read-only; never propose edits to it, never work around it. (2) Spawn the oracle translator and the generator/serializer as separate subagents with no shared context; pass each only human/DECISIONS.md and Interface/. (3) Never weaken a comparison, filter an input, or reinterpret a Prolog clause to make a check pass. Report survivors, mismatches, and unproved goals as findings. (4) On any blocker requiring human/ changes, write it to STATE.md under ## Blockers and halt that lane. (5) Open PRs; never merge. (6) Before each phase, update docs/HANDOFF.md with exactly what the human must deliver, in the contract format from §4. (7) Every subagent prompt ends with a self-review listing its assumptions about Prolog semantics, and a circuit breaker: three failed edit cycles on one test means stop and report.
6. Phases
Week 0: contracts and decisions
[ASTRA] Phase 0.1: scaffold and contracts.
Create the repo layout in §3. Generate human/DECISIONS.md as a template per §4.1 with every \+, !, findall, sumlist, is, and date comparison in sara/statutes/ listed with file:line. Generate Interface/Household.lean as a draft type from the fact predicates in sara/, marked DRAFT pending DECISIONS.md. Write stubs for parity/check.py (§4.2, exits 2 "unimplemented"), gate/exploits/README.md (§4.3), invariants/statements/README.md (§4.4). Write docs/HANDOFF.md phase 0 listing what the human must fill. Do not translate any Lean yet.
[YOU] Checkpoint 0 (one day).
* Fill DECISIONS.md. Every listed hazard gets an explicit translation.
* Review Interface/Household.lean and approve or edit. Money as Int cents, dates as day counts.
* Implement parity/check.py to the §4.2 contract. It's short: load two JSON dirs, compare by id, write mismatches. Keep it dumb on purpose.
* Pin hashes. Commit human/.
Week 1: oracle with parity
[ASTRA] Phase 1.1: harness and serializer (subagent A, GREEN).
Build harness/swipl.py (run a case, return JSON answer) and harness/facts.py (parse SARA cases into Household, emit Prolog facts and a Lean term per Interface/Household.lean). Round-trip must be identity on all 376 cases. Use only predicates present in sara/. You will not see Oracle/.
[ASTRA] Phase 1.2: translate sections (subagent B, RED, Fable-class, one session per section, order §7703, 3306, 3301, 2, 63, 68, 151, 152, 1).
Translate sara/statutes/s{N}.pl to Oracle/S{N}.lean following DECISIONS.md exactly. One Lean definition per Prolog clause, comment citing the clause. Annotate -- NAF, -- CUT, -- AGG where DECISIONS.md applies. No partial, sorry, native_decide. After translating, call harness/ to produce outputs for cases touching this section, then run human/parity/check.py --section {N}. Report mismatches verbatim with the Prolog clause you believe is responsible. Do not fix by changing semantics. You will not see harness/facts.py source.
[YOU] Checkpoint 1 (half day).
* For each section, read the -- NAF, -- CUT, -- AGG annotations against your DECISIONS.md list. Every hazard should appear exactly once.
* Triage mismatches. Expect rounding and NAF. Fix by re-running 1.2 with a clarified DECISIONS.md entry, not by editing Oracle/ yourself, so the decision is recorded.
* Gate: zero mismatches on 376 cases, parity/check.py hash unchanged.
Week 2: inputs, interfaces, gate
[ASTRA] Phase 2.1: generators (subagent A's lane).
Build gen/boundary.py: every numeric literal and date in sara/statutes/ yields k-1, k, k+1 on the relevant field. gen/random.py: schema-valid households with named adversarial modes: absent facts, duplicate facts, deep dependent chains, year-boundary dates, zero and negative-edge incomes. gen/coverage.py: instrument Oracle/ arms, report hits. Generate until every arm ≥ 20 hits, target ≥ 10k inputs, emitted via harness/facts.py.
[ASTRA] Phase 2.2: adversarial parity.
Produce Prolog and Lean outputs for all gen/out/ and run human/parity/check.py per section. Report every mismatch with input, both outputs, suspected clause. Do not edit Oracle/ or gen/ in this session.
[ASTRA] Phase 2.3: per-section interfaces.
For each section create Interface/S{N}.lean: shared types, Valid with Decidable, target signature with sorry body. Cross-section dependencies import Oracle/, never a model file.
[ASTRA] Phase 2.4: hygiene gate (RED).
Build gate/check.py: compiles on the pinned toolchain; no sorry; #print axioms on every declaration ⊆ whitelist in DECISIONS.md; reject native_decide, implemented_by, @[extern], unsafe, partial, opaque bodies, check-disabling set_option, imports outside Interface/ and Oracle/. Build it from the spec above without reading human/gate/exploits/. Then run it against that directory and report any file not rejected.
[YOU] Checkpoint 2 (half day plus exploit writing).
* Write gate/exploits/ before Astra runs 2.4's final check. Minimum: one per banned construct, one axiom smuggled through a helper file, one Decidable instance that lies, one Valid shadowing, one that proves False under a hidden axiom.
* Triage 2.2 mismatches as in Checkpoint 1.
* Gate: zero mismatches on 10k+, every arm covered, every exploit rejected.
Week 3: grader validation
[ASTRA] Phase 3.1: mutation operators.
mutate/ops.py over Oracle/: flip comparators, perturb constants ±1 and ±1 unit, delete match arm, swap adjacent ordered arms, negate guard, replace a NAF check with true. Emit whole-section mutants.
[ASTRA] Phase 3.2: validity filter and kill rate (RED).
mutate/run.py: a mutant counts only if it compiles, passes gate/check.py, and differs from the oracle on ≥ 1 input in gen/out/. Run the differential grader on valid mutants. Report per section: valid, killed, survivors with diffs. Do not modify gen/ or the grader to raise the kill rate. Survivors are findings.
[ASTRA] Phase 3.3: invariant mining.
invariants/mine.py: test templates on oracle outputs over gen/out/: non-negative, bounded by income, monotone in income, monotone in dependents, piecewise linear between thresholds, exception dominates base. Write every template that holds on all inputs to invariants/candidates/ in the §4.4 format. Do not write to statements/.
[YOU] Checkpoint 3a.
* Read candidates/. Promote the ones you'd defend in a paper into human/invariants/statements/, tightened where needed. Drop sampling artifacts. Pin hashes.
* Read mutation survivors. Each one is a generator blind spot: name the missing input mode for Astra.
[ASTRA] Phase 3.4: oracle-side proofs (RED, Fable-class).
For each file in human/invariants/statements/, instantiate with the oracle and prove it in invariants/proofs/, tactics limited to omega, simp, decide, grind, case splits, 5-minute budget each. Unproved: record last goal state in invariants/UNPROVED.md. Never weaken a statement.
[ASTRA] Phase 3.5: grader.
eval/grade.py, conjunctive: (1) gate/check.py → INVALID; (2) attempt ∀ h, Valid h → model h = oracle h, fixed tactic set, 10-minute budget → PROVED-EQUIV; (3) differential on gen/out/ → REFUTED with first witness; (4) each proved statement instantiated with the model's impl, same tactics → refuted REFUTED, unproved PARTIAL; else CONSISTENT. Also record compile yes/no and per-case accuracy on the 376 originals. Sanity: the oracle itself must grade PROVED-EQUIV.
[YOU] Checkpoint 3b.
* Gate: kill rate ≥ 95% per section on valid mutants, ≥ 3 proved statements per section, oracle grades PROVED-EQUIV. Read UNPROVED.md: decide drop or keep-as-unproved (reported, not graded).
Week 4: runs and draft
[ASTRA] Phase 4.1: counterfactuals.
eval/counterfactual.py: per section, consistently edit one threshold, rate, or date in statute text and Oracle/. Accept only if oracle output changes on ≥ 5% of gen/out/. 10 variants per section, each with regenerated boundary inputs, each re-run through parity against a correspondingly edited Prolog copy in eval/cf_prolog/ (not human/sara/).
[ASTRA] Phase 4.2: model runner.
eval/run.py: for each (section, variant, model) send statute text plus Interface/S{N}.lean with a fixed prompt, one attempt plus ≤ 3 compiler-feedback retries, temperature 0 where supported, outputs cached. Models from eval/models.yaml.
[ASTRA] Phase 4.3: reports.
eval/report.py: per model and section: compile rate; verdict distribution; original vs counterfactual gap; headline table: fraction of outputs at 100% per-case accuracy on originals that are REFUTED differentially. First-class tables for grader kill rates, parity counts, and coverage.
[ASTRA] Phase 4.4: related-work draft from a citation list you supply (Kordjamshidi et al. 2026, Lorenzo et al. 2025, VeriBench, DeonticBench, Heydari & Leowald 2026, CertJudge).
[YOU] Checkpoint 4.
* Pick models: 6+, including Goedel-Prover and one other prover-specialized model. Set the budget.
* Write the paper. Claims stay at "consistent with a verified reference," never "faithful to the statute." Kill rates and parity counts go in the body, not an appendix.
7. Gates
Week	Gate	Meter owner
0	DECISIONS.md complete, contracts stubbed, hashes pinned	You
1	0 mismatches / 376 cases	Your check.py
2	0 mismatches / 10k+, full coverage, all exploits rejected	Your check.py, your exploits
3	kill ≥ 95%, ≥ 3 proved statements/section, oracle PROVED-EQUIV	Your statements
4	6+ models, headline table, draft	You
8. Time you actually spend
Week 0: one day. Checkpoints 1 to 3: half a day each, plus exploit writing (a few hours) and invariant promotion (a few hours). Week 4: the paper. Roughly five working days across the month. The rest is Astra's, gated by meters it can't edit.
If week 1 slips past eight days, cut counterfactuals before cutting mutation testing. The validation week is the paper.
I can also put this in a doc or a docs/PLAN.md file for the repo if you want it handed to Astra directly.
