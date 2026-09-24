payment_(alice_is_paid).
patient_(alice_is_paid,alice).
start_(alice_is_paid,"2012-12-31").
amount_(alice_is_paid,54268).
service_(alice_employer).
patient_(alice_employer,alice).
agent_(alice_employer,bob).
start_(alice_employer,"2012-02-01").
end_(alice_employer,"2012-09-02").
location_(alice_employer,"caracas, venezuela").
country_("caracas, venezuela","venezuela").
payment_(alice_pays).
agent_(alice_pays,alice).
patient_(alice_pays,bob).
start_(alice_pays,"2012-09-02").
purpose_(alice_pays,alice_employer).
amount_(alice_pays,11571).
citizenship_(bob_is_american).
agent_(bob_is_american,bob).
patient_(bob_is_american,"usa").
