#!/usr/bin/env bash
set -euo pipefail

die() {
  printf 'consult: %s\n' "$*" >&2
  exit 2
}

if [[ $# -ne 1 ]]; then
  printf 'Usage: scripts/consult.sh docs/consult/Q-NNN.md\n' >&2
  exit 2
fi

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd -- "$repo_root"

question="$1"
if [[ ! "$question" =~ ^docs/consult/Q-([0-9]{3})\.md$ ]]; then
  die 'question must be docs/consult/Q-NNN.md, with three decimal digits'
fi
question_number="${BASH_REMATCH[1]}"
[[ "$question_number" != 000 ]] || die 'numbering starts at Q-001'
answer="docs/consult/A-${question_number}.md"

[[ ! -L docs && ! -L docs/consult ]] || die 'consult directories must not be symlinks'
[[ -f "$question" && ! -L "$question" && -s "$question" ]] ||
  die "question is missing, empty, or a symlink: $question"
[[ ! -L "$answer" ]] || die "answer must not be a symlink: $answer"

# No model is spawned, no session is resumed, and no repository file is written.
# A repeated invocation polls the SAME question; it does not reuse its number
# for a new question. Published Q numbers and all A files must be preserved.
if [[ ! -e "$answer" ]]; then
  printf 'consult: %s is awaiting the governor; expected %s. Halt the affected lane.\n' \
    "$question" "$answer" >&2
  exit 1
fi
[[ -f "$answer" && -s "$answer" ]] ||
  die "answer is not a nonempty regular file: $answer"

# The governor seals the answer on creation. Retrieval never edits its bytes
# or permissions. Success means delivered, NOT that escalation or a gate cleared.
printf 'consult: read %s; check escalation before resuming. Never answer your own Q.\n' \
  "$answer" >&2
cat -- "$answer"
