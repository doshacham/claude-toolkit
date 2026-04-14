# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Generate ASCII box diagrams for slide embedding.

Useful for terminal/brutalist/monochrome themes where a monospace box diagram
fits the aesthetic better than Mermaid.

Modes:
- boxes: horizontal chain of labeled boxes with arrows (default)
- tree:  directory-tree style from a newline-separated list of paths
- grid:  2D grid of labeled boxes

Usage:
    python ascii_box.py --mode boxes --labels "Client,API,Service,DB"
    python ascii_box.py --mode tree --input paths.txt
    python ascii_box.py --mode grid --labels "A,B,C,D,E,F" --cols 3
"""

import argparse
import sys
from pathlib import Path


def render_boxes(labels: list[str]) -> str:
    """Horizontal chain: [label1] --> [label2] --> [label3]"""
    if not labels:
        return ""
    # Each box is padded to 2+len+2 with borders.
    boxes = [f"| {lbl} |" for lbl in labels]
    tops = ["+" + "-" * (len(lbl) + 2) + "+" for lbl in labels]
    arrows = [" --> " for _ in labels[:-1]]

    top_line = ""
    mid_line = ""
    bot_line = ""
    for i, (t, b) in enumerate(zip(tops, boxes)):
        top_line += t
        mid_line += b
        bot_line += t
        if i < len(labels) - 1:
            # Center the arrow on the middle row; pad top/bottom with spaces.
            top_line += " " * len(arrows[i])
            mid_line += arrows[i]
            bot_line += " " * len(arrows[i])

    return "\n".join([top_line, mid_line, bot_line])


def render_tree(paths: list[str]) -> str:
    """Render a tree from a list of slash-separated paths."""
    # Build a nested dict.
    root: dict = {}
    for path in paths:
        parts = [p for p in path.strip().split("/") if p]
        node = root
        for p in parts:
            node = node.setdefault(p, {})

    lines: list[str] = []

    def walk(node: dict, prefix: str):
        entries = list(node.items())
        for i, (name, child) in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + name)
            if child:
                extension = "    " if is_last else "│   "
                walk(child, prefix + extension)

    walk(root, "")
    return "\n".join(lines)


def render_grid(labels: list[str], cols: int) -> str:
    """2D grid of labeled boxes. Boxes are uniform width (widest label)."""
    if not labels:
        return ""
    width = max(len(lbl) for lbl in labels) + 2
    rows = [labels[i:i + cols] for i in range(0, len(labels), cols)]

    out: list[str] = []
    for row in rows:
        top = "+" + ("-" * width + "+") * len(row)
        mid = "|" + "".join(f" {lbl:<{width - 1}}|" for lbl in row)
        out.append(top)
        out.append(mid)
    out.append("+" + ("-" * width + "+") * len(rows[-1]))
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Generate ASCII box diagrams.")
    parser.add_argument("--mode", required=True, choices=["boxes", "tree", "grid"])
    parser.add_argument("--labels", help="Comma-separated labels (boxes, grid).")
    parser.add_argument("--input", help="File with newline-separated paths (tree).")
    parser.add_argument("--cols", type=int, default=3, help="Grid column count.")
    parser.add_argument("--out", help="Write to file instead of stdout.")
    parser.add_argument("--fence", action="store_true",
                        help="Wrap output in triple-backtick fences for Markdown.")
    args = parser.parse_args()

    labels: list[str] = []
    if args.mode in ("boxes", "grid"):
        if not args.labels:
            print(f"error: --labels required for {args.mode}", file=sys.stderr)
            return 2
        labels = [lbl.strip() for lbl in args.labels.split(",") if lbl.strip()]

    if args.mode == "boxes":
        out = render_boxes(labels)
    elif args.mode == "grid":
        out = render_grid(labels, args.cols)
    elif args.mode == "tree":
        if not args.input:
            print("error: --input required for tree", file=sys.stderr)
            return 2
        src = Path(args.input).resolve()
        if not src.exists():
            print(f"error: input not found: {src}", file=sys.stderr)
            return 2
        paths = [line for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]
        out = render_tree(paths)
    else:
        print(f"error: unknown mode: {args.mode}", file=sys.stderr)
        return 2

    if args.fence:
        out = f"```\n{out}\n```"

    if args.out:
        dest = Path(args.out).resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out + "\n", encoding="utf-8")
        print(f"ok: wrote {dest}")
    else:
        print(out)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
