#!/usr/bin/env -S uv run --script
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import os
import sys
import subprocess

# Fix Windows encoding for Unicode characters
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

BLUE = "\033[94m"
RESET = "\033[0m"
WHITE = "\033[97m"
DARK_BLUE = "\033[34m"


def create_progress_bar(percentage, width=15):
    """Create a visual progress bar."""
    filled = int((percentage / 100) * width)
    empty = width - filled
    bar = f"{WHITE}{'#' * filled}{DARK_BLUE}{'-' * empty}{RESET}"
    return f"[{bar}]"


def format_tokens(tokens):
    """Format token count in human-readable format."""
    if tokens is None:
        return "0"
    if tokens < 1000:
        return str(int(tokens))
    elif tokens < 1000000:
        return f"{tokens / 1000:.1f}k"
    else:
        return f"{tokens / 1000000:.2f}M"


def get_git_branch():
    """Get current git branch if in a git repository."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_git_status():
    """Get git status indicators."""
    try:
        # Check if there are uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                lines = changes.split('\n')
                return f"±{len(lines)}"
    except Exception:
        pass
    return ""


def generate_status_line(input_data):
    """Generate the status line based on input data."""
    parts = []

    # Model display name
    model_info = input_data.get('model', {})
    model_name = model_info.get('display_name', 'Claude')
    parts.append(f"{BLUE}[{model_name}]{RESET}")

    # Context window usage
    context_data = input_data.get('context_window', {})
    used_percentage = context_data.get('used_percentage', 0) or 0
    context_window_size = context_data.get('context_window_size', 200000) or 200000
    remaining_tokens = int(context_window_size * ((100 - used_percentage) / 100))
    progress_bar = create_progress_bar(used_percentage)
    tokens_left_str = format_tokens(remaining_tokens)
    parts.append(f"{BLUE}#{RESET} {progress_bar} {BLUE}{used_percentage:.1f}% ~{tokens_left_str} left{RESET}")

    # Current directory
    workspace = input_data.get('workspace', {})
    current_dir = workspace.get('current_dir', '')
    if current_dir:
        dir_name = os.path.basename(current_dir)
        parts.append(f"{BLUE}\U0001f4c1 {dir_name}{RESET}")

    # Git branch and status
    git_branch = get_git_branch()
    if git_branch:
        git_status = get_git_status()
        git_info = f"\U0001f33f {git_branch}"
        if git_status:
            git_info += f" {git_status}"
        parts.append(f"{BLUE}{git_info}{RESET}")

    # Version info (optional, smaller)
    version = input_data.get('version', '')
    if version:
        parts.append(f"{BLUE}v{version}{RESET}")

    return " | ".join(parts)


def main():
    try:
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Generate status line
        status_line = generate_status_line(input_data)

        # Output the status line (first line of stdout becomes the status line)
        print(status_line)

        # Success
        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully - output basic status
        print(f"{BLUE}[Claude] Unknown{RESET}")
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully - output basic status
        print(f"{BLUE}[Claude] Error{RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
