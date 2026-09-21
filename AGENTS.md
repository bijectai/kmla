# Working rules

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

## Consulting Fable

When you hit a doubt in a category listed in docs/consult/FABLE_PROMPT.md,
write docs/consult/Q-NNN.md, run bash scripts/consult.sh docs/consult/Q-NNN.md,
read the A file, and proceed. If the A file says escalate: yes, halt that
lane and record it in STATE.md under ## Blockers. Never edit an A file.
Never answer your own Q file.
