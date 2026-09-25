% Control for the G6 diagnostic: the candidate household without the
% "private home" location. Everything else is identical, so a difference in the
% root result isolates section3306.pl's domestic-location branch (:597-604).
service_(alice_domestic_service).
agent_(alice_domestic_service, bob).
patient_(alice_domestic_service, alice).
purpose_(alice_domestic_service, "domestic service").
location_(alice_domestic_service, "usa").
