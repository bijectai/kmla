#!/usr/bin/env python3
"""Run the G6 diagnostic's commands in the pinned runtime and keep raw evidence.

Each command is one `docker run` of the pinned image by ID, with the corpus
mounted read-only at /corpus (the working directory), this directory mounted
read-only at /audit, no network, a read-only root and a tmpfs /tmp. For each
command, commands/NNN.command.json records argv, timeout, exit status,
whether it timed out and elapsed seconds; NNN.stdout and NNN.stderr hold the
streams verbatim. identity.json records host, image and in-container identity.
Diagnosis only: nothing under human/ is written, and no result is interpreted
here.
"""
import hashlib, json, os, platform, subprocess, sys, time, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
IMAGE = "sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7"
TIMEOUT = 300
PROBES = [  # (household file, probe label) in execution order
    ("household.pl", "root_tax"),
    ("household.pl", "s3301"),
    ("household.pl", "s3306_a"),
    ("household.pl", "s3306_c"),
    ("household.pl", "s3306_a_3"),
    ("household.pl", "root_tax_bob"),
    ("household_control.pl", "root_tax"),
    ("household.pl", "v5_is_child_of"),
    ("household.pl", "v10_s152_c_2"),
    ("household.pl", "v8_s151_c_applies"),
]


def base(name):
    return ["docker", "run", "--rm", "--name", name, "--platform", "linux/amd64",
            "--network", "none", "--read-only", "--tmpfs", "/tmp", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
            "--workdir", "/corpus",
            "--mount", f"type=bind,src={REPO}/human/sara/sara,dst=/corpus,readonly",
            "--mount", f"type=bind,src={HERE},dst=/audit,readonly"]


def run(n, argv, name):
    out = HERE / "commands"
    out.mkdir(exist_ok=True)
    start = time.monotonic()
    try:
        proc = subprocess.run(argv, capture_output=True, timeout=TIMEOUT)
        code, timed_out, so, se = proc.returncode, False, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as expired:
        subprocess.run(["docker", "kill", name], capture_output=True)
        code, timed_out, so, se = None, True, expired.stdout or b"", expired.stderr or b""
    elapsed = round(time.monotonic() - start, 3)
    (out / f"{n:03d}.stdout").write_bytes(so)
    (out / f"{n:03d}.stderr").write_bytes(se)
    record = {"argv": argv, "timeout_seconds": TIMEOUT, "exit": code, "timed_out": timed_out,
              "stdout": f"{n:03d}.stdout", "stderr": f"{n:03d}.stderr", "elapsed_seconds": elapsed}
    (out / f"{n:03d}.command.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"{n:03d} exit={code} timed_out={timed_out} elapsed={elapsed}s  {argv[-4:]}", flush=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    probe_script = ("uname -m; readlink /proc/self/exe; "
                    "if [ -e /run/rosetta/rosetta ]; then sha256sum /run/rosetta/rosetta; fi; "
                    "swipl --version; echo TZ=$TZ; date -d 2017-01-15 +%z; date -d 2017-07-15 +%z; "
                    "sha256sum /usr/share/zoneinfo/America/New_York; "
                    "cd /corpus/statutes/prolog && sha256sum *.pl")
    name = "kmla-g6-" + uuid.uuid4().hex[:12]
    run(0, base(name) + ["--entrypoint", "sh", IMAGE, "-c", probe_script], name)
    for i, (household, label) in enumerate(PROBES, 1):
        name = "kmla-g6-" + uuid.uuid4().hex[:12]
        run(i, base(name) + ["--entrypoint", "swipl", IMAGE, "-q", "-f", "none", "-s",
                             "/audit/g6_domestic.pl", "-g", f"main('{household}',{label})",
                             "-t", "halt"], name)
    inspect = json.loads(subprocess.run(["docker", "image", "inspect", IMAGE], capture_output=True,
                                        check=True).stdout)[0]
    version = subprocess.run(["docker", "version", "--format", "{{.Server.Version}} {{.Server.Arch}}"],
                             capture_output=True, text=True).stdout.strip()
    identity = {
        "image_id": inspect["Id"], "image_platform": f'{inspect["Os"]}/{inspect["Architecture"]}',
        "image_repo_tags": inspect.get("RepoTags"), "image_labels": inspect["Config"].get("Labels"),
        "image_env": inspect["Config"].get("Env"),
        "runtime_record": "docs/contracts/RUNTIME.json",
        "runtime_record_sha256": sha(REPO / "docs/contracts/RUNTIME.json"),
        "decisions_sha256": sha(REPO / "human/DECISIONS.md"),
        "manifest_sha256": sha(REPO / "human/HASHES.txt"),
        "host": {"os": platform.system(), "machine": platform.machine(), "docker_server": version},
        "emulated": platform.machine() != "x86_64",
        "inputs_sha256": {p.name: sha(p) for p in sorted(HERE.glob("*.pl"))},
        "scope": "G6 definedness diagnosis only (A-025, R-Q025); no V-rule, exclusion or reference answer",
    }
    (HERE / "identity.json").write_text(json.dumps(identity, indent=2) + "\n")
    print("identity.json written; emulated =", identity["emulated"])


if __name__ == "__main__":
    sys.exit(main())
