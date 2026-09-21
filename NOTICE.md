# Notices and attribution

## The SARA dataset

This project evaluates against **SARA** (Statutory Reasoning Assessment), which
it does not own, did not create, and does not modify. SARA is the work of its
authors at **Johns Hopkins University** and is redistributed here under its own
licence.

**Source:** <https://nlp.jhu.edu/law/sara/> — the canonical page, and the place
to take the dataset's citation from before publishing any result that uses it.
The archive this repository carries was downloaded from the `sara.tar.gz` link
on that page and verified byte for byte against a fresh download.

**Copyright © 2020 Nils Holzenberger**, per `human/sara/sara/LICENSE`. The
dataset accompanies the SARA paper by Nils Holzenberger, Andrew Blair-Stanek and
Benjamin Van Durme; use the citation given on the JHU page above, which is
authoritative, rather than this paragraph.

**Archive identity** (SHA-256 of `human/sara/SARA.tar.gz`):

```text
e4f1b845016fc38b95b702bbbb27a5c9af3eadfa856ba585662b8b2cd71c187c
```

### Licence terms

`human/sara/sara/LICENSE` grants permission to use, copy, modify, merge,
publish, distribute, sublicense and sell copies of the dataset, on one
condition:

> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Dataset.

**That condition binds every copy made of this repository, including the
`human/` bundle if it is split into its own repository.** `LICENSE` sits inside
`human/sara/sara/`, so it travels with the corpus automatically; it is covered by
`human/HASHES.txt` and any manifest check will fail if it is removed. Do not
relocate or omit it.

The dataset is provided "as is", without warranty of any kind. See the LICENSE
file for the full disclaimer.

### What this project changed in SARA

**Nothing.** The corpus is mounted read-only and every file is hash-pinned.
`human/HASHES.txt` covers all 408 protected files and
`python3 -B scripts/human_manifest.py verify` checks them.

This project *does* record defects it found in the SARA reference implementation
— see `docs/contracts/SOURCE_FINDINGS.md` and the source hazard inventory in
`human/DECISIONS.md`. Those are **observations about the published artifact,
recorded so results are reproducible**, not corrections applied to it and not a
criticism of the authors. Two examples: the recorded New York run has 376 clean
directive outcomes (two execute no test and pass vacuously), whereas the UTC run
has two failed directives; and `section63.pl:358` holds a
counter value that differs from its parallel clause. The oracle translates the
code as written, divergences included, because the parity meter compares against
the unmodified program (`human/DECISIONS.md` G9).

Any claim this project publishes is of the form "consistent with a verified
reference", never "faithful to the statute".

## Other components

**SWI-Prolog 7.2.3** — the reference interpreter, specified by the SARA
instructions. `harness/Dockerfile` installs Debian's `swi-prolog-nox 7.2.3+dfsg-6`
from `archive.debian.org`. SWI-Prolog is © Jan Wielemaker and contributors,
under the Simplified BSD licence; the Debian packaging is the Debian
maintainers' work. See `docs/DECISION_LOG.md` P-RUNTIME.

### Debian redistribution

The runtime includes the complete installed Debian package closure, not just
SWI-Prolog. Its components retain their own copyrights and licences; this
repository's licence cannot replace them. Preserve the package notices under
`/usr/share/doc/<package>/copyright` and the referenced texts under
`/usr/share/common-licenses` with redistributed images and rebuild bundles.
Debian specifies these notice locations in its
[Policy Manual, §12.5](https://www.debian.org/doc/debian-policy/ch-docs.html#copyright-information).

Before distributing the binary closure, image or image archive, provide the
complete corresponding sources for GPL-covered packages and meet every
included package's licence obligations. Merely pointing to a third-party mirror
that may remove those sources is not a durable substitute. Keep exact source
versions, Debian packaging/patches and checksums alongside the rebuild materials;
see [Debian's binary-distribution guidance](https://www.debian.org/CD/vendors/legal).
This notice records the obligation, not a claim that the source bundle or
archival deposit has already been assembled. P-RUNTIME requires that evidence
before the archival work is marked complete.

**United States Internal Revenue Code** — the statute text under
`human/sara/sara/statutes/source/` is United States federal law and is not
subject to copyright.
