% Diagnostic only: print exact stipulated solutions before the unchanged encoder.
:- consult('/harness/grounding.pl').

probe :- catch(run_probe, E, (print_message(error,E),halt(2))), halt(0).
run_probe :-
    current_prolog_flag(argv,[Input,Registry]),
    consult(Registry),
    setup_call_cleanup(open(Input,read,S,[encoding(utf8)]),read_clauses(S,C),close(S)),
    declare_heads(C), consult('/corpus/statutes/prolog/init.pl'), install(C,1,Refs),
    findall(H,stipulated_solution(Refs,H),Heads),
    numbervars(Heads,0,_),
    forall(member(H,Heads), (write('stipulated_head='),write_canonical(H),nl)),
    flush_output,
    encode_stips(Heads,_).
