service_('alice_employer').
patient_('alice_employer','alice').
agent_('alice_employer','bob').
start_('alice_employer',"2017-02-01").
end_('alice_employer',"2017-09-02").
location_('alice_employer',"caracas, venezuela").
payment_('alice_pays').
agent_('alice_pays','alice').
patient_('alice_pays','bob').
start_('alice_pays',"2017-09-02").
purpose_('alice_pays','alice_employer').
amount_('alice_pays',3200).
citizenship_('alice_is_venezuelan').
agent_('alice_is_venezuelan','alice').
patient_('alice_is_venezuelan',"venezuela").
citizenship_('bob_is_american').
agent_('bob_is_american','bob').
patient_('bob_is_american',"usa").
