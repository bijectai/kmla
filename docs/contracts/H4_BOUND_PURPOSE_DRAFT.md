# H4.2 bound-purpose exception — reviewed candidate

Status: **CANDIDATE ONLY. Reviewed in A-020; implemented and measured for
tax_case_33; all-376 verification incomplete. Not installed or certified.**
On 2026-09-23 Dev approved this exact candidate for Fable review, then
implementation and verification if Fable endorses it as explicit. A missing
choice or counterexample must go to Dev before implementation. The prior
consultation permission block is cleared by explicit owner authorization.
The proposed text below incorporates A-020 §3's four clarifications without
changing the domain, order or preservation criterion. Only Dev installs
human/DECISIONS.md and re-pins; candidate approval is not installed text or
round-trip/CP1 acceptance.

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
`tax_case_33.pl`, the two-input call replaces, rather than supplements, the
single-input call of step (ii) for this predicate in this file. The raising
single-input call is not made and the predicate is not traversed twice.
Keep the first-position event traversal from step (ii), without deduplicating
it: repeated unary declarations retain repeated outer iterations. Step (i)
retains each unary predicate's provenance, not only a merged event universe.
For each such event, traverse the ground `service_/1`
terms obtained in step (i), once per distinct tagged term in first-occurrence
order, and execute the original `purpose_(Event,Service)` with both arguments
bound. Append every successful proof of that call in interpreter order; never
deduplicate its proof results. Only the inner candidate domain is deduplicated;
neither the outer traversal nor successful proofs are deduplicated.
This second-input domain traversal is scoped
to that exact original rule, not a replacement for other purpose clauses.
Bodyless wildcard facts retain H2/A3 patterns and shared variable identity;
no wildcard is expanded by this exception. All other H4.2 steps and H4.3(a,b)
stay unchanged. A raise, nontermination or failed H4.3 check remains a finding,
never an empty result, skipped original, broader candidate domain or source
repair. Recognize the exception by the pinned file digest above and the unique
matching `purpose_/2` clause; require exactly one match and halt on a mismatch,
rather than widening the exception. Report both H4.3 checks for every one of
the 376 originals before claiming round-trip completion.

## What approval would and would not settle

This explicitly proposes the second-input domain and its traversal order;
neither is silently treated as installed signed text. Domain deduplication applies
only to that proposed input enumeration, not fact lists or proof results.
Dev's conditional authorization and A-020's endorsement permit implementing and
testing this candidate. They do not
certify its preservation, authorize a fallback on failure, exclude an original,
change comparison/canonicalization, or pass Checkpoint 1.

The existing numeric audit found 157 payment solutions, 157 service solutions
and 157 successful pairs on their declared product. A ground pair outside
both sets also succeeds. Thus this draft does NOT claim global extensional
completeness. The required criterion remains exactly H4.3, not a stronger
replacement. Both H4.3 checks now pass for tax_case_33: 1,736 ordered facts and
the tax/3 first result 27181 are preserved. The measured traversal has 316 outer
event proofs and 157 distinct inner service terms, making 49,612 two-input
calls and retaining 157 successes. Whole grounding (not purpose-only) wall time
was 0.052663 seconds in the retained run-2 measurement. Full evidence and timing
scope are in docs/phase1/H4_CANDIDATE_REPORT_2026-09-23.md.

All-376 completion is still open: the generic binary path loses a supplied
country_/2 fact, with a measured H4.3(b) mismatch in s3306_c_A_pos. That path is
halted for Q-021 review; permission to send its new payload is required. No
revised traversal is implemented and no claim that other cases work follows
from the narrow candidate's success.

## Self-review

The measured assumption is that the first split accepts its bound atom on
SWI-Prolog 7.2.3+dfsg-6, while the second rejects its free input. The proposal's
preservation obligation was tested on this case's actual H4.3 observations,
not inferred from the 157-pair count. It is not global completeness. Three
failed edit cycles on one test means stop and report. The separate static-loader
defect had one failed measurement and one corrective edit before passing; the
country mismatch remains failing with no remedy attempt. No breaker threshold
was reached and no protected file has been touched.
