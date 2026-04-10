# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Detect project language, manifest, entry points, and source directories.

Usage:
    python detect_project.py <repo_path>

Outputs JSON to stdout with detected project metadata.
Supports: Go, Python, TypeScript/JavaScript, Rust, Java, C#, Ruby, PHP.
"""

import json
import os
import sys
from pathlib import Path


MANIFESTS = {
    "go.mod": "go",
    "pyproject.toml": "python",
    "setup.py": "python",
    "setup.cfg": "python",
    "requirements.txt": "python",
    "package.json": "javascript",
    "tsconfig.json": "typescript",
    "Cargo.toml": "rust",
    "pom.xml": "java",
    "build.gradle": "java",
    "build.gradle.kts": "kotlin",
    "*.csproj": "csharp",
    "*.sln": "csharp",
    "Gemfile": "ruby",
    "composer.json": "php",
    "Makefile": "makefile",
    "CMakeLists.txt": "cpp",
}

SOURCE_EXTENSIONS = {
    "go": [".go"],
    "python": [".py"],
    "javascript": [".js", ".jsx", ".mjs", ".cjs"],
    "typescript": [".ts", ".tsx", ".mts", ".cts"],
    "rust": [".rs"],
    "java": [".java"],
    "kotlin": [".kt", ".kts"],
    "csharp": [".cs"],
    "ruby": [".rb"],
    "php": [".php"],
    "cpp": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
}

ENTRY_POINT_PATTERNS = {
    "go": ["cmd/*/main.go", "main.go", "cmd/main.go"],
    "python": ["__main__.py", "main.py", "app.py", "cli.py", "src/*/cli.py", "src/*/__main__.py"],
    "javascript": ["index.js", "src/index.js", "src/main.js", "bin/*.js"],
    "typescript": ["index.ts", "src/index.ts", "src/main.ts", "bin/*.ts"],
    "rust": ["src/main.rs", "src/lib.rs"],
    "java": ["src/main/java/**/Main.java", "src/main/java/**/Application.java"],
    "csharp": ["Program.cs", "**/Program.cs"],
    "ruby": ["bin/*", "lib/*.rb"],
    "php": ["index.php", "public/index.php", "artisan"],
}

EXCLUDE_DIRS = {
    "node_modules", "vendor", ".git", "__pycache__", ".tox", ".venv",
    "venv", "env", "dist", "build", "target", ".idea", ".vscode",
    "coverage", ".next", ".nuxt", "out", "bin", "obj",
}

TEST_PATTERNS = [
    "_test.go", "test_", "_test.py", ".test.", ".spec.",
    "tests/", "test/", "__tests__/", "spec/",
]


def detect_language(repo_path: Path) -> tuple[str, str | None]:
    """Detect primary language and manifest file."""
    for manifest, lang in MANIFESTS.items():
        if "*" in manifest:
            import glob
            matches = glob.glob(str(repo_path / manifest))
            if matches:
                return lang, os.path.basename(matches[0])
        elif (repo_path / manifest).exists():
            return lang, manifest

    # Fallback: count files by extension
    counts: dict[str, int] = {}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            ext = Path(f).suffix.lower()
            for lang, exts in SOURCE_EXTENSIONS.items():
                if ext in exts:
                    counts[lang] = counts.get(lang, 0) + 1

    if counts:
        primary = max(counts, key=counts.get)
        return primary, None

    return "unknown", None


def find_entry_points(repo_path: Path, language: str) -> list[str]:
    """Find entry point files for the detected language."""
    import glob as globmod

    entries = []
    patterns = ENTRY_POINT_PATTERNS.get(language, [])
    for pattern in patterns:
        matches = globmod.glob(str(repo_path / pattern), recursive=True)
        for m in matches:
            rel = os.path.relpath(m, repo_path)
            entries.append(rel.replace("\\", "/"))

    return entries


def find_source_dirs(repo_path: Path, language: str) -> list[str]:
    """Find directories containing source files."""
    exts = SOURCE_EXTENSIONS.get(language, [])
    if not exts:
        return []

    src_dirs = set()
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if any(f.endswith(ext) for ext in exts):
                rel = os.path.relpath(root, repo_path)
                if rel == ".":
                    rel = "."
                src_dirs.add(rel.replace("\\", "/"))

    return sorted(src_dirs)


def count_source_files(repo_path: Path, language: str) -> dict:
    """Count source files, test files, and total lines."""
    exts = SOURCE_EXTENSIONS.get(language, [])
    source_count = 0
    test_count = 0
    total_lines = 0
    source_files = []
    test_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not any(f.endswith(ext) for ext in exts):
                continue

            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, repo_path).replace("\\", "/")
            is_test = any(tp in rel for tp in TEST_PATTERNS)

            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    lines = sum(1 for _ in fh)
            except (OSError, UnicodeDecodeError):
                lines = 0

            if is_test:
                test_count += 1
                test_files.append(rel)
            else:
                source_count += 1
                source_files.append(rel)
                total_lines += lines

    return {
        "source_files": source_count,
        "test_files": test_count,
        "total_source_lines": total_lines,
        "source_file_list": source_files,
        "test_file_list": test_files,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_project.py <repo_path>", file=sys.stderr)
        sys.exit(1)

    repo_path = Path(sys.argv[1]).resolve()
    if not repo_path.is_dir():
        print(f"Error: {repo_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    language, manifest = detect_language(repo_path)
    entry_points = find_entry_points(repo_path, language)
    source_dirs = find_source_dirs(repo_path, language)
    file_stats = count_source_files(repo_path, language)

    result = {
        "repo_path": str(repo_path),
        "language": language,
        "manifest": manifest,
        "entry_points": entry_points,
        "source_dirs": source_dirs,
        "source_files": file_stats["source_files"],
        "test_files": file_stats["test_files"],
        "total_source_lines": file_stats["total_source_lines"],
        "source_file_list": file_stats["source_file_list"],
        "test_file_list": file_stats["test_file_list"],
    }

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
