# Governor consult channel

Under P-ROLES, accepted by Dev on 2026-09-24, Claude Code sessions build;
Astra is the governor and design authority. `FABLE_PROMPT.md` is unchanged
historical rationale, not a live prompt/import. `scripts/consult.sh` launches
no model. Under P-WAKE a builder may instead wake the governor for one
registered Q with the separate `scripts/wake_governor.sh` (below). Neither
script authorizes a phase, contract installation or checkpoint.

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
affected lane halts. Wake the governor under P-WAKE (below), or notify
Dev/the governor with the Q path for a manual relay. consult.sh itself is a
manual, event-driven handoff, not an automatic notification, background poller
or subprocess consultation. Never launch Claude to answer a builder's Q.

Once the governor has written/sealed A, the same command prints it unchanged
and exits **0**. Delivery is not approval: read the escalation/contract fields
before proceeding. Invalid input, symlinks, empty or non-regular answers exit
**2** with a stderr diagnostic. No retry, answer generation, permission change,
session save or other repository write occurs in the script.

## Waking the governor (P-WAKE)

Check before consulting: look in `docs/DECISION_LOG.md`, `human/DECISIONS.md`,
`Interface/` and prior A files first; Astra is expensive. Owner-only matters
(installations under human/, re-pins, checkpoint sign-off, merges) go straight
to Dev. A suspected design flaw is halted, recorded under `STATE.md` →
`Blockers`, reported to Dev and sent to the governor as a Q to classify.

From the repository root, once the Q is committed and consult.sh reports it
awaiting (exit 1):

```sh
bash scripts/wake_governor.sh docs/consult/Q-NNN.md
```

Run it on demand, one question at a time, with the Bash tool's
run_in_background option (not `&` or `nohup`); no polling, schedulers, hooks
or standing automation. Manual relay through Dev remains the fallback. Tell Dev
in one line when a wake starts; before the first live wake, show Dev the exact
command and wait for Dev's go. If the Bash tool is sandboxed, ask Dev before
running the wake unsandboxed. Until the completion notification arrives, run
only read-only commands; while `$STATE/lock` exists no other builder session in
this checkout writes. The refs, stash and worktree checks cover the whole
repository, so any commit, branch, stash, fetch or worktree change anywhere in
it during a wake (including by Dev's own tools) also ends in exit 3.

Configuration comes from `KMLA_GOVERNOR_THREAD`, `KMLA_GOVERNOR_MODEL` and
`KMLA_GOVERNOR_EFFORT` in the environment, else from `KEY=VALUE` lines in
`$STATE/config` (parsed, never sourced), where
`STATE=${KMLA_GOVERNOR_STATE:-$HOME/.kmla-governor}` lies outside the
repository. There is no default model: a missing or malformed value exits 2.

Refusals exit 4 with a one-line reason and wake nothing: a `$STATE/HALT` exists
(only Dev clears it); `$STATE/lock` is held (a run never removes a lock it did
not create); `git status --porcelain -uall` is not empty; the A already exists
(sealed: read it with consult.sh; unsealed: do not read or act on it, report to
Dev); or `lsof -t` shows another Codex process holding Astra's thread lock
under `${CODEX_HOME:-$HOME/.codex}/thread-writer-locks/` (ask Dev to close
Astra's thread in the ChatGPT app). The script never kills, signals or unlocks
anything except its own Codex child and that child's process group. Invalid Q
paths exit 2, exactly as consult.sh rejects them.

The script snapshots HEAD, refs, the stash list, the worktree list and a digest
of the names and modes under `human/`, keeping the snapshot in its lock
directory under `$STATE`, outside the checkout, `$TMPDIR` and `/tmp`, which
Codex's workspace-write sandbox can write by default. It then runs the
fixed `codex exec resume` command and message recorded in the P-WAKE
decision-log entry, from the repository root under `timeout 2h`, with stdin
from `/dev/null` and `PYTHONDONTWRITEBYTECODE=1`. Codex's stdout and stderr go
only to `$STATE/logs/Q-NNN-<UTC timestamp>.log`. When Codex exits, the script
stops anything left in its process group, then audits the checkout. The only
allowed changes are the new A, sealed (regular, nonempty, not a symlink, no
write bits), and new `| ` rows at the end of the `docs/DECISION_LOG.md` Status
index table plus bytes appended at the end of that file. The verdict lists
paths and counts, never contents, with the Codex version and the log path; a
change under `human/` is reported only as "human/ changed".

Ignored paths are judged by the ignore rules in force before the wake: any new
or changed `.gitignore` is itself an out-of-scope change. So is any new or
changed file under a `__pycache__/` directory, which `.gitignore` hides but
Python loads. The audit's own Python runs isolated (`python3 -I`), so nothing in
the checkout is imported, and its Git commands ignore repository fsmonitor
hooks. Not audited: other ignored paths; `.git` contents other than HEAD,
refs, the stash list and the worktree list (hooks, config, `info/exclude`,
index flags); processes that leave Codex's process group and write later; and
writes outside the checkout. The audit is a check at one moment, not a
sandbox.

| Exit | Meaning | Builder action |
| --- | --- | --- |
| 3 | Out-of-scope change, whether or not an A appeared or Codex failed; the Q and verdict are written to `$STATE/HALT` | No retry, wake, commit, edit, revert or clean. Report the verdict and log path to Dev; the lane stays halted until Dev has looked |
| 1 | No sealed A: Codex failed, the timeout fired, Astra declined, the A is unsealed, or the wake was interrupted | Retry once only if Codex itself failed (nonzero exit or timeout), no A exists and the decision log is unchanged. Otherwise no retry; never read an unsealed A, and report a sealed A to Dev before reading it. Tell Dev; without an A, leave the Q standing for a manual relay |
| 0 | Sealed A and a clean audit | Read the A with consult.sh and honor its Contract change and Escalate to Dev fields. Commit the A and any governor log append, unedited, in a separate commit |
| 2 | Invalid input or configuration | Fix the input or configuration |
| 4 | Refused without waking | No retry; tell Dev the reason |

Builder interpretations of Dev's spec, for Dev to confirm or reverse:

- Exit 1 outranks 0, so a sealed A that appears although Codex failed, timed
  out or was interrupted still yields 1; the builder reports it to Dev before
  reading it.
- The message substitutes the Q's number in both the Q and the A path, and
  keeps `$TMPDIR` literal for the governor's own shell.
- `timeout` gets `-k 60s`, so a Codex that ignores SIGTERM is killed; that
  shows as exit 137. A terminated wake stops its child, sweeps the child's
  process group, audits, and releases its lock.
- A HALT is checked again after taking the lock, and written before any
  output. A failed audit is exit 3. A log name that already exists gets a
  `-PID` suffix rather than a refusal.
- The two ignore-rule and bytecode checks above, and the isolated audit, go
  beyond the listed snapshot. They judge "ignored paths" by the rules in force
  before the wake.

No builder session opens, lists, greps, tails or copies anything under
~/.kmla-governor/logs/ or ~/.codex/. Astra reviews both lanes, so its
transcript can contain either lane's implementation. The only governor output
a builder reads is the sealed A file, through consult.sh. If a log needs
inspecting, give Dev its path.

`scripts/test_wake_governor.py` exercises every exit code with a fake `codex`
and `lsof` in a disposable repository; it never wakes a real model.

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

Consult delivery may create/seal only the new A and append to DECISION_LOG,
including new Status index rows.
Separate governor reviews live in docs/reviews/ with their audience/lane labeled.
Audit changed paths after each consult.sh call (expected changes: none) and
each answer-delivery interval; for a P-WAKE wake, wake_governor.sh performs
that audit. Coordinate quiescence for attributable before/after
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
the queue. No CLI failure breaker or fallback spawn is part of consult.sh.

`scripts/test_consult.py` tests awaiting/delivery, numbering/path rejection,
symlinks, repeat reads, exact file preservation and absence of spawning.
Obsolete spawn/resume/JSON/tool-boundary tests were removed, not skipped; their
original behavior and verification remain in Git and `SMOKE_TEST.md`.

Historical Q-001/002 tested B003 and context persistence; A-003 corrected two
overstatements in A-001 without editing it. A-004's Dev-relayed semantic body
is `DECISIONS_RECOMMENDED.md`. These historical artifacts and prior A-files
remain unchanged; none reactivates the old roles or overrides accepted contracts.
