s3306_c(Service_event,alice,Employee,Day,_) :-
    member(Day, ["2017-01-24","2017-02-04","2017-03-03","2017-03-19","2017-04-02","2017-05-09","2017-10-15","2017-10-25","2017-11-08","2017-11-22","2017-12-01","2017-12-03"]),
    (
        (
            Day == "2017-01-24",
            member(Employee, [bob,cameron,dan,emily,fred])
        );
        (
            Day == "2017-02-04",
            member(Employee, [bob,cameron,dan,emily,fred])
        );
        (
            Day == "2017-03-03",
            member(Employee, [bob,cameron,dan,emily,fred])
        );
        (
            Day == "2017-03-19",
            member(Employee, [cameron,dan,emily,fred,george])
        );
        (
            Day == "2017-04-02",
            member(Employee, [bob,cameron,dan,fred,george])
        );
        (
            Day == "2017-05-09",
            member(Employee, [cameron,dan,emily,fred,george])
        );
        (
            Day == "2017-10-15",
            member(Employee, [bob,cameron,dan,emily,george])
        );
        (
            Day == "2017-10-25",
            member(Employee, [bob,cameron,dan,emily,fred,george])
        );
        (
            Day == "2017-11-08",
            member(Employee, [bob,cameron,emily,fred,george])
        );
        (
            Day == "2017-11-22",
            member(Employee, [bob,cameron,dan,emily,fred])
        );
        (
            Day == "2017-12-01",
            member(Employee, [bob,cameron,dan,emily,george])
        );
        (
            Day == "2017-12-03",
            member(Employee, [bob,cameron,dan,emily,george])
        )
    ),
    atom_concat("alice_employer_",Day,Service_event).
purpose_(_,"agricultural labor").
