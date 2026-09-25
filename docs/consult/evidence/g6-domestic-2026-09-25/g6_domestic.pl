% Read-only G6 diagnostic (A-025, R-Q025). NOT a V-rule, exclusion, repair or
% reference answer. It consults the pinned statutes unchanged, installs one
% household's facts with assertz (as the 2026-09-23 H4 diagnostic did), runs ONE
% probe goal to its first solution under catch/3, and prints the result or the
% exception. For the first instantiation error of the probe it also prints the
% exception-time backtrace (goal, bindings and clause locations). No clause is
% rewritten and no goal is substituted.
:- use_module(library(prolog_stack)).
:- multifile user:prolog_exception_hook/4.
:- dynamic g6_backtrace_printed/0.

user:prolog_exception_hook(error(instantiation_error, Context), _, Frame, _) :-
    \+ g6_backtrace_printed,
    assertz(g6_backtrace_printed),
    snapshot(first_instantiation_error(Context)),
    catch(( get_prolog_backtrace(60, Backtrace, [frame(Frame)]),
            format('BACKTRACE-BEGIN~n', []),
            print_prolog_backtrace(user_output, Backtrace),
            format('BACKTRACE-END~n', []) ),
          BacktraceError,
          snapshot(backtrace_unavailable(BacktraceError))),
    flush_output,
    fail.

main(HouseholdFile, Label) :-
    catch(run(HouseholdFile, Label), Error,
          ( snapshot(driver_error(Error)), halt(3) )),
    halt(0).

run(HouseholdFile, Label) :-
    consult('/corpus/statutes/prolog/init.pl'),
    atom_concat('/audit/', HouseholdFile, Path),
    setup_call_cleanup(open(Path, read, Stream, [encoding(utf8)]),
                       install(Stream), close(Stream)),
    probe(Label, Goal),
    snapshot(household(HouseholdFile)),
    snapshot(probe(Label, Goal)),
    catch(( once(Goal) -> Result = success(Goal) ; Result = failure ),
          Exception, Result = exception(Exception)),
    snapshot(result(Label, Result)).

% The probes Dev authorized (see README.md): the root query first, then the
% localizing calls on the source path, then V-rule support queries.
probe(root_tax,        tax(alice, 2017, _Tax)).
probe(root_tax_bob,    tax(bob, 2017, _Tax)).
probe(s3301,           s3301(alice, 2017, _Wages, _Employee, _Employment, _Tax)).
probe(s3306_a,         s3306_a(alice, 2017)).
probe(s3306_c,         s3306_c(_Service, alice, _Employee, _Day, _Caly)).
probe(s3306_a_3,       s3306_a_3(alice, _Service, _Wages, _Caly)).
probe(v5_is_child_of,  is_child_of(bob, alice, _Start, _End)).
probe(v10_s152_c_2,    findall(D-T, s152_c_2(D, T, _, _), _Pairs)).
probe(v8_s151_c_applies, findall(T-D, (member(T, [alice, bob]), s151_c_applies(T, D, 2017)), _Solutions)).

install(Stream) :-
    read_term(Stream, Term, [syntax_errors(error)]),
    ( Term == end_of_file -> true
    ; Term = (:- _) -> throw(error(unexpected_directive, install/1))
    ; assertz(Term), install(Stream)
    ).

snapshot(Term) :-
    copy_term(Term, Copy), numbervars(Copy, 0, _),
    write_term(Copy, [quoted(true), numbervars(true)]), nl, flush_output.
