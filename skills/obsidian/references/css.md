# Obsidian CSS Theming Reference

## Table of contents

1. Themes
2. CSS snippets
3. Key CSS variables
4. cssclasses property
5. Light/dark mode targeting
6. Snippet recipes

---

## 1. Themes

- **Install**: Settings > Appearance > Themes > Manage > browse community themes
- **Location**: `.obsidian/themes/<theme-name>/`
- **Files**: `theme.css` (required), `manifest.json` (`{name, version, minAppVersion, author}`)
- Only one theme active at a time. Active theme set in `appearance.json > cssTheme`.

---

## 2. CSS snippets

- **Location**: `.obsidian/snippets/*.css`
- **Enable**: Settings > Appearance > CSS snippets > toggle each file
- Snippets load **after** the theme (override it). Hot-reload on save.
- Active snippets listed in `appearance.json > enabledCssSnippets`.

---

## 3. Key CSS variables

Obsidian exposes hundreds of `--*` CSS custom properties. Override them in snippets or themes.

### Backgrounds
- `--background-primary` -- main editor/note area
- `--background-primary-alt` -- slightly darker variant
- `--background-secondary` -- sidebar background
- `--background-secondary-alt` -- secondary darker variant
- `--background-modifier-border` -- borders between panes
- `--background-modifier-hover` -- hover state

### Text
- `--text-normal` -- body text
- `--text-muted` -- secondary text (less emphasis)
- `--text-faint` -- tertiary text (least emphasis)
- `--text-on-accent` -- text on accent-colored backgrounds
- `--text-accent` -- accented inline text (links)

### Accent color
- `--accent-h` / `--accent-s` / `--accent-l` -- HSL components
- `--interactive-accent` -- buttons, toggles, active tabs
- `--interactive-hover` -- hover state of interactive elements

### Status colors
`--color-red`, `--color-orange`, `--color-yellow`, `--color-green`, `--color-cyan`, `--color-blue`, `--color-purple`, `--color-pink` (plus `-rgb` variants for alpha usage).

### Typography
- `--font-interface` -- UI font (menus, sidebars)
- `--font-text` -- note body font
- `--font-monospace` -- code blocks, inline code
- `--font-text-size` -- base font size
- `--font-normal` / `--font-medium` / `--font-semibold` / `--font-bold` -- weight values

### Layout
- `--file-line-width` -- readable line length (default ~700px)
- `--radius-s` / `--radius-m` / `--radius-l` / `--radius-xl` -- border radii

Full reference: https://docs.obsidian.md/Reference/CSS+variables/CSS+variables

---

## 4. cssclasses property

Set in YAML frontmatter to add CSS classes to the note's view container:

```yaml
---
cssclasses:
  - wide
  - hide-properties
  - custom-table
---
```

Obsidian adds each value as a class on `.markdown-source-view` and `.markdown-preview-view`, enabling per-note styling via snippets.

**Note**: `cssclasses` (plural) is the current reserved name. `cssclass` (singular) is deprecated since v1.9.

---

## 5. Light/dark mode targeting

```css
body.theme-dark {
  --background-primary: #1e1e1e;
  --text-normal: #d4d4d4;
}

body.theme-light {
  --background-primary: #ffffff;
  --text-normal: #333333;
}
```

---

## 6. Snippet recipes

### Wider editor (global)
```css
body {
  --file-line-width: 60rem;
}
```

### Wider editor (per-note via cssclass)
```css
.wide {
  --file-line-width: 60rem;
}
```
Use with `cssclasses: [wide]` in frontmatter.

### Custom callout styling
```css
.callout[data-callout="tip"] {
  --callout-color: 255, 121, 198;
  --callout-icon: lucide-sparkles;
}
```

### Hide properties section on specific notes
```css
.hide-properties {
  --metadata-display-reading: none;
  --metadata-display-editing: none;
}
```
Use with `cssclasses: [hide-properties]`.

### Compact sidebar
```css
.nav-file-title {
  font-size: 0.85em;
  padding: 2px 8px;
}
```
