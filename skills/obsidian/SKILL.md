---
name: obsidian
description: "Operate Obsidian vaults end-to-end: run the official Obsidian CLI (v1.12+), call the Local REST API, build Dataview and Tasks queries, write Templater templates, create daily notes and templates, edit notes and properties, configure core and community plugins, manage community plugin installation and settings, script with ExcalidrawAutomate, handle Obsidian Clipper raw inbox workflows, and apply PKM workflows including the LLM Wiki pattern. Relevant when the user mentions Obsidian, asks to work with a vault, create or edit notes, build daily note templates, script vault automation, query vault contents, configure plugins, or when notes involve wikilinks, callouts, block references, properties, Dataview, Templater, Obsidian Tasks, QuickAdd, Periodic Notes, Canvas, Graph view, Excalidraw, Kanban, Linter, Obsidian Git, Obsidian Clipper, CSS snippets, themes, cssclasses, Meta Bind, or PKM methodologies like Zettelkasten, PARA, LYT, or LLM Wiki."
allowed-tools: Read Write Edit Glob Grep Bash WebFetch WebSearch
---

# Obsidian vault operations

Operate Obsidian vaults: read and edit notes, query with Dataview, script with the official CLI or Local REST API, configure plugins, and apply PKM patterns. Detailed references live in `references/` -- read the relevant file when you need precise syntax.

## Before any operation

1. **Locate the vault.** A vault is any folder containing a `.obsidian/` subfolder. **Always discover dynamically** — never trust a hardcoded path. If cwd contains `.obsidian/`, it IS the vault. Otherwise, match the user's description against vault profiles in `references/vaults.md` by name or fingerprint, scan the filesystem, and confirm the match. If not found, ask.
2. **Check whether Obsidian is running.** If the desktop app is open on the target vault, prefer the official CLI or Local REST API over direct filesystem writes -- direct writes race the indexer.
3. **Read the vault's conventions.** Check `.obsidian/daily-notes.json`, `.obsidian/templates.json`, `.obsidian/types.json`, and `.obsidian/community-plugins.json` before writing anything. These tell you the date format, template folder, property types, and which plugins are installed.
4. **Check for CLAUDE.md in the vault root.** LLM Wiki vaults (like OpenClaw) have a schema file defining page types, naming conventions, and the ingest/query/lint workflow. Follow that schema exactly.

## The three CLI interfaces

| When you need to | Use | Reference |
|---|---|---|
| Quick vault operation from the terminal | Official Obsidian CLI (`obsidian daily`, `obsidian search`, `obsidian append`, `obsidian read`, `obsidian create`, `obsidian tasks`, `obsidian tags`, `obsidian diff`) | `references/cli.md` |
| Surgical edits (append under heading, patch frontmatter, run commands, search via DQL) | Local REST API plugin (ports 27123/27124, Bearer auth) | `references/cli.md` |
| One-shot URI from a script, shortcut, or hotkey | `obsidian://` or `obsidian://adv-uri` | `references/cli.md` |
| Export vault to portable Markdown | `obsidian-export` (Rust binary by zoni) | `references/cli.md` |
| Edit files when Obsidian is closed | Direct filesystem Read/Write/Edit | -- |

## Writing to a vault

Always preserve the existing frontmatter format. Quote internal links in property values (`link: "[[Note]]"`) -- YAML parses unquoted `[[...]]` as a list. Never overwrite `cssclasses`, `aliases`, or `tags` without merging. When adding a new property, check `.obsidian/types.json` first -- property types are vault-wide and a type mismatch corrupts the Properties UI.

Detailed rules: `references/properties.md` and `references/guardrails.md`.

## Obsidian-flavored Markdown

Obsidian extends CommonMark with wikilinks (`[[Page]]`, `[[Page|alias]]`, `[[Page#Heading]]`, `[[Page#^block-id]]`), embeds (`![[Note]]`), callouts (`> [!type]`), block references (`^block-id`), highlight syntax (`==text==`), and comments (`%%hidden%%`). Reference: `references/syntax.md`.

## Querying a vault

- **Built-in search**: boolean, regex, `file:`, `path:`, `content:`, `tag:`, `line:`, `block:`, `section:`, `task:`, `task-todo:`, `task-done:`, `[property:value]`. Reference: `references/search.md`.
- **Dataview (DQL)**: `LIST`/`TABLE`/`TASK`/`CALENDAR` from `"folder"` / `#tag` / `[[link]]`. Always put `SORT` before `LIMIT`. Reference: `references/dataview.md`.
- **DataviewJS**: `dv.pages(source).where(...)`, `dv.table(...)`, `dv.list(...)`. Same reference.
- **Obsidian Tasks query blocks**: ` ```tasks ... ``` ` with filters like `not done`, `due before tomorrow`, `sort by due`, `group by folder`. Reference: `references/tasks.md`.

## Creating templates

Two template engines:

1. **Core Templates plugin**: static substitution of `{{title}}`, `{{date}}`, `{{time}}`, with inline moment.js format like `{{date:YYYY-MM-DD}}`. Good for simple cases.
2. **Templater plugin**: full JS with `<% %>` and `<%* %>` syntax, modules `tp.date`, `tp.file`, `tp.system.prompt`/`suggester`, `tp.frontmatter`, `tp.user`, `tp.web`, `tp.hooks`. Reference: `references/templater.md`.

Starter templates: `assets/templates/` (daily note, meeting, zettel, project, MOC, weekly review). Dori-wiki vault-specific templates: `dori-wiki-concept`, `dori-wiki-entity`, `dori-wiki-source`, `dori-wiki-synthesis` (match the wiki's CLAUDE.md schema). LLM wiki templates: `llm-wiki-source`, `llm-wiki-entity`, `llm-wiki-concept`, `llm-wiki-synthesis` (for Karpathy-pattern vaults like OpenClaw).

## Configuring plugins

Core and community plugin detection and settings: `references/plugins.md`.
All `.obsidian/` config files and their schemas: `references/config.md`.
CSS theming, snippets, variables, and `cssclasses`: `references/css.md`.

Plugin settings live in `.obsidian/plugins/<plugin-id>/data.json` -- safe to edit when Obsidian is closed.

### Key plugin references

- **Excalidraw** (visual diagrams, `.excalidraw.md` files, ExcalidrawAutomate scripting API): `references/excalidraw.md`
- **Obsidian Web Clipper** (browser extension, raw inbox, template variables, AI Interpreter): `references/clipper.md`
- **Community plugin management** (installation, data.json, BRAT, restricted mode): bottom of `references/plugins.md`

## PKM methodologies

Recognize these vault layouts and speak the right vocabulary:

- **Zettelkasten**: timestamp-ID notes, fleeting/literature/permanent folders, dense wikilinks.
- **PARA** (Tiago Forte): `1 Projects / 2 Areas / 3 Resources / 4 Archives` folders.
- **LYT / ACCESS** (Nick Milo): MOCs, home note, Atlas/Calendar/Cards/Extras/Sources/Spaces.
- **Johnny Decimal**: numbered `10-19`/`11.01` hierarchy.
- **Evergreen notes** (Andy Matuschak): declarative titles, concept-oriented, densely linked.
- **LLM Wiki** (Karpathy): `raw/` (immutable sources via Clipper), `wiki/` (LLM-generated pages: sources, entities, concepts, synthesis), `CLAUDE.md` schema. Three operations: ingest, query, lint.

Reference: `references/workflows.md`.

## LLM Wiki vaults

For vaults following the Karpathy LLM Wiki pattern:

1. **Check CLAUDE.md first** -- it defines the schema, page types, naming conventions, and operations for that vault.
2. **Respect `raw/` immutability** -- never edit raw source files (only update frontmatter `status`).
3. **Follow the ingest workflow** -- read raw, create source page, update entities/concepts, update index, append to log.
4. **Always cite sources** -- `(from [[sources/slug]])` in every wiki page.
5. **Update `wiki/index.md`** after creating new pages.
6. **Append to `wiki/log.md`** after every ingest/lint operation.

Clipper integration: raw content drops into `raw/` with `status: unread`. The LLM processes it. See `references/clipper.md` for Clipper template setup.

## Dori's vaults

Known vaults on this system with their paths and profiles: `references/vaults.md`. Read this first when the user says "my vault" without specifying which one.

## Guardrails (always apply)

- Never edit `workspace.json` while Obsidian is running -- it races the app.
- Never rename notes from the OS shell -- use Obsidian, the CLI, or the REST API.
- Quote internal links in YAML: `link: "[[Note]]"`.
- `SORT` before `LIMIT` in DQL, always.
- Templater: escape `---` frontmatter fences in templates or use `<% "---" %>`.
- Do not mix frontmatter and inline Dataview fields for the same key.
- `cssclasses` (plural) is the reserved name; `cssclass` (singular) is deprecated.
- Dates in frontmatter: always ISO `YYYY-MM-DD`. Never `2026/04/12` or natural language.

Full list with rationale: `references/guardrails.md`.
