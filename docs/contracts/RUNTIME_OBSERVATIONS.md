# Runtime observations on the pinned interpreter

**These are observations, not decisions.** They record what SWI-Prolog 7.2.3
actually does on the shipped corpus. Several of them settle questions that
`docs/contracts/DECISION_WORKSHEET.md` had to leave open; the owner still records
the resulting decision in `human/DECISIONS.md`. Nothing here amends a contract —
proposed amendments are in `docs/DECISION_LOG.md`.

Nothing under `human/` was modified: the corpus is mounted read-only.

## Reproducing

```sh
KMLA_TZ=America/New_York bash harness/pin_runtime.sh > docs/contracts/RUNTIME.json
docker run --rm --platform linux/amd64 -e TZ=America/New_York \
  -v "$PWD/human/sara/sara:/corpus:ro" -w /corpus kmla-swipl:7.2.3 \
  -q -f cases/s151_a_pos.pl
```

Interpreter, verified from inside the container: `SWI-Prolog version 7.2.3 for
amd64`, `PLARCH=amd64`, `uname -m = x86_64`, Debian `swi-prolog-nox 7.2.3+dfsg-6`.
Host is `darwin/arm64`, so amd64 runs emulated. See `RUNTIME.json` and DL-001.

---

## O-1. The working directory is the corpus root, and getting it wrong is silent

All 378 consult directives use the relative path `[statutes/prolog/init]`, which
SWI resolves against the **process working directory**.

| Working directory | Result |
| --- | --- |
| corpus root | Loads and runs correctly |
| `cases/` | `source_sink 'statutes/prolog/init' does not exist`, then `Undefined procedure: s151_a/3` — **and still exits 0** |

The harness must `cd` to the corpus root. A wrong working directory produces a
completely unloaded program that is indistinguishable from success by exit status.

## O-2. Exit status carries no information whatsoever

| Situation | Exit | stdout | stderr |
| --- | ---: | --- | --- |
| Directive succeeds | 0 | empty | empty |
| Directive **fails** | 0 | empty | `Warning: … Goal (directive) failed: user:…` |
| Directive **errors** | 0 | empty | `ERROR: …` then the same `Warning:` |
| Statutes never loaded | 0 | empty | `ERROR: source_sink … does not exist` |

Every one of the 376 shipped cases exits **0**, in every configuration tested.
`:- halt.` exits 0 regardless of what came before it.

**Therefore the only available pass/fail signal is stderr text.** A grader must
parse stderr, and must separately distinguish an honest test failure from an
infrastructure failure, because both surface as the same `Goal (directive) failed`
warning. That is the substance of blocker B006 and it is now measured, not
predicted. A positive check that the statutes actually loaded is also required;
otherwise a broken mount scores as 376 passes.

## O-3. `:- discontiguous` is load-bearing, not cosmetic

A case file adding a clause to a statute predicate, with the declaration the
corpus always writes before the consult:

```text
with    :- discontiguous s63/3.   →  s63/3 has 2 clauses: the statute rule AND the case fact
without                           →  s63/3 has 1 clause: the case fact ONLY
                                     stderr: "Redefined static procedure s63/3
                                              Previously defined at …/section63.pl:2"
```

**Without the declaration SWI discards the statute definition entirely.** With it,
SWI appends and warns about nothing.

This resolves B007 benignly for the shipped corpus — every one of the 151 files
that extends a statute predicate does declare it — but it is a knife-edge. Any
serializer that regenerates case files **must** emit those declarations, and any
generated input that extends a statute predicate without one silently destroys the
statute rule rather than failing.

## O-4. The two B005 files are indistinguishable from passing cases

`s3306_c_2_neg.pl` and `s3306_c_2_pos.pl` both terminate in about a second,
exit 0, with **empty stdout and empty stderr** — byte-identical observable
behaviour to a case whose test genuinely succeeds.

The negation cycle documented in `SOURCE_FINDINGS.md` F-001 does **not** loop:
nothing calls `s3306_b/8` during loading, so the injected clause is never tried.
"Keep both and run them as-is" is therefore safe from non-termination. It is not
safe from silence: these two cases assert nothing and no observable signal says so.

## O-5. Corpus baseline: the reference disagrees with its own labels under UTC

Every case run once, classified by stderr:

| TZ | Cases whose own test succeeds | Failures |
| --- | --- | --- |
| `America/New_York` | **376 / 376** | none |
| `UTC` | 374 / 376 | `s3306_a_1_B_neg`, `s3306_a_2_B_neg` |
| `Asia/Tokyo` | 374 / 376 | the same two |

Exactly two cases differ between timezones; the other 374 are identical.

## O-6. Why: a double defect that cancels only in a negative-offset zone

`utils.pl:7` adds one day (`DI1 is DI+1`) before `date_time_stamp/2` builds a
stamp at a **zero UTC offset** (`utils.pl:8`). `format_time/3` renders in **local**
time (`section3306.pl:76`, `:192`, `section7703.pl:210`). In a negative-offset
zone the render moves the date back a day and cancels the `+1`.

Measured on `s3306_a_1_B_neg`, whose ten employment days must fall in ≥10 distinct
`%W` weeks for §3306(a)(1)(B) to apply:

```text
as written   : 9 distinct weeks  [04 05 09 11 13 43 45 47 48]
after +1     : 10 distinct weeks [04 05 09 12 14 43 45 47 48 49]
```

2017-03-19, 2017-04-02 and 2017-12-03 are Sundays. The `+1` pushes each into the
following Monday's week, splitting three collisions and turning 9 into 10. Nine
weeks makes the statute fail and the case's `\+` test succeed — the labelled
answer, "Contradiction". Ten makes the test fail.

JHU is in Baltimore, US Eastern. The published labels are consistent with having
been produced in a negative-offset zone. **`TZ` is part of the artifact's
identity, not an environment detail.** See DL-002 for the options.

## O-7. Arithmetic, typing and flags

Measured directly. These settle worksheet items that were marked needs-runtime.

**Flags:** `bounded=false`, `iso=false`, `double_quotes=string`.
`prefer_rationals` and `max_integer` do not exist in 7.2.3.

| Question | Observation |
| --- | --- |
| `round/1` ties (`money-tie-rule`) | **Half away from zero**, not banker's. `round(4.5)=5`, `round(5.5)=6`, `round(-4.5)=-5`, `round(-0.5)=-1`. Same rule on rationals: `round(9 rdiv 2)=5`. |
| `ceil/1` (`ceil-evaluable`) | **Evaluable.** Both `ceil/1` and `ceiling/1` work; `ceil(1.2)=2`. |
| `Int/Int` (`int-division-flags`) | **Type depends on exactness.** `6/2=3` (integer), `7/2=3.5` (float). So `ceil(Difference/1250)` sees a float when inexact and an integer when exact. `2*ceil(3000/1250)=6`. |
| `Float rdiv Int` (`rdiv-float-operand`) | **Coerces, does not throw.** `2.5 rdiv 2 = 5 rdiv 4`. |
| `min`/`max` typing (`minmax-typing`) | Integer is preserved: `max(3,2.0)=3`, and on a tie `min(3,3.0)=3` returns the integer. |
| Integer width (`integer-width`) | **Unbounded** (GMP). `2**200` is exact. Overflow is not a concern. |
| `duration/3` units (`duration-units`) | **Seconds, as a float.** One day apart = `86400.0`; 2017-01-01 to 2017-12-31 = `31449600.0` (= 364 days; the `+1` cancels within a duration because both endpoints shift). |
| Atom vs string (`D4-atom-vs-string`) | **Distinct terms.** `usa == "usa"` is false and `usa = "usa"` is false; `atom_string(usa,S)` gives `"usa"`. A `Location=="private home"` test only matches the double-quoted form. |

## O-8. `section3306.pl:650` does throw, and no shipped case reaches it

`Day_offset is Dob_d+7671` where `split_string/4` bound `Dob_d` to a string:

```text
X is "15"+7671   →  type_error([],"15"), '"x" must hold one character'
X is "5"+7671    →  7724      (a ONE-character string evaluates as its char code)
date_time_stamp(date("2017",...))  →  type_error(integer,"2017")
```

ISO dates are zero-padded, so `Dob_d` is always two characters and the goal always
raises. `s3306_c_5_B/4` is therefore unusable as written.

No shipped case reaches it: `is_child_of/4` guards the arithmetic and fails first
in `s3306_c_5_neg` (the case asserts only the inert `sibling_`), while
`s3306_c_5_pos` succeeds in `s3306_c_5_A` before `_B` is tried. Both run clean in
the full sweep. **Phase 2 generation will reach it**, and when it does the goal
raises rather than failing — which O-2 shows is invisible in the exit status.

---

## What this leaves open

The observations above answer the *behavioural* questions. They do not answer the
*normative* ones, which remain the owner's:

- Which timezone the experiment pins, and therefore whether the corpus baseline is
  376 or 374 (DL-002).
- Whether Debian's `7.2.3+dfsg-6` satisfies B001 (DL-001).
- Whether the Lean oracle reproduces these behaviours (`round` half-away-from-zero,
  `/` changing type with exactness, a raising `s3306_c_5_B`) or corrects them.
- What the pass/fail protocol is, now that exit status is known to be useless.
