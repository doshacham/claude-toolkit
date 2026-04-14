# .obsidian/ Configuration Files Reference

All files are UTF-8 JSON. Missing files = Obsidian uses defaults. Safe to hand-edit when Obsidian is closed.

## Safety classification

- **Safe to edit**: `app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json`, `hotkeys.json`, `graph.json`, `daily-notes.json`, `templates.json`, `zk-prefixer.json`, `types.json`, `bookmarks.json`, small core-plugin JSONs, `plugins/*/data.json`, `snippets/*.css`
- **Edit with care**: `workspace.json` / `workspace-mobile.json` (machine-written, vault-specific)
- **Never touch**: `plugins/*/main.js`, `plugins/*/manifest.json` (update via plugin manager), `themes/*/theme.css` (update via theme manager)

---

## Top-level JSON files

### app.json
App-level settings (Files & Links, Editor behavior). Sparse: keys exist only when changed from default.
```json
{ "attachmentFolderPath": "Attachments", "newLinkFormat": "relative",
  "useMarkdownLinks": true, "alwaysUpdateLinks": true, "tabSize": 2,
  "livePreview": true, "vimMode": false, "trashOption": "local" }
```

### appearance.json
Theme, fonts, CSS snippets.
```json
{ "theme": "obsidian", "cssTheme": "Minimal", "baseFontSize": 16,
  "interfaceFontFamily": "Inter", "enabledCssSnippets": ["tweaks"] }
```

### core-plugins.json
Enabled core plugins. Modern: object of `id: boolean`. Legacy: string array.
```json
{ "file-explorer": true, "graph": true, "daily-notes": true,
  "templates": true, "canvas": true, "bookmarks": true }
```

### community-plugins.json
Array of enabled community plugin IDs (must match folder under `plugins/`).
```json
["obsidian-git", "dataview", "templater-obsidian", "obsidian-tasks-plugin"]
```

### hotkeys.json
Only user-customized bindings. Keys are command IDs, values are arrays of `{modifiers, key}`.
```json
{ "app:go-back": [{ "modifiers": ["Mod"], "key": "[" }],
  "daily-notes": [{ "modifiers": ["Mod", "Alt"], "key": "T" }] }
```
**Modifiers**: `"Mod"` (Cmd on macOS, Ctrl on Win/Linux), `"Ctrl"`, `"Shift"`, `"Alt"`, `"Meta"`. **Keys**: uppercase letters, `"ArrowUp"`, `"Enter"`, etc. Empty array `[]` unbinds a default.

### workspace.json / workspace-mobile.json
Full pane layout, open files, sidebar widths. Machine-written. Do NOT edit manually. Usually gitignored.

### graph.json
Global graph view settings.
```json
{ "showTags": false, "showOrphans": true, "centerStrength": 0.5,
  "repelStrength": 10, "linkDistance": 250 }
```

### bookmarks.json
Tree of bookmarked files, folders, searches, headings.
```json
{ "items": [{ "type": "file", "path": "Daily/2026-04-12.md", "title": "Today" }] }
```

### daily-notes.json
Core Daily Notes plugin config.
```json
{ "folder": "Daily", "format": "YYYY-MM-DD",
  "template": "Templates/Daily", "autorun": false }
```

### templates.json
Core Templates plugin: folder and default formats.
```json
{ "folder": "Templates", "dateFormat": "YYYY-MM-DD", "timeFormat": "HH:mm" }
```

### types.json
Manual property type assignments. Valid types: `text`, `multitext`, `number`, `checkbox`, `date`, `datetime`, `tags`, `aliases`.
```json
{ "types": { "rating": "number", "created": "date",
  "tags": "tags", "categories": "multitext" } }
```

### Other core-plugin configs
One file each, written when toggled: `backlink.json`, `page-preview.json`, `switcher.json`, `global-search.json`, `outgoing-link.json`, `note-composer.json`, `file-recovery.json`, `outline.json`, `sync.json`, `publish.json`.

---

## Subfolders

### plugins/\<plugin-id\>/
- `manifest.json` -- `{id, name, version, minAppVersion, description, author}`
- `main.js` -- compiled plugin code (never edit)
- `styles.css` -- plugin CSS (optional)
- `data.json` -- per-vault plugin settings (safe to edit when Obsidian is closed)

### themes/\<theme-name\>/
- `manifest.json` -- `{name, version, minAppVersion, author}`
- `theme.css` -- the theme stylesheet

### snippets/
User CSS snippets. Any `*.css` file here appears in Settings > Appearance > CSS snippets. Active snippets listed in `appearance.json > enabledCssSnippets`.

---

## Vault config folder name

Default is `.obsidian`. Can be renamed via Settings > Files & Links > "Override config folder". In practice, `.obsidian` is nearly universal -- only probe for a custom name if the user reports one.
