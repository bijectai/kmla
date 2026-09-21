# Human-owned inputs

This directory was created as a layout-only placeholder at your request.
It is not yet a Git submodule, hash-pinned, or mounted read-only.

Add the designated source corpus under `sara/`, record your semantic decisions
in `DECISIONS.md`, and supply the independent artifacts in the directories below.
Preserve the original corpus layout and provenance.

- `sara/`: original Prolog statutes and the designated 376 cases.
- `DECISIONS.md`: your decisions using the supplied section headings.
- `parity/check.py`: your independent output comparator; currently absent.
- `gate/exploits/`: your adversarial Lean cases, authored before gate validation.
- `invariants/statements/`: claims you approve for proof and grading.
- `HASHES.txt`: actual artifact hashes after the manifest contract is settled.

The decision template and hash placeholder are incomplete and confer no approval.
See [the handoff](../docs/HANDOFF.md) for the contracts still to be finalized.
Supply the intended submodule repository and pinned revision before enforcement
is configured. Keep any information added here when setting up that submodule.
