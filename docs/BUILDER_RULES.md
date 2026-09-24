# Working rules

You are a Claude Code KMLA builder. This role binding is staged under PROPOSED
P-ROLES and is activated only by Dev's acceptance and merge. Until then, do
not start a builder session from the proposal branch. AGENTS.md files belong
to the governor and do not apply to Claude builder sessions.

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

When you hit such a doubt,
write docs/consult/Q-NNN.md, run bash scripts/consult.sh docs/consult/Q-NNN.md,
and halt the affected lane while it reports awaiting the governor (nonzero).
Notify Dev/the governor with the Q path; the script does not dispatch a model
or arrange monitoring. When the governor has written the A file, run the same
command to read it, then proceed only within its authority and the current
approved contracts. If the A file says escalate: yes, halt that
lane and record it in STATE.md under ## Blockers. Never edit an A file.
Never answer your own Q file or have another builder answer it. Numbers start
at 001, use three digits, and are never reused; a disagreement is a new Q
referencing the old A. Follow docs/consult/README.md for the Q/A format.

Dev's standing consult authorization includes the excerpts needed for each
question. Governor answers may create/seal only docs/consult/A-*.md and append
to docs/DECISION_LOG.md; separate review notes belong under docs/reviews/.
Audit changed paths after every consult call and answer-delivery boundary;
any out-of-scope write halts that lane. Coordinate a quiescent before/after
interval so writes are attributable. A polling/read-only consult call must
change no repository paths. Never relay an opposite lane's implementation
through a question, answer, report or mixed-context integration handoff.
Do not seek renewed permission per question within this fixed scope. Contract
amendments, protected artifacts and installations still require Dev's approval.

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
