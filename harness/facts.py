"""Lossless Household transport, NOT query packaging, H4 grounding or Valid.

Authority: human/DECISIONS.md H1–H4/G4/D1/M1/A3 and
Interface/HOUSEHOLD_WIRE.md. No oracle implementation is imported.
Stipulation arity is deliberately separate from transport (Stip stores List Pat).
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re


class TransportError(ValueError):
    pass


# Exact supplied registry; the tests compare it with the declarative Interface.
FACT_TYPES = {
    "agent_": ("Term", "Term"),
    "agricultural_service": ("Term",) * 3,
    "alice_employer": ("Term",) * 3,
    "alice_household_maintenance": ("Term",) * 4,
    "american_employer_": ("Term",),
    "amount_": ("Term", "Int"),
    "attending_classes_": ("Term",),
    "beneficiary_": ("Term", "Term"),
    "birth_": ("Term",),
    "blindness_": ("Term",),
    "brother_": ("Term",),
    "business_": ("Term",),
    "business_trust_": ("Term",),
    "citizenship_": ("Term",),
    "country_": ("Term", "Term"),
    "daughter_": ("Term",),
    "death_": ("Term",),
    "deduction_": ("Term",),
    "destination_": ("Term", "Term"),
    "disability_": ("Term",),
    "educational_institution_": ("Term",),
    "end_": ("Term", "Day"),
    "enrollment_": ("Term",),
    "father_": ("Term",),
    "hospital_": ("Term",),
    "incarceration_": ("Term",),
    "income_": ("Term",),
    "international_organization_": ("Term",),
    "itemize_deductions_": ("Term",),
    "joint_return_": ("Term",),
    "legal_separation_": ("Term",),
    "location_": ("Term", "Term"),
    "marriage_": ("Term",),
    "means_": ("Term", "Term"),
    "medical_institution_": ("Term",),
    "medical_patient_": ("Term",),
    "migration_": ("Term",),
    "mother_": ("Term",),
    "nonresident_alien_": ("Term",),
    "nurses_training_school_": ("Term",),
    "patient": ("Term", "Term"),
    "patient_": ("Term", "Term"),
    "payment_": ("Term",),
    "penal_institution_": ("Term",),
    "plan_": ("Term",),
    "purpose_": ("Pat", "Term"),
    "reason_": ("Term", "Term"),
    "residence_": ("Term",),
    "retirement_": ("Term",),
    "service_": ("Term",),
    "sibling_": ("Term",),
    "sister_": ("Term",),
    "son_": ("Term",),
    "start_": ("Term", "Day"),
    "termination_": ("Term",),
    "type_": ("Term", "Term"),
    "unemployment_compensation_agreement_": ("Term",),
}

STIP_SIGNATURES = {
    "s63_3": ("s63", 3), "s7703_4": ("s7703", 4),
    "s3306_b_8": ("s3306_b", 8), "s2_b_3": ("s2_b", 3),
    "s2_a_3": ("s2_a", 3), "s151_c_applies_3": ("s151_c_applies", 3),
    "s152_c_1_3": ("s152_c_1", 3), "s3306_c_5": ("s3306_c", 5),
    "s151_5": ("s151", 5), "s151_d_4": ("s151_d", 4),
    "s151_b_applies_3": ("s151_b_applies", 3), "s151_c_4": ("s151_c", 4),
    "s151_b_applies_2": ("s151_b_applies", 2),
    "total_wages_employer_6": ("total_wages_employer", 6),
    "s68_b_3": ("s68_b", 3), "s152_c_2_4": ("s152_c_2", 4),
    "s152_c_3": ("s152_c", 3), "s152_b_2_4": ("s152_b_2", 4),
    "s3306_a_2": ("s3306_a", 2), "s63_c_1_3": ("s63_c_1", 3),
    "s63_c_2_3": ("s63_c_2", 3), "s63_c_3_3": ("s63_c_3", 3),
    "s63_f_1_A_2": ("s63_f_1_A", 2), "s63_f_1_B_3": ("s63_f_1_B", 3),
    "s63_d_4": ("s63_d", 4), "s152_c_3_3": ("s152_c_3", 3),
    "s2_a_5": ("s2_a", 5), "s152_d_2_H_6": ("s152_d_2_H", 6),
    "s63_c_3": ("s63_c", 3), "s63_c_3_4": ("s63_c_3", 4),
    "s151_b_3": ("s151_b", 3),
}


def _integer(value):
    if type(value) is not int:
        raise TransportError(f"expected exact integer, got {value!r}")
    return value


def _decimal(value):
    """Exact decimal, including values beyond Python's int/string digit cap."""
    _integer(value)
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    chunks = []
    while value:
        value, part = divmod(value, 10**9)
        chunks.append(part)
    return sign + str(chunks[-1]) + "".join(f"{n:09d}" for n in reversed(chunks[:-1]))


def _parse_decimal(text):
    negative = text.startswith("-")
    digits = text[1:] if negative else text
    value = 0
    for offset in range(0, len(digits), 9):
        chunk = digits[offset:offset + 9]
        value = value * 10**len(chunk) + int(chunk)
    return -value if negative else value


def _string(value):
    if type(value) is not str:
        raise TransportError(f"expected string, got {value!r}")
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as error:
        raise TransportError("unpaired surrogate is not UTF-8 text") from error
    return value


def _object(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise TransportError(f"expected object with exactly {keys!r}, got {value!r}")


def _array(value):
    if type(value) is not list:
        raise TransportError("expected explicit JSON array")
    return value


@dataclass(frozen=True)
class Term:
    tag: str
    value: str | int

    def __post_init__(self):
        if self.tag == "int":
            _integer(self.value)
        elif self.tag in ("atom", "str"):
            _string(self.value)
        else:
            raise TransportError(f"unknown Term tag {self.tag!r}")


@dataclass(frozen=True)
class Pat:
    tag: str
    value: Term | int

    def __post_init__(self):
        if self.tag == "wild":
            if _integer(self.value) < 0:
                raise TransportError("wildcard identity must be Nat")
        elif self.tag != "val" or not isinstance(self.value, Term):
            raise TransportError("expected Pat.val Term or Pat.wild Nat")


def day_from_iso(text):
    """Civil arithmetic only; no V3 admission, timestamp shift or normalization."""
    text = _string(text)
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
        raise TransportError(f"noncanonical Day spelling: {text!r}")
    y, m, d = map(int, text.split("-"))
    leap = y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
    lengths = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not (1 <= m <= 12 and 1 <= d <= lengths[m - 1]):
        raise TransportError(f"invalid civil date: {text!r}")
    y -= m <= 2
    era, yoe = divmod(y, 400)
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    return era * 146097 + yoe * 365 + yoe // 4 - yoe // 100 + doy - 719468


def day_to_iso(day):
    z = _integer(day) + 719468
    era, doe = divmod(z, 146097)
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    y += m <= 2
    if not 0 <= y <= 9999:
        raise TransportError("Day cannot be spelled with the specified four-digit year")
    return f"{y:04d}-{m:02d}-{d:02d}"


@dataclass(frozen=True)
class Fact:
    ctor: str
    args: tuple[Term | Pat | int, ...]

    def __post_init__(self):
        types = FACT_TYPES.get(self.ctor)
        if types is None or type(self.args) is not tuple or len(types) != len(self.args):
            raise TransportError(f"unknown Fact signature or incorrect arity: {self.ctor!r}")
        for kind, arg in zip(types, self.args):
            if kind in ("Int", "Day"):
                _integer(arg)
            elif not isinstance(arg, Term if kind == "Term" else Pat):
                raise TransportError(f"{self.ctor}: expected {kind}, got {arg!r}")


@dataclass(frozen=True)
class Stip:
    pred: str
    args: tuple[Pat, ...]

    def __post_init__(self):
        if self.pred not in STIP_SIGNATURES:
            raise TransportError(f"unknown StipPred: {self.pred!r}")
        if type(self.args) is not tuple or any(not isinstance(p, Pat) for p in self.args):
            raise TransportError("Stip args must be an ordered tuple of Pat")

    @property
    def well_formed(self):
        return len(self.args) == STIP_SIGNATURES[self.pred][1]


@dataclass(frozen=True)
class Household:
    facts: tuple[Fact, ...]
    stipulations: tuple[Stip, ...]

    def __post_init__(self):
        for values, cls in ((self.facts, Fact), (self.stipulations, Stip)):
            if type(values) is not tuple or any(not isinstance(v, cls) for v in values):
                raise TransportError(f"expected ordered tuple of {cls.__name__}")


def _term(value):
    if type(value) is int:
        return Term("int", value)
    if type(value) is dict and len(value) == 1:
        for key, tag in (("a", "atom"), ("s", "str")):
            if key in value:
                return Term(tag, value[key])
    raise TransportError(f"invalid Term: {value!r}")


def _pat(value):
    if type(value) is dict and len(value) == 1:
        if "val" in value:
            return Pat("val", _term(value["val"]))
        if "wild" in value:
            return Pat("wild", value["wild"])
    raise TransportError(f"invalid Pat: {value!r}")


def from_value(value):
    _object(value, ("facts", "stipulations"))
    facts, stips = [], []
    for fact in _array(value["facts"]):
        _object(fact, ("ctor", "args"))
        ctor = _string(fact["ctor"])
        args = _array(fact["args"])
        kinds = FACT_TYPES.get(ctor)
        if kinds is None or len(kinds) != len(args):
            raise TransportError(f"unknown Fact signature or incorrect arity: {ctor!r}")
        converters = {"Term": _term, "Pat": _pat, "Int": _integer, "Day": day_from_iso}
        facts.append(Fact(ctor, tuple(converters[k](v) for k, v in zip(kinds, args))))
    for stip in _array(value["stipulations"]):
        _object(stip, ("pred", "args"))
        stips.append(Stip(_string(stip["pred"]), tuple(map(_pat, _array(stip["args"])))))
    return Household(tuple(facts), tuple(stips))


def _term_value(term):
    return term.value if term.tag == "int" else {"a" if term.tag == "atom" else "s": term.value}


def _pat_value(pat):
    return {pat.tag: _term_value(pat.value) if pat.tag == "val" else pat.value}


def to_value(household):
    def arg_value(kind, value):
        if kind == "Term":
            return _term_value(value)
        if kind == "Pat":
            return _pat_value(value)
        return day_to_iso(value) if kind == "Day" else value

    return {
        "facts": [{"ctor": f.ctor, "args": [arg_value(k, a) for k, a in zip(FACT_TYPES[f.ctor], f.args)]}
                  for f in household.facts],
        "stipulations": [{"pred": s.pred, "args": list(map(_pat_value, s.args))}
                         for s in household.stipulations],
    }


def encode(household):
    """Canonical UTF-8 bytes, without BOM/newline. No list normalization."""
    def emit(value):
        if type(value) is int:
            return _decimal(value)
        if type(value) is list:
            return "[" + ",".join(map(emit, value)) + "]"
        if type(value) is dict:
            return "{" + ",".join(emit(k) + ":" + emit(v) for k, v in value.items()) + "}"
        return json.dumps(_string(value), ensure_ascii=False)
    return emit(to_value(household)).encode("utf-8")


def _pairs(pairs):
    value = {}
    for k, v in pairs:
        if k in value:
            raise TransportError(f"duplicate JSON key: {k!r}")
        value[k] = v
    return value


def _not_integer(value):
    raise TransportError(f"non-integer JSON number: {value}")


def decode(data):
    """Inverse value parser; object order/whitespace need not be canonical."""
    if isinstance(data, bytes):
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise TransportError("invalid UTF-8") from error
    try:
        value = json.loads(data, object_pairs_hook=_pairs, parse_int=_parse_decimal, parse_float=_not_integer,
                           parse_constant=_not_integer)
    except (ValueError, TypeError) as error:
        raise TransportError(str(error)) from error
    return from_value(value)


def _prolog_quote(text, quote):
    chunks = []
    for ch in text:
        if ord(ch) < 32 or ord(ch) == 127:
            chunks.append(f"\\x{ord(ch):x}\\")
        elif ch in (quote, "\\"):
            chunks.append("\\" + ch)
        else:
            chunks.append(ch)
    return quote + "".join(chunks) + quote


def _prolog_term(term):
    if term.tag == "int":
        return _decimal(term.value)
    return _prolog_quote(term.value, "'" if term.tag == "atom" else '"')


def _prolog_pat(pat):
    return "_KMLA_W" + _decimal(pat.value) if pat.tag == "wild" else _prolog_term(pat.value)


def emit_prolog(household):
    """Ordered bodyless clauses, to append AFTER statutes in a pinned consumer.

    Wildcard IDs are retained in variable spelling for syntax inspection. Prolog
    variables have clause scope and freshen on invocation; spelling is not a
    runtime identity/freshening proof or an H4 re-grounding result.
    """
    lines = []
    for fact in household.facts:
        args = []
        for kind, arg in zip(FACT_TYPES[fact.ctor], fact.args):
            if kind == "Term":
                args.append(_prolog_term(arg))
            elif kind == "Pat":
                args.append(_prolog_pat(arg))
            elif kind == "Day":
                args.append(_prolog_quote(day_to_iso(arg), '"'))
            else:
                args.append(_decimal(arg))
        lines.append(f"{fact.ctor}({','.join(args)}).")
    for stip in household.stipulations:
        if not stip.well_formed:
            raise TransportError(f"cannot emit {stip.pred} with {len(stip.args)} arguments")
        pred, _ = STIP_SIGNATURES[stip.pred]
        lines.append(f"{pred}({','.join(map(_prolog_pat, stip.args))}).")
    return "\n".join(lines) + ("\n" if lines else "")


def _lean_string(text):
    # Code-point construction avoids Lean/JSON/Prolog escape-dialect confusion,
    # including NUL. All strings were checked for Unicode scalar values above.
    return "(String.ofList [" + ", ".join(f"Char.ofNat {ord(c)}" for c in text) + "])"


def _lean_term(term):
    v = "(" + _decimal(term.value) + ")" if term.tag == "int" else _lean_string(term.value)
    return f"(KMLA.Term.{term.tag} {v})"


def _lean_pat(pat):
    v = _decimal(pat.value) if pat.tag == "wild" else _lean_term(pat.value)
    return f"(KMLA.Pat.{pat.tag} {v})"


def emit_lean(household):
    """A closed KMLA.Household expression; no admission instance or oracle."""
    facts = []
    for f in household.facts:
        args = []
        for kind, arg in zip(FACT_TYPES[f.ctor], f.args):
            args.append(_lean_term(arg) if kind == "Term" else
                        _lean_pat(arg) if kind == "Pat" else "(" + _decimal(arg) + ")")
        facts.append(f"(KMLA.Fact.{f.ctor} {' '.join(args)})")
    stips = [f"({{ pred := KMLA.StipPred.{s.pred}, args := [" +
             ", ".join(map(_lean_pat, s.args)) + "] } : KMLA.Stip)" for s in household.stipulations]
    return "({ facts := [" + ", ".join(facts) + "], stipulations := [" + ", ".join(stips) + "] } : KMLA.Household)"
