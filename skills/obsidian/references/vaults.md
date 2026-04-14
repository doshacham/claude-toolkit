# Dori's Obsidian Vaults

## Vault discovery protocol

**Never assume a path is correct.** Always discover the vault dynamically:

1. **Check the current working directory first.** If cwd contains `.obsidian/`, it IS the vault — use it.
2. **If the user names a vault** — match against the profiles below by **name or fingerprint**, then scan for it:
   ```bash
   find /c/Users/User/Desktop /c/Users/User/Documents -maxdepth 5 -name ".obsidian" -type d 2>/dev/null
   ```
3. **Confirm the match** by checking the vault's fingerprint (CLAUDE.md, folder structure, community-plugins.json) against the profile.
4. **If not found** — ask the user for the path. Don't guess.
5. **After locating** — read the vault's `.obsidian/` config and `CLAUDE.md` (if any) to get the actual current state. Profiles below are snapshots that may be outdated.

---

## Vault profiles

Profiles describe what makes each vault recognizable. They are keyed by **name**, not path. The fingerprint is what you match against when scanning.

### Desktop (mega vault)

- **Fingerprint**: `.obsidian/` directly inside `~/Desktop`. No community plugins. ~5k+ notes. No CLAUDE.md.
- **Profile**: The entire Desktop folder treated as a vault. Catch-all with project subfolders, task files, guides, backups. Fully default config.
- **Structure**: Flat root with project subfolders
- **Plugins**: Core only (defaults)

### Help The Clanker

- **Fingerprint**: Folder named `Help The clanker` (case matters). Contains `skills i want to create/` with subfolders `AI Loops/`, `Commands/`, `Debugging/`, `Get Shit Done/`.
- **Profile**: Project planning vault for Claude Code skills/agent development. ~120 notes.
- **Structure**: `skills i want to create/`, `notes/`, `plans/`, `diagrams/`, `images/`
- **Plugins**: Core only (Daily Notes, Templates, Bases, Sync, Graph, Search, Bookmarks, Outline, Properties)

### Dori-wiki

- **Fingerprint**: Has `CLAUDE.md` defining the "LLM Wiki Pattern". Contains `raw/`, `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/`, `core/` (viewer app code), `docs/`.
- **Profile**: Personal LLM-wiki / knowledge base. ~34 notes. Formal schema in CLAUDE.md.
- **Schema**: Read its `CLAUDE.md` for page types, frontmatter, naming, links, citations. Always follow that schema.
- **Plugins**: Core only
- **Templates**: Use this skill's `assets/templates/dori-wiki-*` templates

### OpenClaw (LLM wiki)

- **Fingerprint**: Has `CLAUDE.md` mentioning "OpenClaw LLM Wiki". Contains `raw/`, `wiki/`, `Drawings/`, `mydatabase.db`. Community plugins include `dataview`, `templater-obsidian`, `obsidian-excalidraw-plugin`, `obsidian-linter`.
- **Profile**: LLM wiki vault (Karpathy pattern). Obsidian Clipper drops raw content into `raw/`. LLM processes into `wiki/` pages.
- **Schema**: Read its `CLAUDE.md` for page types, frontmatter, naming, operations (ingest/query/lint).
- **Plugins**: Dataview, Templater, Excalidraw, Linter
- **Clipper workflow**: raw/ is the inbox. Files arrive with `status: unread`. LLM ingests. Raw files are immutable.

### Documents Vault

- **Fingerprint**: Inside `~/Documents`. Has `obsidian-local-rest-api` in community plugins. Nearly empty (~0 notes). Contains `skills i want to create/`.
- **Profile**: Fresh vault with Local REST API. Potential "main" personal vault.
- **Plugins**: `obsidian-local-rest-api`

---

## Inactive / duplicates

- **workspace-vault**: Empty scratch vault (~1 note). Likely a code workspace artifact.
- **tmp-repos/Dori-wiki**: Clone/worktree of Dori-wiki. Temporary copy.

---

## Common conventions

- Most vaults use default `app.json`.
- Core plugins commonly enabled: Daily Notes, Templates, Graph, Search, Bookmarks, Properties, Outline.
- LLM wiki vaults (Dori-wiki, OpenClaw) have formal schemas in `CLAUDE.md` — always read and follow them.
- Link format: wikilinks (shortest path) everywhere.
- Dates: ISO `YYYY-MM-DD` in frontmatter.

---

## Bootstrap checklist (for new vaults)

1. Enable core plugins: Daily Notes, Templates, Bookmarks, Graph, Search, Properties, Outline
2. Install community plugins: Dataview, Templater, Obsidian Tasks, Linter
3. Create `Templates/` folder, add templates from this skill's `assets/templates/`
4. Configure Daily Notes: format `YYYY-MM-DD`, folder `Daily/`, template `Templates/Daily`
5. Configure Templates: folder `Templates/`
6. Configure Linter: enable `yaml-timestamp`
7. Set attachment folder: `Attachments/`
8. Add `.gitignore` from `references/guardrails.md` if using git
