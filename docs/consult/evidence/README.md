# Evidence for A-004 / DECISIONS_RECOMMENDED.md

All interpreter runs used the local image `kmla-swipl:7.2.3` (SWI-Prolog
7.2.3, Multi-threaded, 64 bits, Debian 9, `linux/amd64`) executed under
emulation on an arm64 host on 2026-09-21. Under emulation the image ignores
command-line arguments, so every run fed its goal through stdin, e.g.

```sh
echo "consult('/probe/probe1_interpreter_facts.pl')." | \
  docker run --rm -i -v "$PWD:/probe:ro" -e TZ=UTC kmla-swipl:7.2.3 swipl
```

Runs that load the statutes mount the corpus root read-only at `/sara` and
use `-w /sara`; the probe files consult `/sara/statutes/prolog/init`. Banner
lines and singleton warnings were filtered from the saved outputs; nothing
else was edited. Nothing under `human/` was written.

| File | What it shows |
| --- | --- |
| `probe1_interpreter_facts.pl` / `.out.txt` | `round/1` half away from zero (floats and rationals), `rdiv` on floats, `/` int-or-float, `ceil`, `rational(0.5)`, `date_time_stamp` (float, day overflow), string arithmetic `type_error`, atom/string inequality, `atom_prefix`/`sub_atom` on strings, `list_to_set` identity, `%W` labels, `split_string`/`atom_number`, `@>` on strings, `sum_list([])`, `max`/`min`, `==` on `5.0`. |
| `probe2_statute_quirks.pl` / `.out_utc.txt` | Against the real statutes: `s2_b_3_A` start+end quirk (F11); three-fold `s3306_c`/`s3306_b` solutions and triple-counted wages (F12); atom `usa` never matches (F3); `s152` with unbound year raises (F9); duplicate `amount_` facts double count (F13); `latest`/`earliest` with unbound entries; `is_before` on equal, unbound and malformed dates; the §7703(b)(3) day window under UTC; declared-but-undefined predicates fail; `s3306_c_5_B` `type_error` (F8); domestic service without a USA location does not loop. The `s151_d(mia,…)` stack error in this file is caused by the kinship cycle facts of the same file (F7), not by `s151_d` itself; see probe3 section A for the clean run. |
| `probe3_cycles_week_table.pl` / `.out_utc.txt`, `probe3_dates.txt` | Clean `s151_d`/`s151` for a plain taxpayer; kinship cycle → `resource_error(stack)` (F7); domestic service in a USA private home → `resource_error(stack)` in `s3306_c_2`, `s3306_c`, `s3306_a_3` (F5); the `%W` label for 1500 consecutive dates as computed by `day_to_stamp` + `format_time` (compared in Python with C `strftime("%W")` of the following day: 0 mismatches). |
| `probe4_hoh_survivor_tz.pl` / `.out_utc.txt`, `.out_ny.txt` | Same probe under both time zones: `s3306_a_1_B` has no solutions from base facts (F4); the §7703(b)(3) window is Jul 2 … Jan 1 under UTC and Jul 1 … Dec 31 under America/New_York; `%W` of the shifted stamp under UTC versus of the actual day under New York (D8). |
| `probe5_hoh_cycle_survivor.pl` / `.out_ny.txt` | Head-of-household recursion: `s2_b_1_B` exceeds a 90 s limit, `s151_d` and `s151` overflow the stack (F6); an unrelated taxpayer receives applicable amount 300000 first because someone else is a surviving spouse (F10); duplicate identical solutions of `s2_a`. |
| `probe6_rounding_bulk.pl` / `.out.txt` | Float formulas of §1 and §3301 versus `rdiv`-exact evaluation: exhaustive 0 ≤ X ≤ 400,000 per formula, 200,000 exact-tie inputs per tie-admitting rate, 20,000 random inputs per formula up to 10^9, and `ceil(D/1250)`, `ceil(D/2500)` versus integer ceiling for 0 ≤ D ≤ 3,000,000 plus 20,000 random D. The only mismatches are 176 evaluations of `s1_d_ii`'s formula below its bracket (X = 8,575 … 14,175), which the clause's range test makes unreachable (M2). |
| `sweep_directives_utc.tsv`, `sweep_directives_ny.tsv` | Each of the 376 case files consulted as written (`consult('cases/<id>.pl')`, cwd = corpus root): status per file, where `DIRFAIL` means the interpreter printed `Goal (directive) failed`. UTC: 374 OK, 2 DIRFAIL (`s3306_a_1_B_neg`, `s3306_a_2_B_neg`); New York: 376 OK (F1). The two `s3306_c_2` files show OK in both because they contain no executable test (F2). |
| `case_goals.tsv` | The test goal extracted from each case (`\+` stripped; column 2 records `neg`/`pos`), used by the next sweep. The two `s3306_c_2` files were read with the missing full stop restored. |
| `sweep_all_solutions_ny.tsv` | For each case, the copy without its test directives was consulted and `findall(G,G,L)` run on the extracted goal under America/New_York: status, seconds, and `N=` solution count. 138 goals have 0 solutions (all `neg`), 190 have 1, 38 have 2–64 identical solutions (duplicate proof paths), and 2 (`tax_case_83`, `tax_case_91`) exceeded the sweep's 150 s limit; a capped re-run (`forall` with a counter, 1500 s limit) found exactly one solution for each after 118 s and 139 s of backtracking. No goal contradicts its label. |
| `sites_*.tsv` | The `\+`, `is`, `findall`, `sum_list`, `!` and comparison sites extracted from `docs/contracts/HAZARDS.json` (file:line:col, predicate, symbol, construct excerpt); `gen_tables.py` turns them into the tables of `DECISIONS_RECOMMENDED.md`. |
