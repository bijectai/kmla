% Diagnostic only: the precise H4.2 event-bound call on the original case.
% The caller supplies reader-approved clause terms, never case directives.
:- use_module(library(http/json)).

main :-
    catch(run, Error, (print_message(error, Error), halt(2))),
    halt(0).

run :-
    current_prolog_flag(argv, [Clauses]),
    consult('/corpus/statutes/prolog/init.pl'),
    setup_call_cleanup(open(Clauses, read, Stream, [encoding(utf8)]),
                       install(Stream), close(Stream)),
    findall(E, payment_(E), Events),
    length(Events, Count),
    json_write(current_output, json([payment_solutions=Count])), nl,
    ( Events = [Event|_] -> true ; throw(error(no_payment_event, run/0)) ),
    write_term(Event, [quoted(true)]), nl,
    % Do not bind the second position or replace this goal after a failure.
    findall(Purpose, purpose_(Event, Purpose), Purposes),
    write_term(Purposes, [quoted(true)]), nl.

install(Stream) :-
    read_term(Stream, Term, [syntax_errors(error)]),
    ( Term == end_of_file -> true
    ; Term = (:- _) -> throw(error(unexpected_directive, install/1))
    ; assertz(Term), install(Stream)
    ).
