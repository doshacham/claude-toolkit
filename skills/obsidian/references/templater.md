# Templater Reference

## Table of contents

1. Syntax
2. Internal modules
3. Whitespace control
4. Settings and triggers
5. User scripts
6. Example templates
7. Gotchas

---

## 1. Syntax

| Tag | Purpose |
|---|---|
| `<% expression %>` | Evaluate and output result |
| `<%* javascript %>` | Execute JS, no auto-output (use `tR +=` to emit) |
| `<%+ expression %>` | Dynamic command (deferred to preview render). Deprecated. |

---

## 2. Internal modules

### tp.date

| Function | Example |
|---|---|
| `tp.date.now(format?, offset?, ref?, refFormat?)` | `<% tp.date.now("YYYY-MM-DD") %>` |
| `tp.date.tomorrow(format?)` | `<% tp.date.tomorrow("YYYY-MM-DD") %>` |
| `tp.date.yesterday(format?)` | `<% tp.date.yesterday() %>` |
| `tp.date.weekday(format?, weekday?, ref?, refFormat?)` | `<% tp.date.weekday("YYYY-MM-DD", 0) %>` (Monday=0) |

Format uses moment.js tokens (`YYYY`, `MM`, `DD`, `dddd`, `HH`, `mm`, `ss`, `A`). Offset accepts days as number or ISO duration (`"P1Y"`, `"P-1M"`).

### tp.file

| Property/Function | Purpose |
|---|---|
| `tp.file.title` | Current filename (no extension) |
| `tp.file.creation_date(format?)` | Creation date |
| `tp.file.last_modified_date(format?)` | Modified date |
| `tp.file.cursor(order?)` | Place cursor position (for sequential tab stops) |
| `tp.file.cursor_append(content)` | Append at cursor |
| `tp.file.exists(filepath)` | Check if file exists |
| `tp.file.find_tfile(filename)` | Get TFile object |
| `tp.file.folder(absolute?)` | Folder path |
| `tp.file.include(link_or_tfile)` | Include another template/note |
| `tp.file.move(new_path, file?)` | Move file |
| `tp.file.path(relative?)` | File path |
| `tp.file.rename(new_title)` | Rename file |
| `tp.file.selection()` | Currently selected text |
| `tp.file.tags` | Array of tags in the file |

### tp.system

| Function | Purpose |
|---|---|
| `tp.system.clipboard()` | System clipboard contents |
| `tp.system.prompt(text, default?, throw_on_cancel?, multiline?)` | User text input |
| `tp.system.suggester(display_items, items, throw?, placeholder?, limit?)` | User selection from list |

### tp.frontmatter

Access current file's YAML: `<% tp.frontmatter.status %>`, `<% tp.frontmatter["note type"] %>`.

**WARNING**: Do NOT reference `tp.frontmatter` inside the same template's frontmatter block. The frontmatter does not exist yet during template generation.

### tp.config

`tp.config.active_file`, `tp.config.run_mode`, `tp.config.target_file`, `tp.config.template_file`.

### tp.obsidian

Full Obsidian API access (`TFile`, `Notice`, `Vault`, `MetadataCache`, etc.).

### tp.user

User-defined script functions from the scripts folder. Call: `<% tp.user.my_script("arg") %>`.

### tp.web

| Function | Purpose |
|---|---|
| `tp.web.daily_quote()` | Formatted daily quote callout |
| `tp.web.random_picture(size?, query?, include_size?)` | Unsplash image |

### tp.hooks

`tp.hooks.on_all_templates_executed(callback)` -- fires after all templates finish. Use for post-processing like `processFrontMatter`.

---

## 3. Whitespace control

| Tag | Behavior |
|---|---|
| `<%-` | Trim one newline before the tag |
| `-%>` | Trim one newline after the tag |
| `<%_` | Trim all whitespace before |
| `_%>` | Trim all whitespace after |

Essential with `<%*` execution blocks to avoid leaving empty lines.

---

## 4. Settings and triggers

- **Template folder location**: Settings > Templater > Template folder
- **Trigger on new file creation**: auto-runs Templater commands in new files (integrates with Daily Notes, Calendar, Note Refactor)
- **Folder Templates**: assign a template per folder. Deepest match wins. Set `/` for catch-all.

---

## 5. User scripts

Put `.js` files in the configured scripts folder. Export a function:

```js
// greet.js
module.exports = function (name) {
  return `Hello, ${name}!`;
};
```

Call: `<% tp.user.greet("Dori") %>`.

Scripts see globals like `app` and `moment` but NOT `tp`. Pass `tp` explicitly if needed: `<% tp.user.fn(tp) %>`.

---

## 6. Example templates

### Daily note

```
---
date: <% tp.date.now("YYYY-MM-DD") %>
---
# <% tp.date.now("dddd, Do MMMM YYYY") %>

Yesterday: [[<% tp.date.yesterday("YYYY-MM-DD") %>]]
Tomorrow: [[<% tp.date.tomorrow("YYYY-MM-DD") %>]]

## Notes
<% tp.file.cursor() %>
```

### Meeting note

```
<%*
const people = ["Alice", "Bob", "Carol", "Dave"];
const attendee = await tp.system.suggester(people, people, false, "Primary attendee");
-%>
---
type: meeting
date: <% tp.date.now("YYYY-MM-DD") %>
attendee: "<% attendee %>"
---
# Meeting - <% tp.date.now("YYYY-MM-DD HH:mm") %>

## Agenda
<% tp.file.cursor(1) %>

## Action items
- [ ] <% tp.file.cursor(2) %>
```

### Zettelkasten note

```
<%*
const topic = await tp.system.prompt("Topic");
const tags = ["concept", "reference", "fleeting", "permanent"];
const tag = await tp.system.suggester(tags, tags, false, "Type");
const uid = tp.date.now("YYYYMMDDHHmmss");
await tp.file.rename(`${uid} ${topic}`);
-%>
---
id: <% uid %>
tags: [<% tag %>]
---
# <% topic %>

<% tp.file.cursor() %>
```

---

## 7. Gotchas

- **YAML frontmatter in templates**: Obsidian may parse `---` fences before Templater runs. Workaround: replace fence lines with `<% "---" %>` or accept the parse.
- **`tp.frontmatter` in the template's own frontmatter**: returns undefined. Use `tp.hooks.on_all_templates_executed()` + `processFrontMatter` to patch after execution.
- **Execution order**: top-to-bottom. Async prompts must be `await`ed.
- **Whitespace**: `<%*` blocks leave blank lines without `-%>` / `<%-` trims.
- **Dynamic commands `<%+`**: deprecated, only re-evaluate on note reload.
