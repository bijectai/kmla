#!/usr/bin/env python3
"""Read the designated Prolog sources; emit a deterministic lexical inventory.

No Prolog execution, AST, operator-precedence parser, translation, or file writes.
Offsets are Unicode character offsets; lines/columns are one-based (a tab is one
character). Bracket balancing and top-level full stops supply review context,
not an interpretation of Prolog terms. Run with python3 -B to avoid bytecode.
"""

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


SOURCE = Path("human/sara/sara/statutes/prolog")
GRAPHIC = frozenset("#$&*+-./:<=>?@^~\\")
PAIRS = {"(": ")", "[": "]", "{": "}"}
SEPARATORS = {",", ";", ":-", "-->", "->", "*->", "."}
COMPARISONS = frozenset({
    "<", ">", "=<", ">=", "=:=", "=\\=", "=", "\\=", "==", "\\==",
    "@<", "@=<", "@>", "@>=", "=@=", "\\=@=", "?=", ":<", ">:<",
    "#<", "#>", "#=<", "#>=", "#=", "#\\=",
})
# Includes ordering, bounds, identity, unification, membership, and deduplication
# candidates. These names are review rules, not claims about builtin resolution.
COMPARISON_CALLS = frozenset({
    "compare", "dif", "between", "succ", "same_term", "unifiable",
    "subsumes_term", "subsumes_chk", "variant", "is_before", "is_after",
    "earliest", "latest", "sort", "msort", "keysort", "predsort",
    "min", "max", "min_list", "max_list", "member", "memberchk", "list_to_set",
    "atom_prefix", "sub_atom", "sub_string",
})
AGGREGATES = {"findall", "sumlist", "sum_list"}
ARITHMETIC = {
    "+", "-", "*", "/", "//", "div", "rdiv", "mod", "rem", "**", "^",
    "round", "ceil", "ceiling", "floor", "truncate", "rational", "rationalize",
    "float", "integer", "abs", "sign", "min", "max", "sqrt", "exp", "log",
}
VARIABLE = {"var", "nonvar", "ground", "nonground", "copy_term", "term_variables"}
DATE_SUPPORT = {
    "day_to_stamp", "duration", "date_time_stamp", "stamp_date_time", "date",
    "format_time", "parse_time", "first_day_year", "last_day_year",
}
LIST_SUPPORT = {"append", "length", "member", "memberchk", "list_to_set", "sort", "msort"}
META = {"call", "apply", "once", "ignore", "maplist", "include", "exclude",
        "forall", "catch", "throw", "op", "term_expansion", "goal_expansion"}
NUMBER = re.compile(r"(?:0[xX][0-9a-fA-F]+|0[oO][0-7]+|0[bB][01]+|[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)")


class InventoryError(ValueError):
    pass


@dataclass(frozen=True)
class Token:
    value: str
    kind: str
    start: int
    end: int


def lex(source):
    """Mask comments and quoted literals without searching inside them."""
    tokens = []
    excluded = Counter()
    i = 0
    while i < len(source):
        start = i
        char = source[i]
        if char.isspace():
            i += 1
            continue
        if char == "%":
            end = source.find("\n", i)
            i = len(source) if end < 0 else end
            excluded["line_comments"] += 1
            continue
        if source.startswith("/*", i):
            i += 2
            depth = 1
            while i < len(source) and depth:
                if source.startswith("/*", i):
                    depth += 1
                    i += 2
                elif source.startswith("*/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            if depth:
                raise InventoryError(f"unterminated block comment at offset {start}")
            excluded["block_comments"] += 1
            continue
        if source.startswith("{|", i):
            raise InventoryError(f"unsupported quasi quotation at offset {i}")
        if char in "'\"`":
            quote = char
            i += 1
            while i < len(source):
                if source[i] == "\\":
                    i += 2
                elif source[i] == quote:
                    if i + 1 < len(source) and source[i + 1] == quote:
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    i += 1
            else:
                raise InventoryError(f"unterminated quoted literal at offset {start}")
            tokens.append(Token(source[start:i], "literal", start, i))
            excluded[{"'": "quoted_atoms", '"': "double_quoted", "`": "backquoted"}[quote]] += 1
            continue
        if char.isdigit():
            match = NUMBER.match(source, i)
            i = match.end()
            if i < len(source) and source[i] == "'":
                raise InventoryError(f"unsupported character/base-number notation at offset {start}")
            kind = "number"
        elif char.isalpha() or char == "_":
            i += 1
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
            kind = "variable" if char.isupper() or char == "_" else "atom"
        elif char in GRAPHIC:
            # A terminating full stop is separate; decimal dots were consumed.
            if char == "." and (i + 1 == len(source) or source[i + 1].isspace()
                                or source[i + 1] == "%" or source.startswith("/*", i + 1)):
                i += 1
            else:
                i += 1
                while i < len(source) and source[i] in GRAPHIC:
                    if source.startswith("/*", i):
                        break
                    i += 1
            kind = "symbol"
        elif char in "()[]{},;!|":
            i += 1
            kind = "symbol"
        else:
            raise InventoryError(f"unsupported character {char!r} at offset {i}")
        tokens.append(Token(source[start:i], kind, start, i))
    return tokens, dict(sorted(excluded.items()))


class SourceView:
    def __init__(self, path, source):
        self.path = path
        self.source = source
        self.lines = [0] + [m.end() for m in re.finditer("\n", source)]
        self.tokens, self.excluded = lex(source)
        self.mates = {}
        self.depth = []
        stack = []
        for i, token in enumerate(self.tokens):
            value = token.value if token.kind == "symbol" else None
            self.depth.append(len(stack))
            if value in PAIRS:
                stack.append(i)
            elif value in PAIRS.values():
                if not stack or PAIRS[self.tokens[stack[-1]].value] != value:
                    raise InventoryError(f"unmatched bracket at {self.ref(token.start)}")
                opening = stack.pop()
                self.mates[opening] = i
                self.mates[i] = opening
        if stack:
            raise InventoryError(f"unclosed bracket at {self.ref(self.tokens[stack[-1]].start)}")

    def position(self, offset):
        line = bisect_right(self.lines, offset)
        return {"offset": offset, "line": line, "column": offset - self.lines[line - 1] + 1}

    def ref(self, offset):
        pos = self.position(offset)
        return f"{self.path}:{pos['line']}:{pos['column']}"

    def span(self, start, end):
        return {"file": self.path, "ref": self.ref(start), "start": self.position(start),
                "end": self.position(end), "excerpt": self.source[start:end]}

    def argument_slices(self, opening):
        closing = self.mates[opening]
        if closing == opening + 1:
            return []
        starts = [opening + 1]
        ends = []
        for i in range(opening + 1, closing):
            if self.tokens[i].value == "," and self.depth[i] == self.depth[opening] + 1:
                ends.append(i)
                starts.append(i + 1)
        return list(zip(starts, ends + [closing]))

    def functor(self, i):
        tokens = self.tokens
        if (tokens[i].kind not in {"atom", "symbol"} or i + 1 >= len(tokens)
                or tokens[i + 1].value != "(" or tokens[i].end != tokens[i + 1].start):
            return None
        # Only unquoted names/graphic operators, never punctuation/grouping.
        if tokens[i].kind == "symbol" and tokens[i].value in set("()[]{},;|.") | {":-", "->", "*->"}:
            return None
        args = self.argument_slices(i + 1)
        return {"signature": f"{tokens[i].value}/{len(args)}", "args": args,
                "end_index": self.mates[i + 1]}

    def chunks(self):
        start = 0
        for i, token in enumerate(self.tokens):
            if token.value == "." and self.depth[i] == 0:
                yield start, i + 1
                start = i + 1
        if start != len(self.tokens):
            raise InventoryError(f"missing final full stop at {self.ref(self.tokens[start].start)}")

    def context_slice(self, index, lo, hi, prefix=False):
        """Bracket-aware slice, deliberately not an operator-precedence parse."""
        left = index
        if not prefix:
            j = index - 1
            while j >= lo:
                value = self.tokens[j].value
                if value in PAIRS.values():
                    j = self.mates[j] - 1
                elif value in SEPARATORS or value in PAIRS:
                    break
                else:
                    j -= 1
            left = j + 1
        j = index + 1
        while j < hi:
            value = self.tokens[j].value
            if value in PAIRS:
                j = self.mates[j] + 1
            elif value in SEPARATORS or value in PAIRS.values():
                break
            else:
                j += 1
        return left, j


def components(graph):
    """Deterministic strongly connected components of lexical dependencies."""
    index = {}
    low = {}
    stack = []
    active = set()
    found = []

    def visit(node):
        index[node] = low[node] = len(index)
        stack.append(node)
        active.add(node)
        for nxt in sorted(graph[node]):
            if nxt not in index:
                visit(nxt)
                low[node] = min(low[node], low[nxt])
            elif nxt in active:
                low[node] = min(low[node], index[nxt])
        if low[node] == index[node]:
            group = []
            while True:
                nxt = stack.pop()
                active.remove(nxt)
                group.append(nxt)
                if nxt == node:
                    break
            found.append(sorted(group))

    for node in sorted(graph):
        if node not in index:
            visit(node)
    return sorted(found)


def analyze_sources(sources):
    files, clauses, sites, functors = [], [], [], []
    definitions = defaultdict(list)
    for path, source in sorted(sources):
        view = SourceView(path, source)
        tokens = view.tokens
        file_record = {"file": path, "characters": len(source), "utf8_bytes": len(source.encode("utf-8")),
                       "lines": len(source.splitlines()), "tokens": len(tokens), "excluded": view.excluded,
                       "graphic_symbols": dict(sorted(Counter(t.value for t in tokens
                                                               if t.kind == "symbol").items()))}
        files.append(file_record)
        for lo, hi in view.chunks():
            head = view.functor(lo)
            directive = tokens[lo].value in {":-", "?-"}
            rule = next((i for i in range(lo, hi) if tokens[i].value in {":-", "-->"}
                         and view.depth[i] == 0), None)
            if directive:
                signature = None
                body_start = lo + 1
            else:
                if tokens[lo].kind != "atom":
                    raise InventoryError(f"unsupported clause head at {view.ref(tokens[lo].start)}")
                signature = head["signature"] if head else tokens[lo].value + "/0"
                head_end = head["end_index"] + 1 if head else lo + 1
                if head_end != (rule if rule is not None else hi - 1):
                    raise InventoryError(f"unsupported head layout at {view.ref(tokens[lo].start)}")
                body_start = rule + 1 if rule is not None else hi
            if rule is not None and tokens[rule].value == "-->":
                raise InventoryError(f"DCG needs separate review at {view.ref(tokens[rule].start)}")
            clause = {"id": view.ref(tokens[lo].start), "predicate": signature,
                      "role": "directive" if directive else "rule" if rule is not None else "fact",
                      **view.span(tokens[lo].start, tokens[hi - 1].end)}
            clauses.append(clause)
            if signature:
                definitions[signature].append(clause["id"])
            for i in range(lo, hi):
                functor = view.functor(i)
                if functor:
                    role = "directive_term" if directive else "body_term" if i >= body_start else "head_term"
                    occurrence = {"signature": functor["signature"], "role": role,
                                  "clause": clause["id"], **view.span(tokens[i].start, tokens[functor["end_index"]].end)}
                    functors.append(occurrence)
            for i in range(body_start, hi - 1):
                token = tokens[i]
                if token.kind in {"literal", "variable"}:
                    continue
                value = token.value
                functor = view.functor(i)
                tags = []
                if value == "\\+":
                    tags.append("naf")
                if value == "!":
                    tags.append("cut")
                # A bare data atom (e.g. member(is, Xs)) is not infix syntax.
                infix_is = (value == "is" and i > body_start and i + 1 < hi - 1
                            and (tokens[i - 1].kind in {"variable", "number", "literal"}
                                 or tokens[i - 1].value in PAIRS.values())
                            and tokens[i + 1].value not in SEPARATORS | set(PAIRS.values()))
                if infix_is or (value == "is" and functor and functor["signature"] == "is/2"):
                    tags.append("is")
                if value in AGGREGATES and functor:
                    tags.append(value)
                if value in COMPARISONS or (value in COMPARISON_CALLS and functor):
                    tags.append("comparison")
                if value in ARITHMETIC:
                    tags.append("arithmetic_observation")
                if value in VARIABLE and functor:
                    tags.append("variable_observation")
                if value in DATE_SUPPORT and functor:
                    tags.append("date_support_observation")
                if value in LIST_SUPPORT and functor:
                    tags.append("list_observation")
                if value in META and functor:
                    tags.append("meta_observation")
                if value in {"->", "*->", ";"}:
                    tags.append("control_observation")
                if token.kind == "number" and any(c in value for c in ".eE"):
                    tags.append("noninteger_literal_observation")
                if not tags:
                    continue
                if functor:
                    a, b = i, functor["end_index"] + 1
                elif value == "!" or value in {"->", "*->", ";"}:
                    a, b = i, i + 1
                else:
                    a, b = view.context_slice(i, body_start, hi, prefix=value == "\\+")
                site = {"id": view.ref(token.start), "symbol": value, "tags": tags,
                        "clause": clause["id"], "predicate": signature, "decision": "TODO",
                        "token": view.span(token.start, token.end),
                        "construct": view.span(tokens[a].start, tokens[b - 1].end)}
                if "comparison" in tags:
                    site["date_use"] = {"status": "needs_human_confirmation", "evidence": [],
                                        "reason": "Conservative comparison/order/unification candidate; no type inference."}
                sites.append(site)

    # A narrowly checked source witness, not a runtime type or binding proof.
    # Recognize exactly the installed helper bodies before marking any use.
    expected = {
        "day_to_stamp/2": 'day_to_stamp(Day,Stamp):-split_string(Day,"-","",[YS,MS,DS]),atom_number(YS,YI),atom_number(MS,MI),atom_number(DS,DI),DI1isDI+1,date_time_stamp(date(YI,MI,DI1,0,0,0,0,-,-),Stamp).',
        "is_before/2": 'is_before(Day1,Day2):-nonvar(Day1),nonvar(Day2),day_to_stamp(Day1,Stamp1),day_to_stamp(Day2,Stamp2),Stamp1=<Stamp2.',
    }
    witnesses = {}
    for signature, shape in expected.items():
        matches = [c for c in clauses if c["predicate"] == signature]
        if len(matches) == 1:
            normalized = "".join(t.value for t in lex(matches[0]["excerpt"])[0])
            if normalized == shape:
                witnesses[signature] = matches[0]["id"]
    helper_verified = len(witnesses) == len(expected)
    signatures_by_ref = {f["ref"]: f["signature"] for f in functors}
    for site in sites:
        if "comparison" not in site["tags"]:
            continue
        if helper_verified and (signatures_by_ref.get(site["id"]) == "is_before/2"
                                or site["clause"] == witnesses["is_before/2"]):
            site["date_use"] = {
                "status": "source_proven_date_use", "evidence": list(witnesses.values()),
                "reason": "Exact lexical helper bodies connect this use to date_time_stamp(date(...),...). This proves source use only, not runtime types, success, units, or target semantics.",
            }
    # Direct operands sharing names with date_time_stamp/2 output arguments are
    # only candidates: lexical co-occurrence is not a binding/dataflow proof.

    graph = {signature: set() for signature in definitions}
    edges = defaultdict(list)
    owners = {c["id"]: c["predicate"] for c in clauses}
    for occurrence in functors:
        if occurrence["role"] != "body_term" or occurrence["signature"] not in definitions:
            continue
        owner = owners[occurrence["clause"]]
        graph[owner].add(occurrence["signature"])
        edges[(owner, occurrence["signature"])].append(occurrence["ref"])
    recursive = []
    for group in components(graph):
        if len(group) == 1 and group[0] not in graph[group[0]]:
            continue
        recursive.append({"predicates": group, "decision": "TODO",
                          "kind": "direct_candidate" if len(group) == 1 else "mutual_candidate",
                          "definitions": {p: definitions[p] for p in group},
                          "edges": [{"from": a, "to": b, "refs": refs}
                                    for (a, b), refs in sorted(edges.items()) if a in group and b in group]})
    functor_index = []
    grouped = defaultdict(list)
    for item in functors:
        grouped[item["signature"]].append(item)
    for signature, occurrences in sorted(grouped.items()):
        functor_index.append({"signature": signature, "defined_in_scope": signature in definitions,
                              "definitions": definitions.get(signature, []),
                              "occurrences": occurrences})
    counts = Counter(tag for site in sites for tag in site["tags"])
    # Explicit zeroes make the absent requested spelling visible.
    for tag in ["naf", "cut", "findall", "sumlist", "sum_list", "is", "comparison"]:
        counts.setdefault(tag, 0)
    for file in files:
        file["counts"] = dict(sorted(Counter(tag for s in sites if s["token"]["file"] == file["file"]
                                                   for tag in s["tags"]).items()))
    symbols = Counter(s["symbol"] for s in sites if "comparison" in s["tags"])
    observations = [
        {"id": "money", "decision": "TODO", "detail": "Plan specifies integer cents. Resolve source units, floating/rational arithmetic, rounding/ties/negative values, intermediate precision, division and error behavior; no rule chosen.",
         "site_tags": ["is", "arithmetic_observation", "noninteger_literal_observation"]},
        {"id": "dates", "decision": "TODO", "detail": "Plan specifies day counts. Resolve epoch, inclusive/exclusive endpoints, DI+1, duration units, calendar overflow, leap years, timezone/formatting, string year term ordering, and date conversion argument types. No epoch or interval policy chosen.",
         "site_tags": ["comparison", "date_support_observation"]},
        {"id": "variables", "decision": "TODO", "detail": "Resolve modes, nonground NAF, var/nonvar, anonymous variables, unification versus identity versus arithmetic comparison, unbound helper outputs, absent facts, and source runtime errors.",
         "site_tags": ["naf", "variable_observation", "comparison"]},
        {"id": "aggregates", "decision": "TODO", "detail": "sumlist and sum_list are separate lexical spellings. Resolve multiplicity/order, list_to_set equality, list concatenation, empty lists and unbound outputs; no duplicate or absence policy chosen.",
         "site_tags": ["findall", "sumlist", "sum_list", "list_observation"]},
        {"id": "control", "decision": "TODO", "detail": "Resolve cut, disjunction, if-then-else, clause order and choice points; lexical contexts are not execution traces.",
         "site_tags": ["cut", "control_observation"]},
        {"id": "builtins", "decision": "TODO", "detail": "Review every functor_index entry with defined_in_scope=false, plus directives and bare atoms in clauses. They may be builtins, external fact predicates, or data constructors. Runtime/dialect/library/operator settings and undefined-predicate behavior are not established.",
         "site_tags": ["meta_observation", "arithmetic_observation", "date_support_observation"]},
        {"id": "recursion", "decision": "TODO", "detail": "Review direct and mutual lexical dependency cycles. Reachability, meta-call targets, modes, finite domains and termination are unresolved; no strategy chosen."},
    ]
    return {
        "schema_version": 1,
        "scope": {"root": SOURCE.as_posix(), "selection": "all recursively discovered regular .pl files; no symlinks",
                  "source_text": "human/sara/sara/statutes/source/ (not scanned or aligned)",
                  "excluded": "No cases, owner decisions, parity, exploits, invariant statements, Oracle, or harness read."},
        "method": {"locations": "UTF-8 decoded without newline normalization; zero-based character offsets; one-based line/column; tab=one character; exclusive ends",
                   "counts": "Unquoted body/directive syntax candidates only; quoted literal contents, comments, clause heads and predicate indicators are not hazard sites. Named calls require adjacent '('. is requires an operand-like predecessor or is/2 functor form. Tags overlap; sites count unique token positions.",
                   "context": "Full balanced functor/NAF or separator-bounded expression plus full enclosing clause. No precedence evaluation or AST.",
                   "comparison_operators": sorted(COMPARISONS), "comparison_calls": sorted(COMPARISON_CALLS),
                   "date_evidence": "source_proven_date_use requires the exact checked day_to_stamp/2 and is_before/2 bodies; all other comparisons (including earliest/latest, year/duration/explicit timestamp operands) require human confirmation.",
                   "recursion": "SCCs of unquoted body functor name/arity matching defined heads, including nested terms/NAF/findall; deliberately conservative."},
        "limitations": [
            "Lexical inventory, not complete semantic analysis or a Prolog parser. A functor-shaped term is not proven executable; data constructors may be included.",
            "Arbitrary custom comparison names are not inferred; the full functor index and all clauses are retained for human review. Implicit comparisons inside dependencies are not expanded.",
            "Quoted atom/string contents never contribute syntax hits, even if a quoted functor or meta-call could invoke a hazardous predicate. Review literals in clause excerpts for such use.",
            "Unquoted operators embedded as data can resemble executable syntax. There is no goal-versus-term semantic classification; inspect enclosing clauses. Bare data atom is is excluded by the operand/functor check.",
            "Recursion candidates can overapproximate term occurrences and miss bare-atom, variable, quoted, module-qualified, external or dynamically constructed calls. No termination or reachability claim.",
            "No runtime dialect flags, library versions, operator declarations, fact data, source prose alignment, target choices, binding analysis, or types are inferred.",
            "Unsupported character/base-number literals, quasi quotations, DCGs, complex heads, malformed quotes/brackets and missing clause stops fail rather than silently produce a partial inventory.",
            "The source-witness date label is deliberately narrow: changing either checked helper body demotes uses to human-confirmation candidates.",
        ],
        "summary": {"files": len(files), "clauses": len(clauses), "defined_predicates": len(definitions),
                    "unique_sites": len(sites), "counts": dict(sorted(counts.items())),
                    "comparison_symbols": dict(sorted(symbols.items())),
                    "date_status": dict(sorted(Counter(s["date_use"]["status"] for s in sites if "date_use" in s).items())),
                    "recursive_components": len(recursive), "recursive_predicate_candidates": sum(len(c["predicates"]) for c in recursive)},
        "files": files, "sites": sites, "clauses": clauses,
        "recursive_candidates": recursive, "functor_index": functor_index, "observations": observations,
    }


def inventory(root):
    base = root / SOURCE
    if not base.is_dir() or any(p.is_symlink() for p in [base, *base.parents]):
        raise InventoryError(f"source directory missing or symlinked: {base}")
    paths = sorted(base.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise InventoryError("symlink under source directory; review scope before scanning")
    paths = [p for p in paths if p.is_file() and p.suffix == ".pl"]
    if not paths:
        raise InventoryError("no .pl sources found")
    return analyze_sources([(p.relative_to(root).as_posix(), p.read_bytes().decode("utf-8")) for p in paths])


def self_test():
    sample = '''% \\+ ! findall sumlist is <
/* outer /* ! */ is > */
p(X) :- X = "\\\\+ ! findall sumlist is >=", X = 'it''s !',
        \\+ (q(X),
             r(X)), !,
        findall(X, (q(X), findall(Y,q(Y),Ys)), Xs),
        sum_list(Xs,S), sumlist(Xs,T), S is
        0.5 + T, S =< T, is_before(X, X).
q(X) :- p(X).
'''
    data = analyze_sources([("fixture.pl", sample)])
    counts = data["summary"]["counts"]
    assert {k: counts[k] for k in ["naf", "cut", "findall", "sumlist", "sum_list", "is", "comparison"]} == {
        "naf": 1, "cut": 1, "findall": 2, "sumlist": 1, "sum_list": 1, "is": 1, "comparison": 4}
    for site in data["sites"]:
        for span in [site["token"], site["construct"]]:
            assert sample[span["start"]["offset"]:span["end"]["offset"]] == span["excerpt"]
    assert "\n" in next(s["construct"]["excerpt"] for s in data["sites"] if s["symbol"] == "is")
    assert next(s for s in data["sites"] if s["symbol"] == "\\+")["construct"]["excerpt"] == "\\+ (q(X),\n             r(X))"
    assert data["summary"]["recursive_predicate_candidates"] == 2
    assert all(s["date_use"]["status"] == "needs_human_confirmation" for s in data["sites"] if "date_use" in s)
    # Maximal graphic tokens must not be split into shorter comparison operators.
    ops, _ = lex("A \\== B, A =\\= B, A @=< B, A -> B, A =:= B.")
    assert [t.value for t in ops if t.value in COMPARISONS] == ["\\==", "=\\=", "@=<", "=:="]
    tokens, ignored = lex('p("escaped \\\" !", `is !`, \'\\\\+\'). % !')
    assert len([t for t in tokens if t.kind == "literal"]) == 3
    assert ignored["line_comments"] == 1
    atom_data = analyze_sources([("fixture.pl", "p(X) :- member(is, X), member(findall, X), X = '!'.")])
    assert all(atom_data["summary"]["counts"][k] == 0 for k in ["is", "findall", "cut"])
    all_ops = analyze_sources([("fixture.pl", "p(A,B) :- " + ", ".join("A " + op + " B" for op in sorted(COMPARISONS)) + ".")])
    assert set(all_ops["summary"]["comparison_symbols"]) == COMPARISONS
    crlf = SourceView("fixture.pl", "% π\r\np(X) :-\r\n\tX is 1.\r\n")
    token = next(t for t in crlf.tokens if t.value == "is")
    assert crlf.position(token.start) == {"offset": 17, "line": 3, "column": 4}
    for malformed in ["p('unterminated).", "p(X.", "/* bad", "p({|x||is|}).", "p(0'a).", "p(X)"]:
        try:
            analyze_sources([("fixture.pl", malformed)])
        except InventoryError:
            pass
        else:
            raise AssertionError(f"expected rejection: {malformed}")
    return {"self_test": "passed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true", help="run in-memory lexical checks; emit JSON")
    args = parser.parse_args()
    try:
        result = self_test() if args.self_test else inventory(args.repo_root.absolute())
    except (InventoryError, OSError, UnicodeError) as exc:
        print(f"inventory_hazards: {exc}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
