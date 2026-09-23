% DRAFT DIAGNOSTIC ONLY. No domain restriction or production codec is installed.
:- module(birth_audit, [main/0]).
:- use_module(library(readutil)).
:- use_module(library(http/json)).
:- use_module(library(lists)).

read_terms(Stream, Terms) :-
    read_term(Stream, T, [syntax_errors(error)]),
    ( T == end_of_file -> Terms = []
    ; Terms = [T|Rest], read_terms(Stream, Rest) ).

source_terms(Path, Offset, Terms) :-
    read_file_to_codes(Path, Original, []),
    ( Offset < 0 -> Codes = Original
    ; length(Prefix, Offset), append(Prefix, Suffix, Original),
      append(Prefix, [46|Suffix], Codes) ),
    setup_call_cleanup(open_codes_stream(Codes, S), read_terms(S, Terms), close(S)).

is_directive((:- _)).
clause_head((H :- _), H) :- !.
clause_head(H, H).

% read_term does not execute the source. Only discontiguous declarations are
% retained. All loads, tests, halts and witness dynamic declarations are skipped.
install(Terms, Clauses, Skipped, Counts) :-
    findall(T, (member(T, Terms), \+ is_directive(T)), Clauses),
    findall(T, (member((:- T), Terms), T \= discontiguous(_)), Skipped),
    forall(member((:- discontiguous(Spec)), Terms), user:discontiguous(Spec)),
    findall(N/A, (member(C, Clauses), clause_head(C,H), functor(H,N,A)), Raw),
    sort(Raw, Sigs),
    % Predeclare case-supplied heads before init: this SWI release rejects
    % changing static predicate attributes after the canonical consult.
    forall(member(Sig, Sigs), user:dynamic(Sig)),
    user:consult('/corpus/statutes/prolog/init.pl'),
    maplist(clause_count,Sigs,Before),
    % assertz appends case clauses in original order, preserving duplicates.
    forall(member(C, Clauses), user:assertz(C)),
    maplist(check_count(Clauses),Sigs,Before,Counts).

clause_count(N/A,Count) :- functor(H,N,A),
    (predicate_property(user:H,number_of_clauses(Count)) -> true ; Count=0).
check_count(Clauses,N/A,Before,_{predicate:Name,arity:A,before:Before,added:Added,after:After}) :-
    atom_string(N,Name),
    findall(1,(member(C,Clauses),clause_head(C,H),functor(H,N,A)),Ones),length(Ones,Added),
    clause_count(N/A,After),Expected is Before+Added,
    (After=:=Expected -> true ; throw(error(clause_count_changed(N/A,Before,Added,After),_))).

ground_term(T) :-
    ( ground(T) -> true ; throw(error(nonground_audit_value(T), _)) ).
person_term(T) :- (atom(T); string(T)), !.
person_term(T) :- throw(error(non_person_term(T), _)).
term_text(T, S) :- ground_term(T), term_string(T,S,[quoted(true),ignore_ops(true)]).
texts(Ts,Ss) :- maplist(term_text,Ts,Ss).
pair_text([A,B],[SA,SB]) :- term_text(A,SA), term_text(B,SB).

% Audit-only set domain: every atom/string subterm in the source, supplemented
% by evaluated agent/patient/beneficiary values of every unary event solution.
% The original predicates are never deduplicated or replaced by these sets.
unary_event_names(Names) :-
    source_terms('/corpus/statutes/prolog/events.pl', -1, Declarations),
    findall(Name, member((:- discontiguous(Name/1)), Declarations), Names).
event_value(E, P) :- (user:agent_(E,P); user:patient_(E,P); user:beneficiary_(E,P)).
domain(Terms, Persons, Events) :-
    findall(T, (member(C,Terms), sub_term(T,C), ground(T), (atom(T);string(T))), Literals),
    unary_event_names(Names),
    findall(E, (member(N,Names), G=..[N,E], call(user:G)), Events),
    maplist(ground_term, Events),
    sort(Events, UniqueEvents),
    findall(P, (member(E,UniqueEvents), event_value(E,P)), Values),
    maplist(ground_term, Values), maplist(person_term,Values),
    append(Literals, Values, All), sort(All, Persons).

birth_record(E, _{event:ES,agents:Agents,starts:Starts}) :-
    term_text(E,ES),
    findall(P,user:agent_(E,P),Ps), texts(Ps,Agents),
    findall(D,user:start_(E,D),Ds), texts(Ds,Starts).

truth(Goal, B) :- (once(Goal) -> B=true ; B=false).
known_birth(P,D) :- user:birth_(E), user:agent_(E,P), user:start_(E,D).
equal_birth_record([P,Q,D], _{left:SP,right:SQ,date:SD,sibling:S,stepsibling:T,
                            k_left_to_right:K1,k_right_to_left:K2}) :-
    term_text(P,SP),term_text(Q,SQ),term_text(D,SD),
    truth(user:is_sibling_of(P,Q,_,_),S),
    truth(user:is_stepsibling_of(P,Q,_,_),T),
    truth(user:s152_c_2(Q,P,_,_),K1),truth(user:s152_c_2(P,Q,_,_),K2).

birth_state(P, Events, Dates) :-
    findall(E,(user:birth_(E),user:agent_(E,P)),Raw),sort(Raw,Events),
    findall(D,(member(E,Events),user:start_(E,D)),Ds),sort(Ds,Dates).

% These are observational checks of the proposed A condition, not source edits.
% Equality/uniqueness use distinct values only here; original clauses retain
% their multiplicity. Strict chronology calls the original date comparator in
% both directions, without changing is_before/2 or s152_c_3/3.
edge_age_record([T,D], _{taxpayer:ST,dependent:SD,c3_success_years:Years,
                       dependent_birth_events:DEs,taxpayer_birth_events:TEs,
                       dependent_dates:DDs,taxpayer_dates:TDs,
                       descendant:Desc,proposed_condition:Allowed,reasons:Reasons}) :-
    term_text(T,ST),term_text(D,SD),
    birth_state(D,DE,DD),birth_state(T,TE,TD),
    texts(DE,DEs),texts(TE,TEs),texts(DD,DDs),texts(TD,TDs),
    truth(user:is_descendent_of(D,T,_,_),Desc),
    findall(Y,(between(1900,2100,Y),once(user:s152_c_3(D,T,Y))),Years),
    ( DE == [] ->
        ( Desc == true -> Allowed=true,Reasons=[]
        ; Allowed=false,Reasons=["birthless_dependent_not_descendant"] )
    ; findall(R,(
          (DE \= [_],R="dependent_birth_event_count_not_one");
          (TE \= [_],R="taxpayer_birth_event_count_not_one");
          (DD \= [_],R="dependent_known_date_count_not_one");
          (TD \= [_],R="taxpayer_known_date_count_not_one");
          (DD=[DDate],TD=[TDate],
           \+ (user:is_before(TDate,DDate),\+ user:is_before(DDate,TDate)),
           R="taxpayer_date_not_strictly_before_dependent")
      ),Reasons),
      (Reasons == [] -> Allowed=true ; Allowed=false)
    ).

probe(Name,Goal,Limit, _{name:Name,inference_limit:Limit,result:Status}) :-
    catch((call_with_inference_limit(once(Goal),Limit,R) ->
             (R == inference_limit_exceeded -> Status="inference_limit_exceeded" ; Status="success")
           ; Status="failure"), E, term_string(E,Status,[quoted(true)])).

witness_probes(witness, Results) :- !,
    probe("finite_marriage_prefix",user:s7703_a(a,_,_,2018),100000,P),
    probe("age_a_b",user:s152_c_3(a,b,2018),100000,A),
    probe("age_b_a",user:s152_c_3(b,a,2018),100000,B),
    probe("s7703_a_100k",user:s7703(a,_,_,2018),100000,C),
    probe("s7703_a_1m",user:s7703(a,_,_,2018),1000000,D),
    Results=[P,A,B,C,D].
witness_probes(_, []).

prefix_solution_text(T,S) :- copy_term(T,C),numbervars(C,0,_),
    term_string(C,S,[quoted(true),numbervars(true),ignore_ops(true)]).
witness_prefix(witness,Persons,Edges,Solutions) :- !,
    findall(prefix(T,D,S,E),
            (member(T,Persons),member(D,Persons),
             user:s152_c_1_A(D,T,S,E),
             user:s152_c_1_B(D,_,T,S,E,2018),
             user:s152_c_1_C(D,T,2018)),Raw),
    maplist(prefix_solution_text,Raw,Solutions),
    findall([T,D],member(prefix(T,D,_,_),Raw),Pairs),sort(Pairs,Unique),
    maplist(pair_text,Unique,Edges).
witness_prefix(_,_,[],[]).

audit(Terms,Clauses,Skipped,Counts,Kind, Result) :-
    domain(Terms,Persons,Events), texts(Persons,PersonTexts),
    findall(E,user:birth_(E),Births), maplist(birth_record,Births,BirthRows),
    findall([Taxp,Dep], (member(Taxp,Persons),member(Dep,Persons),
                        once(user:s152_c_2(Dep,Taxp,_,_))), K),
    maplist(pair_text,K,KTexts),
    maplist(edge_age_record,K,AgeRows),
    findall([Child,Parent],user:is_child_of(Child,Parent,_,_),ParentRaw),
    sort(ParentRaw,ParentPairs), maplist(pair_text,ParentPairs,ParentTexts),
    findall([P,Q,D],(known_birth(P,D),known_birth(Q,D),P @< Q),EqualRaw),
    sort(EqualRaw,EqualPairs),maplist(equal_birth_record,EqualPairs,EqualRows),
    findall(S,(member(C,Clauses),clause_head(C,H),functor(H,N,_),
               member(N,[s152_c_2,s152_c_3]),
               term_string(C,S,[quoted(true),numbervars(true)])),Stipulations),
    findall(S,(member(T,Skipped),term_string(T,S,[quoted(true),numbervars(true)])),SkippedTexts),
    length(Clauses,ClauseCount),length(Events,EventSolutions),
    length(Persons,DomainCount),Pairs is DomainCount*DomainCount,
    witness_probes(Kind,Probes),
    witness_prefix(Kind,Persons,PrefixEdges,PrefixSolutions),
    Result=_{status:ok,clause_count:ClauseCount,loaded_clause_counts:Counts,unary_event_solutions:EventSolutions,
             domain:PersonTexts,domain_count:DomainCount,k_pairs_tested:Pairs,
             births:BirthRows,equal_birth_pairs:EqualRows,k_edges:KTexts,
             k_age_checks:AgeRows,
             child_parent_edges:ParentTexts,stipulated_c2_c3:Stipulations,
             skipped_directives:SkippedTexts,witness_probes:Probes,
             witness_c1_prefix_edges_2018:PrefixEdges,
             witness_c1_prefix_solutions_2018:PrefixSolutions}.

run(Path,Offset,Kind,Result) :-
    source_terms(Path,Offset,Terms), install(Terms,Clauses,Skipped,Counts),
    call_with_inference_limit(audit(Terms,Clauses,Skipped,Counts,Kind,Data),500000000,R),
    ( R == inference_limit_exceeded -> Result=_{status:inference_limit_exceeded}
    ; Result=Data ).

main :-
    current_prolog_flag(argv,[Path,OffsetAtom,Kind]),atom_number(OffsetAtom,Offset),
    catch((run(Path,Offset,Kind,Data) -> Result=Data ; Result=_{status:failed}),
          E,(term_string(E,Error,[quoted(true)]),Result=_{status:error,error:Error})),
    json_write_dict(current_output,Result,[width(0)]),nl,halt.
