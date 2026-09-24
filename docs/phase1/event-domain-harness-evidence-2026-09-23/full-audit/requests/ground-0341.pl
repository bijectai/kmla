s3306_c(alice_employer,alice,bob,Day,_) :-
    (
        nonvar(Day),
        is_before("2011-02-01",Day),
        is_before(Day,"2019-11-19")
    );
    var(Day).
purpose_(alice_employer,"agricultural labor").
death_(bob_dies).
agent_(bob_dies,bob).
start_(bob_dies,"2019-11-25").
end_(bob_dies,"2019-11-25").
marriage_(bob_and_charlie).
agent_(bob_and_charlie,bob).
agent_(bob_and_charlie,charlie).
payment_(alice_pays).
agent_(alice_pays,alice).
patient_(alice_pays,charlie).
start_(alice_pays,"2020-01-20").
end_(alice_pays,"2020-01-20").
purpose_(alice_pays,alice_employer).
amount_(alice_pays,1200).
