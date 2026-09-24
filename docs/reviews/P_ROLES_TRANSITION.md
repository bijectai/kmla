# P-ROLES transition review

Audience: Dev / integration only. No lane implementation is conveyed here.
Status: **PROPOSED**, not accepted or merged. After this task, wait for Dev's
acceptance; no implementation, consultation or monitoring job is started.

## Branches and sequence

1. Existing implementation was already committed; push confirmed up-to-date at
   `fe25216db512aefdb205cdd0ba3e0c8769208176`. No new build work started.
2. Role-neutral handoff/history committed and pushed on
   `claude/checkpoint-0-integration` as
   `96722c5b8d8bbc9bf6d74327b84ac3736eb56f8f`.
3. `roles/claude-builder` was cut from that pushed head. Commit `a178c2a`
   proposes P-ROLES in the log/index and PROTOCOL.
4. `a2d2877` records the three lane renames as Git moves (94%/97%/94%
   similarity). The subsequent binding commit (containing this note) supplies
   the remaining instruction, queue and settings changes. Its final hash is
   reported with the push, not embedded self-referentially here. No role changes
   were placed on the integration branch. Nothing is merged.

All commits use only
`Devakh Rashie <59419810+arkanemystic@users.noreply.github.com>`.

## Exact task file list

Integration handoff commit (two paths):

```text
docs/HANDOFF.md
docs/phase1/HANDOFF_HISTORY.md
```

Roles proposal, relative to integration head 96722c5 (all changed/new paths,
including both sides of the lane instruction moves):

```text
.claude/settings.json
.claude/lanes/oracle.json
.claude/lanes/harness.json
.github/workflows/verify.yml
AGENTS.md
CLAUDE.md
Oracle/AGENTS.md
Oracle/CLAUDE.md
STATE.md
docs/BUILDER_RULES.md
docs/DECISION_LOG.md
docs/HANDOFF.md
docs/PROTOCOL.md
docs/consult/README.md
docs/reviews/P_ROLES_TRANSITION.md
gen/AGENTS.md
gen/CLAUDE.md
gen/README.md
harness/AGENTS.md
harness/CLAUDE.md
scripts/consult.sh
scripts/test_consult.py
```

The workflow change is only the protected-file diagnostic's pointer from
AGENTS to BUILDER_RULES; no enforcement or workload changed. Lane rules were
git-moved, then changed only to name the new root entry point; new governor
AGENTS files occupy their old paths. The archived handoff includes every byte
of the former handoff, behind an explicitly historical header.

## Cheap verification

- `python3 -B scripts/test_consult.py`: **13 tests, OK**. Each invocation
  asserts a byte/mode/path snapshot of its temporary fixture is unchanged;
  a trap detects any Claude spawn. Awaiting exits 1, bad inputs exit 2,
  matching answer retrieval exits 0 without changing bytes or permissions.
- `python3 -B scripts/human_manifest.py verify`: **passes**. Meter source and
  exploits were not inspected; this is the requested manifest verification,
  not an evidence re-hash or full-corpus execution.
- `jq -e .` on all three settings files: **passes**. Project attribution and
  five denies match Dev's requested values exactly. Each lane deny is an
  anchored Read/Edit pair for an existing opposite-lane or mixed-review path.
- `bash -n scripts/consult.sh`: **passes**; executable Git mode retained.
- Import inspection: the four root/lane CLAUDE files contain one `@` import;
  `@docs/BUILDER_RULES.md` resolves, with no nested import (depth 1).
- Byte comparison (not re-hashing): archived HANDOFF body equals the complete
  old file at fe25216; lane CLAUDE text equals the former AGENTS text except
  root-entry references. The initial Ruby string comparison mixed encodings;
  explicit binary comparison confirms identical bytes, without an archive edit.
- `rg -n 'Astra|Fable|AGENTS\.md|CLAUDE\.md'` over the operative root,
  lane, builder, consult, handoff, protocol and script files was reviewed:
  no live assignment of building to Astra remains in the proposed bindings.
  STATE's current/resume text routes roles through the pending proposal.
- `git diff --check`: **passes**. Protected tree, PLAN, old FABLE_PROMPT,
  prior Q/A files, dated reports, Oracle proofs/tests and harness/Interface
  implementation are unchanged. No full audit or multi-agent work was run.

Intentional old-role exceptions: PLAN; human/; FABLE_PROMPT; immutable A-files
and historical Q-files; old consult smoke/PR/recommended-semantics documents;
HANDOFF_HISTORY; dated phase/evidence reports; dated Oracle/UNPROVED ledgers and
test diagnostics; historical log/STATE bodies and contract drafts recording
earlier Fable reviews; untouched stale worktrees. They are history or protected
artifacts, not operative role instructions. P-ROLES lists this same boundary.

## Limits and self-review

Claude Code's actual loaded memory/settings were **not** confirmed; no Claude
session was launched. The owner supplied the CLI/loading/permission facts.
The first new builder must run `/memory`, check the root/import/lane CLAUDE
rules and confirm no AGENTS loaded, following HANDOFF's staged startup sequence.
Static JSON/import checks cannot prove that runtime behavior.

Permission rules are defence in depth, not a sandbox. Written lane isolation
remains primary; list-merging and shell bypass limitations are documented.
The queue does not allocate numbers or prove authorship/history: never-reuse
and no-self-answer remain written review obligations. It creates no scheduler
or notification, and existing ignored session state is left untouched.

Both stale worktrees and the pre-existing untracked Python cache are preserved;
the cache is not committed. No owner install, re-pin, checkpoint sign-off or
Project instructions setting change occurred. The generator settings file is
deferred until that lane opens, as requested.

Prolog assumptions: none added or changed; no semantic execution was performed.
Circuit breaker: three failed edit cycles on one check means stop and report.
The consult replacement passed its first test cycle; no breaker fired. The
path-pair check initially found the planned review-note directory absent before
this note was created; no rule or check was weakened to accommodate it.
