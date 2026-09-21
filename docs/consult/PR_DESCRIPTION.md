# infra: Fable consult channel

## Summary

- Add synchronous `scripts/consult.sh` with persistent, ignored Fable session ID.
- Add the exact root `CLAUDE.md`, consulting instructions in `AGENTS.md`, and
  the Q/A protocol. Preserve Dev's supplied prompt.
- Expose only Read, Glob, Grep, Write, and Edit. Disable skill entry points and
  configured MCP servers; do not grant Bash.
- Validate response JSON and answer files, preserve read-only A files, prevent
  concurrent session use, and retain raw responses privately for diagnosis.
- Include three real consultations and fifteen offline regression tests.

## Smoke-test output

```text
Claude Code: 2.1.247
Schema probe: PASS; session_id observed before implementation
Q-001: Claude success, A-001 created; wrapper chmod portability failure
Recovery: corrected chmod; restored session_id from Q-001's actual JSON
Q-002: exit 0; same session; exact Q-001 receipt recalled from conversation
Q-003: exit 0; same session; A-001 overstatements explicitly withdrawn
Saved session: matches all three live responses; ignored by Git
Prior answers: unchanged and read-only
Observed Fable writes: A-001.md, A-002.md, A-003.md only
Out-of-scope repository changes caused by this task: none
Regression suite: Ran 15 tests in 2.498s — OK
bash -n scripts/consult.sh: PASS
git diff --check: PASS
Real Claude command failures: 0
```

Q-002's transcript contains only Read Q-002 and Write A-002, yet its answer
recalls `orchid-4821-cobalt`, which Q-002 did not supply. Q-001/A-001 were not
reread for that test.

A-001 is immutable. A-003 supersedes its unsupported value-disjointness and
invariant-witness restrictions; the approved B003/B004 contract was not changed.
No consultation requested escalation. Full commands, recovery details, file
hashes, scope evidence, and the CLI/JSON assumption self-review are in
`docs/consult/SMOKE_TEST.md`.

Publication revalidation: all fifteen offline tests passed again with the
current supplied prompt (2.567 seconds). That prompt was revised between the
initial smoke test and publication; the builder preserved it unchanged. Its
current SHA-256 is
`4835f00f6081a639eca00b2442354d8666e783d0eda5b11745208f2e408f9373`.
The live results above refer to the earlier prompt; both hashes and the
unchanged answer hashes are recorded in the smoke-test report.

## Scope and limitations

No KMLA phase work. `human/`, `docs/PLAN.md`, `STATE.md`, Dev's prompt, and all
unrelated pre-existing work are unchanged. Q/A files are intended for version
control; the session ID is local-only. Tool restrictions are not a filesystem
sandbox, so future consultations still require write-scope audits.

## Publication scope

Dev authorized committing these task files to `infra/fable-consult`, pushing
that branch, and opening this PR against `main`. No commit directly to `main`
or merge is authorized. Include the Dev-supplied prompt unchanged; exclude the
local session ID and the unrelated, pre-existing Phase 0 scaffold.

Checkpoint 0 is still pending: the human-owned semantic decisions and hash
manifest remain TODO. This infrastructure PR does not approve B005 semantics,
pass a checkpoint, or authorize dependent KMLA implementation.
