# Semantic decisions: Phase 0.1 owner draft

Status: **TODO — no owner semantic decisions have been filled.** This is the review template in `docs/contracts/`, not the protected specification in `human/DECISIONS.md`. Owner approval and promotion are required. No translation is authorized by this inventory.

The [build plan](../PLAN.md), [approved protocol](../PROTOCOL.md), and [source contract](SOURCE.md) supply the phase purpose, bootstrap boundary, provenance, and required runtime. Source provenance and hashes are maintained in the source contract, not re-established here. The plan specifies integer cents and day counts; neither representation fixes the unresolved rules below.

The reproducible lexical snapshot is [HAZARDS.json](HAZARDS.json), emitted by [inventory_hazards.py](../../scripts/inventory_hazards.py). It covers every recursively discovered `.pl` file under `human/sara/sara/statutes/prolog/`, including all helpers and declaration/loading files. It does not scan case files or align the statute prose in `human/sara/sara/statutes/source/`. No protected owner material, Oracle code, or harness code was inspected.

Inventory totals: **12 files, 299 clauses/directives, 220 defined predicate signatures, 1,243 distinct observed token sites** (core hazards and supplementary observations combined). The required syntax counts are 150 `\+`, 2 `!`, 43 `findall`, 0 `sumlist`, 12 `sum_list`, 101 `is`, and 315 conservative comparison/order/unification sites. Tags can overlap; comparison sites are not all dates.

| File | NAF | Cut | findall | sumlist | sum_list | is | Comparison candidates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `human/sara/sara/statutes/prolog/events.pl` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `human/sara/sara/statutes/prolog/init.pl` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `human/sara/sara/statutes/prolog/section1.pl` | 7 | 0 | 0 | 0 | 0 | 20 | 36 |
| `human/sara/sara/statutes/prolog/section151.pl` | 7 | 2 | 4 | 0 | 1 | 10 | 11 |
| `human/sara/sara/statutes/prolog/section152.pl` | 14 | 0 | 0 | 0 | 0 | 2 | 40 |
| `human/sara/sara/statutes/prolog/section2.pl` | 30 | 0 | 0 | 0 | 0 | 4 | 45 |
| `human/sara/sara/statutes/prolog/section3301.pl` | 0 | 0 | 6 | 0 | 2 | 1 | 9 |
| `human/sara/sara/statutes/prolog/section3306.pl` | 42 | 0 | 25 | 0 | 4 | 8 | 88 |
| `human/sara/sara/statutes/prolog/section63.pl` | 18 | 0 | 3 | 0 | 1 | 34 | 24 |
| `human/sara/sara/statutes/prolog/section68.pl` | 6 | 0 | 0 | 0 | 0 | 12 | 3 |
| `human/sara/sara/statutes/prolog/section7703.pl` | 8 | 0 | 3 | 0 | 2 | 3 | 23 |
| `human/sara/sara/statutes/prolog/utils.pl` | 18 | 0 | 2 | 0 | 2 | 7 | 36 |

Locations are literal `human/...file:line:column` references: one-based Unicode character columns, tabs counting as one character, with zero-based character offsets and exclusive span ends in JSON. `token` identifies the exact syntax; `construct` retains the complete multiline span; `clause` points to the full enclosing clause in the `clauses` array. Comments and quoted literal contents are excluded from syntax counts but retained in source excerpts. Markdown previews collapse whitespace and stop at 165 characters; **the JSON excerpts are exact and untruncated**.

Verification from the repository root (commands read files and write only to stdout):

```sh
python3 -B scripts/inventory_hazards.py --self-test
python3 -B scripts/inventory_hazards.py | cmp - docs/contracts/HAZARDS.json
python3 -B scripts/inventory_hazards.py | python3 -B -c 'import json,sys; print(json.dumps(json.load(sys.stdin)["summary"], indent=2))'
```

The scanner uses only the Python standard library, never runs Prolog, and exposes no output-file option. The snapshot has no timestamp, absolute workspace path, or filesystem-order dependency. `--repo-root` selects a repository; the source subdirectory remains fixed. Symlinks are refused. Unsupported lexical forms fail instead of returning a partial inventory.

Lexical limitations: this is delimiter balancing and token indexing, not a Prolog parser, call-mode analysis, or semantic proof. Name/arity functor shapes can be terms rather than calls; arithmetic such as `2*(...)` can appear in the functor index as a shape. Quoted functors, bare-atom or variable calls, meta-calls, operator declarations, runtime flags, external definitions, module resolution and arbitrary custom comparison names are not resolved. Unquoted operators embedded as data may resemble syntax; inspect their clauses. A bare data atom `is` is excluded by the operand/functor check. All functor occurrences and complete clauses are retained so these boundaries are visible. No source-to-statute fidelity, runtime success, absence policy, duplicate policy, or termination result is claimed.

## Money

Decision: TODO. Required representation from the plan: integer cents. Source units and conversion to cents: TODO. Rounding rule, tie behavior, negative values, floating versus rational intermediates, division, overflow/error behavior, and rounding stage: TODO. Worked examples: TODO.

Inventory: all 101 `is` sites are listed here, including date, duration and counter arithmetic. This grouping does not assert that each expression is monetary. JSON also records 210 arithmetic observations and 28 noninteger literal observations, including decimal constants, `/`, `rdiv`, `round`, `ceil`, `rational`, `min`, and `max`.

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section1.pl:70:9` | `is` | `s1_a_i/2` | `Tax is round(Taxinc*0.15)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:75:9` | `is` | `s1_a_ii/2` | `Tax is round(5535+(Taxinc-36900)*0.28)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:80:9` | `is` | `s1_a_iii/2` | `Tax is round(20165+(Taxinc-89150)*0.31)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:85:9` | `is` | `s1_a_iv/2` | `Tax is round(35928.50+(Taxinc-140000)*0.36)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:89:9` | `is` | `s1_a_v/2` | `Tax is round(75528.50+(Taxinc-250000)*0.396)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:108:9` | `is` | `s1_b_i/2` | `Tax is round(Taxinc*0.15)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:113:9` | `is` | `s1_b_ii/2` | `Tax is round(4440+(Taxinc-29600)*0.28)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:118:9` | `is` | `s1_b_iii/2` | `Tax is round(17544+(Taxinc-76400)*0.31)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:123:9` | `is` | `s1_b_iv/2` | `Tax is round(33385+(Taxinc-127500)*0.36)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:127:9` | `is` | `s1_b_v/2` | `Tax is round(77485+(Taxinc-250000)*0.396)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:148:9` | `is` | `s1_c_i/2` | `Tax is round(Taxinc*0.15)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:153:9` | `is` | `s1_c_ii/2` | `Tax is round(3315+(Taxinc-22100)*0.28)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:158:9` | `is` | `s1_c_iii/2` | `Tax is round(12107+(Taxinc-53500)*0.31)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:163:9` | `is` | `s1_c_iv/2` | `Tax is round(31172+(Taxinc-115000)*0.36)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:167:9` | `is` | `s1_c_v/2` | `Tax is round(79772+(Taxinc-250000)*0.396)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:195:9` | `is` | `s1_d_i/2` | `Tax is round(Taxinc*0.15)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:200:9` | `is` | `s1_d_ii/2` | `Tax is round(2767.50+(Taxinc-18450)*0.28)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:205:9` | `is` | `s1_d_iii/2` | `Tax is round(10082.50+(Taxinc-44575)*0.31)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:210:9` | `is` | `s1_d_iv/2` | `Tax is round(17964.25+(Taxinc-70000)*0.36)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:214:9` | `is` | `s1_d_v/2` | `Tax is round(37764.25+(Taxinc-125000)*0.396)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:15:16` | `is` | `s151/5` | `S2 is Total_ex_taxpayer+Total_ex_spouse` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:129:8` | `is` | `s151_d_1/1` | `Ea is 2000` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:140:8` | `is` | `s151_d_2/4` | `Ea is 0` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:156:22` | `is` | `s151_d_3_A/7` | `Reduction_amount is round( (Exemption_amount_in*Ap) rdiv 100)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:157:8` | `is` | `s151_d_3_A/7` | `Ea is max(Exemption_amount_in-Reduction_amount,0)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:165:16` | `is` | `s151_d_3_B/5` | `Difference is max(Agi-Aa,0)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:180:20` | `is` | `s151_d_3_B/5` | `Number is 2*ceil(Difference/1250)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:183:20` | `is` | `s151_d_3_B/5` | `Number is 2*ceil(Difference/2500)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:186:8` | `is` | `s151_d_3_B/5` | `Ap is min(Number,100)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:193:8` | `is` | `s151_d_5/2` | `Ea is 0` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:134:24` | `is` | `s152_c_1_B/6` | `Half_year_duration is Taxy_duration rdiv 2` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:227:10` | `is` | `s152_c_3/3` | `Taxy_25 is Taxy+25` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:37:11` | `is` | `s2_a_1_A/5` | `Taxy2 is Taxy-2` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:40:11` | `is` | `s2_a_1_A/5` | `Taxy1 is Taxy-1` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:183:31` | `is` | `s2_b_1/4` | `Taxy1 is Taxy+1` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:249:24` | `is` | `s2_b_1_A/4` | `Half_year_duration is Taxy_duration rdiv 2` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:9:9` | `is` | `s3301/6` | `Tax is round(0.06*Wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:33:11` | `is` | `s3306_a_1_A/3` | `Pyear is Caly-1` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:52:11` | `is` | `s3306_a_1_B/4` | `Year1 is Caly-1` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:119:11` | `is` | `s3306_a_2_A/4` | `Pyear is Caly-1` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:167:11` | `is` | `s3306_a_2_B/6` | `Year1 is Caly-1` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:242:11` | `is` | `s3306_a_3/4` | `Pyear is Caly-1` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:306:19` | `is` | `s3306_b_1/2` | `Remuneration2 is min(7000,Remuneration)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:522:11` | `is` | `s3306_c_1_A_i/5` | `Year1 is Caly-1` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:650:20` | `is` | `s3306_c_5_B/4` | `Day_offset is Dob_d+7671` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:10:9` | `is` | `s63/3` | `Taxinc is max(Taxable_income_tmp,0)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:20:8` | `is` | `s63_a/5` | `Ded63 is Total_deduction_reduced + Exemption_151` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:21:24` | `is` | `s63_a/5` | `Taxable_income_tmp is Grossinc - Ded63` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:22:9` | `is` | `s63_a/5` | `Taxinc is max(Taxable_income_tmp,0)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:32:24` | `is` | `s63_b/4` | `Taxable_income_tmp is Grossinc - Amount1 - Amount2` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:33:9` | `is` | `s63_b/4` | `Taxinc is max(Taxable_income_tmp,0)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:59:21` | `is` | `s63_c_1/3` | `Standed is Bassd+Addsd` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:69:19` | `is` | `s63_c_1_A/3` | `Bassd is min(Basic_amount,Max_amount)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:73:19` | `is` | `s63_c_1_A/3` | `Bassd is Basic_amount` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:89:15` | `is` | `s63_c_2/3` | `Bassd is Multiplier*Default_amount` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:107:16` | `is` | `s63_c_2_A/3` | `Multiplier is 2` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:131:19` | `is` | `s63_c_2_B/3` | `Bassd is 4400` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:140:15` | `is` | `s63_c_2_C/2` | `Bassd is 3000` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:161:13` | `is` | `s63_c_5/5` | `Amount1 is 500` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:163:13` | `is` | `s63_c_5/5` | `Amount2 is 250+Grossinc` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:164:11` | `is` | `s63_c_5/5` | `Bassd is max(Amount1,Amount2)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:173:13` | `is` | `s63_c_6/3` | `Standed is 0` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:260:12` | `is` | `s63_c_7_i/2` | `Amount is 18000` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:266:12` | `is` | `s63_c_7_ii/2` | `Amount is 12000` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:314:20` | `is` | `s63_f/3` | `Amount is 600` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:317:24` | `is` | `s63_f/3` | `Additional_amounts is (Counts_blind+Counts_aged)*Amount` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:323:37` | `is` | `s63_f_1/3` | `Count1 is 1` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:323:50` | `is` | `s63_f_1/3` | `Count1 is 0` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:324:39` | `is` | `s63_f_1/3` | `Count2 is 1` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:324:52` | `is` | `s63_f_1/3` | `Count2 is 0` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:325:12` | `is` | `s63_f_1/3` | `Counts is Count1+Count2` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:334:12` | `is` | `s63_f_1_A/2` | `Taxy65 is Taxy+65` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:347:12` | `is` | `s63_f_1_B/3` | `Taxy65 is Taxy+65` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:357:37` | `is` | `s63_f_2/3` | `Count1 is 1` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:357:50` | `is` | `s63_f_2/3` | `Count1 is 0` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:358:39` | `is` | `s63_f_2/3` | `Count2 is 600` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:358:54` | `is` | `s63_f_2/3` | `Count2 is 0` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:359:12` | `is` | `s63_f_2/3` | `Counts is Count1+Count2` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:387:12` | `is` | `s63_f_3/3` | `Amount is 750` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:5:31` | `is` | `s68/4` | `Amount_deductions_out is Amount_deductions_in` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:11:35` | `is` | `s68/4` | `Amount_deductions_out is Amount_deductions_in-Reduction` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:15:35` | `is` | `s68/4` | `Amount_deductions_out is Amount_deductions_in` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:28:8` | `is` | `s68_a/6` | `S7 is min(Reduction1,Reduction2)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:32:7` | `is` | `s68_a_1/3` | `X is 3*(Agi-Aa)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:33:8` | `is` | `s68_a_1/3` | `S9 is round(X rdiv 100)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:38:7` | `is` | `s68_a_2/4` | `X is 80*Itemded` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:39:9` | `is` | `s68_a_2/4` | `S14 is round(X rdiv 100)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:53:12` | `is` | `amount/2` | `Amount is 300000` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:55:12` | `is` | `amount/2` | `Amount is 275000` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:57:12` | `is` | `amount/2` | `Amount is 250000` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:60:12` | `is` | `amount/2` | `Amount is round(Amount_A rdiv 2)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:21:8` | `is` | `s7703_a_1/5` | `Taxy1 is Taxy+1` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:137:24` | `is` | `s7703_b_1/4` | `Half_year_duration is Taxy_duration rdiv 2` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:183:8` | `is` | `s7703_b_2/4` | `Ratio is Payment_by_individual rdiv Cost` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:7:6` | `is` | `day_to_stamp/2` | `DI1 is DI+1` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:95:11` | `is` | `duration/3` | `Duration is Stamp2-Stamp1` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:286:26` | `is` | `gross_income/3` | `Gross_income is Income_individual+Income_spouse` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:330:18` | `is` | `gross_income_individual/3` | `Gross_income is Income+Payment` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:338:24` | `is` | `tax/3` | `Income_tax is 0` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:345:28` | `is` | `tax/3` | `Employment_tax is 0` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:348:9` | `is` | `tax/3` | `Tax is Income_tax+Employment_tax` | TODO |

Supplementary arithmetic observations (these are not resolved builtin semantics):

| Lexical spelling | Sites | Example locations (all locations in HAZARDS.json) | Decision |
| --- | ---: | --- | --- |
| `-` | 40 | `human/sara/sara/statutes/prolog/section1.pl:75:30`; `human/sara/sara/statutes/prolog/section1.pl:80:31`; `human/sara/sara/statutes/prolog/section1.pl:85:34` | TODO |
| `*` | 28 | `human/sara/sara/statutes/prolog/section1.pl:70:24`; `human/sara/sara/statutes/prolog/section1.pl:75:37`; `human/sara/sara/statutes/prolog/section1.pl:80:38` | TODO |
| `/` | 63 | `human/sara/sara/statutes/prolog/events.pl:1:24`; `human/sara/sara/statutes/prolog/events.pl:2:38`; `human/sara/sara/statutes/prolog/events.pl:3:32` | TODO |
| `+` | 33 | `human/sara/sara/statutes/prolog/section1.pl:75:22`; `human/sara/sara/statutes/prolog/section1.pl:80:23`; `human/sara/sara/statutes/prolog/section1.pl:85:26` | TODO |
| `ceil` | 2 | `human/sara/sara/statutes/prolog/section151.pl:180:25`; `human/sara/sara/statutes/prolog/section151.pl:183:25` | TODO |
| `max` | 6 | `human/sara/sara/statutes/prolog/section151.pl:157:11`; `human/sara/sara/statutes/prolog/section151.pl:165:19`; `human/sara/sara/statutes/prolog/section63.pl:10:12` | TODO |
| `min` | 4 | `human/sara/sara/statutes/prolog/section151.pl:186:11`; `human/sara/sara/statutes/prolog/section3306.pl:306:22`; `human/sara/sara/statutes/prolog/section63.pl:69:22` | TODO |
| `rational` | 1 | `human/sara/sara/statutes/prolog/section7703.pl:184:9` | TODO |
| `rdiv` | 8 | `human/sara/sara/statutes/prolog/section151.pl:156:57`; `human/sara/sara/statutes/prolog/section152.pl:134:41`; `human/sara/sara/statutes/prolog/section2.pl:249:41` | TODO |
| `round` | 25 | `human/sara/sara/statutes/prolog/section1.pl:70:12`; `human/sara/sara/statutes/prolog/section1.pl:75:12`; `human/sara/sara/statutes/prolog/section1.pl:80:12` | TODO |

TODO observation: numeric comparisons, source decimal constants and rational expressions require an explicit owner rule before integer-cents arithmetic can be implemented. No coercion, rounding or unit scaling has been selected.

## Dates

Decision: TODO. Required representation from the plan: day counts. Epoch: TODO. Interval boundaries per predicate: TODO. Calendar/leap-year rules, timezone, date parsing, timestamp units, overflow days and year handling: TODO.

Inventory: all 315 comparison candidates are listed, including arithmetic comparison, equality/unification/identity, term ordering, `between`, `min`/`max`, list membership/deduplication, atom prefix/substring relations, and the temporal helpers. Broad inclusion is intentional: names such as `Taxy`, `Duration`, or `Stamp` do not prove a type. There are **104 source-witness sites and 211 sites needing human confirmation**.

`Source witness` corresponds to JSON `source_proven_date_use`: 103 `is_before/2` uses and its internal `=<`. The script checks the exact token sequences of `day_to_stamp/2` (`human/sara/sara/statutes/prolog/utils.pl:2:1`) and `is_before/2` (`human/sara/sara/statutes/prolog/utils.pl:10:1`), which connect those sites to `date_time_stamp(date(...), ...)`. This proves only the explicit source use of date conversion, not argument types, runtime behavior, interval interpretation, or translation. A change to either helper demotes the label. `earliest`/`latest`, year bounds, duration comparisons and explicit timestamp operands remain `Confirm`; lexical co-occurrence is not a dataflow proof. Every decision still says TODO.

| Source token location | Syntax | Enclosing predicate | Construct preview | Date evidence | Decision |
| --- | --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section1.pl:36:27` | `=` | `s1_a_1/6` | `Start_time=First_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:43:25` | `=` | `s1_a_1/6` | `End_time=Last_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:47:9` | `is_before` | `s1_a_1/6` | `is_before(Start_time,Last_day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:48:9` | `is_before` | `s1_a_1/6` | `is_before(First_day,End_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:69:12` | `=<` | `s1_a_i/2` | `Taxinc =< 36900` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:73:12` | `=<` | `s1_a_ii/2` | `Taxinc =< 89150` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:74:11` | `<` | `s1_a_ii/2` | `36900 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:78:12` | `=<` | `s1_a_iii/2` | `Taxinc =< 140000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:79:11` | `<` | `s1_a_iii/2` | `89150 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:83:12` | `=<` | `s1_a_iv/2` | `Taxinc =< 250000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:84:12` | `<` | `s1_a_iv/2` | `140000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:88:12` | `<` | `s1_a_v/2` | `250000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:107:12` | `=<` | `s1_b_i/2` | `Taxinc =< 29600` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:111:12` | `=<` | `s1_b_ii/2` | `Taxinc =< 76400` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:112:11` | `<` | `s1_b_ii/2` | `29600 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:116:12` | `=<` | `s1_b_iii/2` | `Taxinc =< 127500` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:117:11` | `<` | `s1_b_iii/2` | `76400 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:121:12` | `=<` | `s1_b_iv/2` | `Taxinc =< 250000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:122:12` | `<` | `s1_b_iv/2` | `127500 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:126:12` | `<` | `s1_b_v/2` | `250000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:147:12` | `=<` | `s1_c_i/2` | `Taxinc =< 22100` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:151:12` | `=<` | `s1_c_ii/2` | `Taxinc =< 53500` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:152:11` | `<` | `s1_c_ii/2` | `22100 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:156:12` | `=<` | `s1_c_iii/2` | `Taxinc =< 115000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:157:11` | `<` | `s1_c_iii/2` | `53500 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:161:12` | `=<` | `s1_c_iv/2` | `Taxinc =< 250000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:162:12` | `<` | `s1_c_iv/2` | `115000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:166:12` | `<` | `s1_c_v/2` | `250000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:194:12` | `=<` | `s1_d_i/2` | `Taxinc =< 18450` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:198:12` | `=<` | `s1_d_ii/2` | `Taxinc =< 44575` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:199:11` | `<` | `s1_d_ii/2` | `18450 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:203:12` | `=<` | `s1_d_iii/2` | `Taxinc =< 70000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:204:11` | `<` | `s1_d_iii/2` | `44575 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:208:12` | `=<` | `s1_d_iv/2` | `Taxinc =< 125000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:209:11` | `<` | `s1_d_iv/2` | `70000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:213:12` | `<` | `s1_d_v/2` | `125000 < Taxinc` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:40:5` | `list_to_set` | `s151_individual/5` | `list_to_set(List_b_2,Set_b)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:46:5` | `list_to_set` | `s151_individual/5` | `list_to_set(List_c,Set_c)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:50:9` | `member` | `s151_individual/5` | `member((Person,_),List_all_exemptions)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:55:9` | `member` | `s151_individual/5` | `member((_,Exemption),List_all_exemptions)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:119:24` | `=` | `s151_d/3` | `Ea = Exemption_in` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:135:10` | `\==` | `s151_d_2/4` | `Taxp \== Otaxp` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:154:8` | `>` | `s151_d_3_A/7` | `Agi>Aa` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:157:11` | `max` | `s151_d_3_A/7` | `max(Exemption_amount_in-Reduction_amount,0)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:165:19` | `max` | `s151_d_3_B/5` | `max(Agi-Aa,0)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:186:11` | `min` | `s151_d_3_B/5` | `min(Number,100)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:192:5` | `between` | `s151_d_5/2` | `between(2018,2025,Taxy)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:4:14` | `\==` | `s152/3` | `Dependent\==Taxp` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:77:16` | `=` | `s152_c_1_A/4` | `End_t = Death_taxpayer_time` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:77:50` | `=` | `s152_c_1_A/4` | `End_t = End_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:84:16` | `=` | `s152_c_1_A/4` | `End_i = Death_individual_time` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:84:52` | `=` | `s152_c_1_A/4` | `End_i = End_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:86:2` | `earliest` | `s152_c_1_A/4` | `earliest([End_t,End_i,End_day],End_relationship)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:130:5` | `earliest` | `s152_c_1_B/6` | `earliest([End_individual,End_taxpayer,Last_day_of_year,End_relationship],End_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:132:5` | `latest` | `s152_c_1_B/6` | `latest([Start_individual,Start_taxpayer,First_day_of_year,Start_relationship],Start_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:136:11` | `>=` | `s152_c_1_B/6` | `Duration >= Half_year_duration` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:167:13` | `=` | `s152_c_2_A/5` | `Dependent=Childc2a` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:168:22` | `=` | `s152_c_2_A/5` | `Start_relationship=Start_child` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:169:20` | `=` | `s152_c_2_A/5` | `End_relationship=End_child` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:172:14` | `\==` | `s152_c_2_A/5` | `Dependent \== Childc2a` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:184:13` | `==` | `s152_c_2_B/5` | `S65 == Bsssc2b` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:204:13` | `is_before` | `s152_c_3/3` | `is_before(Taxpayer_dob,Individual_dob)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:230:17` | `=<` | `s152_c_3/3` | `Age_individual =< Duration_25_years` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:254:16` | `=` | `s152_d_1_A/5` | `End_t = Death_taxpayer_time` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:254:50` | `=` | `s152_d_1_A/5` | `End_t = End_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:261:16` | `=` | `s152_d_1_A/5` | `End_i = Death_individual_time` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:261:52` | `=` | `s152_d_1_A/5` | `End_i = End_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:263:2` | `earliest` | `s152_d_1_A/5` | `earliest([End_t,End_i,End_day],End_relationship)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:269:18` | `==` | `s152_d_1_B/2` | `Gross_income == 0` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:295:13` | `=` | `s152_d_2_A/4` | `Dependent=Child` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:296:13` | `=` | `s152_d_2_A/4` | `Start_day=Start_child` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:297:11` | `=` | `s152_d_2_A/4` | `End_day=End_child` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:300:14` | `\==` | `s152_d_2_A/4` | `Dependent \== Child` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:324:5` | `latest` | `s152_d_2_E/5` | `latest([Start_day_sibling,Start_day_child],Start_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:325:5` | `earliest` | `s152_d_2_E/5` | `earliest([End_day_sibling,End_day_child],End_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:331:5` | `latest` | `s152_d_2_F/5` | `latest([Start_day_sibling,Start_day_child],Start_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:332:5` | `earliest` | `s152_d_2_F/5` | `earliest([End_day_sibling,End_day_child],End_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:344:15` | `\==` | `s152_d_2_H/6` | `Dependent \== Taxp` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:352:9` | `is_before` | `s152_d_2_H/6` | `is_before(Start,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:356:4` | `is_before` | `s152_d_2_H/6` | `is_before(First_day_year,End)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:365:5` | `is_before` | `s152_d_2_H/6` | `is_before(Start_taxpayer_residence,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:369:3` | `is_before` | `s152_d_2_H/6` | `is_before(Last_day_year,End_taxpayer_residence)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:377:5` | `is_before` | `s152_d_2_H/6` | `is_before(Start_individual_residence,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:381:3` | `is_before` | `s152_d_2_H/6` | `is_before(Last_day_year,End_individual_residence)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:385:5` | `latest` | `s152_d_2_H/6` | `latest([Start_taxpayer_residence,Start_individual_residence],Start_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:386:5` | `earliest` | `s152_d_2_H/6` | `earliest([End_taxpayer_residence,End_individual_residence],End_day)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:387:6` | `==` | `s152_d_2_H/6` | `S145==S143` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:20:10` | `\==` | `s2_a_1_A/5` | `Taxp \== Spouse` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:27:5` | `is_before` | `s2_a_1_A/5` | `is_before(Start_marriage,Time_death)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:34:13` | `is_before` | `s2_a_1_A/5` | `is_before(Time_death,End_marriage)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:39:5` | `is_before` | `s2_a_1_A/5` | `is_before(First_day_year,Time_death)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:42:5` | `is_before` | `s2_a_1_A/5` | `is_before(Time_death,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:55:5` | `is_before` | `s2_a_1_B/4` | `is_before(Start_taxpayer_residence,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:62:13` | `is_before` | `s2_a_1_B/4` | `is_before(Last_day_year,End_taxpayer_residence)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:70:5` | `is_before` | `s2_a_1_B/4` | `is_before(Start_dependent_residence,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:77:13` | `is_before` | `s2_a_1_B/4` | `is_before(Last_day_year,End_dependent_residence)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:87:9` | `is_before` | `s2_a_1_B/4` | `is_before(Start_dependent,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:91:9` | `is_before` | `s2_a_1_B/4` | `is_before(Last_day_year,End_dependent)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:110:16` | `\==` | `s2_a_2_A/5` | `Remarriage \== Previous_marriage` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:111:5` | `is_before` | `s2_a_2_A/5` | `is_before(Start_previous_marriage,S31)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:113:5` | `is_before` | `s2_a_2_A/5` | `is_before(S31,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:130:17` | `is_before` | `s2_a_2_B/3` | `is_before(Start_nra,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:140:17` | `is_before` | `s2_a_2_B/3` | `is_before(First_day_year,End_nra)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:159:16` | `\==` | `s2_b_1/4` | `Spouse \== Taxp` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:162:9` | `is_before` | `s2_b_1/4` | `is_before(Start_marriage,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:171:25` | `is_before` | `s2_b_1/4` | `is_before(Last_day_year,Death_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:185:25` | `is_before` | `s2_b_1/4` | `is_before(First_day_year1,End_marriage)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:213:9` | `is_before` | `s2_b_1_A/4` | `is_before(Start_taxpayer_residence,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:220:9` | `is_before` | `s2_b_1_A/4` | `is_before(Last_day_year,End_taxpayer_residence)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:232:40` | `=` | `s2_b_1_A/4` | `Start_individual_residence = First_day_year` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:241:38` | `=` | `s2_b_1_A/4` | `End_individual_residence = Last_day_year` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:250:35` | `>=` | `s2_b_1_A/4` | `Duration_individual_residence >= Half_year_duration` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:289:5` | `is_before` | `s2_b_1_B/5` | `is_before(Start_dependent_residence,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:297:13` | `is_before` | `s2_b_1_B/5` | `is_before(Last_day_year,End_dependent_residence)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:302:9` | `is_before` | `s2_b_1_B/5` | `is_before(Start_child,First_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:306:9` | `is_before` | `s2_b_1_B/5` | `is_before(Last_day_year,End_child)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:323:10` | `\==` | `s2_b_2_A/5` | `Taxp \== Spouse` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:332:5` | `is_before` | `s2_b_2_A/5` | `is_before(Divorce_time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:349:13` | `is_before` | `s2_b_2_B/3` | `is_before(Start_nra,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:358:13` | `is_before` | `s2_b_2_B/3` | `is_before(First_day_year,Stop_nra)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:379:13` | `is_before` | `s2_b_2_C/4` | `is_before(Time_death,End_marriage)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:382:5` | `is_before` | `s2_b_2_C/4` | `is_before(First_day_year,Time_death)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:383:5` | `is_before` | `s2_b_2_C/4` | `is_before(Time_death,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:404:17` | `=` | `s2_b_3_A/3` | `S119=First_day_year` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:408:13` | `is_before` | `s2_b_3_A/3` | `is_before(Start_nra,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:409:17` | `=` | `s2_b_3_A/3` | `S119=Last_day_year` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:418:13` | `is_before` | `s2_b_3_A/3` | `is_before(First_day_year,Stop_nra)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:419:13` | `earliest` | `s2_b_3_A/3` | `earliest([S119,Stop_nra],S119)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:443:13` | `is_before` | `s2_b_3_B/3` | `is_before(Start_relationship,First_day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:447:13` | `is_before` | `s2_b_3_B/3` | `is_before(End_relationship,Last_day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:453:9` | `is_before` | `s2_b_3_B/3` | `is_before(StartH,First_day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:457:9` | `is_before` | `s2_b_3_B/3` | `is_before(Last_day,EndH)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:18:13` | `is_before` | `total_wages_employer/6` | `is_before(Start_day,Remuneration_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:19:13` | `is_before` | `total_wages_employer/6` | `is_before(Remuneration_time,End_day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:25:9` | `member` | `total_wages_employer/6` | `member((Individual,_,_),Individuals_x_wages)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:28:5` | `list_to_set` | `total_wages_employer/6` | `list_to_set(Individual_list,Individual_set)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:32:13` | `member` | `total_wages_employer/6` | `member(Individual, Individual_set)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:35:17` | `member` | `total_wages_employer/6` | `member((Individual,Wage,_),Individuals_x_wages)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:46:13` | `member` | `total_wages_employer/6` | `member(Individual,Individual_set)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:47:13` | `member` | `total_wages_employer/6` | `member((Individual,Wage),Individuals_x_capped_wages)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:54:9` | `member` | `total_wages_employer/6` | `member((_,_,Service),Individuals_x_wages)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:21:5` | `is_before` | `s3306_a_1_is_wages/4` | `is_before(Time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:23:5` | `is_before` | `s3306_a_1_is_wages/4` | `is_before(First_day_year,Time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:40:7` | `>=` | `s3306_a_1_A/3` | `Wages>=1500` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:58:13` | `is_before` | `s3306_a_1_B/4` | `is_before(First_day_year1,Day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:59:13` | `is_before` | `s3306_a_1_B/4` | `is_before(Day,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:66:9` | `member` | `s3306_a_1_B/4` | `member((Stamp,_,_),Stamp_day_individual)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:69:5` | `list_to_set` | `s3306_a_1_B/4` | `list_to_set(Emp_days,Emp_days_set)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:71:10` | `>=` | `s3306_a_1_B/4` | `Num_days>=10` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:75:4` | `member` | `s3306_a_1_B/4` | `member(Stamp,Emp_days)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:80:2` | `list_to_set` | `s3306_a_1_B/4` | `list_to_set(Weeks,Weeks_set)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:82:11` | `>=` | `s3306_a_1_B/4` | `Num_weeks>=10` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:85:9` | `member` | `s3306_a_1_B/4` | `member((_,Day,_),Stamp_day_individual)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:90:9` | `member` | `s3306_a_1_B/4` | `member((_,_,Individual),Stamp_day_individual)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:108:5` | `is_before` | `s3306_a_2_is_wages/5` | `is_before(Time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:110:5` | `is_before` | `s3306_a_2_is_wages/5` | `is_before(First_day_year,Time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:127:9` | `member` | `s3306_a_2_A/4` | `member((Amount,_),Amount_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:132:9` | `member` | `s3306_a_2_A/4` | `member((_,Service_),Amount_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:136:7` | `>=` | `s3306_a_2_A/4` | `Wages>=20000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:153:9` | `member` | `s3306_a_2_is_day_of_employment/4` | `member((Employee,_),Employee_x_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:158:9` | `member` | `s3306_a_2_is_day_of_employment/4` | `member((_,Labor),Employee_x_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:161:5` | `list_to_set` | `s3306_a_2_is_day_of_employment/4` | `list_to_set(Employees,Individuals)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:163:15` | `>=` | `s3306_a_2_is_day_of_employment/4` | `Num_employees>=5` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:174:13` | `is_before` | `s3306_a_2_B/6` | `is_before(First_day_year1,Day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:175:13` | `is_before` | `s3306_a_2_B/6` | `is_before(Day,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:182:9` | `member` | `s3306_a_2_B/6` | `member((Stamp,_,_,_),Stamp_day_employees_labor)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:185:2` | `list_to_set` | `s3306_a_2_B/6` | `list_to_set(Stamp_list,Days_stamp)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:187:10` | `>=` | `s3306_a_2_B/6` | `Num_days>=10` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:191:4` | `member` | `s3306_a_2_B/6` | `member(Stamp,Stamp_list)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:196:5` | `list_to_set` | `s3306_a_2_B/6` | `list_to_set(Weeks,S33)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:198:11` | `>=` | `s3306_a_2_B/6` | `Num_weeks>=10` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:201:9` | `member` | `s3306_a_2_B/6` | `member((_,_,Employees,_),Stamp_day_employees_labor)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:206:9` | `member` | `s3306_a_2_B/6` | `member((_,_,_,Labor),Stamp_day_employees_labor)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:211:9` | `member` | `s3306_a_2_B/6` | `member((_,Day,_,_),Stamp_day_employees_labor)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:214:5` | `list_to_set` | `s3306_a_2_B/6` | `list_to_set(Days_list,Workday)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:223:5` | `is_before` | `s3306_a_3_is_wages/5` | `is_before(Time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:225:5` | `is_before` | `s3306_a_3_is_wages/5` | `is_before(First_day_year,Time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:250:9` | `member` | `s3306_a_3/4` | `member((Amount,_),Amount_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:255:9` | `member` | `s3306_a_3/4` | `member((_,Service_),Amount_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:259:7` | `>=` | `s3306_a_3/4` | `Wages>=1000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:306:22` | `min` | `s3306_b_1/2` | `min(7000,Remuneration)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:316:11` | `==` | `s3306_b_2/6` | `Employee==Payee` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:345:8` | `\==` | `s3306_b_7/6` | `Medium\=="cash"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:350:6` | `\==` | `s3306_b_7/6` | `S92 \== Type_service` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:361:11` | `==` | `s3306_b_10/6` | `Employee==Payee` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:364:25` | `==` | `s3306_b_10/6` | `Any_of_his_dependents==Payee` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:377:5` | `is_before` | `s3306_b_10_A/6` | `is_before(Start_termination,Start_remuneration)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:401:11` | `\==` | `s3306_b_11/3` | `Medium\=="cash"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:418:19` | `@>` | `s3306_b_15/5` | `Year_remuneration@>Caly` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:459:35` | `=` | `s3306_c_A/3` | `Geographical_location = "usa"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:465:20` | `==` | `s3306_c_A/3` | `Country=="usa"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:469:34` | `==` | `s3306_c_A/3` | `Geographical_location=="usa"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:480:20` | `\==` | `s3306_c_B/4` | `Country\=="usa"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:484:21` | `\==` | `s3306_c_B/4` | `Location\=="usa"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:540:13` | `is_before` | `s3306_c_1_A_i/5` | `is_before(First_day_year,Payment_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:541:13` | `is_before` | `s3306_c_1_A_i/5` | `is_before(Payment_time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:553:9` | `member` | `s3306_c_1_A_i/5` | `member((Amount,_,_),Amounts_employee_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:557:18` | `>=` | `s3306_c_1_A_i/5` | `Remuneration >= 20000` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:560:9` | `member` | `s3306_c_1_A_i/5` | `member((_,Individual,_),Amounts_employee_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:565:9` | `member` | `s3306_c_1_A_i/5` | `member((_,_,Service_),Amounts_employee_service)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:583:11` | `\==` | `s3306_c_1_B/2` | `Country \== "usa"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:599:11` | `==` | `s3306_c_2/3` | `Location=="private home"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:600:11` | `==` | `s3306_c_2/3` | `Location=="local college club"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:601:11` | `==` | `s3306_c_2/3` | `Location=="local chapter of a college fraternity"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:602:11` | `==` | `s3306_c_2/3` | `Location=="local chapter of a college sorority"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:624:21` | `\==` | `s3306_c_5_A/4` | `Employer\==Employee` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:626:13` | `is_before` | `s3306_c_5_A/4` | `is_before(Time_start,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:633:21` | `is_before` | `s3306_c_5_A/4` | `is_before(Workday,Time_end)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:654:17` | `>` | `s3306_c_5_B/4` | `Stamp_21>Stamp_day` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:660:10` | `==` | `s3306_c_6/1` | `Employer=="united states government"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:665:2` | `atom_prefix` | `s3306_c_7/2` | `atom_prefix(Employer,"state of ")` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:680:11` | `==` | `s3306_c_10_A/4` | `Employee==Student` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:694:2` | `is_before` | `s3306_c_10_A_i/3` | `is_before(Start_enrollment,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:695:2` | `is_before` | `s3306_c_10_A_i/3` | `is_before(Start_attendance,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:702:4` | `is_before` | `s3306_c_10_A_i/3` | `is_before(Workday,Stop_enrollment)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:711:4` | `is_before` | `s3306_c_10_A_i/3` | `is_before(Workday,Stop_attendance)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:726:4` | `is_before` | `s3306_c_10_A_ii/3` | `is_before(Start_marriage,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:735:4` | `is_before` | `s3306_c_10_A_ii/3` | `is_before(Workday,End_marriage)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:751:2` | `is_before` | `s3306_c_10_B/4` | `is_before(Start_patient,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:758:4` | `is_before` | `s3306_c_10_B/4` | `is_before(Workday,End_patient)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:766:2` | `sub_atom` | `s3306_c_11/2` | `sub_atom(Employer,_,11,0,Suffix)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:767:8` | `==` | `s3306_c_11/2` | `Suffix==' government'` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:768:10` | `\==` | `s3306_c_11/2` | `Employer\=="united states government"` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:789:2` | `is_before` | `s3306_c_13/4` | `is_before(Start_enrollment,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:790:2` | `is_before` | `s3306_c_13/4` | `is_before(Start_attendance,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:797:4` | `is_before` | `s3306_c_13/4` | `is_before(Workday,Stop_enrollment)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:806:4` | `is_before` | `s3306_c_13/4` | `is_before(Workday,Stop_attendance)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:826:2` | `is_before` | `s3306_c_21/4` | `is_before(Start_incarceration,Workday)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:833:4` | `is_before` | `s3306_c_21/4` | `is_before(Workday,End_incarceration)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:10:12` | `max` | `s63/3` | `max(Taxable_income_tmp,0)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:22:12` | `max` | `s63_a/5` | `max(Taxable_income_tmp,0)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:33:12` | `max` | `s63_b/4` | `max(Taxable_income_tmp,0)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:69:22` | `min` | `s63_c_1_A/3` | `min(Basic_amount,Max_amount)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:164:14` | `max` | `s63_c_5/5` | `max(Amount1,Amount2)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:195:4` | `is_before` | `s63_c_6_A/4` | `is_before(First_day_year,Start)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:196:4` | `is_before` | `s63_c_6_A/4` | `is_before(Start,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:210:13` | `is_before` | `s63_c_6_B/2` | `is_before(Start_nra,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:219:13` | `is_before` | `s63_c_6_B/2` | `is_before(First_day_year,End_nra)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:235:13` | `is_before` | `s63_c_6_D/2` | `is_before(Start_trust,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:244:13` | `is_before` | `s63_c_6_D/2` | `is_before(First_day_year,End_trust)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:258:9` | `>` | `s63_c_7_i/2` | `Taxy>2017` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:259:9` | `<` | `s63_c_7_i/2` | `Taxy<2026` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:264:9` | `>` | `s63_c_7_ii/2` | `Taxy>2017` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:265:9` | `<` | `s63_c_7_ii/2` | `Taxy<2026` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:281:4` | `is_before` | `s63_d/4` | `is_before(First,Start)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:282:4` | `is_before` | `s63_d/4` | `is_before(Start,Last)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:288:3` | `member` | `s63_d/4` | `member((Amount,_),Amount_deduction)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:292:3` | `>` | `s63_d/4` | `L>0` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:296:3` | `member` | `s63_d/4` | `member((_,Deduction),Amount_deduction)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:337:21` | `>=` | `s63_f_1_A/2` | `Time_since_birth>=Sixtyfive_years` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:350:21` | `>=` | `s63_f_1_B/3` | `Time_since_birth>=Sixtyfive_years` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:367:5` | `is_before` | `s63_f_2_A/2` | `is_before(Start_time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:376:5` | `is_before` | `s63_f_2_B/3` | `is_before(Start_time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:25:8` | `>` | `s68_a/6` | `Agi>Aa` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:28:11` | `min` | `s68_a/6` | `min(Reduction1,Reduction2)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:111:5` | `between` | `s68_f/1` | `between(2018,2025,Taxy)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:7:10` | `\==` | `s7703/4` | `Taxp \== Spouse` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:27:6` | `\==` | `s7703_a_1/5` | `Taxp\==Spouse` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:31:28` | `=` | `s7703_a_1/5` | `Start_marriage = First_day_year` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:37:5` | `is_before` | `s7703_a_1/5` | `is_before(Start_marriage,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:43:4` | `is_before` | `s7703_a_1/5` | `is_before(First_day_year,S13)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:44:4` | `is_before` | `s7703_a_1/5` | `is_before(S13,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:47:4` | `is_before` | `s7703_a_1/5` | `is_before(Start_marriage,S13)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:54:6` | `is_before` | `s7703_a_1/5` | `is_before(S13,End_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:70:7` | `is_before` | `s7703_a_1/5` | `is_before(First_day_next_year,End_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:78:6` | `is_before` | `s7703_a_1/5` | `is_before(First_day_next_year,End_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:89:9` | `\==` | `s7703_a_2/5` | `Taxp\==Spouse` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:98:2` | `is_before` | `s7703_a_2/5` | `is_before(Divorce_time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:126:5` | `latest` | `s7703_b_1/4` | `latest([Start_time,First_day_year],Start)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:133:5` | `earliest` | `s7703_b_1/4` | `earliest([End_time,Last_day_year],End)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:138:11` | `>=` | `s7703_b_1/4` | `Duration >= Half_year_duration` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:158:8` | `==` | `s7703_b_2/4` | `Taxy==Taxy_payment_int` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:176:8` | `==` | `s7703_b_2/4` | `Taxy==Taxy_payment_int` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:182:6` | `>` | `s7703_b_2/4` | `Cost>0` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:184:7` | `>=` | `s7703_b_2/4` | `Ratio>=rational(0.5)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:192:5` | `is_before` | `s7703_b_3_is_member_of_household/3` | `is_before(Time_start,Day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:199:4` | `is_before` | `s7703_b_3_is_member_of_household/3` | `is_before(Day,Time_end)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:208:13` | `between` | `s7703_b_3/4` | `between(2,185,Day_offset)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:216:13` | `==` | `s7703_b_3/4` | `Num_days==0` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:14:11` | `=<` | `is_before/2` | `Stamp1=<Stamp2` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:30:9` | `latest` | `latest/2` | `latest(Days,Day,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:34:9` | `latest` | `latest/2` | `latest(Days,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:44:17` | `is_before` | `latest/3` | `is_before(Day,Latest)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:45:17` | `latest` | `latest/3` | `latest(Days,Latest,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:48:20` | `is_before` | `latest/3` | `is_before(Day,Latest)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:49:17` | `latest` | `latest/3` | `latest(Days,Day,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:55:9` | `latest` | `latest/3` | `latest(Days,Latest,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:64:9` | `earliest` | `earliest/2` | `earliest(Days,Day,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:68:9` | `earliest` | `earliest/2` | `earliest(Days,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:78:17` | `is_before` | `earliest/3` | `is_before(Earliest,Day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:79:17` | `earliest` | `earliest/3` | `earliest(Days,Earliest,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:82:20` | `is_before` | `earliest/3` | `is_before(Earliest,Day)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:83:17` | `earliest` | `earliest/3` | `earliest(Days,Day,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:89:9` | `earliest` | `earliest/3` | `earliest(Days,Earliest,Output)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:117:7` | `\==` | `is_child_of/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:144:7` | `\==` | `is_sibling_of/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:173:7` | `\==` | `is_stepsibling_of/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:180:5` | `latest` | `is_stepsibling_of/4` | `latest([Day_start_x,Day_start_y,Start_time], Day_start)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:187:5` | `earliest` | `is_stepsibling_of/4` | `earliest([Day_end_x,Day_end_y,End_time],Day_end)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:198:7` | `\==` | `is_sibling_in_law_of_aux/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:205:5` | `latest` | `is_sibling_in_law_of_aux/4` | `latest([Start_time,Day_start_y],Day_start)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:212:5` | `earliest` | `is_sibling_in_law_of_aux/4` | `earliest([End_time,Day_end_y],Day_end)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:219:7` | `\==` | `is_child_in_law_of/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:226:5` | `latest` | `is_child_in_law_of/4` | `latest([Start_time,Day_start_y],Day_start)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:233:5` | `earliest` | `is_child_in_law_of/4` | `earliest([End_time,Day_end_y],Day_end)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:240:7` | `\==` | `is_parent_in_law_of/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:247:5` | `latest` | `is_parent_in_law_of/4` | `latest([Start_time,Day_start_y],Day_start)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:254:5` | `earliest` | `is_parent_in_law_of/4` | `earliest([End_time,Day_end_y],Day_end)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:262:5` | `latest` | `is_stepparent_of/4` | `latest([Start_time,Day_start_y],Day_start)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:263:7` | `\==` | `is_stepparent_of/4` | `X \== Y` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:270:5` | `earliest` | `is_stepparent_of/4` | `earliest([End_time,Day_end_y],Day_end)` | Confirm | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:311:13` | `is_before` | `gross_income_individual/3` | `is_before(First_day_year,Start_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:312:13` | `is_before` | `gross_income_individual/3` | `is_before(Start_time,Last_day_year)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:323:13` | `is_before` | `gross_income_individual/3` | `is_before(First_day_year,Start_time)` | Source witness | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:324:13` | `is_before` | `gross_income_individual/3` | `is_before(Start_time,Last_day_year)` | Source witness | TODO |

Date-support inventory (119 additional or overlapping observations; these are not additional date-comparison claims):

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section1.pl:23:5` | `first_day_year` | `s1_a_1/6` | `first_day_year(Taxy,First_day)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:24:5` | `last_day_year` | `s1_a_1/6` | `last_day_year(Taxy,Last_day)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:178:9` | `first_day_year` | `s1_d/5` | `first_day_year(Taxy,First_day)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:179:9` | `last_day_year` | `s1_d/5` | `last_day_year(Taxy,Last_day)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:3:2` | `first_day_year` | `s151/5` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:4:5` | `last_day_year` | `s151/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:76:8` | `first_day_year` | `s151_b_applies/3` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:78:8` | `last_day_year` | `s151_b_applies/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:173:16` | `first_day_year` | `s151_d_3_B/5` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:175:16` | `last_day_year` | `s151_d_3_B/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:49:5` | `first_day_year` | `s152_b_2/4` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:51:5` | `last_day_year` | `s152_b_2/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:97:3` | `first_day_year` | `s152_c_1_B/6` | `first_day_year(Taxy,Start_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:105:3` | `last_day_year` | `s152_c_1_B/6` | `last_day_year(Taxy,End_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:116:3` | `first_day_year` | `s152_c_1_B/6` | `first_day_year(Taxy,Start_taxpayer)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:124:3` | `last_day_year` | `s152_c_1_B/6` | `last_day_year(Taxy,End_taxpayer)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:129:5` | `last_day_year` | `s152_c_1_B/6` | `last_day_year(Taxy,Last_day_of_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:131:5` | `first_day_year` | `s152_c_1_B/6` | `first_day_year(Taxy,First_day_of_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:133:5` | `duration` | `s152_c_1_B/6` | `duration(First_day_of_year,Last_day_of_year,Taxy_duration)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:135:5` | `duration` | `s152_c_1_B/6` | `duration(Start_day,End_day,Duration)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:149:9` | `first_day_year` | `s152_c_1_E/3` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:151:9` | `last_day_year` | `s152_c_1_E/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:225:2` | `last_day_year` | `s152_c_3/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:226:2` | `duration` | `s152_c_3/3` | `duration(Individual_dob,Last_day_year,Age_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:228:2` | `last_day_year` | `s152_c_3/3` | `last_day_year(Taxy_25,Last_day_year_25)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:229:2` | `duration` | `s152_c_3/3` | `duration(Last_day_year,Last_day_year_25,Duration_25_years)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:345:5` | `first_day_year` | `s152_d_2_H/6` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:346:5` | `last_day_year` | `s152_d_2_H/6` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:38:5` | `first_day_year` | `s2_a_1_A/5` | `first_day_year(Taxy2,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:41:5` | `last_day_year` | `s2_a_1_A/5` | `last_day_year(Taxy1,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:49:5` | `first_day_year` | `s2_a_1_B/4` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:50:5` | `last_day_year` | `s2_a_1_B/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:112:5` | `last_day_year` | `s2_a_2_A/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:129:17` | `last_day_year` | `s2_a_2_B/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:139:17` | `first_day_year` | `s2_a_2_B/3` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:161:9` | `last_day_year` | `s2_b_1/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:184:25` | `first_day_year` | `s2_b_1/4` | `first_day_year(Taxy1,First_day_year1)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:205:5` | `first_day_year` | `s2_b_1_A/4` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:206:5` | `last_day_year` | `s2_b_1_A/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:247:5` | `duration` | `s2_b_1_A/4` | `duration(Start_individual_residence,End_individual_residence,Duration_individual_residence)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:248:5` | `duration` | `s2_b_1_A/4` | `duration(First_day_year,Last_day_year,Taxy_duration)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:282:5` | `first_day_year` | `s2_b_1_B/5` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:283:5` | `last_day_year` | `s2_b_1_B/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:331:5` | `last_day_year` | `s2_b_2_A/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:336:5` | `first_day_year` | `s2_b_2_B/3` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:337:5` | `last_day_year` | `s2_b_2_B/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:364:5` | `first_day_year` | `s2_b_2_C/4` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:365:5` | `last_day_year` | `s2_b_2_C/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:397:5` | `first_day_year` | `s2_b_3_A/3` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:398:5` | `last_day_year` | `s2_b_3_A/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:425:5` | `first_day_year` | `s2_b_3_B/3` | `first_day_year(Taxy,First_day)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:426:5` | `last_day_year` | `s2_b_3_B/3` | `last_day_year(Taxy,Last_day)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:5:5` | `first_day_year` | `s3301/6` | `first_day_year(Caly,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:6:5` | `last_day_year` | `s3301/6` | `last_day_year(Caly,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:20:5` | `last_day_year` | `s3306_a_1_is_wages/4` | `last_day_year(Year,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:22:5` | `first_day_year` | `s3306_a_1_is_wages/4` | `first_day_year(Year,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:51:5` | `last_day_year` | `s3306_a_1_B/4` | `last_day_year(Caly,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:53:5` | `first_day_year` | `s3306_a_1_B/4` | `first_day_year(Year1,First_day_year1)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:60:13` | `day_to_stamp` | `s3306_a_1_B/4` | `day_to_stamp(Day,Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:76:4` | `format_time` | `s3306_a_1_B/4` | `format_time(atom(Week), "%W", Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:107:5` | `last_day_year` | `s3306_a_2_is_wages/5` | `last_day_year(Year,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:109:5` | `first_day_year` | `s3306_a_2_is_wages/5` | `first_day_year(Year,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:166:5` | `last_day_year` | `s3306_a_2_B/6` | `last_day_year(Caly,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:168:5` | `first_day_year` | `s3306_a_2_B/6` | `first_day_year(Year1,First_day_year1)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:176:13` | `day_to_stamp` | `s3306_a_2_B/6` | `day_to_stamp(Day,Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:192:4` | `format_time` | `s3306_a_2_B/6` | `format_time(atom(Week), "%W", Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:222:5` | `last_day_year` | `s3306_a_3_is_wages/5` | `last_day_year(Year,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:224:5` | `first_day_year` | `s3306_a_3_is_wages/5` | `first_day_year(Year,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:521:5` | `last_day_year` | `s3306_c_1_A_i/5` | `last_day_year(Caly,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:523:5` | `first_day_year` | `s3306_c_1_A_i/5` | `first_day_year(Year1,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:651:9` | `date_time_stamp` | `s3306_c_5_B/4` | `date_time_stamp(date(Dob_y,Dob_m,Day_offset,0,0,0,0,-,-), Stamp_21)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:651:25` | `date` | `s3306_c_5_B/4` | `date(Dob_y,Dob_m,Day_offset,0,0,0,0,-,-)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:653:9` | `date_time_stamp` | `s3306_c_5_B/4` | `date_time_stamp(date(Year,Month,Day1,0,0,0,0,-,-), Stamp_day)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:653:25` | `date` | `s3306_c_5_B/4` | `date(Year,Month,Day1,0,0,0,0,-,-)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:115:5` | `first_day_year` | `s63_c_2_A_i/3` | `first_day_year(Taxy,First_day)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:117:5` | `last_day_year` | `s63_c_2_A_i/3` | `last_day_year(Taxy,Last_day)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:180:4` | `first_day_year` | `s63_c_6_A/4` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:181:4` | `last_day_year` | `s63_c_6_A/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:202:5` | `first_day_year` | `s63_c_6_B/2` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:203:5` | `last_day_year` | `s63_c_6_B/2` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:227:5` | `first_day_year` | `s63_c_6_D/2` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:228:5` | `last_day_year` | `s63_c_6_D/2` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:272:2` | `first_day_year` | `s63_d/4` | `first_day_year(Taxy,First)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:273:2` | `last_day_year` | `s63_d/4` | `last_day_year(Taxy,Last)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:332:5` | `last_day_year` | `s63_f_1_A/2` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:333:5` | `duration` | `s63_f_1_A/2` | `duration(Day_of_birth,Last_day_year,Time_since_birth)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:335:5` | `last_day_year` | `s63_f_1_A/2` | `last_day_year(Taxy65,Last_day_year65)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:336:5` | `duration` | `s63_f_1_A/2` | `duration(Last_day_year,Last_day_year65,Sixtyfive_years)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:345:5` | `last_day_year` | `s63_f_1_B/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:346:5` | `duration` | `s63_f_1_B/3` | `duration(Day_of_birth,Last_day_year,Time_since_birth)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:348:5` | `last_day_year` | `s63_f_1_B/3` | `last_day_year(Taxy65,Last_day_year65)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:349:5` | `duration` | `s63_f_1_B/3` | `duration(Last_day_year,Last_day_year65,Sixtyfive_years)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:366:5` | `last_day_year` | `s63_f_2_A/2` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:375:5` | `last_day_year` | `s63_f_2_B/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:70:13` | `first_day_year` | `s68_b_1_A/5` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:72:13` | `last_day_year` | `s68_b_1_A/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:98:9` | `first_day_year` | `s68_b_1_D/3` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:100:9` | `last_day_year` | `s68_b_1_D/3` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:19:2` | `last_day_year` | `s7703_a_1/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:20:2` | `first_day_year` | `s7703_a_1/5` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:22:2` | `first_day_year` | `s7703_a_1/5` | `first_day_year(Taxy1,First_day_next_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:97:2` | `last_day_year` | `s7703_a_2/5` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:111:2` | `first_day_year` | `s7703_b_1/4` | `first_day_year(Taxy,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:112:2` | `last_day_year` | `s7703_b_1/4` | `last_day_year(Taxy,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:135:5` | `duration` | `s7703_b_1/4` | `duration(Start,End,Duration)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:136:5` | `duration` | `s7703_b_1/4` | `duration(First_day_year,Last_day_year,Taxy_duration)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:209:13` | `date_time_stamp` | `s7703_b_3/4` | `date_time_stamp(date(Taxy,7,Day_offset,0,0,0,0,-,-), Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:209:29` | `date` | `s7703_b_3/4` | `date(Taxy,7,Day_offset,0,0,0,0,-,-)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:210:13` | `format_time` | `s7703_b_3/4` | `format_time(atom(Day), "%Y-%m-%d", Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:8:2` | `date_time_stamp` | `day_to_stamp/2` | `date_time_stamp(date(YI,MI,DI1,0,0,0,0,-,-), Stamp)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:8:18` | `date` | `day_to_stamp/2` | `date(YI,MI,DI1,0,0,0,0,-,-)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:12:2` | `day_to_stamp` | `is_before/2` | `day_to_stamp(Day1,Stamp1)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:13:2` | `day_to_stamp` | `is_before/2` | `day_to_stamp(Day2,Stamp2)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:93:2` | `day_to_stamp` | `duration/3` | `day_to_stamp(Day1, Stamp1)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:94:2` | `day_to_stamp` | `duration/3` | `day_to_stamp(Day2, Stamp2)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:274:2` | `first_day_year` | `gross_income/3` | `first_day_year(Year,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:275:5` | `last_day_year` | `gross_income/3` | `last_day_year(Year,Last_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:302:5` | `first_day_year` | `gross_income_individual/3` | `first_day_year(Year,First_day_year)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:303:5` | `last_day_year` | `gross_income_individual/3` | `last_day_year(Year,Last_day_year)` | TODO |

TODO observations with concrete source evidence:

- `human/sara/sara/statutes/prolog/utils.pl:7:6` — `DI1 is DI+1`; determine the role of the source day increment and timestamp conversion before choosing day-count behavior.
- `human/sara/sara/statutes/prolog/utils.pl:95:11` — `Duration is Stamp2-Stamp1`; determine how these source duration units relate to planned day counts.
- `human/sara/sara/statutes/prolog/section3306.pl:418:19` — `Year_remuneration@>Caly`; the clause obtains year components with `split_string`. Confirm term ordering and representation without substituting numeric comparison.
- `human/sara/sara/statutes/prolog/section3306.pl:650:20` — `Day_offset is Dob_d+7671`; the clause also passes split components to `date_time_stamp`. Confirm operand types, conversion/error behavior, and the fixed offset.
- `human/sara/sara/statutes/prolog/section3306.pl:654:17` — `Stamp_21>Stamp_day`; same-clause timestamp outputs are visible, but the inventory does not prove successful bindings.
- `human/sara/sara/statutes/prolog/section7703.pl:208:13` — `between(2,185,Day_offset)`; confirm the source day-offset enumeration and calendar overflow behavior.

## Household

Decision: TODO. Shared type and field list: TODO, owned by the separate Interface/Household lane. No schema, field type, valid-input restriction, fact multiplicity, or missing-field behavior is chosen here.

Blocking cross-reference — TODO: resolve the [Household lane's unsupported forms and blocking findings](HOUSEHOLD.md#unsupported-forms-and-blocking-findings) before affected semantic ingestion or round-trip work resumes. That lane reports the missing full stops before `% Test` in `s3306_c_2_neg.pl:26` and `s3306_c_2_pos.pl:26`, plus case-local rules and non-ground clauses that block facts-only ingestion. The main lane independently confirmed the clause-boundary finding and recorded the semantic halt as B005. HOUSEHOLD.md records **376 case files but 374 standalone test directives**; those totals describe different source objects, and no case was dropped. This inventory neither re-inspects those cases nor interprets, repairs, filters, or duplicates their parser/inventory; the required owner decisions and evidence remain in HOUSEHOLD.md.

Inventory support: `HAZARDS.json.functor_index` contains each unquoted functor-shaped occurrence, its name/arity, its definition locations when available, whether it occurs in a head/body/directive, and an exact excerpt. `events.pl` contributes all 61 declaration clauses; `init.pl` contributes all 11 load directives even though both have zero core hazard sites. The fact/interface inventory must include helper dependencies and consult the separate Household draft. Case facts and their population have not been re-read by this inventory.

## NAF

Decision: TODO. Intended translation at each of the 150 sites: TODO. Groundness, goal order, unbound/anonymous variables, missing facts, and explicit negative versus absent information: TODO.

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section1.pl:27:5` | `\+` | `s1_a_1/6` | `\+ ( % nonresident aliens can't file jointly nonresident_alien_(someone_is_nra), ( agent_(someone_is_nra,Taxp); agent_(someone_is_nra,Spouse) ), ( ( \+ start_(someo…` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:35:17` | `\+` | `s1_a_1/6` | `\+ start_(someone_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:42:17` | `\+` | `s1_a_1/6` | `\+ end_(someone_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:133:5` | `\+` | `s1_c/4` | `\+ s2_a(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:134:5` | `\+` | `s1_c/4` | `\+ s2_b(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:135:5` | `\+` | `s1_c/4` | `\+ s7703(Taxp,_,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section1.pl:174:5` | `\+` | `s1_d/5` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), first_day_year(Taxy,First_day), last_day_year(Taxy,Last_day), start_(Joint…` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:20:13` | `\+` | `s151/5` | `\+ ( s7703(Taxp,Spouse,_,Taxy), joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), start_(Joint_return,First_day_year), end_(Joint…` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:72:5` | `\+` | `s151_b_applies/3` | `\+ ( % if a joint return is not made by the taxpayer and his spouse joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), first_day_y…` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:81:5` | `\+` | `s151_b_applies/3` | `\+ s152(Spouse,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:112:13` | `\+` | `s151_d/3` | `\+ s151_d_2(Taxp,_,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:113:13` | `\+` | `s151_d/3` | `\+ s151_d_5(_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:118:21` | `\+` | `s151_d/3` | `\+ s151_d_3(Taxp,Exemption_in,Ea,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:169:13` | `\+` | `s151_d_3_B/5` | `\+ ( % if a joint return is not made by the taxpayer and his spouse joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), first_day_y…` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:3:2` | `\+` | `s152/3` | `\+ ( var(Dependent), var(Taxp) )` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:5:2` | `\+` | `s152/3` | `\+ s152_b_1(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:7:2` | `\+` | `s152/3` | `\+ s152_b_2(Dependent,_,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:95:3` | `\+` | `s152_c_1_B/6` | `\+ start_(Residence_individual,_)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:103:3` | `\+` | `s152_c_1_B/6` | `\+ end_(Residence_individual,_)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:114:3` | `\+` | `s152_c_1_B/6` | `\+ start_(Residence_taxpayer,_)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:122:3` | `\+` | `s152_c_1_B/6` | `\+ end_(Residence_taxpayer,_)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:144:5` | `\+` | `s152_c_1_E/3` | `\+ ( s7703(Dependent,Spouse,_,Taxy), joint_return_(Joint_return), agent_(Joint_return,Dependent), agent_(Joint_return,Spouse), first_day_year(Taxy,First_day_year), …` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:207:13` | `\+` | `s152_c_3/3` | `\+ ( birth_(Someone_is_born), ( agent_(Someone_is_born,Dependent); agent_(Someone_is_born,Dependent) ) )` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:273:5` | `\+` | `s152_d_1_D/2` | `\+ s152_c(Dependent,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:347:5` | `\+` | `s152_d_2_H/6` | `\+ ( marriage_(Marriage), agent_(Marriage,Dependent), agent_(Marriage,Taxp), start_(Marriage,Start), is_before(Start,Last_day_year), ( end_(Marriage,End) -> is_befo…` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:358:4` | `\+` | `s152_d_2_H/6` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:371:3` | `\+` | `s152_d_2_H/6` | `\+ end_(Taxpayer_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:383:3` | `\+` | `s152_d_2_H/6` | `\+ end_(Individual_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:6:5` | `\+` | `s2_a/3` | `\+ s2_a_2(Taxp,Spouse,Previous_marriage,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:30:13` | `\+` | `s2_a_1_A/5` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:58:13` | `\+` | `s2_a_1_B/4` | `\+ end_(Taxpayer_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:73:13` | `\+` | `s2_a_1_B/4` | `\+ end_(Dependent_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:100:5` | `\+` | `s2_a_2/4` | `\+ s2_a_2_B(Taxp,Spouse,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:117:5` | `\+` | `s2_a_2_B/3` | `\+ ( % no joint return shall be made if either the husband or wife at any time during the taxable year is a nonresident alien nonresident_alien_(Someone_is_nra), ( …` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:125:17` | `\+` | `s2_a_2_B/3` | `\+ start_(Someone_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:135:17` | `\+` | `s2_a_2_B/3` | `\+ end_(Someone_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:149:5` | `\+` | `s2_b/3` | `\+ s2_b_3(Taxp,Dependent,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:155:5` | `\+` | `s2_b_1/4` | `\+ ( % "such individual is not married" marriage_(Marriage), agent_(Marriage,Taxp), agent_(Marriage,Spouse), Spouse \== Taxp, start_(Marriage,Start_marriage), last_…` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:176:17` | `\+` | `s2_b_1/4` | `\+ ( death_(Spouse_dies), agent_(Spouse_dies,Spouse) )` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:188:25` | `\+` | `s2_b_1/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:193:9` | `\+` | `s2_b_1/4` | `\+ s2_b_2_A(_,_,_,Marriage,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:194:9` | `\+` | `s2_b_1/4` | `\+ s2_b_2_B(Taxp,Spouse,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:196:5` | `\+` | `s2_b_1/4` | `\+ s2_a(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:215:9` | `\+` | `s2_b_1_A/4` | `\+ start_(Taxpayer_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:222:9` | `\+` | `s2_b_1_A/4` | `\+ end_(Taxpayer_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:231:13` | `\+` | `s2_b_1_A/4` | `\+ start_(Individual_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:240:13` | `\+` | `s2_b_1_A/4` | `\+ end_(Individual_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:259:5` | `\+` | `s2_b_1_A_i/3` | `\+ ( s2_b_1_A_i_I(Dependent,Taxy), s2_b_1_A_i_II(Dependent,Taxp,Taxy) )` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:293:13` | `\+` | `s2_b_1_B/5` | `\+ end_(Parent_residence,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:345:13` | `\+` | `s2_b_2_B/3` | `\+ start_(Spouse_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:354:13` | `\+` | `s2_b_2_B/3` | `\+ end_(Spouse_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:369:5` | `\+` | `s2_b_2_C/4` | `\+ s2_b_2_B(Taxp,Spouse,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:375:13` | `\+` | `s2_b_2_C/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:403:13` | `\+` | `s2_b_3_A/3` | `\+ start_(Taxpayer_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:414:13` | `\+` | `s2_b_3_A/3` | `\+ end_(Taxpayer_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:427:5` | `\+` | `s2_b_3_B/3` | `\+ s152_b(Dependent,Taxp,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:428:5` | `\+` | `s2_b_3_B/3` | `\+ s152_a_1(Dependent,Taxp,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:431:5` | `\+` | `s2_b_3_B/3` | `\+ ( ( s152_d_2_A(Dependent,Taxp,Start_relationship,End_relationship); s152_d_2_B(Dependent,Taxp,Start_relationship,End_relationship); s152_d_2_C(Dependent,Taxp,Sta…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:24:5` | `\+` | `s3306_a_1_is_wages/4` | `\+ purpose_(Service, "agricultural labor")` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:25:2` | `\+` | `s3306_a_1_is_wages/4` | `\+ purpose_(Service, "domestic service")` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:45:5` | `\+` | `s3306_a_1_is_day_of_employment/3` | `\+ purpose_(Service,"agricultural labor")` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:46:5` | `\+` | `s3306_a_1_is_day_of_employment/3` | `\+ purpose_(Service,"domestic service")` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:47:5` | `\+` | `s3306_a_1_is_day_of_employment/3` | `\+ type_(Service,"agricultural labor")` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:48:5` | `\+` | `s3306_a_1_is_day_of_employment/3` | `\+ type_(Service,"domestic service")` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:228:4` | `\+` | `s3306_a_3_is_wages/5` | `\+ means_(Remuneration,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:273:10` | `\+` | `s3306_b/8` | `\+ means_(Remuneration,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:280:13` | `\+` | `s3306_b/8` | `\+ plan_(Payee)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:298:2` | `\+` | `s3306_b/8` | `\+ s3306_b_2(Remuneration,Employment,Payer,Payee,_,Plan)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:299:5` | `\+` | `s3306_b/8` | `\+ s3306_b_7(Remuneration,Employment,Payer,Payee,_,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:300:2` | `\+` | `s3306_b/8` | `\+ s3306_b_10(Remuneration,Employment,Payer,Payee,_,Plan)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:301:2` | `\+` | `s3306_b/8` | `\+ s3306_b_11(Remuneration,Employment,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:302:5` | `\+` | `s3306_b/8` | `\+ s3306_b_15(Remuneration,Employer,Payee,Employee,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:415:3` | `\+` | `s3306_b_15/5` | `\+ end_(Emar,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:440:2` | `\+` | `s3306_c/5` | `\+ s3306_c_1(Service,Caly)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:441:2` | `\+` | `s3306_c/5` | `\+ s3306_c_2(Service,_,Caly)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:442:2` | `\+` | `s3306_c/5` | `\+ s3306_c_5(Service,Employer,Employee,Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:443:2` | `\+` | `s3306_c/5` | `\+ s3306_c_6(Service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:444:2` | `\+` | `s3306_c/5` | `\+ s3306_c_7(Service,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:445:2` | `\+` | `s3306_c/5` | `\+ s3306_c_10(Service,Employer,Employee,Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:446:2` | `\+` | `s3306_c/5` | `\+ s3306_c_11(Service,Employer)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:447:2` | `\+` | `s3306_c/5` | `\+ s3306_c_13(Service,Employer,Employee,Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:448:2` | `\+` | `s3306_c/5` | `\+ s3306_c_16(Service,Employer)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:449:2` | `\+` | `s3306_c/5` | `\+ s3306_c_21(Service,Employee,_,Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:458:13` | `\+` | `s3306_c_A/3` | `\+ location_(Service,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:468:13` | `\+` | `s3306_c_A/3` | `\+ country_(Geographical_location,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:483:13` | `\+` | `s3306_c_B/4` | `\+ country_(Location,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:487:2` | `\+` | `s3306_c_B/4` | `\+ ( unemployment_compensation_agreement_(Agreement), agent_(Agreement,"usa"), agent_(Agreement,Location) )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:504:2` | `\+` | `s3306_c_1/2` | `\+ ( s3306_c_1_A(Service,_,Caly), s3306_c_1_B(Service,_) )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:544:21` | `\+` | `s3306_c_1_A_i/5` | `\+ means_(Payment,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:575:2` | `\+` | `s3306_c_1_B/2` | `\+ ( ( type_(Service,"agricultural labor"); purpose_(Service,"agricultural labor") ), citizenship_(Employee_citizenship), agent_(Employee_citizenship,Employee), pat…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:604:2` | `\+` | `s3306_c_2/3` | `\+ s3306_a_3(Person,_,_,Caly)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:629:21` | `\+` | `s3306_c_5_A/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:698:4` | `\+` | `s3306_c_10_A_i/3` | `\+ end_(Student_is_enrolled,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:707:4` | `\+` | `s3306_c_10_A_i/3` | `\+ end_(Student_attends_classes,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:722:4` | `\+` | `s3306_c_10_A_ii/3` | `\+ start_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:731:4` | `\+` | `s3306_c_10_A_ii/3` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:754:4` | `\+` | `s3306_c_10_B/4` | `\+ end_(Employee_is_medical_patient,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:793:4` | `\+` | `s3306_c_13/4` | `\+ end_(Student_is_enrolled,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:802:4` | `\+` | `s3306_c_13/4` | `\+ end_(Student_attends_classes,_)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:829:4` | `\+` | `s3306_c_21/4` | `\+ end_(Person_goes_to_jail,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:6:4` | `\+` | `s63/3` | `\+ s63_b(Taxp,Taxy,_,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:28:5` | `\+` | `s63_b/4` | `\+ s63_d(Taxp,_,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:56:12` | `\+` | `s63_c_1/3` | `\+ s63_c_6(Taxp,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:72:13` | `\+` | `s63_c_1_A/3` | `\+ s63_c_5(Taxp,_,_,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:87:9` | `\+` | `s63_c_2/3` | `\+ s63_c_2_B(Taxp,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:92:9` | `\+` | `s63_c_2/3` | `\+ s63_c_2_A(Taxp,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:96:9` | `\+` | `s63_c_2/3` | `\+ s63_c_2_A(Taxp,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:97:9` | `\+` | `s63_c_2/3` | `\+ s63_c_2_B(Taxp,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:130:13` | `\+` | `s63_c_2_B/3` | `\+ s63_c_7_i(Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:139:9` | `\+` | `s63_c_2_C/2` | `\+ s63_c_7_ii(Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:182:4` | `\+` | `s63_c_6_A/4` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), start_(Joint_return,First_day_year), end_(Joint_return,Last_day_year) )` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:206:13` | `\+` | `s63_c_6_B/2` | `\+ start_(Taxp_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:215:13` | `\+` | `s63_c_6_B/2` | `\+ end_(Taxp_is_nra,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:231:13` | `\+` | `s63_c_6_D/2` | `\+ start_(Taxp_is_trust,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:240:13` | `\+` | `s63_c_6_D/2` | `\+ end_(Taxp_is_trust,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:313:13` | `\+` | `s63_f/3` | `\+ s63_f_3(Taxp,Taxy,_)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:385:5` | `\+` | `s63_f_3/3` | `\+ s7703(Taxp,_,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:386:5` | `\+` | `s63_f_3/3` | `\+ s2_a(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:8:9` | `\+` | `s68/4` | `\+ s68_f(Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:14:13` | `\+` | `s68/4` | `\+ s68_a(Taxp,_,_,Amount_deductions_in,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:86:5` | `\+` | `s68_b_1_C/3` | `\+ s7703(Taxp,_,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:87:5` | `\+` | `s68_b_1_C/3` | `\+ s2_a(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:88:5` | `\+` | `s68_b_1_C/3` | `\+ s2_b(Taxp,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section68.pl:94:5` | `\+` | `s68_b_1_D/3` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), agent_(Joint_return,Spouse), first_day_year(Taxy,First_day_year), start_(Joint_return,First_day_year), …` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:9:2` | `\+` | `s7703/4` | `\+ s7703_b(Taxp,Spouse,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:14:2` | `\+` | `s7703_a/4` | `\+ s7703_a_2(Taxp,Spouse,Marriage,_,Taxy)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:30:13` | `\+` | `s7703_a_1/5` | `\+ start_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:50:6` | `\+` | `s7703_a_1/5` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:61:6` | `\+` | `s7703_a_1/5` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:113:2` | `\+` | `s7703_b_1/4` | `\+ ( joint_return_(Joint_return), agent_(Joint_return,Taxp), start_(Joint_return,First_day_year), end_(Joint_return,Last_day_year) )` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:129:13` | `\+` | `s7703_b_1/4` | `\+ end_(Child_lives_at_home,_)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:195:4` | `\+` | `s7703_b_3_is_member_of_household/3` | `\+ end_(Spouse_lives_in_household,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:48:17` | `\+` | `latest/3` | `\+ is_before(Day,Latest)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:82:17` | `\+` | `earliest/3` | `\+ is_before(Earliest,Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:120:13` | `\+` | `is_child_of/4` | `\+ start_(Relationship,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:126:4` | `\+` | `is_child_of/4` | `\+ end_(Relationship,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:147:13` | `\+` | `is_sibling_of/4` | `\+ start_(Relationship,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:153:4` | `\+` | `is_sibling_of/4` | `\+ end_(Relationship,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:176:13` | `\+` | `is_stepsibling_of/4` | `\+ start_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:183:4` | `\+` | `is_stepsibling_of/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:201:13` | `\+` | `is_sibling_in_law_of_aux/4` | `\+ start_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:208:4` | `\+` | `is_sibling_in_law_of_aux/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:222:13` | `\+` | `is_child_in_law_of/4` | `\+ start_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:229:4` | `\+` | `is_child_in_law_of/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:243:13` | `\+` | `is_parent_in_law_of/4` | `\+ start_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:250:4` | `\+` | `is_parent_in_law_of/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:266:4` | `\+` | `is_stepparent_of/4` | `\+ end_(Marriage,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:289:13` | `\+` | `gross_income/3` | `\+ ( s7703(Person,Spouse,_,Year), joint_return_(Joint_return), agent_(Joint_return,Person), agent_(Joint_return,Spouse), start_(Joint_return,First_day_year), end_(J…` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:337:13` | `\+` | `tax/3` | `\+ s1(Taxp,Taxy,_,_)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:344:13` | `\+` | `tax/3` | `\+ s3301(Taxp,Taxy,_,_,_,_)` | TODO |

Variable-sensitive observations: all 25 `var`/`nonvar` sites follow. They do not settle call modes or a representation for absence. The empty-list clauses of `latest/2` and `earliest/2` visibly use anonymous output arguments; review their full clauses rather than assigning a default date.

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section152.pl:3:7` | `var` | `s152/3` | `var(Dependent)` | TODO |
| `human/sara/sara/statutes/prolog/section152.pl:3:23` | `var` | `s152/3` | `var(Taxp)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:86:9` | `var` | `s2_a_1_B/4` | `var(Start_dependent)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:90:9` | `var` | `s2_a_1_B/4` | `var(End_dependent)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:303:9` | `var` | `s2_b_1_B/5` | `var(Start_child)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:307:9` | `var` | `s2_b_1_B/5` | `var(End_child)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:442:13` | `var` | `s2_b_3_B/3` | `var(Start_relationship)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:446:13` | `var` | `s2_b_3_B/3` | `var(End_relationship)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:452:9` | `var` | `s2_b_3_B/3` | `var(StartH)` | TODO |
| `human/sara/sara/statutes/prolog/section2.pl:456:9` | `var` | `s2_b_3_B/3` | `var(EndH)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:428:13` | `var` | `s3306_c/5` | `var(Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:431:13` | `nonvar` | `s3306_c/5` | `nonvar(Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:513:5` | `nonvar` | `s3306_c_1_A/3` | `nonvar(Caly)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:4:9` | `nonvar` | `s7703/4` | `nonvar(Taxp)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:5:9` | `nonvar` | `s7703/4` | `nonvar(Spouse)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:11:5` | `nonvar` | `is_before/2` | `nonvar(Day1)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:11:19` | `nonvar` | `is_before/2` | `nonvar(Day2)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:29:9` | `nonvar` | `latest/2` | `nonvar(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:33:9` | `var` | `latest/2` | `var(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:41:9` | `nonvar` | `latest/3` | `nonvar(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:54:9` | `var` | `latest/3` | `var(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:63:9` | `nonvar` | `earliest/2` | `nonvar(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:67:9` | `var` | `earliest/2` | `var(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:75:9` | `nonvar` | `earliest/3` | `nonvar(Day)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:88:9` | `var` | `earliest/3` | `var(Day)` | TODO |

## Cut

Decision: TODO. Intended ordering, commitment and interaction with preceding goals/backtracking at each of the two sites: TODO. Both cuts occur in `s151_d_3_A/7`; the complete enclosing clause is retained in JSON.

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section151.pl:151:5` | `!` | `s151_d_3_A/7` | `!` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:153:5` | `!` | `s151_d_3_A/7` | `!` | TODO |

TODO observation: the snapshot also records 237 disjunction/if-then control tokens (`;`, `->` as present). Their evaluation order and interaction with NAF, cuts and unbound variables remain unresolved. See the `control_observation` tag and full clause excerpts; the inventory is not an execution trace.

## Aggregates

Decision: TODO. Duplicate and ordering semantics per site: TODO. Equality used for deduplication, empty aggregates, concatenation, variable scope, errors and unbound results: TODO.

Inventory: 43 `findall`, **zero `sumlist`**, and 12 `sum_list`. Both requested and observed sum spellings are tracked independently. Nested and multiline `findall` expressions are retained in full in JSON; an inner `findall` has its own token location as well as appearing in the outer excerpt.

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section151.pl:34:5` | `findall` | `s151_individual/5` | `findall( (Person,Exemption), s151_b(Taxp,Person,Exemption,Taxy), List_b )` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:41:5` | `findall` | `s151_individual/5` | `findall( (Person,Exemption), s151_c(Taxp,Person,Exemption,Taxy), List_c )` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:48:5` | `findall` | `s151_individual/5` | `findall( Person, member((Person,_),List_all_exemptions), Person_list )` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:53:5` | `findall` | `s151_individual/5` | `findall( Exemption, member((_,Exemption),List_all_exemptions), Exemptions_list )` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:58:5` | `sum_list` | `s151_individual/5` | `sum_list(Exemptions_list,S2)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:13:5` | `findall` | `total_wages_employer/6` | `findall( (Individual,Wages,Service), ( s3306_b(Wages,Remuneration,Service,Employer,Individual,Employer,_,_), start_(Remuneration,Remuneration_time), is_before(Start…` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:23:5` | `findall` | `total_wages_employer/6` | `findall( Individual, member((Individual,_,_),Individuals_x_wages), Individual_list )` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:29:5` | `findall` | `total_wages_employer/6` | `findall( (Individual,Total_wage), ( member(Individual, Individual_set), findall( Wage, member((Individual,Wage,_),Individuals_x_wages), Individual_wages ), sum_list…` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:33:13` | `findall` | `total_wages_employer/6` | `findall( Wage, member((Individual,Wage,_),Individuals_x_wages), Individual_wages )` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:38:13` | `sum_list` | `total_wages_employer/6` | `sum_list(Individual_wages,Wage_sum)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:43:5` | `findall` | `total_wages_employer/6` | `findall( Wage, ( member(Individual,Individual_set), member((Individual,Wage),Individuals_x_capped_wages) ), Capped_wages )` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:51:5` | `sum_list` | `total_wages_employer/6` | `sum_list(Capped_wages,Total_wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:52:5` | `findall` | `total_wages_employer/6` | `findall( Service, member((_,_,Service),Individuals_x_wages), Service_list )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:28:2` | `findall` | `s3306_a_1_A/3` | `findall( Amount, ( s3306_a_1_is_wages(Employee, Caly, Remuneration, Amount); ( Pyear is Caly-1, s3306_a_1_is_wages(Employee, Pyear, Remuneration, Amount) ) ), Wages…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:39:2` | `sum_list` | `s3306_a_1_A/3` | `sum_list(Wages_list,Wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:54:2` | `findall` | `s3306_a_1_B/4` | `findall( (Stamp,Day,Individual), ( s3306_a_1_is_day_of_employment(Employer,Individual,Day), is_before(First_day_year1,Day), is_before(Day,Last_day_year), day_to_sta…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:64:5` | `findall` | `s3306_a_1_B/4` | `findall( Stamp, member((Stamp,_,_),Stamp_day_individual), Emp_days )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:72:5` | `findall` | `s3306_a_1_B/4` | `findall( Week, ( member(Stamp,Emp_days), format_time(atom(Week), "%W", Stamp) ), Weeks )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:83:5` | `findall` | `s3306_a_1_B/4` | `findall( Day, member((_,Day,_),Stamp_day_individual), Workday )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:88:5` | `findall` | `s3306_a_1_B/4` | `findall( Individual, member((_,_,Individual),Stamp_day_individual), Employee )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:114:2` | `findall` | `s3306_a_2_A/4` | `findall( (Amount,Service_), ( s3306_a_2_is_wages(Employer, Caly, Epay, Amount, Service_); ( Pyear is Caly-1, s3306_a_2_is_wages(Employer, Pyear, Epay, Amount, Servi…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:125:5` | `findall` | `s3306_a_2_A/4` | `findall( Amount, member((Amount,_),Amount_service), Wageslist )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:130:5` | `findall` | `s3306_a_2_A/4` | `findall( Service_, member((_,Service_),Amount_service), Service )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:135:2` | `sum_list` | `s3306_a_2_A/4` | `sum_list(Wageslist,Wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:140:2` | `findall` | `s3306_a_2_is_day_of_employment/4` | `findall( (Employee,Service), ( s3306_c(Service,Person,Employee,Day,_), ( purpose_(Service,"agricultural labor"); type_(Service,"agricultural labor") ) ), Employee_x…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:151:5` | `findall` | `s3306_a_2_is_day_of_employment/4` | `findall( Employee, member((Employee,_),Employee_x_service), Employees )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:156:5` | `findall` | `s3306_a_2_is_day_of_employment/4` | `findall( Labor, member((_,Labor),Employee_x_service), Agricultural_labor )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:169:2` | `findall` | `s3306_a_2_B/6` | `findall( (Stamp,Day,Employees,Labor), ( s3306_c(_,Employer,_,Day,_), % narrow down the list of days s3306_a_2_is_day_of_employment(Employer,Employees,Labor,Day), % …` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:180:5` | `findall` | `s3306_a_2_B/6` | `findall( Stamp, member((Stamp,_,_,_),Stamp_day_employees_labor), Stamp_list )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:188:5` | `findall` | `s3306_a_2_B/6` | `findall( Week, ( member(Stamp,Stamp_list), format_time(atom(Week), "%W", Stamp) ), Weeks )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:199:5` | `findall` | `s3306_a_2_B/6` | `findall( Employees, member((_,_,Employees,_),Stamp_day_employees_labor), Employee )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:204:5` | `findall` | `s3306_a_2_B/6` | `findall( Labor, member((_,_,_,Labor),Stamp_day_employees_labor), Service )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:209:5` | `findall` | `s3306_a_2_B/6` | `findall( Day, member((_,Day,_,_),Stamp_day_employees_labor), Days_list )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:237:2` | `findall` | `s3306_a_3/4` | `findall( (Amount,Service_), ( s3306_a_3_is_wages(Employer, Caly, Epay, Service_, Amount); ( Pyear is Caly-1, s3306_a_3_is_wages(Employer, Pyear, Epay, Service_, Amo…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:248:5` | `findall` | `s3306_a_3/4` | `findall( Amount, member((Amount,_),Amount_service), Wages_list )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:253:5` | `findall` | `s3306_a_3/4` | `findall( Service_, member((_,Service_),Amount_service), Service )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:258:2` | `sum_list` | `s3306_a_3/4` | `sum_list(Wages_list,Wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:524:5` | `findall` | `s3306_c_1_A_i/5` | `findall( (Amount,Employee_,Service_), ( payment_(Payment), agent_(Payment,Employer), patient_(Payment,Employee_), service_(Service_), agent_(Service_,Employee_), pa…` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:551:5` | `findall` | `s3306_c_1_A_i/5` | `findall( Amount, member((Amount,_,_),Amounts_employee_service), Amounts )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:556:5` | `sum_list` | `s3306_c_1_A_i/5` | `sum_list(Amounts,Remuneration)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:558:5` | `findall` | `s3306_c_1_A_i/5` | `findall( Individual, member((_,Individual,_),Amounts_employee_service), Employee )` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:563:5` | `findall` | `s3306_c_1_A_i/5` | `findall( Service_, member((_,_,Service_),Amounts_employee_service), Service )` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:274:2` | `findall` | `s63_d/4` | `findall( (Amount,Deduction), ( deduction_(Deduction), agent_(Deduction,Taxp), amount_(Deduction,Amount), start_(Deduction,Start), is_before(First,Start), is_before(…` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:286:2` | `findall` | `s63_d/4` | `findall( Amount, member((Amount,_),Amount_deduction), Amounts )` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:293:2` | `sum_list` | `s63_d/4` | `sum_list(Amounts,Total_amount)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:294:2` | `findall` | `s63_d/4` | `findall( Deduction, member((_,Deduction),Amount_deduction), Itemded )` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:143:5` | `findall` | `s7703_b_2/4` | `findall( Payment_amount, ( payment_(Payment), residence_(Residence), agent_(Payment,Taxp), patient_(Residence,Household), ( purpose_(Payment,Residence); purpose_(Pa…` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:162:2` | `findall` | `s7703_b_2/4` | `findall( Payment_amount, ( payment_(Payment), residence_(Residence), patient_(Residence,Household), ( purpose_(Payment,Residence); purpose_(Payment,Household) ), am…` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:180:2` | `sum_list` | `s7703_b_2/4` | `sum_list(Payments_by_individual,Payment_by_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:181:2` | `sum_list` | `s7703_b_2/4` | `sum_list(Payments_all,Cost)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:205:5` | `findall` | `s7703_b_3/4` | `findall( Day_offset, ( between(2,185,Day_offset), date_time_stamp(date(Taxy,7,Day_offset,0,0,0,0,-,-), Stamp), format_time(atom(Day), "%Y-%m-%d", Stamp), s7703_b_3_…` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:304:5` | `findall` | `gross_income_individual/3` | `findall( Amount, ( income_(Income), agent_(Income,Person), amount_(Income,Amount), start_(Income,Start_time), is_before(First_day_year,Start_time), is_before(Start_…` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:316:5` | `findall` | `gross_income_individual/3` | `findall( Amount, ( payment_(Payment), patient_(Payment,Person), amount_(Payment,Amount), start_(Payment,Start_time), is_before(First_day_year,Start_time), is_before…` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:328:5` | `sum_list` | `gross_income_individual/3` | `sum_list(Income_amounts,Income)` | TODO |
| `human/sara/sara/statutes/prolog/utils.pl:329:5` | `sum_list` | `gross_income_individual/3` | `sum_list(Payment_amounts,Payment)` | TODO |

List-processing observations (48 total, including nine `list_to_set` sites; comparison tags may overlap):

| Source token location | Syntax | Enclosing predicate | Construct preview | Decision |
| --- | --- | --- | --- | --- |
| `human/sara/sara/statutes/prolog/section151.pl:16:13` | `append` | `s151/5` | `append(Indiv_list_taxpayer,Indiv_list_spouse,Person_list)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:17:13` | `append` | `s151/5` | `append(Ex_list_taxpayer,Ex_list_spouse,Exemptions_list)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:39:5` | `append` | `s151_individual/5` | `append([(Taxp,Exemption_amount_self)],List_b,List_b_2)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:40:5` | `list_to_set` | `s151_individual/5` | `list_to_set(List_b_2,Set_b)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:46:5` | `list_to_set` | `s151_individual/5` | `list_to_set(List_c,Set_c)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:47:5` | `append` | `s151_individual/5` | `append(Set_b,Set_c,List_all_exemptions)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:50:9` | `member` | `s151_individual/5` | `member((Person,_),List_all_exemptions)` | TODO |
| `human/sara/sara/statutes/prolog/section151.pl:55:9` | `member` | `s151_individual/5` | `member((_,Exemption),List_all_exemptions)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:25:9` | `member` | `total_wages_employer/6` | `member((Individual,_,_),Individuals_x_wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:28:5` | `list_to_set` | `total_wages_employer/6` | `list_to_set(Individual_list,Individual_set)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:32:13` | `member` | `total_wages_employer/6` | `member(Individual, Individual_set)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:35:17` | `member` | `total_wages_employer/6` | `member((Individual,Wage,_),Individuals_x_wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:46:13` | `member` | `total_wages_employer/6` | `member(Individual,Individual_set)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:47:13` | `member` | `total_wages_employer/6` | `member((Individual,Wage),Individuals_x_capped_wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3301.pl:54:9` | `member` | `total_wages_employer/6` | `member((_,_,Service),Individuals_x_wages)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:66:9` | `member` | `s3306_a_1_B/4` | `member((Stamp,_,_),Stamp_day_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:69:5` | `list_to_set` | `s3306_a_1_B/4` | `list_to_set(Emp_days,Emp_days_set)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:70:2` | `length` | `s3306_a_1_B/4` | `length(Emp_days_set,Num_days)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:75:4` | `member` | `s3306_a_1_B/4` | `member(Stamp,Emp_days)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:80:2` | `list_to_set` | `s3306_a_1_B/4` | `list_to_set(Weeks,Weeks_set)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:81:2` | `length` | `s3306_a_1_B/4` | `length(Weeks_set,Num_weeks)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:85:9` | `member` | `s3306_a_1_B/4` | `member((_,Day,_),Stamp_day_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:90:9` | `member` | `s3306_a_1_B/4` | `member((_,_,Individual),Stamp_day_individual)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:127:9` | `member` | `s3306_a_2_A/4` | `member((Amount,_),Amount_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:132:9` | `member` | `s3306_a_2_A/4` | `member((_,Service_),Amount_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:153:9` | `member` | `s3306_a_2_is_day_of_employment/4` | `member((Employee,_),Employee_x_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:158:9` | `member` | `s3306_a_2_is_day_of_employment/4` | `member((_,Labor),Employee_x_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:161:5` | `list_to_set` | `s3306_a_2_is_day_of_employment/4` | `list_to_set(Employees,Individuals)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:162:2` | `length` | `s3306_a_2_is_day_of_employment/4` | `length(Individuals,Num_employees)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:182:9` | `member` | `s3306_a_2_B/6` | `member((Stamp,_,_,_),Stamp_day_employees_labor)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:185:2` | `list_to_set` | `s3306_a_2_B/6` | `list_to_set(Stamp_list,Days_stamp)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:186:2` | `length` | `s3306_a_2_B/6` | `length(Days_stamp,Num_days)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:191:4` | `member` | `s3306_a_2_B/6` | `member(Stamp,Stamp_list)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:196:5` | `list_to_set` | `s3306_a_2_B/6` | `list_to_set(Weeks,S33)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:197:2` | `length` | `s3306_a_2_B/6` | `length(S33,Num_weeks)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:201:9` | `member` | `s3306_a_2_B/6` | `member((_,_,Employees,_),Stamp_day_employees_labor)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:206:9` | `member` | `s3306_a_2_B/6` | `member((_,_,_,Labor),Stamp_day_employees_labor)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:211:9` | `member` | `s3306_a_2_B/6` | `member((_,Day,_,_),Stamp_day_employees_labor)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:214:5` | `list_to_set` | `s3306_a_2_B/6` | `list_to_set(Days_list,Workday)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:250:9` | `member` | `s3306_a_3/4` | `member((Amount,_),Amount_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:255:9` | `member` | `s3306_a_3/4` | `member((_,Service_),Amount_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:553:9` | `member` | `s3306_c_1_A_i/5` | `member((Amount,_,_),Amounts_employee_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:560:9` | `member` | `s3306_c_1_A_i/5` | `member((_,Individual,_),Amounts_employee_service)` | TODO |
| `human/sara/sara/statutes/prolog/section3306.pl:565:9` | `member` | `s3306_c_1_A_i/5` | `member((_,_,Service_),Amounts_employee_service)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:288:3` | `member` | `s63_d/4` | `member((Amount,_),Amount_deduction)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:291:2` | `length` | `s63_d/4` | `length(Amounts,L)` | TODO |
| `human/sara/sara/statutes/prolog/section63.pl:296:3` | `member` | `s63_d/4` | `member((_,Deduction),Amount_deduction)` | TODO |
| `human/sara/sara/statutes/prolog/section7703.pl:215:5` | `length` | `s7703_b_3/4` | `length(Days_membership,Num_days)` | TODO |

## Recursion

Decision: TODO. A termination strategy and permitted modes/domain per recursive candidate: TODO. No cycle has been declared divergent, harmless, well-founded or unreachable.

Inventory: 40 predicate signatures in ten strongly connected components of the lexical dependency graph. Six single-predicate components have a direct self-reference; four components have mutual references. An edge means an unquoted functor name/arity in a body matches a defined predicate. Nested terms, NAF and `findall` are included conservatively. Predicate heads and declarations do not create edges. Meta-calls, bare-atom/variable/quoted/external calls and module semantics are not resolved, so these are candidates, not a complete runtime call graph.

| Component | Predicate candidate | Definition locations | Termination / modes decision |
| --- | --- | --- | --- |
| R1 (direct) | `amount/2` | `human/sara/sara/statutes/prolog/section68.pl:52:1`; `human/sara/sara/statutes/prolog/section68.pl:54:1`; `human/sara/sara/statutes/prolog/section68.pl:56:1`; `human/sara/sara/statutes/prolog/section68.pl:58:1` | TODO |
| R2 (direct) | `earliest/2` | `human/sara/sara/statutes/prolog/utils.pl:59:1`; `human/sara/sara/statutes/prolog/utils.pl:61:1` | TODO |
| R3 (direct) | `earliest/3` | `human/sara/sara/statutes/prolog/utils.pl:71:1`; `human/sara/sara/statutes/prolog/utils.pl:73:1` | TODO |
| R4 (direct) | `is_descendent_of/4` | `human/sara/sara/statutes/prolog/utils.pl:158:1` | TODO |
| R5 (direct) | `latest/2` | `human/sara/sara/statutes/prolog/utils.pl:25:1`; `human/sara/sara/statutes/prolog/utils.pl:27:1` | TODO |
| R6 (direct) | `latest/3` | `human/sara/sara/statutes/prolog/utils.pl:37:1`; `human/sara/sara/statutes/prolog/utils.pl:39:1` | TODO |
| R7 (mutual) | `s151_c/4` | `human/sara/sara/statutes/prolog/section151.pl:98:1` | TODO |
| R7 (mutual) | `s151_d/3` | `human/sara/sara/statutes/prolog/section151.pl:105:1` | TODO |
| R7 (mutual) | `s151_d_3/4` | `human/sara/sara/statutes/prolog/section151.pl:143:1` | TODO |
| R7 (mutual) | `s151_d_3_A/7` | `human/sara/sara/statutes/prolog/section151.pl:149:1` | TODO |
| R7 (mutual) | `s151_d_3_B/5` | `human/sara/sara/statutes/prolog/section151.pl:162:1` | TODO |
| R7 (mutual) | `s2_b/3` | `human/sara/sara/statutes/prolog/section2.pl:146:1` | TODO |
| R7 (mutual) | `s2_b_1/4` | `human/sara/sara/statutes/prolog/section2.pl:154:1` | TODO |
| R7 (mutual) | `s2_b_1_B/5` | `human/sara/sara/statutes/prolog/section2.pl:281:1` | TODO |
| R7 (mutual) | `s68_b/3` | `human/sara/sara/statutes/prolog/section68.pl:43:1` | TODO |
| R7 (mutual) | `s68_b_1_B/3` | `human/sara/sara/statutes/prolog/section68.pl:80:1` | TODO |
| R7 (mutual) | `s68_b_1_C/3` | `human/sara/sara/statutes/prolog/section68.pl:85:1` | TODO |
| R8 (mutual) | `s152/3` | `human/sara/sara/statutes/prolog/section152.pl:2:1` | TODO |
| R8 (mutual) | `s152_b_1/3` | `human/sara/sara/statutes/prolog/section152.pl:38:1` | TODO |
| R9 (mutual) | `s152_a_1/3` | `human/sara/sara/statutes/prolog/section152.pl:19:1` | TODO |
| R9 (mutual) | `s152_c/3` | `human/sara/sara/statutes/prolog/section152.pl:57:1` | TODO |
| R9 (mutual) | `s152_c_1/3` | `human/sara/sara/statutes/prolog/section152.pl:63:1` | TODO |
| R9 (mutual) | `s152_c_1_E/3` | `human/sara/sara/statutes/prolog/section152.pl:143:1` | TODO |
| R9 (mutual) | `s7703/4` | `human/sara/sara/statutes/prolog/section7703.pl:2:1` | TODO |
| R9 (mutual) | `s7703_b/3` | `human/sara/sara/statutes/prolog/section7703.pl:103:1` | TODO |
| R9 (mutual) | `s7703_b_1/4` | `human/sara/sara/statutes/prolog/section7703.pl:110:1` | TODO |
| R10 (mutual) | `s3306_a_2_B/6` | `human/sara/sara/statutes/prolog/section3306.pl:165:1` | TODO |
| R10 (mutual) | `s3306_a_2_is_day_of_employment/4` | `human/sara/sara/statutes/prolog/section3306.pl:139:1` | TODO |
| R10 (mutual) | `s3306_a_3/4` | `human/sara/sara/statutes/prolog/section3306.pl:236:1` | TODO |
| R10 (mutual) | `s3306_a_3_is_wages/5` | `human/sara/sara/statutes/prolog/section3306.pl:219:1` | TODO |
| R10 (mutual) | `s3306_b/8` | `human/sara/sara/statutes/prolog/section3306.pl:270:1` | TODO |
| R10 (mutual) | `s3306_b_10/6` | `human/sara/sara/statutes/prolog/section3306.pl:353:1` | TODO |
| R10 (mutual) | `s3306_b_15/5` | `human/sara/sara/statutes/prolog/section3306.pl:404:1` | TODO |
| R10 (mutual) | `s3306_b_2/6` | `human/sara/sara/statutes/prolog/section3306.pl:309:1` | TODO |
| R10 (mutual) | `s3306_b_7/6` | `human/sara/sara/statutes/prolog/section3306.pl:342:1` | TODO |
| R10 (mutual) | `s3306_c/5` | `human/sara/sara/statutes/prolog/section3306.pl:424:1` | TODO |
| R10 (mutual) | `s3306_c_1/2` | `human/sara/sara/statutes/prolog/section3306.pl:499:1` | TODO |
| R10 (mutual) | `s3306_c_1_A/3` | `human/sara/sara/statutes/prolog/section3306.pl:510:1` | TODO |
| R10 (mutual) | `s3306_c_1_A_ii/6` | `human/sara/sara/statutes/prolog/section3306.pl:570:1` | TODO |
| R10 (mutual) | `s3306_c_2/3` | `human/sara/sara/statutes/prolog/section3306.pl:591:1` | TODO |

All within-component lexical edges, with their source occurrence locations:

- R1: `amount/2` → `amount/2` at `human/sara/sara/statutes/prolog/section68.pl:59:5`.
- R2: `earliest/2` → `earliest/2` at `human/sara/sara/statutes/prolog/utils.pl:68:9`.
- R3: `earliest/3` → `earliest/3` at `human/sara/sara/statutes/prolog/utils.pl:79:17`; `human/sara/sara/statutes/prolog/utils.pl:83:17`; `human/sara/sara/statutes/prolog/utils.pl:89:9`.
- R4: `is_descendent_of/4` → `is_descendent_of/4` at `human/sara/sara/statutes/prolog/utils.pl:164:3`.
- R5: `latest/2` → `latest/2` at `human/sara/sara/statutes/prolog/utils.pl:34:9`.
- R6: `latest/3` → `latest/3` at `human/sara/sara/statutes/prolog/utils.pl:45:17`; `human/sara/sara/statutes/prolog/utils.pl:49:17`; `human/sara/sara/statutes/prolog/utils.pl:55:9`.
- R7: `s151_c/4` → `s151_d/3` at `human/sara/sara/statutes/prolog/section151.pl:100:5`.
- R7: `s151_d/3` → `s151_d_3/4` at `human/sara/sara/statutes/prolog/section151.pl:116:17`; `human/sara/sara/statutes/prolog/section151.pl:118:24`.
- R7: `s151_d_3/4` → `s151_d_3_A/7` at `human/sara/sara/statutes/prolog/section151.pl:144:5`.
- R7: `s151_d_3_A/7` → `s151_d_3_B/5` at `human/sara/sara/statutes/prolog/section151.pl:155:5`.
- R7: `s151_d_3_A/7` → `s68_b/3` at `human/sara/sara/statutes/prolog/section151.pl:152:5`.
- R7: `s151_d_3_B/5` → `s68_b/3` at `human/sara/sara/statutes/prolog/section151.pl:164:5`.
- R7: `s2_b/3` → `s2_b_1/4` at `human/sara/sara/statutes/prolog/section2.pl:147:5`.
- R7: `s2_b_1/4` → `s2_b_1_B/5` at `human/sara/sara/statutes/prolog/section2.pl:199:9`.
- R7: `s2_b_1_B/5` → `s151_c/4` at `human/sara/sara/statutes/prolog/section2.pl:309:5`.
- R7: `s68_b/3` → `s68_b_1_B/3` at `human/sara/sara/statutes/prolog/section68.pl:45:5`.
- R7: `s68_b/3` → `s68_b_1_C/3` at `human/sara/sara/statutes/prolog/section68.pl:46:5`.
- R7: `s68_b_1_B/3` → `s2_b/3` at `human/sara/sara/statutes/prolog/section68.pl:81:5`.
- R7: `s68_b_1_C/3` → `s2_b/3` at `human/sara/sara/statutes/prolog/section68.pl:88:8`.
- R8: `s152/3` → `s152_b_1/3` at `human/sara/sara/statutes/prolog/section152.pl:5:5`.
- R8: `s152_b_1/3` → `s152/3` at `human/sara/sara/statutes/prolog/section152.pl:39:5`.
- R9: `s152_a_1/3` → `s152_c/3` at `human/sara/sara/statutes/prolog/section152.pl:20:5`.
- R9: `s152_c/3` → `s152_c_1/3` at `human/sara/sara/statutes/prolog/section152.pl:58:5`.
- R9: `s152_c_1/3` → `s152_c_1_E/3` at `human/sara/sara/statutes/prolog/section152.pl:67:5`.
- R9: `s152_c_1_E/3` → `s7703/4` at `human/sara/sara/statutes/prolog/section152.pl:145:9`.
- R9: `s7703/4` → `s7703_b/3` at `human/sara/sara/statutes/prolog/section7703.pl:9:5`.
- R9: `s7703_b/3` → `s7703_b_1/4` at `human/sara/sara/statutes/prolog/section7703.pl:104:2`.
- R9: `s7703_b_1/4` → `s152_a_1/3` at `human/sara/sara/statutes/prolog/section7703.pl:139:5`.
- R10: `s3306_a_2_B/6` → `s3306_a_2_is_day_of_employment/4` at `human/sara/sara/statutes/prolog/section3306.pl:173:4`.
- R10: `s3306_a_2_B/6` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:172:13`.
- R10: `s3306_a_2_is_day_of_employment/4` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:143:13`.
- R10: `s3306_a_3/4` → `s3306_a_3_is_wages/5` at `human/sara/sara/statutes/prolog/section3306.pl:240:4`; `human/sara/sara/statutes/prolog/section3306.pl:243:5`.
- R10: `s3306_a_3_is_wages/5` → `s3306_b/8` at `human/sara/sara/statutes/prolog/section3306.pl:220:5`.
- R10: `s3306_b/8` → `s3306_b_10/6` at `human/sara/sara/statutes/prolog/section3306.pl:300:5`.
- R10: `s3306_b/8` → `s3306_b_15/5` at `human/sara/sara/statutes/prolog/section3306.pl:302:8`.
- R10: `s3306_b/8` → `s3306_b_2/6` at `human/sara/sara/statutes/prolog/section3306.pl:298:5`.
- R10: `s3306_b/8` → `s3306_b_7/6` at `human/sara/sara/statutes/prolog/section3306.pl:299:8`.
- R10: `s3306_b/8` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:295:2`.
- R10: `s3306_b_10/6` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:354:2`.
- R10: `s3306_b_15/5` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:405:5`.
- R10: `s3306_b_2/6` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:310:2`.
- R10: `s3306_b_7/6` → `s3306_c/5` at `human/sara/sara/statutes/prolog/section3306.pl:343:2`.
- R10: `s3306_c/5` → `s3306_c_1/2` at `human/sara/sara/statutes/prolog/section3306.pl:440:5`.
- R10: `s3306_c/5` → `s3306_c_2/3` at `human/sara/sara/statutes/prolog/section3306.pl:441:5`.
- R10: `s3306_c_1/2` → `s3306_c_1_A/3` at `human/sara/sara/statutes/prolog/section3306.pl:505:3`.
- R10: `s3306_c_1_A/3` → `s3306_c_1_A_ii/6` at `human/sara/sara/statutes/prolog/section3306.pl:516:3`.
- R10: `s3306_c_1_A_ii/6` → `s3306_a_2_B/6` at `human/sara/sara/statutes/prolog/section3306.pl:571:2`.
- R10: `s3306_c_2/3` → `s3306_a_3/4` at `human/sara/sara/statutes/prolog/section3306.pl:604:5`.

TODO observation: `amount/2` appears as a direct candidate because its `"D"` clause calls the same name/arity with `"A"`. This lexical cycle alone establishes neither recursive execution for every input nor divergence. Similarly, the list/kinship and cross-section components require owner-approved modes and domain assumptions before any termination strategy is selected.

## Axioms

Decision: TODO. Owner-approved whitelist: TODO. The plan names `propext`, `Quot.sound`, and `Classical.choice` as the proposed whitelist; this template does not approve it. No Lean declaration, axiom dependency, proof or gate implementation was analyzed or changed by this inventory.

Uncovered builtin/runtime semantics remain TODO. The table lists every functor signature without a definition in the scanned files. These are **unresolved functor shapes**, not a claim that each is a builtin or even an executed call: they include fact predicates, constructors such as `date/9`, and arithmetic groupings. Full occurrence lists and exact source spans are in `functor_index`. Also review `events.pl` declarations and `init.pl` loading, which are present in the clause inventory. The required SWI-Prolog 7.2.3/linux-amd64 runtime is specified in the source contract; no runtime was executed here.

| Unresolved signature | Body/directive occurrences | Example locations (all in JSON) | Semantics decision |
| --- | ---: | --- | --- |
| `*/1` | 1 | `human/sara/sara/statutes/prolog/section68.pl:32:11` | TODO |
| `+/1` | 16 | `human/sara/sara/statutes/prolog/section1.pl:75:22`; `human/sara/sara/statutes/prolog/section1.pl:80:23`; `human/sara/sara/statutes/prolog/section1.pl:85:26` | TODO |
| `agent_/2` | 154 | `human/sara/sara/statutes/prolog/section1.pl:21:5`; `human/sara/sara/statutes/prolog/section1.pl:22:5`; `human/sara/sara/statutes/prolog/section1.pl:30:13` | TODO |
| `american_employer_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:492:5` | TODO |
| `amount_/2` | 7 | `human/sara/sara/statutes/prolog/section3306.pl:296:2`; `human/sara/sara/statutes/prolog/section3306.pl:538:13`; `human/sara/sara/statutes/prolog/section63.pl:279:10` | TODO |
| `append/3` | 4 | `human/sara/sara/statutes/prolog/section151.pl:16:13`; `human/sara/sara/statutes/prolog/section151.pl:17:13`; `human/sara/sara/statutes/prolog/section151.pl:39:5` | TODO |
| `atom/1` | 3 | `human/sara/sara/statutes/prolog/section3306.pl:76:16`; `human/sara/sara/statutes/prolog/section3306.pl:192:16`; `human/sara/sara/statutes/prolog/section7703.pl:210:25` | TODO |
| `atom_number/2` | 10 | `human/sara/sara/statutes/prolog/section2.pl:26:5`; `human/sara/sara/statutes/prolog/section3306.pl:294:2`; `human/sara/sara/statutes/prolog/section3306.pl:357:2` | TODO |
| `atom_prefix/2` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:665:2` | TODO |
| `atom_string/2` | 2 | `human/sara/sara/statutes/prolog/utils.pl:17:2`; `human/sara/sara/statutes/prolog/utils.pl:21:2` | TODO |
| `attending_classes_/1` | 2 | `human/sara/sara/statutes/prolog/section3306.pl:690:2`; `human/sara/sara/statutes/prolog/section3306.pl:785:2` | TODO |
| `beneficiary_/2` | 2 | `human/sara/sara/statutes/prolog/section3306.pl:285:13`; `human/sara/sara/statutes/prolog/section3306.pl:314:2` | TODO |
| `between/3` | 3 | `human/sara/sara/statutes/prolog/section151.pl:192:5`; `human/sara/sara/statutes/prolog/section68.pl:111:5`; `human/sara/sara/statutes/prolog/section7703.pl:208:13` | TODO |
| `birth_/1` | 7 | `human/sara/sara/statutes/prolog/section152.pl:198:13`; `human/sara/sara/statutes/prolog/section152.pl:201:13`; `human/sara/sara/statutes/prolog/section152.pl:208:17` | TODO |
| `blindness_/1` | 2 | `human/sara/sara/statutes/prolog/section63.pl:363:5`; `human/sara/sara/statutes/prolog/section63.pl:372:5` | TODO |
| `brother_/1` | 1 | `human/sara/sara/statutes/prolog/utils.pl:133:3` | TODO |
| `business_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:346:5` | TODO |
| `business_trust_/1` | 1 | `human/sara/sara/statutes/prolog/section63.pl:225:5` | TODO |
| `ceil/1` | 2 | `human/sara/sara/statutes/prolog/section151.pl:180:25`; `human/sara/sara/statutes/prolog/section151.pl:183:25` | TODO |
| `citizenship_/1` | 2 | `human/sara/sara/statutes/prolog/section3306.pl:494:2`; `human/sara/sara/statutes/prolog/section3306.pl:580:3` | TODO |
| `country_/2` | 4 | `human/sara/sara/statutes/prolog/section3306.pl:464:13`; `human/sara/sara/statutes/prolog/section3306.pl:468:16`; `human/sara/sara/statutes/prolog/section3306.pl:479:13` | TODO |
| `date/9` | 4 | `human/sara/sara/statutes/prolog/section3306.pl:651:25`; `human/sara/sara/statutes/prolog/section3306.pl:653:25`; `human/sara/sara/statutes/prolog/section7703.pl:209:29` | TODO |
| `date_time_stamp/2` | 4 | `human/sara/sara/statutes/prolog/section3306.pl:651:9`; `human/sara/sara/statutes/prolog/section3306.pl:653:9`; `human/sara/sara/statutes/prolog/section7703.pl:209:13` | TODO |
| `daughter_/1` | 2 | `human/sara/sara/statutes/prolog/section152.pl:221:3`; `human/sara/sara/statutes/prolog/utils.pl:103:17` | TODO |
| `death_/1` | 12 | `human/sara/sara/statutes/prolog/section152.pl:74:4`; `human/sara/sara/statutes/prolog/section152.pl:81:4`; `human/sara/sara/statutes/prolog/section152.pl:251:4` | TODO |
| `deduction_/1` | 2 | `human/sara/sara/statutes/prolog/section63.pl:189:4`; `human/sara/sara/statutes/prolog/section63.pl:277:10` | TODO |
| `destination_/2` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:586:3` | TODO |
| `disability_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:379:3` | TODO |
| `educational_institution_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:676:2` | TODO |
| `end_/2` | 95 | `human/sara/sara/statutes/prolog/section1.pl:26:5`; `human/sara/sara/statutes/prolog/section1.pl:42:20`; `human/sara/sara/statutes/prolog/section1.pl:45:13` | TODO |
| `enrollment_/1` | 2 | `human/sara/sara/statutes/prolog/section3306.pl:686:2`; `human/sara/sara/statutes/prolog/section3306.pl:781:2` | TODO |
| `father_/1` | 1 | `human/sara/sara/statutes/prolog/utils.pl:110:5` | TODO |
| `findall/3` | 43 | `human/sara/sara/statutes/prolog/section151.pl:34:5`; `human/sara/sara/statutes/prolog/section151.pl:41:5`; `human/sara/sara/statutes/prolog/section151.pl:48:5` | TODO |
| `format_time/3` | 3 | `human/sara/sara/statutes/prolog/section3306.pl:76:4`; `human/sara/sara/statutes/prolog/section3306.pl:192:4`; `human/sara/sara/statutes/prolog/section7703.pl:210:13` | TODO |
| `hospital_/1` | 2 | `human/sara/sara/statutes/prolog/section3306.pl:745:2`; `human/sara/sara/statutes/prolog/section3306.pl:776:9` | TODO |
| `incarceration_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:822:2` | TODO |
| `income_/1` | 1 | `human/sara/sara/statutes/prolog/utils.pl:307:13` | TODO |
| `international_organization_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:814:2` | TODO |
| `joint_return_/1` | 15 | `human/sara/sara/statutes/prolog/section1.pl:20:5`; `human/sara/sara/statutes/prolog/section1.pl:175:9`; `human/sara/sara/statutes/prolog/section151.pl:8:13` | TODO |
| `legal_separation_/1` | 2 | `human/sara/sara/statutes/prolog/section2.pl:324:5`; `human/sara/sara/statutes/prolog/section7703.pl:90:2` | TODO |
| `length/2` | 7 | `human/sara/sara/statutes/prolog/section3306.pl:70:2`; `human/sara/sara/statutes/prolog/section3306.pl:81:2`; `human/sara/sara/statutes/prolog/section3306.pl:162:2` | TODO |
| `list_to_set/2` | 9 | `human/sara/sara/statutes/prolog/section151.pl:40:5`; `human/sara/sara/statutes/prolog/section151.pl:46:5`; `human/sara/sara/statutes/prolog/section3301.pl:28:5` | TODO |
| `location_/2` | 5 | `human/sara/sara/statutes/prolog/section3306.pl:456:9`; `human/sara/sara/statutes/prolog/section3306.pl:458:16`; `human/sara/sara/statutes/prolog/section3306.pl:597:5` | TODO |
| `marriage_/1` | 17 | `human/sara/sara/statutes/prolog/section152.pl:348:9`; `human/sara/sara/statutes/prolog/section2.pl:17:5`; `human/sara/sara/statutes/prolog/section2.pl:104:5` | TODO |
| `max/2` | 6 | `human/sara/sara/statutes/prolog/section151.pl:157:11`; `human/sara/sara/statutes/prolog/section151.pl:165:19`; `human/sara/sara/statutes/prolog/section63.pl:10:12` | TODO |
| `means_/2` | 10 | `human/sara/sara/statutes/prolog/section3306.pl:228:7`; `human/sara/sara/statutes/prolog/section3306.pl:231:4`; `human/sara/sara/statutes/prolog/section3306.pl:273:13` | TODO |
| `medical_patient_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:747:2` | TODO |
| `member/2` | 28 | `human/sara/sara/statutes/prolog/section151.pl:50:9`; `human/sara/sara/statutes/prolog/section151.pl:55:9`; `human/sara/sara/statutes/prolog/section3301.pl:25:9` | TODO |
| `migration_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:584:3` | TODO |
| `min/2` | 4 | `human/sara/sara/statutes/prolog/section151.pl:186:11`; `human/sara/sara/statutes/prolog/section3306.pl:306:22`; `human/sara/sara/statutes/prolog/section63.pl:69:22` | TODO |
| `mother_/1` | 1 | `human/sara/sara/statutes/prolog/utils.pl:111:17` | TODO |
| `nonresident_alien_/1` | 5 | `human/sara/sara/statutes/prolog/section1.pl:28:9`; `human/sara/sara/statutes/prolog/section2.pl:118:9`; `human/sara/sara/statutes/prolog/section2.pl:341:5` | TODO |
| `nonvar/1` | 10 | `human/sara/sara/statutes/prolog/section3306.pl:431:13`; `human/sara/sara/statutes/prolog/section3306.pl:513:5`; `human/sara/sara/statutes/prolog/section7703.pl:4:9` | TODO |
| `nurses_training_school_/1` | 2 | `human/sara/sara/statutes/prolog/section3306.pl:775:9`; `human/sara/sara/statutes/prolog/section3306.pl:779:5` | TODO |
| `patient_/2` | 52 | `human/sara/sara/statutes/prolog/section152.pl:92:5`; `human/sara/sara/statutes/prolog/section152.pl:111:5`; `human/sara/sara/statutes/prolog/section152.pl:363:5` | TODO |
| `payment_/1` | 6 | `human/sara/sara/statutes/prolog/section3306.pl:271:2`; `human/sara/sara/statutes/prolog/section3306.pl:311:2`; `human/sara/sara/statutes/prolog/section3306.pl:527:13` | TODO |
| `penal_institution_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:820:2` | TODO |
| `plan_/1` | 4 | `human/sara/sara/statutes/prolog/section3306.pl:280:16`; `human/sara/sara/statutes/prolog/section3306.pl:284:13`; `human/sara/sara/statutes/prolog/section3306.pl:313:2` | TODO |
| `purpose_/2` | 24 | `human/sara/sara/statutes/prolog/section3306.pl:24:8`; `human/sara/sara/statutes/prolog/section3306.pl:25:5`; `human/sara/sara/statutes/prolog/section3306.pl:45:8` | TODO |
| `rational/1` | 1 | `human/sara/sara/statutes/prolog/section7703.pl:184:9` | TODO |
| `reason_/2` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:378:2` | TODO |
| `residence_/1` | 14 | `human/sara/sara/statutes/prolog/section152.pl:90:5`; `human/sara/sara/statutes/prolog/section152.pl:109:5`; `human/sara/sara/statutes/prolog/section152.pl:361:5` | TODO |
| `round/1` | 25 | `human/sara/sara/statutes/prolog/section1.pl:70:12`; `human/sara/sara/statutes/prolog/section1.pl:75:12`; `human/sara/sara/statutes/prolog/section1.pl:80:12` | TODO |
| `service_/1` | 10 | `human/sara/sara/statutes/prolog/section3306.pl:288:2`; `human/sara/sara/statutes/prolog/section3306.pl:393:5`; `human/sara/sara/statutes/prolog/section3306.pl:425:2` | TODO |
| `sister_/1` | 1 | `human/sara/sara/statutes/prolog/utils.pl:134:3` | TODO |
| `son_/1` | 2 | `human/sara/sara/statutes/prolog/section152.pl:220:3`; `human/sara/sara/statutes/prolog/utils.pl:102:17` | TODO |
| `split_string/4` | 12 | `human/sara/sara/statutes/prolog/section2.pl:25:5`; `human/sara/sara/statutes/prolog/section3306.pl:293:2`; `human/sara/sara/statutes/prolog/section3306.pl:356:2` | TODO |
| `start_/2` | 106 | `human/sara/sara/statutes/prolog/section1.pl:25:5`; `human/sara/sara/statutes/prolog/section1.pl:35:20`; `human/sara/sara/statutes/prolog/section1.pl:38:13` | TODO |
| `string_concat/3` | 2 | `human/sara/sara/statutes/prolog/utils.pl:18:2`; `human/sara/sara/statutes/prolog/utils.pl:22:2` | TODO |
| `sub_atom/5` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:766:2` | TODO |
| `sum_list/2` | 12 | `human/sara/sara/statutes/prolog/section151.pl:58:5`; `human/sara/sara/statutes/prolog/section3301.pl:38:13`; `human/sara/sara/statutes/prolog/section3301.pl:51:5` | TODO |
| `termination_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:373:2` | TODO |
| `type_/2` | 9 | `human/sara/sara/statutes/prolog/section3306.pl:47:8`; `human/sara/sara/statutes/prolog/section3306.pl:48:8`; `human/sara/sara/statutes/prolog/section3306.pl:146:17` | TODO |
| `unemployment_compensation_agreement_/1` | 1 | `human/sara/sara/statutes/prolog/section3306.pl:488:3` | TODO |
| `var/1` | 15 | `human/sara/sara/statutes/prolog/section152.pl:3:7`; `human/sara/sara/statutes/prolog/section152.pl:3:23`; `human/sara/sara/statutes/prolog/section2.pl:86:9` | TODO |

Owner questions still open: source-unit conversion and rounding; date epoch and interval rules; Household domains and absence/multiplicity; modes and nonground NAF; cut/branch ordering; aggregate order and duplicates; reachable recursion and termination; builtin conversions/errors; and the axiom whitelist. These are pending decisions, not grounds to reinterpret a source clause or change the input population.

Self-review assumptions: ordinary unquoted atom/variable/graphic token boundaries, `%` line comments, nested `/* ... */` comments, escaped/doubled quoted delimiters, balanced brackets, and top-level full stops are used only as lexical conventions. Adjacent `name(...)` supplies a candidate arity. Definition/body boundaries supply candidate dependencies. The only date witness is the exact checked helper source; no semantics are inferred from a variable name. All translation, rounding, epoch, absence, duplicate, control and termination choices remain TODO. New material design flaws must halt the affected lane under the approved protocol; none was established by this lexical inventory.
