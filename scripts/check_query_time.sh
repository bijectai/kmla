#!/usr/bin/env bash
# Compile both shared modules and their boundary checks on the pinned toolchain.
set -euo pipefail
ROOT="$(cd "${1:-.}" && pwd)"
test -f "$ROOT/lean-toolchain" || { echo "missing lean-toolchain" >&2; exit 2; }
CHECK_DIR="$(mktemp -d)"
trap 'rm -rf "$CHECK_DIR"' EXIT
mkdir -p "$CHECK_DIR/Interface"
cd "$ROOT"
export LEAN_PATH="$CHECK_DIR"
lean -o "$CHECK_DIR/Interface/Household.olean" Interface/Household.lean
python3 -B scripts/check_time_schema.py
lean -o "$CHECK_DIR/Interface/QuerySchema.olean" Interface/QuerySchema.lean
lean -o "$CHECK_DIR/Interface/QueryTime.olean" Interface/QueryTime.lean
lean scripts/query_time_guards.lean
echo "ok    query-time guards and kernel-checked boundary proofs passed"
