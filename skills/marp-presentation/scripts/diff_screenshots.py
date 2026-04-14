# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Diff two directories of Marp QA screenshots at the file level.

Pure stdlib — no Pillow dependency. Pairs files by name, compares by SHA-256
hash, reports which slides were added, removed, changed, or unchanged. The
agent then opens the changed slides in Playwright MCP to inspect visually.

Typical layout (committed to the repo for historical comparison):

    docs/qa/
      v1/
        slide_01.png
        slide_02.png
      v2/
        slide_01.png
        slide_02.png

Usage:
    python diff_screenshots.py --before docs/qa/v1 --after docs/qa/v2
    python diff_screenshots.py --before docs/qa/v1 --after docs/qa/v2 --format json

Exit code:
    0 — no changes detected
    1 — changes detected
    2 — I/O or arg error
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def catalog(dir_path: Path) -> dict[str, dict]:
    """Return {filename: {hash, size, path}} for every .png in the directory."""
    out: dict[str, dict] = {}
    for p in sorted(dir_path.glob("*.png")):
        try:
            out[p.name] = {
                "path": str(p),
                "size": p.stat().st_size,
                "hash": sha256_of(p),
            }
        except OSError as e:
            print(f"warning: skipping {p}: {e}", file=sys.stderr)
    return out


def compare(before: dict, after: dict) -> dict:
    before_names = set(before.keys())
    after_names = set(after.keys())

    added = sorted(after_names - before_names)
    removed = sorted(before_names - after_names)

    common = sorted(after_names & before_names)
    changed: list[dict] = []
    unchanged: list[str] = []
    for name in common:
        b = before[name]
        a = after[name]
        if b["hash"] == a["hash"]:
            unchanged.append(name)
        else:
            changed.append({
                "name": name,
                "before_size": b["size"],
                "after_size": a["size"],
                "before_path": b["path"],
                "after_path": a["path"],
            })

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare two directories of QA screenshots by filename + hash."
    )
    parser.add_argument("--before", required=True, help="Directory with BEFORE PNGs.")
    parser.add_argument("--after", required=True, help="Directory with AFTER PNGs.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    before_dir = Path(args.before).resolve()
    after_dir = Path(args.after).resolve()

    if not before_dir.is_dir():
        print(f"error: --before not a directory: {before_dir}", file=sys.stderr)
        return 2
    if not after_dir.is_dir():
        print(f"error: --after not a directory: {after_dir}", file=sys.stderr)
        return 2

    before = catalog(before_dir)
    after = catalog(after_dir)
    result = compare(before, after)

    has_changes = bool(result["added"] or result["removed"] or result["changed"])

    if args.format == "json":
        payload = {
            "before": str(before_dir),
            "after": str(after_dir),
            "summary": {
                "added": len(result["added"]),
                "removed": len(result["removed"]),
                "changed": len(result["changed"]),
                "unchanged": len(result["unchanged"]),
            },
            "details": result,
        }
        print(json.dumps(payload, indent=2))
        return 1 if has_changes else 0

    # Text format.
    print(f"before: {before_dir}  ({len(before)} files)")
    print(f"after:  {after_dir}  ({len(after)} files)")
    print()
    print(f"  unchanged: {len(result['unchanged'])}")
    print(f"  changed:   {len(result['changed'])}")
    print(f"  added:     {len(result['added'])}")
    print(f"  removed:   {len(result['removed'])}")

    if result["added"]:
        print("\nadded:")
        for n in result["added"]:
            print(f"  + {n}")

    if result["removed"]:
        print("\nremoved:")
        for n in result["removed"]:
            print(f"  - {n}")

    if result["changed"]:
        print("\nchanged (open both in Playwright MCP to inspect):")
        for entry in result["changed"]:
            delta = entry["after_size"] - entry["before_size"]
            sign = "+" if delta >= 0 else ""
            print(f"  ~ {entry['name']}  ({sign}{delta} bytes)")
            print(f"      before: {entry['before_path']}")
            print(f"      after:  {entry['after_path']}")

    if not has_changes:
        print("\nno changes detected.")

    return 1 if has_changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
