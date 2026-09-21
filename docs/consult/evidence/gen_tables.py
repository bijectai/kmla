import re,collections,sys
S=sys.argv[1]
def load(k): return [l.rstrip("\n").split("\t") for l in open(f"{S}/sites_{k}.tsv")]
def esc(s): return s.replace("|","\\|")
def key(loc):
    f,l,c=loc.split(":"); return (f,int(l),int(c))
out={}

# ---------------- NAF ----------------
naf_notes={
 "section1.pl:27:5": "N-CONJ. No nonresident-alien event whose agent is Taxp or Spouse and whose effective period [start (default Jan 1), end (default Dec 31)] overlaps the tax year (start ≤ Dec 31 ∧ Jan 1 ≤ end). Both defaults come from the inner N-ABS-DATE disjunctions; overlap test is closed on both ends.",
 "section1.pl:174:5": "N-CONJ. No joint-return event J with agent_(J,Taxp), agent_(J,Spouse), start_(J, Jan 1 Taxy) and end_(J, Dec 31 Taxy). Exact string match on the two dates (equality on Day values), not an interval test.",
 "section151.pl:20:13": "N-CONJ. Negation of the whole joint branch: ¬∃ Spouse (s7703 Taxp Spouse Taxy) with a year-long joint return (same exact-date pattern as section1.pl:174). Spouse ranges over the s7703 solution list.",
 "section151.pl:72:5": "N-CONJ. Same exact joint-return pattern with Taxp and the already-bound Spouse.",
 "section151.pl:169:13": "N-CONJ. Same exact joint-return pattern; the whole (s7703 ∧ ¬joint) condition is the `->` guard for the $1,250 step, committing to the first s7703 spouse.",
 "section152.pl:3:2": "N-MODE. Instantiation guard: succeeds iff at least one of Dependent, Taxp is bound. In Lean this is a mode split: the function is only ever called with Dependent bound or Taxp bound; the both-unbound call made by s152_b_1 inside s152 is translated as the constant empty solution list (see R-152).",
 "section152.pl:144:5": "N-CONJ. Dependent has no spouse (in the s7703 sense) with whom a year-long joint return (exact dates) exists.",
 "section152.pl:207:13": "N-CONJ. No birth_ event whose agent is Dependent. The disjunction repeats `agent_(Someone_is_born,Dependent)` twice (source as written; Taxp is not tested).",
 "section152.pl:347:5": "N-CONJ. No marriage M between Dependent and Taxp with start ≤ Dec 31 Taxy and (end present → end ≥ Jan 1 Taxy ; end absent). The inner `->` commits to the first end_ fact of M.",
 "section2.pl:117:5": "N-CONJ. No nonresident-alien event for Taxp or Spouse whose period overlaps the year: (start absent ∨ start ≤ Dec 31) ∧ (end absent ∨ Jan 1 ≤ end).",
 "section2.pl:155:5": "N-CONJ. \"Not married at close of year\": no marriage M of Taxp with some Spouse ≠ Taxp, start ≤ Dec 31, such that [spouse has a death event and (s2_b_2_C holds for M ∨ death date > Dec 31)] ∨ [spouse has no death event and (end ≥ Jan 1 of Taxy+1 ∨ no end)], and ¬s2_b_2_A(any,any,any,M,Taxy) and ¬s2_b_2_B(Taxp,Spouse,Taxy). Translate the inner structure literally; the two inner NAFs are N-CALL over M and (Taxp,Spouse).",
 "section2.pl:176:17": "N-CONJ. Spouse has no death_ event at all (any date).",
 "section2.pl:259:5": "N-CONJ. Not (Dependent is married under s7703 in Taxy AND Dependent has a year-long joint return with Taxp as the spouse via s152_b_2(Dependent,_,Taxp,Taxy)).",
 "section2.pl:431:5": "N-CONJ. No relationship under s152_d_2 (A)–(G) between Dependent and Taxp whose Start is unbound or ≤ Jan 1 and whose End is unbound or ≤ Dec 31 (note: End ≤ Dec 31, not ≥; source as written). Unbound Start/End arise from kinship events without start_/end_ facts and are Option.none in Lean (D7).",
 "section3306.pl:487:2": "N-CONJ. No unemployment_compensation_agreement_ event with agent_ \"usa\" (string) and agent_ Location. Location is whatever the preceding disjunction bound (possibly unbound → then any agreement with a \"usa\" agent and any second agent satisfies the conjunction).",
 "section3306.pl:504:2": "N-CONJ. Not (s3306_c_1_A(Service,_,Caly) ∧ s3306_c_1_B(Service,_)); c_1_A requires Caly bound (nonvar guard) and c_1_B is itself a NAF.",
 "section3306.pl:575:2": "N-CONJ. Not (service is agricultural by type_ or purpose_ ∧ some employee-citizenship event with patient ≠ \"usa\" ∧ a migration_ event for that Employee with destination_ \"usa\" and purpose_ \"agricultural labor\"). Employee is unbound at the call site (s3306_c_1_B(Service,_)), so it ranges over all citizenship agents.",
 "section63.pl:182:4": "N-CONJ. Same exact year-long joint-return pattern for Taxp and Spouse.",
 "section68.pl:94:5": "N-CONJ. Same exact year-long joint-return pattern for Taxp and Spouse.",
 "section7703.pl:113:2": "N-CONJ. No joint-return event of Taxp (any co-agent) with start_ = Jan 1 and end_ = Dec 31 of Taxy (exact dates).",
 "utils.pl:289:13": "N-CONJ. Negation of the joint-income branch: ¬∃ Spouse from s7703 with a year-long joint return (exact dates).",
 "utils.pl:48:17": "N-CMP. Both operands bound here: ¬(Day ≤ Latest) ⇔ Day > Latest. Together with the first branch this is max over bound entries.",
 "utils.pl:82:17": "N-CMP. ¬(Earliest ≤ Day) ⇔ Day < Earliest. Together with the first branch this is min over bound entries.",
}
def naf_row(loc,pred,ex):
    e=re.sub(r"\s+"," ",ex)
    if loc in naf_notes: return naf_notes[loc]
    m=re.match(r"\\\+ (start_|end_)\((\w+),_\)",e)
    if m: return f"N-ABS-DATE. `{m.group(2)}` has no `{m.group(1)}` fact in the Household. Paired with the sibling branch this yields the candidate list rule (see N2)."
    m=re.match(r"\\\+ (means_|location_|country_)\((\w+),_\)",e)
    if m: return f"N-ABS-ATTR. No `{m.group(1)}` fact whose first argument is `{m.group(2)}` (closed world over the fact list)."
    m=re.match(r"\\\+ plan_\((\w+)\)",e)
    if m: return f"N-ABS-ATTR. `{m.group(1)}` is not the argument of any `plan_` fact."
    m=re.match(r"\\\+ (purpose_|type_)\((\w+),\s*\"([^\"]*)\"\)",e)
    if m: return f"N-ABS-TAG. No `{m.group(1)}` fact for `{m.group(2)}` whose second argument is the *string* \"{m.group(3)}\" (atom values never match, G4)."
    m=re.match(r"\\\+ ([A-Za-z_0-9]+)\((.*)\)$",e)
    if m:
        args=m.group(2)
        return f"N-CALL. `({m.group(1)} …).isEmpty` with the bound arguments substituted; `_`/free positions are existentially quantified (the solution list is computed and tested for emptiness, never enumerated further)."
    return "UNCLASSIFIED — review"
rows=[]
for loc,pred,sym,ex in sorted(load("naf"),key=lambda r:key(r[0])):
    e=re.sub(r"\s+"," ",ex)
    rows.append(f"| `{loc}` | `{pred}` | `{esc(e[:90])}{'…' if len(e)>90 else ''}` | {esc(naf_row(loc,pred,ex))} |")
out["naf"]="| Site | Predicate | Construct | Intended translation |\n| --- | --- | --- | --- |\n"+"\n".join(rows)

# ---------------- IS ----------------
def is_row(loc,pred,e):
    if re.search(r"round\(0\.06\*",e): return "M2/M6. `roundHalfAway (6 * Wages / 100)` exact rational; no ties possible; Int result."
    if re.search(r"round\(.*0\.\d+",e):
        m=re.search(r"round\((?:([\d.]+)\+)?\(?(?:Taxinc(?:-(\d+))?)\)?\*(0\.\d+)\)",e)
        return "M2. Bracket formula: exact rational `c + (Taxinc − k) · r` with c, k, r as the decimal literals shown; result `roundHalfAway`. Float/exact agreement argued in M2; boundary examples in M7."
    if "rdiv 100" in e: return "M3. `roundHalfAway (X / 100)` with exact rational division; X is an Int computed in the preceding `is`."
    if "Amount_A rdiv 2" in e: return "M3. `roundHalfAway (300000 / 2) = 150000` (constant)."
    if "rdiv 2" in e: return "D4. Half-year threshold: never materialised; the comparison site is rewritten as `2·(End − Start) ≥ (Dec31 − Jan1)` in whole days."
    if "rdiv Cost" in e: return "M3. Ratio never materialised; `Ratio ≥ 1/2` is rewritten as `2·Payment_by_individual ≥ Cost` (Cost > 0 already checked)."
    if "ceil(" in e:
        d=re.search(r"/(\d+)",e).group(1); return f"M4. `2 * ((Difference + {int(d)-1}) / {d})` with Nat/Int floor division (Difference ≥ 0 by the preceding max)."
    if re.search(r"Tax(y|y1|y2|y65|y_25)? is|Pyear is|Year1 is",e): return "D5. Int year arithmetic."
    if "Stamp2-Stamp1" in e: return "D4. Duration in seconds = 86400·(day2 − day1); all consumers are rewritten in whole days."
    if "DI+1" in e: return "D2. The +1 day shift inside `day_to_stamp`; cancels in every comparison and duration; matters only for `format_time` (D8)."
    if "7671" in e: return "E1. Unreachable without a type error: `Dob_d` is a two-character string, so `is/2` raises `type_error`. Valid excludes the trigger (V-STR); no Lean arithmetic is defined for this site."
    if re.search(r"Count\d? is \d+|Counts is",e):
        if "600" in e: return "M5. As written: a blind spouse contributes 600 to the *count*, which is then multiplied by the amount (F17). Translate literally."
        return "M5. Int counter arithmetic (0/1 from the `->` guards)."
    return "M5. Int arithmetic: +, −, ·constant, min, max (max(·,0) clamps at zero). No rounding."
rows=[]
for loc,pred,sym,ex in sorted(load("is"),key=lambda r:key(r[0])):
    e=re.sub(r"\s+"," ",ex)
    rows.append(f"| `{loc}` | `{pred}` | `{esc(e)}` | {esc(is_row(loc,pred,e))} |")
out["is"]="| Site | Predicate | Expression | Decision |\n| --- | --- | --- | --- |\n"+"\n".join(rows)

# ---------------- FINDALL ----------------
fa_notes={
 "section151.pl:34:5":"A-SOL. Solution list of `s151_b/4` (spouse exemption): pairs (Spouse, Ea) in SLD order; stipulated s151_b/4 tuples follow the statute solutions (H4).",
 "section151.pl:41:5":"A-SOL. Solution list of `s151_c/4` (dependent exemptions) in SLD order; stipulated tuples (possibly with wildcard Person) follow; wildcard outputs are pairwise distinct for the later `list_to_set` (A3).",
 "section151.pl:48:5":"A-PROJ. First components of List_all_exemptions in order, multiplicity kept.",
 "section151.pl:53:5":"A-PROJ. Second components in order, multiplicity kept; summed by sum_list.",
 "section3301.pl:13:5":"A-SOL. Every solution of `s3306_b` for payer = employer = Employer whose remuneration start lies in [Start_day, End_day]; one entry per *solution*, so a payment provable through k locations/countries or k `means_`/`patient_` alternatives appears k times (F12).",
 "section3301.pl:23:5":"A-PROJ. Individuals in order with multiplicity; deduplicated next by list_to_set (A3).",
 "section3301.pl:29:5":"A-NEST. For each distinct individual (in first-occurrence order), the capped sum of all of that individual's wage entries (inner findall below).",
 "section3301.pl:33:13":"A-PROJ. All wage entries of Individual, in order, multiplicity kept (so duplicates are summed).",
 "section3301.pl:43:5":"A-PROJ. Capped wage per individual in Individual_set order; `member((Individual,Wage),…)` yields exactly one entry per individual because Individuals_x_capped_wages was built from the set.",
 "section3301.pl:52:5":"A-PROJ. Service of every entry (multiplicity kept, so repeated services appear repeatedly); output only.",
 "section3306.pl:28:2":"A-SOL. Amounts of non-agricultural, non-domestic wage solutions for Caly followed by those for Caly−1 (disjunction order); multiplicity per solution.",
 "section3306.pl:54:2":"A-SOL. Triples (Stamp, Day, Individual) for every day-of-employment solution with Jan 1 of Caly−1 ≤ Day ≤ Dec 31 of Caly. From base facts this list is always empty (F4): the statute never binds Workday; only stipulated `s3306_c/5` tuples supply days.",
 "section3306.pl:64:5":"A-PROJ. Stamps in order; deduplicated next by list_to_set (distinct days).",
 "section3306.pl:72:5":"A-DAYS. `%W` week label (D8) of every stamp in Emp_days (with multiplicity, deduplicated next). The label carries no year, so equal week numbers of Caly−1 and Caly collapse.",
 "section3306.pl:83:5":"A-PROJ. Days in order (output only).",
 "section3306.pl:88:5":"A-PROJ. Individuals in order (output only).",
 "section3306.pl:114:2":"A-SOL. (Amount, Service) of agricultural wage solutions for Caly then Caly−1; multiplicity per solution.",
 "section3306.pl:125:5":"A-PROJ. Amounts in order, multiplicity kept, summed.",
 "section3306.pl:130:5":"A-PROJ. Services in order (output only).",
 "section3306.pl:140:2":"A-SOL. (Employee, Service) for every agricultural `s3306_c` solution on Day; from base facts this requires a bound Day and is empty when reached with Day unbound (F4).",
 "section3306.pl:151:5":"A-PROJ. Employees in order; deduplicated next by list_to_set.",
 "section3306.pl:156:5":"A-PROJ. Services in order (output only).",
 "section3306.pl:169:2":"A-SOL. Day-level tuples; the leading `s3306_c(_,Employer,_,Day,_)` yields Day only from stipulated tuples (F4); the following `is_before` calls fail on an unbound Day, so base facts contribute nothing.",
 "section3306.pl:180:5":"A-PROJ. Stamps; deduplicated next.",
 "section3306.pl:188:5":"A-DAYS. `%W` labels (D8) with multiplicity; deduplicated next.",
 "section3306.pl:199:5":"A-PROJ. Output only.",
 "section3306.pl:204:5":"A-PROJ. Output only.",
 "section3306.pl:209:5":"A-PROJ. Days; deduplicated next by list_to_set.",
 "section3306.pl:237:2":"A-SOL. (Amount, Service) of domestic-service cash wage solutions for Caly then Caly−1; multiplicity per solution; reaching `s3306_b` here is where the E4 cycle starts when the service is a USA private-home domestic service.",
 "section3306.pl:248:5":"A-PROJ. Amounts in order, summed.",
 "section3306.pl:253:5":"A-PROJ. Services (output only).",
 "section3306.pl:524:5":"A-EV. (Amount, Employee, Service) for every payment by Employer to an employee for an agricultural service, dated in [Jan 1 Caly−1, Dec 31 Caly], paid in cash or with no means_ fact; one entry per fact-combination (a payment with two `purpose_` links or two `amount_` facts appears twice).",
 "section3306.pl:551:5":"A-PROJ. Amounts in order, summed.",
 "section3306.pl:558:5":"A-PROJ. Output only.",
 "section3306.pl:563:5":"A-PROJ. Output only.",
 "section63.pl:274:2":"A-EV. (Amount, Deduction) for every deduction_ event with agent Taxp, an amount_ fact and a start_ in [Jan 1, Dec 31] of Taxy; one entry per (amount_ fact × start_ fact) combination.",
 "section63.pl:286:2":"A-PROJ. Amounts in order, summed; `length > 0` requires at least one entry (an empty itemised list makes s63_d fail, so s63_b applies).",
 "section63.pl:294:2":"A-PROJ. Deduction ids in order (output; observed as a list, order and multiplicity kept).",
 "section7703.pl:143:5":"A-EV. Amounts of payments by Taxp whose purpose is a residence event at Household or the Household itself, and whose start_ date has year == Taxy; one entry per (residence_ × purpose_ × amount_ × start_) combination, so a household with r residence events at the same place multiplies each payment r times in *both* sums (ratio unaffected, Cost > 0 unaffected).",
 "section7703.pl:162:2":"A-EV. Same as the previous site without the agent restriction (all payers).",
 "section7703.pl:205:5":"A-DAYS. The 184 window days (D8: Jul 1 … Dec 31 under the pinned TZ) on which the spouse's residence at Household is ongoing (start ≤ day ∧ (end absent ∨ day ≤ end)); one entry per (day × residence event) solution; only the emptiness of the list is used.",
 "utils.pl:304:5":"A-EV. Amounts of income_ events of Person with start_ in [Jan 1, Dec 31]; one entry per (amount_ × start_) fact combination (duplicate facts double-count, F13).",
 "utils.pl:316:5":"A-EV. Amounts of payment_ events with patient Person and start_ in the year; same multiplicity rule.",
}
rows=[]
for loc,pred,sym,ex in sorted(load("findall"),key=lambda r:key(r[0])):
    e=re.sub(r"\s+"," ",ex)
    rows.append(f"| `{loc}` | `{pred}` | `{esc(e[:80])}…` | {esc(fa_notes.get(loc,'REVIEW'))} |")
out["findall"]="| Site | Predicate | Construct | Duplicate and order decision |\n| --- | --- | --- | --- |\n"+"\n".join(rows)
rows=[]
for loc,pred,sym,ex in sorted(load("sum_list"),key=lambda r:key(r[0])):
    rows.append(f"| `{loc}` | `{pred}` | `{esc(ex.strip())}` | A2. Int fold over the list as produced by the preceding findall (order irrelevant to the sum, multiplicity counted); empty list sums to 0. |")
out["sum_list"]="| Site | Predicate | Construct | Decision |\n| --- | --- | --- | --- |\n"+"\n".join(rows)

# ---------------- CMP (date) ----------------
cmp=load("cmp")
date_syms={"is_before","earliest","latest"}
rows=[]
for loc,pred,sym,ex in sorted(cmp,key=lambda r:key(r[0])):
    if sym in date_syms or (sym in (">=","=<") and re.search(r"Duration|Age_individual|Time_since_birth",ex)) or sym=="@>":
        e=re.sub(r"\s+"," ",ex)
        rows.append(f"| `{loc}` | `{pred}` | `{sym}` | `{esc(e[:70])}` |")
out["datecmp"]="| Site | Predicate | Symbol | Construct |\n| --- | --- | --- | --- |\n"+"\n".join(rows)
print({k:len(v.splitlines()) for k,v in out.items()})
for k,v in out.items():
    open(f"{S}/frag/{k}.md","w").write(v+"\n")
