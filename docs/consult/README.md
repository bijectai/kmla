# Fable consult channel

Fable is the design authority; Astra builds. Dev supplies `FABLE_PROMPT.md`.
Keep that prompt unchanged. This channel is infrastructure and does not itself
authorize KMLA phase work or changes to human-owned artifacts.

## Questions

Use `Q-001.md` onward, with three zero-padded digits, never reused. Check all
existing Q and A files before choosing the next number. Each question includes:

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
A proposal for review, or None. Never present it as Fable's answer.
```

Run from the repository root:

```sh
bash scripts/consult.sh docs/consult/Q-NNN.md
```

The executable script also works when invoked by its full path from another
directory; supply the same repository-relative question argument. It blocks
until Claude finishes, then prints the corresponding A file to stdout.

## Answers

Only Fable writes `A-NNN.md`. Each answer includes:

- Answer.
- Rationale.
- Contract change: yes/no. If yes, append the proposed change to
  `docs/DECISION_LOG.md`; do not apply it without the required approval.
- Escalate to Dev: yes/no.
- A final one-line self-review naming assumptions Dev should verify.

A files are read-only once written. The script removes their write bits and
refuses an existing answer path. Never edit, delete, or reuse an A file. A
disagreement becomes a new Q referencing the old A. An incomplete answer left
by a failed run is still preserved; report it and use a new Q for follow-up.
Never answer your own Q. If escalation is yes, halt that lane and record the
reason under `STATE.md` → `Blockers`.

## Session and tool boundary

The script reads and atomically saves the live CLI's `session_id` in
`.fable_session`, passing `--resume` on subsequent calls. That local file is
ignored by Git; Q and A files are versioned. Do not fork the session or use
`--continue`, which could select a different conversation. A lock prevents
concurrent consults from racing the shared session. After an interrupted process,
verify no consult is running before removing a stale, empty lock directory.

Claude receives only the `Read,Glob,Grep,Write,Edit` built-in tool set via
`--tools`, with the same list pre-approved by `--allowedTools`, and
`--permission-mode acceptEdits`. Bash and MCP tools are denied; strict empty MCP
configuration and disabled slash commands prevent additional tool entry points.
The supplied prompt body is passed using `--append-system-prompt`; shell command
substitution strips trailing newline characters, not the prompt's content.
No model override is selected; the local CLI's configured model is used.

The tool flags restrict available tools, not filesystem write paths. Fable's
instructions limit writes to `docs/consult/` and `docs/DECISION_LOG.md`.
Audit changed paths after calls; an out-of-scope write is a finding and stops
the lane. For these infrastructure smoke tests, the narrower authorized path
list also excludes `docs/DECISION_LOG.md`; any such write must be reported.

Raw CLI JSON is retained in a private temporary file; its path is printed to
stderr. Successful stdout contains only the answer text. The first live schema
probe confirmed `session_id`; `.uuid` is a different, result-event identifier.
If a future response lacks a valid session ID, warn and skip saving it (leave an
existing saved ID unchanged). Never claim persistence from a warning-only run.

## Failure handling

Missing Dev prompt, invalid question paths, existing answers, malformed session
IDs, CLI errors, malformed/error JSON, and missing or empty answers fail with
a nonzero exit and a stderr diagnostic. The script never writes an answer itself
and never automatically retries or silently starts a fresh session on failure.

If the Claude command fails three times for the same reason, stop and record
the error verbatim under `STATE.md` → `Blockers`. Do not weaken the tool boundary
to make a run succeed. If the Dev prompt is absent, record the requested blocker
`B005: FABLE_PROMPT.md not installed.`; preserve any existing B005 history.

## Verification

Q-001 asks for confirmation of resolved B003. Q-002 asks what Q-001 asked,
using the same session and conversation memory rather than rereading Q-001/A-001.
Check answer consistency, the saved ID, unchanged previous answers, and changed
file scope after each call. Q-003 corrects two overstatements in A-001 without
editing it or changing the approved B003/B004 contract. Read A-001 together with
A-003. See `SMOKE_TEST.md` for actual results and CLI assumptions.
