"""Fail-closed dispatch tests: no new H6 roles, modes or production mocks."""
import unittest
from unittest.mock import patch

from harness.case_reader import parse_case, read_case
from harness.grounding import CORPUS, GroundingFailure, Measurement
from harness.grounding_observations import MODES
from scripts.test_grounding import ObservationPlan, compare_observations, observation_plan


def case(goal):
    return parse_case(("% Test\n:- " + goal + ".\n").encode())


class DispatchTests(unittest.TestCase):
    def test_reuses_exact_six_modes(self):
        goals = ["s3306_c_A(e,_,_)", "s3306_c_B(e,_,_,_)", r"\+ s3306_c_B(_,alice,bob,_)",
                 "s3306_c_1(e,2017)", "s3306_c_1_A_i(alice,_,[bob],_,2017)", "s3306_c_1_B(e,_)"]
        plans = [observation_plan(case(g)) for g in goals]
        self.assertTrue(all(p.kind == "paragraph" for p in plans))
        self.assertEqual({(p.query.predicate,p.query.mode) for p in plans},
                         MODES - {("s2_a_1_B", "bffb"), ("s63_d_2", "bbb")})

    def test_unknown_mismatched_arity_and_bound_modes_do_not_dispatch(self):
        for goal in ("s151_a(alice,4000,2015)", "s3306_c_A(e,alice,bob)", "s3306_c_A(e,_)",
                     "s3306_c_A(e,_,_,_)", "s3306_c_B(e,alice,_,_)", "s3306_c_A(X,Y,Z)"):
            with self.subTest(goal=goal):
                plan = observation_plan(case(goal))
                self.assertEqual(plan.kind, "unimplemented")
                self.assertIsNone(plan.query)
                with patch("scripts.test_grounding.observe", side_effect=AssertionError("must not run")):
                    result = compare_observations(None,plan,None,None,name="unit",timeout=1)
                self.assertTrue(result["status"].startswith("unimplemented:"))
                self.assertFalse(result["owner_choice_blocker"])

    def test_extra_constraints_not_stripped(self):
        plan = observation_plan(case("(s3306_c_A(e,X,Y),X=alice)"))
        self.assertEqual(plan.kind, "unimplemented")
        self.assertIsNone(plan.query)

    def test_multiple_goals_do_not_select_one(self):
        source = parse_case(b"% Test\n:- s3306_c_A(e,_,_).\n:- s3306_c_1(e,2017).\n")
        self.assertEqual(observation_plan(source).kind, "unimplemented")

    def test_original_input_projection_and_naf_preserved(self):
        positive = observation_plan(read_case(CORPUS / "cases/s3306_c_1_A_i_pos.pl")).query
        negative = observation_plan(read_case(CORPUS / "cases/s3306_c_1_A_i_neg.pl")).query
        self.assertIn("['bob']", positive.goal)
        self.assertIn(",'bob',", negative.goal)
        self.assertEqual(positive.outputs, ("Q0","Q1"))
        self.assertTrue(negative.outer_naf)

    def test_tax_unbound_amount_still_scalar_not_paragraph(self):
        plan = observation_plan(case("tax(alice,2015,27181)"))
        self.assertEqual(plan.kind, "tax_first_solution")
        self.assertEqual(plan.tax_input, "tax_inputs('alice',2015)")
        self.assertIsNone(plan.query)

    def test_tax_bad_input_mode_has_no_fallback(self):
        for goal in ("tax(alice,Y,27181)", "tax(P,2015,27181)"):
            with self.subTest(goal=goal), self.assertRaises(GroundingFailure):
                observation_plan(case(goal))

    def test_scalar_comparison_uses_recorded_first_solution(self):
        plan = observation_plan(case("tax(alice,2015,27181)"))
        left = Measurement(None,{"tax":{"status":"first_solution","value":3}},"unit-left")
        right = Measurement(None,{"tax":{"status":"first_solution","value":4}},"unit-right")
        with patch("scripts.test_grounding.observe", side_effect=AssertionError("never findall tax")):
            self.assertEqual(compare_observations(None,plan,left,right,name="unit",timeout=1)["status"], "fail")

    def test_unknown_dispatch_variant_is_error_not_empty_answer(self):
        for plan in (ObservationPlan("guessed"), ObservationPlan("paragraph"), ObservationPlan("tax_first_solution")):
            with self.subTest(plan=plan), self.assertRaises(GroundingFailure):
                compare_observations(None,plan,None,None,name="unit",timeout=1)

    def test_paragraph_comparison_is_complete_canonical_output(self):
        plan = observation_plan(case("s3306_c_A(e,_,_)"))
        before = {"canonical":[[{"a":"alice"},{"a":"bob"}]]}
        after = {"canonical":[]}
        with patch("scripts.test_grounding.observe", side_effect=[before,after]) as run:
            result = compare_observations(None,plan,None,None,name="unit",timeout=1)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(run.call_count, 2)
        self.assertEqual(result["original"], before)
        self.assertEqual(result["serialized"], after)


if __name__ == "__main__":
    unittest.main()
