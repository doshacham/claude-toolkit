# Excalidraw Plugin Reference

Plugin ID: `obsidian-excalidraw-plugin` by Zsolt Viczian.

**Docs**: [API docs](https://zsviczian.github.io/obsidian-excalidraw-plugin/), [Community wiki](https://excalidraw-obsidian.online/), [GitHub](https://github.com/zsviczian/obsidian-excalidraw-plugin)

---

## 1. File format: .excalidraw.md

The `.excalidraw.md` format is a dual markdown+JSON structure optimized for Obsidian integration. Incompatible with excalidraw.com but enables search, backlinks, and properties.

### Structure

```
---
[YAML Frontmatter]
---

[Optional Markdown Content — "back of the note"]

# Excalidraw Data
[LZ-String compressed JSON, chunked into 256-char lines]

# Element Properties
[Custom metadata for elements]

# Text Elements
[Searchable text content with block reference IDs]
Text content here ^block-id
Another element ^another-id

## Embedded Files
[[image.png]]
[[folder/icon.svg]]
```

### Frontmatter properties

| Property | Values | Purpose |
|---|---|---|
| `excalidraw-plugin` | `parsed` | Marks file as Excalidraw-managed |
| `tags` | `[excalidraw]` | Standard tagging |
| `excalidraw-export-transparent` | `true\|false` | Transparent background in exports |
| `excalidraw-export-dark` | `true\|false` | Dark mode export |
| `excalidraw-export-padding` | number | Pixel padding around export |
| `excalidraw-autoexport` | `none\|both\|png\|svg` | Auto-export trigger |
| `excalidraw-default-mode` | `view\|zen` | Default view when opened |
| `excalidraw-font` | `Virgil\|Cascadia\|custom.ttf` | Font selection |
| `excalidraw-font-color` | CSS color | Text color |
| `excalidraw-link-prefix` | string | Prefix for generated links |
| `excalidraw-url-prefix` | string | Icon for external URLs |
| `excalidraw-link-brackets` | `true\|false` | Use `[[]]` notation |

Custom YAML properties are preserved and can be used with Dataview.

### Compression

- LZ-String compression enabled by default (`compress` setting)
- Chunked into 256-char lines for git-friendly diffs
- `decompressForMDView`: auto-decompress when switching to Markdown view

### Text Elements section

Each text element appears as `text content ^element-id`. This enables:
- Obsidian search indexing of drawing text
- Block references: `![[drawing.excalidraw.md#^block-id]]`
- Transclusion from other notes

### Embedded Files section

Uses wikilink notation exclusively: `[[filename]]`. Must be wikilinks (not markdown links) for images to render in Excalidraw view.

---

## 2. ExcalidrawAutomate scripting API

Three integration methods: Script Engine, Templater, DataviewJS.

### Core workflow pattern

```javascript
const ea = ExcalidrawAutomate;
ea.reset();  // Always reset first

// Configure styling
ea.style.strokeColor = "red";
ea.style.fillStyle = "solid";

// Add elements (returns element ID)
const id1 = ea.addRect(-150, -50, 450, 300);
const id2 = ea.addText(0, 0, "Hello");

// Connect elements
ea.connectObjects(id1, id2, "arrow", {
  startPosition: "right", endPosition: "left"
});

// Create file or add to view
await ea.create({filename: "Drawing", foldername: "Drawings/"});
```

### Style properties

Set before adding elements; persist until changed.

```javascript
// Color
ea.style.strokeColor = "red" | "#FF0000"
ea.style.backgroundColor = "blue" | "transparent"

// Stroke
ea.style.strokeWidth = 1 | 2 | 4 | 8
ea.style.fillStyle = "hachure" | "cross-hatch" | "solid"
ea.style.strokeStyle = "solid" | "dashed" | "dotted"
ea.style.strokeSharpness = "round" | "sharp"

// Text
ea.style.fontFamily = "Virgil" | "Helvetica" | "Cascadia"
ea.style.fontSize = 20
ea.style.textAlign = "left" | "center" | "right"
ea.style.verticalAlign = "top" | "middle" | "bottom"

// Other
ea.style.opacity = 0-100
ea.style.angle = Math.PI/2  // radians
ea.style.roughness = "architect" | "artist" | "cartoonist"
ea.style.startArrowHead = "arrow" | "bar" | "dot" | "none"
ea.style.endArrowHead = "arrow" | "bar" | "dot" | "none"
```

### Canvas properties

```javascript
ea.canvas.theme = "light" | "dark"
ea.canvas.viewBackgroundColor = "#ffffff" | "transparent"
```

### Shape creation methods (all return element ID)

```javascript
ea.addRect(x, y, width, height)
ea.addDiamond(x, y, width, height)
ea.addEllipse(x, y, width, height)
ea.addLine([[x1,y1], [x2,y2], ...])
ea.addArrow([[x1,y1], [x2,y2], ...])
ea.addText(x, y, "Text content")
ea.addText(x, y, "Text", { width: 200, box: true })  // text with box
ea.connectObjects(id1, id2, "arrow", { startPosition: "top", endPosition: "bottom" })
```

Coordinate system: origin (0,0) = center of canvas. +X = right, +Y = down.

### View access (require targetView)

```javascript
ea.setView("first")  // "first", "last", or filename
const selected = ea.getViewSelectedElement()
const elements = ea.getViewElements()
await ea.addElementsToView(true, false)  // replace selected?, open if not focused?
```

### Output methods

```javascript
await ea.create({ filename: "Name", foldername: "Folder/", templateFile: "template.excalidraw.md" })
const svg = ea.createSVG()
const png = await ea.createPNG()
await ea.toClipboard()
```

---

## 3. Wikilink integration

### Linking from drawings

- Text elements can contain clickable links (stored in element `link` property in JSON)
- **Limitation**: These links do NOT appear in Obsidian's backlinks pane
- Only one `[[wikilink]]` per text element currently supported

### Embedding drawings in notes

```markdown
![[drawing.excalidraw.md]]           # full embed
![[drawing.excalidraw.md|width=400]] # sized embed
```

### Block references to drawing text

```markdown
![[drawing.excalidraw.md#^element-id]]  # transclude specific text element
```

### Graph view

Excalidraw files appear as nodes. Wikilink-based connections are visible in the graph.

---

## 4. Templater integration

```javascript
<%*
const ea = ExcalidrawAutomate;
ea.reset();
ea.style.strokeWidth = 2;
ea.addRect(0, 0, 100, 100);
ea.addText(10, 10, tp.file.title);
await ea.create({filename: tp.file.title + "_diagram"});
%>
```

## 5. DataviewJS integration

```javascript
const ea = ExcalidrawAutomate;
ea.reset();
const pages = dv.pages('"projects"').array();
let y = 0;
for (const page of pages) {
  ea.addText(0, y, page.file.name);
  y += 30;
}
await ea.createSVG();
```

---

## 6. Vault organization

**Recommended**: dedicated folder (e.g., `Drawings/`) or co-located with related notes. Name with prefixes for clarity: `flowchart_workflow.excalidraw.md`, `mindmap_architecture.excalidraw.md`.

**Assets**: store reusable icons/images in a subfolder, reference with `[[Assets/icon.svg]]`.

---

## 7. Settings (data.json)

Lives at `.obsidian/plugins/obsidian-excalidraw-plugin/data.json`.

Key settings:
- `compress`: boolean (default true) -- LZ-String compression
- `decompressForMDView`: boolean -- auto-decompress in markdown view
- Auto-export format, transparent bg, dark mode, padding
- Autosave: desktop 60s, mobile 30s
- Fourth font option (custom font)
- Script library activation

---

## 8. Key patterns

- **Workbench pattern**: elements are mutable in `elementsDict`, immutable in scene. Commit with `addElementsToView()` or `create()`.
- **Style persistence**: style properties stick until changed. Set color once, draw multiple shapes in that color.
- **ID-based connections**: shape methods return IDs. Use `connectObjects(id1, id2)` to draw arrows between shapes.

---

## 9. Common issues

| Problem | Cause | Fix |
|---|---|---|
| Images broken | Not using wikilinks | Use `[[file.png]]` in Embedded Files section |
| Links not in backlinks | Excalidraw-native links | Use wikilinks in text content instead |
| Performance slow | Large drawing | Enable compression, split into smaller drawings |
| Sync conflicts | Simultaneous edits | Wait for autosave before switching devices |
