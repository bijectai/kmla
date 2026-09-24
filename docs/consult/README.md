# Governor consult channel

Under PROPOSED P-ROLES, Claude Code sessions build; Astra is the governor and
design authority. This routing takes effect only after Dev accepts and merges
the roles branch. `FABLE_PROMPT.md` is unchanged historical rationale, not a
live prompt/import. No model is launched by this channel and no phase,
contract installation or checkpoint is authorized by it.

## Questions

Use `Q-001.md` onward, with three zero-padded digits, never reused. Check all
existing Q and A files and their Git history before allocating the next number;
a deleted file does not free its number. Preserve published questions. Polling
the same Q is not reusing its number for another question. Each Q includes:

```markdown
# Q-NNN

## Phase
The phase or infrastructure task.

## Lane
oracle | serializer | gen | gate | mutate | invariants | eval | infra

## Question
The specific doubt or decision needed.

## What was tried
Commands, evidence, failures, and relevant prior consultations.

## Files involved
Repository-relative paths and useful line numbers.

## Proposed answer
A proposal for review, or None. Never present it as the governor's answer.
```

From the repository root:

```sh
bash scripts/consult.sh docs/consult/Q-NNN.md
```

The executable script also works by its full path from another directory with
the same repo-relative argument. It validates the path, three-digit positive
number, nonempty regular Q file, safe directories and answer path. It does not
allocate numbers, infer authorship, enforce Git history or decide semantics;
the author/reviewer must enforce never-reuse and no-self-answer rules.

If A is absent, it reports **awaiting the governor**, exits **1**, and the
affected lane halts. Notify Dev/the governor with the Q path. This is a manual,
event-driven handoff, not an automatic notification, background poller or
subprocess consultation. Never launch Claude to answer a builder's Q.

Once the governor has written/sealed A, the same command prints it unchanged
and exits **0**. Delivery is not approval: read the escalation/contract fields
before proceeding. Invalid input, symlinks, empty or non-regular answers exit
**2** with a stderr diagnostic. No retry, answer generation, permission change,
session save or other repository write occurs in the script.

## Answers

Only the governor writes `A-NNN.md`. No one answers their own Q, including
historical questions they authored as builder; obtain independent review
through Dev in that situation. Each answer includes:

- Answer.
- Rationale.
- Contract change: yes/no. If yes, append the proposed change to
  `docs/DECISION_LOG.md`; do not apply it without required owner approval.
- Escalate to Dev: yes/no.
- A final one-line self-review naming assumptions Dev should verify.

The governor removes the completed A's write bits once, then it is sealed
read-only. Never edit, delete, replace or reuse an A. Retrieval leaves bytes
and permissions alone. Disagreement/correction is a new Q referencing the old A.
An incomplete delivered answer remains preserved and requires follow-up, not
repair in place. If escalation is yes, the builder halts that lane and records
the reason under `STATE.md` → `Blockers`.

## Scope, isolation and audits

Consult delivery may create/seal only the new A and append to DECISION_LOG.
Separate governor reviews live in docs/reviews/ with their audience/lane labeled.
Audit changed paths after each script call (expected changes: none) and each
answer-delivery interval. Coordinate quiescence for attributable before/after
checks; any out-of-scope write stops the lane. No per-question permission is
needed inside the standing scope. Contract amendments, installations under
human/, re-pins and checkpoint sign-offs remain Dev's.

The governor may see both lanes to review them but may not relay either
implementation to the other. Questions, excerpts, answers and review notes
must respect that boundary. DECISIONS/Interface supply shared semantics;
opaque outputs and verbatim mismatches are not permission to share source.

## Failure handling and historical channel

Three failed edit cycles on one check means stop and report; no fourth
attempt and no weakened check. Repeated exit 1 while awaiting A is expected
queue state, not a failed implementation edit cycle.

The old Claude subprocess, --resume, JSON session_id, tool flags and locks are
retired. Existing ignored .fable_session/lock files are left untouched and are
not consumed. Dev's FABLE_PROMPT remains history and is not a precondition of
the queue. No CLI failure breaker or fallback spawn is part of this script.

`scripts/test_consult.py` tests awaiting/delivery, numbering/path rejection,
symlinks, repeat reads, exact file preservation and absence of spawning.
Obsolete spawn/resume/JSON/tool-boundary tests were removed, not skipped; their
original behavior and verification remain in Git and `SMOKE_TEST.md`.

Historical Q-001/002 tested B003 and context persistence; A-003 corrected two
overstatements in A-001 without editing it. A-004's Dev-relayed semantic body
is `DECISIONS_RECOMMENDED.md`. These historical artifacts and prior A-files
remain unchanged; none reactivates the old roles or overrides accepted contracts.
