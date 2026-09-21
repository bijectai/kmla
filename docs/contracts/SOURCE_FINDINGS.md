# Source findings in the designated SARA corpus

Draft for owner review. These are defects and anomalies **in the installed source
archive**, not in anything the assistant produced. Nothing here was repaired,
filtered, or worked around: `human/` is read-only and the approved
design-flaw standard requires reporting rather than silent correction.

Every count below is reproducible from the repository root with:

```sh
python3 -B scripts/inventory_cases.py --self-test
python3 -B scripts/inventory_cases.py --summary
python3 -B scripts/inventory_cases.py | cmp - docs/contracts/CASES.json
```

The scanner is lexical. It performs no Prolog execution, so every claim about
what SWI-Prolog 7.2.3 **does at load time** is marked `needs-runtime` and is an
open question for the owner, not an established result. No interpreter is
installed on this host (`swipl` is absent; the Docker daemon is not running).

Corpus totals: 376 case files, 7,122 clauses, 5,342 facts, 434 rules,
378 consult directives, 218 `discontiguous` directives, 374 test directives,
376 `halt` directives.

---

## F-001 (B005): two cases execute no test at all

`s3306_c_2_neg.pl` and `s3306_c_2_pos.pl` are missing the full stop that ends
line 26. Under ordinary Prolog clause syntax a clause ends only at a full stop
followed by layout; the `% Test` comment on line 28 is skipped by the reader, so
the `:-` on line 29 is read as the neck of the clause that began on line 26.

`human/sara/sara/cases/s3306_c_2_neg.pl:26`, verbatim:

```prolog
:- discontiguous s3306_b/8.          % line 8
:- [statutes/prolog/init].           % line 9
...
amount_(alice_pays,3200).            % line 25
s3306_b(3200,alice_pays,alice_employer,alice,bob,alice,bob,_)   % line 26, no full stop
                                     % line 27 blank
% Test                               % line 28
:- \+ s3306_c_2(alice_employer,_,2017).                          % line 29
:- halt.                                                         % line 30
```

What is actually read is one rule, then one directive:

```prolog
s3306_b(3200,alice_pays,alice_employer,alice,bob,alice,bob,_) :-
    \+ s3306_c_2(alice_employer,_,2017).
:- halt.
```

`s3306_c_2_pos.pl` has the identical defect with the positive guard
(`... :- s3306_c_2(alice_employer,_,2017).`) and `amount_` of 300.

### Consequences

1. **Neither file runs a test.** These are the only 2 of 376 cases with no test
   directive; the scanner reports `files_without_a_test_directive: 2` and names
   exactly these two. The corpus has 374 test directives, not 376.
2. The intended fact becomes **conditional on the very goal under test**. Line 8
   declares `:- discontiguous s3306_b/8.`, which is only needed if line 26 was
   meant to add a clause to the statute predicate `s3306_b/8`; so the author's
   intent was a fact, and the defect turned it into a circular guard.
3. Both cases are in the **train** split (`splits/train:131` and `:132`), so the
   120-case test split is unaffected. The Checkpoint 1 parity gate ("zero
   mismatches on 376 cases") is affected, because its denominator includes them.
4. Any claim of the form "N of 376 cases pass" is an overstatement unless these
   two are separately accounted for. The number of cases that assert anything
   is 374.
5. **The injected clause closes a negation cycle back onto itself.** The clause is
   added to `s3306_b/8`, a statute predicate whose own definition is at
   `section3306.pl:270`. Its body calls `s3306_c_2/3` (`section3306.pl:591`), whose
   final goal is `\+ s3306_a_3(Person,_,_,Caly)` (`:604`); `s3306_a_3/4` (`:236`)
   is a `findall` over `s3306_a_3_is_wages/5` (`:219`), whose **first** goal is
   `s3306_b(Wages,Remuneration,Service,Person,_,_,_,_)` (`:220`) — back into
   `s3306_b/8`, which now carries the case's own clause. The path crosses two
   negation-as-failure barriers in an engine with no tabling. The risk is therefore
   not only that no test runs: the file may not terminate. `needs-runtime`.
6. The injected clause is read at line 26, after the consult at line 9, so it is
   appended *after* the statute's own rule and is tried on backtracking. It is
   therefore live for every `s3306_b/8` call in the program, including
   `section3306.pl:18` and `:105` and `section3301.pl:16`
   (`total_wages_employer/6`) — not only for the intended test.
7. `needs-runtime`: whether SWI-Prolog 7.2.3 emits a warning while loading the
   merged clause, and what the process exit status is, has not been observed.
   Both variable occurrences in the merged clause are the anonymous `_`, so the
   singleton checker has nothing to report, but whether any other diagnostic is
   printed is a runtime question, not a syntactic one.

### What the owner must decide

The assistant may not pick any of these; each changes the reported experiment.

| Option | Consequence |
| --- | --- |
| Exclude both cases; report 374 as the denominator throughout | Cleanest statistics; requires saying so in the paper and in every table |
| Keep both, define their expected outcome as "loads without error, asserts nothing" | Preserves 376 but the two cases test nothing; the gate must not count them as passes. Consequence 5 must be checked first: if the negation cycle does not terminate, "run them as-is" is not a viable option |
| Repair the source (add the full stop) in a **derived** copy, never in `human/` | Changes the artifact; needs an explicit, hashed derivation step and a stated diff from upstream |
| Report upstream to JHU and keep the corpus verbatim pending a reply | Preserves provenance; leaves the blocker open |

Whichever is chosen, `round-trip identity on all 376 cases` (Phase 1.1) needs a
definition that covers these two files, because a serializer that reproduces the
file byte-for-byte must reproduce the missing full stop.

---

## F-002: 151 of 376 cases add clauses to statute predicates

28 predicate signatures head clauses in **both** `cases/` and `statutes/prolog/`.
**151 of the 376 case files** contribute **224** such clauses: 194 facts and 30
rules. Leading signatures: `s63/3` (60), `s7703/4` (26), `s3306_b/8` (20),
`s2_b/3` (19), `s2_a/3` (19), `s151_c_applies/3` (15), `s152_c_1/3` (8),
`s3306_c/5` (8).

Separately, 434 of the 7,122 case clauses are rules overall. The 30 that head a
statute predicate are the sharpest case, because no finite fact set represents
them. Examples, verbatim from `docs/contracts/CASES.json`:

```prolog
% cases/s152_c_1_pos.pl
s152_c_3(bob,alice,Year) :- between(2015,2020,Year).

% cases/s2_a_1_B_pos.pl
s151(bob,_,[charlie],[0],Year) :- between(2014,2017,Year).

% cases/s2_b_1_A_ii_pos.pl
s151_c_applies(bob,charlie,Year) :- between(2015,2019,Year).
```

These are genuinely parameterized over a year; no finite fact set represents
them without enumerating the range. The remaining 404 rule clauses define event
predicates conditionally or define case-local helpers.

The event predicates a flat household record would model are themselves computed
in some cases. Rule-head counts across `cases/`: `start_` 65, `agent_` 60,
`end_` 53, `amount_` 52, `purpose_` 52, `payment_` 50, `patient_` 9, `service_` 5.
Their bodies call `between/3` (81), `atom_concat/3` (71), `member/2` (55),
`first_day_year/2` (54), `last_day_year/2` (51), `split_string/4` (16),
`is_before/2` (8) and `nonvar/1` (4), plus case-local helpers such as
`bob_household_maintenance` (197 calls).

**Consequence.** A facts-only ingestion contract cannot represent the corpus. It
would reject 151 of 376 files outright and silently drop 434 rule clauses across
61 files, changing the answers. This is the concrete form of the ingestion
question recorded in `STATE.md` under B005 and B007.

**Owner decision.** Whether `Interface/Household.lean` models a fact set, an
evaluated event set, or a program; and what `round-trip identity` means when the
round trip must reproduce rules. Options and costs are in
`docs/contracts/DECISION_WORKSHEET.md`.

---

## F-003: 108 facts carry an anonymous variable

108 bodyless clauses contain the anonymous variable `_` and no named variable;
0 contain a named variable. Example: `s151_c(alice,_,2000,2015).`
(`cases/s151_a_neg.pl:15`). These are non-ground facts: the `_` unifies with
anything, so the clause asserts a family of ground facts, not one.

This confirms the count recorded in `STATE.md`. An earlier independent count of
112 came from a scanner that did not mask quoted literals and matched capital
letters inside strings such as `"Walter Brown Family Trust II"`; with literals
masked the count is exactly 108, with 0 named-variable facts. The definition used
is stated in the `definitions` object of `CASES.json`, because the definition is
itself a choice.

**Owner decision.** Whether a Lean `Household` stores `_` as a wildcard, as an
existential, or refuses to ingest such a fact. Refusing loses 108 facts.

---

## F-004: 24 clauses are inert — nothing in the loaded program can reach them

`CASES.json` reports 8 signatures, covering **24 clauses in 22 case files**, that
are asserted by a case and (a) never called from any statute rule body at that
name and arity, (b) never defined by any statute program at that signature, and
(c) never called by any case-file rule either. Matching is by **name/arity**: a
name defined at one arity does not make another arity reachable, and that
distinction is what the two groups below turn on.

| Signature | Clauses | Files | Why nothing reaches it |
| --- | ---: | ---: | --- |
| `retirement_/1` | 11 | 11 | Name never appears in `statutes/prolog/` |
| `s151_d/4` | 5 | 5 | Statutes define `s151_d/3` (`section151.pl:105`) |
| `patient/2` | 2 | 1 | Name never called; see below |
| `sibling_/1` | 2 | 2 | Statutes read `brother_`/`sister_`, never `sibling_` |
| `bob_income/4` | 1 | 1 | Case-local rule nothing calls; see below |
| `medical_institution_/1` | 1 | 1 | Name never appears in `statutes/prolog/` |
| `s2_a/5` | 1 | 1 | Statutes define `s2_a/3` (`section2.pl:4`) |
| `s63_c_3/4` | 1 | 1 | Statutes define `s63_c_3/3` (`section63.pl:146`) |

### Group A: a name the statutes never mention (16 clauses)

`retirement_`, `patient`, `sibling_`, `medical_institution_`, `bob_income/4`.
`events.pl` declares the first four as `discontiguous` (`events.pl:39,45,53,55`),
so the source authors declared predicates the statutes never consult.

Two look like defects rather than deliberate distractors:

- **`patient` vs `patient_`.** The corpus convention is `patient_/2`: 615 fact
  heads and 9 rule heads across `cases/`, 628 textual occurrences in all.
  `patient/2` occurs twice, both in `tax_case_25.pl`. The natural-language
  text of that case reads "Bob is Charlie and Dorothy's son", and the two
  `patient(bob_birth,·)` facts are exactly where `patient_(bob_birth,·)` would
  record the parents. Every statute reference is to `patient_`; `patient` appears
  in the statutes only inside a comment (`section3306.pl:740`) and in
  `events.pl:45`. `needs-runtime`: whether the recorded answer `$259487`
  (`tax_case_25.pl:5,48`) was computed with or without the parent relation cannot
  be settled without running the pinned interpreter.
- **`sibling_` vs `brother_`/`sister_`.** `utils.pl:133-134` consults
  `brother_(Relationship)` and `sister_(Relationship)`; nothing consults
  `sibling_`. The two `sibling_(bob_brother_of_alice)` facts therefore do not
  establish the sibling relation they name. In `s3306_c_5_neg.pl` this happens not
  to change the verdict — the case passes because no parent-child fact exists at
  all — so the case passes for a different reason than its text describes.

`bob_income/4` (`s2_b_3_B_pos.pl:37`) is a case-local generator rule that the
same file never calls: every projection rule beneath it calls
`bob_household_maintenance/4` instead. `tax_case_90.pl:38` defines and uses the
arity-3 form correctly, so this reads as a copy-paste leftover.

### Group B: a statute predicate asserted at the wrong arity (7 clauses)

`s151_d/4` (5 clauses), `s2_a/5` (1), `s63_c_3/4` (1). In each, the statutes
define the name at a **different** arity, so the asserted facts land in a
predicate no rule ever calls:

```prolog
% cases/s151_d_2_neg.pl and four others
s151_d(alice,_,2000,2015).            % arity 4
% statutes/prolog/section151.pl:105
s151_d(Taxp,Ea,Taxy) :- ...           % arity 3
```

These are the three signatures that case files declare `:- discontiguous` but
that `statutes/prolog/` never defines at that arity. A name-only analysis hides
them completely, which is why `inventory_cases.py` matches on name/arity.

### Consequence

These facts are invisible to the Prolog oracle. A Lean oracle that *does* read
them would diverge from Prolog on those cases and fail parity. The Lean side must
ignore them exactly as Prolog does, which is a decision the owner must record
rather than a translator's judgement call. The arity mismatches in Group B are
sharper still: a translator working from the case text will read
`s151_d(alice,_,2000,2015)` as supplying an exemption amount, and the reference
program does not.

Eight further signatures (`bob_household_maintenance/4`,
`alice_household_maintenance/4`, `someone_household_maintenance/4`,
`agricultural_service/3`, `alice_employer/3`, `payment_for_labor/4`,
`bob_income/3`, `joint_return_alice_and_bob/4`) are also never called by the
statutes but **are** called by case-file rules, so they are live case-local
helpers, not dead facts. `CASES.json` separates the two with the
`called_by_case_rules` field; `unreadable_signatures` holds both groups and
`inert_signatures` holds only the dead ones.

---

## F-005: two cases consult the statute program twice

`tax_case_37.pl:8-9` and `tax_case_86.pl:8-9` both contain
`:- [statutes/prolog/init].` twice in succession. The corpus has 378 consult
directives across 376 files for this reason.

`needs-runtime`: SWI's behaviour on reconsulting a file within one session
(whether clauses are replaced, duplicated, or the load is a no-op) determines
whether these two cases behave like the other 374. Until the pinned interpreter
runs, the effect on their recorded answers is unknown.

---

## F-006: case files add clauses to predicates already loaded from another file

218 `discontiguous` directives appear in case files, and they are written
**before** the `:- [statutes/prolog/init].` consult (for example
`cases/s151_a_neg.pl:8-9`). The predicates so declared are statute predicates:
`s63/3` (60 files), `s7703/4` (26), `s2_b/3` (19), `s2_a/3` (19),
`s151_c_applies/3` (15), `s3306_b/8` (10), and others.

This is the source's own mechanism for letting a case add clauses to a statute
predicate. **`needs-runtime`, and it is a prerequisite for everything else:**
SWI-Prolog's handling of clauses for a predicate already loaded from a different
file — append, warn-and-append, or redefine-and-discard — decides what the oracle
actually computes for at least 60 cases. This must be observed on the pinned
7.2.3 image before any translation begins, and the observation belongs in
`DECISIONS.md`.

---

## F-007: a blind spouse contributes 600 to a counter that should hold 1

`section63.pl:358`:

```prolog
s63_f_2(Taxp,Taxy,Counts) :-
    (s63_f_2_A(Taxp,Taxy) -> Count1 is 1; Count1 is 0),
    (s63_f_2_B(Taxp,_,Taxy) -> Count2 is 600; Count2 is 0),   % line 358
    Counts is Count1+Count2.
```

The parallel clause for the aged, `section63.pl:324`, is identical in shape but
uses `Count2 is 1`:

```prolog
s63_f_1(Taxp,Taxy,Counts) :-
    (s63_f_1_A(Taxp,Taxy) -> Count1 is 1; Count1 is 0),
    (s63_f_1_B(Taxp,_,Taxy) -> Count2 is 1; Count2 is 0),     % line 324
    Counts is Count1+Count2.
```

`s63_f/3` then computes `Additional_amounts is (Counts_blind+Counts_aged)*Amount`
(`section63.pl:317`) with `Amount is 600` (`section63.pl:314`). A taxpayer whose
spouse is blind therefore receives roughly **$360,000** of additional standard
deduction instead of $600. The statute comment immediately above, at
`section63.pl:355`, reads "The taxpayer shall be entitled to an additional amount
of $600", so the `$600` from the prose appears to have landed in the counter.

**Reachability.** No shipped case exercises it. Seven case files assert
`blindness_`; in all four numerical tax cases (`tax_case_3`, `tax_case_47`,
`tax_case_89`, and `s63_f_2_B_*`) the blind person is the taxpayer
(`agent_(alice_is_blind,alice)`), which fires `s63_f_2_A` and `Count1 is 1`.
`s63_f_2_B_pos.pl` does target `s63_f_2_B`, but as a boolean entailment
(`Section 63(f)(2)(B) applies to Bob in 2017. Entailment`), which succeeds
whatever the counter holds. The defect is latent until a generator produces a
taxpayer with a blind spouse — which Phase 2.1 will.

**Owner decision.** The Lean oracle must reproduce the reference, including this,
or parity fails. Whether to reproduce it, correct it in a derived copy, or treat
it as a counterfactual is yours. It is also concrete support for the plan's own
framing that results are "consistent with a verified reference", never "faithful
to the statute".

---

## F-008: section 1's nonresident-alien bar is inert across the whole corpus

`section1.pl:28` guards joint filing with a lowercase **atom**:

```prolog
    \+ ( % nonresident aliens can't file jointly
        nonresident_alien_(someone_is_nra),     % line 28 — an atom
        ( agent_(someone_is_nra,Taxp); agent_(someone_is_nra,Spouse) ),
```

The parallel guard in `section2.pl:118` uses a **variable**:

```prolog
    \+ ( % no joint return shall be made if either ... is a nonresident alien
        nonresident_alien_(Someone_is_nra),     % line 118 — a variable
```

`nonresident_alien_/1` is never a clause head in any statute file, so every fact
for it comes from a case. No case file mentions the atom `someone_is_nra`: the
count across all 376 is zero. The inner conjunction therefore always fails, the
`\+` always succeeds, and **§1(a)'s nonresident-alien bar never blocks anything**.

**Owner decision.** As with F-007: reproduce, correct in a derived copy, or treat
as a counterfactual. Record it either way, because a translator reading §1 in
isolation will naturally write the variable form and silently diverge.

---

## F-009: the reference program is not stratified

There is a call cycle through two negation-as-failure edges:

```text
s3306_c/5            section3306.pl:441   \+ s3306_c_2(Service,_,Caly)
  -> s3306_c_2/3     section3306.pl:604   \+ s3306_a_3(Person,_,_,Caly)
  -> s3306_a_3/4     section3306.pl:236   findall over s3306_a_3_is_wages/5
  -> ..._is_wages/5  section3306.pl:220   s3306_b(...)
  -> s3306_b/8       section3306.pl:270   ... -> s3306_c(Employment,_,_,_,Year)
```

That cycle carries 8 negative edges inside a single strongly-connected component,
and it is not the only one. An adversarial re-derivation by Tarjan SCC found
**four** recursive components and **all four are non-stratified**: the §151/§68
component via `section151.pl:118` (`s151_d` → `\+ s151_d_3`) and `section68.pl:88`
(`s68_b_1_C` → `\+ s2_b`); the `s152`/`s152_b_1` component via `section152.pl:5`;
the §152(c) component via `section152.pl:145`; and the §3306 component above.

A logic program with a negative edge inside a recursive cycle has no unique
least model. Its answers are defined **operationally**, by SLDNF resolution order,
not declaratively. Separately, the `s152/3` ↔ `s152_b_1/3` cycle terminates only
because of the extra-logical guard `\+ ( var(Dependent), var(Taxp) )` at
`section152.pl:3`; `var/1` inspects instantiation state and has no counterpart in
a declarative Lean definition.

**Consequence.** This is not a corner of the program. For every predicate in
those four components, "translate the clause to a Lean definition" has no
declarative reading to translate to. The owner must decide what the Lean
oracle is a model of: Prolog's operational behaviour on the pinned interpreter, or
a declarative reading that is knowingly different where stratification fails.
This is the deepest semantic decision in the project and it is not visible from
any single clause. `needs-runtime` to characterise the actual behaviour.

---

## F-010: a set-based interface is refuted by the corpus

`findall/3` retains duplicates and `sum_list/2` sums them. This is observable on
shipped cases, not merely in principle.

`cases/s151_a_pos.pl` asserts exactly one exemption fact,
`s151_c(alice,_,2000,2015).` (line 15), and expects `s151_a(alice,4000,2015)`
(line 18) — **$4,000 from a single $2,000 fact**. The route is
`section151.pl:46-58`: `list_to_set(List_c,Set_c)` deduplicates within one list,
but `append(Set_b,Set_c,List_all_exemptions)` at line 47 does **not** deduplicate
across the two, and `sum_list(Exemptions_list,S2)` at line 58 sums what is left.

**Consequence.** Any Lean interface that models these collections as `Finset`, or
that deduplicates anywhere in this chain, returns 2,000 and fails a shipped case.
Order and multiplicity are part of the observable answer. This constrains
deliverable 2 directly. Note also that the `_` in `s151_c(alice,_,2000,2015)` is
one of the 108 non-ground facts from F-003, so F-003 and F-010 interact: the
wildcard is what lets one clause contribute more than once.

---

## Verification status

| Finding | Established by | Needs the pinned interpreter |
| --- | --- | --- |
| F-001 clause structure | Clause lexing; self-tested | Load-time warning and exit status |
| F-002 rule counts | `CASES.json` | No |
| F-003 108 non-ground facts | `CASES.json` | No |
| F-004 inert clauses | `CASES.json` (`inert_signatures`) | Whether recorded answers assume the typo |
| F-005 double consult | `CASES.json` | Effect of reconsulting |
| F-006 clause addition | `CASES.json` | **Yes — blocking** |
| F-007 blind-spouse counter | `section63.pl:324` vs `:358`, `:314`, `:317` | Only to price the effect |
| F-008 inert NRA guard | `section1.pl:28` vs `section2.pl:118`; 0 of 376 cases | No |
| F-009 non-stratification | Call graph, cited above | Yes — to characterise behaviour |
| F-010 duplicate retention | `section151.pl:46-58`; `s151_a_pos.pl:15,18` | Only to confirm the route |

No Prolog was executed. No file under `human/` was created, modified, moved, or
had its permissions changed while producing this document.
