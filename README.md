# KMLA

Kernel-checked, Mutation-validated Lean Autoformalization.

Phase 0 drafts are ready for review. The canonical JHU archive is installed and
verified. Semantic finalization is paused on source findings recorded in
`STATE.md`; implementation and evaluation await the human Checkpoint 0.

```text
kmla/
  human/                    Human-owned inputs; submodule setup pending
    sara/                   Source archive, hash sidecar, and extracted sara/
    DECISIONS.md            Semantic decisions to fill in
    parity/                 Independent check.py belongs here
    gate/exploits/          Human-written adversarial Lean files
    invariants/statements/  Human-approved invariant claims
    HASHES.txt              Hash manifest to populate
  Oracle/                   Per-section Lean reference implementations
  Interface/                Shared types and target signatures
  harness/                  Prolog runner, serializer, Lean runner
  gen/                      Boundary/random generators and coverage
    out/                    Generated inputs
  gate/                     Hygiene checker
  mutate/                   Mutation operators and runner
    witnesses/              Admission witnesses, isolated from grading inputs
  invariants/
    candidates/             Proposed invariants awaiting human approval
    proofs/                 Proofs of approved invariants
  eval/                     Grader, model runner, counterfactuals, reports
    cf_prolog/              Edited Prolog copies for counterfactuals
  docs/
    PLAN.md                 Original build plan
    PROTOCOL.md             User-approved amendments
    contracts/              Drafts for human review and promotion
    HANDOFF.md              Required inputs and outstanding decisions
  STATE.md                  Progress and blockers
```

Start with the [Phase 0 handoff](docs/HANDOFF.md) and
[staged contracts](docs/contracts/README.md). `.gitkeep` files preserve otherwise
empty directories in Git. The staged parity script is an exit-2 placeholder,
not an implemented comparator.

`human/` contains the supplied corpus but is not yet a configured submodule or
an enforced read-only mount. The assistant treats it as strictly read-only;
the human owner installs approved drafts and pins hashes. Submodule setup and
runtime enforcement remain pending.

Source provenance, the archive digest, and the verified 376-case inventory are
recorded in [SOURCE.md](docs/contracts/SOURCE.md). The approved mutation and
invariant contracts and the design-flaw stop-and-report standard are recorded
in [PROTOCOL.md](docs/PROTOCOL.md).
