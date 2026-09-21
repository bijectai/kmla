#!/usr/bin/env python3
"""Bounded Docker measurements and immutable local runtime records (P-RUNTIME)."""

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time
import uuid

HERE = Path(__file__).resolve().parent
TZ = "America/New_York"
VERSION = "7.2.3"
PACKAGE = "7.2.3+dfsg-6"
PLATFORM = "linux/amd64"
BASE = "sha256:c5c5200ff1e9c73ffbf188b4a67eb1c91531b644856b4aefe86a58d2f0cb05be"
LABEL = "org.kmla.runtime.dockerfile-sha256"


class RuntimeFailure(Exception):
    pass


def sha256(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def identity(record):
    """Future fields participate automatically; exactly one field is excluded."""
    result = copy.deepcopy(record)
    result["image"].pop("local_image_id", None)
    return result


def identity_sha256(record):
    data = json.dumps(identity(record), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def output_path(path):
    path = Path(path).absolute()
    if "human" in path.parts or "human" in path.resolve().parts:
        raise RuntimeFailure(f"protected output path: {path}")
    if path.exists() or path.is_symlink():
        raise RuntimeFailure(f"refusing to overwrite existing record/diagnostics: {path}")
    return path


def write_json(path, value):
    path = output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def positive_seconds(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be finite and greater than zero")
    return number


class Commands:
    """Retain argv, timeout/exit, elapsed time and complete raw stdout/stderr."""

    def __init__(self, directory):
        self.directory = output_path(directory)
        self.directory.mkdir(parents=True)
        self.number = 0

    def run(self, argv, *, timeout=60, check=True):
        self.number += 1
        stem = f"{self.number:03d}"
        stdout = self.directory / f"{stem}.stdout"
        stderr = self.directory / f"{stem}.stderr"
        result = {"argv": [str(x) for x in argv], "timeout_seconds": timeout,
                  "exit": None, "timed_out": False, "stdout": stdout.name,
                  "stderr": stderr.name}
        start = time.monotonic()
        with stdout.open("xb") as out, stderr.open("xb") as err:
            try:
                process = subprocess.Popen(result["argv"], stdout=out, stderr=err,
                                           stdin=subprocess.DEVNULL, start_new_session=True)
                try:
                    result["exit"] = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    result["timed_out"] = True
                    os.killpg(process.pid, signal.SIGKILL)
                    result["exit"] = process.wait()
            except OSError as error:
                result["error"] = str(error)
        result["elapsed_seconds"] = round(time.monotonic() - start, 6)
        write_json(self.directory / f"{stem}.command.json", result)
        if check and (result["timed_out"] or result["exit"] != 0):
            raise RuntimeFailure(f"command failed: {result}; see {self.directory}")
        return result, stdout.read_bytes(), stderr.read_bytes()

    def json(self, argv):
        _, out, _ = self.run(argv)
        return json.loads(out)


def container(log, image, command, *, mounts=(), timeout=60):
    name = "kmla-runtime-" + uuid.uuid4().hex
    argv = ["docker", "run", "--rm", "--name", name, "--platform", PLATFORM,
            "--network", "none", "--read-only", "--tmpfs", "/tmp",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}", "--workdir", "/corpus"]
    for source, target, readonly in mounts:
        source = str(Path(source).resolve())
        if "," in source:
            raise RuntimeFailure("Docker mount paths containing commas are unsupported")
        argv += ["--mount", f"type=bind,src={source},dst={target}" + (",readonly" if readonly else "")]
    argv += ["--entrypoint", command[0], image, *command[1:]]
    result, out, err = log.run(argv, timeout=timeout, check=False)
    if result["timed_out"]:
        # Killing the Docker client does not stop its container. Remove only ours.
        cleanup, _, _ = log.run(["docker", "rm", "--force", name], timeout=20, check=False)
        result["cleanup_exit"] = cleanup["exit"]
    return result, out, err


def parse_probe(data):
    values = {}
    for line in data.decode("utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) != 2 or fields[0] in values:
            raise RuntimeFailure(f"malformed/duplicate probe row: {line!r}")
        values[fields[0]] = fields[1]
    return values


def parse_packages(data):
    packages = []
    seen = set()
    for line in data.decode("utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) != 4 or not all(fields) or fields[0] in seen or fields[3] != "installed":
            raise RuntimeFailure(f"malformed, duplicate or uninstalled package row: {line!r}")
        seen.add(fields[0])
        packages.append(dict(zip(("name", "version", "architecture", "status"), fields)))
    approved = [p for p in packages if p["name"] == "swi-prolog-nox"]
    if len(approved) != 1 or approved[0]["version"] != PACKAGE or approved[0]["architecture"] != "amd64":
        raise RuntimeFailure(f"expected installed swi-prolog-nox={PACKAGE} for amd64")
    return sorted(packages, key=lambda p: p["name"])


def translator(probe, daemon):
    evidence = {key: probe[key] for key in (
        "process_exe", "process_exe_sha256", "process_elf_machine", "swipl_exe", "swipl_exe_sha256")}
    evidence["docker_daemon_architecture"] = daemon["Architecture"]
    for field in ("process_exe_sha256", "swipl_exe_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", evidence[field]):
            raise RuntimeFailure(f"invalid executable digest: {field}")
    exe = probe["process_exe"]
    if (daemon["Architecture"] in ("amd64", "x86_64") and
            probe["process_elf_machine"] == "3e00" and
            exe == probe["swipl_exe"] and
            probe["process_exe_sha256"] == probe["swipl_exe_sha256"]):
        return {"name": "none (native amd64)", "kind": "native", "evidence": evidence}
    if (exe == "/run/rosetta/rosetta" and probe["process_elf_machine"] == "b700" and
            daemon["Architecture"] in ("aarch64", "arm64")):
        return {"name": "Rosetta for Linux", "kind": "translation",
                "binary_sha256": probe["process_exe_sha256"], "evidence": evidence}
    if re.fullmatch(r"qemu-x86_64(?:-static)?", Path(exe).name):
        return {"name": "QEMU linux-user x86_64", "kind": "translation",
                "binary_sha256": probe["process_exe_sha256"], "evidence": evidence}
    raise RuntimeFailure(f"translator identity unresolved; retain evidence and report: {evidence}")


def measure(log, image, tag, require_native=False):
    metadata = log.json(["docker", "image", "inspect", image])[0]
    if metadata["Os"] != "linux" or metadata["Architecture"] != "amd64":
        raise RuntimeFailure("image must be linux/amd64")
    dockerfile_sha = sha256(HERE / "Dockerfile")
    if (metadata.get("Config", {}).get("Labels") or {}).get(LABEL) != dockerfile_sha:
        raise RuntimeFailure("image lacks the current Dockerfile build label; rebuild and retain a new record")
    daemon = log.json(["docker", "info", "--format", "{{json .}}"])
    if daemon["OSType"] != "linux":
        raise RuntimeFailure("Docker daemon must run Linux")
    result, out, err = container(log, metadata["Id"], ["sh", "/harness/runtime_probe.sh"],
                                 mounts=[(HERE, "/harness", True)])
    if result["timed_out"] or result["exit"] != 0 or err:
        raise RuntimeFailure("runtime probe failed; see retained command diagnostics")
    probe = parse_probe(out)
    expected = {"version_string": "SWI-Prolog version 7.2.3 for amd64", "plarch": "amd64",
                "plversion": "70203", "uname_m": "x86_64", "dpkg_arch": "amd64", "tz": TZ,
                "winter_offset": "-0500", "summer_offset": "-0400"}
    for key, value in expected.items():
        if probe.get(key) != value:
            raise RuntimeFailure(f"runtime {key}: got {probe.get(key)!r}, expected {value!r}")
    if not re.fullmatch(r"[0-9a-f]{64}", probe.get("tz_sha256", "")):
        raise RuntimeFailure("missing timezone data digest")
    fmt = "${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Status}\n"
    result, out, err = container(log, metadata["Id"], ["dpkg-query", "-W", "-f", fmt])
    if result["timed_out"] or result["exit"] != 0 or err:
        raise RuntimeFailure("package closure measurement failed")
    packages = parse_packages(out)
    execution = translator(probe, daemon)
    if require_native and execution["kind"] != "native":
        raise RuntimeFailure("native amd64 CI baseline requested, but a translator is active")
    return {
        "schema_version": 2,
        "interpreter": {"version_string": probe["version_string"], "version": VERSION,
                        "plarch": probe["plarch"], "uname_m": probe["uname_m"],
                        "debian_package_version": PACKAGE, "installed_packages": packages,
                        "verified_from_inside_container": True},
        "image": {"tag": tag, "local_image_id": metadata["Id"],
                  "base_image_digest": BASE, "dockerfile_sha256": dockerfile_sha,
                  "platform": PLATFORM, "repo_digests": sorted(metadata.get("RepoDigests") or [])},
        "environment": {"TZ": probe["tz"], "tzdata_sha256": probe["tz_sha256"],
                        "winter_offset": probe["winter_offset"], "summer_offset": probe["summer_offset"],
                        "client_os": platform.system(), "client_arch": platform.machine(),
                        "docker_daemon_arch": daemon["Architecture"],
                        "docker_server_version": daemon["ServerVersion"], "translator": execution},
        "provenance_caveats": [
            "Debian swi-prolog-nox=7.2.3+dfsg-6 includes Debian repackaging and patches.",
            "Identity is the whole record except image.local_image_id; future fields participate.",
            "A local image config ID is not a registry manifest digest. Publication is a separate archival step.",
            "Packages currently come from archive.debian.org; vendoring the full closure and image export are outstanding archival work.",
            "APT Check-Valid-Until is disabled for expired stretch metadata; signature checks remain enabled.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", nargs="?", default="kmla-swipl:7.2.3")
    parser.add_argument("--out", type=Path, required=True, help="NEW RUNTIME.json; never overwritten")
    parser.add_argument("--require-native", action="store_true")
    parser.add_argument("--build-timeout", type=positive_seconds, default=900)
    args = parser.parse_args()
    log = None
    try:
        out = output_path(args.out)
        if os.environ.get("KMLA_TZ") != TZ:
            raise RuntimeFailure(f"set KMLA_TZ={TZ}; the approved build argument has no default")
        log = Commands(str(out) + ".diagnostics")
        if f"debian:stretch@{BASE}" not in (HERE / "Dockerfile").read_text():
            raise RuntimeFailure("Dockerfile no longer contains the approved base digest")
        log.run(["docker", "build", "--platform", PLATFORM, "--build-arg", f"KMLA_TZ={TZ}",
                 "--label", f"{LABEL}={sha256(HERE / 'Dockerfile')}", "-t", args.tag,
                 "-f", str(HERE / "Dockerfile"), str(HERE)], timeout=args.build_timeout)
        record = measure(log, args.tag, args.tag, args.require_native)
        write_json(out, record)
        print(f"Recorded {out}; identity SHA-256 {identity_sha256(record)}")
        return 0
    except (RuntimeFailure, OSError, ValueError, KeyError, IndexError) as error:
        if log is not None:
            write_json(log.directory / "failure.json", {"error": str(error)})
        print(f"FAIL: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
