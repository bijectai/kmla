% Read-only diagnostic of the existing H4.2 call. NOT a replacement grounder.
% First execute the original goal unchanged. Then retrieve its original clause
% and expose each conjunction call, in order, to report the failing bindings.
% No clause body is rewritten; no Household, reference answer or fallback is made.

main :- catch(run, Error, (print_message(error, Error), halt(2))), halt(0).

run :-
    consult('/corpus/statutes/prolog/init.pl'),
    setup_call_cleanup(open('/request/001.pl', read, Stream, [encoding(utf8)]),
                       install(Stream), close(Stream)),
    findall(E, payment_(E), Events),
    Events = [Event|_],
    ground(Event), var(Purpose),
    snapshot(original_call(findall(Purpose, purpose_(Event,Purpose), Purposes))),
    catch(findall(Purpose, purpose_(Event,Purpose), Purposes), OriginalError, true),
    ( var(OriginalError) -> throw(error(unexpected_original_success, run/0))
    ; snapshot(original_exception(OriginalError))
    ),
    % Select the actual retained rule with its original two split_string calls.
    % All unifications below inspect its syntax; neither split input is filled in.
    once((clause(purpose_(Event,Service), Body),
          Body = (split_string(Event,"_","",[Xp,Yp,Zp]),
                 (split_string(Service,"_","",[Xs,Ys,Zs]),_)))),
    snapshot(original_clause((purpose_(Event,Service) :- Body))),
    trace_conjunction(Body,
        [event=Event, service=Service, xp=Xp, yp=Yp, zp=Zp, xs=Xs, ys=Ys, zs=Zs]).

trace_conjunction(Goal, Bindings) :-
    ( Goal = (First,Rest) ->
        trace_conjunction(First, Bindings), trace_conjunction(Rest, Bindings)
    ; snapshot(before_call(Goal, Bindings)), call(Goal)
    ).

snapshot(Term) :-
    copy_term(Term, Copy), numbervars(Copy, 0, _),
    write_term(Copy, [quoted(true), numbervars(true)]), nl, flush_output.

install(Stream) :-
    read_term(Stream, Term, [syntax_errors(error)]),
    ( Term == end_of_file -> true
    ; Term = (:- _) -> throw(error(unexpected_directive, install/1))
    ; assertz(Term), install(Stream)
    ).
