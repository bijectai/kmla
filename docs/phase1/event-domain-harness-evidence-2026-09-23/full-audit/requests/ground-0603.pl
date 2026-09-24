income_(alice_income).
agent_(alice_income,alice).
amount_(alice_income,6662).
start_(alice_income,"2017-12-31").
income_(bob_income).
agent_(bob_income,bob).
amount_(bob_income,17896).
start_(bob_income,"2017-12-31").
marriage_(alice_and_bob).
agent_(alice_and_bob,alice).
agent_(alice_and_bob,bob).
start_(alice_and_bob,"1992-02-03").
residence_(alice_and_bob_residence).
agent_(alice_and_bob_residence,charlie).
agent_(alice_and_bob_residence,bob).
patient_(alice_and_bob_residence,bob_s_house).
start_(alice_and_bob_residence,"2004-01-01").
end_(alice_and_bob_residence,"2019-12-31").
bob_household_maintenance(Year,Event,Start_day,End_day) :-
    between(2015,2019,Year),
    atom_concat('bob_maintains_household_',Year,Event),
    first_day_year(Year,Start_day),
    last_day_year(Year,End_day).
payment_(Event) :- bob_household_maintenance(_,Event,_,_).
agent_(Event,bob) :- bob_household_maintenance(_,Event,_,_).
amount_(Event,1) :- bob_household_maintenance(_,Event,_,_).
purpose_(Event,bob_s_house) :- bob_household_maintenance(_,Event,_,_).
start_(Event,Start_day) :- bob_household_maintenance(_,Event,Start_day,_).
end_(Event,End_day) :- bob_household_maintenance(_,Event,_,End_day).
