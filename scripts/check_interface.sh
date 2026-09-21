#!/usr/bin/env bash
# Type-check Interface/Household.lean on the pinned toolchain and run its
# behavioural guards. Writes only to a temporary file.
#
# Usage: bash scripts/check_interface.sh [repo-root]
set -euo pipefail
ROOT="$(cd "${1:-.}" && pwd)"
IFACE="$ROOT/Interface/Household.lean"
INC="$ROOT/scripts/interface_guards.lean.inc"
[ -f "$IFACE" ] || { echo "error: no $IFACE" >&2; exit 2; }
[ -f "$ROOT/lean-toolchain" ] || { echo "error: no lean-toolchain; a bare lean call would download the elan default" >&2; exit 2; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/lean-toolchain" "$TMP/lean-toolchain"
cat "$IFACE" > "$TMP/Check.lean"
GUARDS=0
if [ -f "$INC" ]; then cat "$INC" >> "$TMP/Check.lean"; GUARDS=$(grep -c '#guard' "$INC" || true); fi

echo "toolchain: $(cat "$ROOT/lean-toolchain")"
cd "$TMP"
if lean Check.lean; then
  echo "ok    Interface/Household.lean type-checks"
  [ "$GUARDS" -gt 0 ] && echo "ok    $GUARDS behavioural guards passed"
  exit 0
else
  echo "FAIL  see the diagnostics above" >&2
  exit 1
fi
