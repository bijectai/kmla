# Phase 1 runner boundary — 2026-09-22

Infra sidecar result: protections implemented and locally verified. No semantic
implementation lane was started. Parent commit:
`0a2a65ac1313c180bea39d137e6665c01b8e833a`. The final Docker run occurred at
`2026-09-23T03:48:50.333936719Z` (2026-09-22 in America/New_York).

The parent independently verified the protected manifest and confirmed the
Checkpoint 0 sign-off. Observed manifest SHA-256:
`5ff23beb28eacdf18d4428395e1d96e4fc8123a8f51ae29abc7943bf0f6062b9`.
This sidecar did not inspect the meter source, exploit directory, Oracle source,
or serializer implementation. The meter was checked only for writability, not
read or executed. No real protected write was attempted.

## Scoped files changed

All paths are relative to /Users/devrashie/Documents/csProjects/kmla.

| File | Change |
| --- | --- |
| harness/runtime.py | Mandatory complete /human read-only mount; validate source and destination boundaries before Docker. |
| scripts/test_runtime.py | Temporary stand-in regressions for source/destination overlap, symlink/hard-link/case aliases, shadowing and mount-option injection. |
| scripts/test_runner_boundary.py | Execute actual CI guard against disposable Git histories; verify workflow wiring and empty-manifest rejection; optional live Docker audit. |
| .github/workflows/verify.yml | Fail-closed PR check, label events, mandatory manifest records, runner regressions, pinned Lean setup and both shared checks. |
| .github/workflows/runtime-baseline.yml | Mandatory manifest records, runner regressions and actual Docker boundary audit before corpus execution; retain audit with existing artifacts. |
| docs/phase1/RUNNER_BOUNDARY_2026-09-22.md | This evidence report. |

Other shared-workspace changes belong to the parent/Fable and were not edited by
this sidecar. No repository commit, push, merge, submodule or branch-protection
change was made. Disposable Git fixture commits used only the owner's specified
attribution; they were removed with their temporary directories.

## Enforcement

Every `runtime.container` call now binds the entire installed protected tree to
`/human` read-only, including the meter. Missing protected roots fail before
Docker. A caller cannot substitute a different tree at /human or shadow one of
its descendants. The original corpus remains read-only at /corpus for corpus
execution; unrelated output mounts remain writable.

Writable source roots cannot equal, contain, or lie within protected/read-only
source trees. Symlinks are resolved, filesystem identity checks cover case
aliases on this host, and hard-linked regular files in writable trees are
rejected. Writable destinations cannot overlap /human, /corpus or any explicitly
read-only mount. Duplicate targets, noncanonical destinations, non-boolean modes
and CSV option-injection characters are rejected. Writable-tree traversal uses
metadata only and does not follow directory symlinks.

The existing read-only root filesystem, network=none, dropped capabilities,
no-new-privileges, uid/gid, /tmp tmpfs and working directory are preserved.
No image, interpreter, package, TZ, Lean pin, source program, observation or
comparison was changed.

The PR check compares the PR contribution from its merge base, disables rename
detection so moves out of human are visible, and treats Git failures as failures.
The existing `owner-human-update` label exception uses array membership instead
of comma-joined labels. Adding/removing labels and editing the PR retrigger
verification. A label never bypasses manifest verification.

Both workflows run manifest verification unconditionally and also require at
least one manifest record. A new negative fixture showed that
`scripts/human_manifest.py verify` alone accepts an empty manifest when the
protected tree is also empty. That helper is outside this sidecar's write scope
and is unchanged. The workflow record check closes that CI gap, including
comments-only placeholders; the existing Phase 0 verifier also rejects empty
manifests.

The verify workflow installs the toolchain named by lean-toolchain
(`leanprover/lean4:v4.33.1`), exports ELAN_TOOLCHAIN for subsequent steps, and
runs both `bash scripts/check_interface.sh` and
`bash scripts/check_query_time.sh`. Installation uses the
[official Elan installer](https://lean-lang.org/install/manual/) and
[documented toolchain selection](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/).

The exact installer URL was also verified with a local HTTP GET, without
installing any dependency. The sandboxed request first exited 6 (DNS unavailable);
the same read-only request with authorized network access exited 0:

```sh
curl --fail --silent --show-error --location --max-time 30 --dump-header - --output /dev/null https://elan.lean-lang.org/elan-init.sh
```

Relevant returned headers, verbatim (2026-09-23 UTC / 2026-09-22 local):

```text
HTTP/2 200
server: GitHub.com
content-type: application/x-sh
last-modified: Wed, 26 Aug 2026 10:54:51 GMT
date: Wed, 23 Sep 2026 03:51:01 GMT
content-length: 9823
```

This verifies that the exact configured endpoint currently serves a shell
installer and matches the official installation documentation. The installer
was not executed locally, and this is not a claim that the full CI installation
has run. The installer's own version is not pinned by this change; the Lean
toolchain remains pinned by the repository's lean-toolchain file.

## Exact local commands and results

Commands ran from /Users/devrashie/Documents/csProjects/kmla unless otherwise
stated.

| Command | Result |
| --- | --- |
| `python3 -B scripts/test_runtime.py -v` | Exit 0; 29 tests passed. Original 18 tests passed before edits. |
| `python3 -B scripts/test_runner_boundary.py -v` | Exit 0; 12 tests passed. |
| `python3 -B scripts/test_verify_phase0.py -v` | Exit 0; 10 tests passed. |
| `python3 -B scripts/human_manifest.py --self-test` | Exit 0; 24/24 temporary-tree checks passed. No actual protected-tree write. |
| `bash scripts/check_interface.sh` | Exit 0; pinned 4.33.1, Interface type-checks, 97 behavioural guards passed. |
| `bash scripts/check_query_time.sh` | Exit 0; query-time guards and kernel-checked boundary proofs passed. |
| `git diff --check` | Exit 0; no output. |
| `git diff --exit-code -- lean-toolchain harness/Dockerfile docs/contracts/RUNTIME.json` | Exit 0; pins unchanged. |
| `git diff --name-only -- human` | Exit 0; no output. The independent manifest verification remains the parent's result. |

Both YAML files parsed and every run block passed bash -n (9 verify blocks,
7 runtime-baseline blocks), using this exact command:

```sh
ruby -ryaml -ropen3 -e 'ARGV.each do |path|; data = YAML.load_file(path); count = 0; data.fetch("jobs").each_value do |job|; job.fetch("steps").each do |step|; next unless step["run"]; _, err, status = Open3.capture3("bash", "-n", stdin_data: step["run"]); abort("#{path}: #{step["name"]}: #{err}") unless status.success?; count += 1; end; end; puts "#{path}: YAML parsed; #{count} shell steps pass bash -n"; end' .github/workflows/verify.yml .github/workflows/runtime-baseline.yml
```

Two development failures were retained as findings during the turn: the
empty-tree/empty-manifest test exposed the workflow gap described above; a new
workflow-extraction test initially included the next job's `if:` block and was
fixed to stop at the next YAML peer/ancestor. Each failed once, then passed.
Expectations were not weakened. No test reached three failed edit cycles.

Final source digests from:

```sh
shasum -a 256 harness/runtime.py scripts/test_runtime.py scripts/test_runner_boundary.py .github/workflows/verify.yml .github/workflows/runtime-baseline.yml human/HASHES.txt
```

```text
9bdbc5bd044f909282325801fd19613b493f67de1507ebfbeb024713fa5fbc83  harness/runtime.py
f5c30bbf81f0b434fea6d3303022d87125b6f85b5d628fc16067339f5fcadbd6  scripts/test_runtime.py
dad96ead80744ceb9198b888c7362eeffcb07034e86782024d57781aeab81cb9  scripts/test_runner_boundary.py
088f73d1112da16af567b79187b7d745321c126c5806b7962100de1e50958cfe  .github/workflows/verify.yml
5ff17903abde612eaac25e4e6c75e6e29ee3c7df000b483c5289efca8e46e6f0  .github/workflows/runtime-baseline.yml
5ff23beb28eacdf18d4428395e1d96e4fc8123a8f51ae29abc7943bf0f6062b9  human/HASHES.txt
```

## Actual Docker audit

Initial `docker version --format '{{json .}}'` and image inspection were denied
by the filesystem sandbox. Authorized escalation succeeded; no auto-review
rejection occurred. The daemon is Docker Desktop 4.58.0 / Engine 29.1.5,
Linux arm64, kernel 6.12.65-linuxkit. The pinned recorded image was used by ID;
the mutable kmla-swipl:7.2.3 tag pointed to a different local image and was not
substituted.

Exact final command (exit 0):

```sh
task_run_dir="$(mktemp -d /tmp/kmla-runner-boundary-final.XXXXXX)"
python3 -B scripts/test_runner_boundary.py --probe-runtime docs/contracts/RUNTIME.json --evidence "$task_run_dir/RUNNER_BOUNDARY.json"
```

The generated directory was /tmp/kmla-runner-boundary-final.BMTPzY. Raw command
argv, exit/timeout records, full stdout/stderr, measured runtime and full
docker-inspect output remain under its RUNNER_BOUNDARY.json.diagnostics
directory. The complete summary is embedded below so the central result does
not depend on that temporary directory surviving.

The probe obtains argv from the production launcher, then splits Docker run
into create/inspect/start, removing only --rm to retain inspectable state.
It inspects actual bind sources, RW flags and hardening settings, starts that
container, checks /proc/mounts and `test ! -w /human/parity/check.py`, then
removes only its uniquely named probe container. Overwrite/create/remove
attempts target only /boundary-fixture, a temporary stand-in. Host sentinel
identity is checked afterward; /out is separately confirmed writable.

```json
{
  "schema_version": 1,
  "passed": true,
  "human_writes_attempted": false,
  "diagnostics": "/tmp/kmla-runner-boundary-final.BMTPzY/RUNNER_BOUNDARY.json.diagnostics",
  "runtime_record": "/Users/devrashie/Documents/csProjects/kmla/docs/contracts/RUNTIME.json",
  "runner_source_sha256": "9bdbc5bd044f909282325801fd19613b493f67de1507ebfbeb024713fa5fbc83",
  "probe_source_sha256": "dad96ead80744ceb9198b888c7362eeffcb07034e86782024d57781aeab81cb9",
  "parent_commit": "0a2a65ac1313c180bea39d137e6665c01b8e833a",
  "runtime_identity_sha256": "744cbb885225c77569618a35c4c856f5c4a6c6e4fb6ecb37f7476eb46bbf5c92",
  "runtime_identity_matches": true,
  "image_id": "sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7",
  "runner_argv": [
    "docker",
    "run",
    "--rm",
    "--name",
    "kmla-runtime-028f487cb3cc423a986685b91a0117c5",
    "--platform",
    "linux/amd64",
    "--network",
    "none",
    "--read-only",
    "--tmpfs",
    "/tmp",
    "--cap-drop",
    "ALL",
    "--security-opt",
    "no-new-privileges",
    "--user",
    "501:20",
    "--workdir",
    "/corpus",
    "--mount",
    "type=bind,src=/Users/devrashie/Documents/csProjects/kmla/human,dst=/human,readonly",
    "--mount",
    "type=bind,src=/Users/devrashie/Documents/csProjects/kmla/human/sara/sara,dst=/corpus,readonly",
    "--mount",
    "type=bind,src=/private/var/folders/nb/1nmz4lr56rz3wcmmcgglfyx00000gn/T/kmla-docker-boundary-wcpc3z9o/stand-in,dst=/boundary-fixture,readonly",
    "--mount",
    "type=bind,src=/private/var/folders/nb/1nmz4lr56rz3wcmmcgglfyx00000gn/T/kmla-docker-boundary-wcpc3z9o/output,dst=/out",
    "--entrypoint",
    "sh",
    "sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7",
    "-c",
    "set -eu\nLC_ALL=C\nexport LC_ALL\nawk '$2 == \"/human\" || $2 == \"/corpus\" || $2 == \"/boundary-fixture\" {\n  print $2 \"\\t\" $4; count++; if ($4 !~ /(^|,)ro(,|$)/) bad=1\n} END {if (count != 3 || bad) exit 2}' /proc/mounts\ntest ! -w /human\ntest ! -w /corpus\ntest ! -w /human/parity/check.py\n# The only attempted writes are to a temporary stand-in and /out.\nif (printf 'overwrite\\n' > /boundary-fixture/sentinel) 2>/tmp/rejection; then exit 3; fi\ngrep 'Read-only file system' /tmp/rejection\nif touch /boundary-fixture/new-file 2>/tmp/rejection; then exit 3; fi\ngrep 'Read-only file system' /tmp/rejection\nif rm /boundary-fixture/sentinel 2>/tmp/rejection; then exit 3; fi\ngrep 'Read-only file system' /tmp/rejection\nprintf 'writable output confirmed\\n' > /out/created\nprintf 'Protected mounts inspected without writes; stand-in overwrite/create/remove rejected.\\n'\n"
  ],
  "docker_mounts": [
    {
      "Type": "bind",
      "Source": "/Users/devrashie/Documents/csProjects/kmla/human",
      "Destination": "/human",
      "Mode": "",
      "RW": false,
      "Propagation": "rprivate"
    },
    {
      "Type": "bind",
      "Source": "/Users/devrashie/Documents/csProjects/kmla/human/sara/sara",
      "Destination": "/corpus",
      "Mode": "",
      "RW": false,
      "Propagation": "rprivate"
    },
    {
      "Type": "bind",
      "Source": "/private/var/folders/nb/1nmz4lr56rz3wcmmcgglfyx00000gn/T/kmla-docker-boundary-wcpc3z9o/stand-in",
      "Destination": "/boundary-fixture",
      "Mode": "",
      "RW": false,
      "Propagation": "rprivate"
    },
    {
      "Type": "bind",
      "Source": "/private/var/folders/nb/1nmz4lr56rz3wcmmcgglfyx00000gn/T/kmla-docker-boundary-wcpc3z9o/output",
      "Destination": "/out",
      "Mode": "",
      "RW": true,
      "Propagation": "rprivate"
    }
  ],
  "docker_host_config": {
    "ReadonlyRootfs": true,
    "NetworkMode": "none",
    "CapDrop": [
      "ALL"
    ],
    "SecurityOpt": [
      "no-new-privileges"
    ],
    "Tmpfs": {
      "/tmp": ""
    },
    "Privileged": false
  },
  "probe_stdout": "/human\tro,nosuid,nodev,relatime,fakeowner\n/corpus\tro,nosuid,nodev,relatime,fakeowner\n/boundary-fixture\tro,nosuid,nodev,relatime,fakeowner\nsh: 11: cannot create /boundary-fixture/sentinel: Read-only file system\ntouch: cannot touch '/boundary-fixture/new-file': Read-only file system\nrm: cannot remove '/boundary-fixture/sentinel': Read-only file system\nProtected mounts inspected without writes; stand-in overwrite/create/remove rejected.\n",
  "probe_stderr": "",
  "container_state": {
    "Status": "exited",
    "Running": false,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 0,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2026-09-23T03:48:50.333936719Z",
    "FinishedAt": "2026-09-23T03:48:50.507746261Z"
  },
  "standin_unchanged": true,
  "disjoint_output_writable": true,
  "cleanup_exit": 0
}
```

## Exact limits and handoff

- This establishes the shared Docker launcher boundary, not a sandbox around
  host-side agent tools or every possible direct Docker command. The host,
  Docker daemon and output-tree lifecycle remain trusted; path checks do not
  prevent a hostile host from swapping paths/links after validation or mounting
  privileged services. Keep output directories dedicated and disjoint.
- Read-only is not confidentiality. The complete protected bundle is visible
  to the container. The separate prohibition on inspecting meter source and
  exploits remains binding; context isolation between semantic lanes is still
  the parent's responsibility.
- P-BUNDLE remains detection-only. A PR can alter its own workflows/verifier.
  The existing label's governance is trusted, not a cryptographic owner
  attestation. Direct pushes run integrity checks but have no PR-label
  authorization check. No ruleset, required-review or submodule change is made.
- The local Docker evidence uses the approved Rosetta runtime and is not a new
  native-amd64 run. Updated GitHub workflows, the CI installer and the native
  boundary step have not been dispatched in this turn. They must run on the
  next authorized push/PR. YAML/bash parsing and local regressions are not
  hosted Actions execution.
- This audit does not claim meter conformance, corpus parity, semantic
  round trips, R5 coverage/termination, any phase gate or checkpoint sign-off.
  The parent owns manifest verification, shared-interface development and
  the current Fable review. Shared checks are point-in-time results in an
  actively edited workspace.
- No protected write probes, protected source edits, case filters, semantic
  changes, commits, pushes or merges were performed. Runtime archival
  obligations remain unchanged.

Self-review: no new assumptions about Prolog clause semantics, rounding, NAF,
cut, recursion or serialization were introduced. The approved runtime identity
is assumed authoritative and was measured unchanged. The mount and CI checks
are infrastructure evidence only. Circuit breaker: three failed edit cycles
on one test means stop and report; no test reached that threshold.
