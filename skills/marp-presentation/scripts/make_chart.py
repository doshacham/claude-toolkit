# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Generate a themed PNG chart from a CSV file.

Uses matplotlib. Auto-applies a color palette matching the selected deck theme
so charts blend with the slide aesthetic.

Usage:
    python make_chart.py --csv data.csv --type bar --x quarter --y revenue --out chart.png
    python make_chart.py --csv data.csv --type line --x day --y signups --theme midnight
    python make_chart.py --csv data.csv --type heatmap --out matrix.png --theme dashboard

Supported types: bar, barh, line, scatter, histogram, box, heatmap, pie.
"""

import argparse
import csv
import sys
from pathlib import Path


TYPES = {"bar", "barh", "line", "scatter", "histogram", "box", "heatmap", "pie"}

# Palettes tuned per theme. Each is a list of hex colors + bg + fg.
THEME_PALETTES = {
    "midnight":     {"bg": "#0a0e27", "fg": "#e2e8f0", "grid": "#334155",
                     "cycle": ["#22d3ee", "#a78bfa", "#f472b6", "#fcd34d", "#6ee7b7"]},
    "paper":        {"bg": "#f5f0e6", "fg": "#2a2520", "grid": "#c9b98f",
                     "cycle": ["#6b4226", "#8b3a3a", "#5a4a3a", "#3d2f20", "#1e5a8a"]},
    "terminal":     {"bg": "#000000", "fg": "#33ff33", "grid": "#1a1a1a",
                     "cycle": ["#33ff33", "#00ffff", "#ffff33", "#ff66cc", "#66ff66"]},
    "corporate":    {"bg": "#ffffff", "fg": "#1e293b", "grid": "#e2e8f0",
                     "cycle": ["#1e40af", "#0891b2", "#be185d", "#ca8a04", "#15803d"]},
    "brutalist":    {"bg": "#ffffff", "fg": "#000000", "grid": "#000000",
                     "cycle": ["#000000", "#555555", "#aaaaaa", "#222222", "#888888"]},
    "neon":         {"bg": "#0a0015", "fg": "#f0abfc", "grid": "#2a0040",
                     "cycle": ["#ff00ff", "#00ffff", "#ffff00", "#00ff88", "#ff6600"]},
    "academic":     {"bg": "#fdfaf3", "fg": "#1a1510", "grid": "#c9b98f",
                     "cycle": ["#1a1510", "#5a4a3a", "#3d2f20", "#6b4226", "#8b3a3a"]},
    "dashboard":    {"bg": "#1e293b", "fg": "#e2e8f0", "grid": "#334155",
                     "cycle": ["#10b981", "#60a5fa", "#fbbf24", "#f472b6", "#a78bfa"]},
    "minimal":      {"bg": "#ffffff", "fg": "#111111", "grid": "#eeeeee",
                     "cycle": ["#000000", "#555555", "#888888", "#bbbbbb", "#333333"]},
    "gradient":     {"bg": "#764ba2", "fg": "#ffffff", "grid": "#9d73bd",
                     "cycle": ["#fef08a", "#f093fb", "#667eea", "#fce7f3", "#fbbf24"]},
    "blueprint":    {"bg": "#0d2847", "fg": "#cfe8ff", "grid": "#1e4670",
                     "cycle": ["#64b4ff", "#ffda5e", "#a0d0ff", "#ffffff", "#cfe8ff"]},
    "monochrome":   {"bg": "#f5f5f5", "fg": "#1a1a1a", "grid": "#cccccc",
                     "cycle": ["#000000", "#444444", "#888888", "#bbbbbb", "#222222"]},
    "kraft":        {"bg": "#c9a876", "fg": "#3d2817", "grid": "#8b6f47",
                     "cycle": ["#8b3a3a", "#1e5a8a", "#3d2817", "#5a3d20", "#fef3a4"]},
    "high_contrast":{"bg": "#ffffff", "fg": "#000000", "grid": "#000000",
                     "cycle": ["#000000", "#0000ee", "#ffff00", "#cc0000", "#008800"]},
    "pastel":       {"bg": "#fef7f7", "fg": "#4a4458", "grid": "#f3e8ff",
                     "cycle": ["#c084fc", "#f472b6", "#60a5fa", "#fef08a", "#fbcfe8"]},
}


def apply_theme(theme: str):
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    palette = THEME_PALETTES.get(theme, THEME_PALETTES["corporate"])
    mpl.rcParams.update({
        "figure.facecolor": palette["bg"],
        "axes.facecolor": palette["bg"],
        "axes.edgecolor": palette["fg"],
        "axes.labelcolor": palette["fg"],
        "xtick.color": palette["fg"],
        "ytick.color": palette["fg"],
        "text.color": palette["fg"],
        "grid.color": palette["grid"],
        "axes.prop_cycle": plt.cycler(color=palette["cycle"]),
        "savefig.facecolor": palette["bg"],
        "savefig.edgecolor": palette["bg"],
    })


def read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            raise ValueError("csv is empty")
        headers = reader.fieldnames or []
    return headers, rows


def coerce(value: str):
    try:
        return float(value)
    except (ValueError, TypeError):
        return value


def main():
    parser = argparse.ArgumentParser(description="Generate a themed chart PNG.")
    parser.add_argument("--csv", required=True, help="Path to CSV input.")
    parser.add_argument("--type", required=True, choices=sorted(TYPES))
    parser.add_argument("--x", help="Column name for x axis (bar/line/scatter).")
    parser.add_argument("--y", help="Column name for y axis (bar/line/scatter/box).")
    parser.add_argument("--out", required=True, help="Output PNG path.")
    parser.add_argument("--theme", default="corporate", choices=sorted(THEME_PALETTES.keys()))
    parser.add_argument("--title", default="")
    parser.add_argument("--width", type=float, default=8.0)
    parser.add_argument("--height", type=float, default=5.0)
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("error: matplotlib not installed. run: pip install matplotlib",
              file=sys.stderr)
        return 2

    apply_theme(args.theme)

    csv_path = Path(args.csv).resolve()
    if not csv_path.exists():
        print(f"error: csv not found: {csv_path}", file=sys.stderr)
        return 2

    headers, rows = read_csv(csv_path)
    fig, ax = plt.subplots(figsize=(args.width, args.height), dpi=args.dpi)

    if args.type in ("bar", "barh", "line", "scatter"):
        if not args.x or not args.y:
            print(f"error: --x and --y required for {args.type}", file=sys.stderr)
            return 2
        xs = [coerce(r[args.x]) for r in rows]
        ys = [coerce(r[args.y]) for r in rows]
        if args.type == "bar":
            ax.bar(xs, ys)
        elif args.type == "barh":
            ax.barh(xs, ys)
        elif args.type == "line":
            ax.plot(xs, ys, marker="o")
        elif args.type == "scatter":
            ax.scatter(xs, ys)
        ax.set_xlabel(args.x)
        ax.set_ylabel(args.y)

    elif args.type == "histogram":
        if not args.y:
            print("error: --y required for histogram", file=sys.stderr)
            return 2
        values = [coerce(r[args.y]) for r in rows]
        values = [v for v in values if isinstance(v, (int, float))]
        ax.hist(values, bins=20)
        ax.set_xlabel(args.y)
        ax.set_ylabel("frequency")

    elif args.type == "box":
        # One box per numeric column if no --y specified.
        numeric_cols = args.y.split(",") if args.y else [
            h for h in headers
            if any(isinstance(coerce(r[h]), (int, float)) for r in rows)
        ]
        data = [
            [coerce(r[c]) for r in rows if isinstance(coerce(r[c]), (int, float))]
            for c in numeric_cols
        ]
        ax.boxplot(data, tick_labels=numeric_cols)

    elif args.type == "heatmap":
        # Expect the CSV to be a numeric matrix (first column = row label).
        label_col = headers[0]
        value_cols = headers[1:]
        labels = [r[label_col] for r in rows]
        matrix = [[coerce(r[c]) for c in value_cols] for r in rows]
        im = ax.imshow(matrix, aspect="auto", cmap="viridis")
        ax.set_xticks(range(len(value_cols)), labels=value_cols, rotation=45)
        ax.set_yticks(range(len(labels)), labels=labels)
        fig.colorbar(im, ax=ax)

    elif args.type == "pie":
        if not args.x or not args.y:
            print("error: --x (labels) and --y (values) required for pie",
                  file=sys.stderr)
            return 2
        labels = [r[args.x] for r in rows]
        values = [coerce(r[args.y]) for r in rows]
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_aspect("equal")

    if args.title:
        ax.set_title(args.title)

    if args.type not in ("pie", "heatmap"):
        ax.grid(True, linestyle="--", alpha=0.3)

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=args.dpi)
    print(f"ok: wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
