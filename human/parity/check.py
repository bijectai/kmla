#!/usr/bin/env python3
"""Independent structural parity meter for KMLA JSON observations."""

import argparse
from decimal import Decimal
import json
import os
import re
import stat
import sys
import tempfile


REPORT_NAME = "mismatches.jsonl"
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")


class MeterError(Exception):
    """The requested comparison is not valid."""


class DuplicateKeyError(Exception):
    """A JSON object contains a repeated key."""


class NonJsonConstantError(Exception):
    """The input used a non-JSON numeric constant."""


class JsonFloat:
    """An exact JSON number whose token was not an integer token."""

    __slots__ = ("value",)

    def __init__(self, token):
        self.value = Decimal(token)

    def __eq__(self, other):
        return type(other) is JsonFloat and self.value == other.value


class MeterArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise MeterError("invalid invocation: " + message)


def parse_args(argv):
    parser = MeterArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--section", required=True, type=int)
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--prolog-out", required=True)
    parser.add_argument("--lean-out", required=True)
    return parser.parse_args(argv)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def reject_non_json_constant(value):
    raise NonJsonConstantError(value)


def directory_identities(inputs, prolog_out, lean_out):
    paths = [
        ("--inputs", inputs),
        ("--prolog-out", prolog_out),
        ("--lean-out", lean_out),
        ("current working directory", os.getcwd()),
    ]
    identities = []
    for label, path in paths:
        try:
            metadata = os.stat(path)
        except OSError as exc:
            raise MeterError("cannot stat {}: {}".format(label, exc)) from exc
        if not stat.S_ISDIR(metadata.st_mode):
            raise MeterError("{} is not a directory".format(label))
        identities.append((label, (metadata.st_dev, metadata.st_ino)))

    for left in range(len(identities)):
        for right in range(left + 1, len(identities)):
            if identities[left][1] == identities[right][1]:
                raise MeterError(
                    "{} and {} identify the same directory".format(
                        identities[left][0], identities[right][0]
                    )
                )


def parse_record(path, stem, section, kind):
    try:
        with open(path, "rb") as source:
            raw = source.read()
    except OSError as exc:
        raise MeterError("cannot read {}: {}".format(path, exc)) from exc

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MeterError("{} is not strict UTF-8".format(path)) from exc
    if text.startswith("\ufeff"):
        raise MeterError("{} begins with a UTF-8 byte-order mark".format(path))

    try:
        record = json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_non_json_constant,
            parse_float=JsonFloat,
        )
    except DuplicateKeyError as exc:
        raise MeterError(
            "{} contains duplicate JSON key {!r}".format(path, exc.args[0])
        ) from exc
    except NonJsonConstantError as exc:
        raise MeterError(
            "{} contains non-JSON constant {}".format(path, exc.args[0])
        ) from exc
    except json.JSONDecodeError as exc:
        raise MeterError("{} contains malformed JSON: {}".format(path, exc)) from exc

    if type(record) is not dict:
        raise MeterError("{} must contain a top-level object".format(path))
    if type(record.get("schema_version")) is not int:
        raise MeterError("{} has a non-integer schema_version".format(path))
    if record["schema_version"] != 1:
        raise MeterError("{} has unsupported schema_version".format(path))
    if type(record.get("input_id")) is not str:
        raise MeterError("{} has a non-string input_id".format(path))
    if record["input_id"] != stem:
        raise MeterError("{} has input_id different from its filename".format(path))
    if type(record.get("section")) is not int:
        raise MeterError("{} has a non-integer section".format(path))
    if record["section"] != section:
        raise MeterError("{} belongs to a different section".format(path))

    if kind == "input":
        if "payload" not in record:
            raise MeterError("{} is missing payload".format(path))
        if "result" in record:
            raise MeterError("{} is an input record containing result".format(path))
    else:
        expected_keys = {"schema_version", "input_id", "section", "result"}
        if set(record) != expected_keys:
            raise MeterError("{} does not have the exact output envelope".format(path))

    return record


def load_directory(path, section, kind):
    try:
        entries = sorted(os.scandir(path), key=lambda entry: entry.name)
    except OSError as exc:
        raise MeterError("cannot enumerate {}: {}".format(path, exc)) from exc

    records = {}
    identities = {}
    folded_ids = {}
    for entry in entries:
        name = entry.name
        if not name.endswith(".json"):
            if name.startswith("."):
                continue
            raise MeterError("unexpected non-JSON entry: {}".format(entry.path))

        stem = name[:-5]
        if ID_PATTERN.fullmatch(stem) is None:
            raise MeterError("invalid input ID in filename: {}".format(entry.path))

        try:
            metadata = entry.stat(follow_symlinks=False)
        except OSError as exc:
            raise MeterError("cannot stat {}: {}".format(entry.path, exc)) from exc
        if not stat.S_ISREG(metadata.st_mode):
            raise MeterError("candidate record is not a regular file: {}".format(entry.path))

        folded = stem.lower()
        if folded in folded_ids:
            raise MeterError(
                "IDs {!r} and {!r} collide under ASCII case folding".format(
                    folded_ids[folded], stem
                )
            )
        folded_ids[folded] = stem

        records[stem] = parse_record(entry.path, stem, section, kind)
        identities[stem] = (metadata.st_dev, metadata.st_ino)

    return records, identities


def strictly_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        if set(left) != set(right):
            return False
        return all(strictly_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(
            strictly_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def encode_json_string(value):
    encoded = json.dumps(value, ensure_ascii=False)
    return "".join(
        "\\u{:04x}".format(ord(character))
        if 0xD800 <= ord(character) <= 0xDFFF
        else character
        for character in encoded
    )


def encode_json(value):
    value_type = type(value)
    if value is None:
        return "null"
    if value_type is bool:
        return "true" if value else "false"
    if value_type is int:
        return str(value)
    if value_type is JsonFloat:
        return str(value.value)
    if value_type is str:
        return encode_json_string(value)
    if value_type is list:
        return "[" + ",".join(encode_json(item) for item in value) + "]"
    if value_type is dict:
        return "{" + ",".join(
            encode_json_string(key) + ":" + encode_json(item)
            for key, item in value.items()
        ) + "}"
    raise MeterError("cannot encode an unsupported JSON value")


def compare(section, inputs_path, prolog_path, lean_path):
    directory_identities(inputs_path, prolog_path, lean_path)

    inputs, _ = load_directory(inputs_path, section, "input")
    prolog, prolog_identities = load_directory(prolog_path, section, "output")
    lean, lean_identities = load_directory(lean_path, section, "output")

    if not inputs:
        raise MeterError("the input population is empty")

    input_ids = set(inputs)
    unexpected_prolog = set(prolog) - input_ids
    unexpected_lean = set(lean) - input_ids
    if unexpected_prolog:
        raise MeterError(
            "unexpected Prolog output ID: {}".format(sorted(unexpected_prolog)[0])
        )
    if unexpected_lean:
        raise MeterError(
            "unexpected Lean output ID: {}".format(sorted(unexpected_lean)[0])
        )

    mismatches = []
    for input_id in sorted(inputs):
        prolog_record = prolog.get(input_id)
        lean_record = lean.get(input_id)
        if prolog_record is not None and lean_record is not None:
            if prolog_identities[input_id] == lean_identities[input_id]:
                raise MeterError(
                    "engine output files share an identity for {}".format(input_id)
                )
            agrees = strictly_equal(
                prolog_record["result"], lean_record["result"]
            )
        else:
            agrees = False

        if not agrees:
            mismatches.append(
                {
                    "input_id": input_id,
                    "prolog": prolog_record,
                    "lean": lean_record,
                }
            )

    if not mismatches:
        return 0, b""

    lines = [encode_json(mismatch) for mismatch in mismatches]
    return 1, ("\n".join(lines) + "\n").encode("utf-8")


def write_report(contents):
    temporary_path = None
    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=".mismatches.", suffix=".tmp", dir="."
        )
        with os.fdopen(descriptor, "wb") as report:
            report.write(contents)
            report.flush()
            os.fsync(report.fileno())
        os.replace(temporary_path, REPORT_NAME)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass


def main(argv):
    try:
        args = parse_args(argv)
        exit_code, report = compare(
            args.section, args.inputs, args.prolog_out, args.lean_out
        )
        write_report(report)
        return exit_code
    except BaseException as exc:
        if isinstance(exc, MeterError):
            message = str(exc)
        else:
            message = "unexpected error: {}".format(exc)
        print(message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
