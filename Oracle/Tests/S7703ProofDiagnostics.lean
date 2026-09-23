import Oracle.S7703

/-! Authorized resumed-round diagnostics. No production definitions or guards. -/
open KMLA KMLA.Oracle.S7703

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

#eval observe (a1Solutions (s7703_a_1_bfffb
  ⟨[.marriage_ (.atom "marriage"), .agent_ (.atom "marriage") (.atom "alice"),
    .agent_ (.atom "marriage") (.atom "bob")], []⟩ (.atom "alice") 2015))
#eval observe (b3Solutions (s7703_b_3_bfbb
  ⟨[.marriage_ (.atom "marriage"), .agent_ (.atom "marriage") (.atom "alice"),
    .agent_ (.atom "marriage") (.atom "bob"),
    .agent_ (.atom "marriage") (.atom "bob")], []⟩ (.atom "alice") (.atom "home") 2015))

example : (364 : Int) ≤ 2 * (min 16618 16800 - 16436) := by decide
example : escapeJson "bob" = "bob" := by rfl
example : escapeJson "bob" = "bob" := by decide
example : Obs.encode (.atom "bob") = "{\"a\":\"bob\"}" := by rfl
example : Obs.encode (.atom "bob") = "{\"a\":\"bob\"}" := by decide
example : Solution.encode [.atom "bob", .atom "marriage", .null] =
    "[{\"a\":\"bob\"},{\"a\":\"marriage\"},null]" := by rfl
example : Solution.encode [.atom "bob", .atom "marriage", .null] =
    "[{\"a\":\"bob\"},{\"a\":\"marriage\"},null]" := by decide
example : observe [[.atom "bob"]] = ["[{\"a\":\"bob\"}]"] := by rfl
example : observe [[.atom "bob"]] = ["[{\"a\":\"bob\"}]"] := by decide
example : observe [[.atom "bob"], [.atom "bob"]] = ["[{\"a\":\"bob\"}]"] := by rfl
example : observe [[.atom "bob"], [.atom "bob"]] = ["[{\"a\":\"bob\"}]"] := by decide
