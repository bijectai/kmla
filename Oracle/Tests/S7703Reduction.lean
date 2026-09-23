import Oracle.S7703

/-! Read-only reduction diagnostics retained for the proof-attempt record. -/

open KMLA KMLA.Oracle.S7703

#check String.foldl_eq_foldl_toList
#synth BEq Term
#print KMLA.instBEqTerm
#print KMLA.instBEqTerm.beq
