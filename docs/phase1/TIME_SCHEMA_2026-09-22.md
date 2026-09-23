# Shared time-schema audit — 2026-09-22

Final declaration: `Interface/TIME_SCHEMA.json`, schema version 1, **175
signatures**: all **31 H4.1 stipulated signatures**, all **135 H6.5 queried
signatures**, and **23 additional internal signatures**. H4/H6 overlap in 14
signatures, so their union is 152. Every position has an explicit role; no
missing-signature, missing-position or unknown-role fallback to `term` is
authorized.

**Pre-dispatch concrete stipulated-Day census: k = 0.** All 376 preserved
records were examined, including all 156 stipulated originals. There are 162
concrete Day occurrences, all canonical in-range `str` values, plus four
Day wildcards. No original is excluded by this measured Day check:
`376 - k = 376`. This is not full ValidStip certification or Checkpoint 1.

## Scope and provenance

This sidecar read AGENTS, PLAN, PROTOCOL, HANDOFF, STATE, the approved decisions,
A-014/A-015, original Prolog and retained diagnostic evidence. It did not inspect
`harness/`, `Oracle/`, `gen/`, the meter source, or gate exploits. Only this
report and `Interface/TIME_SCHEMA.json` are written. Main owns admission,
generated Lean tables and `scripts/check_time_schema.py`; no script is created
by this sidecar. No protected files, audit evidence, attribution, commits,
pushes or merges are changed.

Entry parent: `0a2a65ac1313c180bea39d137e6665c01b8e833a`.
Current DECISIONS SHA-256:
`12d534e2ea589f97dfd27d93ddebb88e37cbc259af66ebe7e1b54f03d7f8686a`.
Current manifest SHA-256:
`5ff23beb28eacdf18d4428395e1d96e4fc8123a8f51ae29abc7943bf0f6062b9`.
Schema SHA-256:
`481ac1423006e18234b06aaa9c8fa2e8f246708fcd6f60bd6af1bf59e62b4f59`.

Each JSON `source` is an exact repository-relative `file:line` citation.
The first source points to a predicate head or preserved extra-arity case
clause; subsequent citations identify operative producers/consumers and the
H4/H6 table rows. Roles were assigned by following source dataflow through
`start_`/`end_`, calendar construction, date comparison, extraction,
arithmetic, lists and forwarding calls. Variable-name resemblance is not the
typing rule. Kinship date forwarding is grounded in
`human/sara/sara/statutes/prolog/utils.pl:122,128,149,155,160,164,178,180,187,205,212,226,233,247,254,262,270`.
G2, D1-D7 and H2-H4 determine their interpretation.

## Role contract

| Role | Meaning of this time-only declaration |
| --- | --- |
| `term` | No Day/Year role is declared here. This is not approval of a codec type, general kind, arbitrary compound or unsupported list. |
| `day` | One date, with D1/D2 canonical Gregorian spelling and V3 range when concrete. Preserve its original atom/str tag. |
| `days` | A list of dates, requiring traversal of actual list elements. It does not authorize replacing the list with one date, or changing order, multiplicity or tags. |
| `year` | An integer calendar-year position. Operational query/root years are checked at the applicable boundary; this label does not authorize blanket filtering of preserved stipulation-year literals. |
| `yearText` | A textual calendar year. Check canonical four-ASCII-digit spelling and 1900–2100 bounds without changing the original atom/str tag. This time check does not establish source unification, full kind validity or mode validity. |

Main explicitly authorized `yearText` during review. It is used in exactly
one position; the four other role spellings remain as originally requested.
Role totals: 433 `term`, 112 `year`, 57 `day`, 3 `days`, 1 `yearText`
(606 argument positions).

`modes` copies the H6.5 case-mode strings exactly, in their published order.
A nonqueried row has `modes: []`; this means no H6.5 original case mode is
declared, not that the predicate is unreachable. In particular,
`s7703/4` is present with `[term,term,term,year]`, `stipulation: true`,
`queried: false`. Internal/root wrapper modes remain the implementation
lane's source-mode audit. H6.5's `b` is boundness, not a declaration that an
argument is an input rather than an expected output.

Wildcards retain their exact `kind` and `value`. They supply no concrete
time in this census; they are not silently assigned a year/date or certified
bounded. Missing tuple positions are structural failures, not wildcards.
A wrong-kind concrete value in a declared Day slot is malformed for the D2
time check, not an instruction to reinterpret it.

## Source findings resolved before generation

| Signature and position | Declaration and operative evidence |
| --- | --- |
| `s3306_a_1_B/4`, 2 | **days**, not scalar Day: `section3306.pl:83-87` builds Workday with `findall(Day,...,Workday)`; source duplicates remain. |
| `s3306_a_2_B/6`, 2 | **days**: `section3306.pl:209-214` projects days then applies `list_to_set(Days_list,Workday)`. |
| `s3306_c_1_A_ii/6`, 2 | **days**: forwarding at `section3306.pl:570-571` preserves the preceding list output. |
| `s3306_b_15/5`, 5 | **yearText**: `section3306.pl:416-418` splits both dates, leaves Caly as a string, and compares directly with `@>`. D5, `human/DECISIONS.md:355-360`, explicitly describes two year strings. |
| `s151_b_applies/2`, 2 | **year**: the universal head at `section151.pl:69` is used as `s151_b_applies(Taxp,Taxy)` at `:85`; `:84-86` forwards the same taxable year to `s151_d/3`. The head alone cannot reveal this role. |
| `s2_a_1_A/5`, 4 and 5 | **year, year**: `section2.pl:25-26` converts the death-date year to numeric S5; `:37-41` does taxable-year arithmetic. |
| `s2_a_2_A/5`, 4 | **day**: S31 is populated by `start_` and compared as a date, `section2.pl:109-113`. |
| `s2_b_3_A/3`, 3 | **day**: S119 receives first/last days and participates in `earliest`, `section2.pl:397-419`. |
| `s7703_a_1/5`, 4 | **day**: S13 receives the spouse's death date at `section7703.pl:42`, then date comparisons at `:43-54`. |
| `s7703_a_2/5`, 4 | **term**: S19 is the legal-separation event, `section7703.pl:90-96`; the event's separate date is Divorce_time. |

All shortened source names in this section are under
`human/sara/sara/statutes/prolog/`; JSON contains the full paths.

The original prompt's scalar description of `s3306_a_1_B` and A-015's
undifferentiated Workday list are corrected by these source bodies. No source
semantics is revised. `s3306_b_15` produces a Prolog `str` from
`split_string`, not an integer; both H6.5 modes (`bbbbf`, `bffff`) leave
position 5 free. Its time-role checker must not convert that output to int,
nor equate an atom with a str. Permitting a tagged textual value through a
time-only check does not assert that it unifies with this source output.

The A-015 internal Workday family, employment-day helpers, household-membership
day, relationship intervals and Caly positions are included. The 23 supplemental
entries are listed by the JSON flags. They include the forwarding
`s152_a_2/5`, `s152_d_1_A/5`, `s7703_a/4`, `s7703_b/3` and wage-year
helpers needed to make the source reasoning explicit. This is not a registry
of every internal Prolog predicate or a completed R8 call-coverage proof.

There are **no unresolved role ambiguities in the declared population** after
the authorized `yearText` addition. Any integration that lacks `days` or
`yearText` support must report that mismatch to main; it must not default the
role to `term` or coerce a value.

## Corpus-only extra arities

The following H4.1 rows are retained with every position explicitly `term`:

| Signature | Exact case sources | Canonical source contrast |
| --- | --- | --- |
| `s151_d/4` | `cases/s151_d_2_neg.pl:10`; `cases/s152_d_1_B_neg.pl:15`; `cases/s152_d_1_B_pos.pl:10`; `cases/s152_d_1_D_neg.pl:20`; `cases/s152_d_1_D_pos.pl:18` | Canonical `section151.pl:105` defines `s151_d/3`. |
| `s2_a/5` | `cases/s1_a_2_i_pos.pl:11` | Canonical `section2.pl:4` defines `s2_a/3`. |
| `s63_c_3/4` | `cases/s63_d_2_neg.pl:14` | Canonical `section63.pl:146` defines `s63_c_3/3`. |

Case paths above are relative to `human/sara/sara/`. Static inspection found
no canonical head or call of these three extra arities. Prolog predicate
identity includes arity: similarly named predicates cannot confer their role
positions on these inert appended heads. A year-looking final literal or a
date-looking placeholder is insufficient evidence of an operational time role.
All original arguments remain opaque and preserved, including wildcards. This
does not broaden their general allowed kinds or establish arbitrary future
meta-call reachability.

The older diagnostic's `metadata.json/time_positions` provisionally assigned
a year to all three extra-arity final positions and dates to `s2_a/5`
positions 3/4. Those classifications are not authoritative. The new census has
263 concrete year occurrences instead of 266: remove seven extra-arity
candidate occurrences and include four `s151_b_applies/2` year occurrences.
Its 148 declared wildcard time occurrences replace the provisional 150 count:
the two `s2_a/5` wildcards stay preserved but are not declared dates.

## Preserved stipulated-Day census

Evidence directory:
`docs/contracts/phase1-decision-audit/stip-time-full-20260922-01/`.
No interpreter rerun or evidence overwrite was performed. Every per-case
`audit.json` agrees with `all_results.json`; every recorded case SHA-256 and
all 12 recorded original Prolog hashes match current read-only source. All 376
retained executions have status `ok`, exit 0 and no timeout. These are
appended-clause evaluations with head positions initially unbound;
`original_test_directives_executed` is false.

| Population | Count |
| --- | ---: |
| Original audit records | 376 |
| Originals with stipulations | 156 |
| Stipulated fact / rule clauses | 203 / 28 |
| Preserved appended-clause solutions, with multiplicity | 440 |
| Originals containing declared Day positions / concrete Day values | 13 / 9 |
| Declared Day occurrences | 166 |
| Concrete Day occurrences, all tagged `str` | 162 |
| Canonical and within 1900-01-01 through 2100-12-31 | 162 |
| Wrong-kind / noncanonical / invalid-calendar / out-of-range concrete Days | 0 / 0 / 0 / 0 |
| Day wildcard occurrences | 4 |
| Originals inadmissible from this concrete-Day check, k | **0** |

The seven stipulated Day positions come from four signatures:
`s152_c_2/4` positions 3/4 (four occurrences);
`s152_d_2_H/6` positions 5/6 (ten);
`total_wages_employer/6` positions 5/6 (eight);
`s3306_c/5` position 4 (144, including four wildcards).
No H4.1 stipulated signature has a `days` or `yearText` role.

| Original ID | Concrete Day occurrences | Wildcard Day occurrences |
| --- | ---: | ---: |
| `s152_c_1_neg` | 2 | 0 |
| `s152_c_1_pos` | 2 | 0 |
| `s2_b_3_B_pos` | 10 | 0 |
| `s3301_neg` | 4 | 0 |
| `s3301_pos` | 4 | 0 |
| `s3306_a_1_B_neg` | 10 | 0 |
| `s3306_a_1_B_pos` | 12 | 0 |
| `s3306_a_2_B_neg` | 57 | 0 |
| `s3306_a_2_B_pos` | 61 | 0 |
| `s3306_b_15_neg` | 0 | 1 |
| `s3306_b_15_pos` | 0 | 1 |
| `s3306_b_7_neg` | 0 | 1 |
| `s3306_b_7_pos` | 0 | 1 |

All four Day wildcard records are at clause 1, solution 1, `s3306_c/5`
position 4, exactly `{"kind":"wild","value":0}`. Their associated year
wildcards are exactly `{"kind":"wild","value":1}`. The remaining 140 year
wildcard occurrences are exactly `{"kind":"wild","value":0}`.
No wildcard identity or textual tag was normalized; values are inspected in
memory only.

Required fields for this measurement are present: IDs, source hashes,
clause kind/source, every solution's predicate/arity and full ordered arguments,
and every argument's kind/value. No missing-field limitation prevents this
census. The evidence does not carry a complete operational call trace or a
kernel admission proof. It also is not a census of query outputs or of every
possible future binding of a wildcard.

The existing year findings remain verbatim, without excluding the originals:

```text
s151_d_3_B_neg: s68_b(alice,2015,250000)
  position 3: {"kind":"int","value":250000}
s151_d_3_B_pos: s68_b(alice,2015,250000)
  position 3: {"kind":"int","value":250000}
```

Each literal is at `human/sara/sara/cases/<id>.pl:15`; each actual query
binds its year to 2015 at `:18`. The direct forwarding call is
`human/sara/sara/statutes/prolog/section151.pl:164` (the more precise
citation than the earlier report's `:166-168`). It cannot unify 2015 with
250000. A-014 and P-INTENT require preservation, not argument swapping or a
blanket stipulation-year rejection. This does not prove every operational
year in every possible mode is covered. The old diagnostic's exit 1 remains
recorded; the new Day-only measurement's exit 0 does not relabel that result.

Evidence identities:

- Retained runtime identity:
  `744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92`.
- `all_results.json` SHA-256:
  `1859473a2bd9bbfaebf1d2a858afbd8923502552225d0294646c224dc35eefc1`.
- Per-case audit inventory SHA-256:
  `51eb85cc914093a7d85661ab0782c523ffcc858379dd968c9c8f00e24ebe0abb`.
  Hash input is sorted relative path, NUL, exact file bytes, NUL for each
  `*/audit.json`, as in the command below.

## Exact verification commands and results

Run from `/Users/devrashie/Documents/csProjects/kmla`. The following commands
ran after the final `yearText` declaration; both exited 0. They are read-only
inline audits, not new script files or implementations of either producer.

```sh
python3 -B - <<'PY'
import collections, json, re
from pathlib import Path
s = json.loads(Path('Interface/TIME_SCHEMA.json').read_text())
rows = s['signatures']
by = {(r['predicate'], r['arity']): r for r in rows}
assert s['schema_version'] == 1 and len(by) == len(rows) == 175
allowed = {'term', 'day', 'days', 'year', 'yearText'}
for r in rows:
    assert len(r['roles']) == r['arity'] and set(r['roles']) <= allowed
    assert len(r['modes']) == len(set(r['modes']))
    assert all(len(m) == r['arity'] and set(m) <= {'b', 'f'} for m in r['modes'])
    for cite in r['source']:
        name, line = cite.rsplit(':', 1)
        assert 1 <= int(line) <= len(Path(name).read_text().splitlines()), cite
    name, line = r['source'][0].rsplit(':', 1)
    head = Path(name).read_text().splitlines()[int(line) - 1]
    assert re.match(re.escape(r['predicate']) + r'\(', head)
    assert len(head.split('(', 1)[1].split(')', 1)[0].split(',')) == r['arity']
d = Path('human/DECISIONS.md').read_text()
h4 = d.split('* H4.1', 1)[1].split('* H4.2', 1)[0]
h6 = d.split('* H6.5', 1)[1].split('## NAF', 1)[0]
stips = {(p, int(a)) for p, a in re.findall(r'^\| `([^`/]+)/(\d+)` \|', h4, re.M)}
queries = {}
for p, a, modes in re.findall(r'^\| §[^|]+ \| `([^`/]+)/(\d+)` \| ([^|]+)\|', h6, re.M):
    queries[(p, int(a))] = re.findall(r'`([bf]+)`', modes)
assert {(r['predicate'], r['arity']) for r in rows if r['stipulation']} == stips
assert {(r['predicate'], r['arity']): r['modes'] for r in rows if r['queried']} == queries
a15 = Path('docs/consult/A-015.md').read_text()
for p, a in re.findall(r'`((?:s[0-9][a-zA-Z0-9_]*|total_wages_employer))/(\d+)`', a15):
    assert (p, int(a)) in by
for key in [('s151_d', 4), ('s2_a', 5), ('s63_c_3', 4)]:
    assert set(by[key]['roles']) == {'term'}
    for f in Path('human/sara/sara/statutes/prolog').glob('*.pl'):
        text = re.sub(r'%[^\n]*', '', f.read_text())
        for m in re.finditer(r'\b' + key[0] + r'\(([^()]*)\)', text):
            assert len(m[1].split(',')) != key[1], (key, str(f), m[0])
for key in [('s3306_a_1_B', 4), ('s3306_a_2_B', 6), ('s3306_c_1_A_ii', 6)]:
    assert by[key]['roles'][1] == 'days'
assert by[('s3306_b_15', 5)]['roles'][4] == 'yearText'
assert by[('s151_b_applies', 2)]['roles'] == ['term', 'year']
assert by[('s7703', 4)]['roles'] == ['term', 'term', 'term', 'year']
assert by[('s7703_a_1', 5)]['roles'][3] == 'day'
assert by[('s7703_a_2', 5)]['roles'][3] == 'term'
assert by[('s2_a_1_A', 5)]['roles'][3:] == ['year', 'year']
assert by[('s2_b_3_A', 3)]['roles'] == ['term', 'year', 'day']
print('PASS: 175 signatures; 31 H4.1; 135 exact H6.5 mode lists; 23 internal-only')
print('PASS: A-015 enumerated signatures; all citations/head arities; extra-arity and special-role checks')
print('roles:', dict(collections.Counter(role for r in rows for role in r['roles'])))
PY
```

Result:

```text
PASS: 175 signatures; 31 H4.1; 135 exact H6.5 mode lists; 23 internal-only
PASS: A-015 enumerated signatures; all citations/head arities; extra-arity and special-role checks
roles: {'term': 433, 'year': 112, 'day': 57, 'days': 3, 'yearText': 1}
```

The A-015 coverage check includes the enumerated SARA signatures. Its incidental
mentions of Prolog builtin `split_string/4` are not registry targets.

```sh
python3 -B - <<'PY'
import collections, datetime, hashlib, json, re
from pathlib import Path
base = Path('docs/contracts/phase1-decision-audit/stip-time-full-20260922-01')
rows = json.loads(Path('Interface/TIME_SCHEMA.json').read_text())['signatures']
by = {(r['predicate'], r['arity']): r for r in rows}
files = sorted(base.glob('*/audit.json'))
assert len(files) == 376
records = [json.loads(f.read_text()) for f in files]
combined = json.loads((base / 'all_results.json').read_text())
assert len(combined) == 376 and {a['id']: a for a in combined} == {a['id']: a for a in records}
meta = json.loads((base / 'metadata.json').read_text())
for name, digest in meta['statutes'].items():
    assert hashlib.sha256((Path('human/sara/sara/statutes/prolog') / name).read_bytes()).hexdigest() == digest
counts = collections.Counter()
tags = collections.Counter()
bad, wild, year_findings = [], [], []
stip_ids, day_ids, concrete_ids = set(), set(), set()
inventory = hashlib.sha256()
for f, a in zip(files, records):
    inventory.update(f.relative_to(base).as_posix().encode() + b'\0' + f.read_bytes() + b'\0')
    assert a['id'] == f.parent.name and re.fullmatch(r'[A-Za-z0-9_-]+', a['id'])
    assert a['status'] == 'ok' and a['execution']['exit'] == 0 and not a['execution']['timed_out']
    source = Path('human/sara/sara/cases') / (a['id'] + '.pl')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == a['source_sha256']
    if a['clauses']:
        stip_ids.add(a['id'])
    for ci, clause in enumerate(a['clauses'], 1):
        counts[clause['kind'] + '_clauses'] += 1
        for si, sol in enumerate(clause['solutions'], 1):
            counts['solutions'] += 1
            row = by[(sol['predicate'], sol['arity'])]
            assert row['stipulation'] and len(sol['args']) == sol['arity']
            for pos, (role, arg) in enumerate(zip(row['roles'], sol['args']), 1):
                assert isinstance(arg, dict) and 'kind' in arg and 'value' in arg
                if role == 'term':
                    continue
                assert role in {'day', 'year'}, 'No declared days/yearText stipulation in H4.1'
                tags[(role, arg['kind'])] += 1
                item = dict(id=a['id'], clause=ci, solution=si, signature=sol['predicate']+'/'+str(sol['arity']),
                            position=pos, role=role, argument=arg, source=clause['source'])
                if role == 'day':
                    day_ids.add(a['id'])
                if arg['kind'] == 'wild':
                    wild.append(item)
                    continue
                if role == 'year':
                    if arg['kind'] != 'int' or type(arg['value']) is not int or not 1900 <= arg['value'] <= 2100:
                        year_findings.append(item)
                    continue
                counts['concrete_days'] += 1
                concrete_ids.add(a['id'])
                reason = None
                if arg['kind'] not in {'atom', 'str'} or not isinstance(arg['value'], str):
                    reason = 'wrong-kind'
                elif not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', arg['value']):
                    reason = 'noncanonical-format'
                else:
                    try:
                        value = datetime.date.fromisoformat(arg['value'])
                        if value.isoformat() != arg['value']:
                            reason = 'noncanonical-format'
                        elif not datetime.date(1900,1,1) <= value <= datetime.date(2100,12,31):
                            reason = 'out-of-range'
                    except ValueError:
                        reason = 'invalid-calendar-date'
                if reason:
                    bad.append(dict(item, reason=reason))
                else:
                    counts['canonical_in_range_days'] += 1
print('records/stipulated/day/concrete-day cases:', len(records), len(stip_ids), len(day_ids), len(concrete_ids))
print('counts:', dict(counts))
print('tags:', {role+':'+kind: n for (role,kind),n in sorted(tags.items())})
print('bad_day_arguments:', json.dumps(bad, sort_keys=True))
print('k:', len({item['id'] for item in bad}))
print('year_findings:', json.dumps(year_findings, sort_keys=True))
print('wild_tags:', dict(collections.Counter(item['role']+':'+json.dumps(item['argument'],sort_keys=True) for item in wild)))
print('audit_inventory_sha256:', inventory.hexdigest())
print('PASS: required measured fields present; 376 case hashes and 12 statute hashes match; combined/per-case evidence agrees')
raise SystemExit(1 if bad else 0)
PY
```

Result: exit 0; populations `376 156 13 9`; 203 fact clauses, 28 rule
clauses and 440 solutions; `day:str=162`, `day:wild=4`,
`year:int=263`, `year:wild=144`; `bad_day_arguments=[]`; `k=0`.
The two year findings and exact wildcard tags are printed unchanged, as
reported above. Required fields, all case/statute hashes and combined/per-case
record equality passed.

Development diagnostics: an initial provenance check incorrectly resolved
recorded Prolog basenames outside `statutes/prolog/`; correcting that path
made all 12 hashes match. One preliminary enumeration check incorrectly
included the builtin `split_string/4`; the final check explicitly targets
SARA signatures. An apply_patch context initially omitted a trailing JSON
comma and made no change; the corrected patch installed `yearText`.
No source, expected semantic result, comparison population or fixture was
changed to repair these diagnostics.

Additional commands: `shasum -a 256 Interface/TIME_SCHEMA.json` produced the
schema digest above; `git diff --check -- Interface/TIME_SCHEMA.json
docs/phase1/TIME_SCHEMA_2026-09-22.md` is the final whitespace check.
Main's Lean generation, admission tests, CP0 checks and lane dispatch are
outside this sidecar's claimed validation.

## Self-review

Prolog assumptions: predicate identity includes both name and arity; G4
atom/str identity is tag-sensitive; `split_string` leaves a string unless
`atom_number` explicitly converts it; `findall` returns a list with
multiplicity, while the explicit `list_to_set` in a_2_B deduplicates as
decided; head/body shared variables transmit call-site roles even when the
head is `s151_b_applies(_,_)`; kinship endpoints can remain unbound and
wildcards are not concrete times; a bound integer 2015 cannot unify with
250000. These are checked against cited source and signed decisions, not
inferred from names. No claims are made about full internal mode coverage,
wildcard grounding equivalence, production V7/V8/V10, R5/R8 adequacy, reference
answers or parity.

Circuit breaker: **three failed edit cycles on one test means stop and
report**. That threshold was not reached. The final schema and evidence
checks pass; the preserved two year-literal findings remain findings.
