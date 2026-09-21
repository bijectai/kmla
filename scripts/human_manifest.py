#!/usr/bin/env python3
"""Generate or verify the protected-artifact hash manifest for `human/`.

Implements the contract in `docs/contracts/HASHES.md`. The generator writes only
to stdout and exposes no output-file option, so it can never write under
`human/`; the owner redirects its output into `human/HASHES.txt` themselves.

This tool reads file bytes to digest them and never prints, stores, or returns
file contents. It can therefore hash the owner's independent parity meter
without inspecting its source. Run with `python3 -B` to avoid bytecode.

Exit codes: 0 success, 1 manifest drift or mismatch, 2 usage or infrastructure
failure. A nonzero exit is never a passed integrity check.
"""

import argparse
from hashlib import sha256
import os
import stat as stat_module
from pathlib import Path, PurePosixPath
import sys
import tempfile


PROTECTED_ROOT = PurePosixPath("human")
MANIFEST_NAME = "HASHES.txt"
DIGEST_SEPARATOR = "  "
DIGEST_LENGTH = 64
HEX = frozenset("0123456789abcdef")
EXCLUDED_COMPONENTS = frozenset({".git", MANIFEST_NAME})
CHUNK = 1 << 20


class ManifestError(ValueError):
    """A condition the contract requires to fail rather than be tolerated."""


def digest_file(path):
    """Return the SHA-256 of a regular file without retaining its contents."""
    accumulator = sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            accumulator.update(block)
    return accumulator.hexdigest()


def check_relative_path(text):
    """Reject every path shape the contract forbids before touching the disk."""
    if not text:
        raise ManifestError("empty path")
    if text != text.strip():
        raise ManifestError(f"path has leading or trailing whitespace: {text!r}")
    if "\\" in text:
        raise ManifestError(f"backslash in path: {text!r}")
    if "\x00" in text:
        raise ManifestError(f"NUL in path: {text!r}")
    if text.startswith("/"):
        raise ManifestError(f"absolute path: {text!r}")
    parts = PurePosixPath(text).parts
    if not parts:
        raise ManifestError(f"path resolves to nothing: {text!r}")
    for part in parts:
        if part in {"", ".", ".."}:
            raise ManifestError(f"traversal or empty component in path: {text!r}")
        if part in EXCLUDED_COMPONENTS:
            raise ManifestError(f"excluded component {part!r} in path: {text!r}")
    return PurePosixPath(text)


def resolve_within(root, relative):
    """Walk each component with lstat so no symlink can leave the protected root."""
    current = root
    for part in relative.parts:
        current = current / part
        info = os.lstat(current)
        if stat_module.S_ISLNK(info.st_mode):
            raise ManifestError(f"symlinked component: {relative}")
    return current


def walk_protected(root):
    """List every protected regular file, sorted, with nothing implicitly omitted."""
    if not root.is_dir():
        raise ManifestError(f"protected root is not a directory: {root}")
    found = []
    for directory, subdirectories, names in os.walk(root, followlinks=False):
        subdirectories[:] = sorted(
            name for name in subdirectories if name not in EXCLUDED_COMPONENTS
        )
        for name in sorted(names):
            if name in EXCLUDED_COMPONENTS:
                continue
            path = Path(directory) / name
            info = os.lstat(path)
            if stat_module.S_ISLNK(info.st_mode):
                raise ManifestError(f"symlink under the protected root: {path}")
            if not stat_module.S_ISREG(info.st_mode):
                raise ManifestError(f"not a regular file: {path}")
            found.append(PurePosixPath(path.relative_to(root).as_posix()))
    return sorted(found, key=str)


def parse_manifest(text):
    """Parse manifest text into ordered (digest, path) records."""
    if "\r" in text:
        raise ManifestError("carriage return in manifest; use LF line endings")
    records = []
    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if DIGEST_SEPARATOR not in line:
            raise ManifestError(f"line {number}: missing the two-space separator")
        digest, _, remainder = line.partition(DIGEST_SEPARATOR)
        if len(digest) != DIGEST_LENGTH or not set(digest) <= HEX:
            raise ManifestError(f"line {number}: malformed digest {digest!r}")
        try:
            relative = check_relative_path(remainder)
        except ManifestError as error:
            raise ManifestError(f"line {number}: {error}") from error
        records.append((digest, relative))
    return records


def render(records):
    header = [
        f"# Protected-artifact manifest for {PROTECTED_ROOT}/, per docs/contracts/HASHES.md.",
        "# Paths are relative to human/. Sorted by path. Excludes .git and this file.",
    ]
    lines = header + [f"{digest}{DIGEST_SEPARATOR}{path}" for digest, path in records]
    return "\n".join(lines) + "\n"


def generate(root):
    return [(digest_file(resolve_within(root, path)), path) for path in walk_protected(root)]


def verify(root, manifest_path):
    """Return a list of contract violations; an empty list means the manifest holds."""
    problems = []
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ManifestError(f"manifest not found: {manifest_path}") from None
    except UnicodeDecodeError as error:
        raise ManifestError(f"manifest is not UTF-8: {error}") from error

    records = parse_manifest(text)
    listed = {}
    for digest, path in records:
        if path in listed:
            problems.append(f"duplicate path listed: {path}")
            continue
        listed[path] = digest

    if [str(path) for _, path in records] != sorted(str(path) for _, path in records):
        problems.append("records are not sorted by relative path")

    for path in sorted(listed, key=str):
        try:
            target = resolve_within(root, path)
        except (ManifestError, FileNotFoundError, NotADirectoryError) as error:
            problems.append(f"missing or unusable listed path: {path} ({error})")
            continue
        info = os.lstat(target)
        if not stat_module.S_ISREG(info.st_mode):
            problems.append(f"listed path is not a regular file: {path}")
            continue
        actual = digest_file(target)
        if actual != listed[path]:
            problems.append(f"digest mismatch: {path}")

    present = set(walk_protected(root))
    for path in sorted(present - set(listed), key=str):
        problems.append(f"unlisted protected file: {path}")
    for path in sorted(set(listed) - present, key=str):
        problems.append(f"listed file absent from the protected root: {path}")
    return problems


def self_test():
    """Exercise generation, verification, and every rejection the contract names."""
    checks = []

    def expect(name, condition):
        checks.append((name, bool(condition)))

    def expect_error(name, action, fragment):
        try:
            action()
        except ManifestError as error:
            expect(name, fragment in str(error))
        else:
            expect(name, False)

    with tempfile.TemporaryDirectory() as workspace:
        root = Path(workspace) / "human"
        (root / "nested").mkdir(parents=True)
        (root / "a.txt").write_bytes(b"alpha\n")
        (root / "nested" / "b.bin").write_bytes(b"\x00\xff")
        (root / MANIFEST_NAME).write_text("# excluded from itself\n", encoding="utf-8")
        (root / ".git").mkdir()
        (root / ".git" / "config").write_text("ignored\n", encoding="utf-8")

        records = generate(root)
        listed = [str(path) for _, path in records]
        expect("walk covers both payload files", listed == ["a.txt", "nested/b.bin"])
        expect("manifest excludes itself and .git", MANIFEST_NAME not in listed)
        by_path = {path: digest for digest, path in records}
        expect(
            "digest matches a known vector",
            by_path[PurePosixPath("a.txt")] == sha256(b"alpha\n").hexdigest(),
        )

        manifest = root / MANIFEST_NAME
        manifest.write_text(render(records), encoding="utf-8")
        expect("a freshly generated manifest verifies", verify(root, manifest) == [])

        (root / "nested" / "b.bin").write_bytes(b"\x00\xfe")
        expect("content drift is reported", any("digest mismatch" in p for p in verify(root, manifest)))
        (root / "nested" / "b.bin").write_bytes(b"\x00\xff")

        (root / "sneaked.txt").write_text("added later\n", encoding="utf-8")
        expect("unlisted files are reported", any("unlisted" in p for p in verify(root, manifest)))
        (root / "sneaked.txt").unlink()

        expect("restored tree verifies again", verify(root, manifest) == [])

        good = render(records)
        expect_error("absolute paths rejected", lambda: parse_manifest(good.replace("  a.txt", "  /a.txt")), "absolute")
        expect_error("traversal rejected", lambda: parse_manifest(good.replace("  a.txt", "  ../a.txt")), "traversal")
        expect_error("short digests rejected", lambda: parse_manifest("abc  a.txt"), "malformed digest")
        expect_error("uppercase digests rejected", lambda: parse_manifest("A" * 64 + "  a.txt"), "malformed digest")
        expect_error("missing separator rejected", lambda: parse_manifest("f" * 64 + " a.txt"), "separator")
        expect_error("CRLF rejected", lambda: parse_manifest("f" * 64 + "  a.txt\r\n"), "carriage return")
        expect_error("self-reference rejected", lambda: parse_manifest("f" * 64 + f"  {MANIFEST_NAME}"), "excluded")
        expect_error("git metadata rejected", lambda: parse_manifest("f" * 64 + "  .git/config"), "excluded")

        unsorted_path = Path(workspace) / "unsorted.txt"
        unsorted_path.write_text(render(list(reversed(records))), encoding="utf-8")
        expect("unsorted manifests are reported",
               any("not sorted" in problem for problem in verify(root, unsorted_path)))

        comments = "# leading comment\n\n" + render(records)
        (Path(workspace) / "c.txt").write_text(comments, encoding="utf-8")
        expect("comments and blank lines are accepted", verify(root, Path(workspace) / "c.txt") == [])

        link_root = Path(workspace) / "linked"
        (link_root / "nested").mkdir(parents=True)
        (link_root / "nested" / "b.bin").write_bytes(b"\x00\xff")
        os.symlink(root / "a.txt", link_root / "a.txt")
        expect_error("symlinks under the root rejected", lambda: walk_protected(link_root), "symlink")

    failures = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'ok  ' if passed else 'FAIL'}  {name}")
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    return 0 if not failures else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", nargs="?", choices=("generate", "verify"),
                        help="generate prints a manifest to stdout; verify checks the installed one")
    parser.add_argument("--repo-root", default=".", help="repository root (default: the current directory)")
    parser.add_argument("--self-test", action="store_true", help="run the built-in checks and exit")
    arguments = parser.parse_args(argv)

    if arguments.self_test:
        return self_test()
    if arguments.command is None:
        parser.error("a command is required unless --self-test is given")

    root = Path(arguments.repo_root) / str(PROTECTED_ROOT)
    try:
        if arguments.command == "generate":
            sys.stdout.write(render(generate(root)))
            return 0
        problems = verify(root, root / MANIFEST_NAME)
    except ManifestError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"\n{len(problems)} manifest problem(s); human/ is NOT verified.", file=sys.stderr)
        return 1
    print(f"verified: every file under {PROTECTED_ROOT}/ is listed and matches its digest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
