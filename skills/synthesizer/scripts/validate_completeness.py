# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Validate symbol completeness: check that public symbols are documented.

Usage:
    python validate_completeness.py --repo <path> --entity-index <file> --output <file>

Extracts public/exported symbols from source code and cross-references
against the entity index built from agent dumps.

Analog to InfoSeek's difficulty criterion: validating that the analysis
captured the important structural elements.
"""

import json
import os
import re
import sys
from pathlib import Path


EXCLUDE_DIRS = {
    "node_modules", "vendor", ".git", "__pycache__", ".tox", ".venv",
    "venv", "env", "dist", "build", "target",
}

TEST_PATTERNS = ["_test.go", "test_", "_test.py", ".test.", ".spec."]


def extract_go_symbols(repo_path: str) -> dict[str, list[str]]:
    """Extract exported Go symbols (capitalized names)."""
    symbols = {"types": [], "functions": [], "interfaces": [], "constants": []}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.endswith(".go") or any(tp in f for tp in TEST_PATTERNS):
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        line = line.strip()
                        # Exported types/structs
                        m = re.match(r'^type\s+([A-Z]\w+)\s+(?:struct|interface)\s*\{', line)
                        if m:
                            name = m.group(1)
                            if "interface" in line:
                                symbols["interfaces"].append(name)
                            else:
                                symbols["types"].append(name)
                            continue
                        # Type aliases
                        m = re.match(r'^type\s+([A-Z]\w+)\s+=?\s+', line)
                        if m:
                            symbols["types"].append(m.group(1))
                            continue
                        # Exported functions
                        m = re.match(r'^func\s+(?:\([^)]+\)\s+)?([A-Z]\w+)\s*\(', line)
                        if m:
                            symbols["functions"].append(m.group(1))
                            continue
                        # Exported constants
                        m = re.match(r'^\s*([A-Z]\w+)\s*=', line)
                        if m and not line.startswith("//"):
                            symbols["constants"].append(m.group(1))
            except OSError:
                continue

    return {k: sorted(set(v)) for k, v in symbols.items()}


def extract_python_symbols(repo_path: str) -> dict[str, list[str]]:
    """Extract public Python symbols (non-underscore names)."""
    symbols = {"types": [], "functions": [], "constants": []}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.endswith(".py") or any(tp in f for tp in TEST_PATTERNS):
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        line = line.strip()
                        m = re.match(r'^class\s+([A-Z]\w+)', line)
                        if m:
                            symbols["types"].append(m.group(1))
                            continue
                        m = re.match(r'^def\s+([a-zA-Z]\w+)\s*\(', line)
                        if m and not m.group(1).startswith("_"):
                            symbols["functions"].append(m.group(1))
                            continue
                        m = re.match(r'^([A-Z][A-Z_0-9]+)\s*=', line)
                        if m:
                            symbols["constants"].append(m.group(1))
            except OSError:
                continue

    return {k: sorted(set(v)) for k, v in symbols.items()}


def extract_ts_symbols(repo_path: str) -> dict[str, list[str]]:
    """Extract exported TypeScript/JavaScript symbols."""
    symbols = {"types": [], "functions": [], "interfaces": [], "constants": []}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not any(f.endswith(ext) for ext in [".ts", ".tsx", ".js", ".jsx"]):
                continue
            if any(tp in f for tp in TEST_PATTERNS) or f.endswith(".d.ts"):
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line.startswith("export"):
                            continue
                        m = re.match(r'export\s+(?:default\s+)?(?:class|type)\s+(\w+)', line)
                        if m:
                            symbols["types"].append(m.group(1))
                            continue
                        m = re.match(r'export\s+(?:default\s+)?interface\s+(\w+)', line)
                        if m:
                            symbols["interfaces"].append(m.group(1))
                            continue
                        m = re.match(r'export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)', line)
                        if m:
                            symbols["functions"].append(m.group(1))
                            continue
                        m = re.match(r'export\s+(?:const|let|var)\s+(\w+)', line)
                        if m:
                            symbols["constants"].append(m.group(1))
            except OSError:
                continue

    return {k: sorted(set(v)) for k, v in symbols.items()}


EXTRACTORS = {
    "go": extract_go_symbols,
    "python": extract_python_symbols,
    "typescript": extract_ts_symbols,
    "javascript": extract_ts_symbols,
}


def detect_language(repo_path: str) -> str:
    """Quick language detection from manifest files."""
    p = Path(repo_path)
    if (p / "go.mod").exists():
        return "go"
    if (p / "pyproject.toml").exists() or (p / "setup.py").exists():
        return "python"
    if (p / "tsconfig.json").exists():
        return "typescript"
    if (p / "package.json").exists():
        return "javascript"
    return "unknown"


def check_completeness(repo_symbols: dict, entity_index: dict) -> dict:
    """Cross-reference repo symbols against documented entities."""
    documented = set()
    for category in ["types", "functions", "interfaces", "constants"]:
        documented.update(entity_index.get(category, []))

    results = {}
    total_symbols = 0
    total_documented = 0

    for category, symbols in repo_symbols.items():
        found = [s for s in symbols if s in documented]
        missing = [s for s in symbols if s not in documented]
        results[category] = {
            "total": len(symbols),
            "documented": len(found),
            "missing": len(missing),
            "missing_list": missing[:50],  # Cap at 50 to keep output manageable
        }
        total_symbols += len(symbols)
        total_documented += len(found)

    pct = (total_documented / total_symbols * 100) if total_symbols else 0

    return {
        "total_symbols": total_symbols,
        "documented_symbols": total_documented,
        "completeness_pct": round(pct, 1),
        "pass": pct >= 60.0,
        "threshold": 60.0,
        "by_category": results,
    }


def main():
    args = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv) - 1, 2)
            if sys.argv[i].startswith("--")}

    repo_path = args.get("--repo", "")
    entity_file = args.get("--entity-index", "")
    output_file = args.get("--output", "")

    if not repo_path or not entity_file:
        print("Usage: python validate_completeness.py --repo <path> "
              "--entity-index <file> [--output <file>]", file=sys.stderr)
        sys.exit(1)

    language = detect_language(repo_path)
    extractor = EXTRACTORS.get(language)
    if not extractor:
        print(f"Warning: no symbol extractor for {language}, skipping", file=sys.stderr)
        result = {"skip": True, "reason": f"no extractor for {language}"}
    else:
        repo_symbols = extractor(repo_path)
        with open(entity_file, "r") as f:
            entity_index = json.load(f)
        result = check_completeness(repo_symbols, entity_index)
        result["language"] = language

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        if not result.get("skip"):
            status = "PASS" if result["pass"] else "FAIL"
            print(f"[{status}] Completeness: {result['completeness_pct']}% "
                  f"({result['documented_symbols']}/{result['total_symbols']} symbols)",
                  file=sys.stderr)
    else:
        json.dump(result, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
