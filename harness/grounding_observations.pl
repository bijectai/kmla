% Bounded H6 observations for country and list-stipulation paragraph slices.
% No expected-answer constraint, outer NAF, inferred output role or tax findall.
:- consult('/harness/grounding.pl').

observe_main :-
    catch(observe_run, Error, (print_message(error,Error), halt(2))), halt(0).

observe_run :-
    current_prolog_flag(argv,[Input,Query]),
    setup_call_cleanup(open(Input,read,S,[encoding(utf8)]),read_clauses(S,Clauses),close(S)),
    declare_heads(Clauses),
    consult('/corpus/statutes/prolog/init.pl'),
    install(Clauses,1,_),
    setup_call_cleanup(open(Query,read,Q,[encoding(utf8)]),
        ( read_term(Q,observation(Goal,Outputs),[syntax_errors(error)]),
          read_term(Q,End,[syntax_errors(error)]), End == end_of_file ),close(Q)),
    checked_observation(Goal,Outputs),
    statistics(cputime,T0), get_time(W0),
    findall(Outputs,Goal,Rows),
    statistics(cputime,T1), get_time(W1),
    observation_rows(Rows,JSON), length(Rows,N), CPU is T1-T0, Wall is W1-W0,
    json_write(current_output,json([raw_solutions=JSON,proof_count=N,
        cpu_seconds=CPU,wall_seconds=Wall])), nl.

approved_mode(s3306_c_A,[b,f,f]).
approved_mode(s3306_c_B,[b,f,f,f]).
approved_mode(s3306_c_B,[f,b,b,f]).
approved_mode(s3306_c_1,[b,b]).
approved_mode(s3306_c_1_A_i,[b,f,b,f,b]).
approved_mode(s3306_c_1_B,[b,f]).
approved_mode(s2_a_1_B,[b,f,f,b]).
% H6.5 bbb and the source Question asks applicability. The deduction list
% remains bound; no output amount is requested or released.
approved_mode(s63_d_2,[b,b,b]).

checked_observation(Goal,Outputs) :-
    ( nonvar(Goal), Goal =.. [P|Args], argument_mode(Args,Mode,Free),
      approved_mode(P,Mode), Outputs == Free -> true
    ; throw(error(unapproved_paragraph_observation,checked_observation/2)) ).
argument_mode([],[],[]).
argument_mode([H|T],[M|MT],Free) :-
    ( var(H) -> M=f, Free=[H|FT]
    ; ground(H) -> M=b, Free=FT
    ; throw(error(partially_bound_observation_argument,argument_mode/3)) ),
    argument_mode(T,MT,FT).

observation_rows([],[]).
observation_rows([H|T],[J|JT]) :-
    observation_values(H,J), observation_rows(T,JT).
observation_values([],[]).
observation_values([H|T],[J|JT]) :-
    observation_value(H,J), observation_values(T,JT).
% All free positions in these modes are Term / Int / lists thereof, not
% Day. An unexpected compound/improper list is an error, never a string cast.
observation_value(V,J) :-
    ( var(V) -> J = @(null)
    ; is_list(V) -> observation_values(V,J)
    ; term_json(V,J) ).
