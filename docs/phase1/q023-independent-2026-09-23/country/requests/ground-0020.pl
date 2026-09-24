service_('alice_employer').
patient_('alice_employer','alice').
agent_('alice_employer','bob').
start_('alice_employer',"2017-02-01").
end_('alice_employer',"2017-09-02").
location_('alice_employer',"stanley, wisconsin, usa").
country_("stanley, wisconsin, usa","usa").
purpose_('alice_employer',"agricultural labor").
payment_('alice_pays').
agent_('alice_pays','alice').
patient_('alice_pays','bob').
start_('alice_pays',"2017-09-02").
purpose_('alice_pays','alice_employer').
amount_('alice_pays',3200).
citizenship_('alice_is_american').
agent_('alice_is_american','alice').
patient_('alice_is_american',"usa").
citizenship_('bob_is_mexican').
agent_('bob_is_mexican','bob').
patient_('bob_is_mexican','mexico').
migration_('bob_migrates_to_usa').
destination_('bob_migrates_to_usa',"usa").
agent_('bob_migrates_to_usa','bob').
purpose_('bob_migrates_to_usa',"agricultural labor").
