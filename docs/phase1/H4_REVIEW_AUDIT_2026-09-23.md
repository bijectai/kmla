# H4 candidate: authorization and review audit

## Push precedes consultation

The owner-requested commits `6e3cdc9`, `f99fafe`, and `866f519` were pushed to
`origin/claude/checkpoint-0-integration` before invoking Q-020. The exact command
was `git push origin 866f5196fc3c645ba393a1b7f3e6e8048631836c:refs/heads/claude/checkpoint-0-integration`.
It exited 0, advancing `b80a807..866f519`; a subsequent
`git ls-remote origin refs/heads/claude/checkpoint-0-integration` returned
`866f5196fc3c645ba393a1b7f3e6e8048631836c`. All three author and committer fields
are `Devakh Rashie <59419810+arkanemystic@users.noreply.github.com>`.

## Actual review, not an inferred answer

`bash scripts/consult.sh docs/consult/Q-020.md` exited 0 after the owner's
explicit permission cleared the prior sandbox hold. The actual CLI JSON had:

```json
{
  "type": "result",
  "subtype": "success",
  "is_error": false,
  "permission_denials": [],
  "result": "docs/consult/A-020.md",
  "num_turns": 5
}
```

Raw response retained locally at
`/var/folders/nb/1nmz4lr56rz3wcmmcgglfyx00000gn/T/kmla-fable-response.UuLzo1`.
`jq -r '.session_id // empty' <response> | cmp -s docs/consult/.fable_session -`
exited 0; the response really contains `session_id` and the saved session
matches. A-020 is read-only (`-r--------`), SHA-256
`0d8922eccfa38aac97de6e0d8de64c1e30651d5de3e634c0c8d817fa206b1311`.
No old answer was edited. Existing CLI flags were not changed.

Fable's working-tree writes were only A-020 and 38 appended lines in
docs/DECISION_LOG.md. Pre-/post-consult hashes of STATE, HANDOFF, the draft and
Q-020 matched. Q-020's submitted hash was
`4cab3c307cb879295fb09a13d63146aef00d6fd5069d7da491745e5ddff1207c`.
The protected manifest verified before and after the consult. Subsequent
draft/status edits and scope-census files are the builder's, not Fable's writes.

## Meaning of the endorsement

A-020 found no missing owner choice or counterexample. Its four clarifications
are incorporated in the staged candidate: replacement (not a second traversal),
per-unary-predicate provenance, asymmetric inner/outer deduplication, and
fail-closed unique-rule recognition. This releases the owner's condition for
candidate implementation and measurement, not protected installation,
preservation, global completeness or Checkpoint 1. Dev alone installs/re-pins.

A-020's claims of regrounding stability and harmlessness of non-service terms
are review arguments, not measured results. In particular, a duplicate-sensitive
H4.3(a) comparison must actually run; neither endorsement nor the 157 declared
pairs is a substitute. Both H4.3 checks for every original and traversal cost
remain separate verification obligations. A failed check is a finding, not
permission to change the procedure.

## Reproducible scope census

Run `python3 -B scripts/audit_h4_scope.py`. Retained output is
`docs/consult/evidence/h4-scope-census-2026-09-23.json`:
376 originals, 16 `split_string/4` calls, exactly one call whose input variable
is not the rule head's first argument variable: tax_case_33.pl:30:5, in the
rule at 29:1, file SHA-256
`5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0`.
This uses the existing source-preserving reader and statement-local variable
identity. It is a syntactic census, not dataflow analysis, candidate-domain
completeness, a no-other-raises certificate or either H4.3 check.

## Self-review

The existing Python regression suite passed again: 111 tests, exit 0. Complete
streams and command metadata are in `docs/phase1/h4-review-regression-2026-09-23/`.
This is regression evidence, not H4.3 verification.

The review's Prolog arguments are not silently promoted to facts. Bound-atom
acceptance/free-input failure and the 157 declared pairs have prior pinned
evidence; grounding order, multiplicity and preservation require new measurement.
The census assumes the existing parser's variable identity, not that matching
spellings across different clauses share a variable. No Oracle implementation
is shared with the isolated harness context. No protected artifact is written
and the independent meter source is never inspected. Three failed edit cycles
on one test means stop and report; no review-related test edit cycle has failed.
