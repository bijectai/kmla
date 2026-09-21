#!/usr/bin/env bash
# Convert the tracked human/ directory into the pinned submodule docs/PLAN.md
# section 2 requires, preserving every file and every digest.
#
# Dry run by default. Nothing is written until you pass --apply.
#
#   bash scripts/make_human_submodule.sh --url git@github.com:you/kmla-human.git
#   bash scripts/make_human_submodule.sh --url ... --apply
#
# Refuses to start unless: the working tree is clean apart from human/HASHES.txt,
# human/ verifies against its own manifest, and no git worktree lives inside
# human/. Those three checks are what stop a migration from losing work.
set -euo pipefail

URL=""; APPLY=0; ROOT="."; BRANCH="main"
while [ $# -gt 0 ]; do
  case "$1" in
    --url) URL="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --root) ROOT="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
ROOT="$(cd "$ROOT" && pwd)"
[ -n "$URL" ] || { echo "error: --url is required (the human-owned repository)" >&2; exit 2; }
[ -d "$ROOT/human" ] || { echo "error: no $ROOT/human" >&2; exit 2; }

say() { if [ "$APPLY" -eq 1 ]; then echo "  $*"; else echo "  would: $*"; fi; }
run() { if [ "$APPLY" -eq 1 ]; then ( cd "$ROOT" && eval "$@" ); else echo "  would run: $*"; fi; }

echo "== preconditions =="

if [ -e "$ROOT/.gitmodules" ] || git -C "$ROOT" ls-tree -d HEAD human 2>/dev/null | grep -q '^160000'; then
  echo "error: human/ already looks like a submodule; nothing to do" >&2; exit 2
fi

nested="$(git -C "$ROOT" worktree list --porcelain | awk '/^worktree /{print $2}' | grep "^$ROOT/human/" || true)"
if [ -n "$nested" ]; then
  echo "error: a git worktree lives inside human/ and would be swallowed by the migration:" >&2
  printf '  %s\n' $nested >&2
  echo "       move it first:  git worktree move <path> .claude/worktrees/<name>" >&2
  exit 2
fi
echo "  ok   no git worktree inside human/"

dirty="$(git -C "$ROOT" status --porcelain | grep -v ' human/HASHES.txt$' || true)"
if [ -n "$dirty" ]; then
  echo "error: working tree is not clean; commit or stash first:" >&2
  printf '%s\n' "$dirty" | head -20 >&2
  exit 2
fi
echo "  ok   working tree clean"

if python3 -B "$ROOT/scripts/human_manifest.py" verify --repo-root "$ROOT" >/dev/null 2>&1; then
  echo "  ok   human/ verifies against human/HASHES.txt ($(grep -c '^[0-9a-f]' "$ROOT/human/HASHES.txt") records)"
else
  echo "error: human/ does not verify against its manifest. Regenerate it first:" >&2
  echo "       python3 -B scripts/human_manifest.py generate > human/HASHES.txt" >&2
  exit 2
fi

for missing in parity/check.py; do
  [ -e "$ROOT/human/$missing" ] || echo "  WARN human/$missing is absent; the pin will not cover the owner's meter"
done

FILES="$(find "$ROOT/human" -type f | wc -l | tr -d ' ')"
echo "  ok   $FILES files under human/ will be preserved"

echo
echo "== migration =="
say "initialise a git repository inside human/ on branch $BRANCH"
run "git -C human init -q -b '$BRANCH'"
say "commit all $FILES files there"
run "git -C human add -A"
run "git -C human -c user.name=\"\$(git config user.name)\" -c user.email=\"\$(git config user.email)\" commit -q -m 'human: protected artifact bundle'"
say "point it at $URL and push"
run "git -C human remote add origin '$URL'"
run "git -C human push -u origin '$BRANCH'"
say "drop human/ from the parent index, keeping the files"
run "git rm -r -q --cached human"
say "register it as a submodule and pin the commit just made"
run "git submodule add --force '$URL' human"
run "git add .gitmodules human"
run "git -c user.name=\"\$(git config user.name)\" -c user.email=\"\$(git config user.email)\" commit -q -m 'human: pin the protected bundle as a submodule'"

echo
if [ "$APPLY" -eq 1 ]; then
  echo "== verify the result =="
  # A recursive clone is the only check that proves the pin is usable from
  # another machine. It catches the common failure where the remote's HEAD
  # points at a branch that was never pushed.
  VTMP="$(mktemp -d)"
  # Git refuses the `file` transport for submodules by default (CVE-2022-39253).
  # A local path remote is normal when rehearsing this migration, so allow it
  # for the check only; a real ssh/https remote is unaffected by the flag.
  FILEOK=""
  case "$URL" in
    *://*) ;;                      # a real transport
    *) FILEOK="-c protocol.file.allow=always" ;;
  esac
  if git $FILEOK clone -q --recurse-submodules "$ROOT" "$VTMP/clone" 2>"$VTMP/err"; then
    N="$(find "$VTMP/clone/human" -type f -not -path '*/.git/*' -not -name '.git' | wc -l | tr -d ' ')"
    if python3 -B "$VTMP/clone/scripts/human_manifest.py" verify --repo-root "$VTMP/clone" >/dev/null 2>&1; then
      echo "  ok   a recursive clone reproduces $N files and the manifest verifies"
    else
      echo "  FAIL the clone's human/ does not verify against its manifest" >&2
    fi
  else
    echo "  FAIL a recursive clone could not fetch the submodule:" >&2
    sed 's/^/       /' "$VTMP/err" >&2
    echo "       Two common causes: the remote's HEAD points at a branch that was" >&2
    echo "       never pushed (fix: git -C <remote.git> symbolic-ref HEAD refs/heads/$BRANCH)," >&2
    echo "       or the clone is being done by someone whose git refuses the file" >&2
    echo "       transport for submodules (CVE-2022-39253)." >&2
  fi
  rm -rf "$VTMP"
  echo
  echo "== result =="
  echo "  parent commit:    $(git -C "$ROOT" rev-parse HEAD)"
  echo "  submodule commit: $(git -C "$ROOT/human" rev-parse HEAD)"
  echo "  gitlink:          $(git -C "$ROOT" ls-tree HEAD human)"
  echo
  echo "  Record both in docs/HANDOFF.md, then re-run:"
  echo "    python3 -B scripts/human_manifest.py verify"
else
  echo "Dry run only; nothing was written. Re-run with --apply to perform it."
fi
