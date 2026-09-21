#!/usr/bin/env bash
# Unmodified reference directive outcomes, including the two known vacuous cases.
# bash harness/run_corpus.sh --runtime RUN/RUNTIME.json --out RUN/BASELINE.json [root]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "$HERE/run_corpus.py" "$@"
