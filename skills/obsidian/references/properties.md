# Obsidian Properties (YAML Frontmatter) Reference

## Table of contents

1. What properties are
2. Supported types
3. Reserved property names
4. Property search syntax
5. Working example
6. Gotchas

---

## 1. What properties are

YAML at the top of a note between `---` delimiters. Managed by Obsidian's Properties UI since v1.4. JSON frontmatter is also accepted but gets normalized to YAML on save.

```yaml
---
title: My Note
tags:
  - project
  - active
status: draft
created: 2026-04-12
---
```

Property **type is global per name** across the vault. Assigning `status` as Text once makes every `status` everywhere Text. Managed via Settings > Properties or types.json.

---

## 2. Supported types

| Type | YAML format | Notes |
|---|---|---|
| Text | `title: A New Hope` | No Markdown rendering, no hashtag parsing |
| List | Block `- item` per line | Also accepts inline `[a, b, c]` but UI writes block style |
| Number | `year: 1977` | Literal only, no expressions |
| Checkbox | `favorite: true` / `false` | Empty = indeterminate (treated as false) |
| Date | `date: 2026-04-12` | ISO `YYYY-MM-DD` stored; picker follows OS locale |
| Date & time | `time: 2026-04-12T10:30:00` | ISO 8601 without timezone |
| Tags | Reserved to the `tags` property | Cannot assign Tags type to other names |
| Aliases | Default list property | Reserved to `aliases` |

---

## 3. Reserved property names

| Name | Type | Purpose |
|---|---|---|
| `tags` | Tags | Note tags (shown in tag pane, graph, search) |
| `aliases` | List | Alternative names for link resolution |
| `cssclasses` | List | CSS classes on the note's view (replaces deprecated `cssclass`) |
| `publish` | Checkbox | Whether to include in Obsidian Publish |
| `permalink` | Text | Custom URL for Publish |
| `description` | Text | SEO description for Publish |
| `image` / `cover` | Text | Cover image for Publish |

**Deprecated**: `tag` (singular), `alias` (singular), `cssclass` (singular).

---

## 4. Property search syntax

From the Search core plugin:

| Query | Matches |
|---|---|
| `[property]` | Notes that have the property (any value) |
| `[property:value]` | Notes where property equals value |
| `[property:null]` | Property exists but is empty |
| `[status:"in progress"]` | Values with spaces must be quoted |
| `[rating:(5 OR 4)]` | Boolean in property values |
| `[author:/^J/]` | Regex in property values |

Numeric comparisons (`>`, `<`) are NOT supported in native search. Use Dataview or Bases for that.

---

## 5. Working example

```yaml
---
title: A New Hope
aliases:
  - Star Wars IV
  - "Episode IV: A New Hope"
tags:
  - film
  - scifi
cssclasses:
  - wide-page
year: 1977
rating: 9.5
favorite: true
watched: false
release_date: 1977-05-25
last_viewed: 2026-04-10T21:30:00
director: "[[George Lucas]]"
cast:
  - Mark Hamill
  - Harrison Ford
  - Carrie Fisher
related:
  - "[[The Empire Strikes Back]]"
  - "[[Return of the Jedi]]"
status: "#draft"
---
```

Note: `status: "#draft"` is quoted because the value starts with `#`.

---

## 6. Gotchas

- **Internal links must be quoted**: `director: "[[George Lucas]]"` -- unquoted `[[...]]` parses as a YAML list.
- **Strings starting with `#`, `:`, `-`, `?`, `{`, `[`, `!`, `|`, `>`, `'`, `"`** must be quoted per YAML spec.
- **Nested properties** are not supported in the Properties UI -- use Source mode to view.
- **No Markdown** in property values (intentional).
- **Each property name must be unique per note** -- duplicate `tags:` keys silently drop one.
- **Empty values**: `tags: ""` or `tags: []` do not match `[property:null]` in search.
- **List syntax**: both block (`- item`) and inline flow (`[a, b, c]`) parse, but the UI always writes block style.
- **Date format must be ISO**: `2026-04-12` parses as a date. `2026/04/12` or `April 12 2026` are parsed as Text.
