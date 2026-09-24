marriage_(bob_and_alice).
agent_(bob_and_alice,bob).
agent_(bob_and_alice,alice).
start_(bob_and_alice,"1992-02-03").
death_(bob_dies).
agent_(bob_dies,bob).
start_(bob_dies,"2014-07-09").
end_(bob_dies,"2014-07-09").
son_(charlie_is_son).
agent_(charlie_is_son,charlie).
patient_(charlie_is_son,bob).
patient_(charlie_is_son,alice).
start_(charlie_is_son,"2000-10-09").
residence_(charlie_and_alice_residence).
agent_(charlie_and_alice_residence,charlie).
agent_(charlie_and_alice_residence,alice).
patient_(charlie_and_alice_residence,alice_s_house).
start_(charlie_and_alice_residence,"2004-01-01").
end_(charlie_and_alice_residence,"2019-12-31").
alice_household_maintenance(Year,Event,Start_day,End_day) :-
    between(2004,2019,Year),
    atom_concat('alice_maintains_household_',Year,Event),
    first_day_year(Year,Start_day),
    last_day_year(Year,End_day).
payment_(Event) :- alice_household_maintenance(_,Event,_,_).
agent_(Event,alice) :- alice_household_maintenance(_,Event,_,_).
amount_(Event,1) :- alice_household_maintenance(_,Event,_,_).
purpose_(Event,alice_s_house) :- alice_household_maintenance(_,Event,_,_).
start_(Event,Start_day) :- alice_household_maintenance(_,Event,Start_day,_).
end_(Event,End_day) :- alice_household_maintenance(_,Event,_,End_day).
income_(alice_income_2017).
agent_(alice_income_2017,alice).
amount_(alice_income_2017,25561).
start_(alice_income_2017,"2017-12-31").
