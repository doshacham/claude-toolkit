# PKM Methodologies and Workflows

## Table of contents

1. Zettelkasten
2. PARA
3. LYT / ACCESS
4. Johnny Decimal
5. CODE / Building a Second Brain
6. Evergreen Notes
7. Daily / weekly / monthly reviews
8. MOCs and dashboards

---

## 1. Zettelkasten (Luhmann / Sonke Ahrens)

Atomic notes, one idea per note, linked to at least one other note.

**Three note types**:
- **Fleeting** -- raw captures, inbox-grade, disposable
- **Literature** -- one per source, written in your own words
- **Permanent** -- distilled, densely linked, concept-oriented

**Obsidian support**: Unique Note Creator core plugin stamps notes with timestamp IDs like `202604121430`. Typical layout: `Inbox/`, `Literature/`, `Permanent/` (or `Slipbox/`).

**When a user says "I do Zettelkasten"**: expect timestamp-prefixed filenames, dense `[[wikilinks]]`, minimal tags, fleeting/literature/permanent folders.

---

## 2. PARA (Tiago Forte)

Four top-level folders, ordered by actionability:
- **Projects** -- finite, deadline-bound outcomes
- **Areas** -- ongoing responsibilities with no finish line
- **Resources** -- topics of long-term interest, reference material
- **Archives** -- inactive items from the other three

Typical vault: `1 Projects/`, `2 Areas/`, `3 Resources/`, `4 Archives/`, optionally `0 Inbox/`. Notes migrate between folders as status changes.

**When a user says "I use PARA"**: expect these four numbered folders. Notes move between them. Folder placement IS the organizing principle.

---

## 3. LYT / ACCESS (Nick Milo)

**LYT (Linking Your Thinking)**: organize with links, not folders. Key artifacts:
- **MOC (Map of Content)** -- a note full of curated wikilinks, acting as a hub for a topic
- **Home note** -- single entry point linking to top MOCs and daily note
- **Hub notes** -- lighter MOCs for sub-topics

**ACCESS** (newer LYT structure): six top-level folders:
- **Atlas** -- MOCs, dashboards, overviews
- **Calendar** -- daily/weekly/monthly notes, journals
- **Cards** -- atomic notes (ideas, concepts, people)
- **Extras** -- attachments, templates, images
- **Sources** -- literature notes (books, articles, podcasts)
- **Spaces** -- broad life domains (Work, Personal)

**When a user says "I use LYT/ACCESS"**: expect MOCs, a home note, minimal folder hierarchy for content, dense linking.

---

## 4. Johnny Decimal

Numbered hierarchy: 10 areas (`10-19 Work`, `20-29 Health`) x 10 categories (`11 Clients`, `12 Invoices`) x items (`11.01`, `11.02`). Two levels, never more. Often layered on top of PARA.

**When a user says "I use Johnny Decimal"**: expect numbered folder names like `11 Clients/`, items like `11.01 Acme/`.

---

## 5. CODE / Building a Second Brain (Tiago Forte)

A process, not a folder system:
- **Capture** -- save what resonates
- **Organize** -- via PARA
- **Distill** -- progressive summarization (bold key passages, then highlight the bolded)
- **Express** -- ship the output

PARA is the storage layer underneath CODE.

---

## 6. Evergreen Notes (Andy Matuschak)

Stricter, more literary cousin of Zettelkasten permanents:
- Atomic, concept-oriented (not project- or source-oriented)
- Densely linked, associative over hierarchical
- Titles are full declarative claims ("Evergreen notes should be densely linked")
- Written to accumulate over years

**When a user says "I write Evergreen notes"**: expect declarative titles, few folders, heavy cross-linking.

---

## 7. Daily / weekly / monthly reviews

Driven by Periodic Notes + Templater + Calendar + Tasks. Typical loop:
- **Daily notes** capture logs, tasks, thoughts
- **Weekly notes** pull from dailies via Dataview (tasks completed, project mentions, metrics)
- **Monthly / quarterly notes** roll up from weeklies

Review template sections: wins, blockers, next period's focus, embedded Dataview queries.

Moment.js formats: `YYYY-MM-DD` (daily), `gggg-[W]ww` (weekly), `YYYY-MM` (monthly), `YYYY-[Q]Q` (quarterly), `YYYY` (yearly).

---

## 8. LLM Wiki (Karpathy pattern)

A pattern for building personal knowledge bases where the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files. Unlike RAG (which re-derives answers each time), the wiki is a **persistent, compounding artifact**.

**Source**: [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Three-layer architecture**:
- **Raw sources** -- immutable curated documents (articles, papers, transcripts). Source of truth. Obsidian Clipper drops content here.
- **The wiki** -- LLM-generated markdown (summaries, entity pages, concept pages, synthesis). The LLM owns this layer entirely.
- **The schema** -- configuration document (e.g., CLAUDE.md) specifying wiki structure, conventions, page types, and workflows.

**Three operations**:
- **Ingest** -- LLM reads new sources, writes summaries, updates entities/concepts, updates index. A single source may touch 10-15 wiki pages.
- **Query** -- LLM searches wiki pages, synthesizes answers, files valuable responses as new wiki pages.
- **Lint** -- periodic health check: find contradictions, stale claims, orphan pages, data gaps.

**Four page types** (typical):
- `source` -- one per ingested source (summary, key claims, entities referenced)
- `entity` -- people, tools, projects, organizations
- `concept` -- abstract ideas, patterns, frameworks
- `synthesis` -- cross-source analysis, comparisons, meta-insights

**Key insight**: the tedious part of a knowledge base is bookkeeping, not thinking. LLMs eliminate the maintenance burden. Human curates sources and asks questions; LLM does everything else.

**Obsidian integration**: Web Clipper for article capture into `raw/`, Dataview for querying across page types, Marp for presentations, wikilinks for dense cross-referencing.

**When a user says "LLM wiki" or follows the Karpathy pattern**: expect `raw/` (immutable sources), `wiki/` (LLM-generated pages), a `CLAUDE.md` schema, and the ingest/query/lint workflow. Respect the `raw/` immutability constraint.

---

## 9. MOCs and dashboards

**Hand-curated MOC** (LYT style):
```markdown
## Core ideas
- [[Atomic notes]]
- [[Densely linked notes]]
- [[Emergence over hierarchy]]

## Open questions
- [[What makes a note done]]
```

**Dataview-generated dashboard**:
````
```dataview
TABLE file.mtime AS "Updated", tags
FROM "Permanent" AND #concept
SORT file.mtime DESC
LIMIT 20
```
````

A home note typically combines: a few MOCs-as-links, an inbox query, a "recently modified" query, and links to the current daily note and active projects.
