---
description: A development process for applications that uses TDD to iterate on a new project
argument-hint: [project-name-or-path]
---

# TDD Development Skill

A test-driven development process for building applications iteratively. Follow every section in order.

## Variables

PROJECT: $ARGUMENTS

## 1. Project Initialization

If PROJECT is a new project name (directory doesn't exist):

```bash
mkdir PROJECT
cd PROJECT
uv init
git init  # if not already in a git repo
```

If PROJECT is a path to an existing project, `cd` into it.

### Add dev dependency first:

```bash
uv add pytest --dev
```

### Add a scaffold test to verify the setup:

```bash
mkdir -p tests
echo 'def test_add():
    assert 1 + 1 == 2' > tests/test_add.py
```

### Verify it passes:

```bash
uv run pytest
```

## 2. README and Spec

- **Always** create a `README.md` starting with the project name as a heading plus a short description.
- **Always** create a `spec.md` with a detailed specification that includes markdown TODO checkbox lists (`- [ ]` / `- [x]`).
- The spec is the living plan — update it throughout development.

## 3. TDD Cycle (repeat for every change)

For **every** feature, fix, or change follow this loop:

### 3a. Write the test FIRST

- Group tests sensibly in test files with related tests.
- Use and reuse `pytest` fixtures for shared setup, including temporary files (`tmp_path`).
- Use `pytest.mark.parametrize` to avoid duplicated test code.

### 3b. Watch it FAIL

```bash
uv run pytest -k name_of_test
```

Confirm the test fails for the right reason (not an import error or typo).

### 3c. Implement the change

Write the minimum code to make the test pass. No more.

### 3d. Watch it PASS

```bash
uv run pytest -k name_of_test
```

Then run the full suite to catch regressions:

```bash
uv run pytest
```

### 3e. Update spec and docs

- Check off completed TODOs in `spec.md` (`- [ ]` → `- [x]`).
- Add new TODOs discovered during implementation.
- Update `README.md` with any relevant documentation.

### 3f. Commit

Commit implementation + tests + docs as a **single commit**. Use conventional commits format:

```bash
git add <specific files>
git commit -m "feat(scope): description"
```

If a remote is configured, push after every commit:

```bash
git push
```

## 4. Cleanup Rules

- **Delete `tests/test_add.py`** once the first real test is implemented.
- **Never include `test_add.py`** in any commit.
- Delete temporary files once they've served their purpose.

## 5. Running Code

Always run code through uv:

```bash
uv run python -c "..."
uv run python -m module.name
```

## 6. Adding Dependencies

Production deps:

```bash
uv add httpx
```

Dev deps:

```bash
uv add ruff --dev
```

## 7. Conventions

- Practice TDD strictly — no implementation without a failing test first.
- Commit often, in sensible chunks.
- Each commit should be atomic: one logical change with its tests and docs.
- Keep the spec.md TODO lists accurate and current at all times.
- Run the full test suite before every commit.
