# H4.2 bound-purpose exception — unapproved draft

Status: **DRAFT ONLY. Not installed, not implemented, not reviewed by Fable.**
Q-020's external review was blocked by the permission reviewer. Dev has not
accepted this proposal. H4.2/H4.3 remain operative as installed in human/.

## Finding that precedes this proposal

The exact original goal is
`findall(Purpose,purpose_(payment_2015_1,Purpose),Purposes)`.
`Payment_event` is the ground atom `payment_2015_1`, not a free variable.
The first split succeeds: `Xp="payment"`, `Yp="2015"`, `Zp="1"`.
The SECOND call, `split_string(Service_event,"_","",[Xs,Ys,Zs])`, has
`Service_event`, `Xs`, `Ys`, `Zs` free and raises:

```text
ERROR: split_string/4: Arguments are not sufficiently instantiated
```

The fresh pinned execution first reproduces the original goal unchanged, then
retrieves the original clause and exposes its conjunction calls in order.
It does not rewrite the clause or implement a grounder. Raw output, exact
argv, exit 2/no timeout and complete measured runtime identity are under
`docs/consult/evidence/h4-bound-goal-2026-09-23/`. Its diagnostic source is
`docs/consult/evidence/h4_bound_goal_bindings.pl`. The protected original is
tax_case_33.pl:29–31, SHA-256
`5c04303da3dfdf96c412994cb0aaa3ce01c5d248d9de01ed4726456ea523ffa0`.

## Proposed appended H4.2 text

For the single `purpose_/2` rule at lines 29–31 of the pinned original
`tax_case_33.pl`, step (ii) binds both inputs. Keep the first-position event
traversal from step (ii). For each such event, traverse the ground `service_/1`
terms obtained in step (i), once per distinct tagged term in first-occurrence
order, and execute the original `purpose_(Event,Service)` with both arguments
bound. Append every successful proof of that call in interpreter order; never
deduplicate its proof results. This second-input domain traversal is scoped
to that exact original rule, not a replacement for other purpose clauses.
Bodyless wildcard facts retain H2/A3 patterns and shared variable identity;
no wildcard is expanded by this exception. All other H4.2 steps and H4.3(a,b)
stay unchanged. A raise, nontermination or failed H4.3 check remains a finding,
never an empty result, skipped original, broader candidate domain or source
repair. Report both H4.3 checks for every one of the 376 originals before
claiming round-trip completion.

## What approval would and would not settle

This explicitly proposes the second-input domain and its traversal order;
neither is silently treated as already signed. Domain deduplication applies
only to that proposed input enumeration, not fact lists or proof results.
Approval would permit implementing and testing this candidate. It would not
certify its preservation, authorize a fallback on failure, exclude an original,
change comparison/canonicalization, or pass Checkpoint 1.

The existing numeric audit found 157 payment solutions, 157 service solutions
and 157 successful pairs on their declared product. A ground pair outside
both sets also succeeds. Thus this draft does NOT claim global extensional
completeness. The required criterion remains exactly H4.3, not a stronger
replacement. Neither H4.3 check nor the full event-by-service traversal cost
has been measured for this candidate. Those are open verification obligations.
No claim that all other cases work follows from this exception.

## Self-review

The measured assumption is that the first split accepts its bound atom on
SWI-Prolog 7.2.3+dfsg-6, while the second rejects its free input. The proposal's
unproved assumption is that the declared service terms suffice for this case's
H4.3 observations; that must be tested, not inferred from the 157-pair count.
Three failed edit cycles on one test means stop and report. No candidate
grounder edit/test cycle has begun and no protected file has been touched.
