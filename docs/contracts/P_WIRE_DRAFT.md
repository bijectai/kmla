# P-WIRE — exact text for owner approval

**Accepted by Dev, 2026-09-22: WIRE, including both handling proposals.**
The proposal below is preserved as the approval record. Its replacement spans
and packaging are installed in `docs/contracts/PARITY.md`; `Interface/WIRE.md`
holds the byte/count contract. Input-codec implementation is still outstanding.
This approval is not Checkpoint 1 sign-off and authorizes no write to `human/`.

## 1. File envelopes: replacement span

Replace these two sentences together, so the preceding future-tense sentence
does not contradict the release:

> The approved `Interface/` and `DECISIONS.md` will define section payloads and
> query encodings. That definition remains pending; the independent meter only
> needs the input identity and section to determine the expected output population.

With exactly:

> Payload and result semantics are supplied by the approved
> `human/DECISIONS.md` H1–H4, G4, D1/V9, M1, H6.1, H6.2 and H6.5 and the
> corresponding `Interface/` declarations, including the G1 ordering and A3
> wildcard-identity rules those sections reference. Their concrete JSON spelling
> is a builder-owned lossless codec of that approved shape, fixed once as a
> byte-level specification in `Interface/` and implemented independently by both
> isolated lanes; the independent meter needs
> only input identity and section to determine the expected output population.

## 2. Comparison requirements: replacement sentence

Keep the preceding sentence, “Both engines must implement only approved
canonicalization before emitting outputs.” Replace:

> Until the payload and result specifications are approved, producers are blocked
> rather than guessing representations.

With exactly:

> Producers may encode fields determined by those approved sections using the
> shared lossless codec; producers remain blocked on any field those sections
> do not determine and must obtain a recorded owner decision before supplying it.

The codec fixes byte spelling, not which semantic value is observed; the retained
approved-canonicalization requirement still governs the latter. The field map
in the shared codec specification must cite each field's governing signed
section or the separately approved packaging choice below. A missing governing
rule stays visible and blocked. These wire paragraphs do not redefine H6.3/H6.4
per-case/model scoring.

## 3. Two handling proposals included in the same approval

These are explicit proposals, not choices silently inferred from the signed text.

| Undetermined item identified in A-008 | Proposed handling |
| --- | --- |
| Record granularity | One record per `(Household, target, bound-argument tuple)`, with the **already approved H6.5** call mode and the year identified wherever that target requires them. Bind these identifiers to the signed table in `Interface/` before producer use; this does not invent modes or assume Phase 2 target declarations already exist. Retain original-case identity separately: records do not redefine the 376-case population or H6.3 case success. Report record, distinct-household and original-case counts separately; interpret the generated ≥10k-input threshold in this declared record unit. |
| Byte-level escape/format pinning | Fix the byte contract once in `Interface/`, shared without exchanging lane implementations: compact JSON (no optional whitespace); UTF-8 with no Unicode normalization; escape quote/backslash, use `\b`, `\f`, `\n`, `\r`, `\t`, and lowercase `\u00xx` for other U+0000–U+001F controls; leave other Unicode, including astral-plane code points, raw (not surrogate-pair escapes). Integers remain exact decimal integers, never floats. Preserve the existing H6.2 tags, ISO-day representation and solution-tuple encoding. Use the existing shared encoded-string ordering and deduplication only at the approved observation boundary. |

The tuple identifies a record logically; it is not concatenated into a filename.
Mint IDs under PARITY.md's existing grammar and ASCII-case-fold uniqueness rule,
and retain the ID-to-target/mode/arguments and case-to-record(s) mappings. One
original may use several records, and records may be shared by originals; the
two extra-conjunct cases still evaluate their H6.3 conjuncts on observed tuples.
Install the approved packaging description alongside the release paragraphs,
not as an implicit convention known only to one producer.

Consequence for Dev's approval: ≥10k records need not mean ≥10k distinct
households. This proposal reports both, without silently imposing or claiming a
new ≥10k-household requirement. Dev can amend that choice in this same approval.

The byte proposal describes the current shared observation encoder, whose
control-character restoration is already installed; it does not authorize a
different representation. Input field spelling remains a future builder-owned
lossless codec, not a completed codec in this draft. Freeze its bytes in
`Interface/` and cross-language fixtures before either producer is used.

Record granularity does **not** change B003's kill-rate denominator: that remains
the set of admitted whole-section mutants. A kill remains a refutation by at
least one record in the frozen grading corpus. Nor does packaging change the
≥20-hits-per-arm requirement. Corpus identities and the chosen unit must be
reported explicitly.

No new semantic mode, output-position projection, default, term coercion, fact
deduplication, missing-value convention or observation canonicalization is
selected here. H1–H4 facts/stipulations keep their approved order and multiplicity;
H6 list observations remain solution sets and scalar entry points retain their
approved first-solution behavior. The meter and its informational envelope-defect
classification are unchanged.

## Scope of approval

After Dev approves the text, its installation releases only P-WIRE. It does not
resolve P-R5CYCLE, sign off Checkpoint 1, or authorize a builder write to `human/`.
No installation, approval or implementation is performed in this draft session.

## Self-review

No new Prolog interpretation is needed for this wording. It assumes the signed
H1–H6/G4/D1/V9/M1 shape remains authoritative and distinguishes a byte codec from
query semantics. In particular, JSON formatting can affect observation-array
order because the shared encoder sorts encoded tuples. Three failed edit cycles
on one test means stop and report; never change the meter, source, comparison or
input domain to force a pass.
