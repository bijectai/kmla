# Hygiene gate contract

Draft for owner review. `docs/PLAN.md` §2.4 specifies what the gate must *check*;
nothing anywhere specified how it is *invoked* or what it *prints*. Three
documents require the gate to "reject every file and print a reason" without
defining a stream, an exit code, a format, or a vocabulary of reasons, so
"every exploit rejected" has not been a measurable claim. This document fixes
that interface so the owner's exploit suite drops in without renegotiation.

`gate/check.py` does not exist yet. Per `docs/PLAN.md` §2.4 it is written from
this spec **without reading `human/gate/exploits/`**, and only then run against
that directory.

## Invocation

```text
python3 gate/check.py [--json] [--helpers DIR] PATH...
```

Each `PATH` is one `.lean` file to judge. Directories are not expanded: the
caller enumerates files, so the set under test is always explicit and a file
added to a directory cannot silently change a result.

## Exit status

| Exit | Meaning |
| ---: | --- |
| 0 | Every path was judged and every one was ACCEPTED |
| 1 | Every path was judged and at least one was REJECTED |
| 2 | The gate could not judge some path: toolchain missing, timeout, unreadable file, bad arguments |

Exit 2 is an infrastructure failure and is never a verdict. A crash must be
trapped and re-reported as exit 2; an uncaught Python traceback exits 1, which
would be indistinguishable from an honest rejection.

## Report

One line per path on **stdout**, in the order given:

```text
<path>\t<ACCEPTED|REJECTED>\t<reason-code>\t<human-readable detail>
```

`reason-code` is `-` for ACCEPTED. `--json` emits one JSON object per line with
the keys `path`, `verdict`, `reason_code`, `detail`. Diagnostics from the Lean
toolchain go to **stderr** and never to stdout, so the report is machine-readable
even when a compile fails.

A file is rejected for the **first** violated rule in the order listed below, so
a verdict is deterministic and a reason code is reproducible.

## Reason codes

This closed vocabulary is what an owner sidecar may name. Adding a code is a
contract change.

| Code | Rejects |
| --- | --- |
| `compile-error` | Does not compile on the pinned toolchain |
| `sorry` | Contains `sorry` or a `sorryAx` in the axiom set of any declaration |
| `axiom-not-whitelisted` | `#print axioms` on a declaration names an axiom outside the `DECISIONS.md` whitelist |
| `banned-native-decide` | Uses `native_decide` |
| `banned-implemented-by` | Uses `@[implemented_by]` |
| `banned-extern` | Uses `@[extern]` |
| `banned-unsafe` | Declares `unsafe` |
| `banned-partial` | Declares `partial` |
| `banned-opaque` | Declares `opaque`, or a body the kernel cannot unfold |
| `banned-set-option` | Sets an option that disables or weakens checking |
| `import-outside-whitelist` | Imports anything outside `Interface/` and `Oracle/` |
| `parse-error` | Is not well-formed Lean (distinct from `compile-error`) |

The whitelist itself lives in the owner's `DECISIONS.md`; `docs/PLAN.md` §4.1
proposes `propext`, `Quot.sound`, `Classical.choice`. The gate reads it rather
than hard-coding it, so tightening the whitelist does not require a gate change.

## Helper files

`docs/PLAN.md` §95 requires an exploit that smuggles an axiom **through a helper
file**, and `docs/PLAN.md` §93 requires the gate to reject imports outside
`Interface/` and `Oracle/`. As written these collide: a helper sitting in
`human/gate/exploits/` is outside both, so the import rule fires before the axiom
check ever runs, and the staged convention's "reject every `.lean` file in the
directory" scores the helper itself as a failed exploit.

Resolution: helpers live in `human/gate/exploits/helpers/`. Files there are
**support material, not cases**. The validation run enumerates only the `.lean`
files directly in `human/gate/exploits/`, and passes `--helpers` so the gate can
resolve the import closure without treating the helper as a subject.

This does **not** exempt helpers from the rules. The import-whitelist check still
fires on an exploit that imports one — and that is the point. See the next
section for why that is still a useful exploit.

## Expected-reason sidecars

`<basename>.EXPECTED.txt`, where `<basename>` is the exploit filename **with the
`.lean` extension removed**: `axiom_smuggle.lean` pairs with
`axiom_smuggle.EXPECTED.txt`. (The protected
`human/gate/exploits/README.md` currently says this naming "remains to be
defined", and POSIX `basename` would also admit `axiom_smuggle.lean.EXPECTED.txt`;
this pins the shorter form.)

The sidecar's first line is a reason code from the table above. Remaining lines
are notes for humans and are not matched.

Validation of the suite has **three** outcomes per file, not two:

| Outcome | Condition |
| --- | --- |
| `PASS` | REJECTED, and the reason code equals the sidecar's (or no sidecar exists) |
| `WRONG-REASON` | REJECTED, but with a different code than the sidecar names |
| `FAIL` | ACCEPTED — the gate did not catch it |

`WRONG-REASON` is reported, never silently counted as a pass. The axiom-smuggling
exploit is exactly where this matters: if the owner expects
`axiom-not-whitelisted` and the gate answers `import-outside-whitelist`, the file
was caught by the perimeter rather than by the check it was written to probe, and
the axiom check remains untested. That is a finding about gate coverage, and the
distinction is invisible to a two-outcome scheme.

A Checkpoint 2 gate of "every exploit rejected" is satisfied by zero `FAIL`.
Whether it should also require zero `WRONG-REASON` is an owner decision.

## Toolchain

The gate compiles on the toolchain pinned by the repository's `lean-toolchain`.
It reads that file rather than invoking a default, because a bare `lean` or
`lake` invocation resolves the elan default and will download a different
toolchain. The gate fails with exit 2, never a verdict, if the pinned toolchain
is not installed.

## What the owner must still decide

1. The axiom whitelist, in `DECISIONS.md`. `docs/PLAN.md` §4.1's three entries are
   a proposal, not a signed decision.
2. Whether Checkpoint 2 requires zero `WRONG-REASON` as well as zero `FAIL`.
3. Which Lean toolchain to pin. `lean-toolchain` currently proposes the version
   the `Interface/Household.lean` draft was checked with; the owner owns that pin.
4. Whether the `--helpers` resolution above is the intended reading of
   `docs/PLAN.md` §95, or whether the axiom-smuggling exploit should instead place
   its helper inside `Interface/` to bypass the import rule and reach the axiom
   check directly. That choice determines what the exploit actually tests.
