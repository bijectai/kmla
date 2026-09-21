# Source provenance

The primary source is the archive linked from the
[JHU SARA page](https://nlp.jhu.edu/law/sara/), not a downstream copy.
The page's download link is lowercase
[`sara.tar.gz`](https://nlp.jhu.edu/law/sara/sara.tar.gz). The uppercase URL
provided in the instructions returned HTTP 403 during verification.

On 2026-09-20, a fresh download to temporary storage matched the already installed
`human/sara/SARA.tar.gz` byte for byte. Its SHA-256 is:

```text
e4f1b845016fc38b95b702bbbb27a5c9af3eadfa856ba585662b8b2cd71c187c
```

The existing `human/sara/SOURCE_SHA256.txt` records the same digest. Nothing under
`human/` was installed, moved, or rewritten during this verification.

## Installed layout

The archive has a `sara/` top-level directory, so the actual corpus root is
`human/sara/sara/`:

- `statutes/source/`: nine source statute texts.
- `statutes/prolog/`: nine section programs plus `init.pl`, `events.pl`, and
  `utils.pl`. Inventory and translation decisions must include the helpers.
- `cases/`: 376 Prolog case files: 276 section entailment cases and 100
  `tax_case_*.pl` numerical cases.
- `splits/train` and `splits/test`: 256 and 120 distinct case IDs, with no overlap,
  missing case, or unknown ID.
- `LICENSE`: MIT terms, copyright 2020 Nils Holzenberger.

All 400 extracted payload files match the archive bytes. No payload file is
missing or extra. The archive also contains 405 `._*` AppleDouble metadata files,
each identified by the `00051607` header. These include 376 metadata companions
under `cases/`: counting every archive entry ending in `.pl` would count 752,
not 376. This is archive metadata, not additional Prolog input. The original
tarball preserves all entries. No case has been filtered to satisfy a count.

The user designates this artifact as SARA v2. The linked JHU page itself does not
state a v2 label; use the verified archive hash as the precise artifact identity.
See `SOURCE_AUDIT.json` for the recorded verification results.

## Runtime and pinning

JHU specifies SWI-Prolog 7.2.3 for amd64 and loads the statute program through
`statutes/prolog/init.pl`. The harness must run that interpreter in a Docker image
for `linux/amd64`. A modern host interpreter is not an accepted substitute.
No Prolog execution or Docker image verification has occurred in Phase 0.

`HASHES.txt` alongside this document stages the archive hash for owner promotion.
It is explicitly partial: the owner must pin the remaining protected files and
the human submodule commit before Checkpoint 0 passes.
