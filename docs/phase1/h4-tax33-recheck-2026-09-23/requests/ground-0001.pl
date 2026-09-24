marriage_(alice_and_bob).
agent_(alice_and_bob,alice).
agent_(alice_and_bob,bob).
start_(alice_and_bob,"1992-02-03").
service_(Service_event) :- between(1,87,Employee_id),
    atom_concat("workforalice_2015_",Employee_id,Service_event).
agent_(Service_event,Employee) :- split_string(Service_event,"_","",[X,Y,Z]),
    X=="workforalice", Y=="2015",
    atom_concat('employee_2015_',Z,Employee).
patient_(Service_event,alice) :- split_string(Service_event,"_","",[X,_,_]),
    X=="workforalice".
start_(Service_event,"2015-01-01") :-
    split_string(Service_event,"_","",[X,Y,_]),
    X=="workforalice", Y=="2015".
end_(Service_event,"2015-12-31") :-
    split_string(Service_event,"_","",[X,Y,_]),
    X=="workforalice", Y=="2015".
payment_(Payment_event) :- between(1,87,Employee_id),
    atom_concat('payment_2015_',Employee_id,Payment_event).
agent_(Payment_event,alice) :- split_string(Payment_event,"_","",[X,_,_]), X=="payment".
purpose_(Payment_event,Service_event) :- split_string(Payment_event,"_","",[Xp,Yp,Zp]),
    split_string(Service_event,"_","",[Xs,Ys,Zs]),
    Xp=="payment",Xs=="workforalice",Yp==Ys,Zp==Zs.
amount_(Payment_event,5207) :- split_string(Payment_event,"_","",[X,Y,_]),
    X=="payment", Y=="2015".
patient_(Payment_event,Employee) :- split_string(Payment_event,"_","",[X,Y,Z]),
    atom_number(Z,Employee_id),
    X=="payment", Y=="2015", between(1,87,Employee_id),
    atom_concat("employee_2015_",Z,Employee).
start_(Payment_event,"2015-12-31") :- split_string(Payment_event,"_","",[X,Y,_]),
    X=="payment", Y=="2015".
service_(Service_event) :- between(1,70,Employee_id),
    atom_concat("workforalice_2016_",Employee_id,Service_event).
agent_(Service_event,Employee) :- split_string(Service_event,"_","",[X,Y,Z]),
    X=="workforalice", Y=="2016",
    atom_concat('employee_2016_',Z,Employee).
start_(Service_event,"2016-01-01") :-
    split_string(Service_event,"_","",[X,Y,_]),
    X=="workforalice", Y=="2016".
end_(Service_event,"2016-12-31") :-
    split_string(Service_event,"_","",[X,Y,_]),
    X=="workforalice", Y=="2016".
payment_(Payment_event) :- between(1,70,Employee_id),
    atom_concat('payment_2016_',Employee_id,Payment_event).
amount_(Payment_event,6341) :- split_string(Payment_event,"_","",[X,Y,_]),
    X=="payment", Y=="2016".
patient_(Payment_event,Employee) :- split_string(Payment_event,"_","",[X,Y,Z]),
    atom_number(Z,Employee_id),
    X=="payment", Y=="2016", between(1,70,Employee_id),
    atom_concat("employee_2016_",Z,Employee).
start_(Payment_event,"2016-12-31") :- split_string(Payment_event,"_","",[X,Y,_]),
    X=="payment", Y=="2016".
joint_return_(alice_and_bob_joint_return).
agent_(alice_and_bob_joint_return,alice).
agent_(alice_and_bob_joint_return,bob).
start_(alice_and_bob_joint_return,"2015-01-01").
end_(alice_and_bob_joint_return,"2015-12-31").
