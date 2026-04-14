# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Estimate the speaking duration of a Marp deck.

Counts words in visible slide content and in speaker notes (HTML comments that
are not Marp directives). Applies words-per-minute rates to produce:

- Total duration
- Per-slide duration
- Flags for slides that run long (>1.5 min per slide, unless the slide has a
  lot of speaker notes which justify the extra time)

Defaults:
- 150 wpm for visible content (a slide title + paragraph reads slow)
- 180 wpm for speaker notes (the presenter reads/paraphrases faster)

Usage:
    python estimate_duration.py --input deck.md
    python estimate_duration.py --input deck.md --target-minutes 15
    python estimate_duration.py --input deck.md --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path


SLIDE_SEP = re.compile(r"^---\s*$", re.MULTILINE)
COMMENT = re.compile(r"<!--\s*(.*?)\s*-->", re.DOTALL)
CODE_FENCE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
DIRECTIVE_PREFIX = re.compile(
    r"^\s*(_|class:|theme:|paginate:|backgroundColor:|color:|header:|footer:|"
    r"size:|math:|style:|marp:)",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[A-Za-z0-9']+")


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:]


def split_slides(body: str):
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
            text = "\n".join(current).strip()
            if text:
                slides.append(text)
            current = []
        else:
            current.append(line)
    tail = "\n".join(current).strip()
    if tail:
        slides.append(tail)
    return slides


def extract_notes(slide: str) -> str:
    parts = []
    for m in COMMENT.finditer(slide):
        inner = m.group(1).strip()
        if not inner or DIRECTIVE_PREFIX.match(inner):
            continue
        parts.append(inner)
    return "\n".join(parts)


def strip_for_visible(slide: str) -> str:
    """Remove comments and code-block *content* from the visible word count."""
    # Remove speaker-note comments (they count separately).
    without_comments = COMMENT.sub(" ", slide)
    # Remove code-block bodies (the agent rarely reads them aloud verbatim).
    without_code = CODE_FENCE.sub(" ", without_comments)
    return without_code


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def estimate(path: Path, slide_wpm: int, note_wpm: int):
    text = path.read_text(encoding="utf-8")
    body = parse_frontmatter(text)
    slides = split_slides(body)

    per_slide = []
    total_visible_words = 0
    total_note_words = 0

    for idx, slide in enumerate(slides, start=1):
        visible = strip_for_visible(slide)
        notes = extract_notes(slide)

        vwords = count_words(visible)
        nwords = count_words(notes)

        vsec = (vwords / slide_wpm) * 60
        nsec = (nwords / note_wpm) * 60
        total_sec = vsec + nsec

        total_visible_words += vwords
        total_note_words += nwords

        per_slide.append({
            "slide": idx,
            "visible_words": vwords,
            "note_words": nwords,
            "seconds": round(total_sec, 1),
            "long": total_sec > 90,  # >1.5 min flag
        })

    total_seconds = sum(s["seconds"] for s in per_slide)
    return {
        "slides": len(slides),
        "visible_words": total_visible_words,
        "note_words": total_note_words,
        "total_words": total_visible_words + total_note_words,
        "slide_wpm": slide_wpm,
        "note_wpm": note_wpm,
        "total_seconds": round(total_seconds, 1),
        "total_minutes": round(total_seconds / 60, 1),
        "per_slide": per_slide,
    }


def fmt_duration(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m{s:02d}s"


def main():
    parser = argparse.ArgumentParser(description="Estimate deck speaking duration.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--slide-wpm", type=int, default=150,
                        help="Words per minute for visible slide content (default 150).")
    parser.add_argument("--note-wpm", type=int, default=180,
                        help="Words per minute for speaker notes (default 180).")
    parser.add_argument("--target-minutes", type=float,
                        help="If set, warn when total duration is outside ±20%% of target.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    path = Path(args.input).resolve()
    if not path.exists():
        print(f"error: input not found: {path}", file=sys.stderr)
        return 2

    result = estimate(path, args.slide_wpm, args.note_wpm)

    if args.target_minutes:
        lo = args.target_minutes * 0.8
        hi = args.target_minutes * 1.2
        result["target_minutes"] = args.target_minutes
        result["within_target"] = lo <= result["total_minutes"] <= hi

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0

    # Text format.
    print(f"deck:   {path}")
    print(f"slides: {result['slides']}")
    print(f"words:  {result['total_words']} "
          f"({result['visible_words']} visible + {result['note_words']} notes)")
    print(f"total:  {fmt_duration(result['total_seconds'])} "
          f"({result['total_minutes']} min) "
          f"@ {result['slide_wpm']}/{result['note_wpm']} wpm")

    if "target_minutes" in result:
        status = "within target" if result["within_target"] else "OUTSIDE target"
        print(f"target: {result['target_minutes']} min -> {status}")

    longs = [s for s in result["per_slide"] if s["long"]]
    if longs:
        print(f"\nlong slides (>1.5 min):")
        for s in longs:
            print(f"  slide {s['slide']}: {fmt_duration(s['seconds'])} "
                  f"({s['visible_words']}+{s['note_words']} words)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
