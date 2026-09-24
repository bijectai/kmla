business_(alice_runs_a_factory).
agent_(alice_runs_a_factory,alice).
type_(alice_runs_a_factory,"manufacturing").
start_(alice_runs_a_factory,"2016-02-01").
service_(alice_employer).
patient_(alice_employer,alice).
agent_(alice_employer,bob).
start_(alice_employer,"2017-06-01").
end_(alice_employer,"2017-08-31").
type_(alice_employer,"painting Alice's house").
payment_(alice_pays_bob).
agent_(alice_pays_bob,alice).
patient_(alice_pays_bob,bob).
start_(alice_pays_bob,"2017-10-02").
end_(alice_pays_bob,"2017-10-02").
purpose_(alice_pays_bob,alice_employer).
amount_(alice_pays_bob,323).
means_(alice_pays_bob,"cash").
s3306_c(alice_employer,alice,bob,Day,_) :-
    (
        nonvar(Day),
        is_before("2017-06-01",Day),
        is_before(Day,"2017-08-31")
    );
    var(Day).
