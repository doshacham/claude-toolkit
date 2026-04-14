# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Scaffold a new Marp deck from a template + theme.

Copies a template to the target path, replaces placeholder tokens in the
frontmatter (title, subtitle, author), and embeds the chosen theme CSS.

Usage:
    python new_deck.py --template technical --theme midnight \
        --out ./deck.md --title "Auth Rewrite" --subtitle "Design review"
"""

import argparse
import sys
from pathlib import Path


TEMPLATES = {"default", "technical", "narrative", "academic", "data"}

THEMES = {
    "midnight", "paper", "terminal", "corporate", "brutalist",
    "neon", "academic", "dashboard", "minimal", "gradient",
    "blueprint", "monochrome", "kraft", "high_contrast", "pastel",
}


def main():
    parser = argparse.ArgumentParser(description="Scaffold a Marp deck.")
    parser.add_argument("--template", required=True, choices=sorted(TEMPLATES))
    parser.add_argument("--theme", required=True, choices=sorted(THEMES))
    parser.add_argument("--out", required=True, help="Output .md path.")
    parser.add_argument("--title", default="Untitled Deck")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--author", default="")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    skill_root = here.parent

    template_path = skill_root / "templates" / f"{args.template}.md"
    if not template_path.exists():
        print(f"error: template not found: {template_path}", file=sys.stderr)
        return 2

    theme_path = skill_root / "themes" / f"{args.theme}.css"
    if not theme_path.exists():
        print(f"error: theme not found: {theme_path}", file=sys.stderr)
        return 2

    out = Path(args.out).resolve()
    if out.exists():
        print(f"error: refusing to overwrite existing file: {out}", file=sys.stderr)
        return 2

    # Theme file is referenced by name in frontmatter; render.py registers it
    # via Marp's --theme-set. We only verify it exists here.
    _ = theme_path

    template_body = template_path.read_text(encoding="utf-8")

    # Token substitution.
    content = template_body
    content = content.replace("{{TITLE}}", args.title)
    content = content.replace("{{SUBTITLE}}", args.subtitle)
    content = content.replace("{{AUTHOR}}", args.author)
    content = content.replace("{{THEME_NAME}}", args.theme)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"ok: scaffolded {out}")
    print(f"  template: {args.template}")
    print(f"  theme:    {args.theme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
