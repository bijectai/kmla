#!/usr/bin/env bash
# Compile the partial §7703 implementation and its full assertion file.
# A proof failure is a nonzero result, never a skip/xfail. This is not parity,
# a complete reference implementation, an axiom hygiene gate or CP1 acceptance.
# Usage: bash scripts/check_oracle7703.sh [repo-root]
set -euo pipefail
REPO_ROOT="$(cd "${1:-.}" && pwd)"
test -s "$REPO_ROOT/lean-toolchain" || { echo "missing lean-toolchain" >&2; exit 2; }
IFS= read -r KMLA_TOOLCHAIN < "$REPO_ROOT/lean-toolchain"
KMLA_CHECK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/kmla-s7703.XXXXXX")"
# Keep the build artifacts for inspection, especially when a proof fails.
echo "toolchain: $KMLA_TOOLCHAIN"
echo "build artifacts: $KMLA_CHECK_DIR"
mkdir -p "$KMLA_CHECK_DIR/Interface" "$KMLA_CHECK_DIR/Oracle/Tests"
cd "$REPO_ROOT"
export LEAN_PATH="$KMLA_CHECK_DIR"
for KMLA_MODULE in Interface/Household Interface/QuerySchema Interface/QueryTime Oracle/S7703; do
  lean "+$KMLA_TOOLCHAIN" -o "$KMLA_CHECK_DIR/$KMLA_MODULE.olean" "$KMLA_MODULE.lean"
done
if lean "+$KMLA_TOOLCHAIN" -o "$KMLA_CHECK_DIR/Oracle/Tests/S7703.olean" Oracle/Tests/S7703.lean; then
  echo "ok    partial §7703 assertion file compiled; open reference obligations remain"
else
  KMLA_TEST_EXIT=$?
  echo "FAIL  §7703 assertions are unproved; see diagnostics above (exit $KMLA_TEST_EXIT)" >&2
  exit "$KMLA_TEST_EXIT"
fi
