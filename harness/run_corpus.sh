#!/usr/bin/env bash
# Run every SARA case once on the pinned interpreter; emit a JSON baseline.
#
# Records, per case, the exit status and a classification of stderr. Exit status
# alone is useless here: every case exits 0 whatever happens, including when the
# statutes never load (docs/contracts/RUNTIME_OBSERVATIONS.md O-2). stderr is the
# only signal, so this script reports it rather than pretending exit status means
# something.
#
# This is a BASELINE of the reference implementation against its own labels. It is
# not a grader: the pass/fail protocol is an owner decision (blocker B006), and
# "clean stderr" is this script's provisional stand-in, not an approved contract.
#
# The corpus is mounted read-only. Writes only to --out and stdout.
#
# Usage: KMLA_TZ=America/New_York bash harness/run_corpus.sh [--out FILE] [repo-root]
set -euo pipefail

OUT=""
ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done
set -- ${ARGS+"${ARGS[@]}"}
ROOT="$(cd "${1:-.}" && pwd)"
TAG="${KMLA_IMAGE:-kmla-swipl:7.2.3}"

if [ -z "${KMLA_TZ:-}" ]; then
  echo "error: KMLA_TZ is required. It changes the answers of 2 of the 376 cases:" >&2
  echo "       America/New_York -> 376/376 agree with their labels; UTC -> 374/376." >&2
  echo "       See docs/DECISION_LOG.md DL-002. This script will not pick for you." >&2
  exit 2
fi
CORPUS="$ROOT/human/sara/sara"
[ -d "$CORPUS/cases" ] || { echo "error: no corpus at $CORPUS" >&2; exit 2; }
if ! docker image inspect "$TAG" >/dev/null 2>&1; then
  echo "error: image $TAG is absent. Build it with harness/pin_runtime.sh." >&2
  exit 2
fi

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
cat > "$WORK/sweep.sh" <<'INNER'
#!/bin/sh
cd /corpus || exit 2
: > /out/rows.jsonl
for f in cases/*.pl; do
  id=$(basename "$f" .pl)
  err=$(swipl -q -f "$f" 2>&1 >/dev/null); code=$?
  if   [ -z "$err" ]; then cls=clean
  elif echo "$err" | grep -q 'does not exist'; then cls=load_failure
  elif echo "$err" | grep -q '^ERROR'; then cls=error
  elif echo "$err" | grep -q 'Goal (directive) failed'; then cls=directive_failed
  else cls=other; fi
  printf '%s\t%s\t%s\t%s\n' "$id" "$code" "$cls" "$(printf '%s' "$err" | tr '\n' '\037')" >> /out/rows.jsonl
done
INNER
chmod +x "$WORK/sweep.sh"

docker run --rm --platform linux/amd64 -e "TZ=$KMLA_TZ" \
  -v "$CORPUS:/corpus:ro" -v "$WORK:/out" --entrypoint sh "$TAG" /out/sweep.sh >&2

python3 - "$WORK/rows.jsonl" "$KMLA_TZ" "$TAG" <<'PY' > "${OUT:-/dev/stdout}"
import json, sys
rows = []
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 4: continue
    rows.append({"id": parts[0], "exit": int(parts[1]), "class": parts[2],
                 "stderr": parts[3].replace("\x1f", "\n")})
by = {}
for r in rows: by[r["class"]] = by.get(r["class"], 0) + 1
json.dump({
    "tz": sys.argv[2], "image": sys.argv[3], "cases": len(rows),
    "exit_codes": {str(c): sum(1 for r in rows if r["exit"] == c) for c in sorted({r["exit"] for r in rows})},
    "classification": dict(sorted(by.items())),
    "note": "Exit status is 0 for every case regardless of outcome; stderr is the only signal.",
    "not_clean": [r for r in rows if r["class"] != "clean"],
}, sys.stdout, indent=2)
sys.stdout.write("\n")
PY
