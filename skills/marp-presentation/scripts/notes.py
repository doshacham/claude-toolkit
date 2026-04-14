# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Extract speaker notes from a Marp deck into a standalone Markdown file.

Marp speaker notes are HTML comments inside slides. This script walks the
deck, finds each `<!-- ... -->` that is NOT a Marp directive, and writes
them grouped by slide number to a presenter script.

Directives (skipped): comments whose first non-whitespace token starts with
`_` (like `_class: lead`) or `class:`, `theme:`, `paginate:`, etc.

Usage:
    python notes.py --input deck.md --out notes.md
    python notes.py --input deck.md --out speaker.md --title "My Talk"
"""

import argparse
import re
import sys
from pathlib import Path


SLIDE_SEP = re.compile(r"^---\s*$", re.MULTILINE)
COMMENT = re.compile(r"<!--\s*(.*?)\s*-->", re.DOTALL)
DIRECTIVE_PREFIX = re.compile(
    r"^\s*(_|class:|theme:|paginate:|backgroundColor:|color:|header:|footer:|"
    r"size:|math:|style:|marp:)",
    re.IGNORECASE,
)


def parse_frontmatter(text: str) -> tuple[str, str]:
    """Split frontmatter from body. Return (frontmatter_raw, body)."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[:end + 4], text[end + 4:]


def extract_slide_title(slide: str) -> str:
    """Use the first heading as a slide title hint."""
    for line in slide.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("# ").strip()
    return ""


def extract_notes_from_slide(slide: str) -> list[str]:
    """Return non-directive comments inside a slide."""
    notes = []
    for m in COMMENT.finditer(slide):
        inner = m.group(1).strip()
        if not inner:
            continue
        if DIRECTIVE_PREFIX.match(inner):
            continue
        notes.append(inner)
    return notes


def main():
    parser = argparse.ArgumentParser(description="Extract speaker notes from Marp deck.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--title", default="", help="Optional title for the notes doc.")
    args = parser.parse_args()

    src = Path(args.input).resolve()
    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2

    text = src.read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)

    # Strip code fences so we don't split on `---` inside them.
    slides_raw = body.lstrip("\n")

    # Simple state machine: split on `---` at top level only (not inside ```).
    slides: list[str] = []
    current: list[str] = []
    in_fence = False
    for line in slides_raw.splitlines():
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
    slides = [s for s in slides if s]

    out_lines: list[str] = []
    title = args.title or src.stem
    out_lines.append(f"# Speaker notes — {title}\n")
    out_lines.append(f"Source: `{src.name}`\n")
    out_lines.append(f"Total slides: {len(slides)}\n")
    out_lines.append("")

    for idx, slide in enumerate(slides, start=1):
        slide_title = extract_slide_title(slide) or "(untitled)"
        notes = extract_notes_from_slide(slide)
        out_lines.append(f"## Slide {idx}: {slide_title}\n")
        if notes:
            for note in notes:
                out_lines.append(f"> {note}\n")
        else:
            out_lines.append("_(no notes)_\n")
        out_lines.append("")

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"ok: wrote {out} ({len(slides)} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
