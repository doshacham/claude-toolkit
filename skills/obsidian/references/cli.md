# Obsidian CLI, REST API, and URI Reference

## Table of contents

1. Official Obsidian CLI (v1.12+)
2. Local REST API plugin
3. Obsidian URI (built-in)
4. Advanced URI plugin
5. obsidian-export (headless)
6. notesmd-cli (headless, no app needed)

---

## 1. Official Obsidian CLI (v1.12+)

Shipped with Obsidian desktop (v1.12.0, Feb 2026). Enable: Settings > General > Command line interface > register to PATH.

### Commands

| Command | Purpose | Example |
|---|---|---|
| `obsidian daily` | Open today's daily note | `obsidian daily` |
| `obsidian search <query>` | Search vault | `obsidian search "tag:#project"` |
| `obsidian append <note> <text>` | Append text to a note | `obsidian append "Daily Note" "- Follow up with Dori"` |
| `obsidian read <note>` | Print note contents | `obsidian read "Projects/Alpha"` |
| `obsidian tasks` | List tasks | `obsidian tasks` |
| `obsidian create <name>` | Create a new note | `obsidian create "Ideas/New Concept"` |
| `obsidian tags` | List all tags | `obsidian tags` |
| `obsidian diff` | Show changes | `obsidian diff` |

### Dev commands

`devtools`, `plugin:reload`, `dev:screenshot`, `eval`, `dev:errors`, `dev:css`, `dev:dom`.

---

## 2. Local REST API plugin (coddingtonbear)

Community plugin. Install from community plugin browser, search "Local REST API".

### Setup

- Default HTTPS: `https://127.0.0.1:27124` (self-signed cert)
- Default HTTP (off by default): `http://127.0.0.1:27123` (enable in plugin settings)
- API key: Settings > Local REST API > copy key
- Auth header: `Authorization: Bearer YOUR_API_KEY`
- `GET /` is unauthenticated (health check)

### Endpoints

**Vault files** (`{path}` = vault-relative path):

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/vault/` | List files at vault root |
| `GET` | `/vault/{path}` | Read file content |
| `PUT` | `/vault/{path}` | Create or overwrite file |
| `POST` | `/vault/{path}` | Append to file |
| `PATCH` | `/vault/{path}` | Surgical insert (see PATCH section) |
| `DELETE` | `/vault/{path}` | Delete file |

**Periodic notes** (`{period}` = `daily|weekly|monthly|quarterly|yearly`):

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/periodic/{period}/` | Get current period's note |
| `PUT` | `/periodic/{period}/` | Overwrite |
| `POST` | `/periodic/{period}/` | Append |
| `PATCH` | `/periodic/{period}/` | Surgical insert |
| `DELETE` | `/periodic/{period}/` | Delete |

**Active note** (currently open in Obsidian):

`GET /active/`, `PUT /active/`, `POST /active/`, `PATCH /active/`, `DELETE /active/`

**Commands**:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/commands/` | List all available commands |
| `POST` | `/commands/{commandId}/` | Execute a command |

**Search**:

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/search/` | Dataview DQL or JsonLogic search |
| `POST` | `/search/simple/?query=foo&contextLength=100` | Simple text search |

**Other**:

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/open/{path}` | Open file in Obsidian UI |
| `GET` | `/tags/` | List all tags with counts |

### PATCH -- surgical edits

PATCH inserts content at a specific location without rewriting the whole file. Configure via headers:

**Required headers**:
- `Operation`: `append` | `prepend` | `replace`
- `Target-Type`: `heading` | `block` | `frontmatter`
- `Target`: what to target
  - For `heading`: delimited path like `Tasks::Today` (nested headings separated by `::`)
  - For `block`: the block ID (the `^abc123` marker, without the caret)
  - For `frontmatter`: the YAML field name (e.g. `tags`, `status`)

**Optional headers**:
- `Target-Delimiter`: default `::`, override if heading names contain `::`
- `Trim-Target-Whitespace`: `true|false`
- `Create-Target-If-Missing`: `true|false` -- auto-create heading/field
- `Apply-If-Content-Preexists`: `true|false` -- skip if same content exists (idempotency)

**Body**: `text/markdown` for content, or `application/json` for frontmatter values.

### Curl examples

```bash
# Set API key
export OBSIDIAN_API_KEY=your_key_here

# Health check (no auth)
curl -k https://127.0.0.1:27124/

# List vault root
curl -k -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  https://127.0.0.1:27124/vault/

# Read a note
curl -k -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  https://127.0.0.1:27124/vault/Daily/2026-04-12.md

# Create or overwrite a note
curl -k -X PUT -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data $'# Meeting Notes\n\n- kickoff' \
  https://127.0.0.1:27124/vault/Meetings/2026-04-12.md

# Append to today's daily note
curl -k -X POST -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data $'\n- Captured at '"$(date +%H:%M)" \
  https://127.0.0.1:27124/periodic/daily/

# Patch under a heading
curl -k -X PATCH https://127.0.0.1:27124/periodic/daily/ \
  -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Operation: append" -H "Target-Type: heading" -H "Target: Log" \
  -H "Content-Type: text/markdown" \
  --data "- 14:02 shipped the feature"

# Execute a command
curl -k -X POST -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  https://127.0.0.1:27124/commands/daily-notes/

# Dataview DQL search
curl -k -X POST -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  -H "Content-Type: application/vnd.olrapi.dataview.dql+txt" \
  --data 'TABLE file.mtime FROM "Projects" WHERE status = "active"' \
  https://127.0.0.1:27124/search/

# Simple text search
curl -k -X POST -H "Authorization: Bearer $OBSIDIAN_API_KEY" \
  "https://127.0.0.1:27124/search/simple/?query=TODO&contextLength=80"
```

---

## 3. Obsidian URI (built-in)

Format: `obsidian://<action>?key=value&...`. Values must be URL-encoded.

### Actions

| Action | Parameters | Purpose |
|---|---|---|
| `open` | `vault`, `file` (or `path`) | Open a vault/file |
| `new` | `vault`, `name` (or `file`), `content`, `silent`, `append`, `overwrite` | Create a note |
| `search` | `vault`, `query` | Open search pane |
| `hook-get-address` | (none) | Copy active note as markdown link (Hookmark) |
| `show-plugin` | `id` | Open plugin page in plugin browser |

Shorthand: `obsidian://vault/<VaultName>/<NotePath>`

### Shell invocation

| OS | Command |
|---|---|
| Windows (cmd) | `start "" "obsidian://open?vault=Work&file=Today"` |
| Windows (PowerShell) | `Start-Process "obsidian://open?vault=Work&file=Today"` |
| Git Bash | `cmd //c start "" "obsidian://open?vault=Work&file=Today"` |
| macOS | `open "obsidian://open?vault=Work&file=Today"` |
| Linux | `xdg-open "obsidian://open?vault=Work&file=Today"` |

Always double-quote the URI -- `&` is a shell metacharacter.

---

## 4. Advanced URI plugin (Vinzent03)

Extends built-in URI with `obsidian://adv-uri?vault=...&...`.

### Key parameters

| Parameter | Purpose |
|---|---|
| `vault` | Vault name (required) |
| `filepath` / `filename` | Target note |
| `uid` | Stable note ID from frontmatter (survives renames) |
| `daily`, `weekly`, `monthly`, `yearly`, `quarterly` | Set to `true` for periodic notes |
| `data` | Content to write (URL-encoded) |
| `clipboard` | Set to `true` to use clipboard |
| `mode` | `write` (if absent) / `overwrite` / `append` / `prepend` / `new` |
| `heading` / `block` / `line` / `column` | Navigate or anchor insertion |
| `commandid` / `commandname` | Execute an Obsidian command |
| `search` / `searchregex` + `replace` | Find and replace |
| `viewmode` | `source` / `live` / `preview` |
| `openmode` | `true` / `tab` / `split` / `window` / `silent` / `popover` |
| `workspace` | Load a named workspace |
| `settingid` / `settingsection` | Open specific settings pane |
| `frontmatterkey` + value | Read/write frontmatter |
| `x-success` / `x-error` | Callback URLs |

### Examples

```
# Append clipboard to today's daily note
obsidian://adv-uri?vault=Work&daily=true&clipboard=true&mode=append

# Open note at a heading in reading view
obsidian://adv-uri?vault=Work&filepath=docs/api&heading=Authentication&viewmode=preview

# Run a command against a specific file
obsidian://adv-uri?vault=Work&filepath=projects/big-one&commandid=workspace:close

# Create a note with content
obsidian://adv-uri?vault=Work&filepath=inbox/capture&mode=new&data=Quick%20thought
```

### URL encoding

Spaces: `%20`. Newlines: `%0A`. Colons: `%3A`. Slashes: `%2F`.
Double-encode when launching from shell (shell + URI handler each strip one layer).

---

## 5. obsidian-export (zoni)

Rust binary that converts a vault to standard Markdown. Resolves wikilinks and embeds.

```bash
# Install
cargo install obsidian-export

# Export entire vault
obsidian-export my-vault exported/

# Export a subfolder
obsidian-export my-vault --start-at my-vault/Books exported/

# Filter by tags
obsidian-export my-vault --only-tags "publish" exported/
obsidian-export my-vault --skip-tags "draft" exported/
```

Supports `.export-ignore` and `.gitignore`. Does not need Obsidian running.

---

## 6. notesmd-cli (formerly Yakitrak/obsidian-cli)

Go binary for vault operations without Obsidian running. Direct filesystem access.

```bash
# Install (Windows)
scoop install notesmd-cli

# Install (macOS/Linux)
brew install yakitrak/yakitrak/notesmd-cli

# Open a note in Obsidian
notesmd-cli open "Projects/Alpha" --vault work

# Search note content
notesmd-cli search-content "project deadline" --vault work --format json

# Create a note
notesmd-cli create "Inbox/Quick Capture" --vault work

# Manage frontmatter
notesmd-cli frontmatter "note" --vault work
```
