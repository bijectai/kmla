#!/usr/bin/env python3
"""Infra regressions and opt-in Docker mount evidence; no semantic lanes.

Default: execute the actual CI protection fragment against temporary Git trees.
--probe-runtime RUNTIME.json --evidence NEW.json: inspect a real container built
from runtime.container's argv, then launch it. Write rejection is tested only
against a temporary stand-in; real human mounts are inspected without writes.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))
import runtime

VERIFY = ROOT / ".github/workflows/verify.yml"
BASELINE = ROOT / ".github/workflows/runtime-baseline.yml"


def workflow_step(path, name):
    # Extract the exact YAML literal shell step, without a third-party parser.
    text = path.read_text(encoding="utf-8")
    block = text.split(f"      - name: {name}\n", 1)[1]
    return re.split(r"\n(?=\S| {1,6}\S)", block, maxsplit=1)[0]


def protection_script():
    block = workflow_step(VERIFY, "Refuse a pull request that modifies human/")
    body = block.split("        run: |\n", 1)[1]
    return "\n".join(line[10:] for line in body.splitlines())


class ProtectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="kmla-ci-boundary-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # Git histories exist only in disposable stand-ins, never the workspace.
        self.env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_AUTHOR_NAME": "Devakh Rashie", "GIT_COMMITTER_NAME": "Devakh Rashie",
                    "GIT_AUTHOR_EMAIL": "59419810+arkanemystic@users.noreply.github.com",
                    "GIT_COMMITTER_EMAIL": "59419810+arkanemystic@users.noreply.github.com"}
        self.git("init", "-q")
        (self.root / "human").mkdir()
        (self.root / "human/sentinel").write_text("owner stand-in\n")
        self.base = self.commit()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, env=self.env,
                              check=True, capture_output=True, text=True, timeout=10).stdout.strip()

    def commit(self):
        self.git("add", "--all")
        self.git("-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                 "commit", "-qm", "temporary boundary fixture")
        return self.git("rev-parse", "HEAD")

    def guard(self, head, *, base=None, owner="false"):
        return subprocess.run(["bash", "-c", protection_script()], cwd=self.root,
                              env={**self.env, "BASE": base or self.base, "HEAD": head,
                                   "OWNER_HUMAN_UPDATE": owner},
                              capture_output=True, text=True, timeout=10)

    def test_unrelated_change_is_allowed(self):
        (self.root / "other").write_text("not protected\n")
        result = self.guard(self.commit())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_protected_change_requires_exact_owner_authorization(self):
        (self.root / "human/sentinel").write_text("changed stand-in\n")
        head = self.commit()
        for owner, expected in (("false", 1), ("true", 0), ("prefix,true,suffix", 1)):
            with self.subTest(owner=owner):
                self.assertEqual(self.guard(head, owner=owner).returncode, expected)

    def test_move_out_of_protected_tree_is_rejected(self):
        (self.root / "human/sentinel").rename(self.root / "moved")
        self.assertEqual(self.guard(self.commit()).returncode, 1)

    def test_new_protected_file_is_rejected(self):
        (self.root / "human/new-file").write_text("stand-in\n")
        self.assertEqual(self.guard(self.commit()).returncode, 1)

    def test_git_failure_is_not_no_changes_even_with_label(self):
        for owner in ("false", "true"):
            result = self.guard("missing-ref", owner=owner)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Cannot determine protected changes", result.stdout)

    def test_base_branch_owner_change_does_not_taint_unrelated_pr(self):
        (self.root / "human/sentinel").write_text("base branch owner update\n")
        new_base = self.commit()
        self.git("checkout", "--detach", self.base)
        (self.root / "other").write_text("PR contribution\n")
        self.assertEqual(self.guard(self.commit(), base=new_base).returncode, 0)

    def test_equal_tip_files_do_not_hide_pr_protected_change(self):
        (self.root / "human/sentinel").write_text("same change on both branches\n")
        new_base = self.commit()
        self.git("checkout", "--detach", self.base)
        (self.root / "human/sentinel").write_text("same change on both branches\n")
        (self.root / "other").write_text("distinct PR commit\n")
        self.assertEqual(self.guard(self.commit(), base=new_base).returncode, 1)


class WorkflowTests(unittest.TestCase):
    def test_manifest_is_unconditional_in_both_workflows(self):
        for path in (VERIFY, BASELINE):
            block = workflow_step(path, "Protected-artifact manifest")
            self.assertNotIn("if:", block)
            self.assertIn("run: python3 -B scripts/human_manifest.py verify", block)
            self.assertLess(path.read_text().index("name: Protected-artifact manifest"),
                            path.read_text().index("name: " + (
                                "Phase 0 acceptance checks" if path == VERIFY else "Runtime regression tests")))

    def test_label_changes_recheck_the_existing_owner_exception(self):
        text = VERIFY.read_text()
        events = re.search(r"pull_request:\s+types: \[(.*?)\]", text).group(1)
        self.assertTrue({"opened", "synchronize", "reopened", "labeled", "unlabeled", "edited"}
                        <= {s.strip() for s in events.split(",")})
        self.assertIn("contains(github.event.pull_request.labels.*.name, 'owner-human-update')", text)
        self.assertNotIn("join(github.event.pull_request.labels", text)

    def test_boundary_tests_and_live_probe_are_wired_into_ci(self):
        for path in (VERIFY, BASELINE):
            self.assertIn("python3 -B scripts/test_runner_boundary.py -v", path.read_text())
            self.assertIn("python3 -B scripts/test_runtime.py -v", path.read_text())
        self.assertIn('--probe-runtime "$RUN_DIR/RUNTIME.json"', BASELINE.read_text())

    def test_shared_checks_use_the_pinned_lean_toolchain(self):
        text = VERIFY.read_text()
        install = workflow_step(VERIFY, "Install the pinned Lean toolchain")
        self.assertIn('toolchain="$(cat lean-toolchain)"', install)
        self.assertIn('elan toolchain install "$toolchain"', install)
        self.assertIn('echo "ELAN_TOOLCHAIN=$toolchain" >> "$GITHUB_ENV"', install)
        for name, command in (("Shared Interface guards", "bash scripts/check_interface.sh"),
                              ("Query-time guards", "bash scripts/check_query_time.sh")):
            block = workflow_step(VERIFY, name)
            self.assertNotIn("if:", block)
            self.assertIn(f"run: {command}", block)
            self.assertLess(text.index("name: Install the pinned Lean toolchain"),
                            text.index(f"name: {name}"))

    def test_manifest_rejects_missing_empty_and_drifted_standin(self):
        with tempfile.TemporaryDirectory(prefix="kmla-manifest-boundary-") as directory:
            root = Path(directory)
            command = [sys.executable, "-B", str(ROOT / "scripts/human_manifest.py"),
                       "verify", "--repo-root", directory]

            def verify():
                results = []
                for workflow in (VERIFY, BASELINE):
                    step = workflow_step(workflow, "Require installed manifest records")
                    body = step.split("        run: |\n", 1)[1]
                    shell = "\n".join(line[10:] for line in body.splitlines())
                    check = subprocess.run(["bash", "-e", "-c", shell], cwd=root,
                                           capture_output=True, text=True, timeout=10)
                    results.append(check if check.returncode else subprocess.run(
                        command, capture_output=True, text=True, timeout=10))
                return results

            def assert_verifies(expected):
                for workflow, result in zip((VERIFY, BASELINE), verify()):
                    with self.subTest(workflow=workflow.name, expected=expected):
                        self.assertEqual(result.returncode == 0, expected, result.stderr)

            assert_verifies(False)
            (root / "human").mkdir()
            manifest = root / "human/HASHES.txt"
            manifest.write_text("")
            assert_verifies(False)
            manifest.write_text("# placeholder\n")
            assert_verifies(False)
            sentinel = root / "human/sentinel"
            sentinel.write_text("fixture\n")
            manifest.write_text(runtime.sha256(sentinel) + "  sentinel\n")
            assert_verifies(True)
            sentinel.write_text("drift\n")
            assert_verifies(False)


PROBE = r'''set -eu
LC_ALL=C
export LC_ALL
awk '$2 == "/human" || $2 == "/corpus" || $2 == "/boundary-fixture" {
  print $2 "\t" $4; count++; if ($4 !~ /(^|,)ro(,|$)/) bad=1
} END {if (count != 3 || bad) exit 2}' /proc/mounts
test ! -w /human
test ! -w /corpus
test ! -w /human/parity/check.py
# The only attempted writes are to a temporary stand-in and /out.
if (printf 'overwrite\n' > /boundary-fixture/sentinel) 2>/tmp/rejection; then exit 3; fi
grep 'Read-only file system' /tmp/rejection
if touch /boundary-fixture/new-file 2>/tmp/rejection; then exit 3; fi
grep 'Read-only file system' /tmp/rejection
if rm /boundary-fixture/sentinel 2>/tmp/rejection; then exit 3; fi
grep 'Read-only file system' /tmp/rejection
printf 'writable output confirmed\n' > /out/created
printf 'Protected mounts inspected without writes; stand-in overwrite/create/remove rejected.\n'
'''


def docker_probe(record_path, evidence_path):
    evidence_path = runtime.output_path(evidence_path)
    log = runtime.Commands(str(evidence_path) + ".diagnostics")
    evidence = {"schema_version": 1, "passed": False, "human_writes_attempted": False,
                "diagnostics": str(log.directory), "runtime_record": str(record_path.resolve()),
                "runner_source_sha256": runtime.sha256(runtime.HERE / "runtime.py"),
                "probe_source_sha256": runtime.sha256(__file__)}
    try:
        _, parent, _ = log.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
        evidence["parent_commit"] = parent.decode("ascii").strip()
        expected = json.loads(record_path.read_text(encoding="utf-8"))
        current = runtime.measure(log, expected["image"]["local_image_id"], expected["image"]["tag"])
        runtime.write_json(log.directory / "RUNTIME.measured.json", current)
        if runtime.identity(current) != runtime.identity(expected):
            raise runtime.RuntimeFailure("runtime differs from supplied record; no substitution allowed")
        evidence["runtime_identity_sha256"] = runtime.identity_sha256(current)
        evidence["runtime_identity_matches"] = True
        evidence["image_id"] = current["image"]["local_image_id"]
        with tempfile.TemporaryDirectory(prefix="kmla-docker-boundary-") as directory:
            root = Path(directory).resolve()
            fixture, out = root / "stand-in", root / "output"
            fixture.mkdir()
            out.mkdir()
            sentinel = fixture / "sentinel"
            sentinel.write_text("temporary stand-in only\n")
            before = runtime.sha256(sentinel)

            class Capture:
                def run(self, argv, **kwargs):
                    self.argv = argv
                    return {"exit": 0, "timed_out": False}, b"", b""

            capture = Capture()
            runtime.container(capture, evidence["image_id"], ["sh", "-c", PROBE], mounts=[
                (ROOT / "human", "/human", True),
                (ROOT / "human/sara/sara", "/corpus", True),
                (fixture, "/boundary-fixture", True), (out, "/out", False)])
            evidence["runner_argv"] = capture.argv
            # Split run into create/inspect/start to retain the actual Docker
            # configuration before exit/removal. All runtime options are kept.
            create = ["docker", "create", *capture.argv[2:]]
            create.remove("--rm")
            name = create[create.index("--name") + 1]
            try:
                log.run(create)
                info = log.json(["docker", "inspect", name])[0]
                runtime.write_json(log.directory / "docker-inspect.json", info)
                evidence["docker_mounts"] = info["Mounts"]
                host = info["HostConfig"]
                evidence["docker_host_config"] = {key: host[key] for key in (
                    "ReadonlyRootfs", "NetworkMode", "CapDrop", "SecurityOpt", "Tmpfs", "Privileged")}
                mounts = {m["Destination"]: m for m in info["Mounts"]}
                for source, target, readonly in runtime.checked_mounts([
                        (ROOT / "human", "/human", True),
                        (ROOT / "human/sara/sara", "/corpus", True),
                        (fixture, "/boundary-fixture", True), (out, "/out", False)]):
                    mount = mounts[str(target)]
                    if (mount["Type"] != "bind" or mount["Source"] != str(source) or
                            mount["RW"] != (not readonly)):
                        raise runtime.RuntimeFailure(f"unexpected Docker mount: {mount}")
                if (not host["ReadonlyRootfs"] or host["NetworkMode"] != "none" or
                        host["Privileged"] or not any(c.upper() == "ALL" for c in host["CapDrop"]) or
                        "no-new-privileges" not in host["SecurityOpt"] or
                        info["Config"]["User"] != f"{os.getuid()}:{os.getgid()}"):
                    raise runtime.RuntimeFailure("Docker runner hardening flags do not match")
                _, stdout, stderr = log.run(["docker", "start", "--attach", name])
                evidence["probe_stdout"] = stdout.decode("utf-8")
                evidence["probe_stderr"] = stderr.decode("utf-8")
                state = log.json(["docker", "inspect", "--format", "{{json .State}}", name])
                evidence["container_state"] = state
                if state["ExitCode"] != 0 or state["Running"] or state.get("OOMKilled") or stderr:
                    raise runtime.RuntimeFailure("Docker mount probe did not complete cleanly")
                if runtime.sha256(sentinel) != before or (fixture / "new-file").exists():
                    raise runtime.RuntimeFailure("read-only stand-in was changed")
                if (out / "created").read_text() != "writable output confirmed\n":
                    raise runtime.RuntimeFailure("disjoint output is not writable")
                evidence["standin_unchanged"] = True
                evidence["disjoint_output_writable"] = True
                evidence["passed"] = True
            finally:
                cleanup, _, _ = log.run(["docker", "rm", "--force", name], timeout=20, check=False)
                evidence["cleanup_exit"] = cleanup["exit"]
                if cleanup["exit"] != 0 or cleanup["timed_out"]:
                    evidence["passed"] = False
                    raise runtime.RuntimeFailure("probe container cleanup failed; see diagnostics")
    except (runtime.RuntimeFailure, OSError, ValueError, KeyError, IndexError) as error:
        evidence["error"] = str(error)
    runtime.write_json(evidence_path, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if evidence["passed"] else 1


if __name__ == "__main__":
    if "--probe-runtime" in sys.argv:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--probe-runtime", type=Path, required=True)
        parser.add_argument("--evidence", type=Path, required=True)
        args = parser.parse_args()
        sys.exit(docker_probe(args.probe_runtime, args.evidence))
    unittest.main()
