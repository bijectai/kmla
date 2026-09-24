% Candidate H4 measurement only. No protected installation or parity producer.
% Source references distinguish case clauses from the original statute clauses.
:- use_module(library(http/json)).
:- use_module(library(lists)).

main :-
    catch(run, Error, (print_message(error, Error), halt(2))),
    halt(0).

run :-
    current_prolog_flag(argv, [Input, Registry, Candidate, TaxInput]),
    consult(Registry),
    setup_call_cleanup(open(Input, read, Stream, [encoding(utf8)]),
                       read_clauses(Stream, Clauses), close(Stream)),
    % Declare before definitions are compiled: SWI 7.2.3 will not convert an
    % already-loaded static statute predicate with dynamic/1. Its original
    % clauses still load first, followed by the case's assertions (H4.1).
    declare_heads(Clauses),
    consult('/corpus/statutes/prolog/init.pl'),
    install(Clauses, 1, Refs),
    check_candidate(Candidate, Refs),
    statistics(cputime, T0),
    get_time(W0),
    % H1: retain source-clause provenance across the H4 evaluation phases.
    findall(I-(P-H), unary_solution(Refs, I, P, H), Unary),
    findall(E, member(_-(_-E), Unary), EventProofs),
    % A-023: the traversal universe has distinct ground terms in first-seen
    % order. Unary/UnaryFacts and every binary proof retain multiplicity.
    distinct_terms(EventProofs, Events),
    findall(E, member(_-(service_-E), Unary), ServiceProofs),
    distinct_terms(ServiceProofs, Services),
    findall(I-H, binary_solution(Refs, Events, Services, Candidate, I, H), Binary),
    findall(I-H, (member(I-(P-E), Unary), H =.. [P,E]), UnaryFacts),
    append(UnaryFacts, Binary, Unsorted),
    keysort(Unsorted, Ordered),
    pairs_values(Ordered, FactHeads),
    findall(I, member(I-_,Ordered), FactSources),
    findall(H, stipulated_solution(Refs, H), StipHeads),
    statistics(cputime, T1), get_time(W1),
    % One numbering traversal preserves shared variables within a solution;
    % findall has already freshened separate solutions per A1/A3.
    % Validate before numbering so a supplied '$VAR'/1 compound cannot be
    % mistaken for a variable marker. Unsupported inputs remain findings.
    validate_stips(StipHeads),
    numbervars(FactHeads-StipHeads, 0, WildCount),
    encode_facts(FactHeads, Facts), encode_stips(StipHeads, Stips),
    encode_unary(Unary, UnaryJSON),
    encode_event_domain(Events, EventDomainJSON),
    length(EventProofs, UnaryProofCount),
    length(Events, EventCount), length(Services, ServiceCount),
    length(ServiceProofs, ServiceProofCount),
    length(FactHeads, FactCount), length(StipHeads, StipCount),
    candidate_counts(Candidate, FactHeads, EventCount, ServiceCount, CandidateStats),
    CPU is T1-T0, Wall is W1-W0,
    % tax/3 is the only observation implemented here: H6.1/H6.2 explicitly
    % mandate its first solution with amount unbound, never full backtracking.
    tax_observation(TaxInput, Tax),
    json_write(current_output, json([
        household=json([facts=Facts, stipulations=Stips]), unary=UnaryJSON,
        event_domain=EventDomainJSON,
        fact_source_clauses=FactSources,
        stats=json([unary_proofs=UnaryProofCount, distinct_event_domain=EventCount,
                    service_proofs=ServiceProofCount,
                    distinct_service_domain=ServiceCount, fact_count=FactCount,
                    stipulation_count=StipCount, wildcard_count=WildCount,
                    grounding_cpu_seconds=CPU, grounding_wall_seconds=Wall,
                    candidate=CandidateStats]),
        tax=Tax])), nl.

read_clauses(Stream, Clauses) :-
    read_term(Stream, Clause, [syntax_errors(error)]),
    ( Clause == end_of_file -> Clauses = []
    ; Clause = (:- _) -> throw(error(unexpected_case_directive, install/3))
    ; validate_country_clause(Clause),
      Clauses = [Clause|Rest], read_clauses(Stream,Rest)
    ).

% A-021: only the supplied, ground BODYLESS country_/2 clause is covered.
% Check syntax before assertz: clause/3 cannot distinguish a fact from :- true.
validate_country_clause(Clause) :-
    clause_parts(Clause,H,_),
    ( functor(H,country_,2) ->
        ( Clause = (_ :- _) -> throw(error(country_rule_not_covered, read_clauses/2))
        ; ground(H) -> true
        ; throw(error(nonground_country_not_covered, read_clauses/2)) )
    ; true ).

declare_heads([]).
declare_heads([Clause|Rest]) :-
    clause_parts(Clause,H,_), functor(H,P,A), dynamic(P/A), declare_heads(Rest).

install([], _, []).
install([Clause|Clauses], I, [ref(I,P,A,Ref)|Refs]) :-
    clause_parts(Clause,Head,_), functor(Head,P,A), assertz(Clause,Ref),
    J is I+1, install(Clauses,J,Refs).

clause_parts((Head :- Body), Head, Body) :- !.
clause_parts(Head, Head, true).

expected_purpose((purpose_(P,S) :-
    split_string(P,"_","",[Xp,Yp,Zp]),
    split_string(S,"_","",[Xs,Ys,Zs]),
    Xp=="payment", Xs=="workforalice", Yp==Ys, Zp==Zs)).

check_candidate(regular, _) :- !.
check_candidate(tax_case_33, Refs) :- !,
    findall(Head-Body,
        (member(ref(_,purpose_,2,Ref), Refs), clause(Head,Body,Ref)), Clauses),
    expected_purpose(Expected),
    ( Clauses = [H-B], (H :- B) =@= Expected -> true
    ; throw(error(candidate_exact_unique_clause_mismatch, check_candidate/2)) ).
check_candidate(Mode, _) :- throw(error(unknown_candidate_mode(Mode), check_candidate/2)).

unary_solution(Refs, I, P, E) :-
    member(ref(I,P,1,Ref), Refs), fact_kind(P,[term]),
    clause(H,Body,Ref), H =.. [P,E], call(Body),
    ( ground(E) -> true ; throw(error(unbound_unary_event(P), unary_solution/4)) ).

binary_solution(Refs, Events, Services, Candidate, I, H) :-
    member(ref(I,P,2,Ref), Refs), fact_kind(P,[_,_]),
    clause(H,Body,Ref), arg(1,H,First),
    ( P == country_ ->
        % H3's place position is not an event position. Emit once at this
        % original source-clause index I (stable keysort above), not grouped
        % before/after the event facts. Tags and duplicate clauses are intact.
        ( Body == true, ground(H) -> true
        ; throw(error(unsupported_country_clause, binary_solution/6)) )
    ; Body == true, var(First) ->
        % H2 explicitly retains the bodyless purpose pattern without expansion.
        ( P == purpose_ -> true ; throw(error(unapproved_event_wildcard(P), binary_solution/6)) )
    ; Candidate == tax_case_33, P == purpose_ ->
        % Replacement, not supplement. All proof copies are retained by findall.
        member(Event,Events), member(Service,Services),
        H = purpose_(Event,Service), call(H)
    ; member(Event,Events), First = Event, call(Body)
    ).

stipulated_solution(Refs, H) :-
    member(ref(_,P,A,Ref), Refs), stip_kind(P,A,_),
    % Calling this clause BODY excludes the base statute's proofs while still
    % resolving any body calls against the complete original program.
    clause(H,Body,Ref), call(Body).

distinct_terms(List, Unique) :- distinct_terms(List, [], Unique).
distinct_terms([], _, []).
distinct_terms([H|T], Seen, U) :-
    ( identical_member(H,Seen) -> distinct_terms(T,Seen,U)
    ; U = [H|Rest], distinct_terms(T,[H|Seen],Rest) ).
identical_member(H,[X|_]) :- H == X, !.
identical_member(H,[_|T]) :- identical_member(H,T).

pairs_values([], []).
pairs_values([_-V|T], [V|R]) :- pairs_values(T,R).

candidate_counts(regular, _, _, _, json([scope=not_applicable])) :- !.
candidate_counts(tax_case_33, Facts, EC, SC, JSON) :-
    Calls is EC*SC,
    findall(1, member(purpose_(_,_),Facts), Proofs), length(Proofs,N),
    JSON = json([outer_iterations=EC,inner_distinct_terms=SC,
                 full_two_input_calls=Calls,successful_proofs=N]).

encode_unary([], []).
encode_unary([I-(P-E)|Rows], [json([source_clause=I,predicate=P,event=Value])|Out]) :-
    term_json(E,Value), encode_unary(Rows,Out).

encode_event_domain([], []).
encode_event_domain([E|Events], [J|JSON]) :-
    term_json(E,J), encode_event_domain(Events,JSON).

encode_facts([], []).
encode_facts([H|T], [json([ctor=P,args=Args])|R]) :-
    H =.. [P|Values], fact_kind(P,Kinds),
    fact_args(Kinds,Values,Args), encode_facts(T,R).
fact_args([], [], []).
fact_args([Kind|KT], [Value|VT], [J|JT]) :-
    fact_arg(Kind,Value,J), fact_args(KT,VT,JT).
fact_arg(term,V,J) :- term_json(V,J).
fact_arg(pat,V,J) :- pat_json(V,J).
fact_arg(int,V,V) :-
    ( integer(V) -> true ; throw(error(noninteger_amount(V), fact_arg/3)) ).
fact_arg(day,V,V) :-
    ( string(V) -> true ; throw(error(nonstring_day(V), fact_arg/3)) ).

encode_stips([], []).
encode_stips([H|T], [json([pred=C,args=Args])|R]) :-
    H =.. [P|Values], length(Values,A), stip_kind(P,A,C),
    pattern_args(Values,Args), encode_stips(T,R).
pattern_args([], []).
pattern_args([V|T], [J|R]) :- stip_arg_json(V,J), pattern_args(T,R).
stip_arg_json('$VAR'(N), json([wild=N])) :- !.
stip_arg_json(V, json([list=Items])) :- is_list(V), !, pattern_args(V,Items).
stip_arg_json(V, json([val=J])) :- term_json(V,J).

validate_stips([]).
validate_stips([H|T]) :- H =.. [_|Args], validate_stip_args(Args), validate_stips(T).
validate_stip_args([]).
validate_stip_args([H|T]) :- validate_stip_arg(H), validate_stip_args(T).
validate_stip_arg(V) :-
    ( var(V) -> true
    ; is_list(V) -> validate_stip_args(V)
    ; integer(V) -> true
    ; atom(V) -> true
    ; string(V) -> true
    ; throw(error(unsupported_household_term(V),validate_stip_arg/1)) ).

pat_json('$VAR'(N), json([wild=N])) :- !.
pat_json(V, json([val=J])) :- term_json(V,J).
term_json(V,J) :-
    ( integer(V) -> J = V
    ; atom(V) -> J = json([a=V])
    ; string(V) -> J = json([s=V])
    ; throw(error(unsupported_household_term(V), term_json/2)) ).

tax_observation(none, json([status=not_requested])) :- !.
tax_observation(Input, json([status=first_solution,value=Amount,cpu_seconds=CPU,wall_seconds=Wall])) :-
    read_term_from_atom(Input, tax_inputs(Person,Year), [syntax_errors(error)]),
    ( ground(Person-Year) -> true ; throw(error(unbound_tax_inputs, tax_observation/2)) ),
    statistics(cputime,T0), get_time(W0),
    ( once(tax(Person,Year,Amount)) -> true ; throw(error(no_tax_first_solution, tax_observation/2)) ),
    ( integer(Amount) -> true ; throw(error(noninteger_tax_observation(Amount), tax_observation/2)) ),
    statistics(cputime,T1), get_time(W1), CPU is T1-T0, Wall is W1-W0.
