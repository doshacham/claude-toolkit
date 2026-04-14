# Obsidian Markdown Syntax Reference

## Table of contents

1. Basic formatting
2. Callouts
3. Wikilinks
4. Embeds (transclusion)
5. Block references
6. Tags
7. Aliases
8. Comments

---

## 1. Basic formatting

Standard CommonMark plus extensions:

| Syntax | Result |
|---|---|
| `**bold**` or `__bold__` | Bold |
| `*italic*` or `_italic_` | Italic |
| `***bold italic***` | Bold italic |
| `~~strikethrough~~` | Strikethrough |
| `==highlight==` | Highlighted text |
| `` `code` `` | Inline code |
| ```` ```lang ```` | Fenced code block |
| `$e=mc^2$` | Inline math (MathJax) |
| `$$\int x\,dx$$` | Display math |
| `[^1]` + `[^1]: text` | Footnote |
| `^[inline footnote]` | Inline footnote |
| `---` or `***` or `___` | Horizontal rule |

**Tables**: standard GFM pipe syntax with alignment (`:---`, `:---:`, `---:`).

**Lists**: unordered with `-`, `*`, `+`; ordered with `1.`; tasks with `- [ ]` / `- [x]`.

---

## 2. Callouts

Blockquotes with a type identifier:

```markdown
> [!note] Optional Title
> Content goes here
```

**Built-in types**: `note`, `abstract` (aliases: `summary`, `tldr`), `info`, `todo`, `tip` (`hint`, `important`), `success` (`check`, `done`), `question` (`help`, `faq`), `warning` (`caution`, `attention`), `failure` (`fail`, `missing`), `danger` (`error`), `bug`, `example`, `quote` (`cite`).

**Foldable callouts**:
- `> [!tip]+ Title` -- expanded by default
- `> [!tip]- Title` -- collapsed by default

**Nested callouts**: add extra `>` levels:
```markdown
> [!question] Parent
> > [!todo] Child
```

---

## 3. Wikilinks

Default link format in Obsidian. Toggle in Settings > Files & Links > Use `[[Wikilinks]]`.

| Syntax | Links to |
|---|---|
| `[[Page Name]]` | Note by filename |
| `[[Page Name\|alias]]` | Note with custom display text |
| `[[Page#Heading]]` | Heading in a note |
| `[[Page#Heading\|alias]]` | Heading with alias |
| `[[Page#^block-id]]` | Block in a note |
| `[[#Heading]]` | Heading in current note |
| `[[#^block-id]]` | Block in current note |

Standard markdown links also work: `[text](Page%20Name.md)`, `[text](Page.md#Heading)`.

**Wikilinks vs markdown links**: wikilinks auto-update on rename and handle spaces natively. Markdown links are more portable to other editors but require URL-encoding and do not always update on rename.

**Unresolved links**: linking to a non-existent note creates an "unresolved link" (muted color). Clicking it creates the note.

---

## 4. Embeds (transclusion)

Prefix any internal link with `!`:

| Syntax | Embeds |
|---|---|
| `![[Note]]` | Full note |
| `![[Note#Heading]]` | Section under a heading |
| `![[Note#^block-id]]` | Single block |
| `![[image.png]]` | Image |
| `![[image.png\|300]]` | Image at 300px width |
| `![[image.png\|100x145]]` | Image at specific dimensions |
| `![[video.mp4]]` | Video |
| `![[audio.mp3]]` | Audio |
| `![[Document.pdf]]` | PDF |
| `![[Document.pdf#page=3]]` | PDF at specific page |

---

## 5. Block references

A block is a paragraph, list item, table, or other discrete chunk. To reference a block:

1. **Create a block ID** by appending `^block-id` at the end of the block (letters, numbers, dashes):
   ```
   This is a paragraph. ^my-block
   ```
2. **Link to it**: `[[Note#^my-block]]` or `![[Note#^my-block]]` for embed.
3. Typing `^` after `#` in a wikilink triggers block suggestions.

For list items, the ID goes at the end of the item line. For tables, put the ID on its own line after the table with blank lines around it.

---

## 6. Tags

| Syntax | Behavior |
|---|---|
| `#tag` | Inline tag |
| `#parent/child` | Nested tag (searching `#parent` matches all children) |
| Properties: `tags: [tag1, tag2]` | Tags in YAML frontmatter |

**Rules**: must contain at least one non-numeric character. Valid characters: letters, numbers, `_`, `-`, `/`. No spaces. Case-insensitive.

---

## 7. Aliases

Set in YAML frontmatter:
```yaml
---
aliases:
  - Short Name
  - Abbreviation
---
```

When linking via an alias, Obsidian rewrites `[[Short Name]]` to `[[Full Note Name|Short Name]]`. Aliases affect quick-switcher and link suggestions.

---

## 8. Comments

Hidden in reading view:

- Inline: `%%comment%%`
- Block:
  ```
  %%
  Multi-line comment
  hidden from preview
  %%
  ```
