#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Scans ~/.claude/skills and ~/.claude/commands to build a styled startup banner.

SKILLS_DIR="$HOME/.claude/skills"
CMDS_DIR="$HOME/.claude/commands"

skills=()
commands=()

_strip() { local s="${1#\"}"; s="${s%\"}"; s="${s#\'}"; echo "${s%\'}"; }

if [[ -d "$SKILLS_DIR" ]]; then
  for skill_dir in "$SKILLS_DIR"/*/; do
    skill_file="$skill_dir/SKILL.md"
    [[ -f "$skill_file" ]] || continue
    name="" desc=""
    while IFS= read -r line; do
      [[ "$line" == "---" && -n "$name$desc" ]] && break
      if [[ "$line" =~ ^name:\ *(.*) ]]; then
        name="${BASH_REMATCH[1]}" ; name="${name#\"}"; name="${name%\"}"; name="${name#\'}"; name="${name%\'}"
      elif [[ "$line" =~ ^description:\ *(.*) ]]; then
        desc="${BASH_REMATCH[1]}" ; desc="${desc#\"}"; desc="${desc%\"}"; desc="${desc#\'}"; desc="${desc%\'}"
        desc="${desc%%.*}."
      fi
    done < "$skill_file"
    [[ -z "$name" ]] && name="${skill_dir%/}" && name="${name##*/}"
    skills+=("/$name|$desc")
  done
fi

if [[ -d "$CMDS_DIR" ]]; then
  for cmd_file in "$CMDS_DIR"/*.md; do
    [[ -f "$cmd_file" ]] || continue
    cmd_name="${cmd_file##*/}" ; cmd_name="${cmd_name%.md}"
    desc=""
    while IFS= read -r line; do
      [[ "$line" == "---" && -n "$desc" ]] && break
      if [[ "$line" =~ ^description:\ *(.*) ]]; then
        desc="${BASH_REMATCH[1]}" ; desc="${desc#\"}"; desc="${desc%\"}"; desc="${desc#\'}"; desc="${desc%\'}"
        desc="${desc%%.*}."
      fi
    done < "$cmd_file"
    commands+=("/$cmd_name|$desc")
  done
fi

if (( ${#skills[@]} == 0 && ${#commands[@]} == 0 )); then
  exit 0
fi

# --- Layout ---
max_name=0
for entry in "${skills[@]}" "${commands[@]}"; do
  n="${entry%%|*}"
  (( ${#n} > max_name )) && max_name=${#n}
done

desc_width=48
W=$(( max_name + 5 + desc_width + 4 ))
(( W < 72 )) && W=72
desc_width=$(( W - max_name - 9 ))

# --- Colors ---
R="\033[0m"
DIM="\033[2m"
BOLD="\033[1m"
CYAN="\033[36m"
BLUE="\033[34m"
MAGENTA="\033[35m"
GREEN="\033[32m"
YELLOW="\033[33m"
WHITE="\033[38;5;252m"

# skill-specific icons
declare -A ICONS
ICONS[code-review-and-quality]="🔍"
ICONS[design-an-interface]="🎨"
ICONS[grill-me]="🔥"
ICONS[marp-presentation]="📊"
ICONS[obsidian]="💎"
ICONS[read-arxiv]="📄"
ICONS[tdd]="🧪"
ICONS[test-driven-development]="🧪"
ICONS[systematic-debugging]="🔬"
ICONS[debugging-and-error-recovery]="🩺"
ICONS[defense-in-depth]="🛡️"
ICONS[incremental-implementation]="🧱"
ICONS[planning-and-task-breakdown]="📋"
ICONS[spec-driven-development]="📝"
ICONS[context-engineering]="🧠"
ICONS[source-driven-development]="📖"
ICONS[ci-cd-and-automation]="🔄"
ICONS[ingest]="📥"
ICONS[simplify]="✂️"
ICONS[improve-codebase-architecture]="🏗️"
ICONS[improve-claude-md]="📐"
ICONS[request-refactor-plan]="🔧"
ICONS[synthesizer]="🧬"
ICONS[karpathy-guidelines]="🧭"
ICONS[clean-coder]="🪥"
ICONS[learn-gh-repo]="📚"
ICONS[read-article]="📰"
ICONS[github-setup]="🔑"
ICONS[prd-to-issues]="🎫"
ICONS[prd-to-plan]="🗺️"
# fallback
DEFAULT_ICON="⚡"
CMD_ICON="⌘"

icon_for() {
  local name="${1#/}"
  echo "${ICONS[$name]:-$DEFAULT_ICON}"
}

# --- Box-drawing helpers ---
top_border() {
  printf "${DIM}╭"
  for (( i=0; i<W; i++ )); do printf "─"; done
  printf "╮${R}\n"
}
bot_border() {
  printf "${DIM}╰"
  for (( i=0; i<W; i++ )); do printf "─"; done
  printf "╯${R}\n"
}
mid_border() {
  printf "${DIM}├"
  for (( i=0; i<W; i++ )); do printf "─"; done
  printf "┤${R}\n"
}
blank_line() {
  printf "${DIM}│${R}%*s${DIM}│${R}\n" "$W" ""
}
# Print a padded line inside the box. $1 = content (may contain ANSI).
# We need visible-length padding, so $2 = visible char count of content.
box_line() {
  local content="$1" vis_len="$2"
  local pad=$(( W - vis_len ))
  (( pad < 0 )) && pad=0
  printf "${DIM}│${R}%b%*s${DIM}│${R}\n" "$content" "$pad" ""
}

# --- Render ---
echo ""
top_border

# Title
title_text="  ✨  YOUR TOOLKIT  ✨"
title_vis=${#title_text}
box_line "${BOLD}\033[38;5;159m${title_text}${R}" "$title_vis"

blank_line

# Skills section
if (( ${#skills[@]} > 0 )); then
  header="  🛠  Skills"
  box_line "${BOLD}${MAGENTA}${header}${R}" "${#header}"
  blank_line

  for entry in "${skills[@]}"; do
    n="${entry%%|*}"
    d="${entry#*|}"
    bare="${n#/}"
    ic="$(icon_for "$n")"
    if (( ${#d} > desc_width )); then
      d="${d:0:$((desc_width-3))}..."
    fi
    pad_name=$(( max_name - ${#n} ))
    # visible: "  <icon> /name      desc"  =>  4 + max_name + 3 + ${#d}
    vis=$(( 4 + max_name + 3 + ${#d} ))
    content="  ${ic} ${BOLD}${GREEN}${n}${R}$(printf '%*s' "$pad_name" '')${DIM} · ${R}${WHITE}${d}${R}"
    box_line "$content" "$vis"
  done
  blank_line
fi

# Commands section
if (( ${#commands[@]} > 0 )); then
  mid_border
  header="  ${CMD_ICON}  Commands"
  box_line "${BOLD}${BLUE}${header}${R}" "${#header}"
  blank_line

  for entry in "${commands[@]}"; do
    n="${entry%%|*}"
    d="${entry#*|}"
    if (( ${#d} > desc_width )); then
      d="${d:0:$((desc_width-3))}..."
    fi
    pad_name=$(( max_name - ${#n} ))
    vis=$(( 4 + max_name + 3 + ${#d} ))
    content="  ${CMD_ICON} ${BOLD}${YELLOW}${n}${R}$(printf '%*s' "$pad_name" '')${DIM} · ${R}${WHITE}${d}${R}"
    box_line "$content" "$vis"
  done
  blank_line
fi

# Footer
hint="  💡 Type /<name> to invoke a skill"
box_line "${DIM}${hint}${R}" "${#hint}"

bot_border
echo ""
