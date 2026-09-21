% Diagnostic against A-009's proposed V10, not a new input-domain decision.
% No birth day is shared between distinct persons: a has 2000 and 2002,
% b has 2001. G1/H1 preserve all these facts; current H5 has no uniqueness rule.
:- consult('/corpus/statutes/prolog/init.pl').
:- dynamic brother_/1.

birth_(birth_a0).
birth_(birth_b1).
birth_(birth_a2).
agent_(birth_a0,a).
agent_(birth_b1,b).
agent_(birth_a2,a).
start_(birth_a0,"2000-01-01").
start_(birth_b1,"2001-01-01").
start_(birth_a2,"2002-01-01").

marriage_(marriage_a).
marriage_(marriage_b).
agent_(marriage_a,a).
agent_(marriage_a,sa).
agent_(marriage_b,b).
agent_(marriage_b,sb).
start_(marriage_a,"2017-01-01").
start_(marriage_b,"2017-01-01").

residence_(residence_a).
residence_(residence_b).
agent_(residence_a,a).
agent_(residence_b,b).
patient_(residence_a,home).
patient_(residence_b,home).
start_(residence_a,"2018-01-01").
start_(residence_b,"2018-01-01").

brother_(sibling_ab).
agent_(sibling_ab,a).
patient_(sibling_ab,b).
