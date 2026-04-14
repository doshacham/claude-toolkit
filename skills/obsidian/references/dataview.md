# Dataview Reference (DQL + DataviewJS)

## Table of contents

1. DQL query types and structure
2. Sources
3. Data commands
4. Implicit fields
5. Custom fields
6. Data types
7. DataviewJS
8. Examples
9. Gotchas

---

## 1. DQL query types and structure

Write queries in fenced `dataview` code blocks:

````
```dataview
<QUERY-TYPE> [fields]
[FROM <source>]
[<data commands>...]
```
````

| Type | Purpose | Argument |
|---|---|---|
| `LIST` | Bullet list of file links | Optional: one expression to display alongside |
| `TABLE` | Table with columns | Comma-separated expressions, `AS "Label"` for aliases |
| `TASK` | Interactive task list | (none) |
| `CALENDAR` | Calendar dot view | Required: a date field |

---

## 2. Sources (FROM clause)

| Source | Syntax |
|---|---|
| Folder | `FROM "folder"` (includes subfolders) |
| Tag | `FROM #tag` (includes subtags) |
| Incoming links | `FROM [[note]]` |
| Outgoing links | `FROM outgoing([[note]])` |
| Single file | `FROM "path/to/note.md"` |
| Combine | `FROM #project AND "Work"` |
| Negate | `FROM #project AND -"Archive"` |

`FROM` is optional. Omitting it queries the entire vault.

---

## 3. Data commands

Optional, can appear multiple times in any order. Execute sequentially.

| Command | Purpose | Example |
|---|---|---|
| `WHERE` | Filter rows | `WHERE status != "done"` |
| `SORT` | Order results | `SORT due ASC` |
| `LIMIT` | Cap result count | `LIMIT 10` |
| `GROUP BY` | Group into buckets | `GROUP BY file.folder` |
| `FLATTEN` | Expand array fields | `FLATTEN authors` |

**IMPORTANT**: `LIMIT` before `SORT` truncates first, then sorts the truncated result. Always put `SORT` before `LIMIT`.

---

## 4. Implicit fields (file.*)

| Field | Type | Description |
|---|---|---|
| `file.name` | text | Filename without extension |
| `file.folder` | text | Folder path |
| `file.path` | text | Full vault-relative path |
| `file.ext` | text | File extension |
| `file.link` | link | Clickable link to the file |
| `file.size` | number | Size in bytes |
| `file.ctime` / `file.cday` | date | Created time / day |
| `file.mtime` / `file.mday` | date | Modified time / day |
| `file.tags` | list | All tags (with subtag breakdown) |
| `file.etags` | list | Explicit tags only |
| `file.inlinks` | list | Incoming links |
| `file.outlinks` | list | Outgoing links |
| `file.aliases` | list | Aliases from frontmatter |
| `file.tasks` | list | All tasks in the file |
| `file.lists` | list | All list items |
| `file.frontmatter` | object | Raw frontmatter |
| `file.day` | date | Date parsed from filename (if present) |

---

## 5. Custom fields

**Frontmatter** (single colon, page-level):
```yaml
---
status: in-progress
rating: 8
due: 2026-04-20
---
```

**Inline fields** (double colon, can sit on list items):
```
Basic Field:: value
I rate this a [rating:: 9].
- [ ] Ship it [due:: 2026-04-15]
```

Both are queryable identically. When the same key exists in both, **frontmatter takes precedence**.

---

## 6. Data types

| Type | Format | Notes |
|---|---|---|
| Text | `"string"` | Default for unrecognized values |
| Number | `42`, `3.14` | Supports arithmetic |
| Boolean | `true`/`false` | |
| Date | `2026-04-12` | ISO 8601. Exposes `.year`, `.month`, `.day`, `.hour` |
| Duration | `dur(3 days)`, `dur(2 hours)` | Arithmetic with dates works |
| Link | `[[Page]]` | |
| List/Array | `[a, b, c]` | YAML or inline |
| Object | nested keys | Dot access: `obj.key` |

---

## 7. DataviewJS

Fenced `dataviewjs` code block. The `dv` object is the API:

````
```dataviewjs
const pages = dv.pages('#project').where(p => p.status === "active")
dv.table(["Name", "Due"], pages.map(p => [p.file.link, p.due]))
```
````

**Core methods**:
- `dv.pages(source)` -- page collection (filterable with `.where()`, `.sort()`, `.limit()`)
- `dv.table(headers, rows)` -- render a table
- `dv.list(items)` -- render a list
- `dv.taskList(tasks, groupByFile)` -- render tasks
- `dv.current()` -- current file's page object
- `dv.header(level, text)` -- render a heading
- `dv.paragraph(text)` -- render a paragraph

**External plugin access**: `app.plugins.plugins.dataview.api`

---

## 8. Examples

**Projects dashboard**:
````
```dataview
TABLE status, due AS "Due", file.mtime AS "Updated"
FROM #project
WHERE status != "done"
SORT due ASC
```
````

**Open tasks grouped by file**:
````
```dataview
TASK
FROM "Work"
WHERE !completed
GROUP BY file.link
```
````

**Recently modified notes (last 7 days)**:
````
```dataview
LIST file.mtime
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```
````

**Calendar of due dates**:
````
```dataview
CALENDAR due
FROM #task
WHERE typeof(due) = "date"
```
````

**DataviewJS activity list**:
````
```dataviewjs
const recent = dv.pages()
  .where(p => p.file.mday >= dv.date("today").minus({days: 30}))
  .sort(p => p.file.mtime, "desc")
  .limit(10)
dv.list(recent.file.link)
```
````

---

## 9. Gotchas

- **Keys with spaces/caps are sanitized for inline fields**: `Due Date` becomes `due-date`. Frontmatter keys are NOT sanitized the same way. Use `row["Due Date"]` for unsanitized access.
- **Dates must be ISO 8601**: `2026-04-12` parses as `date`. `2026/04/12` or `April 12 2026` parse as `text` and comparisons silently fail.
- **Double vs single colon**: inline fields need `::`, frontmatter needs `:`. Swapping silently breaks indexing.
- **`LIMIT` before `SORT`** truncates first, sorts second. Always `SORT` first.
- **Subtags are included**: `FROM #project` matches `#project/work`. Use `file.etags` for exact match.
- **Inline vs frontmatter precedence for same key**: frontmatter wins for page-level queries. Do not duplicate keys across both.
