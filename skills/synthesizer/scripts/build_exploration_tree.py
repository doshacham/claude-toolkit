# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Build an exploration tree from a repository's import/dependency graph.

Usage:
    python build_exploration_tree.py <repo_path> [--output exploration_tree.json]

Follows imports from entry points to build an acyclic dependency tree.
Supports: Go, Python, TypeScript/JavaScript, Rust.

Inspired by InfoSeek's Research Tree construction (arXiv:2509.00375).
The tree represents the codebase's actual dependency structure, not its
directory layout, enabling adaptive exploration.
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


EXCLUDE_DIRS = {
    "node_modules", "vendor", ".git", "__pycache__", ".tox", ".venv",
    "venv", "env", "dist", "build", "target", ".idea", ".vscode",
    "coverage", ".next", ".nuxt", "out", "bin", "obj",
}

TEST_PATTERNS = [
    "_test.go", "test_", "_test.py", ".test.", ".spec.",
]


def is_test_file(filepath: str) -> bool:
    return any(tp in filepath for tp in TEST_PATTERNS)


def estimate_complexity(filepath: str) -> int:
    """Estimate file complexity by line count."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for line in f if line.strip() and not line.strip().startswith("//")
                       and not line.strip().startswith("#")
                       and not line.strip().startswith("*"))
    except OSError:
        return 0


# --- Go import parser ---

def parse_go_imports(filepath: str) -> list[str]:
    """Extract import paths from a Go file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return imports

    # Single import: import "path"
    for m in re.finditer(r'import\s+"([^"]+)"', content):
        imports.append(m.group(1))

    # Block import: import ( ... )
    for block in re.finditer(r'import\s*\((.*?)\)', content, re.DOTALL):
        for m in re.finditer(r'"([^"]+)"', block.group(1)):
            imports.append(m.group(1))

    return imports


def build_go_tree(repo_path: Path) -> dict:
    """Build exploration tree for a Go project."""
    # Find the module path from go.mod
    go_mod = repo_path / "go.mod"
    module_path = ""
    if go_mod.exists():
        with open(go_mod, "r") as f:
            for line in f:
                if line.startswith("module "):
                    module_path = line.split()[1].strip()
                    break

    # Collect all Go source files and their imports
    file_imports: dict[str, list[str]] = {}
    package_files: dict[str, list[str]] = defaultdict(list)

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.endswith(".go") or is_test_file(f):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, repo_path).replace("\\", "/")
            imports = parse_go_imports(fpath)
            # Filter to internal imports only
            internal = [i for i in imports if module_path and i.startswith(module_path)]
            file_imports[rel] = internal
            # Group by package directory
            pkg_dir = os.path.dirname(rel)
            package_files[pkg_dir].append(rel)

    # Build adjacency list at package level
    pkg_deps: dict[str, set[str]] = defaultdict(set)
    for rel, imports in file_imports.items():
        src_pkg = os.path.dirname(rel)
        for imp in imports:
            # Convert module import path to directory
            if module_path:
                dep_pkg = imp[len(module_path):].lstrip("/")
                if dep_pkg and dep_pkg != src_pkg:
                    pkg_deps[src_pkg].add(dep_pkg)

    return _build_tree_from_deps(repo_path, package_files, pkg_deps)


# --- Python import parser ---

def parse_python_imports(filepath: str) -> list[str]:
    """Extract import module names from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("import "):
                    parts = line[7:].split(",")
                    for part in parts:
                        mod = part.strip().split(" as ")[0].strip()
                        imports.append(mod.split(".")[0])
                elif line.startswith("from "):
                    match = re.match(r"from\s+(\S+)\s+import", line)
                    if match:
                        mod = match.group(1)
                        if not mod.startswith("."):
                            imports.append(mod.split(".")[0])
                        else:
                            imports.append(mod)
    except OSError:
        pass
    return imports


def build_python_tree(repo_path: Path) -> dict:
    """Build exploration tree for a Python project."""
    # Find top-level packages (directories with __init__.py or src/*)
    top_packages = set()
    src_dir = repo_path / "src"
    search_root = src_dir if src_dir.is_dir() else repo_path

    for item in search_root.iterdir():
        if item.is_dir() and (item / "__init__.py").exists():
            top_packages.add(item.name)

    package_files: dict[str, list[str]] = defaultdict(list)
    pkg_deps: dict[str, set[str]] = defaultdict(set)

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.endswith(".py") or is_test_file(f):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, repo_path).replace("\\", "/")
            pkg_dir = os.path.dirname(rel)
            package_files[pkg_dir].append(rel)

            imports = parse_python_imports(fpath)
            for imp in imports:
                base = imp.lstrip(".").split(".")[0]
                if base in top_packages and base != os.path.basename(pkg_dir):
                    pkg_deps[pkg_dir].add(base)

    return _build_tree_from_deps(repo_path, package_files, pkg_deps)


# --- TypeScript/JavaScript import parser ---

def parse_ts_imports(filepath: str) -> list[str]:
    """Extract import paths from a TS/JS file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return imports

    # import ... from "path"
    for m in re.finditer(r'(?:import|from)\s+["\']([^"\']+)["\']', content):
        path = m.group(1)
        if path.startswith("."):
            imports.append(path)

    # require("path")
    for m in re.finditer(r'require\s*\(\s*["\']([^"\']+)["\']\s*\)', content):
        path = m.group(1)
        if path.startswith("."):
            imports.append(path)

    return imports


def build_ts_tree(repo_path: Path) -> dict:
    """Build exploration tree for a TypeScript/JavaScript project."""
    package_files: dict[str, list[str]] = defaultdict(list)
    pkg_deps: dict[str, set[str]] = defaultdict(set)

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not any(f.endswith(ext) for ext in [".ts", ".tsx", ".js", ".jsx"]):
                continue
            if is_test_file(f) or f.endswith(".d.ts"):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, repo_path).replace("\\", "/")
            pkg_dir = os.path.dirname(rel) or "."
            package_files[pkg_dir].append(rel)

            imports = parse_ts_imports(fpath)
            for imp in imports:
                resolved = os.path.normpath(os.path.join(os.path.dirname(fpath), imp))
                dep_dir = os.path.relpath(os.path.dirname(resolved), repo_path).replace("\\", "/")
                if dep_dir != pkg_dir:
                    pkg_deps[pkg_dir].add(dep_dir)

    return _build_tree_from_deps(repo_path, package_files, pkg_deps)


# --- Rust import parser ---

def parse_rust_imports(filepath: str) -> list[str]:
    """Extract crate-internal use paths from a Rust file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("use crate::") or line.startswith("mod "):
                    imports.append(line)
    except OSError:
        pass
    return imports


def build_rust_tree(repo_path: Path) -> dict:
    """Build exploration tree for a Rust project."""
    package_files: dict[str, list[str]] = defaultdict(list)
    pkg_deps: dict[str, set[str]] = defaultdict(set)

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.endswith(".rs") or is_test_file(f):
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, repo_path).replace("\\", "/")
            pkg_dir = os.path.dirname(rel)
            package_files[pkg_dir].append(rel)

    return _build_tree_from_deps(repo_path, package_files, pkg_deps)


# --- Generic tree builder ---

def _build_tree_from_deps(
    repo_path: Path,
    package_files: dict[str, list[str]],
    pkg_deps: dict[str, set[str]],
) -> dict:
    """Build a tree structure from package files and dependencies."""
    nodes = []
    for pkg, files in sorted(package_files.items()):
        complexity = sum(estimate_complexity(str(repo_path / f)) for f in files)
        deps = sorted(pkg_deps.get(pkg, set()))
        nodes.append({
            "id": pkg or ".",
            "path": pkg or ".",
            "files": sorted(files),
            "file_count": len(files),
            "complexity": complexity,
            "depends_on": deps,
            "type": "entry_point" if _is_entry_package(pkg, files) else "package",
        })

    # Compute reverse deps (who depends on me)
    reverse_deps: dict[str, list[str]] = defaultdict(list)
    for pkg, deps in pkg_deps.items():
        for dep in deps:
            reverse_deps[dep].append(pkg)

    for node in nodes:
        node["depended_by"] = sorted(reverse_deps.get(node["id"], []))

    # Find root nodes (no one depends on them, or they are entry points)
    all_deps = set()
    for deps in pkg_deps.values():
        all_deps.update(deps)

    roots = [n["id"] for n in nodes if n["id"] not in all_deps or n["type"] == "entry_point"]
    if not roots and nodes:
        roots = [nodes[0]["id"]]

    return {
        "repo_path": str(repo_path),
        "total_packages": len(nodes),
        "total_files": sum(n["file_count"] for n in nodes),
        "total_complexity": sum(n["complexity"] for n in nodes),
        "roots": roots,
        "nodes": nodes,
    }


def _is_entry_package(pkg: str, files: list[str]) -> bool:
    """Check if a package contains entry point files."""
    entry_indicators = ["main.go", "main.py", "__main__.py", "cli.py", "index.ts",
                        "index.js", "main.rs", "Program.cs"]
    return any(os.path.basename(f) in entry_indicators for f in files)


# --- Fallback: directory-based tree ---

def build_directory_tree(repo_path: Path) -> dict:
    """Fallback: build tree from directory structure instead of imports."""
    package_files: dict[str, list[str]] = defaultdict(list)

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, repo_path).replace("\\", "/")
            if is_test_file(rel):
                continue
            ext = Path(f).suffix.lower()
            source_exts = {e for exts in SOURCE_EXTENSIONS.values() for e in exts}
            if ext in source_exts:
                pkg_dir = os.path.dirname(rel)
                package_files[pkg_dir].append(rel)

    return _build_tree_from_deps(repo_path, package_files, {})


def main():
    if len(sys.argv) < 2:
        print("Usage: python build_exploration_tree.py <repo_path> [--output FILE]", file=sys.stderr)
        sys.exit(1)

    repo_path = Path(sys.argv[1]).resolve()
    output_file = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    if not repo_path.is_dir():
        print(f"Error: {repo_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Detect language
    from detect_project import detect_language
    language, _ = detect_language(repo_path)

    # Build language-specific tree
    builders = {
        "go": build_go_tree,
        "python": build_python_tree,
        "typescript": build_ts_tree,
        "javascript": build_ts_tree,
        "rust": build_rust_tree,
    }

    builder = builders.get(language, build_directory_tree)
    tree = builder(repo_path)
    tree["language"] = language
    tree["method"] = "import_graph" if language in builders else "directory_fallback"

    if output_file:
        with open(output_file, "w") as f:
            json.dump(tree, f, indent=2)
        print(f"Exploration tree written to {output_file}", file=sys.stderr)
    else:
        json.dump(tree, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
