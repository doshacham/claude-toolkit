# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Insert (or replace) a table-of-contents slide in a Marp deck.

Walks the deck, extracts the first heading of each slide, and inserts a TOC
slide at the given position. By default the TOC goes at slide 2 (just after
the title slide).

Detects an existing TOC slide (one that starts with "## Contents" or
"## Outline" or "## Table of contents") and replaces it in place.

Usage:
    python insert_toc.py --input deck.md
    python insert_toc.py --input deck.md --at 2 --title "Outline"
    python insert_toc.py --input deck.md --max-depth 2  # include h2 subsections
"""

import argparse
import re
import sys
from pathlib import Path


HEADING = re.compile(r"^\s*(#{1,3})\s+(.+?)\s*$", re.MULTILINE)
TOC_MARKER = re.compile(r"^\s*##\s+(contents|outline|table of contents)\s*$",
                        re.MULTILINE | re.IGNORECASE)


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
            slides.append("\n".join(current).rstrip())
            current = []
        else:
            current.append(line)
    if current:
        slides.append("\n".join(current).rstrip())
    return slides


def first_heading(slide: str, max_depth: int) -> tuple[int, str] | None:
    """Return (level, text) of the first heading at or above max_depth."""
    for m in HEADING.finditer(slide):
        level = len(m.group(1))
        if level <= max_depth:
            return level, m.group(2).strip()
    return None


def build_toc_slide(
    slides: list[str],
    skip_indices: set[int],
    toc_title: str,
    max_depth: int,
) -> str:
    """Build a new TOC slide as a markdown string."""
    lines = [f"## {toc_title}", ""]
    for idx, slide in enumerate(slides, start=1):
        if idx - 1 in skip_indices:
            continue
        heading = first_heading(slide, max_depth)
        if heading is None:
            continue
        level, text = heading
        if level == 1:
            lines.append(f"{idx}. **{text}**")
        else:
            lines.append(f"{idx}. {text}")
    return "\n".join(lines)


def is_toc_slide(slide: str) -> bool:
    return bool(TOC_MARKER.search(slide))


def is_lead_slide(slide: str) -> bool:
    """Heuristic: first slide or any slide with `<!-- _class: lead -->`."""
    return "_class: lead" in slide


def main():
    parser = argparse.ArgumentParser(description="Insert a TOC slide into a Marp deck.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", help="Write to a new file (default: overwrite input).")
    parser.add_argument("--at", type=int, default=2,
                        help="Slide number at which to insert the TOC (1-based). Default 2.")
    parser.add_argument("--title", default="Outline",
                        help='Heading text for the TOC slide (default "Outline").')
    parser.add_argument("--max-depth", type=int, default=1,
                        help="Max heading depth to include (1 = h1 only, 2 = h1+h2).")
    args = parser.parse_args()

    path = Path(args.input).resolve()
    if not path.exists():
        print(f"error: input not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    slides = split_slides(body)

    # Detect existing TOC.
    existing_toc_idx: int | None = None
    for i, s in enumerate(slides):
        if is_toc_slide(s):
            existing_toc_idx = i
            break

    # Skip lead + existing TOC when building the list.
    skip = set()
    for i, s in enumerate(slides):
        if is_lead_slide(s) or is_toc_slide(s):
            skip.add(i)

    toc_body = build_toc_slide(slides, skip, args.title, args.max_depth)

    if existing_toc_idx is not None:
        slides[existing_toc_idx] = toc_body
        action = f"replaced existing TOC at slide {existing_toc_idx + 1}"
    else:
        insert_at = max(1, min(args.at, len(slides) + 1)) - 1
        slides.insert(insert_at, toc_body)
        action = f"inserted TOC at slide {insert_at + 1}"

    new_body = "\n\n---\n\n".join(slides)
    if fm:
        new_text = fm + "\n\n" + new_body.lstrip("\n") + "\n"
    else:
        new_text = new_body + "\n"

    out = Path(args.out).resolve() if args.out else path
    out.write_text(new_text, encoding="utf-8")
    print(f"ok: {action} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
