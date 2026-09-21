#!/usr/bin/env python3
"""Pure lexical reader tests; --accounting prints every original case to stdout.

Run with python3 -B. No Prolog process, oracle, meter, or protected writes.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.case_reader import CaseReaderError, parse_case, read_case

CASES = ROOT / "human/sara/sara/cases"
SPLITS = ROOT / "human/sara/sara/splits"


def bare(node):
    while node.tag == "group":
        node = node.args[0]
    return node


def shape(node):
    """Syntax-only shorthand for readable precedence assertions."""
    return (node.tag, node.value, tuple(shape(n) for n in node.args))


def inventory(programs):
    """Reader accounting only; does not classify target modes or statute meaning."""
    rows = []
    for program in programs:
        kinds = Counter(s.kind for s in program.statements)
        roles = Counter(d.role for d in program.directives)
        rows.append({
            "id": Path(program.source.name).stem,
            "sha256": program.source.sha256,
            "bytes": len(program.source.original),
            "facts": kinds["fact"], "rules": kinds["rule"],
            "loads": roles["load"], "declarations": roles["declaration"],
            "queries": roles["query"], "halts": roles["halt"], "other": roles["other"],
            "reader_edits": len(program.source.edits),
        })
    totals = {key: sum(row[key] for row in rows) for key in rows[0] if key not in ("id", "sha256")}
    totals["cases"] = len(rows)
    totals["cases_with_rules"] = sum(row["rules"] > 0 for row in rows)
    identities = "".join(f"{row['id']}.pl\t{row['sha256']}\n" for row in sorted(rows, key=lambda r: r["id"]))
    return {"claim": "lexical reader accounting only; no execution, grounding, round-trip or parity",
            "source_inventory_sha256": sha256(identities.encode("utf-8")).hexdigest(),
            "totals": totals, "cases": rows}


class SyntaxTests(unittest.TestCase):
    def parse(self, text):
        return parse_case(text.encode("utf-8"))

    def test_literal_tags_and_exact_spelling(self):
        p = self.parse('p(usa,"usa",\'usa\',123,"2017-01-01","café").\n')
        args = p.clauses[0].head.args
        self.assertEqual([(a.tag, a.value) for a in args],
                         [("atom", "usa"), ("str", "usa"), ("atom", "usa"),
                          ("int", 123), ("str", "2017-01-01"), ("str", "café")])
        self.assertEqual(p.original_text(args[2]), "'usa'")
        self.assertEqual(p.original_text(args[5]), '"café"')
        self.assertEqual(p.clause_texts(), (p.source.original.decode().rstrip(),))

    def test_lexemes_partition_bytes_including_comments_and_crlf(self):
        text = '% Text\r\n% café :- p(x).\r\np("% Test . :-",\'a.b\'). % final\r\n'
        p = self.parse(text)
        self.assertEqual("".join(t.lexeme for t in p.tokens).encode(), p.source.original)
        self.assertEqual(len(p.clauses), 1)
        self.assertEqual(p.queries, ())
        self.assertEqual([e.label for e in p.evidence], ["Text"])

    def test_named_variable_identity_and_anonymous_freshness(self):
        p = self.parse("p(X,X,_,_,_Name) :- q(X,_Name,_).\np(X).\n")
        first, second = p.clauses
        args = first.head.args
        self.assertIs(args[0].value, args[1].value)
        self.assertIs(args[0].value, first.body.args[0].value)
        self.assertIs(args[4].value, first.body.args[1].value)
        self.assertNotEqual(args[2].value, args[3].value)
        self.assertNotEqual(args[3].value, first.body.args[2].value)
        self.assertNotEqual(args[0].value, second.head.args[0].value)
        self.assertEqual([v.name for v in first.variables], ["X", "_", "_", "_Name", "_"])

    def test_same_named_variable_different_source_identity(self):
        a = parse_case(b"p(X).", source_name="a.pl")
        b = parse_case(b"p(X).", source_name="b.pl")
        c = parse_case(b"p(X).\n", source_name="a.pl")
        self.assertNotEqual(a.clauses[0].variables[0], b.clauses[0].variables[0])
        self.assertNotEqual(a.clauses[0].variables[0], c.clauses[0].variables[0])

    def test_comma_semicolon_and_if_then_precedence(self):
        body = self.parse("p :- a,b -> c,d ; e,f.\n").clauses[0].body
        atom = lambda x: ("atom", x, ())
        op = lambda x, a, b: ("op", x, (a, b))
        self.assertEqual(shape(body), op(";", op("->", op(",", atom("a"), atom("b")),
                                                       op(",", atom("c"), atom("d"))),
                                               op(",", atom("e"), atom("f"))))
        body = self.parse("p :- a,b,c.\n").clauses[0].body
        self.assertEqual(body.args[1].value, ",")

    def test_naf_scope_and_parentheses_are_retained(self):
        body = self.parse("p :- \\+ X == a, q(X).\n").clauses[0].body
        self.assertEqual(body.value, ",")
        self.assertEqual(body.args[0].value, "\\+")
        self.assertEqual(body.args[0].args[0].value, "==")
        body = self.parse("p :- \\+ (a,b).\n").clauses[0].body
        self.assertEqual(body.args[0].tag, "group")
        self.assertEqual(body.args[0].args[0].value, ",")

    def test_lists_tuples_and_argument_separators(self):
        p = self.parse("p([a,b],[],(X,Y),f(z)).\n")
        a, b, c, d = p.clauses[0].head.args
        self.assertEqual([n.value for n in a.args], ["a", "b"])
        self.assertEqual(b.tag, "list")
        self.assertEqual(b.args, ())
        self.assertEqual(c.tag, "group")
        self.assertEqual(c.args[0].value, ",")
        self.assertEqual(d.tag, "compound")

    def test_quoted_operator_is_an_atom(self):
        p = self.parse("p('==',';','/','discontiguous').")
        self.assertEqual([n.tag for n in p.clauses[0].head.args], ["atom"] * 4)

    def test_no_directive_leaks_to_clause_slices(self):
        text = ("% Question\n% Answer is 10.\n% Facts\n"
                ":- discontiguous p/1.\n:- [statutes/prolog/init].\n"
                "p(a).\np(a).\np(X) :- q(X).\n"
                "% Test\n:- \\+ (p(X),q(X)).\n:- halt.\n")
        p = self.parse(text)
        self.assertEqual(p.clause_texts(), ("p(a).", "p(a).", "p(X) :- q(X)."))
        self.assertEqual([d.role for d in p.directives], ["declaration", "load", "query", "halt"])
        self.assertEqual(p.original_text(p.evidence[0]), "% Question\n% Answer is 10.\n")
        self.assertEqual(p.original_text(p.evidence[-1]), "% Test\n:- \\+ (p(X),q(X)).\n:- halt.\n")
        query = p.queries[0].goal
        self.assertEqual(query.value, "\\+")
        conjunction = bare(query.args[0])
        self.assertIs(conjunction.args[0].args[0].value, conjunction.args[1].args[0].value)
        self.assertNotEqual(conjunction.args[0].args[0].value, p.clauses[-1].head.args[0].value)
        path = p.directives[1].goal.args[0]
        self.assertEqual(path.value, "/")
        self.assertEqual(path.args[0].value, "/")

    def test_preserves_duplicate_directives_and_unknown_roles(self):
        p = self.parse(":- [init].\n:- [init].\n:- unknown(foo).\n")
        self.assertEqual([d.role for d in p.directives], ["load", "load", "other"])
        self.assertEqual([s.index for s in p.statements], [0, 1, 2])
        self.assertEqual(p.clause_texts(), ())

    def test_malformed_and_unsupported_syntax_is_never_skipped(self):
        for text in ("p(a)", "p(a)\nq(b).", "p(a).q(b).", "p(a,).", "p([a,]).",
                     'p("unterminated).', "p(X) :- X = Y = Z.", "p(a). garbage",
                     "p(1.2).", "p([a|T]).", 'p("a\\n").', "/* comment */ p(a).",
                     "p (a).", "p(X) :- X is 1+2."):
            with self.subTest(text=text), self.assertRaises(CaseReaderError):
                self.parse(text)

    def test_errors_use_original_source_location(self):
        with self.assertRaisesRegex(CaseReaderError, r"bad\.pl:3:1: expected \."):
            parse_case(b"% Text\np(a)\nq(b).", source_name="bad.pl")
        with self.assertRaisesRegex(CaseReaderError, "invalid UTF-8 at byte 0"):
            parse_case(b"\xff")


class OriginalCasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = sorted(CASES.glob("*.pl"))
        cls.programs = [read_case(path) for path in cls.paths]
        cls.by_id = {path.stem: p for path, p in zip(cls.paths, cls.programs)}

    def test_complete_376_population_and_train_test_coverage(self):
        self.assertEqual(len(self.paths), 376)
        train = (SPLITS / "train").read_text().splitlines()
        test = (SPLITS / "test").read_text().splitlines()
        self.assertEqual(len(train), 256)
        self.assertEqual(len(test), 120)
        self.assertEqual(len(set(train + test)), 376)
        self.assertEqual(set(train + test), set(self.by_id))

    def test_population_accounting_after_h44(self):
        self.assertEqual(inventory(self.programs)["totals"], {
            "bytes": 370212, "facts": 5344, "rules": 432, "loads": 378,
            "declarations": 218, "queries": 376, "halts": 376, "other": 0,
            "reader_edits": 2, "cases": 376, "cases_with_rules": 59,
        })

    def test_source_bytes_unchanged_after_reading(self):
        for path, p in zip(self.paths, self.programs):
            with self.subTest(case=path.name):
                self.assertEqual(path.read_bytes(), p.source.original)

    def test_all_cases_have_one_whole_query_and_preserved_evidence(self):
        for p in self.programs:
            with self.subTest(case=p.source.name):
                self.assertEqual([e.label for e in p.evidence], ["Text", "Question", "Facts", "Test"])
                self.assertEqual(len(p.queries), 1)
                self.assertEqual(sum(d.role == "halt" for d in p.directives), 1)
                self.assertFalse(any(d.role == "other" for d in p.directives))
                self.assertTrue(p.original_text(p.evidence[1]).startswith("% Question\n% "))
                self.assertIn(p.original_text(p.queries[0].statement), p.original_text(p.evidence[3]))

    def test_all_bytes_tokens_clauses_and_node_spans_accounted_for(self):
        for p in self.programs:
            with self.subTest(case=p.source.name):
                self.assertEqual("".join(t.lexeme for t in p.tokens).encode(), p.source.reader)
                self.assertEqual("".join(t.lexeme for t in p.tokens if not t.synthetic).encode(),
                                 p.source.original)
                self.assertEqual(len(p.clauses) + len(p.directives), len(p.statements))
                cursor = 0
                for t in p.tokens:
                    self.assertEqual(t.reader_span.start, cursor)
                    self.assertEqual(p.original_text(t), "" if t.synthetic else t.lexeme)
                    cursor = t.reader_span.end
                self.assertEqual(cursor, len(p.source.reader))
                for statement in p.statements:
                    for node in statement.ast.walk():
                        self.assertGreaterEqual(node.span.start, statement.span.start)
                        self.assertLessEqual(node.span.end, statement.span.end)
                        self.assertTrue(p.original_text(node))
                    original = p.original_text(statement)
                    self.assertEqual(p.reader_text(statement), original + (
                        "." if any(e.offset == statement.span.end for e in p.source.edits) else ""))

    def test_exactly_two_h44_edits_with_provenance(self):
        repaired = [p for p in self.programs if p.source.edits]
        self.assertEqual([Path(p.source.name).name for p in repaired],
                         ["s3306_c_2_neg.pl", "s3306_c_2_pos.pl"])
        for p in repaired:
            edit, = p.source.edits
            self.assertEqual(edit.line, 26)
            self.assertEqual(edit.inserted, b".")
            self.assertEqual(edit.source_sha256, sha256(p.source.original).hexdigest())
            self.assertEqual(p.source.original[:edit.offset].count(b"\n"), 25)
            self.assertEqual(p.source.reader[:edit.offset] + p.source.reader[edit.offset + 1:],
                             p.source.original)
            fact = p.clauses[-1]
            self.assertEqual(fact.kind, "fact")
            self.assertEqual(fact.head.value, "s3306_b")
            self.assertEqual(fact.span.end, edit.offset)
            self.assertEqual(p.source.location(p.queries[0].statement.span.start).rsplit(":", 2)[1:],
                             ["29", "1"])
            synthetic, = [t for t in p.tokens if t.synthetic]
            self.assertEqual(synthetic.span.start, edit.offset)

    def test_h44_does_not_repair_other_names_or_modified_sources(self):
        for suffix in ("neg", "pos"):
            p = self.by_id[f"s3306_c_2_{suffix}"]
            unpatched = parse_case(p.source.original, source_name="different.pl")
            self.assertEqual(unpatched.source.edits, ())
            self.assertEqual(unpatched.clauses[-1].kind, "rule")
            self.assertEqual(unpatched.queries, ())
            with self.assertRaisesRegex(CaseReaderError, "H4.4 source identity changed"):
                parse_case(p.source.original + b"\n", source_name=p.source.name)

    def test_duplicate_init_preserved(self):
        twice = [Path(p.source.name).stem for p in self.programs
                 if sum(d.role == "load" for d in p.directives) == 2]
        self.assertEqual(twice, ["tax_case_37", "tax_case_86"])

    def test_real_duplicate_fact_blocks_are_kept(self):
        for case in ("tax_case_16", "tax_case_41"):
            p = self.by_id[case]
            facts = [p.reader_text(s) for s in p.clauses if s.kind == "fact"]
            counts = Counter(facts)
            self.assertGreater(max(counts.values()), 1)
            self.assertEqual(len(facts), sum(counts.values()))

    def test_real_rule_text_reaches_handoff_unchanged(self):
        p = self.by_id["tax_case_33"]
        rule = next(s for s in p.clauses if s.head.value == "amount_" and s.kind == "rule")
        self.assertEqual(p.reader_text(rule), 'amount_(Payment_event,5207) :- '
                         'split_string(Payment_event,"_","",[X,Y,_]),\n'
                         '    X=="payment", Y=="2015".')
        self.assertIn(p.reader_text(rule), p.clause_texts())
        self.assertIs(rule.head.args[0].value, rule.body.args[0].args[0].value)

    def test_real_conjunctive_query_keeps_shared_variables_and_naf(self):
        for suffix in ("neg", "pos"):
            p = self.by_id[f"s152_d_2_D_{suffix}"]
            query = p.queries[0].goal
            if suffix == "neg":
                self.assertEqual(query.value, "\\+")
                query = bare(query.args[0])
            self.assertEqual(query.value, ",")
            nodes = list(query.walk())
            self.assertEqual([n.value for n in nodes if n.tag == "compound"],
                             ["s152_d_2_D", "var", "first_day_year", "is_before"])
            start = [n.value for n in nodes if n.tag == "var" and n.value.name == "Start_relationship"]
            self.assertEqual(len(start), 2)
            self.assertIs(start[0], start[1])

    def test_source_goal_not_filename_selects_query(self):
        p = self.by_id["s3306_c_10_A_i_pos"]
        q = p.queries[0].goal
        self.assertEqual(q.value, ",")
        self.assertEqual([n.value for n in q.args], ["s3306_c_10_A", "s3306_c_10_A_i"])

    def test_ground_answer_and_question_retained_without_output_projection(self):
        p = self.by_id["s151_a_pos"]
        self.assertEqual([a.value for a in p.queries[0].goal.args], ["alice", 4000, 2015])
        self.assertIn("4000", p.original_text(p.evidence[1]))
        self.assertFalse(hasattr(p.queries[0], "output_positions"))

    def test_original_wildcard_fact_is_a_variable_not_a_ground_value(self):
        for suffix in ("neg", "pos"):
            p = self.by_id[f"s3306_a_2_B_{suffix}"]
            fact = p.clauses[-1]
            self.assertEqual(fact.head.value, "purpose_")
            self.assertEqual(fact.head.args[0].tag, "var")
            self.assertEqual(fact.head.args[0].value.name, "_")
            self.assertEqual(fact.head.args[1].tag, "str")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accounting", action="store_true", help="print all case rows as JSON; no tests")
    args, rest = parser.parse_known_args()
    if args.accounting:
        if rest:
            parser.error(f"unexpected arguments: {rest}")
        print(json.dumps(inventory([read_case(path) for path in sorted(CASES.glob('*.pl'))]), indent=2))
    else:
        unittest.main(argv=[sys.argv[0], *rest])
