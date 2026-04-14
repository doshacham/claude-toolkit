#!/usr/bin/env bash
# Adds license header to newly created files after Claude's Write tool runs.
# Called by Claude Code PostToolUse hook for the Write tool.

set -euo pipefail

# Bail if jq is not available
command -v jq >/dev/null 2>&1 || exit 0

# Hook data arrives via stdin as JSON
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Skip if no file path
[[ -z "${FILE:-}" ]] && exit 0

# Skip if file doesn't exist
[[ -f "$FILE" ]] && true || exit 0

# Skip non-code files (data, config, lockfiles)
case "${FILE##*/}" in
  *.json|*.lock|*.env|*.env.*|*.gitignore|*.gitattributes|*.editorconfig|*.md|*.ico|*.png|*.jpg|*.jpeg|*.gif|*.svg|*.woff|*.woff2|*.ttf|*.eot|*.mp3|*.mp4|*.zip|*.tar|*.gz|*.pdf|*.bin|*.exe|*.dll|*.so|*.dylib|*.wasm|*.map|*.min.js|*.min.css|LICENSE|LICENSE.*|LICENCE|LICENCE.*)
    exit 0
    ;;
esac

HEADER_LINE1="Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved."
HEADER_LINE2="SPDX-License-Identifier: Proprietary"

# Already has a copyright header?
head -5 "$FILE" | grep -qi "copyright" && exit 0

# Determine comment style from extension
ext="${FILE##*.}"
case "$ext" in
  go|c|cpp|cc|cxx|h|hpp|java|js|jsx|ts|tsx|rs|swift|kt|kts|cs|dart|scala|groovy|proto|v|sv)
    C1="// $HEADER_LINE1"
    C2="// $HEADER_LINE2"
    ;;
  py|rb|sh|bash|zsh|fish|nix|yaml|yml|toml|pl|pm|r|R|ps1|psm1|psd1|tf|hcl|dockerfile|Dockerfile|makefile|Makefile|cmake|conf|cfg|ini|awk|sed)
    C1="# $HEADER_LINE1"
    C2="# $HEADER_LINE2"
    ;;
  sql|lua|hs|lhs|elm|purs)
    C1="-- $HEADER_LINE1"
    C2="-- $HEADER_LINE2"
    ;;
  css|scss|sass|less)
    C1="/* $HEADER_LINE1"
    C2="   $HEADER_LINE2 */"
    ;;
  html|xml|vue|svelte)
    C1="<!-- $HEADER_LINE1"
    C2="     $HEADER_LINE2 -->"
    ;;
  tex|bib|cls|sty|erl)
    C1="% $HEADER_LINE1"
    C2="% $HEADER_LINE2"
    ;;
  lisp|cl|clj|cljs|cljc|edn|el|scm|rkt)
    C1=";; $HEADER_LINE1"
    C2=";; $HEADER_LINE2"
    ;;
  bat|cmd)
    C1="rem $HEADER_LINE1"
    C2="rem $HEADER_LINE2"
    ;;
  ex|exs)
    C1="# $HEADER_LINE1"
    C2="# $HEADER_LINE2"
    ;;
  *)
    # Unknown extension — skip
    exit 0
    ;;
esac

# Clean up temp file on failure
trap 'rm -f "${TMPFILE:-}"' EXIT

# Handle shebang: insert header after it
FIRST_LINE=$(head -1 "$FILE")
if [[ "$FIRST_LINE" == "#!"* ]]; then
  TMPFILE=$(mktemp -p "$(dirname "$FILE")")
  { head -1 "$FILE"; printf '%s\n%s\n\n' "$C1" "$C2"; tail -n +2 "$FILE"; } > "$TMPFILE"
  mv "$TMPFILE" "$FILE"
else
  TMPFILE=$(mktemp -p "$(dirname "$FILE")")
  { printf '%s\n%s\n\n' "$C1" "$C2"; cat "$FILE"; } > "$TMPFILE"
  mv "$TMPFILE" "$FILE"
fi
