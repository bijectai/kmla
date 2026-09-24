educational_institution_(hopkins_is_a_university).
agent_(hopkins_is_a_university,"johns hopkins university").
marriage_(bob_and_alice).
agent_(bob_and_alice,bob).
agent_(bob_and_alice,alice).
service_(bob_employed).
patient_(bob_employed,"johns hopkins university").
agent_(bob_employed,bob).
start_(bob_employed,"2017-01-01").
end_(bob_employed,"2017-12-31").
location_(bob_employed,baltimore).
location_(bob_employed,maryland).
location_(bob_employed,usa).
payment_(bob_is_paid).
agent_(bob_is_paid,"johns hopkins university").
patient_(bob_is_paid,bob).
start_(bob_is_paid,"2017-12-31").
purpose_(bob_is_paid,bob_employed).
amount_(bob_is_paid,3200).
enrollment_(alice_goes_to_hopkins).
agent_(alice_goes_to_hopkins,alice).
patient_(alice_goes_to_hopkins,"johns hopkins university").
start_(alice_goes_to_hopkins,"2015-08-29").
end_(alice_goes_to_hopkins,"2019-05-30").
attending_classes_(alice_goes_to_class).
agent_(alice_goes_to_class,alice).
location_(alice_goes_to_class,"johns hopkins university").
start_(alice_goes_to_class,"2015-08-29").
end_(alice_goes_to_class,"2019-05-30").
