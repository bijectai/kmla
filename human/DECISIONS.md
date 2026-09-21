# Semantic decisions

Status: TODO — human decisions and source inventory pending.
This template contains no approved translations. Hazard listings cannot be
populated until the designated SARA source is available.

## Money

TODO: representation, units, rounding rule, and worked examples.
The build plan calls for integer cents; record the approved details here.

## Dates

TODO: epoch, day-count representation, and interval semantics per predicate.
TODO: source locations and decisions for each date comparison.

## Household

TODO: the shared type and field list derived from the source fact predicates.
TODO: review and approve the eventual `Interface/Household.lean` draft.

## NAF

TODO: list every `\+` with its source file, line, and intended translation.

## Cut

TODO: list every `!` with its source file, line, and intended ordering.

## Aggregates

TODO: list every `findall` and `sumlist` with source file and line.
TODO: specify duplicate and order semantics for each occurrence.

## Recursion

TODO: list recursive predicates and the termination strategy for each.

## Axioms

TODO: confirm the build plan's whitelist: `propext`, `Quot.sound`,
and `Classical.choice`.

## Source hazard inventory

TODO: populate after the designated corpus is supplied, covering every `\+`,
`!`, `findall`, `sumlist`, `is`, and date comparison in `sara/statutes/`.
Record source file and line, link to the corresponding decision, and add explicit
arithmetic decisions for `is`. An empty inventory does not mean no hazards exist.
