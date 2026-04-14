# Obsidian Plugin Map

## Detecting installed plugins

- **Core plugins**: read `.obsidian/core-plugins.json` (object of `id: true/false`, or legacy string array)
- **Community plugins**: read `.obsidian/community-plugins.json` (array of enabled plugin IDs)
- **Plugin settings**: `.obsidian/plugins/<plugin-id>/data.json`

---

## Core plugins

| Plugin ID | Name | Purpose |
|---|---|---|
| `file-explorer` | File explorer | Browse vault files/folders |
| `graph` | Graph view | Visualize note relationships |
| `daily-notes` | Daily notes | Open/create today's note |
| `templates` | Templates | Insert template snippets ({{title}}, {{date}}, {{time}}) |
| `canvas` | Canvas | Infinite whiteboard (.canvas JSON Canvas files) |
| `search` | Search | Full-text vault search |
| `bookmarks` | Bookmarks | Bookmark files, headings, searches |
| `properties` | Properties view | Browse/manage all vault properties |
| `bases` | Bases | Database views over frontmatter (v1.9+) |
| `backlink` | Backlinks | Show incoming links to active note |
| `outgoing-link` | Outgoing links | Show links from active note |
| `outline` | Outline | Table of contents for active note |
| `page-preview` | Page preview | Hover-preview linked notes |
| `switcher` | Quick switcher | Search and open notes by title |
| `command-palette` | Command palette | Keyboard command launcher |
| `slash-command` | Slash commands | `/` inline command picker |
| `note-composer` | Note composer | Merge or split notes |
| `unique-note-creator` | Unique note creator | Timestamp-ID notes (Zettelkasten) |
| `word-count` | Word count | Live word/char count |
| `file-recovery` | File recovery | Periodic local snapshots |
| `workspaces` | Workspaces | Save and switch pane layouts |
| `slides` | Slides | Turn a note into a presentation |
| `audio-recorder` | Audio recorder | Record audio into notes |
| `random-note` | Random note | Jump to a random note |
| `sync` | Sync | E2E encrypted cross-device sync (paid) |
| `publish` | Publish | Publish notes as a website (paid) |

---

## Key community plugins

### Dataview (`dataview`)
DQL query engine. Treats notes as a database. See `references/dataview.md`.

### Templater (`templater-obsidian`)
Advanced template engine with JS execution. See `references/templater.md`.

### Obsidian Tasks (`obsidian-tasks-plugin`)
Task management with emoji metadata and query blocks. See `references/tasks.md`.

### QuickAdd (`quickadd`)
Rapid note/data entry automation. Four choice types: Template, Capture, Macro, Multi. Format variables: `{{VALUE}}`, `{{DATE}}`, `{{LINKCURRENT}}`, `{{TEMPLATE:path}}`, `{{FIELD:name}}`. Built-in AI Assistant for LLM calls.

### Periodic Notes (`periodic-notes`)
Extends Daily Notes with weekly/monthly/quarterly/yearly. Each period has its own folder, format, template. Moment.js formats: `gggg-[W]ww` (weekly), `YYYY-MM` (monthly), `YYYY-[Q]Q` (quarterly), `YYYY` (yearly).

### Calendar (`obsidian-calendar-plugin`)
Sidebar calendar widget. Click day = open daily note. Week numbers = open weekly note. Defers to Periodic Notes settings when both installed.

### Linter (`obsidian-linter`)
Rule-driven auto-formatter. Key YAML rules: `yaml-title`, `yaml-title-alias`, `yaml-timestamp` (auto-created/modified dates), `sort-yaml-keys`, `format-yaml-array`.

### Obsidian Git (`obsidian-git`)
Git version control for vaults. Auto-commit/pull/push on interval. Gitignore `workspace.json` to avoid noise.

### Local REST API (`obsidian-local-rest-api`)
HTTP API for vault operations. See `references/cli.md`.

### Advanced URI (`obsidian-advanced-uri`)
Extended `obsidian://adv-uri` scheme. See `references/cli.md`.

### Excalidraw (`obsidian-excalidraw-plugin`)
Hand-drawn whiteboard. Files are `.excalidraw.md`. Text elements can be wikilinked. ExcalidrawAutomate JS API for programmatic drawing.

### Kanban (`obsidian-kanban`)
Markdown-backed kanban boards. `## Heading` = lane, `- [ ] text` = card. Frontmatter key `kanban-plugin: basic` marks a file as a board. Looking for new maintainers.

### Projects (`obsidian-projects`)
Metadata-driven views (table, board, calendar, gallery) over frontmatter. Discontinued May 2025 but still installable.

### Homepage (`obsidian-homepage`)
Opens a specific note/workspace/daily note on startup.

### Meta Bind (`obsidian-meta-bind-plugin`)
Inline input fields (`INPUT[toggle:done]`) and buttons bound to frontmatter. Modern replacement for Buttons plugin.

### Folder Notes (`obsidian-folder-notes`)
Click a folder to open its associated note (LostPaul). Auto-create, templates, folder overview codeblock.

### Auto Note Mover (`obsidian-auto-note-mover`)
Move notes to folders based on tag or title-regex rules.

### Excalidraw (`obsidian-excalidraw-plugin`)
Hand-drawn whiteboard with `.excalidraw.md` files (dual markdown+JSON), ExcalidrawAutomate scripting API, wikilink integration, block references. See `references/excalidraw.md`.

### Web Clipper (browser extension, not a vault plugin)
Official browser extension for clipping web content as markdown with frontmatter. Template system with variables, CSS selectors, schema.org extraction, and AI Interpreter. See `references/clipper.md`.

---

## Community plugin management

### Plugin file requirements

Each plugin lives in `.obsidian/plugins/<plugin-id>/`:
- **`manifest.json`** (required) -- `{id, name, version, minAppVersion, description, author}`
- **`main.js`** (required) -- compiled plugin code
- **`styles.css`** (optional) -- custom CSS
- **`data.json`** (auto-created) -- per-vault settings, safe to edit when Obsidian is closed

The folder name **must** match the `id` field in `manifest.json`.

### community-plugins.json (in vault)

The vault-level `.obsidian/community-plugins.json` is an array of enabled plugin IDs. It controls which installed plugins are active:
```json
["dataview", "templater-obsidian", "obsidian-excalidraw-plugin", "obsidian-linter"]
```

This is separate from the global plugin registry at `obsidianmd/obsidian-releases`.

### Installing plugins

**Via Obsidian UI** (recommended): Settings > Community plugins > Browse. Obsidian downloads `manifest.json`, `main.js`, `styles.css` from GitHub releases.

**Manual installation**: place `manifest.json` + `main.js` in `.obsidian/plugins/<plugin-id>/`, then enable via Settings > Community plugins > Installed plugins > toggle ON. Manually installed plugins don't auto-update.

**Via BRAT** (`obsidian42-brat`): install beta/unreleased plugins by pasting a GitHub repo URL. Handles updates automatically.

### Editing data.json

Safe to hand-edit **only when Obsidian is closed**. Changes require a full restart to take effect. Obsidian may overwrite manual edits if it writes settings while running.

Best practice: use the plugin's settings UI. Reserve manual editing for bulk vault setup, recovery, or programmatic pre-configuration.

### Restricted mode and trust

New vaults open in restricted mode (no community plugins). When opening a vault with pre-installed plugins, Obsidian shows a trust prompt. User must click "Trust author and enable plugins" to activate them.

### Pre-configuring plugins for a new vault

1. Install plugins via Obsidian UI (or manually place files)
2. Configure each plugin's settings
3. The resulting `.obsidian/plugins/` directory + `community-plugins.json` can be copied to new vaults
4. Recipients will see the trust prompt on first open
