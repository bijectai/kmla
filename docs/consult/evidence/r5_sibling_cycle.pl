% Diagnostic input for R5; not an original case or a proposed domain revision.
% The original statute files are loaded from the read-only /corpus mount.
:- consult('/corpus/statutes/prolog/init.pl').
% Dynamic only to permit the explicitly reported no-sibling diagnostic control.
:- dynamic brother_/1.

birth_(birth_a).
birth_(birth_b).
agent_(birth_a,a).
agent_(birth_b,b).
start_(birth_a,"2000-01-01").
start_(birth_b,"2000-01-01").

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
