#!/usr/bin/env bash
# Build, measure and retain a NEW runtime record. Existing records are immutable.
# KMLA_TZ=America/New_York bash harness/pin_runtime.sh --out RUN/RUNTIME.json [tag]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "$HERE/runtime.py" "$@"
