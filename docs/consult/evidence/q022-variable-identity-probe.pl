% Non-production diagnostic for numbervars identity inside proper lists.
probe :-
    Term = sample(X,[X,Y,[Y]],Y),
    numbervars(Term,0,End),
    write_canonical(Term), nl,
    write('next_id='), write(End), nl,
    ( Term == sample('$VAR'(0),['$VAR'(0),'$VAR'(1),['$VAR'(1)]],'$VAR'(1)), End == 2
      -> halt(0) ; halt(1) ).
