# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Suggest a deck mode based on source material.

Given a file or directory of source material, computes signals and returns a
ranked list of modes the source is most likely to fit:

- technical: code density (def/class/function/imports/brackets)
- research: tex, bibtex, arxiv refs, math equations
- narrative: vision/launch/mission/stakes keywords, emotional words
- data: CSV, JSON arrays, SQL, numeric density
- onboarding: README, .env.example, contributing guide, how-to language
- architecture: C4/container/component keywords, sequence diagram patterns

Output:
    {
      "ranked": [["technical", 0.62], ["architecture", 0.24], ...],
      "signals": { ... }
    }

Usage:
    python detect_mode.py --input src/auth.py
    python detect_mode.py --input ./my-repo --format text
    python detect_mode.py --input paper.md
"""

import argparse
import json
import re
import sys
from pathlib import Path


MAX_BYTES_PER_FILE = 200_000  # Skip massive files (generated, binary).
MAX_TOTAL_BYTES = 2_000_000  # Cap total bytes scanned for a directory.

CODE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cpp", ".c", ".rb", ".php"}
DATA_EXTS = {".csv", ".tsv", ".json", ".yaml", ".yml", ".sql"}
TEXT_EXTS = {".md", ".txt", ".tex", ".rst"}

SIGNALS = {
    "technical": {
        "keywords": ["def ", "function ", "class ", "import ", "from ", "return ",
                     "const ", "let ", "var ", "async ", "await ", "public ",
                     "private ", "struct ", "impl ", "fn ", "pub "],
        "patterns": [r"\{[^}]*\}", r"\(.*?\)", r"=>"],
    },
    "research": {
        "keywords": ["abstract", "\\cite", "\\section", "\\begin", "arxiv",
                     "et al.", "bibliography", "theorem", "lemma", "proof"],
        "patterns": [r"\$\$.*?\$\$", r"\\\w+\{"],
    },
    "narrative": {
        "keywords": ["vision", "mission", "launch", "pitch", "story", "journey",
                     "customer", "user", "imagine", "believe", "transform",
                     "disrupt", "change the world", "our ask"],
        "patterns": [r"\"[^\"]{20,}\""],  # long quoted sections
    },
    "data": {
        "keywords": ["select ", "from ", "where ", "group by ", "count(",
                     "sum(", "avg(", "percent", "rate", "conversion",
                     "cohort", "lift", "metric"],
        "patterns": [r"\d{1,3}(?:,\d{3})*\.?\d*", r"\d+\.\d+%", r"\$\d"],
    },
    "onboarding": {
        "keywords": ["readme", "getting started", "installation", "setup",
                     "prerequisites", "contributing", "first pr", "onboarding",
                     "how to", "welcome"],
        "patterns": [r"```sh", r"```bash", r"npm install", r"pip install"],
    },
    "architecture": {
        "keywords": ["architecture", "system design", "microservice",
                     "database", "api gateway", "load balancer", "service mesh",
                     "container", "component", "subsystem", "context diagram",
                     "sla", "slo", "rps", "latency", "throughput"],
        "patterns": [r"C4(Context|Container|Component|Dynamic|Deployment)",
                     r"sequenceDiagram"],
    },
}


def read_source(path: Path) -> str:
    """Read a file or walk a directory, capping total bytes."""
    if path.is_file():
        try:
            return path.read_text(encoding="utf-8", errors="ignore")[:MAX_BYTES_PER_FILE]
        except OSError:
            return ""

    if not path.is_dir():
        return ""

    ignore_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv",
                   "dist", "build", ".next", "target"}
    buf = []
    total = 0
    for p in sorted(path.rglob("*")):
        if any(part in ignore_dirs for part in p.parts):
            continue
        if not p.is_file():
            continue
        if p.suffix.lower() not in CODE_EXTS | DATA_EXTS | TEXT_EXTS:
            continue
        try:
            chunk = p.read_text(encoding="utf-8", errors="ignore")[:MAX_BYTES_PER_FILE]
        except OSError:
            continue
        buf.append(chunk)
        total += len(chunk)
        if total >= MAX_TOTAL_BYTES:
            break
    return "\n".join(buf)


def score(text: str) -> dict:
    """Return raw signal scores per mode."""
    lower = text.lower()
    results: dict[str, float] = {}
    details: dict[str, dict] = {}

    for mode, cfg in SIGNALS.items():
        keyword_count = sum(lower.count(kw.lower()) for kw in cfg["keywords"])
        pattern_count = 0
        for pat in cfg["patterns"]:
            try:
                pattern_count += len(re.findall(pat, text, re.DOTALL))
            except re.error:
                pass
        raw = keyword_count * 2 + pattern_count
        results[mode] = float(raw)
        details[mode] = {"keywords": keyword_count, "patterns": pattern_count}

    # Normalize to probabilities.
    total = sum(results.values()) or 1.0
    normalized = {m: round(v / total, 3) for m, v in results.items()}

    return {"ranked": sorted(normalized.items(), key=lambda kv: -kv[1]),
            "details": details}


def main():
    parser = argparse.ArgumentParser(description="Suggest a deck mode from source.")
    parser.add_argument("--input", required=True, help="File or directory.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    path = Path(args.input).resolve()
    if not path.exists():
        print(f"error: not found: {path}", file=sys.stderr)
        return 2

    text = read_source(path)
    if not text.strip():
        print("warning: no readable text found", file=sys.stderr)
        return 1

    result = score(text)

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0

    print(f"source: {path}")
    print(f"scanned: {len(text):,} characters\n")
    print("mode ranking (higher = stronger fit):")
    for mode, p in result["ranked"]:
        bar = "#" * int(p * 40)
        print(f"  {mode:14s} {p:.3f}  {bar}")
    print(f"\ntop suggestion: {result['ranked'][0][0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
