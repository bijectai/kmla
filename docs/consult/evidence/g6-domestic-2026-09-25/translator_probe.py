#!/usr/bin/env python3
"""Supplementary identity probe: which translator ran the amd64 image.

Command 000's `readlink /proc/self/exe` names readlink itself, so it cannot tell
Rosetta from QEMU. This probe starts a background amd64 process and reads its
/proc/<pid>/exe and interpreter, as docs/contracts/RUNTIME.json's translator
evidence does. Output goes to commands/011.* through run.py's recorder.
"""
import sys, uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run as runner

script = ("sleep 3 & pid=$!; sleep 0.5; echo exe=$(readlink /proc/$pid/exe); "
          "if [ -e /run/rosetta/rosetta ]; then echo rosetta_present=yes; sha256sum /run/rosetta/rosetta; "
          "else echo rosetta_present=no; fi; "
          "grep -m1 -E 'rosetta|qemu' /proc/$pid/maps || echo no_rosetta_or_qemu_mapping; wait")
name = "kmla-g6-" + uuid.uuid4().hex[:12]
if "--only-014" not in sys.argv:
    runner.run(11, runner.base(name) + ["--entrypoint", "sh", runner.IMAGE, "-c", script], name)

# Command 014: digest the translator and interpreter through the running
# process's /proc/<pid>/exe link (the path itself is not visible in the
# container), for comparison with RUNTIME.json's translator record.
script = ("swipl -q -g 'sleep(3)' -t halt & pid=$!; sleep 1; echo exe=$(readlink /proc/$pid/exe); "
          "sha256sum /proc/$pid/exe; sha256sum /usr/lib/swi-prolog/bin/amd64/swipl; wait")
name = "kmla-g6-" + uuid.uuid4().hex[:12]
runner.run(14, runner.base(name) + ["--entrypoint", "sh", runner.IMAGE, "-c", script], name)
