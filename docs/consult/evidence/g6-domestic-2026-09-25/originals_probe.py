#!/usr/bin/env python3
"""Measure the candidate G6 region on all 376 originals (command 012).

Runs g6_originals.pl once in the pinned runtime, with the same mounts and
restrictions as run.py, and records it through run.py's recorder. It measures
the effect on the originals for the exclusion proposal and implements nothing.
"""
import sys, uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run as runner

runner.TIMEOUT = 1800
name = "kmla-g6-" + uuid.uuid4().hex[:12]
runner.run(12, runner.base(name) + ["--entrypoint", "swipl", runner.IMAGE, "-q", "-f", "none",
                                     "-s", "/audit/g6_originals.pl", "-g", "main", "-t", "halt"], name)

name = "kmla-g6-" + uuid.uuid4().hex[:12]
runner.run(13, runner.base(name) + ["--entrypoint", "swipl", runner.IMAGE, "-q", "-f", "none",
                                     "-s", "/audit/g6_originals.pl", "-g",
                                     "main_files(['/audit/household.pl','/audit/household_control.pl'])",
                                     "-t", "halt"], name)
