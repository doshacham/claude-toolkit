# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""PostToolUse hook wrapper: lint Marp decks after Write/Edit.

Reads the PostToolUse JSON payload from stdin, extracts the file path, and
runs lint.py if the file is a Marp deck. Always exits 0 — hook failures must
not block the agent.

Intended to be wired into the marp-presentation skill via:

    hooks:
      PostToolUse:
        - matcher: "Write|Edit"
          hooks:
            - type: command
              command: "python ${CLAUDE_SKILL_DIR}/scripts/_hook_lint.py"
              timeout: 30
"""

import json
import subprocess
import sys
from pathlib import Path


def _read_payload() -> dict:
    """Parse stdin as JSON. Return {} on any failure."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return {}


def _extract_path(payload: dict) -> str | None:
    """Walk the common payload shapes to find a file_path."""
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    for key in ("file_path", "path", "target"):
        if key in tool_input and isinstance(tool_input[key], str):
            return tool_input[key]
    return None


def _is_marp(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except OSError:
        return False
    return "marp: true" in head


def main() -> int:
    payload = _read_payload()
    raw_path = _extract_path(payload)
    if not raw_path:
        return 0

    path = Path(raw_path)
    if path.suffix.lower() != ".md":
        return 0
    if not path.exists():
        return 0
    if not _is_marp(path):
        return 0

    lint_script = Path(__file__).resolve().parent / "lint.py"
    try:
        result = subprocess.run(
            [sys.executable, str(lint_script), "--input", str(path),
             "--format", "text", "--no-links"],
            capture_output=True, text=True, timeout=20,
        )
        if result.returncode != 0 or result.stdout.strip():
            print("marp-presentation lint:")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
