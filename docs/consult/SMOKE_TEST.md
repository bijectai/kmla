# Fable consult channel: verification

Initial verification date: 2026-09-20, before publication was authorized.
Infrastructure only; no KMLA phase work was performed. Historical no-commit
statements below describe that initial verification session.

## Outcome

The synchronous channel and session resume work. Q-002 recalled Q-001 from the
same conversation without rereading the earlier files. Q-003 corrected two
unsupported restrictions in A-001; read those answers together. No approved
contract was changed and no consultation requested escalation.

The first invocation encountered a wrapper portability bug after a successful
Claude response. That failure and its recovery are recorded below; it is not
represented as a clean first-run pass. Fifteen offline regression tests pass.

## Live schema inspection before implementation

Installed CLI: `claude --version` returned `2.1.247 (Claude Code)`.
`claude --help` was inspected before choosing flags and again at final review.

Before hardcoding a JSON field name, ran this read-only transport probe:

```sh
claude -p 'Transport-schema probe only, not a KMLA consultation. Reply exactly READY. Do not inspect or modify files.' \
  --tools '' --disallowedTools '*' \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --disable-slash-commands --permission-mode acceptEdits --output-format json
```

Observed one JSON result object with `type: result`, `subtype: success`,
`is_error: false`, `result: READY`, and a UUID-valued `session_id`. The separate
`uuid` field differed from `session_id`. This probe's session was not used as
the design consultation session. Raw consultation responses are retained in
private temporary files; the script prints each location to stderr. They are
not committed, and the local saved session ID remains ignored.

## Consultation results

Commands actually run, in order; do not rerun them because A files are immutable:

```sh
bash scripts/consult.sh docs/consult/Q-001.md
bash scripts/consult.sh docs/consult/Q-002.md
bash scripts/consult.sh docs/consult/Q-003.md
```

| Question | Observed result |
| --- | --- |
| Q-001: restate resolved B003 | Claude exited 0, returned successful JSON with `result: docs/consult/A-001.md`, and created A-001. The wrapper subsequently exited 1 at `chmod`; see recovery below. |
| Q-002: recall Q-001 | Corrected wrapper exited 0 and printed A-002. Returned the same session ID, saved automatically. Recalled the exact receipt `orchid-4821-cobalt` and the earlier question's substance. |
| Q-003: clarify A-001 overstatements | Wrapper exited 0 and printed A-003. Same session ID, saved automatically. Fable withdrew both extra restrictions without a contract change or escalation. |

All three real consultation responses have `type: result`, `subtype: success`,
`is_error: false`, an empty `permission_denials` array, and the same `session_id`.
Each response's `result` is exactly its corresponding A file path. The final
saved ID equals that common ID. A files have no write bits; the session file
has mode 0600. The next unused question number is Q-004.

### First-run wrapper finding and recovery

The original `chmod a-w -- "$answer"` invocation failed on this macOS host:

```text
chmod: --: No such file or directory
```

The answer and successful Claude JSON already existed. Changed only the wrapper
to `chmod a-w "$answer"`; its validated `docs/consult/A-NNN.md` path cannot be
an option. Recovered `.fable_session` from the actual Q-001 JSON's verified
`session_id`, set mode 0600, and did not rerun Q-001 or edit its answer. Q-002
then exercised the fixed response handling and automatic session save against
the real CLI. Fresh-session automatic saving is additionally covered by the
offline regression suite, not claimed as a second live fresh-session run.

Real Claude command failures: zero. Wrapper failures: one, resolved above.
The three-identical-CLI-failures circuit breaker was not reached. Mock failures
in offline tests are deliberate fixtures, not real Claude failures.

### Answer-consistency finding and resolution

A-001 correctly restated admission, UNRESOLVED, frozen-corpus differential
kills, and v2 reporting, but additionally claimed the two searches could never
produce the same input values and barred admission witnesses from invariant
refutation. Neither blanket restriction appears in approved B003/B004.

The builder did not implement these additions or edit A-001. Q-003 asked Fable
to resolve them. A-003 expressly withdraws the named wording: independently
generated inputs may coincide in value; a kernel-checked invariant violation
does not become invalid merely because of witness provenance. Admission
witnesses still must not be inserted into the frozen grading corpus, and an
invariant refutation alone is not a differential kill. `docs/PROTOCOL.md` and
`docs/HANDOFF.md` remain unchanged and authoritative.

### Independent recall and tool-use check

Inspected only this consultation's local Claude JSONL transcript, using Python
to select assistant `tool_use` blocks for each question. Observed:

```text
Q-001: Read Q-001, PLAN, STATE, HANDOFF, PROTOCOL; Glob;
       Read consult/README; Write A-001
Q-002: Read Q-002; Write A-002
Q-003: Read Q-003; Write A-003
```

Q-002 did not read Q-001, A-001, transcript files, or memory files, or search
for the receipt. Its question did not supply the receipt. This supports genuine
conversation persistence rather than file-based recovery. No Bash, MCP, or
other unlisted tool calls occurred. Fable's repository writes were only the
three new A files. Earlier answers' content and modes remained unchanged.

## Regression and scope checks

```sh
/usr/bin/python3 -B scripts/test_consult.py
bash -n scripts/consult.sh
git diff --check
git check-ignore docs/consult/.fable_session
```

Captured test summary:

```text
Ran 15 tests in 2.498s

OK
```

Tests use a fake CLI in isolated temporary repositories, never the real Claude
command. Coverage includes new/resumed sessions, exact arguments, missing IDs
with/without a previous ID, changed IDs, malformed saved IDs, existing locks,
immutable answer paths, answer symlinks, missing answers/prompts, bad JSON,
reported CLI errors, invalid paths, and invocation from another directory.

Shell syntax and tracked-diff whitespace checks passed. An exact byte comparison
confirmed the required three-line `CLAUDE.md`; `scripts/consult.sh` is executable.
The session is ignored; Q/A files are not ignored and are intended for commit,
but no file was staged, committed, or pushed in this task.

A pre-task inventory covered 443 repository files, excluding Git metadata,
using SHA-256 plus permission modes. Compared it after every live consultation
and again at final review, including untracked files. All task changes are
within `docs/consult/`, `scripts/`, `.gitignore`, `AGENTS.md`, and `CLAUDE.md`.
All 409 files under `human/`, `docs/PLAN.md`, `STATE.md`, the Dev-supplied
`FABLE_PROMPT.md`, and the pre-existing root README changes were preserved.
No `docs/DECISION_LOG.md` was written. There were no out-of-scope task changes.

The worktree already had a modified root README and untracked KMLA scaffold.
Consequently, plain `git diff --name-only` still lists that pre-existing README
change and omits new untracked files. It cannot by itself establish this task's
scope; the before/after content-and-mode audit supplies that evidence.

Protected prompt SHA-256 at the initial smoke test:
`b31414d1873a5e2c5609056ceb0c947b98645204afe78ff97e0e5b79aa689820`.

Immutable answer SHA-256 values:

```text
A-001.md  41b43ea92037f3f3dfb889ff831e53ba2e7e7a20499e02e76f650757c8c89af9
A-002.md  9ecac44393fd0cd861ac3fd4f78aa7b344aeaf27a8c16ec468c3da0a5ab27017
A-003.md  0a6dcba303179b5f247c3780b6f3b3ba03899fb6debe76c546895c9ba99fdfed
```

## Self-review: CLI and JSON assumptions

Each assumption is paired with the command used to verify it. Live execution
means the three `bash scripts/consult.sh ...` commands above, not a hypothetical
future run. Negative/error paths were verified with the offline tests where
real failures were not observed.

| Assumption used | Verification command and evidence |
| --- | --- |
| `-p` runs synchronously and exits, rather than starting an interactive/background agent. | `claude --help` describes print-and-exit; the schema probe and live calls returned to the shell. No `--bg` flag is used. |
| `--append-system-prompt` appends the supplied body without replacing the default system prompt. | `claude --help`; live calls accepted the flag. `/usr/bin/python3 -B scripts/test_consult.py` checks the exact passed body, allowing only shell removal of trailing newlines. |
| A comma-delimited `--allowedTools` pre-approves names; it is not by itself an exclusive exposure list. | `claude --help` plus the official CLI reference below. Live calls and the exact-argument test accepted `Read,Glob,Grep,Write,Edit`. |
| `--tools` restricts the built-in tool set to those five names. | `claude --help` explicitly describes the available built-in list; live calls accepted it, and transcript inspection found no tools outside it. |
| `--disallowedTools 'Bash,mcp__*'` provides an additional denial rule. | `claude --help` confirms the flag; live calls accepted it. No denied tool was attempted. The exclusive built-in list and empty MCP configuration are the primary boundary; wildcard enforcement was not independently adversarially tested. |
| `--strict-mcp-config --mcp-config '{"mcpServers":{}}'` excludes configured MCP servers for this process. | `claude --help` says only the supplied MCP configuration is used and accepts JSON strings. The schema probe and live calls accepted the empty configuration; no MCP calls occurred. |
| `--disable-slash-commands` disables skill entry points. | `claude --help` states "Disable all skills"; live calls accepted it. No skill tool calls occurred. |
| `--permission-mode acceptEdits` permits the requested file writes without an interactive prompt. | `claude --help` lists `acceptEdits`; live calls, with stdin closed, created A files with no permission denials. This is not a filesystem-path sandbox. |
| `--output-format json` produces one JSON result object on stdout. | `claude --help`, the schema probe, and parsing all three retained live responses with Python `json.loads`. The script additionally rejects malformed/non-object JSON. |
| A successful result has `type == result`, `subtype == success`, and `is_error == false`. | The probe and all three parsed live responses matched these fields. `/usr/bin/python3 -B scripts/test_consult.py` verifies rejection of malformed and error envelopes; no unobserved error schema is relied upon. |
| `session_id`, not `uuid`, is the resumable identifier; emitted IDs are UUID-shaped. | Inspected the schema probe before implementing extraction; parsed all live responses. `claude --help` documents UUID session identifiers. All observed IDs match the validation pattern. Missing IDs warn; an incompatible future format needs review. |
| `--resume <id>` keeps the same conversation and ID without `--fork-session`. | `claude --help`; Q-002/Q-003 live commands returned Q-001's ID, and Q-002 recalled its receipt without file recovery. The wrapper rejects a changed returned ID. |
| `.result` is an informational response, not authoritative filesystem evidence. | Parsed live JSON reported the expected A path. The wrapper checks the actual nonempty regular A file instead; the offline missing-answer test proves a successful envelope alone is insufficient. |
| Nonzero CLI exits and reported JSON errors must not be treated as successful answers. | `/usr/bin/python3 -B scripts/test_consult.py` propagates a mock exit 7 and rejects error JSON. No real CLI failure was induced to test this. |
| Omitting `--model` uses local configuration, not a pinned model called Fable. | `claude --help` and retained live `modelUsage` keys: `claude-opus-5[1m]` and `claude-haiku-4-5-20251001`. Fable is the consultation role here; no model-selection claim or override is made. |

Primary references cross-checked against the installed help:
[CLI reference](https://code.claude.com/docs/en/cli-reference) and
[programmatic usage](https://code.claude.com/docs/en/headless).
The local version and observed responses, not future documentation changes,
are the implementation's verification target. Tool restrictions do not enforce
write paths: instructions, preserved-answer checks, and repository audits are
still required. No claim of a filesystem sandbox is made.

## Initial PR handoff and subsequent authorization

Requested title: `infra: Fable consult channel`.

At the initial handoff no PR was opened because the user prohibited commits,
the work was uncommitted, and the remote had only `main`. Verified with:

```sh
git rev-parse HEAD origin/main
gh api repos/bijectai/kmla/branches --jq '.[].name'
```

Both revisions were `6406e0cbb2efd778d46c333a6522dfceda6ac67d`; the only remote
branch was `main`. No commit, push, branch publication, PR, or merge was
performed during the initial verification session.

Dev subsequently authorized branch `infra/fable-consult`, a commit of only the
consult-channel task files, pushing that branch, and opening a PR using
`PR_DESCRIPTION.md`. Direct commits to `main` and merging remain prohibited.
The unrelated pre-existing Phase 0 scaffold stays outside this PR. Publication
does not pass Checkpoint 0 or resolve the human-owned build decisions.

At publication revalidation, the supplied prompt already differed from the
initial smoke-test snapshot. Its current SHA-256 is
`4835f00f6081a639eca00b2442354d8666e783d0eda5b11745208f2e408f9373`.
The builder preserved those supplied bytes without editing or restoring the
prompt. A-001 through A-003 still match their original hashes. The fifteen
offline tests were rerun successfully with the current prompt (2.567 seconds);
the live consultations above are historical results for the earlier prompt,
not a claim that the revised prompt was sent in another live consultation.
