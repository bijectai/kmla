marriage_(alice_and_bob).
agent_(alice_and_bob,alice).
agent_(alice_and_bob,bob).
start_(alice_and_bob,"1992-02-03").
death_(alice_dies).
agent_(alice_dies,alice).
start_(alice_dies,"2014-07-09").
end_(alice_dies,"2014-07-09").
residence_(charlie_and_bob_residence).
agent_(charlie_and_bob_residence,charlie).
agent_(charlie_and_bob_residence,bob).
patient_(charlie_and_bob_residence,bob_s_house).
start_(charlie_and_bob_residence,"2004-01-01").
end_(charlie_and_bob_residence,"2019-12-31").
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
s152_d_2_H(charlie,bob,Year,_,Start_day,End_day) :-
    between(2015,2019,Year),first_day_year(Year,Start_day),last_day_year(Year,End_day).
bob_income(Year,Event,Start_day,End_day) :-
    between(2015,2019,Year),
    atom_concat('bob_income_',Year,Event),
    first_day_year(Year,Start_day),
    last_day_year(Year,End_day).
income_(Event) :- bob_household_maintenance(_,Event,_,_).
agent_(Event,bob) :- bob_household_maintenance(_,Event,_,_).
amount_(Event,300000) :- bob_household_maintenance(_,Event,_,_).
start_(Event,Start_day) :- bob_household_maintenance(_,Event,Start_day,_).
end_(Event,End_day) :- bob_household_maintenance(_,Event,_,End_day).
