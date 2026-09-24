% Non-production diagnostic: preserve aliases within each findall solution,
% but freshen variables between ordered solution copies, including list tails.
probe :-
    findall(sample(X,[X,Y,[Y]],Y),member(_,[first,second]),Rows),
    numbervars(Rows,0,End), write_canonical(Rows), nl,
    write('next_id='), write(End), nl,
    Expected = [sample('$VAR'(0),['$VAR'(0),'$VAR'(1),['$VAR'(1)]],'$VAR'(1)),
                sample('$VAR'(2),['$VAR'(2),'$VAR'(3),['$VAR'(3)]],'$VAR'(3))],
    ( Rows == Expected, End == 4 -> halt(0) ; halt(1) ).
