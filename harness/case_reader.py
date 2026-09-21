"""Source-preserving, non-executing reader for the original SARA case syntax.

This is a syntax tree, not a Household, Prolog evaluator, or output projection.
Only the operators used by the cases are accepted. Unsupported syntax fails
with an original-source location; it is never skipped or evaluated elsewhere.
See docs/phase1/SERIALIZER_READER.md for scope and grounding handoff.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterator


class CaseReaderError(ValueError):
    """Malformed or unsupported source, with an original-source location."""


@dataclass(frozen=True)
class Span:
    """Half-open UTF-8 byte offsets into the ORIGINAL source, not reader text."""

    start: int
    end: int


@dataclass(frozen=True)
class ReaderEdit:
    """An insertion authorized by H4.4; offsets always refer to original bytes."""

    offset: int
    inserted: bytes
    line: int
    decision: str
    source_sha256: str


@dataclass(frozen=True)
class Source:
    name: str
    original: bytes
    reader: bytes
    edits: tuple[ReaderEdit, ...]

    @property
    def sha256(self) -> str:
        return sha256(self.original).hexdigest()

    def text(self, span: Span) -> str:
        return self.original[span.start:span.end].decode("utf-8")

    def location(self, offset: int) -> str:
        prefix = self.original[:offset]
        line = prefix.count(b"\n") + 1
        column = len(prefix.rsplit(b"\n", 1)[-1].decode("utf-8")) + 1
        return f"{self.name}:{line}:{column}"

    def original_offset(self, reader_offset: int) -> int:
        shift = 0
        for edit in self.edits:
            start = edit.offset + shift
            if reader_offset <= start:
                break
            if reader_offset < start + len(edit.inserted):
                return edit.offset
            shift += len(edit.inserted)
        return reader_offset - shift

    def span(self, start: int, end: int) -> Span:
        return Span(self.original_offset(start), self.original_offset(end))


@dataclass(frozen=True)
class Token:
    kind: str
    lexeme: str
    span: Span
    reader_span: Span
    synthetic: bool = False


@dataclass(frozen=True)
class Variable:
    """Identity local to one source statement; '_' always gets a fresh ordinal.

    Named occurrences share this object, including between a rule head/body or
    different conjuncts. This is NOT an Interface.Pat.wild allocation scheme.
    """

    source_name: str
    source_sha256: str
    statement: int
    ordinal: int
    name: str


@dataclass(frozen=True)
class Node:
    """Syntax tags: atom, str, int, var, compound, list, group, op.

    group retains explicit parentheses; list retains element order; op retains
    its syntactic operator tree. value is a spelling, integer, or Variable.
    Equality of Nodes includes provenance; it is not Prolog term equality.
    """

    tag: str
    value: str | int | Variable | None
    args: tuple[Node, ...]
    span: Span

    def walk(self) -> Iterator[Node]:
        yield self
        for arg in self.args:
            yield from arg.walk()


@dataclass(frozen=True)
class Statement:
    index: int
    kind: str  # fact, rule, directive
    ast: Node
    span: Span
    reader_span: Span
    variables: tuple[Variable, ...]

    @property
    def head(self) -> Node | None:
        if self.kind == "directive":
            return None
        return self.ast.args[0] if self.kind == "rule" else self.ast

    @property
    def body(self) -> Node | None:
        return self.ast.args[-1] if self.kind != "fact" else None


@dataclass(frozen=True)
class Evidence:
    """Original section, from its '% Question' etc. marker to the next marker.

    Test evidence includes its directives, comments and whitespace verbatim.
    No natural-language interpretation or expected-answer extraction occurs.
    """

    label: str
    span: Span


@dataclass(frozen=True)
class Directive:
    statement: Statement
    role: str  # load, declaration, halt, query, other
    evidence: Evidence | None

    @property
    def goal(self) -> Node:
        return self.statement.ast.args[0]


@dataclass(frozen=True)
class CaseProgram:
    source: Source
    tokens: tuple[Token, ...]  # includes every whitespace/comment token
    statements: tuple[Statement, ...]
    evidence: tuple[Evidence, ...]
    directives: tuple[Directive, ...]

    @property
    def clauses(self) -> tuple[Statement, ...]:
        """All supplied facts AND rules, including helpers and stipulations."""
        return tuple(s for s in self.statements if s.kind != "directive")

    @property
    def queries(self) -> tuple[Directive, ...]:
        """Entire % Test goals, including NAF/conjuncts; no output modes inferred."""
        return tuple(d for d in self.directives if d.role == "query")

    def original_text(self, item: Statement | Evidence | Node | Token) -> str:
        return self.source.text(item.span)

    def reader_text(self, statement: Statement) -> str:
        s = statement.reader_span
        return self.source.reader[s.start:s.end].decode("utf-8")

    def clause_texts(self) -> tuple[str, ...]:
        """Exact clause slices for a later pinned-SWI consumer, in source order.

        Includes full stops (the two H4.4 stops are synthetic), inline comments,
        and original spelling. Excludes ALL directives. Nothing is executed,
        grounded, sorted, renamed or reconstructed from the AST. A consumer
        must separately arrange approved init/declarations and a readonly runner.
        """
        return tuple(self.reader_text(s) for s in self.clauses)


# Exact installed source identities, checked before applying the ONLY repairs.
# A changed file at either name is an error, never a fuzzy repair candidate.
_H44 = {
    "s3306_c_2_neg.pl": "20ac10863992b937b3aff70b79ac1c27fa101a555a45feeb21f01c4f0374097e",
    "s3306_c_2_pos.pl": "1b912b348ef4481643a509a920bd6653522571dd9c1f29673d2ad2280c478d88",
}


def _source(data: bytes, name: str) -> Source:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CaseReaderError(f"{name}: invalid UTF-8 at byte {error.start}") from error
    expected = _H44.get(Path(name).name)
    if expected is None:
        return Source(name, data, data, ())
    digest = sha256(data).hexdigest()
    if digest != expected:
        raise CaseReaderError(f"{name}: H4.4 source identity changed: {digest}")
    lines = data.splitlines(keepends=True)
    offset = sum(map(len, lines[:26])) - len(lines[25]) + len(lines[25].rstrip(b"\r\n"))
    edit = ReaderEdit(offset, b".", 26, "human/DECISIONS.md H4.4 / F2", digest)
    return Source(name, data, data[:offset] + b"." + data[offset:], (edit,))


_LAYOUT = b" \t\r\n\f\v"
_SYMBOLS = (b"\\==", b":-", b"\\+", b"->", b"==", b"=", b"/", b",", b";")
_PUNCT = b"()[]"


def _lex(source: Source) -> tuple[Token, ...]:
    data = source.reader
    result = []
    i = 0
    while i < len(data):
        start = i
        c = data[i]
        if c in _LAYOUT:
            i += 1
            while i < len(data) and data[i] in _LAYOUT:
                i += 1
            kind = "layout"
        elif c == ord("%"):
            end = data.find(b"\n", i)
            i = len(data) if end < 0 else end
            kind = "comment"
        elif c in (ord("'"), ord('"')):
            quote = c
            i += 1
            while i < len(data) and data[i] != quote:
                if data[i] in (ord("\\"), 10, 13):
                    raise CaseReaderError(
                        f"{source.location(source.original_offset(i))}: "
                        "escaped/multiline quoted syntax is outside the case subset")
                i += 1
            if i == len(data):
                raise CaseReaderError(f"{source.location(source.original_offset(start))}: unclosed quote")
            i += 1
            kind = "atom" if quote == ord("'") else "str"
        elif ord("0") <= c <= ord("9"):
            i += 1
            while i < len(data) and ord("0") <= data[i] <= ord("9"):
                i += 1
            kind = "int"
        elif c == ord("_") or ord("A") <= c <= ord("Z") or ord("a") <= c <= ord("z"):
            i += 1
            while i < len(data) and (
                data[i] == ord("_") or ord("A") <= data[i] <= ord("Z")
                or ord("a") <= data[i] <= ord("z") or ord("0") <= data[i] <= ord("9")
            ):
                i += 1
            kind = "var" if c == ord("_") or ord("A") <= c <= ord("Z") else "atom"
        elif c in _PUNCT:
            i += 1
            kind = chr(c)
        elif c == ord(".") and (i + 1 == len(data) or data[i + 1] in _LAYOUT + b"%"):
            i += 1
            kind = "."
        else:
            symbol = next((s for s in _SYMBOLS if data.startswith(s, i)), None)
            if symbol is None:
                raise CaseReaderError(
                    f"{source.location(source.original_offset(i))}: unsupported syntax {data[i:i+12]!r}")
            i += len(symbol)
            kind = symbol.decode("ascii")
        span = source.span(start, i)
        result.append(Token(kind, data[start:i].decode("utf-8"), span,
                            Span(start, i), span.start == span.end))
    return tuple(result)


# Fixed syntax precedence, not a dynamic operator table or semantics engine.
# Lower Prolog priority binds tighter. Parentheses reset priority to zero.
_INFIX = {";": (1100, "xfy"), "->": (1050, "xfy"), ",": (1000, "xfy"),
          "=": (700, "xfx"), "==": (700, "xfx"), "\\==": (700, "xfx"),
          "/": (400, "yfx")}


class _Parser:
    def __init__(self, source: Source, tokens: tuple[Token, ...]):
        self.source = source
        self.tokens = tuple(t for t in tokens if t.kind not in ("layout", "comment"))
        self.i = 0
        self.statement_index = 0
        self.named: dict[str, Variable] = {}
        self.variables: list[Variable] = []
        self.digest = source.sha256

    def peek(self, kind: str) -> bool:
        return self.i < len(self.tokens) and self.tokens[self.i].kind == kind

    def error(self, message: str) -> CaseReaderError:
        offset = self.tokens[self.i].span.start if self.i < len(self.tokens) else len(self.source.original)
        return CaseReaderError(f"{self.source.location(offset)}: {message}")

    def take(self, kind: str | None = None) -> Token:
        if self.i == len(self.tokens) or (kind is not None and not self.peek(kind)):
            raise self.error(f"expected {kind or 'term'}")
        token = self.tokens[self.i]
        self.i += 1
        return token

    def expr(self, limit: int = 1200) -> tuple[Node, int]:
        if self.peek("\\+"):
            token = self.take()
            arg, _ = self.expr(900)
            left = Node("op", token.lexeme, (arg,), Span(token.span.start, arg.span.end))
            priority = 900
        else:
            left = self.primary()
            priority = 0
        while self.i < len(self.tokens):
            token = self.tokens[self.i]
            spec = _INFIX.get(token.kind)
            if spec is None or spec[0] > limit:
                break
            op_priority, fixity = spec
            if priority > op_priority or (priority == op_priority and fixity[0] == "x"):
                raise self.error("operator requires parentheses")
            self.take()
            right, _ = self.expr(op_priority if fixity[2] == "y" else op_priority - 1)
            left = Node("op", token.lexeme, (left, right), Span(left.span.start, right.span.end))
            priority = op_priority
        if priority > limit:
            raise self.error("operator requires parentheses")
        return left, priority

    def primary(self) -> Node:
        token = self.take()
        if token.kind == "(":
            node, _ = self.expr()
            closing = self.take(")")
            return Node("group", None, (node,), Span(token.span.start, closing.span.end))
        if token.kind == "[":
            args = []
            if not self.peek("]"):
                args.append(self.expr(999)[0])
                while self.peek(","):
                    self.take()
                    args.append(self.expr(999)[0])
            closing = self.take("]")
            return Node("list", None, tuple(args), Span(token.span.start, closing.span.end))
        if token.kind == "var":
            name = token.lexeme
            variable = self.named.get(name) if name != "_" else None
            if variable is None:
                variable = Variable(self.source.name, self.digest, self.statement_index,
                                    len(self.variables), name)
                self.variables.append(variable)
                if name != "_":
                    self.named[name] = variable
            return Node("var", variable, (), token.span)
        if token.kind == "int":
            return Node("int", int(token.lexeme), (), token.span)
        if token.kind not in ("atom", "str"):
            raise self.error(f"expected term, got {token.lexeme!r}")
        value = token.lexeme[1:-1] if token.lexeme[0] in "\"'" else token.lexeme
        if token.kind == "atom" and self.peek("("):
            if self.tokens[self.i].reader_span.start != token.reader_span.end:
                raise self.error("functor and '(' must be adjacent")
            self.take("(")
            args = [self.expr(999)[0]]
            while self.peek(","):
                self.take()
                args.append(self.expr(999)[0])
            closing = self.take(")")
            return Node("compound", value, tuple(args), Span(token.span.start, closing.span.end))
        return Node(token.kind, value, (), token.span)

    def statements(self) -> tuple[Statement, ...]:
        result = []
        while self.i < len(self.tokens):
            start = self.tokens[self.i]
            self.statement_index = len(result)
            self.named = {}
            self.variables = []
            if self.peek(":-"):
                self.take()
                # The only operator-form declaration in the case population.
                if self.peek("atom") and self.tokens[self.i].lexeme == "discontiguous":
                    decl = self.take()
                    arg, _ = self.expr(1149)
                    body = Node("op", "discontiguous", (arg,), Span(decl.span.start, arg.span.end))
                else:
                    body, _ = self.expr(1199)
                ast = Node("op", ":-", (body,), Span(start.span.start, body.span.end))
                kind = "directive"
            else:
                head = self.primary()
                if head.tag not in ("atom", "compound"):
                    raise self.error("case clause head must be an atom or compound")
                if self.peek(":-"):
                    self.take()
                    body, _ = self.expr(1199)
                    ast = Node("op", ":-", (head, body), Span(head.span.start, body.span.end))
                    kind = "rule"
                else:
                    ast, kind = head, "fact"
            stop = self.take(".")
            result.append(Statement(len(result), kind, ast, Span(start.span.start, stop.span.end),
                                    Span(start.reader_span.start, stop.reader_span.end),
                                    tuple(self.variables)))
        return tuple(result)


def parse_case(data: bytes, *, source_name: str = "<memory>") -> CaseProgram:
    """Parse bytes without executing directives or inferring any output positions.

    H4.4 applies only to the two exact named/hashed originals. All other source
    must be well terminated. No generalized full-stop recovery is performed.
    """
    source = _source(data, source_name)
    tokens = _lex(source)
    statements = _Parser(source, tokens).statements()
    markers = []
    for token in tokens:
        if token.kind == "comment" and token.lexeme.strip() in ("% Text", "% Question", "% Facts", "% Test"):
            line_prefix = source.original[:token.span.start].rsplit(b"\n", 1)[-1]
            if not line_prefix.strip():
                markers.append((token.lexeme.strip()[2:], token.span.start))
    evidence = tuple(Evidence(label, Span(start, markers[i + 1][1] if i + 1 < len(markers)
                                        else len(data))) for i, (label, start) in enumerate(markers))
    starts = [e.span.start for e in evidence]
    directives = []
    for statement in statements:
        if statement.kind != "directive":
            continue
        i = bisect_right(starts, statement.span.start) - 1
        section = evidence[i] if i >= 0 else None
        goal = statement.ast.args[0]
        if goal.tag == "list":
            role = "load"
        elif goal.tag == "op" and goal.value == "discontiguous":
            role = "declaration"
        elif goal.tag == "atom" and goal.value == "halt":
            role = "halt"
        elif section is not None and section.label == "Test":
            role = "query"
        else:
            role = "other"
        directives.append(Directive(statement, role, section))
    return CaseProgram(source, tokens, statements, evidence, tuple(directives))


def read_case(path: str | Path) -> CaseProgram:
    """Read exactly one UTF-8 case file. No loads, caches or writes are made."""
    path = Path(path)
    return parse_case(path.read_bytes(), source_name=str(path))
