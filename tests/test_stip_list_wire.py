"""Shared declarative fixture checks; no lane codec or Prolog execution.

json.dumps below checks standard JSON spelling of an already declared JSON
value. This file implements no Household encoder/decoder or semantic admission.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEGACY_WIRE_SHA256 = {
    "empty": "2ed1ddea16e3e469333cf76db848d9f00ee8521bd1713962b33edbbb8210cae0",
    "tags_order_integers": "3748cd7efdb7f226c43a3e63e6967f35c9b3836d40540083abaf78a77d1908c1",
    "controls_unicode": "f9a5a1131b7b705a0e34360e2ce16916f3e955f7d6b5004720368db1cc91b41c",
    "dates_and_tagged_patterns": "b347632aa592c1ebfca37372a0057eff451880290bd922180b2be11ff931455c",
    "wildcard_identity": "8f783f31ab3f2774ea3c34e1618aaeab98f4ac51a761ec5ad1aeb5752566819a",
    "opaque_helpers_extra_arities": "5e4ba9ca19cceaf5051c8287cc68a219b3bcfe642e41063be0bcceb9a0bfab5e",
}


def unique_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise AssertionError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


class StipListWireTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(
            (ROOT / "Interface/fixtures/household_wire.json").read_text(),
            object_pairs_hook=unique_keys,
        )["cases"]
        cls.by_name = {case["name"]: case for case in cls.cases}

    def test_legacy_wire_bytes_are_unchanged(self):
        self.assertEqual([c["name"] for c in self.cases[:6]], list(LEGACY_WIRE_SHA256))
        for name, expected in LEGACY_WIRE_SHA256.items():
            with self.subTest(name=name):
                raw = self.by_name[name]["wire"].encode("utf-8")
                self.assertEqual(hashlib.sha256(raw).hexdigest(), expected)

    def test_all_declared_values_match_exact_wire_bytes(self):
        self.assertEqual(len(self.cases), 8)
        self.assertEqual(len(self.by_name), 8)
        for case in self.cases:
            with self.subTest(name=case["name"]):
                wire = case["wire"]
                self.assertFalse(wire.startswith("\ufeff"))
                self.assertFalse(wire.endswith("\n"))
                self.assertEqual(
                    json.loads(wire, object_pairs_hook=unique_keys), case["household"]
                )
                self.assertEqual(
                    json.dumps(case["household"], ensure_ascii=False, separators=(",", ":")),
                    wire,
                )

    def check_declared_argument(self, arg):
        # Fixture-shape assertion only; not a reusable production decoder.
        self.assertIs(type(arg), dict)
        self.assertEqual(len(arg), 1)
        key = next(iter(arg))
        self.assertIn(key, ("val", "wild", "list"))
        if key == "list":
            self.assertIs(type(arg[key]), list)
            for item in arg[key]:
                self.check_declared_argument(item)
        elif key == "wild":
            self.assertIs(type(arg[key]), int)
            self.assertGreaterEqual(arg[key], 0)
        elif type(arg[key]) is not int:
            self.assertIs(type(arg[key]), dict)
            self.assertEqual(len(arg[key]), 1)
            tag = next(iter(arg[key]))
            self.assertIn(tag, ("a", "s"))
            self.assertIs(type(arg[key][tag]), str)

    def test_stipulations_use_declared_arities_and_recursive_tags(self):
        source = (ROOT / "Interface/Household.lean").read_text()
        arity_block = source.split("def StipPred.arity", 1)[1].split("structure Stip where", 1)[0]
        arities = dict(
            (name, int(arity))
            for name, arity in re.findall(r"^  \| \.(\w+) => (\d+)$", arity_block, re.M)
        )
        self.assertEqual(len(arities), 31)
        for case in self.cases:
            with self.subTest(name=case["name"]):
                self.assertEqual(list(case["household"]), ["facts", "stipulations"])
                for stip in case["household"]["stipulations"]:
                    self.assertEqual(list(stip), ["pred", "args"])
                    self.assertEqual(len(stip["args"]), arities[stip["pred"]])
                    for arg in stip["args"]:
                        self.check_declared_argument(arg)

    def test_original_s151_shapes_from_q022(self):
        # Exact heads cited in Q-022; no corpus-wide or ValidStip assertion.
        heads = self.by_name["supplied_s151_lists"]["household"]["stipulations"]
        self.assertEqual(len(heads), 5)
        for ident, year in enumerate(range(2014, 2018)):
            self.assertEqual(heads[ident], {
                "pred": "s151_5",
                "args": [
                    {"val": {"a": "bob"}}, {"wild": ident},
                    {"list": [{"val": {"a": "charlie"}}]},
                    {"list": [{"val": 0}]}, {"val": year},
                ],
            })
        self.assertEqual(heads[4], {
            "pred": "s151_5",
            "args": [
                {"val": {"a": "alice"}}, {"val": 2000},
                {"list": [{"val": {"a": "alice"}}]}, {"wild": 4}, {"val": 2017},
            ],
        })

    def test_nested_identity_tags_precision_order_and_multiplicity(self):
        args = self.by_name["recursive_lists_shared_ids"]["household"]["stipulations"][0]["args"]
        self.assertEqual(args[:3], [
            {"wild": 0},
            {"list": [{"wild": 0}, {"wild": 1}, {"list": [{"wild": 1}]}]},
            {"wild": 1},
        ])
        self.assertEqual(args[3], {"list": [
            {"list": []}, {"val": {"a": "[]"}}, {"val": {"s": "[]"}},
            {"val": {"a": "usa"}}, {"val": {"s": "usa"}},
            {"val": 123456789012345678901234567890},
            {"val": -123456789012345678901234567890},
            {"val": {"a": "dup"}}, {"val": {"a": "dup"}},
        ]})
        self.assertEqual(args[4], {"val": 2015})
        self.assertIs(type(args[3]["list"][5]["val"]), int)


if __name__ == "__main__":
    unittest.main()
