# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Lint a Marp deck before rendering.

Deterministic checks (always run):
- Frontmatter has `marp: true`
- Slide count sanity (global floor of 3; ceiling 40 unless --mode overrides)
- Per-mode slide budget (if --mode is passed)
- Per-slide line-count heuristic (warn on slides > 25 source lines)
- No slide has more than 5 bullets (warn)
- All fenced code blocks close properly (error)
- Title-as-assertion check: warn on topic-only titles
- Link check: HEAD every http/https URL via curl, warn on 4xx/5xx

Optional checks (run if tools are installed via npx):
- markdownlint-cli2
- cspell

Outputs a JSON report to stdout (or --format text). Exit 0 on no errors, 1 otherwise.

Usage:
    python lint.py --input ./deck.md
    python lint.py --input ./deck.md --mode technical --format text
    python lint.py --input ./deck.md --no-links
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


SLIDE_SEPARATOR = re.compile(r"^---\s*$", re.MULTILINE)
BULLET_LINE = re.compile(r"^\s*[-*+] ", re.MULTILINE)
CODE_FENCE = re.compile(r"^```", re.MULTILINE)
HEADING = re.compile(r"^\s*(#{1,3})\s+(.+?)\s*$", re.MULTILINE)
MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")

# Per-mode slide budgets (min_slides, max_slides).
MODE_BUDGETS = {
    "technical":    (12, 25),
    "research":     (10, 20),
    "narrative":    (6, 15),
    "data":         (5, 12),
    "onboarding":   (8, 18),
    "architecture": (8, 18),
}

# Per-mode speaking-time budgets (min_minutes, max_minutes).
MODE_TIME_BUDGETS = {
    "technical":    (15, 30),
    "research":     (12, 20),
    "narrative":    (5, 15),
    "data":         (5, 12),
    "onboarding":   (10, 25),
    "architecture": (10, 25),
}

COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
CODE_BLOCK_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
WORD_RE = re.compile(r"[A-Za-z0-9']+")
DIRECTIVE_PREFIX_RE = re.compile(
    r"^\s*(_|class:|theme:|paginate:|backgroundColor:|color:|header:|footer:|"
    r"size:|math:|style:|marp:)",
    re.IGNORECASE,
)

# Heuristics for title-as-assertion detection.
ASSERTION_VERBS = {
    "is", "are", "was", "were", "has", "have", "had", "does", "did", "do",
    "will", "would", "should", "can", "could", "must", "may", "might",
    "lost", "gained", "doubled", "tripled", "halved", "grew", "shrank",
    "shipped", "broke", "fixed", "fell", "rose", "dropped", "jumped",
    "drives", "drove", "caused", "needs", "wants", "takes", "moves",
    "shows", "proves", "means", "beats", "wins", "loses", "matters",
    "costs", "saves", "earns", "kills", "launches", "launched",
}
# Clearly topic-style words that almost never signal an assertion title.
TOPIC_WORDS = {
    "overview", "summary", "introduction", "background", "metrics",
    "results", "conclusion", "agenda", "outline", "architecture",
}

NUM_RE = re.compile(r"\d")


def parse_frontmatter(text: str):
    """Return (frontmatter_dict, body) or (None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_raw = text[4:end].strip()
    body = text[end + 4:]
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def split_slides(body: str):
    """Split body into slide chunks using top-level `---` separators.

    Respects code fences — a `---` inside ```...``` does NOT split.
    """
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


def check_code_fences_balanced(text: str):
    return len(CODE_FENCE.findall(text)) % 2 == 0


def slide_title(slide: str) -> str | None:
    """First heading line of the slide, stripped of leading #."""
    m = HEADING.search(slide)
    if not m:
        return None
    return m.group(2).strip()


def is_assertion_title(title: str) -> bool:
    """Heuristic: does this title read as a finding/assertion rather than a topic?

    A title is assertion-like if ANY of:
    - Contains a digit (numbers strongly signal findings)
    - Contains a verb from ASSERTION_VERBS
    - Has 6+ words (long titles usually contain clauses)
    - Ends with ? (question framing is OK)
    """
    if not title:
        return True  # don't flag empty; other checks will
    if NUM_RE.search(title):
        return True
    if title.rstrip().endswith("?"):
        return True
    words = re.findall(r"[A-Za-z']+", title.lower())
    if not words:
        return True
    if len(words) >= 6:
        return True
    if any(w in ASSERTION_VERBS for w in words):
        return True
    if any(w in TOPIC_WORDS for w in words) and len(words) <= 3:
        return False
    # Default: short noun-only phrase → topic (flag).
    return False


def run_optional(cmd):
    exe = shutil.which(cmd[0]) or shutil.which(cmd[0] + ".cmd")
    if not exe:
        return False, "", "", 0
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return True, result.stdout, result.stderr, result.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return True, "", str(e), 1


def estimate_minutes(body: str, slide_wpm: int = 150, note_wpm: int = 180) -> float:
    """Estimate speaking duration (in minutes) for the deck body.

    Counts visible words (stripping code blocks and HTML comments) and note
    words (non-directive HTML comments), applies per-category wpm rates.
    """
    visible_words = 0
    note_words = 0

    # Notes first (before stripping them out for visible count).
    for m in COMMENT_RE.finditer(body):
        inner = m.group(0)[4:-3].strip()  # strip <!-- -->
        if not inner or DIRECTIVE_PREFIX_RE.match(inner):
            continue
        note_words += len(WORD_RE.findall(inner))

    # Visible: body minus comments minus code blocks.
    visible = COMMENT_RE.sub(" ", body)
    visible = CODE_BLOCK_RE.sub(" ", visible)
    visible_words = len(WORD_RE.findall(visible))

    seconds = (visible_words / slide_wpm) * 60 + (note_words / note_wpm) * 60
    return seconds / 60


def check_links(text: str, timeout: int = 5) -> list[tuple[str, int]]:
    """HEAD every http(s) link, return list of (url, status) where status != 200."""
    curl = shutil.which("curl") or shutil.which("curl.exe")
    if not curl:
        return []

    bad: list[tuple[str, int]] = []
    seen: set[str] = set()
    for m in MD_LINK.finditer(text):
        url = m.group(2).strip()
        if url in seen:
            continue
        seen.add(url)
        try:
            result = subprocess.run(
                [curl, "--ssl-no-revoke", "-sI", "-o", "/dev/null",
                 "-w", "%{http_code}", "-m", str(timeout), url],
                capture_output=True, text=True, timeout=timeout + 2,
            )
            code = int(result.stdout.strip() or "0")
            if code < 200 or code >= 400:
                bad.append((url, code))
        except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
            bad.append((url, -1))
    return bad


def lint_deck(path: Path, mode: str | None, check_links_flag: bool):
    text = path.read_text(encoding="utf-8")
    issues: list[dict] = []

    # Frontmatter.
    fm, body = parse_frontmatter(text)
    if fm is None:
        issues.append({"severity": "error", "type": "frontmatter",
                       "detail": "missing YAML frontmatter"})
        return issues, 0

    if fm.get("marp", "").lower() != "true":
        issues.append({"severity": "error", "type": "frontmatter",
                       "detail": "frontmatter missing `marp: true`"})

    # Code fence balance.
    if not check_code_fences_balanced(text):
        issues.append({"severity": "error", "type": "syntax",
                       "detail": "unbalanced fenced code blocks"})

    # Slide breakdown.
    slides = split_slides(body)
    slide_count = len(slides)

    # Global sanity.
    if slide_count < 3:
        issues.append({"severity": "warning", "type": "slide_count",
                       "detail": f"only {slide_count} slides; decks under 3 are rarely useful"})
    if slide_count > 40:
        issues.append({"severity": "warning", "type": "slide_count",
                       "detail": f"{slide_count} slides is long; consider splitting"})

    # Per-mode slide budget.
    if mode and mode in MODE_BUDGETS:
        lo, hi = MODE_BUDGETS[mode]
        if slide_count < lo:
            issues.append({"severity": "warning", "type": "mode_budget",
                           "detail": f"{mode} decks usually land {lo}-{hi} slides; you have {slide_count}"})
        elif slide_count > hi:
            issues.append({"severity": "warning", "type": "mode_budget",
                           "detail": f"{mode} decks usually land {lo}-{hi} slides; you have {slide_count}"})

    # Per-mode time budget.
    if mode and mode in MODE_TIME_BUDGETS:
        duration = estimate_minutes(body)
        lo_t, hi_t = MODE_TIME_BUDGETS[mode]
        if duration < lo_t:
            issues.append({"severity": "info", "type": "mode_duration",
                           "detail": f"estimated {duration:.1f} min; {mode} decks typically run {lo_t}-{hi_t} min"})
        elif duration > hi_t:
            issues.append({"severity": "warning", "type": "mode_duration",
                           "detail": f"estimated {duration:.1f} min; {mode} decks typically run {lo_t}-{hi_t} min"})

    # Per-slide checks.
    for idx, slide in enumerate(slides, start=1):
        lines = slide.splitlines()
        if len(lines) > 25:
            issues.append({"severity": "warning", "type": "slide_length",
                           "slide": idx,
                           "detail": f"{len(lines)} source lines; may overflow"})

        bullets = BULLET_LINE.findall(slide)
        if len(bullets) > 5:
            issues.append({"severity": "warning", "type": "bullet_count",
                           "slide": idx,
                           "detail": f"{len(bullets)} bullets; rewrite as prose + visual"})

        # Title-as-assertion check.
        title = slide_title(slide)
        if title and not is_assertion_title(title):
            issues.append({"severity": "info", "type": "topic_title",
                           "slide": idx,
                           "detail": f"title reads as a topic: \"{title}\". Consider rewriting as an assertion."})

    # Link check.
    if check_links_flag:
        bad_links = check_links(body)
        for url, code in bad_links:
            code_str = "timeout/unreachable" if code == -1 else f"HTTP {code}"
            issues.append({"severity": "warning", "type": "broken_link",
                           "detail": f"{code_str}: {url}"})

    # Optional: markdownlint-cli2 + cspell.
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx:
        # Ship a shared config that disables Marp-incompatible rules (MD025
        # multiple-h1, MD041 first-line-h1, etc).
        md_config = Path(__file__).resolve().parent / "markdownlint.jsonc"
        md_cmd = [npx, "--yes", "markdownlint-cli2", str(path)]
        if md_config.exists():
            md_cmd.extend(["--config", str(md_config)])
        available, stdout, stderr, rc = run_optional(md_cmd)
        if available and rc != 0:
            for line in (stdout + stderr).splitlines():
                line = line.strip()
                if line and ".md:" in line:
                    issues.append({"severity": "info", "type": "markdownlint",
                                   "detail": line})

        available, stdout, stderr, rc = run_optional(
            [npx, "--yes", "cspell", "--no-progress", "--no-summary", str(path)]
        )
        if available and rc != 0 and stdout:
            for line in stdout.splitlines():
                line = line.strip()
                if line and "Unknown word" in line:
                    issues.append({"severity": "info", "type": "spelling",
                                   "detail": line})

    return issues, slide_count


def main():
    parser = argparse.ArgumentParser(description="Lint a Marp deck.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--mode", choices=sorted(MODE_BUDGETS.keys()),
                        help="Presentation mode (enables per-mode slide budget).")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument("--no-links", action="store_true",
                        help="Skip HTTP link verification.")
    args = parser.parse_args()

    path = Path(args.input).resolve()
    if not path.exists():
        print(f"error: input not found: {path}", file=sys.stderr)
        return 2

    issues, slide_count = lint_deck(
        path, mode=args.mode, check_links_flag=not args.no_links
    )

    errors = sum(1 for i in issues if i["severity"] == "error")
    warnings = sum(1 for i in issues if i["severity"] == "warning")
    infos = sum(1 for i in issues if i["severity"] == "info")

    report = {
        "deck": str(path),
        "mode": args.mode,
        "slide_count": slide_count,
        "summary": {"errors": errors, "warnings": warnings, "info": infos},
        "issues": issues,
    }

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(f"deck: {path}")
        print(f"mode: {args.mode or '(not set)'}")
        print(f"slides: {slide_count}")
        print(f"errors: {errors}  warnings: {warnings}  info: {infos}")
        for i in issues:
            loc = f" (slide {i['slide']})" if "slide" in i else ""
            print(f"  [{i['severity']}] {i['type']}{loc}: {i['detail']}")

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
