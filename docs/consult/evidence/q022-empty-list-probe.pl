% Non-production diagnostic for proper-list versus scalar atom transport.
probe :-
    ( atom([]) -> write('atom_empty_list=true') ; write('atom_empty_list=false') ), nl,
    ( atom('[]') -> write('atom_quoted_brackets=true') ; write('atom_quoted_brackets=false') ), nl,
    ( [] == '[]' -> write('identical=true') ; write('identical=false') ), nl,
    write('bare='),write_canonical([]),nl,
    write('quoted='),write_canonical('[]'),nl,
    halt(0).
