# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Render a Marp Markdown deck via Marp CLI.

Wraps `npx @marp-team/marp-cli@latest` so no global install is required.
All 15 bundled themes are auto-registered via --theme-set.

Supports:
- Single-format: --format pptx | pdf | html
- Bundle: --format bundle (renders pptx + pdf + html in one call)
- Handout: --format handout (PDF with speaker notes as presenter-view PDF)
- Watch:  --watch (re-render on file change)
- Server: --server (live preview at localhost:8080)

Usage:
    python render.py --input deck.md --format html
    python render.py --input deck.md --format bundle
    python render.py --input deck.md --format handout
    python render.py --input deck.md --watch --format html
    python render.py --server --input-dir ./decks/
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


SINGLE_FORMATS = {"pptx", "pdf", "html"}
ALL_FORMATS = SINGLE_FORMATS | {"bundle", "handout"}
CACHE_FILENAME = ".marp_render_cache.json"


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_path_for(input_path: Path) -> Path:
    return input_path.parent / CACHE_FILENAME


def load_cache(input_path: Path) -> dict:
    p = cache_path_for(input_path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(input_path: Path, cache: dict) -> None:
    p = cache_path_for(input_path)
    try:
        p.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    except OSError:
        pass  # non-fatal


def can_skip(input_path: Path, out_path: Path, fmt: str) -> bool:
    """Return True if the cached hash matches and the output already exists."""
    if not out_path.exists():
        return False
    cache = load_cache(input_path)
    key = f"{input_path.name}:{fmt}"
    entry = cache.get(key)
    if not entry:
        return False
    try:
        current_hash = hash_file(input_path)
    except OSError:
        return False
    return (
        entry.get("hash") == current_hash
        and entry.get("output") == str(out_path)
    )


def update_cache(input_path: Path, out_path: Path, fmt: str) -> None:
    try:
        current_hash = hash_file(input_path)
    except OSError:
        return
    cache = load_cache(input_path)
    cache[f"{input_path.name}:{fmt}"] = {
        "hash": current_hash,
        "output": str(out_path),
    }
    save_cache(input_path, cache)


def find_npx():
    """Locate npx executable; handle .cmd shim on Windows."""
    for name in ("npx", "npx.cmd"):
        path = shutil.which(name)
        if path:
            return path
    return None


def themes_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "themes"


def build_cmd(npx: str, input_path: Path, out_path: Path, fmt: str,
              allow_local_files: bool, extra: list[str] | None = None) -> list[str]:
    cmd = [
        npx, "--yes", "@marp-team/marp-cli@latest",
        str(input_path),
        f"--{fmt}",
        "--output", str(out_path),
        "--theme-set", str(themes_dir()),
    ]
    if allow_local_files:
        cmd.append("--allow-local-files")
    if extra:
        cmd.extend(extra)
    return cmd


def run(cmd: list[str]) -> int:
    print(f"running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def render_one(npx: str, input_path: Path, fmt: str, out: Path | None,
               allow_local_files: bool, extra: list[str] | None = None,
               skip_unchanged: bool = False) -> int:
    out_path = out if out else input_path.with_suffix(f".{fmt}")

    if skip_unchanged and can_skip(input_path, out_path, fmt):
        print(f"skip: {out_path} is up to date (cached hash match)")
        return 0

    cmd = build_cmd(npx, input_path, out_path, fmt, allow_local_files, extra)
    rc = run(cmd)
    if rc == 0:
        print(f"ok: wrote {out_path}")
        if skip_unchanged:
            update_cache(input_path, out_path, fmt)
    else:
        print(f"error: marp-cli exited with code {rc}", file=sys.stderr)
    return rc


def render_bundle(npx: str, input_path: Path, allow_local_files: bool,
                  skip_unchanged: bool = False) -> int:
    """Render html + pdf + pptx in sequence."""
    rc_total = 0
    for fmt in ("html", "pdf", "pptx"):
        rc = render_one(npx, input_path, fmt, None, allow_local_files,
                        skip_unchanged=skip_unchanged)
        if rc != 0:
            rc_total = rc
    return rc_total


def render_handout(npx: str, input_path: Path, allow_local_files: bool) -> int:
    """Render a presenter-notes PDF (handout style).

    Marp CLI's `--pdf-notes` flag adds speaker-notes pages alongside slides
    in the PDF output. That is the cleanest way to produce a handout.
    """
    out_path = input_path.with_name(input_path.stem + "_handout.pdf")
    cmd = build_cmd(npx, input_path, out_path, "pdf", allow_local_files,
                    extra=["--pdf-notes"])
    rc = run(cmd)
    if rc == 0:
        print(f"ok: wrote {out_path}")
    else:
        print(f"error: marp-cli exited with code {rc}", file=sys.stderr)
    return rc


def run_server(npx: str, input_dir: Path, allow_local_files: bool) -> int:
    """Run Marp's live-preview server."""
    cmd = [
        npx, "--yes", "@marp-team/marp-cli@latest",
        "--server",
        "--theme-set", str(themes_dir()),
        str(input_dir),
    ]
    if allow_local_files:
        cmd.append("--allow-local-files")
    print(f"running: {' '.join(cmd)}")
    print("server will start; open the URL it prints. Ctrl+C to stop.")
    return subprocess.run(cmd).returncode


def run_watch(npx: str, input_path: Path, fmt: str, allow_local_files: bool) -> int:
    """Watch a single file and re-render on change."""
    out_path = input_path.with_suffix(f".{fmt}")
    cmd = build_cmd(npx, input_path, out_path, fmt, allow_local_files,
                    extra=["--watch"])
    print(f"running: {' '.join(cmd)}")
    print("watch mode active. Ctrl+C to stop.")
    return subprocess.run(cmd).returncode


def main():
    parser = argparse.ArgumentParser(description="Render a Marp deck.")
    parser.add_argument("--input", help="Path to the .md deck (required for non-server modes).")
    parser.add_argument("--input-dir", help="Directory to serve (used with --server).")
    parser.add_argument("--format", choices=sorted(ALL_FORMATS),
                        help="Output format. Use `bundle` for all three, `handout` for PDF with notes.")
    parser.add_argument("--out", help="Output path (single-format only).")
    parser.add_argument("--watch", action="store_true",
                        help="Watch the input file and re-render on changes.")
    parser.add_argument("--server", action="store_true",
                        help="Run Marp's live-preview server on a directory.")
    parser.add_argument(
        "--allow-local-files", action="store_true",
        help="Pass --allow-local-files (needed for local images).",
    )
    parser.add_argument(
        "--skip-unchanged", action="store_true",
        help="Skip the render if the input hash matches the cached hash AND the output exists.",
    )
    args = parser.parse_args()

    npx = find_npx()
    if not npx:
        print("error: npx not found on PATH. Install Node.js from https://nodejs.org",
              file=sys.stderr)
        return 2

    # Server mode.
    if args.server:
        input_dir = Path(args.input_dir or ".").resolve()
        if not input_dir.exists() or not input_dir.is_dir():
            print(f"error: input dir not found: {input_dir}", file=sys.stderr)
            return 2
        return run_server(npx, input_dir, args.allow_local_files)

    # All other modes need --input.
    if not args.input:
        print("error: --input is required unless --server is used", file=sys.stderr)
        return 2

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"error: input not found: {input_path}", file=sys.stderr)
        return 2

    # Watch mode: re-render a single format on each change.
    if args.watch:
        fmt = args.format if args.format in SINGLE_FORMATS else "html"
        return run_watch(npx, input_path, fmt, args.allow_local_files)

    if not args.format:
        print("error: --format is required", file=sys.stderr)
        return 2

    if args.format == "bundle":
        return render_bundle(npx, input_path, args.allow_local_files,
                             skip_unchanged=args.skip_unchanged)
    if args.format == "handout":
        return render_handout(npx, input_path, args.allow_local_files)

    out = Path(args.out).resolve() if args.out else None
    return render_one(npx, input_path, args.format, out, args.allow_local_files,
                      skip_unchanged=args.skip_unchanged)


if __name__ == "__main__":
    raise SystemExit(main())
