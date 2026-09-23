% Read-only syntax diagnostic for emitted bodyless clauses, NOT H4 grounding.
:- use_module(library(http/json)).

main :-
    catch(run, Error, (print_message(error, Error), halt(2))),
    halt(0).

run :-
    current_prolog_flag(argv, [Path]),
    setup_call_cleanup(open(Path, read, Stream, [encoding(utf8)]),
                       clauses(Stream, Clauses), close(Stream)),
    json_write(current_output, Clauses), nl.

clauses(Stream, Clauses) :-
    read_term(Stream, Term, [variable_names(Names), syntax_errors(error)]),
    ( Term == end_of_file -> Clauses = []
    ; ( Term = (:- _) ; Term = (_ :- _) ) ->
        throw(error(expected_bodyless_clause, clauses/2))
    ; compound(Term) ->
        Term =.. [Pred|Args],
        arguments(Args, Names, Values),
        Clauses = [json([pred=Pred, args=Values])|Rest],
        clauses(Stream, Rest)
    ; throw(error(expected_predicate_arguments, clauses/2))
    ).

arguments([], _, []).
arguments([Arg|Args], Names, [Value|Values]) :-
    argument(Arg, Names, Value),
    arguments(Args, Names, Values).

argument(Arg, Names, Value) :-
    ( var(Arg) -> variable_name(Names, Arg, Name), Value = json([variable=Name])
    ; integer(Arg) -> Value = Arg
    ; atom(Arg) -> Value = json([a=Arg])
    ; string(Arg) -> Value = json([s=Arg])
    ; throw(error(unsupported_term(Arg), argument/3))
    ).

variable_name([Name=Var|Rest], Arg, Result) :-
    ( Var == Arg -> Result = Name ; variable_name(Rest, Arg, Result) ).
variable_name([], _, _) :- throw(error(unnamed_variable, variable_name/3)).
