#!/usr/bin/env python3
"""Black-box checks for parity policies not fully covered by the fixture suite."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


SECTION = 151
REPORT = "mismatches.jsonl"


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def write_bytes(path, contents):
    with open(path, "wb") as destination:
        destination.write(contents)


def write_json(path, value):
    contents = json.dumps(
        value, ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")
    write_bytes(path, contents)


def input_record(input_id, payload=None):
    return {
        "schema_version": 1,
        "input_id": input_id,
        "section": SECTION,
        "payload": {} if payload is None else payload,
    }


def output_record(input_id, result):
    return {
        "schema_version": 1,
        "input_id": input_id,
        "section": SECTION,
        "result": result,
    }


class Fixture:
    def __init__(self, meter):
        self._temporary = tempfile.TemporaryDirectory(prefix="kmla-parity-owner-")
        self.root = Path(self._temporary.name)
        self.run = self.root / "run"
        self.inputs = self.root / "inputs"
        self.prolog = self.root / "prolog"
        self.lean = self.root / "lean"
        self.meter = str(Path(meter).resolve())
        for directory in (self.run, self.inputs, self.prolog, self.lean):
            directory.mkdir()

    def close(self):
        self._temporary.cleanup()

    def add_complete(self, input_id="x", result=None):
        write_json(self.inputs / (input_id + ".json"), input_record(input_id))
        write_json(
            self.prolog / (input_id + ".json"), output_record(input_id, result)
        )
        write_json(self.lean / (input_id + ".json"), output_record(input_id, result))

    def invoke(self, cwd=None, inputs=None, prolog=None, lean=None):
        return subprocess.run(
            [
                sys.executable,
                "-B",
                self.meter,
                "--section",
                str(SECTION),
                "--inputs",
                str(self.inputs if inputs is None else inputs),
                "--prolog-out",
                str(self.prolog if prolog is None else prolog),
                "--lean-out",
                str(self.lean if lean is None else lean),
            ],
            cwd=str(self.run if cwd is None else cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )


def require_outcome(process, code):
    require(process.returncode == code, "expected exit {}, got {}".format(code, process.returncode))
    require(process.stdout == b"", "meter wrote to stdout")
    if code == 2:
        require(process.stderr != b"", "exit 2 did not explain the failure on stderr")


def test_executable_and_shebang(meter):
    path = Path(meter)
    require(path.is_file(), "meter is not a regular file")
    require(os.access(str(path), os.X_OK), "meter is not executable")
    with open(path, "rb") as source:
        first_line = source.readline()
    require(first_line == b"#!/usr/bin/env python3\n", "unexpected shebang")


def test_dot_entries_are_ignored(meter):
    fixture = Fixture(meter)
    try:
        fixture.add_complete(result={"word": "café"})
        write_bytes(fixture.inputs / ".DS_Store", b"ignored")
        hidden = fixture.prolog / ".cache"
        hidden.mkdir()
        write_bytes(hidden / "nested.json", b"not read")
        process = fixture.invoke()
        require_outcome(process, 0)
        require((fixture.run / REPORT).read_bytes() == b"", "success report is not zero bytes")
    finally:
        fixture.close()


def test_other_entries_are_rejected(meter):
    fixtures = []
    try:
        regular = Fixture(meter)
        fixtures.append(regular)
        regular.add_complete()
        write_bytes(regular.inputs / "notes.txt", b"stray")
        write_bytes(regular.run / REPORT, b"stale\n")
        process = regular.invoke()
        require_outcome(process, 2)
        require((regular.run / REPORT).read_bytes() == b"stale\n", "exit 2 changed a stale report")

        dotted_json = Fixture(meter)
        fixtures.append(dotted_json)
        dotted_json.add_complete()
        write_bytes(dotted_json.inputs / ".extra.json", b"{}")
        require_outcome(dotted_json.invoke(), 2)

        json_directory = Fixture(meter)
        fixtures.append(json_directory)
        json_directory.add_complete()
        (json_directory.inputs / "extra.json").mkdir()
        require_outcome(json_directory.invoke(), 2)

        symlink = Fixture(meter)
        fixtures.append(symlink)
        symlink.add_complete()
        os.symlink(str(symlink.prolog / "x.json"), str(symlink.prolog / "extra.json"))
        require_outcome(symlink.invoke(), 2)

        if hasattr(os, "mkfifo"):
            fifo = Fixture(meter)
            fixtures.append(fifo)
            fifo.add_complete()
            os.mkfifo(str(fifo.lean / "extra.json"))
            require_outcome(fifo.invoke(), 2)
    finally:
        for fixture in fixtures:
            fixture.close()


def test_directory_aliases(meter):
    fixtures = []
    try:
        engine_alias = Fixture(meter)
        fixtures.append(engine_alias)
        engine_alias.add_complete()
        alias_path = engine_alias.root / "lean-alias"
        os.symlink(str(engine_alias.prolog), str(alias_path))
        require_outcome(engine_alias.invoke(lean=alias_path), 2)
        require(not (engine_alias.run / REPORT).exists(), "alias failure created a report")

        cwd_alias = Fixture(meter)
        fixtures.append(cwd_alias)
        cwd_alias.add_complete()
        require_outcome(cwd_alias.invoke(cwd=cwd_alias.inputs), 2)
        require(not (cwd_alias.inputs / REPORT).exists(), "cwd alias failure created a report")
    finally:
        for fixture in fixtures:
            fixture.close()


def test_output_file_alias(meter):
    fixture = Fixture(meter)
    try:
        write_json(fixture.inputs / "x.json", input_record("x"))
        write_json(fixture.prolog / "x.json", output_record("x", [1, 2]))
        os.link(str(fixture.prolog / "x.json"), str(fixture.lean / "x.json"))
        process = fixture.invoke()
        require_outcome(process, 2)
        require(not (fixture.run / REPORT).exists(), "file alias failure created a report")
    finally:
        fixture.close()


def test_exact_report_bytes(meter):
    fixture = Fixture(meter)
    try:
        write_json(fixture.inputs / "a.json", input_record("a"))
        write_json(fixture.inputs / "b.json", input_record("b"))
        prolog_a = output_record("a", {"word": "café"})
        lean_a = output_record("a", {"word": "thé"})
        prolog_b = output_record("b", [1, 2])
        write_json(fixture.prolog / "a.json", prolog_a)
        write_json(fixture.lean / "a.json", lean_a)
        write_json(fixture.prolog / "b.json", prolog_b)

        process = fixture.invoke()
        require_outcome(process, 1)
        expected = (
            '{"input_id":"a","prolog":{"schema_version":1,"input_id":"a",'
            '"section":151,"result":{"word":"café"}},"lean":{"schema_version":1,'
            '"input_id":"a","section":151,"result":{"word":"thé"}}}\n'
            '{"input_id":"b","prolog":{"schema_version":1,"input_id":"b",'
            '"section":151,"result":[1,2]},"lean":null}\n'
        ).encode("utf-8")
        actual = (fixture.run / REPORT).read_bytes()
        require(actual == expected, "mismatch report bytes differ from the pinned format")
        require(b"\r" not in actual, "report contains a carriage return")
        require(b"caf\\u00e9" not in actual, "report escaped non-ASCII text")
    finally:
        fixture.close()


def test_invalid_utf8_and_bom_preserve_report(meter):
    fixtures = []
    try:
        for label, contents in (("invalid", b"\xff"), ("bom", b"\xef\xbb\xbf{}")):
            fixture = Fixture(meter)
            fixtures.append(fixture)
            fixture.add_complete()
            write_bytes(fixture.inputs / "x.json", contents)
            write_bytes(fixture.run / REPORT, (label + "-stale\n").encode("ascii"))
            process = fixture.invoke()
            require_outcome(process, 2)
            require(
                (fixture.run / REPORT).read_bytes() == (label + "-stale\n").encode("ascii"),
                "{} JSON changed the report".format(label),
            )
    finally:
        for fixture in fixtures:
            fixture.close()


def test_casefold_collision_when_materializable(meter):
    fixture = Fixture(meter)
    try:
        write_json(fixture.inputs / "A.json", input_record("A"))
        write_json(fixture.inputs / "a.json", input_record("a"))
        names = {entry.name for entry in fixture.inputs.iterdir()}
        if names == {"A.json", "a.json"}:
            process = fixture.invoke()
            require_outcome(process, 2)
            return "checked"
        return "filesystem-collapsed"
    finally:
        fixture.close()


def test_strict_envelopes_and_nested_duplicates(meter):
    fixtures = []
    try:
        extra_output = Fixture(meter)
        fixtures.append(extra_output)
        write_json(extra_output.inputs / "x.json", input_record("x"))
        bad = output_record("x", None)
        bad["extra"] = True
        write_json(extra_output.prolog / "x.json", bad)
        write_json(extra_output.lean / "x.json", output_record("x", None))
        require_outcome(extra_output.invoke(), 2)

        no_payload = Fixture(meter)
        fixtures.append(no_payload)
        bad_input = input_record("x")
        del bad_input["payload"]
        write_json(no_payload.inputs / "x.json", bad_input)
        write_json(no_payload.prolog / "x.json", output_record("x", None))
        write_json(no_payload.lean / "x.json", output_record("x", None))
        require_outcome(no_payload.invoke(), 2)

        duplicate = Fixture(meter)
        fixtures.append(duplicate)
        write_json(duplicate.inputs / "x.json", input_record("x"))
        raw = (
            b'{"schema_version":1,"input_id":"x","section":151,'
            b'"result":{"nested":1,"nested":2}}'
        )
        write_bytes(duplicate.prolog / "x.json", raw)
        write_json(duplicate.lean / "x.json", output_record("x", None))
        require_outcome(duplicate.invoke(), 2)
    finally:
        for fixture in fixtures:
            fixture.close()


def test_raw_number_precision(meter):
    fixture = Fixture(meter)
    try:
        for input_id in ("large", "precise"):
            write_json(fixture.inputs / (input_id + ".json"), input_record(input_id))
        write_bytes(
            fixture.prolog / "large.json",
            b'{"schema_version":1,"input_id":"large","section":151,"result":1e400}',
        )
        write_bytes(
            fixture.lean / "large.json",
            b'{"schema_version":1,"input_id":"large","section":151,"result":1e399}',
        )
        write_bytes(
            fixture.prolog / "precise.json",
            b'{"schema_version":1,"input_id":"precise","section":151,'
            b'"result":0.10000000000000001}',
        )
        write_bytes(
            fixture.lean / "precise.json",
            b'{"schema_version":1,"input_id":"precise","section":151,"result":0.1}',
        )
        process = fixture.invoke()
        require_outcome(process, 1)
        report = (fixture.run / REPORT).read_bytes()
        require(b"1E+400" in report, "large exponent was not preserved exactly")
        require(
            b"0.10000000000000001" in report,
            "high-precision number was not preserved exactly",
        )
    finally:
        fixture.close()


def test_escaped_surrogates_remain_reportable(meter):
    fixture = Fixture(meter)
    try:
        write_json(fixture.inputs / "x.json", input_record("x"))
        write_bytes(
            fixture.prolog / "x.json",
            b'{"schema_version":1,"input_id":"x","section":151,"result":"\\ud800"}',
        )
        write_bytes(
            fixture.lean / "x.json",
            b'{"schema_version":1,"input_id":"x","section":151,"result":"\\ud801"}',
        )
        process = fixture.invoke()
        require_outcome(process, 1)
        report = (fixture.run / REPORT).read_bytes()
        report.decode("utf-8")
        require(b"\\ud800" in report, "first escaped surrogate was not retained")
        require(b"\\ud801" in report, "second escaped surrogate was not retained")
    finally:
        fixture.close()


def run_checks(meter):
    checks = [
        ("executable-and-shebang", lambda: test_executable_and_shebang(meter)),
        ("dot-entries-ignored", lambda: test_dot_entries_are_ignored(meter)),
        ("other-entry-types-rejected", lambda: test_other_entries_are_rejected(meter)),
        ("directory-and-cwd-aliases", lambda: test_directory_aliases(meter)),
        ("hardlinked-engine-outputs", lambda: test_output_file_alias(meter)),
        ("exact-report-bytes", lambda: test_exact_report_bytes(meter)),
        ("strict-utf8-and-exit2-preservation", lambda: test_invalid_utf8_and_bom_preserve_report(meter)),
        ("strict-envelopes-and-nested-duplicates", lambda: test_strict_envelopes_and_nested_duplicates(meter)),
        ("raw-number-precision", lambda: test_raw_number_precision(meter)),
        ("escaped-surrogate-reporting", lambda: test_escaped_surrogates_remain_reportable(meter)),
    ]
    failures = 0
    for name, check in checks:
        try:
            check()
            print("ok   " + name)
        except Exception as exc:
            failures += 1
            print("FAIL {}: {}".format(name, exc))

    try:
        result = test_casefold_collision_when_materializable(meter)
        if result == "checked":
            print("ok   ascii-casefold-collision")
        else:
            print("note ascii-casefold-collision: host filesystem collapsed the names")
    except Exception as exc:
        failures += 1
        print("FAIL ascii-casefold-collision: {}".format(exc))

    print("{} owner checks passed; {} failed".format(11 - failures, failures))
    return 1 if failures else 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--meter", required=True)
    args = parser.parse_args(argv)
    return run_checks(args.meter)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
