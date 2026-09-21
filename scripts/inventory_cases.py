#!/usr/bin/env python3
"""Read the designated SARA case programs; emit a deterministic structural inventory.

Companion to `inventory_hazards.py`, which covers `statutes/prolog/` only. This
scanner covers `human/sara/sara/cases/` and answers the structural questions the
B005 blocker raises: how many clauses are facts, how many are rules, how many test
directives actually stand alone, and which asserted predicates no statute rule can
read.

No Prolog execution, no operator-precedence parsing, no translation, no file
writes. Clause splitting is full-stop detection outside comments and quoted
literals, which is exactly the property B005 turns on. Anything this scanner
cannot lex is raised, never silently skipped. Run with `python3 -B`.

Counting definitions are stated in the emitted JSON because the definitions are
themselves owner decisions; two defensible definitions give different totals.
"""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys


CASES = Path("human/sara/sara/cases")
STATUTES = Path("human/sara/sara/statutes/prolog")
NECK = ":-"
FUNCTOR = re.compile(r"([a-z][A-Za-z0-9_]*)\s*\(")
ATOM_HEAD = re.compile(r"^([a-z][A-Za-z0-9_]*)\s*(?:\(|$)")
NAMED_VARIABLE = re.compile(r"(?<![A-Za-z0-9_])[A-Z][A-Za-z0-9_]*")
ANY_VARIABLE = re.compile(r"(?<![A-Za-z0-9_])[A-Z_][A-Za-z0-9_]*")
DISCONTIGUOUS = re.compile(r"^discontiguous\s+([a-z][A-Za-z0-9_]*)\s*/\s*(\d+)$")


class InventoryError(ValueError):
    """A lexical condition the scanner refuses to guess about."""


class Clause:
    """One top-level term, with the text of quoted literals masked out."""

    __slots__ = ("line", "text", "masked")

    def __init__(self, line, text, masked):
        self.line = line
        self.text = " ".join(text.split())
        self.masked = " ".join(masked.split())

    @property
    def is_directive(self):
        return self.masked.startswith(NECK)

    @property
    def goal(self):
        return self.masked[len(NECK):].strip()

    def split_neck(self):
        """Return (head, body) using the first top-level neck outside brackets."""
        depth = 0
        index = 0
        while index < len(self.masked) - 1:
            char = self.masked[index]
            if char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
            elif depth == 0 and self.masked.startswith(NECK, index):
                return self.masked[:index].strip(), self.masked[index + len(NECK):].strip()
            index += 1
        return self.masked, None


def lex_clauses(source, origin):
    """Split a program into clauses at end-of-clause full stops.

    A full stop is a `.` followed by whitespace, a comment, or end of input, and
    outside any comment or quoted literal. Text left over after the last full stop
    is returned separately: that residue is precisely the B005 defect signature.
    """
    clauses = []
    raw = []
    masked = []
    index = 0
    line = 1
    clause_line = None
    length = len(source)

    while index < length:
        char = source[index]
        if char == "\n":
            line += 1
            raw.append(char)
            masked.append(char)
            index += 1
            continue
        if char == "%":
            end = source.find("\n", index)
            index = length if end < 0 else end
            continue
        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end < 0:
                raise InventoryError(f"{origin}:{line}: unterminated block comment")
            line += source.count("\n", index, end)
            index = end + 2
            continue
        if char in "'\"`":
            end = index + 1
            while end < length:
                if source[end] == "\\":
                    end += 2
                    continue
                if source[end] == char:
                    if end + 1 < length and source[end + 1] == char:
                        end += 2
                        continue
                    break
                end += 1
            else:
                raise InventoryError(f"{origin}:{line}: unterminated quoted literal")
            literal = source[index:end + 1]
            if clause_line is None:
                clause_line = line
            raw.append(literal)
            masked.append(char + "\x00" * (len(literal) - 2) + char)
            line += literal.count("\n")
            index = end + 1
            continue
        if char == "." and (index + 1 >= length or source[index + 1] in " \t\n\r%"):
            body = "".join(raw).strip()
            if body:
                clauses.append(Clause(clause_line or line, body, "".join(masked).strip()))
            raw, masked, clause_line = [], [], None
            index += 1
            continue
        if not char.isspace() and clause_line is None:
            clause_line = line
        raw.append(char)
        masked.append(char)
        index += 1

    residue = "".join(raw).strip()
    return clauses, (Clause(clause_line or line, residue, "".join(masked).strip()) if residue else None)


def functor_of(head):
    match = ATOM_HEAD.match(head.strip())
    return match.group(1) if match else None


def arity_of(head):
    """Count top-level arguments of a compound head; 0 for a bare atom."""
    head = head.strip()
    if not head.endswith(")"):
        return 0
    open_index = head.find("(")
    if open_index < 0:
        return 0
    depth = 0
    count = 1
    for char in head[open_index + 1:-1]:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            count += 1
    return count


def signature(head):
    name = functor_of(head)
    return None if name is None else f"{name}/{arity_of(head)}"


def called_signatures(body):
    """Yield name/arity for every compound goal-shaped term in a clause body.

    This is lexical: it cannot tell a call from a data term of the same shape,
    and it does not resolve meta-calls. It is used only to decide whether a
    signature is *never* mentioned, which is the safe direction for that claim.
    """
    found = []
    for match in FUNCTOR.finditer(body):
        name = match.group(1)
        depth = 0
        index = match.end() - 1
        while index < len(body):
            char = body[index]
            if char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
                if depth == 0:
                    break
            index += 1
        else:
            continue
        found.append(f"{name}/{arity_of(body[match.start():index + 1])}")
    return found


def statute_predicates(root):
    """Every predicate name a statute rule body can actually call, and every head."""
    heads = set()
    head_signatures = set()
    called = Counter()
    files = sorted((root / STATUTES).glob("*.pl"))
    if not files:
        raise InventoryError(f"no statute programs under {root / STATUTES}")
    for path in files:
        clauses, residue = lex_clauses(path.read_text(encoding="utf-8"), path.name)
        if residue is not None:
            raise InventoryError(f"{path.name}: unterminated final clause")
        for clause in clauses:
            if clause.is_directive:
                continue
            head, body = clause.split_neck()
            name = functor_of(head)
            if name:
                heads.add(name)
                head_signatures.add(signature(head))
            if body:
                for called_name in FUNCTOR.findall(body):
                    called[called_name] += 1
                for called_signature in called_signatures(body):
                    called[called_signature] += 1
    return heads, head_signatures, called


def scan(root):
    directory = root / CASES
    files = sorted(directory.glob("*.pl"))
    if not files:
        raise InventoryError(f"no case programs under {directory}")

    heads_defined, signatures_defined, called_in_statutes = statute_predicates(root)

    per_file = []
    totals = Counter()
    directive_kinds = Counter()
    fact_predicates = Counter()
    fact_signatures = Counter()
    rule_signatures = Counter()
    signature_files = defaultdict(set)
    rule_heads = Counter()
    rule_body_goals = Counter()
    unterminated = []
    without_test = []
    rules_extending_statutes = []
    anonymous_only_facts = []
    named_variable_facts = []
    shapes = Counter()

    for path in files:
        clauses, residue = lex_clauses(path.read_text(encoding="utf-8"), path.name)
        name = path.name
        counts = Counter()

        if residue is not None:
            unterminated.append({
                "file": f"{CASES}/{name}",
                "line": residue.line,
                "residue": residue.text,
            })

        for clause in clauses:
            if clause.is_directive:
                goal = clause.goal
                match = DISCONTIGUOUS.match(goal)
                if match:
                    kind = "discontiguous"
                elif goal.startswith("["):
                    kind = "consult"
                elif goal == "halt":
                    kind = "halt"
                else:
                    kind = "test"
                directive_kinds[kind] += 1
                counts[kind] += 1
                continue

            head, body = clause.split_neck()
            functor = functor_of(head)
            head_signature = signature(head)
            if head_signature:
                signature_files[head_signature].add(f"{CASES}/{name}")
            if body is None:
                counts["fact"] += 1
                if functor:
                    fact_predicates[functor] += 1
                if head_signature:
                    fact_signatures[head_signature] += 1
                if ANY_VARIABLE.search(clause.masked):
                    record = {"file": f"{CASES}/{name}", "line": clause.line, "clause": clause.text}
                    if NAMED_VARIABLE.search(clause.masked):
                        named_variable_facts.append(record)
                    else:
                        anonymous_only_facts.append(record)
            else:
                counts["rule"] += 1
                if head_signature:
                    rule_signatures[head_signature] += 1
                if functor:
                    rule_heads[functor] += 1
                    if functor in heads_defined:
                        rules_extending_statutes.append({
                            "file": f"{CASES}/{name}",
                            "line": clause.line,
                            "predicate": functor,
                            "clause": clause.text,
                        })
                for goal_name in FUNCTOR.findall(body):
                    rule_body_goals[goal_name] += 1
                for goal_signature in called_signatures(body):
                    rule_body_goals[goal_signature] += 1

        if not counts["test"]:
            without_test.append(f"{CASES}/{name}")
        shapes[
            f"consult={counts['consult']} discontiguous={counts['discontiguous']}"
            f" test={counts['test']} halt={counts['halt']}"
        ] += 1
        totals.update(counts)
        per_file.append({
            "file": f"{CASES}/{name}",
            "clauses": len(clauses),
            "facts": counts["fact"],
            "rules": counts["rule"],
            "test_directives": counts["test"],
            "consult_directives": counts["consult"],
            "unterminated_residue": residue is not None,
        })

    asserted_signatures = set(fact_signatures) | set(rule_signatures)
    unreadable = sorted(
        {
            item: {
                "asserted_as_facts": fact_signatures.get(item, 0),
                "asserted_as_rules": rule_signatures.get(item, 0),
                "called_by_case_rules": rule_body_goals.get(item, 0),
                "name_defined_by_statutes": item.split("/")[0] in heads_defined,
                "name_called_by_statutes": called_in_statutes.get(item.split("/")[0], 0),
                "signature_defined_by_statutes": item in signatures_defined,
                "files": sorted(signature_files.get(item, ())),
            }
            for item in asserted_signatures
            if called_in_statutes.get(item, 0) == 0
            and item not in signatures_defined
        }.items()
    )
    inert = {
        item: detail for item, detail in unreadable
        if detail["called_by_case_rules"] == 0
    }
    extending = sorted(
        {
            item: {
                "asserted_as_facts": fact_signatures.get(item, 0),
                "asserted_as_rules": rule_signatures.get(item, 0),
                "files": len(signature_files.get(item, ())),
            }
            for item in asserted_signatures if item in signatures_defined
        }.items()
    )

    return {
        "definitions": {
            "clause": "one top-level term ended by a full stop outside comments and quoted literals",
            "fact": "a non-directive clause with no top-level neck operator",
            "rule": "a non-directive clause with a top-level neck operator",
            "test_directive": "a directive that is not consult, halt, or discontiguous",
            "unterminated_residue": "text after the last full stop; the B005 defect signature",
            "variable_bearing_fact": "a fact whose masked text contains a variable token; "
                                    "anonymous-only and named-variable facts are counted separately "
                                    "because the distinction is an owner decision",
            "unreadable_signature": "a name/arity asserted by a case whose NAME is never called "
                                    "by a statute rule body and whose exact signature no statute "
                                    "program defines. Matching is by name/arity, because a name "
                                    "defined at one arity does not make another arity reachable. "
                                    "A lexical result, not a proof of runtime inertness",
            "inert_signature": "an unreadable signature that no case-file rule calls either, so "
                               "nothing in the loaded program can reach it",
            "extending_signature": "a name/arity a case asserts that a statute program also "
                                   "defines; these are the facts-only-ingestion population",
        },
        "summary": {
            "case_files": len(files),
            "clauses": sum(item["clauses"] for item in per_file),
            "facts": totals["fact"],
            "rules": totals["rule"],
            "directives": dict(sorted(directive_kinds.items())),
            "files_without_a_test_directive": len(without_test),
            "files_with_unterminated_residue": len(unterminated),
            "variable_bearing_facts_anonymous_only": len(anonymous_only_facts),
            "variable_bearing_facts_with_named_variables": len(named_variable_facts),
            "rule_clauses_extending_statute_predicates": len(rules_extending_statutes),
            "distinct_fact_predicates": len(fact_predicates),
            "distinct_rule_head_predicates": len(rule_heads),
            "unreadable_signatures": len(unreadable),
            "unreadable_clauses": sum(d["asserted_as_facts"] + d["asserted_as_rules"]
                                      for _, d in unreadable),
            "inert_signatures": len(inert),
            "inert_clauses": sum(d["asserted_as_facts"] + d["asserted_as_rules"]
                                 for d in inert.values()),
            "signatures_extending_statutes": len(extending),
            "clauses_extending_statutes": sum(d["asserted_as_facts"] + d["asserted_as_rules"]
                                              for _, d in extending),
            "files_extending_statutes": len({
                f for item, _ in extending for f in signature_files.get(item, ())
            }),
        },
        "unterminated_clauses": unterminated,
        "files_without_a_test_directive": without_test,
        "rules_extending_statute_predicates": rules_extending_statutes,
        "unreadable_signatures": dict(unreadable),
        "inert_signatures": inert,
        "signatures_extending_statutes": dict(extending),
        "variable_bearing_facts": {
            "anonymous_only": anonymous_only_facts,
            "named_variables": named_variable_facts,
        },
        "file_shapes": dict(sorted(shapes.items())),
        "fact_predicates": dict(sorted(fact_predicates.items())),
        "rule_head_predicates": dict(sorted(rule_heads.items())),
        "rule_body_goals": dict(sorted(rule_body_goals.items())),
        "per_file": per_file,
    }


def self_test():
    checks = []

    def expect(name, condition):
        checks.append((name, bool(condition)))

    clauses, residue = lex_clauses("a(1).\nb(2).\n", "t")
    expect("two terminated clauses", len(clauses) == 2 and residue is None)

    clauses, residue = lex_clauses('f("a.b").\n', "t")
    expect("full stop inside a quoted literal is not a terminator", len(clauses) == 1 and residue is None)

    clauses, residue = lex_clauses("a(1)\n% Test\n:- b(2).\n", "t")
    expect("B005 shape reads as one rule, not a fact plus a directive", len(clauses) == 1)
    expect("that clause is not a directive", clauses and not clauses[0].is_directive)
    head, body = clauses[0].split_neck()
    expect("its head is the unterminated fact", head.startswith("a(1)"))
    expect("its body is the apparent test", body == "b(2)")

    clauses, residue = lex_clauses("a(1).\nb(2)\n", "t")
    expect("trailing residue is reported", residue is not None and residue.text == "b(2)")

    clauses, _ = lex_clauses(":- discontiguous p/2.\n", "t")
    expect("directives are recognised", clauses[0].is_directive)
    expect("discontiguous is matched", DISCONTIGUOUS.match(clauses[0].goal) is not None)

    clauses, _ = lex_clauses("p(X) :- q(X), r(X).\n", "t")
    head, body = clauses[0].split_neck()
    expect("neck split finds head and body", head == "p(X)" and body == "q(X), r(X)")

    clauses, _ = lex_clauses("p(a) :- q(a ; b).\n", "t")
    expect("a neck inside brackets is not split on", clauses[0].split_neck()[0] == "p(a)")

    try:
        lex_clauses("p('unterminated).\n", "t")
    except InventoryError:
        expect("unterminated literals raise", True)
    else:
        expect("unterminated literals raise", False)

    try:
        lex_clauses("/* open\n", "t")
    except InventoryError:
        expect("unterminated block comments raise", True)
    else:
        expect("unterminated block comments raise", False)

    failures = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'ok  ' if passed else 'FAIL'}  {name}")
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    return 0 if not failures else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", default=".", help="repository root (default: the current directory)")
    parser.add_argument("--self-test", action="store_true", help="run the built-in lexer checks and exit")
    parser.add_argument("--summary", action="store_true", help="print only the summary object")
    arguments = parser.parse_args(argv)

    if arguments.self_test:
        return self_test()
    try:
        inventory = scan(Path(arguments.repo_root))
    except InventoryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    payload = inventory["summary"] if arguments.summary else inventory
    json.dump(payload, sys.stdout, indent=2, sort_keys=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
