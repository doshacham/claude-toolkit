# Obsidian Web Clipper Reference

The official browser extension for capturing web content into Obsidian vaults as Markdown.

**Official**: [obsidian.md/clipper](https://obsidian.md/clipper), [GitHub](https://github.com/obsidianmd/obsidian-clipper), [Help docs](https://help.obsidian.md/Plugins/Web+Clipper)
**Community templates**: [github.com/obsidian-community/web-clipper-templates](https://github.com/obsidian-community/web-clipper-templates)

---

## 1. How clipped content arrives

- **Format**: `.md` files with YAML frontmatter
- **Extraction**: Mozilla Readability strips nav/footer/ads, keeps article content
- **Location**: configurable per-template via `path` field, or default folder
- **Metadata captured**: title, URL, author, published date, clip timestamp, Open Graph data, schema.org structured data

### Default frontmatter

```yaml
---
source: https://example.com/article
author: Author Name
clipped: 2026-04-14T15:30:00Z
published: 2026-04-10
tags: [clipping]
status: unread
---
```

---

## 2. Template system

Templates are JSON configs defining how content is captured, formatted, and saved.

### Template structure

```json
{
  "schemaVersion": "0.1.0",
  "name": "Template Name",
  "behavior": "create",
  "noteNameFormat": "{{title|safe_name}}",
  "path": "Clippings",
  "noteContentFormat": "# {{title}}\n\n{{content|markdown}}",
  "properties": [
    { "name": "source", "value": "{{url}}", "type": "text" },
    { "name": "clipped", "value": "{{date|date:YYYY-MM-DD}}", "type": "date" }
  ],
  "triggers": ["https://example.com", "/regex-pattern/"]
}
```

### Template fields

| Field | Purpose |
|---|---|
| `schemaVersion` | Format version (`"0.1.0"`) |
| `name` | Display name in extension |
| `behavior` | `create` (new note), `append` (add to existing), `daily` (add to daily note) |
| `noteNameFormat` | Filename pattern |
| `path` | Destination folder |
| `noteContentFormat` | Note body markdown |
| `properties` | Frontmatter array (name, value, type) |
| `triggers` | URL/regex patterns for auto-apply |

### Property types

`text`, `multitext`, `date`, `datetime`, `checkbox`, `number`

---

## 3. Template variables

### Preset variables (auto-extracted)

| Variable | Returns |
|---|---|
| `{{content}}` | Article content (or highlights if present, or selection) |
| `{{contentHtml}}` | Article HTML |
| `{{fullHtml}}` | Complete page HTML |
| `{{excerpt}}` | Meta description / excerpt |
| `{{title}}` | Page title |
| `{{author}}` | Article author |
| `{{url}}` | Current URL |
| `{{date}}` | Current timestamp (clip time) |
| `{{published}}` | Publication date |
| `{{highlights}}` | User-highlighted text |
| `{{siteTitle}}` | Website/domain name |
| `{{siteName}}` | Friendly site name |

### Meta variables (HTML meta tags)

```
{{meta:name:description}}
{{meta:name:author}}
{{meta:name:keywords}}
{{meta:property:og:title}}
{{meta:property:og:image}}
{{meta:property:og:description}}
```

### Selector variables (CSS selectors)

```
{{selector:.article-content}}          # text content
{{selector:.article-content?html}}     # HTML content
{{selector:img.hero?src}}              # attribute value
{{selectorHtml:.main-article}}         # HTML shorthand
```

### Schema.org variables (JSON-LD)

```
{{schema:@type}}
{{schema:author}}
{{schema:author[*].name}}        # all authors
{{schema:author[0].name}}        # first author
{{schema:datePublished}}
{{schema:keywords}}
{{schema:articleBody}}
```

### Prompt variables (AI Interpreter)

Natural language prompts processed by configured LLM:

```
{{"summarize in 2-3 sentences"}}
{{"extract 5 key takeaways"}}
{{"list main arguments"}}
{{"translate to Spanish"}}
{{"extract entities: people, orgs, places"}}
```

Requires Interpreter enabled + API key for Anthropic/OpenAI/Google/Ollama.

---

## 4. Filters

Chain with `|` pipe syntax:

| Filter | Purpose | Example |
|---|---|---|
| `markdown` | HTML to Markdown | `{{contentHtml\|markdown}}` |
| `lower` | Lowercase | `{{title\|lower}}` |
| `upper` | Uppercase | `{{title\|upper}}` |
| `safe_name` | Filename-safe | `{{title\|safe_name}}` |
| `capitalize` | Title case | `{{title\|capitalize}}` |
| `date:"FMT"` | Format date | `{{date\|date:"YYYY-MM-DD"}}` |
| `trim` | Strip whitespace | `{{title\|trim}}` |
| `truncate:N` | Truncate to N chars | `{{excerpt\|truncate:200}}` |
| `first_paragraphs:N` | First N paragraphs | `{{content\|first_paragraphs:2}}` |
| `slugify` | URL-friendly slug | `{{title\|slugify}}` |

**Chaining**: `{{title|lower|safe_name}}`

---

## 5. Trigger rules (auto-apply templates)

```
https://medium.com                         # simple URL match
/^https:\/\/www\.imdb\.com\/title\/tt\d+/  # regex (in slashes)
schema:@Recipe                             # schema.org type match
schema:@Article.author=John Doe            # schema.org field match
```

First matching trigger wins. Drag to reorder priority.

---

## 6. Interpreter (AI/LLM feature)

### Supported providers

| Provider | Recommended model | Notes |
|---|---|---|
| Anthropic | Claude Haiku (fast, cheap) | External API |
| OpenAI | GPT-4 Mini | External API |
| Google | Gemini Flash | Very fast, free tier |
| Ollama | Any local model | Fully private, free |

### Setup

1. Enable Interpreter in Web Clipper settings
2. Select provider, paste API key
3. Configure context scope (which page data AI can access)
4. Use `{{"prompt"}}` in templates

### Performance

5-30s depending on model and content length. Use small models (Haiku, Mini, Flash) for speed.

---

## 7. Raw inbox workflow

The pattern for LLM wiki vaults where Clipper drops raw content:

### Setup

1. Create inbox folder in vault (e.g., `raw/`)
2. Set default folder in Clipper settings to `raw/`
3. Create a "Quick Capture" template:

```json
{
  "schemaVersion": "0.1.0",
  "name": "Raw Capture",
  "behavior": "create",
  "noteNameFormat": "{{title|safe_name}}",
  "path": "raw",
  "noteContentFormat": "# {{title}}\n\n**Source**: {{url}}\n**Author**: {{author}}\n**Clipped**: {{date|date:YYYY-MM-DD}}\n\n---\n\n{{content|markdown}}",
  "properties": [
    { "name": "source", "value": "{{url}}", "type": "text" },
    { "name": "author", "value": "{{author}}", "type": "text" },
    { "name": "clipped", "value": "{{date|date:YYYY-MM-DD}}", "type": "date" },
    { "name": "status", "value": "unread", "type": "text" }
  ],
  "triggers": []
}
```

4. Processing: LLM reads from `raw/`, generates wiki pages in `wiki/`, updates index

### Site-specific templates

Create additional templates with triggers for specific sites (YouTube, GitHub, arXiv, etc.) that route to `raw/` with richer metadata extraction.

---

## 8. Highlighting

1. Click highlighter button in Clipper UI
2. Click/drag to select text, hover paragraphs to highlight whole sections
3. Highlighted text becomes `{{highlights}}` variable
4. Highlights persist across visits (stored in extension)
5. Export all highlights as JSON for backup

---

## 9. Community templates

Pre-built templates at [github.com/obsidian-community/web-clipper-templates](https://github.com/obsidian-community/web-clipper-templates).

Popular: YouTube (with transcript), Medium, GitHub releases, Goodreads, Twitter/X, academic papers.

**To use**: copy raw JSON from repo, paste into Web Clipper > Templates > New Template.
