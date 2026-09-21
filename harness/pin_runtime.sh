#!/usr/bin/env bash
# Build the pinned SWI-Prolog runtime and emit its identity record to stdout.
#
# Implements the verification docs/contracts/RUNTIME.md requires: build for
# linux/amd64, then read the interpreter's own reported version and architecture
# from INSIDE the container and fail if either does not match. Writes nothing
# except to stdout, so it cannot touch human/.
#
# Usage: bash harness/pin_runtime.sh [image-tag] > docs/contracts/RUNTIME.json
set -euo pipefail

TAG="${1:-kmla-swipl:7.2.3}"
KMLA_TZ="${KMLA_TZ:-}"
if [ -z "$KMLA_TZ" ]; then
  echo "FAIL: set KMLA_TZ before building. It is a semantic choice, not a default:" >&2
  echo "      America/New_York reproduces 376/376 shipped labels, UTC reproduces 374/376." >&2
  echo "      See harness/Dockerfile and docs/DECISION_LOG.md DL-002." >&2
  exit 2
fi
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WANT_VERSION="7.2.3"
WANT_ARCH="amd64"

docker build --platform linux/amd64 --build-arg "KMLA_TZ=$KMLA_TZ" \
  -t "$TAG" -f "$HERE/Dockerfile" "$HERE" >&2

inside() { docker run --rm --platform linux/amd64 --entrypoint sh "$TAG" -c "$1"; }

VERSION_LINE="$(inside 'swipl --version' | tr -d '\r')"
PLARCH="$(inside 'swipl --dump-runtime-variables' | sed -n 's/^PLARCH="\(.*\)";$/\1/p')"
UNAME_M="$(inside 'uname -m')"
PKG="$(inside 'dpkg -s swi-prolog-nox' | sed -n 's/^Version: //p' | tr -d '\r')"
TZ_IN="$(inside 'printf %s "$TZ"')"

case "$VERSION_LINE" in
  *"$WANT_VERSION"*) ;;
  *) echo "FAIL: interpreter reports '$VERSION_LINE', wanted $WANT_VERSION" >&2; exit 1 ;;
esac
if [ "$PLARCH" != "$WANT_ARCH" ]; then
  echo "FAIL: PLARCH is '$PLARCH', wanted $WANT_ARCH" >&2; exit 1
fi
if [ -z "$TZ_IN" ]; then
  echo "FAIL: container TZ is unset; date rendering is not reproducible" >&2; exit 1
fi
if [ "$TZ_IN" != "$KMLA_TZ" ]; then
  echo "FAIL: container TZ is '$TZ_IN' but the build was asked for '$KMLA_TZ'" >&2; exit 1
fi

IMAGE_ID="$(docker image inspect "$TAG" --format '{{.Id}}')"
BASE_DIGEST="$(sed -n 's/^FROM .*debian:stretch@\(sha256:[0-9a-f]*\)$/\1/p' "$HERE/Dockerfile")"
DOCKERFILE_SHA="$(shasum -a 256 "$HERE/Dockerfile" | awk '{print $1}')"
HOST_ARCH="$(uname -m)"

cat <<JSON
{
  "interpreter": {
    "version_string": "$VERSION_LINE",
    "version": "$WANT_VERSION",
    "plarch": "$PLARCH",
    "uname_m": "$UNAME_M",
    "debian_package_version": "$PKG",
    "verified_from_inside_container": true
  },
  "image": {
    "tag": "$TAG",
    "local_image_id": "$IMAGE_ID",
    "base_image_digest": "$BASE_DIGEST",
    "dockerfile_sha256": "$DOCKERFILE_SHA",
    "platform": "linux/amd64"
  },
  "environment": {
    "TZ": "$TZ_IN",
    "host_arch": "$HOST_ARCH",
    "emulated": $([ "$HOST_ARCH" = "x86_64" ] && echo false || echo true)
  },
  "provenance_caveats": [
    "Not upstream's 7.2.3 build: Debian's swi-prolog-nox $PKG carries Debian patches.",
    "local_image_id is this build's config digest and is NOT reproducible across builds; the reproducible identity is base_image_digest plus debian_package_version plus dockerfile_sha256.",
    "For a registry-pinned immutable digest the image must be pushed and referenced by that digest.",
    "archive.debian.org is the package source; it is an archive, not a guaranteed-permanent mirror. Vendor the .deb if long-term reproducibility is required.",
    "TZ is part of the artifact identity, not an environment detail: it changes the answers of 2 of the 376 shipped cases. See docs/DECISION_LOG.md DL-002."
  ]
}
JSON
