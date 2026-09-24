service_(alice_employer).
patient_(alice_employer,alice).
agent_(alice_employer,bob).
start_(alice_employer,"2017-02-01").
end_(alice_employer,"2017-09-02").
purpose_(alice_employer,"domestic service").
payment_(alice_pays_bob).
agent_(alice_pays_bob,alice).
patient_(alice_pays_bob,bob).
start_(alice_pays_bob,"2017-09-02").
purpose_(alice_pays_bob,alice_employer).
amount_(alice_pays_bob,53200).
income_(alice_income).
start_(alice_income,"2017-12-31").
amount_(alice_income,921324).
agent_(alice_income,alice).
