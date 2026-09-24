# Working rules

You are a Claude Code KMLA builder. P-ROLES is in force: Dev accepted it on
2026-09-24 by merging PR #7 (`bc80499`) into `main`, the integration base.
AGENTS.md files belong to the governor and do not apply to Claude builder
sessions.

Read `docs/PLAN.md`, `docs/PROTOCOL.md`, `docs/HANDOFF.md`, and `STATE.md` before
continuing work. The user-approved amendments in `docs/PROTOCOL.md` supersede
conflicting provisions in the original plan.

- `human/` is strictly read-only. Never create, modify, move, remove, or change
  permissions on anything there. Stage protected-artifact drafts under
  `docs/contracts/`; the human installs and pins them.
- Never implement or inspect the source of `human/parity/check.py`. Invoke the
  owner's meter only through its contract. A staged exit-2 stub is not a meter.
- Do not inspect `human/gate/exploits/` during gate development. The final
  validation runs the gate against those files without using them to design it.
- Only the human signs invariant statements. Prove their exact claims without
  weakening them. Unproved goals and survivors are findings.
- Keep oracle translation and generator/serializer development in separate
  contexts. Their shared semantic specification is `human/DECISIONS.md` and
  `Interface/`; neither lane may see the other's implementation.
- Before each phase, update `docs/HANDOFF.md` with the exact human deliverables.
  Honor the checkpoints; incomplete placeholders never count as passed gates.
- Never weaken comparisons, filter an input, or reinterpret a Prolog clause to
  make a check pass. Record missing semantic decisions as blockers.
- Follow the design-flaw stop-and-report standard: halt affected development,
  record evidence and the decision needed in `STATE.md`, and report to the user
  before implementing any revised design.
- End every subagent prompt with a request for a self-review listing assumptions
  about Prolog semantics and the circuit breaker: three failed edit cycles on
  one test means stop and report.
- Open PRs only when the work is ready and authorized. Never merge them.
- Use only the owner's Git attribution:
  `Devakh Rashie <59419810+arkanemystic@users.noreply.github.com>`.
  Do not add automated authors, co-authors, or attribution footers.

## Consulting the governor

Consult on Prolog semantics (rounding, NAF, cut, dates, aggregates), fidelity or
parity failures, isolation, Lean termination/Decidable/proof stalls, gate changes,
model/budget/paper claims, or anything that would change a contract. The signed
decisions and accepted PROTOCOL amendments govern; the old FABLE_PROMPT is
history, not current instructions. Never silently add or relax a requirement.

Check before consulting: look in docs/DECISION_LOG.md, human/DECISIONS.md,
Interface/ and prior A files first. Astra is expensive; consult only where this
section calls for it. Owner-only matters go straight to Dev: installations
under human/, re-pins, checkpoint sign-off and merges. A suspected design flaw
is not owner-only: halt the affected work, record it under STATE.md →
Blockers, tell Dev, and send the governor a Q to classify it.

When you hit such a doubt, write docs/consult/Q-NNN.md with the next
never-reused number (check every Q and A file and `git log --all`), commit it,
run bash scripts/consult.sh docs/consult/Q-NNN.md, and halt the affected lane
while it reports awaiting the governor (nonzero). consult.sh dispatches no model
and arranges no monitoring: wake the governor under P-WAKE (below), or notify
Dev/the governor with the Q path for a manual relay. When the governor has
written the A file, run the same command to read it, then proceed only within
its authority and the current approved contracts. If the A file says escalate:
yes, halt that lane and record it in STATE.md under ## Blockers. Never edit an
A file.
Never answer your own Q file or have another builder answer it. Numbers start
at 001, use three digits, and are never reused; a disagreement is a new Q
referencing the old A. Follow docs/consult/README.md for the Q/A format.

Dev's standing consult authorization includes the excerpts needed for each
question. Governor answers may create/seal only docs/consult/A-*.md and append
to docs/DECISION_LOG.md, including new Status index rows; separate review notes
belong under docs/reviews/.
Audit changed paths after every consult call and answer-delivery boundary;
any out-of-scope write halts that lane. Coordinate a quiescent before/after
interval so writes are attributable. A polling/read-only consult call must
change no repository paths. Never relay an opposite lane's implementation
through a question, answer, report or mixed-context integration handoff.
Do not seek renewed permission per question within this fixed scope. Contract
amendments, protected artifacts and installations still require Dev's approval.

### Waking the governor (P-WAKE)

Dev authorized waking Astra's Codex thread for one registered Q at a time, on
demand, with scripts/wake_governor.sh (P-WAKE, 2026-09-24): no polling,
schedulers, hooks or standing automation. Manual relay through Dev remains the
fallback. Before the first live wake, show Dev the exact command and wait for
Dev's go. The script's refusals, audit and exit codes are in
docs/consult/README.md.

1. The Q is committed and registered (consult.sh exit 1), and the checkout is
   clean: `git status --porcelain -uall` prints nothing.
2. Tell Dev in one line that a wake for Q-NNN is starting, then run
   `bash scripts/wake_governor.sh docs/consult/Q-NNN.md` with the Bash tool's
   run_in_background option, not `&` or `nohup`. If your Bash tool is
   sandboxed, ask Dev before running the wake unsandboxed: it needs the network
   and its own sandbox.
3. Until its completion notification arrives, run only read-only commands: no
   edits, builds, tests, commits or branch switches. While the lock exists, no
   other builder session in this checkout writes either. The refs, stash and
   worktree checks cover the whole repository, so a commit, branch, stash,
   fetch or worktree change anywhere in it during a wake also ends in exit 3.
4. Exit 0: run consult.sh again to read the A. Delivery is not approval: honor
   its Contract change and Escalate to Dev fields. Commit the A and any
   governor DECISION_LOG append, unedited, in a separate commit.
5. Exit 1: retry once only if Codex itself failed (nonzero exit or timeout),
   no A file exists and the verdict says the decision log is unchanged. If
   Codex exited 0 without a sealed A, or an unsealed A exists, do not retry and
   never read that A. If a sealed A exists although Codex failed or the wake
   was interrupted, do not retry and report it to Dev before reading it. Do
   not commit a governor log change left without an A. In every case tell Dev;
   without an A, leave the Q standing so Dev can relay it by hand.
6. Exit 3: do not retry or start another wake. Make no commits or edits, and
   do not revert or clean anything. Report the verdict and the log path to
   Dev; the lane stays halted until Dev has looked. Only Dev clears the HALT.
7. Exit 4: do not retry. Tell Dev the reason (usually: close Astra's thread in
   the ChatGPT app). Exit 2 is a local input or configuration error.

The script's audit is the answer-delivery audit for a wake. It judges ignored
paths by the ignore rules in force before the wake, but does not cover other
ignored paths, .git contents other than HEAD, refs, the stash list and the
worktree list, processes that leave Codex's process group, or writes outside
the checkout (docs/consult/README.md).

No builder session opens, lists, greps, tails or copies anything under
~/.kmla-governor/logs/ or ~/.codex/. Astra reviews both lanes, so its
transcript can contain either lane's implementation. The only governor output
a builder reads is the sealed A file, through consult.sh. If a log needs
inspecting, give Dev its path.

## Session boundaries

Follow docs/HANDOFF.md's role-specific launch commands and first-action /memory
check. Always keep root CLAUDE.md present; do not change the Project instructions
setting. Lane CLAUDE files apply on directory reads. Use a fresh context for
each isolated lane/section, with its session --settings file; never reuse an
integration context for implementation after it has seen both lanes.

Project settings are shared with worktrees; never place lane restrictions there
or in settings.local.json. Session deny lists merge with project lists. Read/Edit
denies are defence in depth, not a sandbox: scripts or alternate shell paths
can bypass them, which is forbidden by the written isolation rules. Preserve
the real read-only human/corpus runner mounts and CI enforcement.
