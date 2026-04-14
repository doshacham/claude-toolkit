# Obsidian Search Query Syntax Reference

## Operators

### Boolean

- **AND** is implicit: `foo bar` = both `foo` AND `bar`
- **OR**: `foo OR bar`
- **NOT**: `-bar` (prefix minus)
- **Grouping**: `(a OR b) (c OR d)`

### Phrase and regex

- **Exact phrase**: `"exact phrase"`
- **Regex**: `/[a-z]{3}/` (JS regex syntax, flags after closing slash: `/foo/i`)

### Scoped operators

All accept nested subqueries in parentheses, e.g. `file:("to be" OR -"2B")`.

| Operator | Purpose | Example |
|---|---|---|
| `file:` | Match filename | `file:".jpg"` |
| `path:` | Match full path | `path:"Daily Notes/2026"` |
| `content:` | Body only (excludes titles/properties) | `content:(query)` |
| `tag:` | Match tag (faster than plaintext `#tag`) | `tag:#work` |
| `line:` | Both terms on same line | `line:(foo bar)` |
| `block:` | Both terms in same block (expensive) | `block:(foo bar)` |
| `section:` | Both terms between same headings | `section:(foo bar)` |
| `task:` | Any task (todo + done) | `task:(account)` |
| `task-todo:` | Unchecked tasks only | `task-todo:(account)` |
| `task-done:` | Completed tasks only | `task-done:(report)` |
| `match-case:` | Force case-sensitive | `match-case:(API)` |
| `ignore-case:` | Force case-insensitive | `ignore-case:(api)` |

### Property search (v1.4.4+)

| Query | Matches |
|---|---|
| `[property]` | Notes with that property |
| `[property:value]` | Property equals value |
| `[property:null]` | Property exists but empty |
| `[status:"in progress"]` | Quoted values with spaces |

Numeric comparisons (`>`, `<`) are not supported. Use Dataview for that.

## Real-world examples

```
tag:#work task-todo:(account -tax)
path:"Daily Notes/" tag:#meeting
[status:draft] -tag:#archived
file:"2026-" line:(#standup "Billy Bob")
section:(## Action Items) task-todo:""
[project] -[status:done]
content:/TODO:\s*\w+/
match-case:(API) -file:".md.bak"
```

## Notes

- Default is case-insensitive (per Settings > Search). Override per-subquery with `match-case:`/`ignore-case:`.
- Unquoted `[...]` is property search. To search literal brackets, quote: `"[[Billy Bob]]"`.
- `task-todo:` requires a term -- bare `task-todo:` returns nothing. Use `task:""` for all tasks.
- `block:` is expensive on large vaults.
- `tag:` respects tag hierarchy: `tag:#project` matches `#project/work`.
