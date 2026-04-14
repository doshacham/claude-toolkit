# Obsidian Guardrails

Rules to prevent data loss, broken links, and corrupted vaults.

---

## Never do

### 1. Do not edit workspace.json while Obsidian is running
**Why**: Obsidian writes workspace state on every pane change, tab switch, and sidebar toggle. Your edit will be overwritten within seconds.
**Instead**: If you must edit it, close Obsidian first. Usually there is no reason to touch it.

### 2. Do not rename files with OS tools
**Why**: External renames (`mv`, `git mv`, OS file manager) bypass Obsidian's link tracker. Every `[[wikilink]]` to the renamed file breaks silently.
**Instead**: Rename inside Obsidian (File Explorer right-click), via the official CLI, or via the Local REST API. These update all backlinks automatically.

### 3. Do not write unquoted internal links in YAML properties
**Why**: `director: [[George Lucas]]` parses as a YAML list `["George Lucas"]`, not a link.
**Instead**: `director: "[[George Lucas]]"` -- always quote.

### 4. Do not use SORT after LIMIT in Dataview
**Why**: DQL data commands execute sequentially. `LIMIT 5` first truncates to 5 random rows, then `SORT` orders only those 5.
**Instead**: Always write `SORT field ASC` before `LIMIT N`.

### 5. Do not use tp.frontmatter inside the same template's frontmatter
**Why**: The frontmatter block does not exist yet when the template is being generated. `tp.frontmatter.key` returns `undefined`.
**Instead**: Use `tp.hooks.on_all_templates_executed()` + `app.fileManager.processFrontMatter()` to modify frontmatter after the template finishes.

### 6. Do not mix frontmatter and inline Dataview fields for the same key
**Why**: Behavior when the same key exists in both is undocumented and inconsistent. Frontmatter takes precedence for page-level queries, but inline wins in some list-item contexts.
**Instead**: Pick one location per field and stick with it vault-wide.

### 7. Do not use deprecated property names
- `cssclass` (singular) is deprecated. Use `cssclasses` (plural).
- `tag` (singular) is deprecated. Use `tags` (plural).
- `alias` (singular) is deprecated. Use `aliases` (plural).

### 8. Do not write non-ISO dates in frontmatter
**Why**: `2026/04/12`, `April 12 2026`, `12-04-2026` are parsed as Text, not Date. Dataview comparisons and Tasks date filters silently fail.
**Instead**: Always use ISO 8601: `2026-04-12` or `2026-04-12T10:30:00`.

### 9. Do not edit plugins/*/main.js or manifest.json
**Why**: These are managed by the plugin updater. Hand edits are overwritten on next update and can break the plugin.
**Instead**: Edit settings via `.obsidian/plugins/<id>/data.json` or through Obsidian's settings UI.

### 10. Do not commit workspace.json to git
**Why**: It changes on every UI interaction, producing massive diff noise and merge conflicts with zero value.
**Instead**: Add to `.gitignore`:
```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
```

---

## Be careful with

### Adding new properties
Property types are vault-wide. Adding a property named `rating` as Text in one note sets `rating` to Text across the whole vault. If another note already uses `rating` as Number, the Properties UI will show a type conflict. Check `types.json` first.

### Templater in YAML frontmatter
The `---` fences in a template may be parsed by Obsidian before Templater runs. Workaround: replace fence lines with `<% "---" %>`, or accept the parse and let Templater fill values inside the existing fences.

### Large vaults (10k+ notes)
Obsidian stays responsive to ~10k notes. Degrades noticeably around 40k and becomes mobile-unusable by 50k. Mitigations: disable "Detect all file extensions", purge unused plugins (Tasks and heavy Dataview queries are known offenders), keep Graph View closed, split truly independent domains into separate vaults.

### iCloud sync alongside Obsidian Sync
Do NOT run Sync and iCloud on the same vault. Files can appear deleted, stuck uploads, and duplicate notes are reported frequently. Pick one sync layer.

### Obsidian Sync file size limits
Standard plan: 5 MB per file. Plus plan: 200 MB per file. Files exceeding the limit are silently skipped.

---

## Recommended .gitignore for Obsidian vaults

```
# Workspace state (changes constantly, causes merge conflicts)
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# Cache
.obsidian/cache

# Trash
.trash/

# OS files
.DS_Store
Thumbs.db
```

Optional stricter additions:
```
# Per-device plugin state (can differ between machines)
# .obsidian/plugins/*/data.json

# Appearance (differs per device)
# .obsidian/appearance.json
```
