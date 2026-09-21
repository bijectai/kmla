p(G) :- format("~q  =>  ", [G]), catch((G -> format("true ~q~n",[G]) ; format("FAIL~n",[])), E, (print_message_lines(user_output,'',[]), format("EXC ~q~n",[E]))).
:- p(X1 is 31536000.0 rdiv 2).
:- p(X2 is 31536001.5 rdiv 2).
:- p(X3 is 3 rdiv 2).
:- p(X4 is round(2.5)), p(X5 is round(-2.5)), p(X6 is round(3.5)), p(X7 is round(0.5)).
:- p(X8 is round(3 rdiv 2)), p(X9 is round(-3 rdiv 2)), p(X10 is round(1 rdiv 2)), p(X11 is round(5 rdiv 2)).
:- p(X12 is round(10*0.15)), p(X13 is round(50*0.31)), p(X14 is round(125*0.396)), p(X15 is round(36900*0.15)).
:- p(X16 is round(75528.50+(250125-250000)*0.396)), p(X17 is round(35928.50+(140050-140000)*0.36)).
:- p(X18 is 2500/1250), p(X19 is 2501/1250), p(X20 is ceil(2501/1250)), p(X21 is ceil(0/1250)), p(X22 is ceil(2500/1250)).
:- p(X23 is round((2000*34) rdiv 100)), p(X24 is round((2000*33) rdiv 100)), p(X25 is round(2000*35 rdiv 100)), p(X26 is round(1 rdiv 2)), p(X27 is round(300000 rdiv 2)), p(X28 is round(300001 rdiv 2)).
:- p((R is 1 rdiv 2, R >= rational(0.5))), p((R2 is 1 rdiv 3, R2 >= rational(0.5))), p(Q is rational(0.5)).
:- p(date_time_stamp(date(2015,1,1,0,0,0,0,-,-),S1)), p(date_time_stamp(date(2015,1,32,0,0,0,0,-,-),S2)), p((date_time_stamp(date(2015,1,32,0,0,0,0,-,-),S3), format_time(atom(D3),"%Y-%m-%d",S3))).
:- p((date_time_stamp(date(2017,7,185,0,0,0,0,-,-),S4), format_time(atom(D4),"%Y-%m-%d",S4))), p((date_time_stamp(date(2017,7,2,0,0,0,0,-,-),S5), format_time(atom(D5),"%Y-%m-%d",S5))).
:- p(Y1 is "15"+7671), p(Y2 is "5"+7671), p(date_time_stamp(date("1990","05",22,0,0,0,0,-,-),S6)), p(date_time_stamp(date(1990,5,"22",0,0,0,0,-,-),S7)).
:- p(("usa"==usa)), p(("usa"=="usa")), p((usa==usa)), p((abc \== "abc")), p((X==Y)), p((_ \== "usa")).
:- p(atom_prefix("state of maryland","state of ")), p(atom_prefix('state of maryland',"state of ")), p(atom_prefix(state_of_md,"state of ")).
:- p((sub_atom("canadian government",_,11,0,Suf), Suf==' government')), p((sub_atom('canadian government',_,11,0,Suf2), Suf2==' government')).
:- p(list_to_set([(A,2000),(B,2000)],LS1)), p(list_to_set([(1,2),(1,2),(2,1)],LS2)), p(list_to_set([(A2,1),(A2,1)],LS3)), p(list_to_set([1.0,1],LS4)).
:- p((date_time_stamp(date(2017,1,1,0,0,0,0,-,-),W1), format_time(atom(WK1),"%W",W1))), p((date_time_stamp(date(2017,1,2,0,0,0,0,-,-),W2), format_time(atom(WK2),"%W",W2))), p((date_time_stamp(date(2017,12,31,0,0,0,0,-,-),W3), format_time(atom(WK3),"%W",W3))), p((date_time_stamp(date(2018,1,1,0,0,0,0,-,-),W4), format_time(atom(WK4),"%W",W4))).
:- p((split_string("2017-02-01","-","",Parts), Parts=[Ys,_,_], atom_number(Ys,Yn))), p((2017 == 2017)), p((split_string("2017-02-01","-","",[Ys2,_,_]), Ys2 == "2017")), p(("2018" @> "2017")), p(("2018" @> 2017)), p(("2017" @> "2017")).
:- p(sum_list([],Z0)), p(sum_list([1,2.0],Z1)), p((length([],L0), L0>0)), p((between(2018,2025,2020))), p(between(2018,2025,2017)).
:- p(X30 is max(3,2.0)), p(X31 is min(7000,7000.0)), p(X32 is round(0.06*33200)), p(X33 is 0.06*33200), p(X34 is round(0.06*7000)), p(X35 is round(0.06*1250)), p(X36 is 0.06*1250), p(X37 is round(0.06*2250)).
:- p((X40 = 5, X40 == 5)), p((X41 is 5.0, X41 == 5)), p((5.0 =:= 5)), p((X42 is 33200 - 12000 - 0)), p(( 1.5 >= 1 rdiv 2)), p((15724800.0 >= 15768000 rdiv 1)).
:- p(day_test) .
:- halt.
