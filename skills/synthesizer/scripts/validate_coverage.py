# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Validate file coverage: check which source files are mentioned in agent dumps.

Usage:
    python validate_coverage.py --repo <path> --dumps <dir> --report <file> --output <file>

Compares the list of source files in the repo against file paths mentioned
in the XML/MD agent dumps. Reports coverage percentage and uncovered files.

Analog to InfoSeek's verifiability criterion: ensuring the analysis actually
covers the source material.
"""

import json
import os
import re
import sys
from pathlib import Path


EXCLUDE_DIRS = {
    "node_modules", "vendor", ".git", "__pycache__", ".tox", ".venv",
    "venv", "env", "dist", "build", "target", ".idea", ".vscode",
    "coverage", ".next", ".nuxt", "out", "bin", "obj",
}

SOURCE_EXTENSIONS = {
    ".go", ".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".java", ".kt",
    ".cs", ".rb", ".php", ".cpp", ".cc", ".h", ".hpp", ".c", ".swift",
}

TEST_PATTERNS = ["_test.go", "test_", "_test.py", ".test.", ".spec."]


def list_source_files(repo_path: str) -> list[str]:
    """List all non-test source files in the repository."""
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in filenames:
            ext = Path(f).suffix.lower()
            if ext not in SOURCE_EXTENSIONS:
                continue
            rel = os.path.relpath(os.path.join(root, f), repo_path).replace("\\", "/")
            if any(tp in rel for tp in TEST_PATTERNS):
                continue
            files.append(rel)
    return sorted(files)


def extract_file_mentions(dumps_dir: str) -> set[str]:
    """Extract file paths mentioned in XML and MD dumps."""
    mentions = set()
    path_patterns = [
        # XML: file="path" or path="path" or name="path"
        re.compile(r'(?:file|path|name)\s*=\s*"([^"]*\.[a-z]{1,5})"'),
        # MD: backtick paths like `cmd/bd/main.go`
        re.compile(r'`([a-zA-Z0-9_/\-\.]+\.[a-z]{1,5})`'),
        # MD: paths in headers like ## cmd/bd/main.go or ### file: main.go
        re.compile(r'#+\s+(?:file:\s*)?([a-zA-Z0-9_/\-\.]+\.[a-z]{1,5})'),
        # Prose mentions: words ending in source extensions
        re.compile(r'(?:^|\s)([a-zA-Z0-9_/\-\.]+\.(?:go|py|ts|rs|java|cs|rb))\b'),
    ]

    for fname in os.listdir(dumps_dir):
        if not (fname.endswith(".xml") or fname.endswith(".md")):
            continue
        fpath = os.path.join(dumps_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            continue

        for pattern in path_patterns:
            for match in pattern.finditer(content):
                path = match.group(1).strip()
                # Normalize: strip leading ./ or repo prefix
                path = path.lstrip("./")
                if any(path.endswith(ext) for ext in SOURCE_EXTENSIONS):
                    mentions.add(path)

    return mentions


def check_report_mentions(report_path: str) -> set[str]:
    """Extract file paths mentioned in the final report."""
    if not os.path.exists(report_path):
        return set()
    try:
        with open(report_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return set()

    mentions = set()
    patterns = [
        re.compile(r'`([a-zA-Z0-9_/\-\.]+\.[a-z]{1,5})`'),
        re.compile(r'(?:^|\s)([a-zA-Z0-9_/\-\.]+\.(?:go|py|ts|rs|java|cs|rb))\b'),
    ]
    for pattern in patterns:
        for match in pattern.finditer(content):
            path = match.group(1).strip().lstrip("./")
            if any(path.endswith(ext) for ext in SOURCE_EXTENSIONS):
                mentions.add(path)
    return mentions


def compute_coverage(source_files: list[str], mentions: set[str]) -> dict:
    """Compute coverage by fuzzy-matching source files against mentions."""
    covered = []
    uncovered = []

    for src in source_files:
        # Check exact match
        if src in mentions:
            covered.append(src)
            continue

        # Check basename match (e.g., "main.go" matches "cmd/bd/main.go")
        basename = os.path.basename(src)
        if basename in mentions:
            covered.append(src)
            continue

        # Check suffix match (e.g., "bd/main.go" matches "cmd/bd/main.go")
        found = False
        for mention in mentions:
            if src.endswith(mention) or mention.endswith(src):
                covered.append(src)
                found = True
                break
            # Also check if the mention contains the last two path components
            parts = src.split("/")
            if len(parts) >= 2:
                suffix = "/".join(parts[-2:])
                if suffix in mention or mention.endswith(suffix):
                    covered.append(src)
                    found = True
                    break

        if not found:
            uncovered.append(src)

    pct = (len(covered) / len(source_files) * 100) if source_files else 0

    return {
        "total_source_files": len(source_files),
        "covered_files": len(covered),
        "uncovered_files": len(uncovered),
        "coverage_pct": round(pct, 1),
        "pass": pct >= 70.0,
        "threshold": 70.0,
        "covered_list": covered,
        "uncovered_list": uncovered,
    }


def main():
    args = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv) - 1, 2)
            if sys.argv[i].startswith("--")}

    repo_path = args.get("--repo", "")
    dumps_dir = args.get("--dumps", "")
    report_path = args.get("--report", "")
    output_file = args.get("--output", "")

    if not repo_path or not dumps_dir:
        print("Usage: python validate_coverage.py --repo <path> --dumps <dir> "
              "[--report <file>] [--output <file>]", file=sys.stderr)
        sys.exit(1)

    source_files = list_source_files(repo_path)
    dump_mentions = extract_file_mentions(dumps_dir)
    report_mentions = check_report_mentions(report_path) if report_path else set()
    all_mentions = dump_mentions | report_mentions

    result = compute_coverage(source_files, all_mentions)
    result["dump_mentions_count"] = len(dump_mentions)
    result["report_mentions_count"] = len(report_mentions)

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        status = "PASS" if result["pass"] else "FAIL"
        print(f"[{status}] Coverage: {result['coverage_pct']}% "
              f"({result['covered_files']}/{result['total_source_files']} files)",
              file=sys.stderr)
    else:
        json.dump(result, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
