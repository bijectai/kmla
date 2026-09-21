% Compare SWI float rounding (as written in the statutes) with exact rational rounding, over ranges.
% Each formula: name, base constant C (dollars, as float literal in source), threshold K, rate R (float literal), exact numerator/denominator of R.
f(a_i,   0,      0,      0.15, 3,20).
f(a_ii,  5535,   36900,  0.28, 7,25).
f(a_iii, 20165,  89150,  0.31, 31,100).
f(a_iv,  35928.50, 140000, 0.36, 9,25).
f(a_v,   75528.50, 250000, 0.396, 99,250).
f(b_ii,  4440,   29600,  0.28, 7,25).
f(b_iii, 17544,  76400,  0.31, 31,100).
f(b_iv,  33385,  127500, 0.36, 9,25).
f(b_v,   77485,  250000, 0.396, 99,250).
f(c_ii,  3315,   22100,  0.28, 7,25).
f(c_iii, 12107,  53500,  0.31, 31,100).
f(c_iv,  31172,  115000, 0.36, 9,25).
f(c_v,   79772,  250000, 0.396, 99,250).
f(d_ii,  2767.50, 18450, 0.28, 7,25).
f(d_iii, 10082.50, 44575, 0.31, 31,100).
f(d_iv,  17964.25, 70000, 0.36, 9,25).
f(d_v,   37764.25, 125000, 0.396, 99,250).
f(s3301, 0,      0,      0.06, 3,50).
exact_c(C, Cn, Cd) :- ( integer(C) -> Cn = C, Cd = 1 ; Cn is round(C*100), Cd = 100 ).
check(Name, X, Ok) :-
    f(Name, C, K, R, P, Q),
    Tf is round(C + (X - K) * R),
    exact_c(C, Cn, Cd),
    Te is round((Cn rdiv Cd) + ((X - K) * P) rdiv Q),
    ( Tf =:= Te -> Ok = ok ; Ok = mismatch(Name, X, Tf, Te) ).
run_range(Name, Lo, Hi) :-
    forall(between(Lo, Hi, X), (check(Name, X, Ok), (Ok == ok -> true ; format("~w~n", [Ok])))).
run_ties(Name, M, Off, Count) :-   % X = Off + M*j, j in 1..Count (exact tie residues)
    forall(between(1, Count, J), (X is Off + M*J, check(Name, X, Ok), (Ok == ok -> true ; format("~w~n", [Ok])))).
:- forall(f(Name,_,_,_,_,_), (run_range(Name, 0, 400000), format("range done ~w~n",[Name]))).
% exact-tie residues: 0.15: x=10(2m+1) ; 0.31: x=100m+50 ; 0.396: x=250m+125 ; 0.06: x=50m+25 (all relative to X-K)
:- run_ties(a_i, 20, 10, 200000), run_ties(s3301, 50, 25, 200000),
   run_ties(a_iii, 100, 89200, 200000), run_ties(b_iii, 100, 76450, 200000), run_ties(c_iii, 100, 53550, 200000), run_ties(d_iii, 100, 44625, 200000),
   run_ties(a_v, 250, 250125, 200000), run_ties(b_v, 250, 250125, 200000), run_ties(c_v, 250, 250125, 200000), run_ties(d_v, 250, 125125, 200000),
   format("ties done~n").
% large random samples up to 10^9
:- forall(f(Name,_,_,_,_,_), forall(between(1,20000,_), (X is random(1000000000), check(Name,X,Ok), (Ok==ok -> true ; format("~w~n",[Ok]))))), format("random done~n").
% ceil(D/1250) and ceil(D/2500) vs integer ceiling
cc(D, N) :- A is ceil(D/N), B is (D + N - 1) // N, (A =:= B -> true ; format("ceil_mismatch(~w,~w,~w,~w)~n",[D,N,A,B])).
:- forall(between(0, 3000000, D), (cc(D,1250), cc(D,2500))), forall(between(1,20000,_), (D is random(1000000000), cc(D,1250), cc(D,2500))), format("ceil done~n").
:- halt.
