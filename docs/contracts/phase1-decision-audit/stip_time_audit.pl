% Read-only diagnostic, not a serializer or an oracle implementation.
:- module(stip_time_audit, [main/0]).
:- use_module('./birth_audit.pl', []).
:- use_module(library(http/json)).
:- use_module(library(lists)).

stipulated(H) :- functor(H,total_wages_employer,6), !.
stipulated(H) :- functor(H,N,_), atom_codes(N,[115,D|_]), D>=48, D=<57.

value(V, Vars, _{kind:"wild", value:I}) :- var(V), !,
    nth0(I,Vars,W), V==W, !.
value(V, _, _{kind:"int", value:V}) :- integer(V), !.
value(V, _, _{kind:"str", value:V}) :- string(V), !.
value(V, _, _{kind:"atom", value:S}) :- atom(V), !, atom_string(V,S).
value(V, _, _{kind:"other", value:S}) :- term_string(V,S,[quoted(true)]).

head_values(H, _{predicate:N, arity:A, args:Values}) :-
    H=..[Name|Args], atom_string(Name,N),length(Args,A),term_variables(H,Vars),
    maplist(value_with(Vars),Args,Values).
value_with(Vars,V,Out) :- value(V,Vars,Out).

solution((H :- B), H) :- !, call(user:B).
solution(H,H).
kind((_ :- _), "rule") :- !.
kind(_,"fact").

clause_record(C, _{kind:Kind,source:Text,solutions:Rows}) :-
    kind(C,Kind), birth_audit:prefix_solution_text(C,Text),
    findall(Row,(solution(C,H),head_values(H,Row)),Rows).

run(Path,Offset,Result) :-
    birth_audit:source_terms(Path,Offset,Terms),
    birth_audit:install(Terms,Clauses,_,Counts),
    findall(C,(member(C,Clauses),birth_audit:clause_head(C,H),stipulated(H)),Stips),
    call_with_inference_limit(maplist(clause_record,Stips,Rows),500000000,Status),
    ( Status==inference_limit_exceeded -> Result=_{status:"inference_limit_exceeded"}
    ; Result=_{status:"ok",clauses:Rows,loaded_clause_counts:Counts} ).

main :-
    current_prolog_flag(argv,[Path,OffsetAtom]),atom_number(OffsetAtom,Offset),
    catch((run(Path,Offset,Data) -> Result=Data ; Result=_{status:"failed"}),
          E,(term_string(E,Error,[quoted(true)]),Result=_{status:"error",error:Error})),
    json_write_dict(current_output,Result,[width(0)]),nl,halt.
