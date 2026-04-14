---
name: ingest
description: "Ingest raw sources into an LLM Wiki vault. Reads unprocessed files from raw/, creates structured wiki pages (sources, entities, concepts, synthesis), links everything with wikilinks, updates the index and log. Use when the user says 'ingest', 'process raw', 'process clippings', 'update wiki', or when raw/ contains unread items that need processing."
allowed-tools: Read Write Edit Glob Grep Bash WebFetch AskUserQuestion
---

# Ingest: Raw Source → Wiki Pages

Automate the **ingest** operation of the LLM Wiki pattern. Transform raw source material into structured, interlinked wiki pages.

## Before starting

1. **Locate the vault.** The vault is the current working directory if it contains `.obsidian/`. Otherwise, ask.
2. **Read the vault's `CLAUDE.md`.** This is the schema — it defines page types, frontmatter, naming conventions, and folder paths. Follow it exactly. If no `CLAUDE.md` exists, this vault is not an LLM Wiki vault — tell the user and stop.
3. **Read `.obsidian/community-plugins.json`** to know what plugins are available (Dataview, Templater, Excalidraw, etc.).

## Arguments

If the user provides arguments (`$ARGUMENTS`), interpret them as:
- A filename or glob pattern to ingest specific files from `raw/`
- `all` to process every unread item
- A URL, repo, or other source to fetch and ingest directly
- Empty = run Step 0 (check inbox, offer to add new material)

## Step 0: Check inbox and offer to add new material

**Always start here.** Before scanning `raw/`, use AskUserQuestion to ask the user:

**Question 1** — "Do you have new material to add before processing?" with options:
- **"Process existing raw/ items"** — skip to Step 1, there's already material in the inbox
- **"Yes, I have something to add"** — proceed to Question 2 to capture it
- **"Fetch something from the web"** — the user will provide a URL to fetch and drop into `raw/`

**Question 2** (if they chose "Yes" or "Fetch") — "What type of source are you adding?" with options:
- **"URL / web article"** — user provides a link. Use WebFetch to grab it, convert to markdown, save to `raw/` with frontmatter (`source`, `clipped`, `status: unread`)
- **"GitHub repo or issue"** — user provides a repo URL, issue URL, or PR URL. Use `gh` CLI to fetch README, issue body, or PR description. Save to `raw/`
- **"Paste / raw text"** — user will paste content directly. Save verbatim to `raw/` with frontmatter
- **"PDF or local file"** — user provides a file path. Read it with the Read tool, save markdown conversion to `raw/`

After capturing, ask: "Want to add more sources, or start processing?" Loop until they say process.

### Source types the user might provide (handle all of these):

| Source type | How to capture | Frontmatter fields |
|---|---|---|
| Web article / blog post | WebFetch the URL, extract content | `source: <url>`, `author`, `clipped`, `status: unread` |
| GitHub repository | `gh repo view <repo> --json name,description,url` + fetch README | `source: <repo-url>`, `type: repo`, `clipped`, `status: unread` |
| GitHub issue | `gh issue view <url> --json title,body,author,labels,comments` | `source: <issue-url>`, `author`, `clipped`, `status: unread` |
| GitHub PR | `gh pr view <url> --json title,body,author,files,comments` | `source: <pr-url>`, `author`, `clipped`, `status: unread` |
| arXiv paper | WebFetch the abstract page, or use /read-arxiv if available | `source: <arxiv-url>`, `author`, `published`, `clipped`, `status: unread` |
| YouTube video | WebFetch the page, extract title/description/transcript if accessible | `source: <yt-url>`, `author`, `published`, `clipped`, `status: unread` |
| Tweet / X post | WebFetch the URL | `source: <tweet-url>`, `author`, `clipped`, `status: unread` |
| Hacker News thread | WebFetch the URL, capture top comments | `source: <hn-url>`, `clipped`, `status: unread` |
| Reddit post | WebFetch the URL | `source: <reddit-url>`, `author`, `clipped`, `status: unread` |
| Documentation page | WebFetch the URL | `source: <url>`, `clipped`, `status: unread` |
| Local file (PDF, .md, .txt) | Read tool to read the file | `source: <filepath>`, `clipped`, `status: unread` |
| Pasted text / notes | User pastes directly in chat | `source: manual`, `clipped`, `status: unread` |
| Linear / Jira ticket | WebFetch or CLI if available | `source: <ticket-url>`, `clipped`, `status: unread` |
| Slack thread | User pastes the content | `source: slack`, `clipped`, `status: unread` |
| Book excerpt / quote | User pastes with attribution | `source: manual`, `author`, `clipped`, `status: unread` |
| API docs / OpenAPI spec | WebFetch the URL | `source: <url>`, `clipped`, `status: unread` |
| Conference talk / slides | WebFetch or user pastes notes | `source: <url>`, `author`, `clipped`, `status: unread` |
| Podcast transcript | WebFetch or user pastes | `source: <url>`, `author`, `published`, `clipped`, `status: unread` |

**Filename for raw files**: use `<slugified-title>.md`. If no title, use `<domain>-<date>.md` or `manual-<date>.md`.

## Step 1: Discover unread sources

Scan the raw sources folder (typically `raw/`) for files with `status: unread` in frontmatter, or files with no `status` field (treat as unread). Use Grep to find them:

```
Grep pattern: "status: unread" in raw/
Glob pattern: raw/*.md
```

Also check for files with no status field — any `.md` file in `raw/` without a `status` property is unread.

List all unread items to the user showing: filename, title, source URL, clipped date. Then proceed to process them.

## Step 2: Read and analyze each source

For each source file being ingested:

1. **Read the full content** of the raw file
2. **Extract metadata** from frontmatter (title, URL, author, clipped date)
3. **Analyze the content** to identify:
   - **Key claims and insights** — the important ideas worth preserving
   - **Entities** — people, tools, projects, organizations mentioned
   - **Concepts** — abstract ideas, patterns, frameworks discussed
   - **Cross-references** — connections to existing wiki pages

## Step 3: Create the source page

Create a wiki source page following the vault's schema. Typical path: `wiki/sources/<slug>.md`

The source page must include:
- Frontmatter matching the schema (`title`, `type: source`, `created`, `updated`, `sources`, `tags`)
- A summary in your own words (not just copied text)
- Key claims as a bulleted list
- Entities and concepts mentioned, as wikilinks: `[[entities/person-name]]`, `[[concepts/idea-name]]`
- A link back to the raw file
- Source URL if available

**Naming**: kebab-case slug derived from the title.

## Step 4: Create or update entity pages

For each significant entity (person, tool, project, organization) mentioned in the source:

1. **Check if the entity page already exists** in `wiki/entities/` using Grep or Glob
2. **If it exists**: update it — add the new source to its `sources` list, add any new facts, add the source wikilink
3. **If new**: create the entity page with frontmatter, a description, key facts, and a "Appears in" section with wikilinks

Only create entity pages for **significant** entities — not every name or tool mentioned in passing. Use judgment.

## Step 5: Create or update concept pages

For each significant concept, pattern, or idea discussed:

1. **Check if the concept page already exists** in `wiki/concepts/`
2. **If it exists**: update it with new information from this source, add source to `sources` list
3. **If new**: create the concept page with a definition, key properties, related concepts (as wikilinks), and sources

## Step 5b: Create Excalidraw relationship map

For each ingested source, create a visual relationship diagram in `Drawings/`:

1. **Create** `Drawings/map-<source-slug>.excalidraw.md`
2. **Layout**: the source as a central node, entities branching in one direction (color: blue), concepts branching in another (color: green), with labeled connection arrows
3. **Wikilinks in nodes**: each node's text should contain a `[[wikilink]]` to its wiki page so clicking navigates there
4. **Frontmatter**: include `excalidraw-plugin: parsed`, `tags: [excalidraw, map]`, `excalidraw-autoexport: svg`
5. **Embed** the drawing in the source page with `![[Drawings/map-<source-slug>.excalidraw]]`

If this is the 2nd+ source ingested, also **update or create** `Drawings/wiki-map.excalidraw.md` — a master graph showing all sources, entities, and concepts with their connections. This grows with each ingest.

## Step 6: Consider synthesis pages

If the source **connects, contradicts, or extends** existing wiki content in a meaningful way, create a synthesis page in `wiki/synthesis/`. Synthesis pages should:

- Compare or contrast claims across multiple sources
- Identify patterns or trends
- Resolve contradictions
- Draw meta-level conclusions

Only create synthesis pages when there's genuine cross-source insight. Don't force it.

## Step 7: Update the index

Read `wiki/index.md` and verify it will surface the new pages. If index.md uses Dataview queries (recommended), no manual update is needed — the queries auto-update. If it's a manual list, add entries for each new page.

## Step 8: Update the log

Append an entry to `wiki/log.md`:

```markdown
## YYYY-MM-DD

- **Ingested**: "Source Title" (`raw/filename.md`)
- **Created**: [[sources/slug]], [[entities/person]], [[concepts/idea]]
- **Updated**: [[entities/existing-entity]] (added new source)
```

## Step 9: Mark raw file as done

Edit the raw file's frontmatter to change `status: unread` to `status: done`. **Do not modify any other content in the raw file** — raw sources are immutable except for the status field.

## Step 10: Report

Show the user a summary:
- How many raw files were processed
- What wiki pages were created (with wikilinks)
- What wiki pages were updated
- Any cross-references or connections discovered
- Any items skipped and why
- Count of remaining unread items in `raw/`

## Linking guidelines

- **Every wiki page must link to its sources**: `(from [[sources/slug]])`
- **Entity and concept pages must cross-link**: if a concept page mentions an entity, link it. If an entity page relates to a concept, link it.
- **Use wikilinks with paths**: `[[sources/karpathy-llm-wiki]]`, not `[[karpathy-llm-wiki]]`
- **Use display aliases for readability**: `[[entities/andrej-karpathy|Karpathy]]`
- **Quote wikilinks in YAML**: `sources: ["[[sources/slug]]"]` or use plain slugs per the vault schema

## Quality standards

- **Summaries in your own words** — never just copy-paste from the source
- **Every claim must cite its source** — `(from [[sources/slug]])`
- **Frontmatter must be complete** — no missing required fields
- **Dates in ISO format** — `YYYY-MM-DD`
- **Kebab-case filenames** — `vannevar-bush.md`, not `Vannevar Bush.md`
- **Check for duplicates** before creating new pages — grep for existing entity/concept names
- **Dense wikilinks** — err on the side of more links, not fewer

## Using installed plugins — USE ALL OF THEM

Every installed plugin exists for a reason. Use them aggressively during ingest.

### Dataview

Include Dataview query blocks in every wiki page where they add value:

- **Source pages**: query for other sources that reference the same entities/concepts
- **Entity pages**: "Appears in" section with `LIST FROM "wiki" WHERE contains(file.outlinks, this.file.link)`
- **Concept pages**: "Related sources" and "Related entities" queries
- **Synthesis pages**: queries that surface the pages being compared

### Excalidraw — auto-create visual maps

After processing each source, **automatically create an Excalidraw relationship diagram** in `Drawings/` that maps:

- The source and its key entities/concepts as nodes
- Connections between them as labeled arrows
- Links back to wiki pages via wikilinks in text elements

Use the ExcalidrawAutomate API pattern:

```javascript
// In a code block or via script — conceptual structure:
// 1. Central node: the source title
// 2. Entity nodes branching out (color-coded by type: person, tool, project, org)
// 3. Concept nodes branching out (different color)
// 4. Arrows labeled with the relationship
// 5. Each node text contains a [[wikilink]] to its page
```

Create the `.excalidraw.md` file directly with the proper structure:

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw, map]
excalidraw-autoexport: svg
excalidraw-export-transparent: true
---

# Excalidraw Data
[compressed JSON data]

# Text Elements
Source: Title ^source-id
Entity: Name ^entity-id
Concept: Idea ^concept-id

## Embedded Files
```

**Naming**: `map-<source-slug>.excalidraw.md` in `Drawings/`

**Embed the drawing** in the source page: `![[Drawings/map-<source-slug>.excalidraw]]`

When multiple sources share entities or concepts, create or update a **master relationship map** (`Drawings/wiki-map.excalidraw.md`) that shows the full knowledge graph.

### Linter

The linter auto-formats YAML on save — write clean YAML and don't fight its formatting. It will handle:
- Sorting YAML keys
- Formatting arrays
- Adding timestamps if configured

### Templater

Templates exist in the vault's `Templates/` folder for manual page creation. During ingest, create pages directly (don't invoke Templater) since you have all the data. But ensure the pages you create match the template structure so they're consistent with manually created pages.
