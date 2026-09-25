# G6 diagnostic: domestic service with a free calendar year (R-Q025)

**Diagnosis only.** Dev authorized it on 2026-09-25, to run in the integration
session, emulated on the Mac, lifting the §3306/§3301/tax definedness halt for
this diagnostic alone. Nothing is implemented or installed, and no `Valid`
rule, exclusion, source repair, fuel value or reference answer is applied. The
exclusion proposal below is for Dev to decide.

## Result

**A household that satisfies V1–V10 makes `tax/3` raise. The A-025 finding is
confirmed.** In the pinned runtime, `tax(alice,2017,T)` on `household.pl` raises
`error(instantiation_error, context(system:(is)/2, _))`. The exception-time
backtrace (`commands/001.stdout`) runs:

```text
utils.pl:342              tax(alice,2017,_)        -> s3301
section3301.pl:7          s3301(alice,2017,...)    -> s3306_a
section3306.pl:5          s3306_a(alice,2017)      -> s3306_a_1 -> s3306_a_1_B
section3306.pl:54         s3306_a_1_B(alice,_,_,2017)  findall over :57
section3306.pl:44         s3306_a_1_is_day_of_employment(alice,bob,_)
section3306.pl:441        s3306_c(alice_domestic_service,alice,bob,_,_)
section3306.pl:604        s3306_c_2(alice_domestic_service,"private home",_)
section3306.pl:237        s3306_a_3(alice,_,_,_)   findall
                          _ is _ - 1               (section3306.pl:242, Pyear is Caly-1)
```

The `is/2` frame is a direct child of the `findall` at `:237`, whose goal
(`:240-244`) contains exactly one `is/2`, at `:242`. Caly is free, because `:44`
passes `_`, and the `var(Workday)` branch at `:428` binds nothing. The first
`findall` disjunct fails because there is no payment, so `:242` is reached.
`s1` at `utils.pl:334-340` completed first without raising; frame [11] is at
`:342`.

## What ran

Every command is one `docker run` of the pinned image, by ID
`sha256:8e53d3a0…`. Each run has the corpus mounted read-only at `/corpus` (the
working directory), this directory read-only at `/audit`, no network, a
read-only root and dropped capabilities. `commands/NNN.command.json` holds the
exact argv, the timeout, the exit status and whether it timed out;
`NNN.stdout` and `NNN.stderr` hold the streams verbatim.

**The exit status is the driver's.** `g6_domestic.pl` catches the probe's
outcome and prints it as `result(...)`, then calls `halt(0)`. So exit 0 does
not mean the query succeeded; read each probe's `result(...)` line.

| # | Household | Probe | `result(...)` |
| --- | --- | --- | --- |
| 000 | — | identity (`sh`) | see Identity |
| 001 | household.pl | `tax(alice,2017,T)` (**root**) | **exception: instantiation_error at :242** |
| 002 | household.pl | `s3301(alice,2017,…)` | same exception, same frames |
| 003 | household.pl | `s3306_a(alice,2017)` | same exception |
| 004 | household.pl | `s3306_c(S,alice,E,D,C)` | same exception |
| 005 | household.pl | `s3306_a_3(alice,_,_,C)` | same exception |
| 006 | household.pl | `tax(bob,2017,T)` (control) | success, `T = 0` |
| 007 | household_control.pl | `tax(alice,2017,T)` (control) | success, `T = 0` |
| 008 | household.pl | `is_child_of(bob,alice,_,_)` (V5 support) | failure |
| 009 | household.pl | `findall(D-T, s152_c_2(D,T,_,_), L)` (V10 support) | `L = []` |
| 010 | household.pl | `s151_c_applies(t,D,2017)`, `t ∈ {alice,bob}` (V8 support) | `[]` |
| 011 | — | translator probe | `/run/rosetta/rosetta` |
| 012 | all 376 originals | candidate region (below) | 0 of 376 |
| 013 | household.pl, household_control.pl | instrument controls for 012 | region found / not found |
| 014 | — | translator and swipl digests | match `RUNTIME.json` |

Commands 006, 007 and 013 are controls I added. The household used for 007
differs from `household.pl` only by the `"private home"` location, so the
difference isolates the domestic-location test at `section3306.pl:597-603`,
which feeds `:604`.

The facts are installed with `assertz` after the unchanged statutes are
consulted, as in the 2026-09-23 H4 diagnostic. Order is kept, and the strings
are `str` (the backtrace shows `"private home"`). The exception hook only
prints; it then fails, so it does not change execution.

## Identity

Recorded in `identity.json` and `identity_supplement.json`:
- **Image and interpreter:** ID `sha256:8e53d3a0…`, the image recorded in
  `docs/contracts/RUNTIME.json`, whose label carries the recorded Dockerfile
  SHA-256. SWI-Prolog 7.2.3 for amd64.
- **Time zone:** `TZ=America/New_York` with offsets -0500/-0400, and a tzdata
  digest matching `RUNTIME.json`.
- **Emulated: yes.** The host is macOS arm64, and Docker ran the amd64 image
  through **Rosetta for Linux**. The running process's executable is
  `/run/rosetta/rosetta`; its SHA-256 `e743f8a5…` and the swipl binary's
  `b6d1ff84…` both match `RUNTIME.json` (command 014).
- **Statutes:** all 12 statute files' digests, measured in the container,
  match `human/HASHES.txt`.
- **Protected files:** `human/DECISIONS.md` is `12d534e2…` and the manifest is
  `5ff23beb…`, both unchanged.
- **Tools:** every tool in this directory is pinned by digest in
  `identity_supplement.json`.

## V1–V10: `household.pl` at year 2017 satisfies every premise

The household is a stipulation-free `Household`, with no stipulations, and the
year index is 2017. Each premise is argued from the signed text
(`human/DECISIONS.md:767-853`, with H1–H3 at `596-692`). No production decider
or test instance is relied on. Commands 008–010 are supporting evidence only.

- **V1.** All six facts use declared predicates at their declared arity:
  `service_/1`, `agent_/2`, `patient_/2`, `purpose_/2` and `location_/2`. Their
  argument kinds follow H2: the event id and the people are atoms, and
  `"domestic service"`, `"private home"` and `"usa"` are non-empty strings.
  There are no wildcards and no stipulations. The roles fit H3: the service's
  patient is its employer, and several `location_` facts per event are allowed
  (F12).
- **V2:** there are no `amount_` facts.
- **V3 and V9:** there are no `start_` or `end_` facts, so no `Day` values, and
  2017 lies within 1900–2100.
- **V4:** there are no `son_`, `daughter_`, `father_` or `mother_` events, so
  the kinship graph is empty.
- **V5:** the service's employee, bob, has no `birth_` event, and no kinship
  facts exist (command 008 agrees).
- **V6:** there are no `plan_` events.
- **V7:** there is no `payment_`, so the `⇒` relation is empty. `dom(S)` also
  fails, because there is no `end_` fact. V7 addresses payment cycles
  (divergence), not this raise path, which is why the household lies outside
  every signed V-rule.
- **V8.** `hohCycle` needs the evaluation of `s2_b_1_B(t,…,y)` to reach
  `s151_c` (`section2.pl:309`). The first event literal of `s2_b_1_B`,
  `residence_` at `section2.pl:285`, has no fact here, so `s151_c` is never
  reached for any person or year, and `hohCycle` is false everywhere. Command
  010 supports this but does not establish it: it checks only a downstream
  condition, for two persons.
- **V10.** There are no `birth_` events, so both uniqueness clauses hold
  vacuously. Every branch of `s152_c_2` (`section152.pl:158-187`) starts with
  a kinship literal the household lacks (`utils.pl:98-116, 131-135, 167-169`),
  so `s152_c_2(d,t,_,_)` has no solution for any ground pair, and the all-years
  condition is vacuous. Command 009 is consistent with this, but its unbound
  enumeration alone would not prove the ground-pair universal.

## Effect on the originals: 0 of 376

`g6_originals.pl` (command 012) runs each original in turn. It:
- asserts the case's own facts and case-local rules;
- skips and lists the stipulated clauses of the 31 H4.1 signatures (listed in
  156 files, H4.1's own count);
- restores the H4.4 full stop in the two `s3306_c_2` files (printed as
  `h44_restored`);
- evaluates two candidate regions under a time limit, then erases what it
  asserted.

The two regions:
- `dom0(S)`: a `service_` with a `"domestic service"` type or purpose, a
  location among the four domestic locations, and `s3306_c_A(S,P,E)` or
  `s3306_c_B(S,P,E,_)` for its patient and agent.
- `reach604(S)`: `dom0(S)`, and additionally `s3306_c_1(S,_)` has no solution
  with the year free (`:440`).

**Result: 0 of 376 originals are in either region.** None of the region's
inputs is a stipulated predicate, so skipping stipulations does not affect the
count. Five originals have a domestic service at "private home":
`s3306_a_3_pos/neg`, `s3306_c_2_pos/neg` and `tax_case_92`. Each fails the US
test in `s3306_c_A/B`. `tax_case_92` uses the atom `usa`, which differs from
the string under G4.

The instrument's controls (command 013) find the candidate household in both
regions, with `:441` raising, and find the control household in neither.

## Minimal exclusion proposal (for Dev; not installed)

The candidate rule, drafted as H5 text:

> **V11 (E6, domestic service reached with a free calendar year).** No
> `service_` event `S` such that `type_(S,"domestic service")` or
> `purpose_(S,"domestic service")`; `location_(S,L)` for some `L` in
> {`"private home"`, `"local college club"`, `"local chapter of a college
> fraternity"`, `"local chapter of a college sorority"`} (strings);
> `patient_(S,P)` and `agent_(S,E)` with `s3306_c_A(S,P,E) ∨ s3306_c_B(S,P,E,_)`;
> and `s3306_c_1(S,C)` has no solution with `C` unbound. Any statute entry into
> `s3306_c` with the work day and calendar year unbound that reaches such an `S`
> (`section3306.pl:44, 143, 172, 310, 343, 354, 405`) calls `s3306_a_3` at `:604`
> with the year unbound. That call never returns normally: it raises an
> instantiation error at `:222`, at `:242` or inside `:220`, or does not
> terminate (G6).

**Why this region.** Within one `s3306_c` entry with the year free, the region
is exact. Every such entry that reaches an `S` in it raises, and no raise at
`:604` with a free year can happen outside it. At household level it is the
narrowest year-independent condition that excludes every such raise, given the
roots `Valid` must cover:
- `s3306_a_1_B/4` (case mode `bffb`), whose H6.2 observation enumerates `:57`
  and reaches `:44` for the employer;
- `s3301/6`, whose observation enumerates `s3306_a` and backtracks into
  `s3306_a_1_B`;
- `tax/3` whenever `s3306_a_1_A` does not succeed first, as in this household;
- the free-employer statute modes of `s3306_b_7` and `s3306_b_15`.

If `tax/3` at its first solution were the only root, the rule would
over-exclude: an employer who already paid at least $1,500 in wages elsewhere
passes `s3306_a_1_A` first, and `tax/3` returns. A narrower exclusion scoped to
a target and its bound arguments cannot be written as a V-rule
(`Valid : Household → Year → Prop`) and would be a separate contract change.

**Effect:**
- 0 of the 376 originals are excluded, so the originals and their counts do not
  change.
- Like V10, the rule would apply in both `Valid` and `ValidStip`. No
  stipulation supplies its inputs.
- It overlaps V7's `dom(S)` without replacing it. V7 excludes payment-cycle
  divergence; V11 excludes this raise. Neither subsumes the other: V11 does
  not require `end_` or a payment.
- It changes no source, comparison or observation, and passes no checkpoint.

**Open for Dev:**
- accept, amend or reject V11, and its E6 label;
- whether it goes in both `Valid` and `ValidStip`;
- the installation wording, including where in H5 it sits. Any installation is
  Dev's, followed by a re-pin.

## Limits

- Static reasoning backs the region's claims beyond the executed probes. The
  executed evidence covers one household, two controls and the 376-original
  measurement. Four independent read-only reviewers confirmed the V1–V10
  assessment, the attribution to `:242`, the region's soundness and the 0/376
  count. The minimality caveat above comes from their review.
- `run.py` wrote `identity.json` before the later tools existed; see
  `identity_supplement.json` for the full, final pinning.
- Only one emulated run was made, as Dev specified. There is no native amd64
  CI confirmation.
