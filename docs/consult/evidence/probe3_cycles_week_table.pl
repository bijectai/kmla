:- use_module(library(time)).
:- ['/sara/statutes/prolog/init'].
p(G) :- format("~q  =>  ", [G]), catch((G -> format("true ~q~n",[G]) ; format("FAIL~n",[])), E, (format("EXC ~q~n",[E]))).
% A: clean-DB s151_d for a plain taxpayer
income_(inc1). agent_(inc1,mia). start_(inc1,"2017-06-01"). amount_(inc1,100).
:- p(s151_d(mia,Ea,2017)), p(s151(mia,S2,PL,EL,2017)).
% B: kinship cycle reachable
son_(c1). agent_(c1,jim). patient_(c1,kim). son_(c2). agent_(c2,kim). patient_(c2,jim).
:- p(catch(call_with_time_limit(10, is_descendent_of(lou,jim,_,_)), E, (write(E), nl, fail))).
% C: domestic service in a private home in the usa (string) -> suspected cycle
service_(svc4). agent_(svc4,pat). patient_(svc4,quinn). start_(svc4,"2017-01-01"). end_(svc4,"2017-12-31"). purpose_(svc4,"domestic service"). location_(svc4,"private home"). location_(svc4,"usa").
payment_(pay4). agent_(pay4,quinn). patient_(pay4,pat). start_(pay4,"2017-12-31"). purpose_(pay4,svc4). amount_(pay4,2000). means_(pay4,"cash").
:- p(catch(call_with_time_limit(30, s3306_c_2(svc4,_,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(30, s3306_c(svc4,_,_,_,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(30, s3306_a_3(quinn,_,_,2017)), E, (write(E), nl, fail))).
% D: %W table as computed by the statute helpers (day_to_stamp shift included)
:- open('/probe3/dates.txt',read,In), repeat, read_line_to_string(In,L), (L==end_of_file -> !, close(In) ; day_to_stamp(L,St), format_time(atom(W),"%W",St), format("W ~w ~w~n",[L,W]), fail).
:- halt.
