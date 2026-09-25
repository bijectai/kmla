% Read-only measurement for the G6 exclusion proposal: which of the 376 originals
% fall in the candidate region. NOT a V-rule implementation, filter or case
% reader for any lane. For each case file it asserts the case's own facts and
% case-local rules (skipping directives and stipulated statute clauses, which
% it lists), evaluates two candidate region predicates under a time limit, and
% then erases the asserted clauses. The two unterminated files get the signed
% H4.4 reader exception: a full stop restored after line 26.
:- use_module(library(time)).
:- use_module(library(readutil)).
:- use_module(library(charsio)).

dom_location("private home").
dom_location("local college club").
dom_location("local chapter of a college fraternity").
dom_location("local chapter of a college sorority").

% dom0: a domestic service at a domestic location, with US employment under
% s3306_c_A or s3306_c_B (section3306.pl:437-438, :591-603).
dom0(S, P, E) :-
    service_(S),
    once(( type_(S, "domestic service") ; purpose_(S, "domestic service") )),
    location_(S, L), dom_location(L),
    patient_(S, P), agent_(S, E),
    once(( s3306_c_A(S, P, E) ; s3306_c_B(S, P, E, _) )).

% reach604: dom0 and the :440 test passes with Caly unbound, as it does when
% s3306_c is entered with Workday and Caly free (:44, :143, :172, :310, :343,
% :354, :405), so evaluation proceeds to :441 and then :604.
reach604(S, P, E) :- dom0(S, P, E), \+ s3306_c_1(S, _Caly).

main :-
    consult('/corpus/statutes/prolog/init.pl'),
    findall(F, ( expand_file_name('/corpus/cases/*.pl', Fs), member(F, Fs) ), Files0),
    msort(Files0, Files),
    length(Files, N), snapshot(cases(N)),
    forall(member(F, Files),
           ( catch(measure(F), Error, (snapshot(measure_error(F, Error)), fail)) -> true
           ; snapshot(measure_failed(F)) )),
    snapshot(done(N)),
    halt(0).

% Positive and negative controls for this instrument: the same predicates on
% the diagnostic's candidate household (expected in the region) and on its
% control household (expected outside it).
main_files(Files) :-
    consult('/corpus/statutes/prolog/init.pl'),
    forall(member(F, Files),
           ( catch(measure(F), Error, (snapshot(measure_error(F, Error)), fail)) -> true
           ; snapshot(measure_failed(F)) )),
    length(Files, N), snapshot(done(N)),
    halt(0).

% The 31 stipulated signatures of H4.1, copied from Interface/TIME_SCHEMA.json
% ("stipulation": true). Two of them (s151_d/4, s63_c_3/4) have no statute
% clauses at that arity, so the clause test below alone would miss them.
h41_stipulated(s2_a/3).
h41_stipulated(s2_b/3).
h41_stipulated(s63/3).
h41_stipulated(s63_c/3).
h41_stipulated(s63_c_1/3).
h41_stipulated(s63_c_2/3).
h41_stipulated(s63_c_3/3).
h41_stipulated(s63_d/4).
h41_stipulated(s63_f_1_A/2).
h41_stipulated(s63_f_1_B/3).
h41_stipulated(s68_b/3).
h41_stipulated(s151/5).
h41_stipulated(s151_b/3).
h41_stipulated(s151_b_applies/2).
h41_stipulated(s151_b_applies/3).
h41_stipulated(s151_c_applies/3).
h41_stipulated(s151_c/4).
h41_stipulated(s152_b_2/4).
h41_stipulated(s152_c/3).
h41_stipulated(s152_c_1/3).
h41_stipulated(s152_c_2/4).
h41_stipulated(s152_c_3/3).
h41_stipulated(s152_d_2_H/6).
h41_stipulated(total_wages_employer/6).
h41_stipulated(s3306_a/2).
h41_stipulated(s3306_b/8).
h41_stipulated(s3306_c/5).
h41_stipulated(s7703/4).
h41_stipulated(s151_d/4).
h41_stipulated(s2_a/5).
h41_stipulated(s63_c_3/4).

stipulation_pred(Name/Arity) :- h41_stipulated(Name/Arity), !.
stipulation_pred(Name/Arity) :- statute_pred(Name/Arity).

statute_pred(Name/Arity) :-
    functor(Head, Name, Arity),
    predicate_property(user:Head, number_of_clauses(C)), C > 0,
    predicate_property(user:Head, file(File)),
    sub_atom(File, _, _, _, '/statutes/prolog/'),
    \+ sub_atom(File, _, _, _, 'events.pl').

measure(File) :-
    file_base_name(File, Base),
    read_file_to_codes(File, Codes0, [encoding(utf8)]),
    h44(Base, Codes0, Codes),
    catch(load_terms(Codes, Stips), LoadError, (Stips = [], snapshot(load_error(Base, LoadError)))),
    eval(Base, dom0,     findall(S-P-E, dom0(S, P, E), L0), L0, Dom0),
    eval(Base, reach604, findall(S-P-E, reach604(S, P, E), L1), L1, Reach),
    ( is_list(Reach) ->
        findall(S-Outcome,
                ( member(S-_-_, Reach),
                  catch(( call_with_time_limit(20, \+ s3306_c_2(S, _, _)) -> Outcome = no_raise_true
                        ; Outcome = no_raise_false ),
                        Ex, Outcome = raised(Ex)) ),
                Raises)
    ; Raises = not_evaluated ),
    sort(Stips, StipPreds),
    findall(R, recorded(g6_ref, R), Refs), length(Refs, NRefs),
    snapshot(case(Base, clauses(NRefs), stipulations_skipped(StipPreds), dom0(Dom0), reach604(Reach), s3306_c_2_at_441(Raises))),
    forall(recorded(g6_ref, R, Key), ( erase(R), erase(Key) )).

% H4.4 (DECISIONS.md:758-762): restore the full stop after line 26 of the two
% unterminated s3306_c_2 files. No other file is altered.
h44(Base, Codes0, Codes) :-
    ( memberchk(Base, ['s3306_c_2_pos.pl', 's3306_c_2_neg.pl']) ->
        split_lines(Codes0, Lines0),
        nth1(26, Lines0, L26), append(L26, [0'.], L26b),
        nth1(26, Lines0, _, Rest), nth1(26, Lines1, L26b, Rest),
        join_lines(Lines1, Codes),
        snapshot(h44_restored(Base, line(26)))
    ; Codes = Codes0 ).

split_lines(Codes, [Line | Lines]) :-
    ( append(Line, [0'\n | Rest], Codes) -> split_lines(Rest, Lines)
    ; Line = Codes, Lines = [] ).
join_lines([Line], Line) :- !.
join_lines([Line | Lines], Codes) :-
    join_lines(Lines, Tail), append(Line, [0'\n | Tail], Codes).

eval(Base, Label, Goal, Result, Out) :-
    catch(( call_with_time_limit(60, Goal) -> Out = Result ; Out = failed ),
          Ex, ( Out = error(Ex), snapshot(eval_error(Base, Label, Ex)) )).

load_terms(Codes, Stips) :-
    setup_call_cleanup(open_chars_stream(Codes, Stream),
                       read_all(Stream, Stips), close(Stream)).

read_all(Stream, Stips) :-
    read_term(Stream, Term, [syntax_errors(error)]),
    ( Term == end_of_file -> Stips = []
    ; Term = (:- _) -> read_all(Stream, Stips)
    ; ( Term = (Head :- _) -> true ; Head = Term ),
      functor(Head, Name, Arity),
      ( stipulation_pred(Name/Arity) ->
          Stips = [Name/Arity | Stips1], read_all(Stream, Stips1)
      ; assertz(Term, Ref), recordz(g6_ref, Ref), read_all(Stream, Stips)
      )
    ).

snapshot(Term) :-
    copy_term(Term, Copy), numbervars(Copy, 0, _),
    write_term(Copy, [quoted(true), numbervars(true)]), nl, flush_output.
