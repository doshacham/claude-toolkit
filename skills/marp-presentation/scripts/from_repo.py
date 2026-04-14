# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Scaffold an onboarding deck from a repository directory.

Walks a repo and emits a Marp deck with slides filled in from:
- README.md (title, project description)
- package.json / pyproject.toml / Cargo.toml (tech stack)
- Top-level directories (repo map)
- .env.example (environment variables)
- CI configs (deploy story)
- docs/ or CONTRIBUTING.md (further reading)

The agent is expected to read the scaffold, verify facts, and flesh out
speaker notes. This script does NOT replace authorship — it collects raw
material and lays out the slide structure.

Usage:
    python from_repo.py --repo ./my-project --out ./onboarding.md
    python from_repo.py --repo . --out ./onboarding.md --theme paper
"""

import argparse
import json
import sys
from pathlib import Path


IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
               "dist", "build", ".next", "target", ".cache"}
MAX_README_BYTES = 12_000


def read_optional(path: Path, limit: int = 8_000) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except OSError:
        return None


def detect_tech_stack(repo: Path) -> list[str]:
    stack = []

    pkg = repo / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps = list(data.get("dependencies", {}).keys()) + \
                   list(data.get("devDependencies", {}).keys())
            if "react" in deps:
                stack.append("React")
            if "next" in deps:
                stack.append("Next.js")
            if "vue" in deps:
                stack.append("Vue")
            if "typescript" in deps:
                stack.append("TypeScript")
            if "express" in deps:
                stack.append("Express")
            if not stack:
                stack.append(f"Node.js ({len(deps)} deps)")
        except (json.JSONDecodeError, OSError):
            stack.append("Node.js")

    if (repo / "pyproject.toml").exists():
        stack.append("Python (pyproject)")
    elif (repo / "setup.py").exists() or (repo / "requirements.txt").exists():
        stack.append("Python")

    if (repo / "Cargo.toml").exists():
        stack.append("Rust")

    if (repo / "go.mod").exists():
        stack.append("Go")

    if (repo / "Gemfile").exists():
        stack.append("Ruby")

    if (repo / "pom.xml").exists() or (repo / "build.gradle").exists():
        stack.append("Java/JVM")

    if (repo / "Dockerfile").exists():
        stack.append("Docker")

    if (repo / ".github" / "workflows").exists():
        stack.append("GitHub Actions")

    return stack or ["(no recognized stack files)"]


def walk_top_level(repo: Path) -> list[tuple[str, str]]:
    """Return (name, one-line hint) for top-level entries."""
    results = []
    for entry in sorted(repo.iterdir()):
        if entry.name.startswith(".") and entry.name not in (".env.example", ".github"):
            continue
        if entry.name in IGNORE_DIRS:
            continue
        if entry.is_dir():
            try:
                count = sum(1 for _ in entry.rglob("*") if _.is_file())
                hint = f"{count} files"
            except OSError:
                hint = "(dir)"
            results.append((entry.name + "/", hint))
        elif entry.is_file():
            size = entry.stat().st_size
            hint = f"{size:,} bytes"
            results.append((entry.name, hint))
    return results[:20]  # Cap to keep slide manageable.


def extract_readme_title(readme: str) -> str:
    for line in readme.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return "Onboarding"


def extract_readme_description(readme: str) -> str:
    lines = readme.splitlines()
    description_lines = []
    past_title = False
    for line in lines:
        if line.startswith("# "):
            past_title = True
            continue
        if past_title:
            if line.startswith("#"):
                break
            if line.strip():
                description_lines.append(line.strip())
            if len(description_lines) >= 3:
                break
    return " ".join(description_lines) or "(describe what this project does)"


def build_deck(repo: Path, theme: str, author: str) -> str:
    readme = read_optional(repo / "README.md", limit=MAX_README_BYTES) or ""
    title = extract_readme_title(readme) or repo.name
    description = extract_readme_description(readme)

    stack = detect_tech_stack(repo)
    top_level = walk_top_level(repo)
    env_example = read_optional(repo / ".env.example", limit=2_000)
    contributing = read_optional(repo / "CONTRIBUTING.md", limit=1_500)

    slides: list[str] = []

    # Slide 1: title (lead)
    slides.append(
        f"<!-- _class: lead -->\n\n"
        f"# {title}\n\n"
        f"### Onboarding deck for new engineers\n\n"
        f"{author or '(author)'}"
    )

    # Slide 2: what this project does
    slides.append(
        f"## What this project does\n\n"
        f"{description}\n\n"
        f"<!-- Describe the problem this solves and who benefits. -->"
    )

    # Slide 3: tech stack
    stack_lines = "\n".join(f"- {s}" for s in stack)
    slides.append(
        f"## Tech stack at a glance\n\n"
        f"{stack_lines}\n\n"
        f"<!-- Mention versions if the user cares. -->"
    )

    # Slide 4: repo map
    map_lines = "\n".join(f"- `{name}` — {hint}" for name, hint in top_level)
    slides.append(
        f"## The repo map\n\n"
        f"{map_lines}\n\n"
        f"<!-- Replace hints with one-line purpose of each directory. -->"
    )

    # Slide 5: environment
    if env_example:
        slides.append(
            f"## Environment\n\n"
            f"```\n{env_example.strip()[:600]}\n```\n\n"
            f"<!-- From `.env.example`. Explain what each var is for. -->"
        )
    else:
        slides.append(
            f"## Environment\n\n"
            f"No `.env.example` found. If this project needs env vars, document them here.\n\n"
            f"<!-- Agent: ask the user what env vars are needed. -->"
        )

    # Slide 6: local setup (placeholder)
    slides.append(
        "## Local setup\n\n"
        "```bash\n"
        "# 1. clone\n"
        "git clone <url>\n"
        "cd <repo>\n\n"
        "# 2. install deps\n"
        "# (fill in the right command for the detected stack)\n\n"
        "# 3. run\n"
        "# (fill in the run command)\n"
        "```\n\n"
        "<!-- Agent: verify commands against README. -->"
    )

    # Slide 7: contributing / first PR
    if contributing:
        slides.append(
            f"## How we ship\n\n"
            f"From `CONTRIBUTING.md`:\n\n"
            f"{contributing.strip()[:500]}\n\n"
            f"<!-- Summarize the PR workflow in 3 bullets max. -->"
        )
    else:
        slides.append(
            "## How we ship\n\n"
            "- Branch from `main`\n"
            "- Open a PR\n"
            "- CI runs (see `.github/workflows/`)\n"
            "- Review + merge\n\n"
            "<!-- Replace with the real workflow. -->"
        )

    # Slide 8: here be dragons
    slides.append(
        "## Here be dragons\n\n"
        "Known gotchas / legacy zones:\n\n"
        "- (agent: ask the user what to warn about)\n"
        "- (common: config drift, flaky tests, slow build)\n\n"
        "<!-- Make this concrete with real examples. -->"
    )

    # Slide 9: who to ask
    slides.append(
        "## Who to ask\n\n"
        "- **Frontend**: (name)\n"
        "- **Backend**: (name)\n"
        "- **Infra**: (name)\n"
        "- **Product**: (name)\n\n"
        "<!-- Fill in from team roster. -->"
    )

    # Slide 10: first PR ideas
    slides.append(
        "## First PR ideas\n\n"
        "- Fix a typo in the README\n"
        "- Add a test for an untested function\n"
        "- Improve error messages in a failing code path\n\n"
        "<!-- Check good-first-issue labels if this is a public repo. -->"
    )

    # Slide 11: closing
    slides.append(
        "<!-- _class: lead -->\n\n"
        "# Welcome aboard\n\n"
        "Questions? Ask anyone."
    )

    body = "\n\n---\n\n".join(slides)

    frontmatter = (
        "---\n"
        "marp: true\n"
        f"theme: {theme}\n"
        "paginate: true\n"
        f"header: \"{title} — onboarding\"\n"
        "---\n\n"
    )

    return frontmatter + body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Scaffold an onboarding deck from a repo.")
    parser.add_argument("--repo", required=True, help="Repo directory to scan.")
    parser.add_argument("--out", required=True, help="Output .md path.")
    parser.add_argument("--theme", default="paper",
                        help="Marp theme name (default: paper).")
    parser.add_argument("--author", default="",
                        help="Author string for the title slide.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.exists() or not repo.is_dir():
        print(f"error: repo not a directory: {repo}", file=sys.stderr)
        return 2

    out = Path(args.out).resolve()
    if out.exists():
        print(f"error: refusing to overwrite: {out}", file=sys.stderr)
        return 2

    deck = build_deck(repo, args.theme, args.author)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(deck, encoding="utf-8")
    print(f"ok: scaffolded onboarding deck -> {out}")
    print("next: open the file, verify facts, fill in placeholders, run lint.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
