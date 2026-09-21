# Protected-artifact hash contract

The human owner installs and maintains `human/HASHES.txt`. All filenames in that
manifest are relative to the `human/` root. Use one SHA-256 record per file:

```text
<64 lowercase hexadecimal digits>  <relative/path>
```

Blank lines and lines beginning with `#` are comments. Sort records by relative
path. Require unique paths and reject absolute paths, traversal components,
symlinks, malformed digests, missing files, and unlisted protected files. Paths
must identify regular files. Nothing is implicitly omitted by an ignore file.

Include the source tarball, source-hash sidecar, extracted source payload, license,
decisions, parity meter, exploits, invariant statements, and other protected
files. Exclude Git's internal `.git` metadata and `HASHES.txt` itself: a manifest
cannot hash its own final contents. Pin the manifest's identity with the reviewed
human-submodule commit recorded by the parent repository's gitlink. CI must
verify that commit as well as exact file coverage and content digests.

`docs/contracts/HASHES.txt` currently contains only the verified archive hash.
It is an explicitly partial draft, not a passed integrity check. The owner must
complete the manifest after promoting and implementing the protected artifacts.

Before implementation lanes start, the runner must actually mount `human/`
read-only. Documentation alone is not filesystem enforcement. Submodule setup,
CI enforcement, and a complete owner-pinned manifest are still pending.
