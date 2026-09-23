% Read-only verification of A-017's numeric/domain claims, NOT a grounder.
% No Household, producer record, reference answer or amended design is emitted.
:- use_module(library(http/json)).

main :- catch(run, Error, (print_message(error, Error), halt(2))), halt(0).

run :-
    consult('/corpus/statutes/prolog/init.pl'),
    setup_call_cleanup(open('/request/001.pl', read, Stream, [encoding(utf8)]),
                       install(Stream), close(Stream)),
    findall(P, payment_(P), Payments),
    findall(S, service_(S), Services),
    length(Payments, PN), length(Services, SN),
    % This finite diagnostic checks a claimed number only. It asserts neither
    % completeness nor any approved ordering/domain for H4 production use.
    findall((P,S), (member(P,Payments), member(S,Services), purpose_(P,S)), Pairs),
    length(Pairs, PairCount),
    (purpose_(payment_2099_999,workforalice_2099_999) -> Outside = true ; Outside = false),
    (payment_(payment_2099_999) -> PaymentDeclared = true ; PaymentDeclared = false),
    (service_(workforalice_2099_999) -> ServiceDeclared = true ; ServiceDeclared = false),
    json_write(current_output, json([
        declared_payment_solutions=PN, declared_service_solutions=SN,
        declared_pair_solutions=PairCount, outside_pair_succeeds=Outside,
        outside_payment_declared=PaymentDeclared, outside_service_declared=ServiceDeclared
    ])), nl.

install(Stream) :-
    read_term(Stream, Term, [syntax_errors(error)]),
    ( Term == end_of_file -> true
    ; Term = (:- _) -> throw(error(unexpected_directive, install/1))
    ; assertz(Term), install(Stream)
    ).
