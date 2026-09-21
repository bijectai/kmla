#!/usr/bin/env bash
set -euo pipefail

die() {
  printf 'consult: %s\n' "$*" >&2
  exit 1
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
prompt_file='docs/consult/FABLE_PROMPT.md'
session_file='docs/consult/.fable_session'
lock_dir='docs/consult/.fable_session.lock'

[[ ! -L docs && ! -L docs/consult ]] || die 'consult directories must not be symlinks'
[[ -f "$prompt_file" && ! -L "$prompt_file" && -s "$prompt_file" ]] ||
  die 'FABLE_PROMPT.md not installed (or not a nonempty regular file)'
[[ -f "$question" && ! -L "$question" && -s "$question" ]] ||
  die "question is missing, empty, or a symlink: $question"
[[ ! -e "$answer" && ! -L "$answer" ]] ||
  die "answer already exists; never reuse or overwrite it: $answer"
[[ ! -L "$session_file" ]] || die 'session file must not be a symlink'
for dependency in claude jq; do
  command -v "$dependency" >/dev/null 2>&1 || die "required command not found: $dependency"
done

# One continuous session must not be resumed concurrently by two questions.
umask 077
mkdir -- "$lock_dir" 2>/dev/null || die "another consult is active (lock: $lock_dir)"
session_tmp=''
cleanup() {
  if [[ -n "$session_tmp" && -f "$session_tmp" ]]; then
    rm -f -- "$session_tmp"
  fi
  rmdir -- "$lock_dir" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# Recheck after taking the lock: another process may have just completed.
[[ ! -e "$answer" && ! -L "$answer" ]] || die "answer already exists: $answer"

uuid_pattern='^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
resume_id=''
allowed_tools='Read,Glob,Grep,Write,Edit'
args=(
  -p "Answer the question in $question. Write your answer to $answer in the format FABLE_PROMPT.md specifies. Print only the path of the A file when done."
  --append-system-prompt "$(cat -- "$prompt_file")"
  --allowedTools "$allowed_tools"
  --tools "$allowed_tools"
  --disallowedTools 'Bash,mcp__*'
  --strict-mcp-config
  --mcp-config '{"mcpServers":{}}'
  --disable-slash-commands
  --permission-mode acceptEdits
  --output-format json
)
if [[ -e "$session_file" ]]; then
  [[ -f "$session_file" ]] || die 'session path is not a regular file'
  resume_id="$(cat -- "$session_file")"
  [[ "$resume_id" =~ $uuid_pattern ]] || die 'saved session id is empty or malformed'
  args+=(--resume "$resume_id")
fi

# Keep the unmodified CLI response for schema inspection and failure diagnosis.
# mktemp makes this a private file outside the repository; only the A body goes
# to stdout. There are no automatic retries and no fallback to a new session.
response_json="$(mktemp "${TMPDIR:-/tmp}/kmla-fable-response.XXXXXX")"
printf 'consult: CLI JSON retained at %s\n' "$response_json" >&2
claude_status=0
claude "${args[@]}" </dev/null >"$response_json" || claude_status=$?

# Once Fable has written an answer, preserve it even if the CLI reports failure.
if [[ -f "$answer" && ! -L "$answer" ]]; then
  chmod a-w "$answer"
fi
if [[ "$claude_status" -ne 0 ]]; then
  printf 'consult: claude exited %s; response: %s\n' "$claude_status" "$response_json" >&2
  if [[ ! -f "$answer" || -L "$answer" ]]; then
    printf 'consult: answer was not created: %s\n' "$answer" >&2
  fi
  exit "$claude_status"
fi
jq -e 'type == "object"' "$response_json" >/dev/null || die "invalid CLI JSON: $response_json"
jq -e '.type == "result" and .subtype == "success" and .is_error == false' \
  "$response_json" >/dev/null || die "CLI reported a failed or unexpected result: $response_json"
[[ -f "$answer" && ! -L "$answer" && -s "$answer" ]] ||
  die "answer was not created as a nonempty regular file: $answer"

# Confirmed from a live Claude Code 2.1.247 JSON response before implementation.
# Do not substitute .uuid, which identifies the result event, not the session.
new_id="$(jq -r '.session_id | select(type == "string")' "$response_json")"
if [[ -z "$new_id" || ! "$new_id" =~ $uuid_pattern ]]; then
  printf 'consult: warning: session_id missing or invalid; no session id saved\n' >&2
else
  if [[ -n "$resume_id" && "$new_id" != "$resume_id" ]]; then
    die 'resumed call returned a different session id; persistence is not verified'
  fi
  session_tmp="$(mktemp 'docs/consult/.fable_session.tmp.XXXXXX')"
  printf '%s\n' "$new_id" >"$session_tmp"
  mv -f -- "$session_tmp" "$session_file"
  session_tmp=''
fi

cat -- "$answer"
