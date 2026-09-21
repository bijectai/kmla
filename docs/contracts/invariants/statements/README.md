# Human-approved invariant contract

Owner promotion target: `human/invariants/statements/`.

Each file imports its section interface and defines a proposition parameterized
by the implementation with `def`, as in the approved example:

```lean
import Interface.S151
def S151_nonneg (impl : Household → Year → Int) : Prop :=
  ∀ h y, Valid h → 0 ≤ impl h y
```

The human must choose and endorse the actual claims. Proposed candidates belong
in root `invariants/candidates/`; endorsement is not inferred from a sample.
Oracle proofs belong in root `invariants/proofs/`, with a theorem applying the
exact claim to the oracle implementation.

For the model, a failed proof attempt is `PARTIAL`. `REFUTED` requires a
kernel-checked proof of the negated claim with a concrete witness. Candidate
witnesses may be searched over quantified variables or taken from the frozen
corpus. A checked violation takes precedence over unproved goals. Nothing may
weaken the signed claim. See `docs/PROTOCOL.md` for the approved requirements.
