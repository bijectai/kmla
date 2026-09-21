:- ['/sara/statutes/prolog/init'].
p(G) :- format("~q  =>  ", [G]), catch((G -> format("true ~q~n",[G]) ; format("FAIL~n",[])), E, (format("EXC ~q~n",[E]))).
pn(G) :- format("~q  =>  ", [G]), catch((findall(G,G,L), length(L,N), format("~w solutions ~q~n",[N,L])), E, (format("EXC ~q~n",[E]))).
% Q1: s2_b_3_A with NRA start and end inside the year
nonresident_alien_(nra1). agent_(nra1,alice). start_(nra1,"2017-03-01"). end_(nra1,"2017-06-30").
nonresident_alien_(nra2). agent_(nra2,bob). start_(nra2,"2017-03-01").
nonresident_alien_(nra3). agent_(nra3,carol). end_(nra3,"2017-06-30").
:- p(s2_b_3_A(alice,2017,_)), p(s2_b_3_A(bob,2017,_)), p(s2_b_3_A(carol,2017,_)).
% Q2: s3306_c solution multiplicity with several location_ and country_ facts
service_(svc1). agent_(svc1,dan). patient_(svc1,erin). start_(svc1,"2017-01-01"). end_(svc1,"2017-12-31").
location_(svc1,"baltimore"). location_(svc1,"maryland"). location_(svc1,"usa").
country_("baltimore","usa"). country_("maryland","usa").
payment_(pay1). agent_(pay1,erin). patient_(pay1,dan). start_(pay1,"2017-12-31"). purpose_(pay1,svc1). amount_(pay1,5000).
:- pn(s3306_c(svc1,E,I,W,2017)), pn(s3306_c_A(svc1,E,I)), pn(s3306_b(W,pay1,S,Pa,Pe,Er,Em,M)).
:- pn(total_wages_employer(erin,T,I,S,"2017-01-01","2017-12-31")).
% Q3: atom location usa vs string
service_(svc2). agent_(svc2,fay). patient_(svc2,gus). start_(svc2,"2017-01-01"). end_(svc2,"2017-12-31"). location_(svc2,usa).
:- pn(s3306_c_A(svc2,E,I)), pn(s3306_c(svc2,E,I,W,2017)).
% Q4: s152 with unbound year for a dependent payee (plan payment)
son_(hal_son). agent_(hal_son,hal). patient_(hal_son,ian). start_(hal_son,"2000-01-01").
:- p(s152(hal,ian,_)).
% Q5: kinship cycle
son_(c1). agent_(c1,jim). patient_(c1,kim). son_(c2). agent_(c2,kim). patient_(c2,jim).
:- p(catch(call_with_time_limit(5, is_descendent_of(jim,lou,_,_)), E, (write(E), nl, fail))).
% Q6: duplicate amount facts summed twice
income_(inc1). agent_(inc1,mia). start_(inc1,"2017-06-01"). amount_(inc1,100). amount_(inc1,100).
:- p(gross_income(mia,2017,G)).
% Q7: date-related helper outputs
:- p(latest(["2017-01-01",_,"2016-05-05"],L1)), p(latest([_,_],L2)), p(earliest(["2017-01-01","2017-01-01"],L3)), p(is_before("2017-01-01","2017-01-01")), p(is_before(_, "2017-01-01")), p(duration("2017-01-01","2017-12-31",D1)), p(duration("2016-01-01","2016-12-31",D2)).
:- p(is_before("2017-1-1","2017-01-02")), p(is_before("2017-02-30","2017-03-01")), p(is_before("2017-02-30","2017-03-02")), p(day_to_stamp("2017-02-30",St)).
% Q8: s7703_b_3 day list
:- p((findall(Day,(between(2,185,Off),date_time_stamp(date(2017,7,Off,0,0,0,0,-,-),Stmp),format_time(atom(Day),"%Y-%m-%d",Stmp)),Ds), Ds=[F|_], last(Ds,La), length(Ds,N), format("first ~w last ~w n ~w~n",[F,La,N]))).
% Q9: undefined-but-declared predicate call
:- p(itemize_deductions_(_)), p(unemployment_compensation_agreement_(_)).
% Q10: s151_d_3_A cut behaviour: taxpayer with two possible s68_b results
:- p(s151_d(mia,Ea,2017)).
% Q11: s3306_c_5_B exception
service_(svc3). agent_(svc3,ned). patient_(svc3,olga). start_(svc3,"2017-01-01"). end_(svc3,"2017-12-31").
son_(ned_son). agent_(ned_son,ned). patient_(ned_son,olga). birth_(ned_b). agent_(ned_b,ned). start_(ned_b,"2005-03-15").
:- p(s3306_c_5(svc3,olga,ned,"2017-05-05")), p(s3306_c(svc3,olga,ned,"2017-05-05",2017)).
% Q12: domestic service recursion
service_(svc4). agent_(svc4,pat). patient_(svc4,quinn). start_(svc4,"2017-01-01"). end_(svc4,"2017-12-31"). purpose_(svc4,"domestic service"). location_(svc4,"private home").
payment_(pay4). agent_(pay4,quinn). patient_(pay4,pat). start_(pay4,"2017-12-31"). purpose_(pay4,svc4). amount_(pay4,2000). means_(pay4,"cash").
:- p(catch(call_with_time_limit(20, s3306_c_2(svc4,_,2017)), E, (write(E), nl, fail))).
:- p(catch(call_with_time_limit(20, s3306_a_3(quinn,_,_,2017)), E, (write(E), nl, fail))).
:- halt.
