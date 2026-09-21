#!/usr/bin/env bash
# Checkpoint 0 acceptance harness.
#
# Re-derives every mechanical claim the Phase 0 drafts make, so the owner can
# check the assistant's work in one command instead of trusting the prose.
# Read-only: it executes self-tests and regenerates inventories into a temporary
# directory for comparison. It never writes to the repository and never touches
# human/.
#
# Usage:  bash scripts/verify_phase0.sh [--strict] [repo-root]
# Exit:   0 no mechanical check failed (outstanding items may remain),
#         1 a check failed or --strict found Checkpoint 0 outstanding items,
#         2 the harness could not run. Exit 0 is not the owner's sign-off.
#
# --strict additionally fails when a Checkpoint 0 requirement is outstanding.
# Checkpoint 2 and 3a artifacts remain reported, outside the Checkpoint 0 counts.
# Use it in CI once Checkpoint 0 has passed, so a regression cannot pass silently.

set -u

STRICT=0
ARGS=()
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    *) ARGS+=("$arg") ;;
  esac
done
set -- ${ARGS+"${ARGS[@]}"}

ROOT="${1:-.}"
if [ ! -d "$ROOT/docs/contracts" ]; then
  echo "error: $ROOT does not look like the KMLA repository root" >&2
  exit 2
fi
ROOT="$(cd "$ROOT" && pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASS=0
FAIL=0
SKIP=0
LATER_PRESENT=0
LATER_OUTSTANDING=0

report() { # status, name, detail
  case "$1" in
    ok)   PASS=$((PASS + 1)); printf 'ok    %s\n' "$2" ;;
    fail) FAIL=$((FAIL + 1)); printf 'FAIL  %s\n        %s\n' "$2" "$3" ;;
    skip) SKIP=$((SKIP + 1)); printf 'skip  %s\n        %s\n' "$2" "$3" ;;
  esac
}

report_later() { # status, name, detail; never alters Checkpoint 0 counters
  case "$1" in
    present) LATER_PRESENT=$((LATER_PRESENT + 1)); printf 'later %s\n        %s\n' "$2" "$3" ;;
    missing) LATER_OUTSTANDING=$((LATER_OUTSTANDING + 1)); printf 'later %s\n        %s\n' "$2" "$3" ;;
  esac
}

run() { # name, command...
  local name="$1"; shift
  local output
  if output="$("$@" 2>&1)"; then
    report ok "$name"
  else
    report fail "$name" "$(printf '%s' "$output" | tail -3 | tr '\n' ' ')"
  fi
}

echo "Checkpoint 0 acceptance checks against $ROOT"
echo

echo "-- scanner self-tests --"
run "statute hazard scanner self-test" \
  python3 -B "$ROOT/scripts/inventory_hazards.py" --self-test
run "case inventory scanner self-test" \
  python3 -B "$HERE/inventory_cases.py" --self-test
run "hash manifest tool self-test" \
  python3 -B "$HERE/human_manifest.py" --self-test
if [ -f "$ROOT/scripts/test_consult.py" ]; then
  run "consult wrapper offline tests" python3 -B "$ROOT/scripts/test_consult.py"
else
  report skip "consult wrapper offline tests" "scripts/test_consult.py is absent"
fi

echo
echo "-- staged inventories regenerate byte for byte --"
if python3 -B "$ROOT/scripts/inventory_hazards.py" --repo-root "$ROOT" > "$WORK/hazards.json" 2>"$WORK/err"; then
  if cmp -s "$WORK/hazards.json" "$ROOT/docs/contracts/HAZARDS.json"; then
    report ok "HAZARDS.json matches a fresh scan"
  else
    report fail "HAZARDS.json matches a fresh scan" "regenerated output differs from the staged file"
  fi
else
  report fail "HAZARDS.json matches a fresh scan" "$(tail -2 "$WORK/err" | tr '\n' ' ')"
fi

if python3 -B "$HERE/inventory_cases.py" --repo-root "$ROOT" > "$WORK/cases.json" 2>"$WORK/err"; then
  if cmp -s "$WORK/cases.json" "$ROOT/docs/contracts/CASES.json"; then
    report ok "CASES.json matches a fresh scan"
  else
    report fail "CASES.json matches a fresh scan" "regenerated output differs from the staged file"
  fi
else
  report fail "CASES.json matches a fresh scan" "$(tail -2 "$WORK/err" | tr '\n' ' ')"
fi

echo
echo "-- source integrity --"
RECORDED="$(awk '/^e4f1b845|^[0-9a-f]{64}  sara\/SARA\.tar\.gz$/ {print $1; exit}' "$ROOT/docs/contracts/HASHES.txt" 2>/dev/null)"
ACTUAL="$(shasum -a 256 "$ROOT/human/sara/SARA.tar.gz" 2>/dev/null | awk '{print $1}')"
if [ -z "$ACTUAL" ]; then
  report skip "source archive digest" "human/sara/SARA.tar.gz is absent"
elif [ "$ACTUAL" = "$RECORDED" ]; then
  report ok "source archive digest matches docs/contracts/HASHES.txt"
else
  report fail "source archive digest matches docs/contracts/HASHES.txt" "on disk $ACTUAL, staged $RECORDED"
fi

if [ -f "$ROOT/human/HASHES.txt" ] && grep -q '^[0-9a-f]\{64\}  ' "$ROOT/human/HASHES.txt"; then
  report ok "human/HASHES.txt is the installed manifest (docs/contracts/HASHES.txt is the superseded staging draft)"
else
  report skip "human/HASHES.txt is the installed manifest" \
    "still the placeholder; promote it with scripts/human_manifest.py generate"
fi

if grep -q '^[0-9a-f]\{64\}  ' "$ROOT/human/HASHES.txt" 2>/dev/null; then
  run "installed human/HASHES.txt verifies" \
    python3 -B "$HERE/human_manifest.py" verify --repo-root "$ROOT"
else
  report skip "installed human/HASHES.txt verifies" \
    "human/HASHES.txt is still the placeholder; deliverable 5 is outstanding"
fi

echo
echo "-- parity meter --"
METER="$ROOT/human/parity/check.py"
if [ -f "$METER" ]; then
  run "owner's meter satisfies the PARITY.md contract" \
    python3 -B "$HERE/parity_conformance.py" --meter "$METER"
else
  report skip "owner's meter satisfies the PARITY.md contract" \
    "human/parity/check.py does not exist; deliverable 3 is outstanding"
  if python3 -B "$HERE/parity_conformance.py" --meter "$ROOT/docs/contracts/parity/check.py" \
       > "$WORK/stub" 2>&1; then
    report fail "staged stub is still a stub" "the exit-2 placeholder passed the full contract suite"
  else
    report ok "staged stub behaves as an unimplemented placeholder (exit 2 everywhere)"
  fi
fi

echo
echo "-- Checkpoint 0 owner decisions --"
check_absent() { # path, deliverable
  if [ -e "$ROOT/$1" ]; then
    report ok "$1 exists"
  else
    report skip "$1" "absent; $2 outstanding"
  fi
}
if grep -q '^TODO\|TODO:' "$ROOT/human/DECISIONS.md" 2>/dev/null; then
  report skip "human/DECISIONS.md is complete" "still the TODO template; deliverable 1 outstanding"
else
  report ok "human/DECISIONS.md contains no TODO markers"
fi
echo
echo "-- runtime pin --"
if docker info > /dev/null 2>&1; then
  report ok "the Docker daemon is running"
else
  report skip "the Docker daemon is running" "not reachable; the runtime pin cannot be built or verified"
fi

if [ -f "$ROOT/docs/contracts/RUNTIME.json" ]; then
  RT_VER="$(python3 -c "import json;print(json.load(open('$ROOT/docs/contracts/RUNTIME.json'))['interpreter']['version'])" 2>/dev/null || echo "")"
  RT_ARCH="$(python3 -c "import json;print(json.load(open('$ROOT/docs/contracts/RUNTIME.json'))['interpreter']['plarch'])" 2>/dev/null || echo "")"
  RT_TZ="$(python3 -c "import json;print(json.load(open('$ROOT/docs/contracts/RUNTIME.json'))['environment']['TZ'])" 2>/dev/null || echo "")"
  if [ "$RT_VER" = "7.2.3" ] && [ "$RT_ARCH" = "amd64" ] && [ -n "$RT_TZ" ]; then
    report ok "runtime identity recorded (7.2.3 / amd64 / TZ=$RT_TZ)"
  else
    report fail "runtime identity recorded" "RUNTIME.json is present but does not record 7.2.3/amd64/TZ"
  fi
else
  report skip "runtime identity recorded" "docs/contracts/RUNTIME.json absent; run harness/pin_runtime.sh"
fi

if docker image inspect "${KMLA_IMAGE:-kmla-swipl:7.2.3}" > /dev/null 2>&1; then
  report ok "the pinned interpreter image is built locally"
else
  report skip "the pinned interpreter image is built locally" \
    "build it with KMLA_TZ=... bash harness/pin_runtime.sh"
fi

for tz in utc america_new_york; do
  f="$ROOT/docs/contracts/CORPUS_BASELINE_$tz.json"
  if [ -f "$f" ]; then
    n="$(python3 -c "import json;d=json.load(open('$f'));print(str(d['classification'].get('clean',0))+'/'+str(d['cases']))" 2>/dev/null || echo "? ?")"
    report ok "corpus baseline recorded for $tz ($n cases clean)"
  else
    report skip "corpus baseline recorded for $tz" "run KMLA_TZ=... bash harness/run_corpus.sh"
  fi
done

PENDING="$(grep -c '^## .* — PENDING — ' "$ROOT/docs/DECISION_LOG.md" 2>/dev/null)"
PENDING="${PENDING:-0}"
if [ "$PENDING" -gt 0 ]; then
  report skip "every decision-log entry is resolved" \
    "$PENDING entry(s) still PENDING: $(grep '^## .* — PENDING — ' "$ROOT/docs/DECISION_LOG.md" | sed 's/.*— PENDING — //; s/:.*//' | tr '\n' ' ')"
else
  report ok "no decision-log entry is still PENDING"
fi

# Later checkpoint artifacts are visible but not Checkpoint 0 requirements.
echo
echo "-- Checkpoint 2: human-authored gate exploits --"
if compgen -G "$ROOT/human/gate/exploits/*.lean" > /dev/null; then
  report_later present "human/gate/exploits contains exploit files" \
    "present; rejection validation is still required at Checkpoint 2"
else
  report_later missing "human/gate/exploits contains no exploit files" \
    "Checkpoint 2 input outstanding; not a Checkpoint 0 blocker"
fi
echo
echo "-- Checkpoint 3a: human-signed invariant statements --"
if compgen -G "$ROOT/human/invariants/statements/*.lean" > /dev/null; then
  report_later present "human/invariants/statements contains claim files" \
    "present; owner signature/review is still required at Checkpoint 3a"
else
  report_later missing "human/invariants/statements contains no claim files" \
    "Checkpoint 3a input outstanding; not a Checkpoint 0 blocker"
fi

# Checkpoint 0 summary: later artifacts cannot change these counters or exits.
echo
printf 'Checkpoint 0: %d passed, %d failed, %d outstanding\n' "$PASS" "$FAIL" "$SKIP"
printf 'Later checkpoints: %d artifact group(s) present, %d outstanding (reported above)\n' \
  "$LATER_PRESENT" "$LATER_OUTSTANDING"
echo "Checkpoint 0 also requires Dev's explicit sign-off; this script cannot grant it."
if [ "$FAIL" -gt 0 ]; then
  echo "Checkpoint 0 has NOT passed: a mechanical claim failed to re-derive."
  exit 1
fi
if [ "$SKIP" -gt 0 ]; then
  echo "No mechanical claim failed, but $SKIP Checkpoint 0 requirement(s) remain outstanding."
  echo "Checkpoint 0 requires zero failures, zero outstanding for Checkpoint 0, and Dev's sign-off."
  if [ "$STRICT" -eq 1 ]; then
    echo "--strict: treating outstanding Checkpoint 0 requirements as a failure."
    exit 1
  fi
fi
exit 0
