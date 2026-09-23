"""Pinned, read-only Prolog transport diagnostics for the Phase 1.1 slice.

No reference-answer/payload producer exists here. A failed process or parse is
an exception with retained raw diagnostics, never an empty answer.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from harness import runtime
from harness.case_reader import read_case

ROOT = Path(__file__).resolve().parent.parent
IMAGE = "sha256:8e53d3a0003635786ccdeafc0048b3344b621815fe4881fd4512914a95606ec7"
CORPUS = ROOT / "human/sara/sara"


class PrologFailure(runtime.RuntimeFailure):
    pass


class PinnedSession:
    """Verify the complete recorded runtime once; use the immutable ID always.

    `directory` must be fresh. All requests, identities, command metadata and
    byte-for-byte process streams remain there, including on failure.
    """

    def __init__(self, directory):
        self.directory = runtime.output_path(directory)
        self.directory.mkdir(parents=True)
        self.log = runtime.Commands(self.directory / "commands")
        self.requests = self.directory / "requests"
        self.requests.mkdir()
        self.number = 0
        expected_path = ROOT / "docs/contracts/RUNTIME.json"
        expected = json.loads(expected_path.read_text())
        try:
            if expected["image"]["local_image_id"] != IMAGE:
                raise PrologFailure("recorded image differs from the dispatched immutable pin")
            measured = runtime.measure(self.log, IMAGE, expected["image"]["tag"])
            runtime.write_json(self.directory / "runtime-measured.json", measured)
            if measured["image"]["local_image_id"] != IMAGE:
                raise PrologFailure("Docker did not resolve the exact dispatched image ID")
            if runtime.identity(measured) != runtime.identity(expected):
                raise PrologFailure("full RUNTIME.json identity mismatch; retained measured record")
            self.runtime_identity_sha256 = runtime.identity_sha256(measured)
            runtime.write_json(self.directory / "identity.json", {
                "image": IMAGE,
                "runtime_identity_sha256": self.runtime_identity_sha256,
                "runtime_record_sha256": runtime.sha256(expected_path),
                "decisions_sha256": runtime.sha256(ROOT / "human/DECISIONS.md"),
                "manifest_sha256": runtime.sha256(ROOT / "human/HASHES.txt"),
                "household_wire_sha256": runtime.sha256(ROOT / "Interface/HOUSEHOLD_WIRE.md"),
                "harness_sha256": {name: runtime.sha256(ROOT / "harness" / name) for name in
                    ("swipl.py", "facts.py", "runtime.py", "case_reader.py", "transport_reader.pl", "grounding_probe.pl")},
                "source_files_sha256": {str(p.relative_to(CORPUS)): runtime.sha256(p)
                    for p in sorted((CORPUS / "statutes/prolog").glob("*.pl"))},
                "scope": "Household transport diagnostics; no Valid/parity/reference answers",
            })
        except Exception as error:
            runtime.write_json(self.directory / "preflight-failure.json", {"error": str(error)})
            raise

    def run(self, source, *, helper="transport_reader.pl", timeout=60, provenance=None):
        if helper not in ("transport_reader.pl", "grounding_probe.pl"):
            raise PrologFailure("unknown diagnostic helper")
        timeout = runtime.positive_seconds(timeout)
        self.number += 1
        request = self.requests / f"{self.number:03d}.pl"
        # Generated request artifacts, never edits to original/protected source.
        with request.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(source)
        runtime.write_json(self.requests / f"{self.number:03d}.json", {
            "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            "provenance": provenance, "helper": helper,
            "runtime_identity_sha256": self.runtime_identity_sha256,
        })
        result, out, err = runtime.container(
            self.log, IMAGE,
            ["swipl", "-q", "-f", "none", "-s", f"/harness/{helper}",
             "-g", "main", "-t", "halt", "--", f"/requests/{request.name}"],
            mounts=[(CORPUS, "/corpus", True), (ROOT / "harness", "/harness", True),
                    (self.requests, "/requests", True)], timeout=timeout)
        if result["timed_out"] or result["exit"] != 0 or re.search(rb"(?m)^ERROR:", err):
            raise PrologFailure(f"Prolog diagnostic failed: {result}; raw streams in {self.log.directory}")
        return out

    def inspect(self, source, *, timeout=60):
        """Read emitted clauses as terms; does NOT execute/ground them."""
        out = self.run(source, timeout=timeout)
        try:
            data = json.loads(out)
            if type(data) is not list:
                raise ValueError("expected complete clause array")
            return data
        except (UnicodeDecodeError, ValueError) as error:
            raise PrologFailure(f"Prolog transport decode failed; raw streams in {self.log.directory}: {error}") from error

    def probe_h4_tax_case_33(self, *, timeout=60):
        """Reproduce H4's precise binding pattern, without changing the rule."""
        case = read_case(CORPUS / "cases/tax_case_33.pl")
        return self.run("\n".join(case.clause_texts()) + "\n", helper="grounding_probe.pl",
                        timeout=timeout, provenance={"original": case.source.name,
                                                     "sha256": case.source.sha256,
                                                     "reader_exceptions": len(case.source.edits)})
