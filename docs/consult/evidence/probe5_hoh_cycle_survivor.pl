:- use_module(library(time)).
:- ['/sara/statutes/prolog/init'].
p(G) :- format("~q  =>  ", [G]), catch((G -> format("true ~q~n",[G]) ; format("FAIL~n",[])), E, (format("EXC ~q~n",[E]))).
pn(G) :- format("~q  =>  ", [G]), catch((findall(G,G,L), length(L,N), format("~w solutions ~q~n",[N,L])), E, (format("EXC ~q~n",[E]))).
% A: unmarried taxpayer (no own residence fact) supporting a parent living in the taxpayer's house, 2017
income_(inc1). agent_(inc1,mia). start_(inc1,"2017-06-01"). amount_(inc1,50000).
father_(f1). agent_(f1,pa). patient_(f1,mia). start_(f1,"1980-01-01").
residence_(r2). agent_(r2,pa). patient_(r2,home). start_(r2,"2010-01-01").
payment_(pay1). agent_(pay1,mia). purpose_(pay1,home). amount_(pay1,1000). start_(pay1,"2017-05-05").
:- p(catch(call_with_time_limit(90, s2_b_1_B(mia,H,D,Ded,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(90, s151_d(mia,Ea,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(90, s151(mia,S,PL,EL,2017)), E, (write(E), nl, fail))).
% B: s68_b_1_A applies to an unrelated taxpayer when anyone is a surviving spouse
marriage_(m1). agent_(m1,sue). agent_(m1,tom). start_(m1,"2000-01-01").
death_(d1). agent_(d1,tom). start_(d1,"2016-03-03").
income_(inc3). agent_(inc3,sue). start_(inc3,"2017-06-01"). amount_(inc3,40000).
residence_(r3). agent_(r3,sue). patient_(r3,sue_home). start_(r3,"2000-01-01").
son_(s1). agent_(s1,kid). patient_(s1,sue). start_(s1,"2005-01-01").
residence_(r4). agent_(r4,kid). patient_(r4,sue_home). start_(r4,"2005-01-01").
payment_(pay2). agent_(pay2,sue). purpose_(pay2,sue_home). amount_(pay2,1000). start_(pay2,"2017-05-05").
income_(inc2). agent_(inc2,zed). start_(inc2,"2017-06-01"). amount_(inc2,50000).
:- pn(s2_a(sue,S,2017)), pn(s68_b(zed,Aa,2017)), pn(s68_b_1_A(zed,J,SS,Aa2,2017)).
:- halt.
