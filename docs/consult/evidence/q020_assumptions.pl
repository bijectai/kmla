% Read-only tests of two A-020 arguments, NOT a grounder or H4.3 check.
main :- catch(run, Error, (print_message(error, Error), halt(2))), halt(0).

run :-
    consult('/corpus/statutes/prolog/init.pl'),
    setup_call_cleanup(open('/request/001.pl', read, Stream, [encoding(utf8)]),
                       install(Stream), close(Stream)),
    findall(P-E, (q020_unary(P), functor(G,P,1), arg(1,G,E), call(G)), Events),
    forall(member(_-E, Events), ground(E)),
    findall(E, service_(E), Services),
    findall(P-E, (member(P-E,Events),
                 split_string(E,"_","",["workforalice",_,_])), WorkEvents),
    findall(P-E, (member(P-E,WorkEvents),
                 (P \== service_ ; \+ member_identical(E,Services))), Violations),
    length(Events, EventCount), length(Services, ServiceCount),
    length(WorkEvents, WorkCount),
    snapshot(unary_solution_count(EventCount)),
    snapshot(service_solution_count(ServiceCount)),
    snapshot(workforalice_solution_count(WorkCount)),
    snapshot(workforalice_provenance(WorkEvents)),
    snapshot(provenance_violations(Violations)),
    Violations == [],
    forall(member(Input,[alice,home,"home","agricultural labor","workforalice"]),
           (expect_failure(split_string(Input,"_","",[_,_,_])),
            expect_failure(purpose_(payment_2015_1,Input)))).

member_identical(E,[H|_]) :- E == H, !.
member_identical(E,[_|T]) :- member_identical(E,T).

expect_failure(Goal) :-
    catch((once(call(Goal)) -> Status=success ; Status=failure),
          Error, Status=raised(Error)),
    snapshot(observation(Goal,Status)),
    (Status == failure -> true ; throw(error(unexpected_result(Goal,Status),run/0))).

snapshot(Term) :-
    copy_term(Term,Copy), numbervars(Copy,0,_),
    write_term(Copy,[quoted(true),numbervars(true)]), nl, flush_output.

install(Stream) :-
    read_term(Stream,Term,[syntax_errors(error)]),
    (Term == end_of_file -> true
    ; Term = (:- _) -> throw(error(unexpected_directive,install/1))
    ; assertz(Term), install(Stream)).
