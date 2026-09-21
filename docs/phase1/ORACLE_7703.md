# Phase 1.2 — §7703 initial slice

Status: dependency/mode audit; no whole-section implementation or parity claim.
This fresh oracle context reads the signed decisions, shared Interface, and
original Prolog as semantic inputs. No case code is executed.

Orchestrator follow-up: section implementation was paused before any Lean
definitions were added. The static report below is retained as the worker's
record. The orchestrator subsequently reproduced the sibling case with bounded
pinned-interpreter runs (Q-009), and a multiple-birth-date variant refuted the
sufficiency of A-009's proposed remedy (Q-010). Full inputs and results are in
`docs/consult/evidence/r5_sibling_cycle*` and `r5_multibirth_cycle*`. These are
diagnostic findings, not production parity or machine-checked validity proofs.

## Scope and dependency closure

Source: `human/sara/sara/statutes/prolog/section7703.pl`. Its nine clauses:

| Predicate / source lines | Direct non-fact dependencies | Disposition |
| --- | --- | --- |
| `s7703/4`, 2–9 | `s7703_a`, `s7703_b`; mode guards, identity | Deferred: recursive closure; H4.1 stipulations must follow statute solutions. |
| `s7703_a/4`, 12–14 | `s7703_a_1`, negated `s7703_a_2` | Independent slice. |
| `s7703_a_1/5`, 17–82 | first/last day of year, `is_before`; three `->` guards | Independent slice. |
| `s7703_a_2/5`, 85–98 | last day of year, `is_before` | Independent slice. |
| `s7703_b/3`, 103–106 | `s7703_b_1`, `s7703_b_2`, `s7703_b_3` | Deferred with `(b)(1)`. |
| `s7703_b_1/4`, 110–139 | first/last day, latest/earliest, duration, `s152_a_1/3` | Deferred: external recursive dependency, never replaced by a stub. |
| `s7703_b_2/4`, 142–184 | year extraction, two `findall`, two sums, exact ratio test | Independent bound-taxpayer/household mode. |
| `s7703_b_3_is_member_of_household/3`, 187–201 | `is_before`, optional end date | Independent slice. |
| `s7703_b_3/4`, 203–216 | `s7703_a`, membership helper, D8 day window, `findall`, length | Independent slice. |

Fact dependencies: `marriage_`, `agent_`, `start_`, `death_`, `end_`,
`legal_separation_`, `patient_`, `joint_return_`, `residence_`, `payment_`,
`purpose_`, `amount_`. Only `(b)(1)` reads `joint_return_`.

The full external closure from line 139 is:

```text
s152_a_1 -> s152_c -> s152_c_1
  -> s152_c_1_A -> s152_c_2 -> s152_c_2_A / s152_c_2_B
       -> is_child_of / is_descendent_of / is_sibling_of / is_stepsibling_of
       -> latest / earliest; death/start/agent facts
  -> s152_c_1_B -> residence/agent/patient/start/end facts; date helpers
  -> s152_c_1_C -> s152_c_3 -> is_descendent_of; birth/son/daughter facts;
       date helpers
  -> s152_c_1_E -> negated (s7703 -> ... -> s7703_b_1 -> s152_a_1)
```

Evidence: `section152.pl:19–20,57–67,70–86,89–153,158–230` and
`utils.pl:2–95,98–187`. This closure does **not** call `s151_c_applies`,
despite the statutory prose and six §7703 cases stipulating that predicate.
Those stipulations cannot substitute for line 139. No other section is
implemented in this task.

## Modes

`b` means bound on entry, `f` free on entry. Filtering a bound output must keep
order and multiplicity (G2). A bound fact occurrence remains a solution;
repeated successful fact matches cannot be collapsed to Bool.

| Predicate | Case / immediate internal modes | Output positions |
| --- | --- | --- |
| `s7703/4` | `bffb` ordinary callers; `bbfb` e.g. §3306:719; reverse person binding can flow from callers; `fffb` guard fails for statute clause | Free persons and marriage, including stipulated wildcards. Both-bound nonvar disjunction yields two statute proofs. Deferred. |
| `s7703_a/4` | inherits person bindings from root; `bffb` / `bbfb` from `(b)(3)` | Free persons, marriage. |
| `s7703_a_1/5` | cases `bfffb`; internal person bindings inherited from `(a)`, marriage may be bound; S13 free | Free persons, marriage, `Option Day` S13. |
| `s7703_a_2/5` | cases `bfffb`; `(a)` NAF calls `bbbfb` | Free persons, marriage, separation event. |
| `s7703_b/3` | `bbb` after `(a)` grounds both persons | No outputs; retain proof multiplicity. Deferred. |
| `s7703_b_1/4` | `bffb` cases and `(b)` | Household and dependent, both bound before §152 call. Deferred. |
| `s7703_b_2/4` | `bbfb` cases, `(b)`, §2:80,224 with bound taxpayer; §2:290 may receive free taxpayer before kinship binds it | Cost. Free taxpayer inside `findall` is existential and does not escape; a future `fbfb` mode must not enumerate taxpayers. |
| membership helper | `bbb` at :211 | Unit per proof. |
| `s7703_b_3/4` | `bfbb` cases, `bbbb` from `(b)` | Spouse when free, otherwise Unit per proof. |

All reached years in this slice are bound. NAF-local variables never escape.
`s152_a_1` is `bbb` at §7703:139; `s152_c`, `s152_c_1` inherit that mode.
`c_1_A` and `c_2` have bound persons/free optional dates; `c_2_A/B` have
their auxiliary person free. `c_1_B` receives bound dependent/taxpayer/year,
free residence, and possibly unbound relationship dates. `c_1_C/c_3` have
bound persons/year. `c_1_E` is `bfb`; its negated `s7703` is `bffb`.
`is_child_of` is `fbff` at §152:164 and recursively at utils:163; descendant
is `bbff`, or carries already selected optional dates at §152:186.
Sibling/stepsibling is `fbff` at §152:180–181. D3/D7 require tracking optional
date bindings, not treating every absent date as a calendar default.

## Stop-and-report: R5 termination justification

Affected development is stopped at `s7703_b_1`, `s7703_b`, `s7703`, and the
mutually recursive §152 closure. No fuel, V-rule change or replacement design
is implemented. The independent rows above do not reach this recursion.

R5 says every round trip follows a child edge and therefore terminates under
V4. The source also admits a sibling at `section152.pl:178–186`.
`utils.pl:131–144` makes that relation symmetric. The age comparison at
`section152.pl:204` is non-strict (`is_before` means ≤, D3), so equal birth
dates do not break a cycle.

A static witness candidate is two siblings `a,b` with the same 2000-01-01
birth date, separate ongoing marriages `(a,sa)` and `(b,sb)`, and residences
for `a,b` at the same place since 2018-01-01. Give a single `brother_` event
with agent `a` and patient `b`; no child/parent facts, joint returns, payments,
services, plans or stipulations. Query `s7703(a,_,_,2018)`.

The left-to-right path is `s7703(a,sa)` → `b_1(a,home,b)` →
`s152_c(b,a)` → `c_1_E(b,_)` → `s7703(b,sb)` → `b_1(b,home,a)` →
`s152_c(a,b)` → `c_1_E(a,_)` → the initial `s7703(a,sa)` again. There is
no joint return, but the NAF at §152:144 invokes `s7703` **before** looking
for one. There is no payment, but `(b)` invokes `(b)(1) **before** `(b)(2)`.
Same-person residence choices fail kinship before this path; they do not
prevent reaching it. Both spouses lack a residence/kinship witness.

V4's parent-edge graph is empty. V1–V6 hold. V7's domestic relation is empty.
V8's divergent head-of-household condition is false in 2018 and no parent
relation exists. This is static evidence of a missing R5 termination argument;
it has **not** been executed in Prolog and no production `OracleGuards` exists
here to certify `Valid` mechanically.

Narrow question for the orchestrator's numbered Fable consult: does the sibling
path invalidate R5/R9's claim that person-count fuel cannot exhaust under the
signed V-rules; if so, what owner-approved reference-domain/termination
decision replaces that claim? Preserve G1/G9 and do not silently return `[]`
for this cycle. This task does not author its own consult answer.

## Validation and completion boundary

Paused before implementation and compilation of the independent slice. No Prolog
case execution, harness use, owner-meter invocation, case round-trip or parity
result is claimed. Shared Interface changes belong to the orchestrator.
