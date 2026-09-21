:- use_module(library(time)).
:- ['/sara/statutes/prolog/init'].
p(G) :- format("~q  =>  ", [G]), catch((G -> format("true ~q~n",[G]) ; format("FAIL~n",[])), E, (format("EXC ~q~n",[E]))).
pn(G) :- format("~q  =>  ", [G]), catch((findall(G,G,L), length(L,N), format("~w solutions ~q~n",[N,L])), E, (format("EXC ~q~n",[E]))).
% A: unmarried taxpayer supporting a parent in own home, 2017 (suspected s151_d <-> s2_b_1_B cycle)
income_(inc1). agent_(inc1,mia). start_(inc1,"2017-06-01"). amount_(inc1,50000).
father_(f1). agent_(f1,pa). patient_(f1,mia). start_(f1,"1980-01-01").
residence_(r1). agent_(r1,mia). patient_(r1,home). start_(r1,"2010-01-01").
residence_(r2). agent_(r2,pa). patient_(r2,home). start_(r2,"2010-01-01").
payment_(pay1). agent_(pay1,mia). purpose_(pay1,home). amount_(pay1,1000). start_(pay1,"2017-05-05").
:- p(catch(call_with_time_limit(60, s151_d(mia,Ea,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(60, s2_b(mia,D,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(60, s151_d(mia,Ea,2019)), E, (write(E), nl, fail))).
% B: s68_b_1_A with an unrelated surviving spouse in the household
marriage_(m1). agent_(m1,sue). agent_(m1,tom). start_(m1,"2000-01-01").
death_(d1). agent_(d1,tom). start_(d1,"2016-03-03").
residence_(r3). agent_(r3,sue). patient_(r3,sue_home). start_(r3,"2000-01-01").
son_(s1). agent_(s1,kid). patient_(s1,sue). start_(s1,"2005-01-01").
residence_(r4). agent_(r4,kid). patient_(r4,sue_home). start_(r4,"2005-01-01").
payment_(pay2). agent_(pay2,sue). purpose_(pay2,sue_home). amount_(pay2,1000). start_(pay2,"2017-05-05").
:- pn(s2_a(sue,S,2017)).
income_(inc2). agent_(inc2,zed). start_(inc2,"2017-06-01"). amount_(inc2,50000).
:- pn(s68_b(zed,Aa,2017)).
% C: s3306_a_1_B from base facts only (does the statute ever bind Workday?)
service_(svc9). agent_(svc9,wk). patient_(svc9,boss). start_(svc9,"2017-01-01"). end_(svc9,"2017-12-31").
payment_(pay9). agent_(pay9,boss). patient_(pay9,wk). start_(pay9,"2017-12-31"). purpose_(pay9,svc9). amount_(pay9,9000).
:- pn(s3306_c(svc9,E,I,W,2017)), pn(s3306_a_1_B(boss,WD,EE,2017)), pn(s3306_a_1_A(boss,2017,Wg)), pn(s3301(boss,2017,Wg2,EE2,EM2,T2)).
% D: s7703_b_3 day window under the process TZ, and %W under the process TZ
:- findall(Day,(between(2,185,Off),date_time_stamp(date(2017,7,Off,0,0,0,0,-,-),Stmp),format_time(atom(Day),"%Y-%m-%d",Stmp)),Ds), Ds=[F|_], last(Ds,La), length(Ds,N), format("b3window first ~w last ~w n ~w~n",[F,La,N]).
:- forall(member(D,["2017-01-01","2017-01-02","2017-01-07","2017-01-08","2017-12-31","2018-01-01","2016-12-31","2017-03-12","2017-11-05"]), (day_to_stamp(D,St), format_time(atom(W),"%W",St), format_time(atom(Dy),"%Y-%m-%d",St), format("W ~w -> localday ~w week ~w~n",[D,Dy,W]))).
:- halt.
