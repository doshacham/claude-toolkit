# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Parse a Python source file and emit a Mermaid flowchart of function calls.

Uses ast to find function definitions and the functions they call inside the
same file. External calls (stdlib, third-party) are ignored so the diagram
focuses on internal structure.

Output is a Mermaid `flowchart` code block ready to paste into a Marp slide.

Usage:
    python code_to_mermaid.py --input src/pipeline.py
    python code_to_mermaid.py --input src/pipeline.py --direction TD --out pipeline.mmd
"""

import argparse
import ast
import sys
from pathlib import Path


def collect_functions(tree: ast.AST):
    """Return {function_name: set_of_called_function_names}."""
    funcs: dict[str, set[str]] = {}

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.current = None

        def _enter_func(self, node):
            prev = self.current
            self.current = node.name
            funcs.setdefault(node.name, set())
            self.generic_visit(node)
            self.current = prev

        def visit_FunctionDef(self, node):
            self._enter_func(node)

        def visit_AsyncFunctionDef(self, node):
            self._enter_func(node)

        def visit_Call(self, node):
            if self.current is not None:
                name = None
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name:
                    funcs[self.current].add(name)
            self.generic_visit(node)

    Visitor().visit(tree)
    return funcs


def sanitize(name: str) -> str:
    """Mermaid node IDs must be alphanum+underscore."""
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name)


def build_mermaid(funcs: dict, direction: str = "TD") -> str:
    lines = [f"flowchart {direction}"]
    defined = set(funcs.keys())

    # Nodes.
    for f in sorted(defined):
        lines.append(f"    {sanitize(f)}[\"{f}()\"]")

    # Edges — only to functions defined in this file.
    seen_edges = set()
    for caller, callees in sorted(funcs.items()):
        for callee in sorted(callees):
            if callee in defined and caller != callee:
                edge = (sanitize(caller), sanitize(callee))
                if edge not in seen_edges:
                    lines.append(f"    {edge[0]} --> {edge[1]}")
                    seen_edges.add(edge)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Python source → Mermaid flowchart.")
    parser.add_argument("--input", required=True, help="Python source file.")
    parser.add_argument("--direction", default="TD", choices=["TD", "LR", "BT", "RL"])
    parser.add_argument("--out", help="Output file (.mmd). Prints to stdout if omitted.")
    parser.add_argument("--fence", action="store_true",
                        help="Wrap output in ```mermaid fences for paste into Markdown.")
    args = parser.parse_args()

    src_path = Path(args.input).resolve()
    if not src_path.exists():
        print(f"error: input not found: {src_path}", file=sys.stderr)
        return 2

    if src_path.suffix != ".py":
        print("warning: only Python (.py) files are supported right now",
              file=sys.stderr)

    try:
        source = src_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(src_path))
    except SyntaxError as e:
        print(f"error: failed to parse {src_path}: {e}", file=sys.stderr)
        return 2

    funcs = collect_functions(tree)
    if not funcs:
        print(f"warning: no function definitions found in {src_path}",
              file=sys.stderr)
        return 1

    mermaid = build_mermaid(funcs, args.direction)
    if args.fence:
        mermaid = f"```mermaid\n{mermaid}\n```"

    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(mermaid + "\n", encoding="utf-8")
        print(f"ok: wrote {out}")
    else:
        print(mermaid)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
