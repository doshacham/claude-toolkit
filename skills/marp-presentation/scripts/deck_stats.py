# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Produce a single-line (or verbose) health summary of a Marp deck.

Counts slides, words, bullets, headings, code blocks, mermaid diagrams, and
images. Computes estimated speaking duration using the same heuristics as
estimate_duration.py. Outputs a terse status line:

    14 slides · 842 words · 6 diagrams · 2 images · ~9 min

With --verbose, prints a breakdown table.

Usage:
    python deck_stats.py --input deck.md
    python deck_stats.py --input deck.md --verbose
    python deck_stats.py --input deck.md --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path


HEADING = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
BULLET = re.compile(r"^\s*[-*+] ", re.MULTILINE)
CODE_FENCE = re.compile(r"^```(\w*)\s*$", re.MULTILINE)
MERMAID_BLOCK = re.compile(r"```mermaid\b.*?```", re.DOTALL)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
WORD_RE = re.compile(r"[A-Za-z0-9']+")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[:end + 4], text[end + 4:]


def split_slides(body: str) -> list[str]:
    body = body.lstrip("\n")
    slides: list[str] = []
    current: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            current.append(line)
            continue
        if not in_fence and line.strip() == "---":
            slides.append("\n".join(current).strip())
            current = []
        else:
            current.append(line)
    if current:
        slides.append("\n".join(current).strip())
    return [s for s in slides if s]


def extract_frontmatter(text: str) -> dict:
    fm: dict = {}
    fm_raw, _ = split_frontmatter(text)
    if not fm_raw:
        return fm
    fm_raw = fm_raw.strip("-\n")
    for line in fm_raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def collect_stats(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm = extract_frontmatter(text)
    _, body = split_frontmatter(text)
    slides = split_slides(body)

    stats = {
        "path": str(path),
        "theme": fm.get("theme", "(unset)"),
        "slides": len(slides),
        "headings": 0,
        "bullets": 0,
        "code_blocks": 0,
        "mermaid_diagrams": 0,
        "images": 0,
        "visible_words": 0,
        "note_words": 0,
    }

    for slide in slides:
        # Strip comments for visible-word count; count note words separately.
        note_text = " ".join(m.group(0) for m in COMMENT.finditer(slide))
        visible = COMMENT.sub(" ", slide)

        stats["headings"] += len(HEADING.findall(visible))
        stats["bullets"] += len(BULLET.findall(visible))
        stats["code_blocks"] += len(CODE_FENCE.findall(visible)) // 2
        stats["mermaid_diagrams"] += len(MERMAID_BLOCK.findall(visible))
        stats["images"] += len(IMAGE_RE.findall(visible))
        stats["visible_words"] += len(WORD_RE.findall(visible))
        stats["note_words"] += len(WORD_RE.findall(note_text))

    stats["total_words"] = stats["visible_words"] + stats["note_words"]

    # Duration estimate (150 wpm visible, 180 wpm notes).
    visible_seconds = (stats["visible_words"] / 150) * 60
    note_seconds = (stats["note_words"] / 180) * 60
    stats["estimated_minutes"] = round((visible_seconds + note_seconds) / 60, 1)

    return stats


def summary_line(stats: dict) -> str:
    parts = [
        f"{stats['slides']} slides",
        f"{stats['total_words']} words",
    ]
    if stats["mermaid_diagrams"] + stats["images"] > 0:
        visuals = stats["mermaid_diagrams"] + stats["images"]
        parts.append(f"{visuals} visuals")
    if stats["code_blocks"] > 0:
        parts.append(f"{stats['code_blocks']} code blocks")
    parts.append(f"~{stats['estimated_minutes']} min")
    return " · ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Compute Marp deck stats.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--verbose", action="store_true", help="Print full breakdown.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    path = Path(args.input).resolve()
    if not path.exists():
        print(f"error: input not found: {path}", file=sys.stderr)
        return 2

    stats = collect_stats(path)

    if args.format == "json":
        print(json.dumps(stats, indent=2))
        return 0

    print(summary_line(stats))
    if args.verbose:
        print()
        print(f"  path:             {stats['path']}")
        print(f"  theme:            {stats['theme']}")
        print(f"  slides:           {stats['slides']}")
        print(f"  headings:         {stats['headings']}")
        print(f"  bullets:          {stats['bullets']}")
        print(f"  code blocks:      {stats['code_blocks']}")
        print(f"  mermaid diagrams: {stats['mermaid_diagrams']}")
        print(f"  images:           {stats['images']}")
        print(f"  visible words:    {stats['visible_words']}")
        print(f"  note words:       {stats['note_words']}")
        print(f"  estimated time:   {stats['estimated_minutes']} min")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
