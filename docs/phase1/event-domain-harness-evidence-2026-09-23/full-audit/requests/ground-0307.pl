s3306_c(Employment_event,alice,bob,Day,_) :-
    member(Day, ["2017-01-24","2017-02-04","2017-03-03","2017-03-19","2017-04-02","2017-10-25","2017-11-08","2017-11-22","2017-12-01","2017-12-03"]),
    atom_concat("alice_employer_",Day,Employment_event).
