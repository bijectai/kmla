# Generator lane — approved domain and isolation

Read root AGENTS.md first. This is a later-phase lane, not permission to begin
Phase 2 before Dev signs off Checkpoint 1.

- Implement against `human/DECISIONS.md`, accepted amendments in
  `docs/PROTOCOL.md`, and `Interface/` only. Do not inspect `Oracle/` source.
  The integrated production Valid instance may be invoked through Interface;
  importing/calling that interface is not permission to inspect its provider.
- Never mint a person associated with multiple distinct birth events, a birth
  with multiple distinct start days, or an eligible dependent pair with the
  same birthday. Eligibility is original K-and-c3, including all applicable
  solutions across every year in shared `r5Years`; do not prefilter the pairs.
  Preserve identical fact repetitions and tag-sensitive identity.
- Require full production `Valid` and query-time coverage before emitting a
  graded record. Test-only OracleGuards mocks are forbidden in production.
  Raw Workdays/years, including supplied arguments, must pass the shared
  checked boundary. Failure is diagnostic, never a normal reference value.
- Follow `Interface/WIRE.md` for spelling, mappings and distinct counts.
  Emit `record_count`, `distinct_household_count`, `original_case_count`
  separately in summaries, freeze manifests and coverage reports. ≥10k uses
  records; ≥20 hits per arm and the admitted-mutant kill denominator are unchanged.
- Do not move mutation-admission witnesses into gen/out/. Freeze/re-freeze only
  at the authorized checkpoints and retain both versioned results under B003.
- The harness owns the 376 originals. Combined coverage reports must preserve
  their accounting; do not drop originals or weaken gates to fit generated data.
- Any design flaw or uncovered semantic choice halts the affected development
  and is reported. Three failed edit cycles on one test means stop and report.
