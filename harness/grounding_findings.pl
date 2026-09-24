% Minimal diagnostic of H6.5's explicit s3306_c_A/3 bff mode.
% Reuses loader plumbing only; never changes the measured grounder.
:- consult('/harness/grounding.pl').

country_probe :-
    catch(country_run, Error, (print_message(error, Error), halt(2))),
    halt(0).

country_run :-
    current_prolog_flag(argv,[Input]),
    setup_call_cleanup(open(Input,read,Stream,[encoding(utf8)]),
                       read_clauses(Stream,Clauses), close(Stream)),
    declare_heads(Clauses),
    consult('/corpus/statutes/prolog/init.pl'), install(Clauses,1,_),
    findall([Employer,Employee],s3306_c_A(alice_employer,Employer,Employee),Rows),
    country_rows(Rows,JSON), json_write(current_output,JSON), nl.

country_rows([],[]).
country_rows([[A,B]|T],[[JA,JB]|R]) :-
    term_json(A,JA), term_json(B,JB), country_rows(T,R).
