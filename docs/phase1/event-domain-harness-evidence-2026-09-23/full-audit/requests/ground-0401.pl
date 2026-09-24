service_(alice_employer).
patient_(alice_employer,alice).
agent_(alice_employer,bob).
start_(alice_employer,"2017-02-01").
end_(alice_employer,"2017-09-02").
location_(alice_employer,baltimore).
location_(alice_employer,maryland).
location_(alice_employer,usa).
purpose_(alice_employer,"domestic service").
location_(alice_employer,"private home").
payment_(alice_pays).
agent_(alice_pays,alice).
patient_(alice_pays,bob).
start_(alice_pays,"2017-09-02").
purpose_(alice_pays,alice_employer).
amount_(alice_pays,300).
s3306_b(300,alice_pays,alice_employer,alice,bob,alice,bob,_).
