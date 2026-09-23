#!/usr/bin/env python3
"""Runtime-only regressions. No owner meter, protected writes, or semantic lanes."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
import runtime
import run_corpus


def probe():
    return {"version_string": "SWI-Prolog version 7.2.3 for amd64", "plarch": "amd64",
            "plversion": "70203", "uname_m": "x86_64", "dpkg_arch": "amd64",
            "tz": runtime.TZ, "tz_sha256": "c" * 64, "winter_offset": "-0500",
            "summer_offset": "-0400", "process_exe": "/usr/lib/swi-prolog/bin/amd64/swipl",
            "swipl_exe": "/usr/lib/swi-prolog/bin/amd64/swipl",
            "process_exe_sha256": "a" * 64, "swipl_exe_sha256": "a" * 64,
            "process_elf_machine": "3e00"}


PACKAGES = b"swi-prolog-nox\t7.2.3+dfsg-6\tamd64\tinstalled\nlibgmp10:amd64\t6.1\tamd64\tinstalled\n"


class FakeLog:
    def json(self, argv):
        if argv[1:3] == ["image", "inspect"]:
            return [{"Os": "linux", "Architecture": "amd64", "Id": "sha256:" + "d" * 64,
                     "Config": {"Labels": {runtime.LABEL: runtime.sha256(runtime.HERE / "Dockerfile")}},
                     "RepoDigests": []}]
        return {"OSType": "linux", "Architecture": "x86_64", "ServerVersion": "test"}


def measured(values=None):
    values = probe() if values is None else values
    data = "".join(f"{k}\t{v}\n" for k, v in values.items()).encode()
    responses = [({"exit": 0, "timed_out": False}, data, b""),
                 ({"exit": 0, "timed_out": False}, PACKAGES, b"")]
    with patch.object(runtime, "container", side_effect=responses):
        return runtime.measure(FakeLog(), "test", "test", require_native=True)


class RuntimeTests(unittest.TestCase):
    def test_entire_record_identity_only_excludes_local_image_id(self):
        original = measured()
        other = copy.deepcopy(original)
        other["image"]["local_image_id"] = "different config id"
        self.assertEqual(runtime.identity_sha256(original), runtime.identity_sha256(other))
        mutations = [("environment", "TZ", "UTC"), ("image", "dockerfile_sha256", "changed"),
                     ("interpreter", "installed_packages", []),
                     ("environment", "translator", {"name": "different"})]
        for section, field, value in mutations:
            with self.subTest(field=field):
                other = copy.deepcopy(original)
                other[section][field] = value
                self.assertNotEqual(runtime.identity_sha256(original), runtime.identity_sha256(other))
        other = copy.deepcopy(original)
        other["future_field"] = {"local_image_id": "still participates"}
        self.assertNotEqual(runtime.identity_sha256(original), runtime.identity_sha256(other))

    def test_exact_runtime_measurements(self):
        changes = {"version_string": "SWI-Prolog version 17.2.3 for amd64", "plversion": "90209",
                   "plarch": "aarch64", "uname_m": "aarch64", "dpkg_arch": "arm64",
                   "tz": "UTC", "winter_offset": "+0000", "summer_offset": "-0500"}
        for field, value in changes.items():
            with self.subTest(field=field):
                values = probe()
                values[field] = value
                with self.assertRaises(runtime.RuntimeFailure):
                    measured(values)

    def test_exact_package_and_complete_closure_parser(self):
        self.assertEqual(len(runtime.parse_packages(PACKAGES)), 2)
        for bad in (PACKAGES.replace(b"dfsg-6", b"dfsg-7"), PACKAGES.replace(b"amd64", b"arm64"),
                    PACKAGES.replace(b"installed", b"unpacked"), PACKAGES + b"bad row\n",
                    PACKAGES + PACKAGES, b""):
            with self.subTest(data=bad), self.assertRaises(runtime.RuntimeFailure):
                runtime.parse_packages(bad)

    def test_probe_never_drops_malformed_or_duplicate_rows(self):
        for bad in (b"version\t7.2.3\n\n", b"version\t7.2.3\nversion\t9.2.9\n", b"bad\n"):
            with self.assertRaises(runtime.RuntimeFailure):
                runtime.parse_probe(bad)

    def test_native_evidence_uses_daemon_and_prolog_process(self):
        native = runtime.translator(probe(), {"Architecture": "x86_64"})
        self.assertEqual(native["kind"], "native")
        with self.assertRaises(runtime.RuntimeFailure):
            runtime.translator(probe(), {"Architecture": "aarch64"})

    def test_rosetta_evidence_is_a_measured_binary(self):
        values = probe()
        values.update(process_exe="/run/rosetta/rosetta", process_elf_machine="b700",
                      process_exe_sha256="b" * 64)
        result = runtime.translator(values, {"Architecture": "aarch64"})
        self.assertEqual(result["name"], "Rosetta for Linux")
        self.assertEqual(result["binary_sha256"], "b" * 64)
        with self.assertRaises(runtime.RuntimeFailure):
            measured(values)  # require-native must not accept Rosetta

    def test_unknown_translator_is_a_provenance_failure(self):
        values = probe()
        values["process_exe"] = "/unknown/translator"
        with self.assertRaisesRegex(runtime.RuntimeFailure, "unresolved"):
            runtime.translator(values, {"Architecture": "aarch64"})

    def test_record_creation_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "RUNTIME.json"
            runtime.write_json(path, {"original": True})
            before = path.read_bytes()
            with self.assertRaises(runtime.RuntimeFailure):
                runtime.write_json(path, {"replacement": True})
            self.assertEqual(before, path.read_bytes())
            alias = Path(tmp) / "alias.json"
            alias.symlink_to(path)
            with self.assertRaises(runtime.RuntimeFailure):
                runtime.write_json(alias, {})

    def test_protected_output_rejected_without_creating_it(self):
        with self.assertRaises(runtime.RuntimeFailure):
            runtime.output_path(runtime.HERE.parent / "human" / "forbidden.json")

    def test_command_failure_and_timeout_retain_raw_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = runtime.Commands(Path(tmp) / "logs")
            result, out, err = log.run([sys.executable, "-c",
                                       "import sys; print('out'); print('err', file=sys.stderr); sys.exit(7)"], check=False)
            self.assertEqual(result["exit"], 7)
            self.assertEqual((out, err), (b"out\n", b"err\n"))
            result, out, _ = log.run([sys.executable, "-u", "-c",
                                     "import time; print('before timeout'); time.sleep(10)"], timeout=0.2, check=False)
            self.assertTrue(result["timed_out"])
            self.assertNotEqual(result["exit"], 0)
            self.assertEqual(out, b"before timeout\n")
            self.assertEqual(len(list(log.directory.glob("*.command.json"))), 2)

    def test_container_timeout_cleans_up_and_mounts_source_readonly(self):
        calls = []

        class Log:
            def run(self, argv, **kwargs):
                calls.append((argv, kwargs))
                return ({"exit": -9, "timed_out": True} if len(calls) == 1 else
                        {"exit": 0, "timed_out": False}), b"", b""

        runtime.container(Log(), "sha256:pin", ["sh", "sweep"],
                          mounts=[(runtime.HERE, "/corpus", True)], timeout=1)
        argv = calls[0][0]
        self.assertIn(f"type=bind,src={runtime.HERE},dst=/corpus,readonly", argv)
        self.assertIn("--read-only", argv)
        self.assertNotIn("-e", argv)  # no silent timezone override
        self.assertEqual(calls[1][0][:3], ["docker", "rm", "--force"])
        self.assertEqual(calls[1][0][3], argv[argv.index("--name") + 1])


class MountBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="kmla-mount-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.human = self.root / "human"
        self.corpus = self.human / "sara/sara"
        self.corpus.mkdir(parents=True)
        self.sentinel = self.human / "sentinel"
        self.sentinel.write_text("stand-in only\n")
        self.harness = self.root / "harness"
        self.harness.mkdir()
        self.out = self.root / "output"
        self.out.mkdir()
        scope = patch.object(runtime, "HERE", self.harness)
        scope.start()
        self.addCleanup(scope.stop)

    def reject(self, mounts):
        log = Mock()
        with self.assertRaises(runtime.RuntimeFailure):
            runtime.container(log, "sha256:pin", ["true"], mounts=mounts)
        log.run.assert_not_called()
        self.assertEqual(self.sentinel.read_text(), "stand-in only\n")

    def test_readonly_protected_mounts_and_disjoint_writable_output(self):
        log = Mock()
        log.run.return_value = ({"exit": 0, "timed_out": False}, b"", b"")
        runtime.container(log, "sha256:pin", ["true"], mounts=[
            (self.human, "/human", True), (self.corpus, "/corpus", True),
            (self.out, "/out", False)])
        argv = log.run.call_args.args[0]
        for source, target, suffix in ((self.human, "/human", ",readonly"),
                                      (self.corpus, "/corpus", ",readonly"),
                                      (self.out, "/out", "")):
            self.assertIn(f"type=bind,src={source},dst={target}{suffix}", argv)

    def test_full_human_mount_is_mandatory_even_for_corpus_only_runner(self):
        mounts = runtime.checked_mounts([(self.corpus, "/corpus", True)])
        self.assertIn((self.human, Path("/human"), True), mounts)
        self.assertIn((self.human, Path("/human"), True), runtime.checked_mounts([]))
        self.reject([(self.corpus, "/human", True)])
        self.reject([(self.out, "/human", True)])
        self.reject([(self.out, "/human/parity", True)])

    def test_writable_protected_root_child_file_and_ancestor_are_rejected(self):
        for source in (self.human, self.corpus, self.sentinel, self.root):
            with self.subTest(source=source):
                self.reject([(source, "/elsewhere", False)])

    def test_symlink_aliases_cannot_hide_protected_sources(self):
        for source in (self.human, self.corpus, self.sentinel, self.root):
            alias = self.out / "alias"
            alias.symlink_to(source)
            self.reject([(alias, "/elsewhere", False)])
            alias.unlink()

    def test_hardlink_aliases_cannot_hide_protected_files(self):
        alias = self.out / "alias"
        os.link(self.sentinel, alias)
        self.reject([(alias, "/elsewhere", False)])
        self.reject([(self.out, "/out", False)])

    def test_host_directory_identity_accounts_for_case_aliases(self):
        alias = self.root / "HUMAN"
        if alias.exists():
            self.assertTrue(alias.samefile(self.human))
            self.reject([(alias, "/elsewhere", False)])
            self.reject([(alias / "sentinel", "/elsewhere", False)])
        else:
            # On case-sensitive hosts this is a distinct, unprotected tree.
            alias.mkdir()
            self.assertIn((alias, Path("/out"), False),
                          runtime.checked_mounts([(alias, "/out", False)]))

    def test_writable_protected_destinations_are_rejected(self):
        for target in ("/human", "/human/parity", "/corpus", "/corpus/cases"):
            with self.subTest(target=target):
                self.reject([(self.out, target, False)])

    def test_readonly_source_aliases_and_destination_shadows_are_rejected(self):
        child = self.harness / "nested"
        child.mkdir()
        for source, target in ((self.harness, "/alias"), (child, "/alias"),
                               (self.out, "/harness/nested"), (self.out, "/harness")):
            for reverse in (False, True):
                mounts = [(self.harness, "/harness", True), (source, target, False)]
                self.reject(list(reversed(mounts)) if reverse else mounts)

    def test_writable_parent_destination_cannot_cover_readonly_child(self):
        self.reject([(self.harness, "/data/harness", True), (self.out, "/data", False)])

    def test_mount_option_injection_and_noncanonical_targets_are_rejected(self):
        for target in ("/out,readonly=false", '/out"', "/out\n", "/out\x00",
                       "relative", "/data/../human", "//human", "/out/", "/"):
            with self.subTest(target=target):
                self.reject([(self.out, target, False)])
        for name in ('bad,source', 'bad"source', 'bad\nsource'):
            source = self.out / name
            source.mkdir()
            self.reject([(source, "/fixture", True)])

    def test_duplicate_targets_and_non_boolean_modes_are_rejected(self):
        self.reject([(self.human, "/human", True), (self.out, "/human", True)])
        for readonly in (None, 0, 1, "false", "true"):
            self.reject([(self.human, "/human", readonly)])


class CorpusTests(unittest.TestCase):
    def test_empty_stderr_does_not_mask_process_failure_or_timeout(self):
        self.assertEqual(run_corpus.classify(1, b"", b""), "process_failure")
        for code in (124, 137):
            self.assertEqual(run_corpus.classify(code, b"", b""), "timeout_or_killed")
        self.assertEqual(run_corpus.classify(0, b"unexpected", b""), "unexpected_stdout")

    def test_zero_exit_does_not_mask_failed_directives_or_loading(self):
        for data, expected in ((b"ERROR: source_sink does not exist", "load_failure"),
                               (b"ERROR: rdiv type error", "error"),
                               (b"Warning: Goal (directive) failed", "directive_failed"),
                               (b"unrecognized warning", "other_stderr")):
            self.assertEqual(run_corpus.classify(0, b"", data), expected)

    def test_interrupted_and_malformed_rows_are_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "interrupted.started").write_text("started\n")
            (directory / "bad.status").write_text("malformed\n")
            (directory / "unexpected.status").write_text("0\t1\t2\n")
            rows, errors = run_corpus.collect_rows(directory, ["missing", "interrupted", "bad"])
            self.assertEqual([r["class"] for r in rows], ["not_run", "incomplete", "invalid_status"])
            self.assertEqual(len(errors), 2)

    def test_status_without_streams_is_not_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "case.started").write_text("started\n")
            (directory / "case.status").write_text("0\t1\t2\n")
            rows, errors = run_corpus.collect_rows(directory, ["case"])
            self.assertEqual(rows[0]["class"], "invalid_status")
            self.assertTrue(errors)

    def test_complete_raw_streams_and_vacuous_annotation(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            case_id = run_corpus.VACUOUS[0]
            for suffix, data in (("started", b"started\n"), ("status", b"0\t1\t2\n"),
                                 ("stdout", b""), ("stderr", b"tab\there\xff\n")):
                (directory / f"{case_id}.{suffix}").write_bytes(data)
            rows, errors = run_corpus.collect_rows(directory, [case_id])
            self.assertFalse(errors)
            self.assertTrue(rows[0]["known_vacuous"])
            self.assertEqual(rows[0]["class"], "other_stderr")
            self.assertEqual((directory / f"{case_id}.stderr").read_bytes(), b"tab\there\xff\n")
            self.assertEqual(rows[0]["stderr_sha256"], runtime.sha256(directory / f"{case_id}.stderr"))

    def test_baseline_requires_every_outcome_and_names_both_vacuous_cases(self):
        ids = [f"case_{i}" for i in range(374)] + list(run_corpus.VACUOUS)
        rows = [{"id": i, "class": "clean", "exit": 0, "known_vacuous": i in run_corpus.VACUOUS} for i in ids]
        success = {"exit": 0, "timed_out": False}
        baseline = run_corpus.report(rows, [], success)
        self.assertTrue(baseline["passed"])
        self.assertEqual(baseline["nonvacuous_cases"], 374)
        self.assertEqual(baseline["known_vacuous_cases"], list(run_corpus.VACUOUS))
        self.assertFalse(run_corpus.report(rows[:-1], [], success)["passed"])
        self.assertFalse(run_corpus.report(rows, [], {"exit": -9, "timed_out": True})["passed"])
        rows[0]["class"] = "timeout_or_killed"
        self.assertFalse(run_corpus.report(rows, [], success)["passed"])

    def test_invalid_budgets_rejected(self):
        for value in ("0", "-1", "nan", "inf"):
            with self.assertRaises(Exception):
                runtime.positive_seconds(value)


if __name__ == "__main__":
    unittest.main()
